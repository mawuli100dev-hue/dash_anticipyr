# dash_anticipyr/core/raster.py

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

import cartopy.crs as ccrs
import cartopy.feature as cfeature


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
        fichier = f"{ssp_num}_{periode_cle}_median.tif"
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


def _ajouter_titre(fig, ax, espece: str, reste: str) -> None:
    """
    Affiche le titre de la carte avec deux styles différents :
    - Nom d'espece  : gras + italique  (convention botanique)
    - Reste du titre: gras uniquement

    Pourquoi deux ax.text et pas ax.set_title ?
    ax.set_title n'accepte qu'un seul style pour tout le texte.
    En plaçant deux Text côte à côte (ha="right" puis ha="left")
    au même point (0.5, 1.02), on simule un titre mixte.

    fontstyle='italic' + fontweight='bold' = gras italique garanti,
    contrairement à mathtext dont le gras ne fonctionne pas sur
    les lettres latines ordinaires.
    """
    y_titre = 1.02   # légèrement au-dessus des axes

    ax.text(
        0.5, y_titre, espece,
        transform=ax.transAxes,
        fontsize=13,
        fontweight="bold",
        fontstyle="italic",
        ha="right",
        va="bottom",
    )
    ax.text(
        0.5, y_titre, reste,
        transform=ax.transAxes,
        fontsize=13,
        fontweight="bold",
        fontstyle="normal",
        ha="left",
        va="bottom",
    )


def creer_figure(data: np.ndarray, bounds, titre: str, mode: str = "continu") -> plt.Figure:
    """
    Crée une figure cartographique avec Cartopy (projection PlateCarree).

    Pourquoi Cartopy ?
    - matplotlib seul affiche les pixels sans corriger le rapport lat/lon
    - A 43°N, 1° de longitude = ~81 km mais 1° de latitude = 111 km
    - Sans correction, la carte est aplatie horizontalement (~37% d'erreur)
    - Cartopy applique set_aspect('equal') dans l'espace géographique réel
    """

    proj = ccrs.PlateCarree()

    fig, ax = plt.subplots(
        figsize=(16, 9),
        subplot_kw={"projection": proj},
    )

    masked = np.ma.masked_invalid(data)

    ax.set_extent(
        [bounds.left, bounds.right, bounds.bottom, bounds.top],
        crs=proj,
    )

    ax.add_feature(cfeature.BORDERS, linewidth=0.6, edgecolor="#555555")
    ax.add_feature(cfeature.COASTLINE, linewidth=0.6, edgecolor="#555555")

    if mode == "continu":
        img = ax.imshow(
            masked,
            cmap="viridis",
            extent=[bounds.left, bounds.right, bounds.bottom, bounds.top],
            transform=proj,
            origin="upper",
            vmin=0.0,
            vmax=1.0,
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
            masked,
            cmap=cmap_bin,
            extent=[bounds.left, bounds.right, bounds.bottom, bounds.top],
            transform=proj,
            origin="upper",
            vmin=-0.5,
            vmax=1.5,
            interpolation="nearest",
        )
        cbar = fig.colorbar(img, ax=ax, fraction=0.012, pad=0.03, shrink=0.8, ticks=[0, 1])
        cbar.set_label("Favorable / Pas favorable", fontsize=11, labelpad=10)
        cbar.set_ticklabels(["Pas favorable (0)", "Favorable (1)"], fontsize=10)

    gl = ax.gridlines(
        draw_labels=True,
        linewidth=0.3,
        color="gray",
        alpha=0.5,
        linestyle="--",
    )
    gl.top_labels   = False
    gl.right_labels = False
    gl.xlabel_style = {"size": 9}
    gl.ylabel_style = {"size": 9}

    # ------------------------------------------------------------------
    # Titre : on coupe sur le premier "·" pour isoler le nom latin
    # Exemple : "Achillea chamaemelifolia · 2041-2060 | SSP 126"
    #   espece_part = "Achillea chamaemelifolia"   -> gras italique
    #   reste_part  = "  ·  2041-2060 | SSP 126"  -> gras normal
    # ------------------------------------------------------------------
    parties = titre.split("\u00b7", 1)   # séparateur ·
    if len(parties) == 2:
        espece_part = parties[0].strip()
        reste_part  = "  \u00b7" + parties[1]
    else:
        # Pas de · : on essaie avec le tiret central ·
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
