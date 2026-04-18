# dash_anticipyr/ui/map_section.py

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
from dash_anticipyr.core.inaturalist import get_photo_espece


def render_map_section(
    espece: str,
    periode_label: str,
    periode_cle: str,
    ssp_choisi: str | None,
    mode_visu: str,
) -> None:

    # ── 1. PHOTO iNaturalist ──────────────────────────────────────────
    PHOTO_WIDTH_PX  = 400
    PHOTO_HEIGHT_PX = 300

    photo_url, attribution = get_photo_espece(espece)

    if photo_url:
        col_photo, col_info = st.columns([1, 3])

        with col_photo:
            # Affiche la photo
            st.markdown(
                f'<img src="{photo_url}" width="{PHOTO_WIDTH_PX}" '
                f'style="border-radius:8px;max-width:100%;" '
                f'alt="{espece}"/>',
                unsafe_allow_html=True,
            )
            # Légende : nom en italique + copyright sur deux lignes
            legende_html = f"<em>{espece}</em>"
            if attribution:
                auteur = attribution.lstrip("© ").lstrip("(c) ")
                legende_html += f"<br>© {auteur}"
            st.markdown(
                f'<p style="font-size:0.75rem;color:#6b7280;margin-top:4px;">'
                f'{legende_html}</p>',
                unsafe_allow_html=True,
            )

        with col_info:
            # Titre principal : nom en italique
            st.markdown(
                f"<h3 style='margin-bottom:8px;'>"
                f"<em>{espece}</em>"
                f"</h3>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"**Période :** {periode_label}  \n"
                f"**Scénario :** {ssp_choisi if ssp_choisi else 'Période actuelle'}"
            )

    else:
        # Pas de photo : titre seul
        st.markdown(
            f"<h3 style='margin-bottom:8px;'>"
            f"<em>{espece}</em>"
            f"</h3>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"**Période :** {periode_label}  \n"
            f"**Scénario :** {ssp_choisi if ssp_choisi else 'Période actuelle'}"
        )
        st.info("Aucune photo disponible sur iNaturalist pour cette espèce.")

    st.divider()

    # ── 2. CONSTRUCTION DU CHEMIN RASTER ─────────────────────────────
    est_binaire = (mode_visu == "Absence/Présence")
    racine = data_cartographies_root()

    try:
        chemin_tif = construire_chemin(
            racine, espece, periode_cle, ssp_choisi, binaire=est_binaire
        )
    except ValueError as e:
        st.warning(str(e))
        return

    if not chemin_tif.exists():
        st.warning(
            f"**Fichier introuvable :** \n`{chemin_tif}` \n\n"
            "Vérifiez que les prédictions ont bien été générées pour cette combinaison."
        )
        st.stop()

    # ── 3. CHARGEMENT DU RASTER ──────────────────────────────────────
    try:
        data, bounds = charger_raster(str(chemin_tif))
    except Exception as e:
        st.error(f"Erreur lors de la lecture du fichier TIF : \n`{e}`")
        st.stop()

    # ── 4. TITRE ET FIGURE ───────────────────────────────────────────
    # Le titre de la carte Matplotlib reste en texte normal (pas de HTML ici)
    if periode_cle == "current":
        titre_carte = f"{espece}  ·  Période actuelle (1970-2000)"
    else:
        titre_carte = f"{espece}  ·  {periode_label} | {ssp_choisi}"
    if est_binaire:
        titre_carte += "  ·  Absence/Présence"

    mode_figure = "binaire" if est_binaire else "continu"
    fig = creer_figure(data, bounds, titre_carte, mode=mode_figure)
    st.pyplot(fig, use_container_width=True)

    # ── 5. TÉLÉCHARGEMENTS ───────────────────────────────────────────
    st.markdown("#### Télécharger la carte sélectionnée")

    nom_fichier = (
        espece.replace(" ", "_")
        + "_"
        + periode_label.replace("–", "-").replace(" ", "_").replace("(", "").replace(")", "")
    )
    if ssp_choisi:
        nom_fichier += "_" + ssp_choisi.replace(" ", "")
    if est_binaire:
        nom_fichier += "_absence_presence"

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
