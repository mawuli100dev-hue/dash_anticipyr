from __future__ import annotations

import io
import base64
from pathlib import Path
from typing import Tuple

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import rasterio
import streamlit as st
from PIL import Image

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import folium


# ---------------------------------------------------------------------------
# Constantes pyrénéennes
# ---------------------------------------------------------------------------
PYRENEES_CENTER = [42.6, 0.7]
PYRENEES_BOUNDS = [[41.5, -2.5], [43.8, 4.0]]
MIN_ZOOM = 7
MAX_ZOOM = 16

# ---------------------------------------------------------------------------
# Utilitaires communs
# ---------------------------------------------------------------------------

@st.cache_data
def lister_especes(dossier_racine: str) -> list[str]:
    racine = Path(dossier_racine)
    if not racine.exists():
        return []
    return sorted([d.name for d in racine.iterdir() if d.is_dir()])


def construire_chemin(
    racine: Path, espece: str, periode_cle: str, ssp: str | None, binaire: bool = False
) -> Path:
    base = racine / espece

    if binaire:
        dossier_bin = base / "binarised_maps"
        if periode_cle == "current":
            return dossier_bin / "pred_cond_median_binarised.tif"
        if not ssp:
            raise ValueError("`ssp` doit être renseigné pour une période future.")
        ssp_num = ssp.replace("SSP ", "")
        fichier = f"model_{ssp_num}_{periode_cle}_median_binarised.tif"
        return dossier_bin / fichier
    else:
        if periode_cle == "current":
            return base / "Median_current_projection.tif"
        if not ssp:
            raise ValueError("`ssp` doit être renseigné pour une période future.")
        ssp_num = ssp.replace("SSP ", "")
        dossier = f"pred_maps_futur_{periode_cle}"
        fichier  = f"{ssp_num}_{periode_cle}_median.tif"
        return base / dossier / fichier


@st.cache_data
def charger_raster(chemin_tif: str) -> Tuple[np.ndarray, rasterio.coords.BoundingBox]:
    with rasterio.open(chemin_tif) as src:
        data   = src.read(1).astype(float)
        bounds = src.bounds
        nodata = src.nodata
        if nodata is not None:
            data[data == nodata] = np.nan
    return data, bounds


# ---------------------------------------------------------------------------
# V1 - Figure statique Cartopy (conservée uniquement pour les exports)
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


def creer_figure(data: np.ndarray, bounds, titre: str, mode: str = "continu") -> plt.Figure:
    """Figure statique Cartopy - conservée pour les exports PNG/JPG/PDF."""
    proj    = ccrs.PlateCarree()
    fig, ax = plt.subplots(figsize=(16, 9), subplot_kw={"projection": proj})
    masked  = np.ma.masked_invalid(data)

    ax.set_extent([bounds.left, bounds.right, bounds.bottom, bounds.top], crs=proj)
    ax.add_feature(cfeature.BORDERS,   linewidth=0.6, edgecolor="#555555")
    ax.add_feature(cfeature.COASTLINE, linewidth=0.6, edgecolor="#555555")

    if mode == "continu":
        img = ax.imshow(
            masked, cmap="viridis",
            extent=[bounds.left, bounds.right, bounds.bottom, bounds.top],
            transform=proj, origin="upper", vmin=0.0, vmax=1.0,
            interpolation="nearest",
        )
        cbar = fig.colorbar(img, ax=ax, fraction=0.012, pad=0.03, shrink=0.8)
        cbar.set_label("Probabilité de présence", fontsize=11, labelpad=10)
        cbar.set_ticks([0.0, 0.25, 0.5, 0.75, 1.0])
        cbar.set_ticklabels(
            ["0.0\n(Pas favorable)", "0.25", "0.50", "0.75", "1.0\n(Très favorable)"],
            fontsize=9,
        )
    elif mode == "binaire":
        cmap_bin = mcolors.ListedColormap(["#4393c3", "#2e7d32"])
        img = ax.imshow(
            masked, cmap=cmap_bin,
            extent=[bounds.left, bounds.right, bounds.bottom, bounds.top],
            transform=proj, origin="upper", vmin=-0.5, vmax=1.5,
            interpolation="nearest",
        )
        cbar = fig.colorbar(img, ax=ax, fraction=0.012, pad=0.03, shrink=0.8, ticks=[0, 1])
        cbar.set_label("Favorable / Pas favorable", fontsize=11, labelpad=10)
        cbar.set_ticklabels(["Pas favorable (0)", "Favorable (1)"], fontsize=10)

    gl = ax.gridlines(
        draw_labels=True, linewidth=0.3, color="gray", alpha=0.5, linestyle="--"
    )
    gl.top_labels   = False
    gl.right_labels = False
    gl.xlabel_style = {"size": 9}
    gl.ylabel_style = {"size": 9}

    parties = titre.split("\u00b7", 1)
    if len(parties) == 2:
        espece_part = parties[0].strip()
        reste_part  = "  \u00b7" + parties[1]
    else:
        parties = titre.split("·", 1)
        if len(parties) == 2:
            espece_part = parties[0].strip()
            reste_part  = "  ·" + parties[1]
        else:
            espece_part = titre
            reste_part  = ""

    _ajouter_titre(fig, ax, espece_part, reste_part)
    fig.tight_layout()
    return fig


def figure_en_bytes(fig: plt.Figure, fmt: str, dpi: int = 150) -> bytes:
    buf = io.BytesIO()
    fig.savefig(buf, format=fmt, dpi=dpi, bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return buf.read()


# ---------------------------------------------------------------------------
# V2 - Carte interactive Folium
# ---------------------------------------------------------------------------

def _raster_vers_image_rgba(data: np.ndarray, mode: str = "continu") -> Image.Image:
    """
    Convertit le raster numpy en image RGBA pour l'overlay Folium.
    NaN -> alpha=0 (transparent), valeur valide -> alpha=180 (70% opaque).
    Downsample automatique si > 1024 px de côté.
    """
    MAX_PIXELS = 1024
    h, w = data.shape
    if max(h, w) > MAX_PIXELS:
        step = max(h, w) // MAX_PIXELS + 1
        data = data[::step, ::step]
        h, w = data.shape

    rgba = np.zeros((h, w, 4), dtype=np.uint8)
    masque_valide = ~np.isnan(data)

    if mode == "continu":
        cmap     = plt.get_cmap("viridis")
        norm     = mcolors.Normalize(vmin=0.0, vmax=1.0)
        couleurs = cmap(norm(np.where(masque_valide, data, 0.0)))
    else:
        cmap     = mcolors.ListedColormap(["#4393c3", "#2e7d32"])
        norm     = mcolors.BoundaryNorm([-0.5, 0.5, 1.5], cmap.N)
        couleurs = cmap(norm(np.where(masque_valide, data, 0.0)))

    rgba[..., :3]           = (couleurs[..., :3] * 255).astype(np.uint8)
    rgba[masque_valide,  3] = 180
    rgba[~masque_valide, 3] = 0

    return Image.fromarray(rgba, mode="RGBA")


def creer_carte_folium(
    data: np.ndarray,
    bounds,
    mode: str = "continu",
    fond: str = "Plan",
    opacite: float = 0.7,     # nouveau paramètre
    ) -> folium.Map:

    # 1. Raster -> image PNG base64
    img_pil = _raster_vers_image_rgba(data, mode)
    buf     = io.BytesIO()
    img_pil.save(buf, format="PNG")
    img_b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    img_url = f"data:image/png;base64,{img_b64}"

    image_bounds = [
        [bounds.bottom, bounds.left],
        [bounds.top,    bounds.right],
    ]

    # 2. Carte de base sans tuile par défaut
    carte = folium.Map(
        location=PYRENEES_CENTER,
        zoom_start=9,
        min_zoom=MIN_ZOOM,
        max_zoom=MAX_ZOOM,
        max_bounds=True,
        max_bounds_viscosity=1.0,
        tiles=None,               # on ajoute les tuiles manuellement
        control_scale=True,
    )

    # 3. Fond de carte selon le choix radio
    if fond == "Plan":
        folium.TileLayer(
            tiles="OpenStreetMap",
            attr="OpenStreetMap contributors",
            min_zoom=MIN_ZOOM,
            max_zoom=MAX_ZOOM,
            overlay=False,
            control=False,        # pas de LayerControl
        ).add_to(carte)

    else:  # Satellite
        # Couche 1 : photo satellite
        folium.TileLayer(
            tiles=(
                "https://server.arcgisonline.com/ArcGIS/rest/services/"
                "World_Imagery/MapServer/tile/{z}/{y}/{x}"
            ),
            attr="Esri World Imagery",
            min_zoom=MIN_ZOOM,
            max_zoom=MAX_ZOOM,
            overlay=False,
            control=False,
        ).add_to(carte)

        # Couche 2 : labels transparents (villes, routes) par-dessus le satellite
        folium.TileLayer(
            tiles=(
                "https://server.arcgisonline.com/ArcGIS/rest/services/"
                "Reference/World_Reference_Overlay/MapServer/tile/{z}/{y}/{x}"
            ),
            attr="Esri World Reference Overlay",
            min_zoom=MIN_ZOOM,
            max_zoom=MAX_ZOOM,
            overlay=True,         # transparent, se superpose au satellite
            control=False,
        ).add_to(carte)

    # 4. Raster SDM - toujours visible, pas de LayerControl
    folium.raster_layers.ImageOverlay(
        image=img_url,
        bounds=image_bounds,
        opacity=opacite,
        interactive=False,
        cross_origin=False,
        zindex=2,
    ).add_to(carte)

    # 5. Vue initiale calée sur l'emprise du raster
    carte.fit_bounds(image_bounds)

    return carte
