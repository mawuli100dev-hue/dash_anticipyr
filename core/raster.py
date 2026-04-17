# dash_anticipyr/core/raster.py

from __future__ import annotations

import io
from pathlib import Path
from typing import Tuple

import matplotlib
matplotlib.use("Agg")

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
import rasterio
import rasterio.coords
import streamlit as st

from dash_anticipyr.core.constants import SEUIL_BINARISATION


@st.cache_data
def lister_especes(dossier_racine: str) -> list[str]:
    racine = Path(dossier_racine)
    if not racine.exists():
        return []
    return sorted([d.name for d in racine.iterdir() if d.is_dir()])


def construire_chemin(racine: Path, espece: str, periode_cle: str, ssp: str | None) -> Path:
    base = racine / espece
    if periode_cle == "current":
        return base / "Median_current_projection.tif"
    if not ssp:
        raise ValueError("`ssp` doit être renseigné pour une période future.")
    ssp_num = ssp.replace("SSP ", "")
    dossier = f"pred_maps_futur_{periode_cle}"
    fichier = f"{ssp_num}_{periode_cle}_median.tif"
    return base / dossier / fichier


@st.cache_data
def charger_raster(chemin_tif: str) -> Tuple[np.ndarray, rasterio.coords.BoundingBox]:
    with rasterio.open(chemin_tif) as src:
        data = src.read(1).astype(float)
        bounds = src.bounds
        nodata = src.nodata
    if nodata is not None:
        data[data == nodata] = np.nan
    return data, bounds


def binariser_raster(data: np.ndarray, mode: str, seuil: float = SEUIL_BINARISATION) -> np.ndarray:
    result = np.full_like(data, np.nan)
    if mode == "absence":
        result[data < seuil] = 0.0
    elif mode == "presence":
        result[data >= seuil] = 1.0
    return result


def creer_figure_composite(
    data: np.ndarray,
    bounds: rasterio.coords.BoundingBox,
    titre: str,
    mode: str = "continu",
    crs_source: str = "EPSG:4326",
) -> plt.Figure:
    """
    Figure matplotlib avec fond de carte OSM (contextily) + raster superposé.
    Si contextily est absent ou le réseau coupé, s'affiche sans fond.
    """
    fig, ax = plt.subplots(figsize=(20, 12))
    masked = np.ma.masked_invalid(data)

    if mode == "continu":
        cmap_plot: str | mcolors.Colormap = "viridis"
        vmin, vmax = 0.0, 1.0
    elif mode == "absence":
        cmap_plot = mcolors.ListedColormap(["#4393c3"])
        vmin, vmax = 0.0, 1.0
    else:  # presence
        cmap_plot = mcolors.ListedColormap(["#2e7d32"])
        vmin, vmax = 0.0, 1.0

    img = ax.imshow(
        masked,
        cmap=cmap_plot,
        extent=[bounds.left, bounds.right, bounds.bottom, bounds.top],
        origin="upper",
        vmin=vmin,
        vmax=vmax,
        interpolation="nearest",
        alpha=0.75,
        zorder=2,
    )

    try:
        import contextily as ctx
        ctx.add_basemap(
            ax,
            crs=crs_source,
            source=ctx.providers.OpenStreetMap.Mapnik,
            zoom="auto",
            zorder=1,
        )
    except Exception:
        pass

    if mode == "continu":
        cbar = fig.colorbar(img, ax=ax, fraction=0.012, pad=0.03)
        cbar.set_label("Probabilité de présence", fontsize=11, labelpad=10)
        cbar.set_ticks([0.0, 0.25, 0.5, 0.75, 1.0])
        cbar.set_ticklabels(
            ["0.0\n(Absent)", "0.25", "0.50", "0.75", "1.0\n(Présent)"],
            fontsize=9,
        )
    else:
        label = (
            f"Absence (prob < {SEUIL_BINARISATION})"
            if mode == "absence"
            else f"Présence (prob >= {SEUIL_BINARISATION})"
        )
        cbar = fig.colorbar(img, ax=ax, fraction=0.012, pad=0.03, ticks=[0.5])
        cbar.set_label(label, fontsize=11, labelpad=10)
        cbar.set_ticklabels(
            ["Absent"] if mode == "absence" else ["Présent"],
            fontsize=10,
        )

    ax.set_xlabel("Longitude (°)", fontsize=10)
    ax.set_ylabel("Latitude (°)", fontsize=10)
    ax.set_title(titre, fontsize=13, fontweight="bold", pad=12)
    ax.tick_params(labelsize=8)
    ax.grid(True, linewidth=0.3, alpha=0.4, color="gray")
    fig.tight_layout()
    return fig


def figure_en_bytes(fig: plt.Figure, fmt: str, dpi: int = 150) -> bytes:
    buf = io.BytesIO()
    fig.savefig(buf, format=fmt, dpi=dpi, bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return buf.read()
