from __future__ import annotations

from pathlib import Path

import streamlit as st

from dash_anticipyr.core.paths import data_cartographies_root
from dash_anticipyr.core.raster import (
    charger_raster,
    construire_chemin,
    creer_figure,
    figure_en_bytes,
)
from dash_anticipyr.core.inaturalist import get_photo_espece  # ← import de ta fonction


def render_map_section(
    espece: str,
    periode_label: str,
    periode_cle: str,
    ssp_choisi: str | None,
) -> None:

    # ── 1. PHOTO iNaturalist ───────────────────────────────────────────────
    PHOTO_WIDTH_PX = 400
    PHOTO_HEIGHT_PX = 300

    photo_url = get_photo_espece(espece)

    if photo_url:
        col_photo, col_info = st.columns([1, 3])
        with col_photo:
            st.markdown(
                f"""
                <img
                    src="{photo_url}"
                    width="{PHOTO_WIDTH_PX}"
                    height="{PHOTO_HEIGHT_PX}"
                    style="object-fit: cover; border-radius: 8px;"
                    alt="{espece}"
                />
                <p style="font-size: 0.75rem; color: gray; margin-top: 4px;">
                    <em>{espece}</em>
                </p>
                """,
                unsafe_allow_html=True,
            )
        with col_info:
            st.markdown(
                f"### *{espece}*\n"
                f"**Période :** {periode_label}  \n"
                f"**Scénario :** {ssp_choisi if ssp_choisi else 'Période actuelle'}"
            )
    else:
        st.markdown(
            f"### *{espece}*\n"
            f"**Période :** {periode_label}  \n"
            f"**Scénario :** {ssp_choisi if ssp_choisi else 'Période actuelle'}"
        )
        st.info("Aucune photo disponible sur iNaturalist pour cette espèce.")

    st.divider()

    # ── 2. CHARGEMENT DU RASTER ───────────────────────────────────────────
    racine = data_cartographies_root()
    chemin_tif = construire_chemin(racine, espece, periode_cle, ssp_choisi)

    if not chemin_tif.exists():
        st.warning(
            f"**Fichier introuvable :**  \n`{chemin_tif}`  \n\n"
            "Vérifiez que les prédictions ont bien été générées pour cette combinaison."
        )
        st.stop()

    try:
        data, bounds = charger_raster(str(chemin_tif))
    except Exception as e:
        st.error(f"Erreur lors de la lecture du fichier TIF :  \n`{e}`")
        st.stop()

    # ── 3. CARTE ──────────────────────────────────────────────────────────
    if periode_cle == "current":
        titre_carte = f"{espece}  ·  Période actuelle (1970–2000)"
    else:
        titre_carte = f"{espece}  ·  {periode_label}  |  {ssp_choisi}"

    fig = creer_figure(data, bounds, titre_carte)
    st.pyplot(fig, use_container_width=True)

    # ── 4. TÉLÉCHARGEMENTS ────────────────────────────────────────────────
    st.markdown("#### Télécharger la carte sélectionnée")

    nom_fichier = (
        espece.replace(" ", "_")
        + "_"
        + periode_label.replace("–", "-").replace(" ", "_").replace("(", "").replace(")", "")
    )
    if ssp_choisi:
        nom_fichier += "_" + ssp_choisi.replace(" ", "")

    dl1, dl2, dl3, dl4 = st.columns(4)

    with dl1:
        st.download_button(
            label="PNG",
            data=figure_en_bytes(fig, "png"),
            file_name=f"{nom_fichier}.png",
            mime="image/png",
            use_container_width=True,
        )
    with dl2:
        st.download_button(
            label="JPG",
            data=figure_en_bytes(fig, "jpeg"),
            file_name=f"{nom_fichier}.jpg",
            mime="image/jpeg",
            use_container_width=True,
        )
    with dl3:
        st.download_button(
            label="PDF",
            data=figure_en_bytes(fig, "pdf"),
            file_name=f"{nom_fichier}.pdf",
            mime="application/pdf",
            use_container_width=True,
        )
    with dl4:
        with open(chemin_tif, "rb") as f:
            tif_brut = f.read()
        st.download_button(
            label="TIF (original)",
            data=tif_brut,
            file_name=f"{nom_fichier}.tif",
            mime="image/tiff",
            use_container_width=True,
        )
