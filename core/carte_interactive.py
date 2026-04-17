# dash_anticipyr/core/carte_interactive.py

from __future__ import annotations

import base64
import io

import branca
import branca.element
import folium
import folium.raster_layers
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
import rasterio.coords

from dash_anticipyr.core.constants import SEUIL_BINARISATION

PYRENEES_BOUNDS = {
    "lat_min": 41.8,
    "lat_max": 43.5,
    "lon_min": -2.0,
    "lon_max": 3.5,
}


def _raster_vers_rgba(data: np.ndarray, mode: str) -> np.ndarray:
    if mode == "continu":
        cmap = plt.get_cmap("viridis")
        norm = mcolors.Normalize(vmin=0.0, vmax=1.0)
    elif mode == "absence":
        cmap = mcolors.ListedColormap(["#4393c3"])
        norm = mcolors.Normalize(vmin=0.0, vmax=1.0)
    elif mode == "presence":
        cmap = mcolors.ListedColormap(["#2e7d32"])
        norm = mcolors.Normalize(vmin=0.0, vmax=1.0)
    else:
        raise ValueError(f"mode inconnu : {mode}")

    nan_mask = np.isnan(data)
    data_clean = np.where(nan_mask, 0.0, data)
    rgba = cmap(norm(data_clean))
    rgba[nan_mask, 3] = 0.0
    rgba[~nan_mask, 3] = 0.75
    return (rgba * 255).astype(np.uint8)


def _rgba_vers_base64(rgba: np.ndarray) -> str:
    from PIL import Image
    img_pil = Image.fromarray(rgba, mode="RGBA")
    buf = io.BytesIO()
    img_pil.save(buf, format="PNG")
    buf.seek(0)
    return "data:image/png;base64," + base64.b64encode(buf.read()).decode()


def _creer_legende_html(mode: str) -> branca.element.MacroElement:
    if mode == "continu":
        corps = """
        <div style="display:flex;flex-direction:column;align-items:center;gap:2px;">
            <span style="font-size:11px;color:#333;">1.0 &mdash; Présent</span>
            <div style="
                width:18px;height:120px;
                background:linear-gradient(to bottom,
                    #fde725,#7ad151,#22a884,#2a788e,#414487,#440154);
                border:1px solid #ccc;border-radius:3px;">
            </div>
            <span style="font-size:11px;color:#333;">0.0 &mdash; Absent</span>
        </div>
        <div style="font-size:10px;text-align:center;margin-top:6px;color:#555;">
            Probabilité de présence
        </div>
        """
    elif mode == "absence":
        corps = f"""
        <div style="display:flex;align-items:center;gap:8px;">
            <div style="width:18px;height:18px;background:#4393c3;
                border:1px solid #ccc;border-radius:3px;"></div>
            <span style="font-size:11px;">Absence<br>(prob &lt; {SEUIL_BINARISATION})</span>
        </div>
        """
    else:
        corps = f"""
        <div style="display:flex;align-items:center;gap:8px;">
            <div style="width:18px;height:18px;background:#2e7d32;
                border:1px solid #ccc;border-radius:3px;"></div>
            <span style="font-size:11px;">Présence<br>(prob &ge; {SEUIL_BINARISATION})</span>
        </div>
        """

    html = f"""
    {{% macro html(this, kwargs) %}}
    <div style="
        position:fixed;bottom:30px;right:10px;z-index:1000;
        background:white;padding:10px 14px;border-radius:8px;
        box-shadow:0 2px 8px rgba(0,0,0,0.25);
        font-family:sans-serif;font-size:12px;min-width:130px;">
        <div style="font-weight:700;margin-bottom:6px;font-size:12px;color:#1b5e35;">
            Légende
        </div>
        {corps}
    </div>
    {{% endmacro %}}
    """
    legende = branca.element.MacroElement()
    legende._template = branca.element.Template(html)
    return legende


def creer_carte_interactive(
    data: np.ndarray,
    bounds: rasterio.coords.BoundingBox,
    titre: str,
    mode: str = "continu",
) -> folium.Map:
    centre_lat = (bounds.bottom + bounds.top) / 2
    centre_lon = (bounds.left + bounds.right) / 2

    carte = folium.Map(
        location=[centre_lat, centre_lon],
        zoom_start=8,
        min_zoom=7,
        max_bounds=True,
        tiles="OpenStreetMap",
    )

    carte.fit_bounds([
        [PYRENEES_BOUNDS["lat_min"], PYRENEES_BOUNDS["lon_min"]],
        [PYRENEES_BOUNDS["lat_max"], PYRENEES_BOUNDS["lon_max"]],
    ])

    rgba = _raster_vers_rgba(data, mode)
    image_b64 = _rgba_vers_base64(rgba)

    folium.raster_layers.ImageOverlay(
        image=image_b64,
        bounds=[[bounds.bottom, bounds.left], [bounds.top, bounds.right]],
        opacity=0.75,
        name=titre,
        interactive=False,
    ).add_to(carte)

    carte.add_child(_creer_legende_html(mode))
    folium.LayerControl().add_to(carte)

    return carte
