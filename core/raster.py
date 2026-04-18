# dash_anticypir/core/raster.py

from __future__ import annotations

import io
from pathlib import Path
from typing import Tuple

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import rasterio
import streamlit as st


@st.cache_data
def lister_especes(dossier_racine: str) -> list[str]:
    racine = Path(dossier_racine)
    if not racine.exists():
        return []
    return sorted([d.name for d in racine.iterdir() if d.is_dir()])


def construire_chemin(
    racine: Path, espece: str, periode_cle: str, ssp: str | None, binaire: bool = False
) -> Path:
    """
    Architecture réelle des données :

    CONTINU (binaire=False) :
        Présent -> {espece}/Median_current_projection.tif
        Futur   -> {espece}/pred_maps_futur_{periode}/{ssp_num}_{periode}_median.tif
                   ex: pred_maps_futur_2030/126_2030_median.tif
                   ATTENTION : les fichiers ._126_... sont des fichiers cachés
                   macOS (AppleDouble), ils ne contiennent pas de données raster.
                   On utilise uniquement les fichiers sans point devant.

    BINAIRE (binaire=True) :
        Présent -> {espece}/binarised_maps/pred_cond_median_binarised.tif
        Futur   -> {espece}/binarised_maps/model_{ssp_num}_{periode}_median_binarised.tif
                   ex: binarised_maps/model_126_2030_median_binarised.tif
    """
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
        # Vrai fichier raster : sans point devant (les ._xxx sont des fichiers cachés macOS)
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


def creer_figure(data: np.ndarray, bounds, titre: str, mode: str = "continu") -> plt.Figure:
    """
    mode : "continu" | "binaire"

    Continu : probabilités 0-1, colormap viridis
              0 = pas favorable, 1 = très favorable
    Binaire : valeurs déjà 0 ou 1 dans le raster (pas de seuil calculé)
              0 = pas favorable (bleu clair)
              1 = favorable (vert foncé)
    """
    fig, ax = plt.subplots(figsize=(20, 12))
    masked = np.ma.masked_invalid(data)

    if mode == "continu":
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
            ["0.0\n(Pas favorable)", "0.25", "0.50", "0.75", "1.0\n(Très favorable)"],
            fontsize=9,
        )

    elif mode == "binaire":
        # 2 couleurs : 0 = bleu (pas favorable), 1 = vert (favorable)
        # vmin=-0.5 / vmax=1.5 : chaque couleur est centrée sur sa valeur 0 ou 1
        cmap_bin = mcolors.ListedColormap(["#4393c3", "#2e7d32"])
        img = ax.imshow(
            masked,
            cmap=cmap_bin,
            extent=[bounds.left, bounds.right, bounds.bottom, bounds.top],
            origin="upper",
            vmin=-0.5,
            vmax=1.5,
            interpolation="nearest",
        )
        cbar = fig.colorbar(img, ax=ax, fraction=0.012, pad=0.03, ticks=[0, 1])
        cbar.set_label("Favorable / Pas favorable", fontsize=11, labelpad=10)
        cbar.set_ticklabels(["Pas favorable (0)", "Favorable (1)"], fontsize=10)

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
