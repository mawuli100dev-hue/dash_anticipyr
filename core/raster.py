from __future__ import annotations

import io
import os
import base64
import tempfile
from pathlib import Path
from typing import Tuple

import math

import matplotlib
matplotlib.use("Agg")

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
import rasterio
import rasterio.coords
import streamlit as st
from PIL import Image

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import contextily as ctx
import folium
import fiona
from shapely.geometry import shape
from folium.plugins import MiniMap

import boto3

from dash_anticipyr.core.translations import t

# ---------------------------------------------------------------------------
# Config B2
# ---------------------------------------------------------------------------
from dash_anticipyr.core.constants import B2_KEY_ID, B2_APPLICATION_KEY, B2_ENDPOINT, B2_BUCKET

SHAPEFILE_PYRENEES = Path(__file__).parent.parent / "data" / "border" / "polygon_PYRENEES.shp"

# ---------------------------------------------------------------------------
# Constantes pyrénéennes
# ---------------------------------------------------------------------------
PYRENEES_CENTER = [42.6, 0.7]
PYRENEES_BOUNDS = [[41.5, -2.5], [43.8, 4.0]]
MIN_ZOOM = 4
MAX_ZOOM = 16

_CTX_SOURCES = {
    "plan": ctx.providers.OpenStreetMap.Mapnik,
    "satellite": ctx.providers.Esri.WorldImagery,
}


def _get_s3():
    return boto3.client(
        "s3",
        endpoint_url=B2_ENDPOINT,
        aws_access_key_id=B2_KEY_ID,
        aws_secret_access_key=B2_APPLICATION_KEY,
    )


# ---------------------------------------------------------------------------
# Utilitaires communs — remplacent les fonctions basées sur Path local
# ---------------------------------------------------------------------------

@st.cache_data(ttl=30)
def lister_especes() -> list[str]:
    """
    Retourne la liste des espèces disponibles dans le bucket B2.
    Remplace l'ancienne version qui lisait un dossier local.
    """
    s3 = _get_s3()
    response = s3.list_objects_v2(Bucket=B2_BUCKET, Delimiter="/")
    prefixes = response.get("CommonPrefixes", [])
    return sorted([p["Prefix"].rstrip("/") for p in prefixes])


def construire_cle(
    espece: str, periode_cle: str, ssp: str | None, binaire: bool = False
) -> str:
    """
    Construit la clé B2 (chemin dans le bucket) d'un fichier raster.
    Remplace construire_chemin() qui retournait un Path local.
    """
    if binaire:
        if periode_cle == "current":
            return f"{espece}/binarised_maps/pred_cond_median_binarised.tif"
        if not ssp:
            raise ValueError(t("ssp_manquant"))
        ssp_num = ssp.replace("SSP ", "")
        return f"{espece}/binarised_maps/model_{ssp_num}_{periode_cle}_median_binarised.tif"
    else:
        if periode_cle == "current":
            return f"{espece}/Median_current_projection.tif"
        if not ssp:
            raise ValueError(t("ssp_manquant"))
        ssp_num = ssp.replace("SSP ", "")
        return f"{espece}/pred_maps_futur_{periode_cle}/{ssp_num}_{periode_cle}_median.tif"


@st.cache_data(ttl=600)
def charger_raster(cle_b2: str) -> Tuple[np.ndarray, rasterio.coords.BoundingBox]:
    """
    Télécharge un .tif depuis B2 et retourne (data, bounds).
    Remplace l'ancienne version qui lisait depuis un chemin local.
    """
    s3 = _get_s3()
    buf = io.BytesIO()
    s3.download_fileobj(B2_BUCKET, cle_b2, buf)
    buf.seek(0)
    with rasterio.open(buf) as src:
        data = src.read(1).astype(float)
        bounds = src.bounds
        nodata = src.nodata
        if nodata is not None:
            data[data == nodata] = np.nan
    return data, bounds


# ---------------------------------------------------------------------------
# Utilitaire shapefile Pyrénées (inchangé)
# ---------------------------------------------------------------------------

@st.cache_data
def _charger_geometries_pyrenees() -> list:
    if not SHAPEFILE_PYRENEES.exists():
        return []
    with fiona.open(str(SHAPEFILE_PYRENEES)) as src:
        return [shape(feat["geometry"]) for feat in src]


# ---------------------------------------------------------------------------
# V1 - Figure statique Cartopy (inchangée)
# ---------------------------------------------------------------------------

def _ajouter_titre(fig, ax, espece: str, reste: str) -> None:
    y_titre = 1.02
    ax.text(
        0.5, y_titre, espece,
        transform=ax.transAxes,
        fontsize=13, fontweight="bold", fontstyle="italic",
        ha="right", va="bottom",
    )
    ax.text(
        0.5, y_titre, reste,
        transform=ax.transAxes,
        fontsize=13, fontweight="bold", fontstyle="normal",
        ha="left", va="bottom",
    )


def creer_figure(
    data: np.ndarray,
    bounds,
    titre: str,
    mode: str = "continu",
    fond: str = "plan",
    opacite: float = 0.7,
) -> plt.Figure:

    data_proj = ccrs.PlateCarree()
    map_proj = ccrs.epsg(3857)

    lat_moy = (bounds.top + bounds.bottom) / 2.0
    ratio_geo = (
        (bounds.right - bounds.left) * math.cos(math.radians(lat_moy))
    ) / (bounds.top - bounds.bottom)
    largeur_fig = 16
    hauteur_fig = largeur_fig / ratio_geo

    fig, ax = plt.subplots(figsize=(largeur_fig, hauteur_fig), subplot_kw={"projection": map_proj})
    masked = np.ma.masked_invalid(data)

    ax.set_extent([bounds.left, bounds.right, bounds.bottom, bounds.top], crs=data_proj)

    try:
        source = _CTX_SOURCES.get(fond, ctx.providers.OpenStreetMap.Mapnik)
        ctx.add_basemap(ax, crs="EPSG:3857", source=source, zoom="auto", attribution=False)
    except Exception as e:
        import sys
        print(f"[WARN] basemap échoué : {type(e).__name__}: {e}", file=sys.stderr)

    ax.add_feature(cfeature.BORDERS, linewidth=0.6, edgecolor="#555555")
    ax.add_feature(cfeature.COASTLINE, linewidth=0.6, edgecolor="#555555")

    if mode == "continu":
        img = ax.imshow(
            masked, cmap="viridis",
            extent=[bounds.left, bounds.right, bounds.bottom, bounds.top],
            transform=data_proj, origin="upper", vmin=0.0, vmax=1.0,
            interpolation="nearest", alpha=opacite, zorder=5,
        )
        cbar = fig.colorbar(img, ax=ax, fraction=0.012, pad=0.03, shrink=0.8)
        cbar.set_label(t("cbar_continu_label"), fontsize=11, labelpad=10)
        cbar.set_ticks([0.0, 0.25, 0.5, 0.75, 1.0])
        cbar.set_ticklabels(
            [t("cbar_continu_min"), "0.25", "0.50", "0.75", t("cbar_continu_max")], fontsize=9,
        )
    elif mode == "binaire":
        cmap_bin = mcolors.ListedColormap(["#4393c3", "#f0c92b"])
        img = ax.imshow(
            masked, cmap=cmap_bin,
            extent=[bounds.left, bounds.right, bounds.bottom, bounds.top],
            transform=data_proj, origin="upper", vmin=-0.5, vmax=1.5,
            interpolation="nearest", alpha=opacite, zorder=5,
        )
        cbar = fig.colorbar(img, ax=ax, fraction=0.012, pad=0.03, shrink=0.8, ticks=[0, 1])
        cbar.set_label(t("cbar_binaire_label"), fontsize=11, labelpad=10)
        cbar.set_ticklabels([t("cbar_binaire_0"), t("cbar_binaire_1")], fontsize=10)

    gl = ax.gridlines(draw_labels=True, linewidth=0.3, color="gray", alpha=0.5, linestyle="--")
    gl.top_labels = False
    gl.right_labels = False
    gl.xlabel_style = {"size": 9}
    gl.ylabel_style = {"size": 9}

    geometries = _charger_geometries_pyrenees()
    if geometries:
        ax.add_geometries(
            geometries, crs=data_proj,
            facecolor="none", edgecolor="red", linewidth=1.5, zorder=10,
        )

    parties = titre.split("·", 1)
    if len(parties) == 2:
        espece_part = parties[0].strip()
        reste_part = "  ·" + parties[1]
    else:
        parties = titre.split("·", 1)
        if len(parties) == 2:
            espece_part = parties[0].strip()
            reste_part = "  ·" + parties[1]
        else:
            espece_part = titre
            reste_part = ""

    _ajouter_titre(fig, ax, espece_part, reste_part)
    fig.tight_layout(pad=1.5)
    return fig


def figure_en_bytes(fig: plt.Figure, fmt: str, dpi: int = 150) -> bytes:
    buf = io.BytesIO()
    fig.savefig(buf, format=fmt, dpi=dpi)
    plt.close(fig)
    buf.seek(0)
    return buf.read()


# ---------------------------------------------------------------------------
# V2 - Carte interactive Folium (inchangée)
# ---------------------------------------------------------------------------

def _raster_vers_image_rgba(data: np.ndarray, mode: str = "continu") -> Image.Image:
    MAX_PIXELS = 1024
    h, w = data.shape
    if max(h, w) > MAX_PIXELS:
        step = max(h, w) // MAX_PIXELS + 1
        data = data[::step, ::step]
        h, w = data.shape

    rgba = np.zeros((h, w, 4), dtype=np.uint8)
    masque_valide = ~np.isnan(data)

    if mode == "continu":
        cmap = plt.get_cmap("viridis")
        norm = mcolors.Normalize(vmin=0.0, vmax=1.0)
        couleurs = cmap(norm(np.where(masque_valide, data, 0.0)))
    else:
        cmap = mcolors.ListedColormap(["#4393c3", "#f0c92b"])
        norm = mcolors.BoundaryNorm([-0.5, 0.5, 1.5], cmap.N)
        couleurs = cmap(norm(np.where(masque_valide, data, 0.0)))

    rgba[..., :3] = (couleurs[..., :3] * 255).astype(np.uint8)
    rgba[masque_valide, 3] = 255
    rgba[~masque_valide, 3] = 0
    return Image.fromarray(rgba, mode="RGBA")


def _html_legende_continu(titre: str, label_min: str, label_max: str) -> str:
    return f"""
    <div style="position:fixed; bottom:30px; right:10px; z-index:1000;
        background:white; border-radius:6px; padding:12px 16px;
        box-shadow:0 2px 8px rgba(0,0,0,0.25); font-family:sans-serif;
        font-size:12px; min-width:180px;">
        <div style="font-weight:700; margin-bottom:8px; color:#333; font-size:13px;">{titre}</div>
        <div style="width:140px; height:14px; border-radius:3px;
            background:linear-gradient(to right,#440154,#31688e,#35b779,#fde725);
            border:1px solid #ccc;"></div>
        <div style="display:flex; justify-content:space-between; width:140px; margin-top:3px;">
            <span style="color:#555;">0</span><span style="color:#555;">0.25</span>
            <span style="color:#555;">0.50</span><span style="color:#555;">0.75</span>
            <span style="color:#555;">1</span>
        </div>
        <div style="display:flex; justify-content:space-between; width:140px; margin-top:2px;">
            <span style="color:#888; font-size:10px; max-width:60px; line-height:1.2;">{label_min}</span>
            <span style="color:#888; font-size:10px; max-width:60px; text-align:right; line-height:1.2;">{label_max}</span>
        </div>
    </div>
    """


def _html_legende_binaire(titre: str, label_0: str, label_1: str) -> str:
    return f"""
    <div style="position:fixed; bottom:30px; right:10px; z-index:1000;
        background:white; border-radius:6px; padding:10px 14px;
        box-shadow:0 2px 8px rgba(0,0,0,0.25); font-family:sans-serif;
        font-size:12px; min-width:160px;">
        <div style="font-weight:700; margin-bottom:8px; color:#333;">{titre}</div>
        <div style="display:flex; align-items:center; gap:8px; margin-bottom:5px;">
            <div style="width:16px; height:16px; background:#4393c3; border-radius:3px; border:1px solid #ccc; flex-shrink:0;"></div>
            <span style="color:#555;">{label_0}</span>
        </div>
        <div style="display:flex; align-items:center; gap:8px;">
            <div style="width:16px; height:16px; background:#f0c92b; border-radius:3px; border:1px solid #ccc; flex-shrink:0;"></div>
            <span style="color:#555;">{label_1}</span>
        </div>
    </div>
    """


def creer_carte_folium(
    data: np.ndarray,
    bounds,
    mode: str = "continu",
    fond: str = "plan",
    opacite: float = 0.7,
    langue: str = "fr",
) -> folium.Map:

    if mode == "continu":
        html_leg = _html_legende_continu(
            titre=t("legende_continu_titre"),
            label_min=t("legende_continu_min").replace("\n", "<br>"),
            label_max=t("legende_continu_max").replace("\n", "<br>"),
        )
    else:
        html_leg = _html_legende_binaire(
            titre=t("legende_binaire_titre"),
            label_0=t("legende_binaire_0"),
            label_1=t("legende_binaire_1"),
        )

    img_pil = _raster_vers_image_rgba(data, mode)
    buf = io.BytesIO()
    img_pil.save(buf, format="PNG")
    img_b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    img_url = f"data:image/png;base64,{img_b64}"

    image_bounds = [[bounds.bottom, bounds.left], [bounds.top, bounds.right]]

    carte = folium.Map(
        location=PYRENEES_CENTER, zoom_start=9,
        min_zoom=MIN_ZOOM, max_zoom=MAX_ZOOM,
        max_bounds=True, max_bounds_viscosity=1.0,
        tiles=None, control_scale=True,
    )

    if fond == "plan":
        folium.TileLayer(
            tiles="OpenStreetMap", attr="OpenStreetMap contributors",
            min_zoom=MIN_ZOOM, max_zoom=MAX_ZOOM, overlay=False, control=False,
        ).add_to(carte)
    else:
        folium.TileLayer(
            tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
            attr="Esri World Imagery", min_zoom=MIN_ZOOM, max_zoom=MAX_ZOOM,
            overlay=False, control=False,
        ).add_to(carte)
        folium.TileLayer(
            tiles="https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Reference_Overlay/MapServer/tile/{z}/{y}/{x}",
            attr="Esri World Reference Overlay", min_zoom=MIN_ZOOM, max_zoom=MAX_ZOOM,
            overlay=True, control=False,
        ).add_to(carte)

    folium.raster_layers.ImageOverlay(
        image=img_url, bounds=image_bounds,
        opacity=opacite, interactive=False, cross_origin=False, zindex=2,
    ).add_to(carte)

    geometries = _charger_geometries_pyrenees()
    if geometries:
        geojson_data = {
            "type": "FeatureCollection",
            "features": [
                {"type": "Feature", "geometry": geom.__geo_interface__, "properties": {}}
                for geom in geometries
            ],
        }
        folium.GeoJson(
            geojson_data, name="Pyrénées",
            style_function=lambda _: {"fillColor": "none", "color": "red", "weight": 2, "fillOpacity": 0},
        ).add_to(carte)

    carte.get_root().html.add_child(folium.Element(html_leg))

    reset_btn_html = f"""
    <div style="position:absolute; top:10px; right:10px; z-index:1000;">
        <button onclick="
            var map = Object.values(window)[
                Object.keys(window).findIndex(k => window[k] && window[k]._leaflet_id)
            ];
            map.flyTo([{PYRENEES_CENTER[0]}, {PYRENEES_CENTER[1]}], 9, {{duration: 1.2}});
        "
        style="background:white; border:2px solid #ccc; border-radius:6px;
            padding:6px 10px; cursor:pointer; font-size:13px; font-weight:600;
            color:#333; box-shadow:0 2px 6px rgba(0,0,0,0.2);"
        title="">
            {t("btn_recentrer")}
        </button>
    </div>
    """
    carte.get_root().html.add_child(folium.Element(reset_btn_html))
    carte.fit_bounds(image_bounds)
    return carte
