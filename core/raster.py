from __future__ import annotations

import io
from pathlib import Path
from typing import Tuple

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import rasterio
import streamlit as st


@st.cache_data
def lister_especes(dossier_racine: str) -> list[str]:
    """
    Parcourt le dossier racine et retourne la liste triée
    des espèces (= sous-dossiers).
    """
    racine = Path(dossier_racine)
    if not racine.exists():
        return []
    return sorted([d.name for d in racine.iterdir() if d.is_dir()])


def construire_chemin(racine: Path, espece: str, periode_cle: str, ssp: str | None) -> Path:
    """
    Construit le chemin vers le fichier .tif selon les paramètres choisis.

    Exemples :
      - période actuelle -> <espece>/Median_current_projection.tif
      - 2021-2040, SSP126 -> <espece>/pred_maps_futur_2030/126_2030_median.tif
    """
    base = racine / espece
    if periode_cle == "current":
        return base / "Median_current_projection.tif"

    if not ssp:
        raise ValueError("`ssp` doit être renseigné pour une période future.")

    # "SSP 126" -> "126"
    ssp_num = ssp.replace("SSP ", "")
    dossier = f"pred_maps_futur_{periode_cle}"
    fichier = f"{ssp_num}_{periode_cle}_median.tif"
    return base / dossier / fichier


@st.cache_data
def charger_raster(chemin_tif: str) -> Tuple[np.ndarray, rasterio.coords.BoundingBox]:
    """
    Charge un raster GeoTIFF avec rasterio.
    Retourne :
      - data : tableau numpy 2D (valeurs entre 0 et 1)
      - bounds : étendue géographique
    """
    with rasterio.open(chemin_tif) as src:
        data = src.read(1).astype(float)
        bounds = src.bounds
        nodata = src.nodata

    if nodata is not None:
        data[data == nodata] = np.nan
    return data, bounds


def creer_figure(data: np.ndarray, bounds, titre: str) -> plt.Figure:
    """
    Crée la figure matplotlib de la carte de distribution.

    Légende basée sur la colorbar (elle est affichée directement sur la carte).
    """
    fig, ax = plt.subplots(figsize=(20, 12))

    masked = np.ma.masked_invalid(data)
    img = ax.imshow(
        masked,
        cmap="viridis",
        extent=[bounds.left, bounds.right, bounds.bottom, bounds.top],
        origin="upper",
        vmin=0.0,
        vmax=1.0,
        interpolation="nearest",
    )

    cbar = fig.colorbar(img, ax=ax, fraction=0.012, pad=0.03)
    cbar.set_label("Probabilité de présence", fontsize=11, labelpad=10)
    cbar.set_ticks([0.0, 0.25, 0.5, 0.75, 1.0])
    cbar.set_ticklabels(
        ["0.0\n(Absent)", "0.25", "0.50", "0.75", "1.0\n(Présent)"],
        fontsize=9,
    )

    ax.set_xlabel("Longitude (°)", fontsize=10)
    ax.set_ylabel("Latitude (°)", fontsize=10)
    ax.set_title(titre, fontsize=13, fontweight="bold", pad=12)
    ax.tick_params(labelsize=8)
    ax.grid(True, linewidth=0.3, alpha=0.4, color="white")

    fig.tight_layout()
    return fig


def figure_en_bytes(fig: plt.Figure, fmt: str, dpi: int = 150) -> bytes:
    """Convertit une figure matplotlib en flux d'octets (téléchargement)."""
    buf = io.BytesIO()
    fig.savefig(buf, format=fmt, dpi=dpi, bbox_inches="tight")
    buf.seek(0)
    return buf.read()

