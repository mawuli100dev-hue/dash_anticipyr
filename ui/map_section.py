# dash_anticipyr/ui/map_section.py

from __future__ import annotations

import streamlit as st
from streamlit_folium import st_folium

from dash_anticipyr.core.carte_interactive import creer_carte_interactive
from dash_anticipyr.core.paths import data_cartographies_root
from dash_anticipyr.core.raster import (
    binariser_raster,
    charger_raster,
    construire_chemin,
    creer_figure_composite,
    figure_en_bytes,
)
from dash_anticipyr.core.inaturalist import get_infos_espece
from dash_anticipyr.core.constants import MODE_MAP, SEUIL_BINARISATION


def render_map_section(
    espece: str,
    periode_label: str,
    periode_cle: str,
    ssp_choisi: str | None,
    mode_visu: str,
) -> None:

    # ── 1. PHOTO iNaturalist ──────────────────────────────────────────────
    infos = get_infos_espece(espece)
    photo_url = infos["photo_url"]

    col_photo, col_info = st.columns([1, 3])

    with col_photo:
        if photo_url:
            st.markdown(
                f"""
                <img
                    src="{photo_url}"
                    width="400"
                    height="300"
                    style="object-fit:cover;border-radius:8px;"
                    alt="{espece}"
                />
                <p style="font-size:0.75rem;color:gray;margin-top:4px;">
                    <em>{espece}</em>
                </p>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.info("Aucune photo disponible sur iNaturalist.")

    with col_info:
        st.markdown(
            f"### *{espece}*\n"
            f"**Période :** {periode_label}  \n"
            f"**Scénario :** {ssp_choisi if ssp_choisi else 'Période actuelle'}"
        )

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

    # ── 3. PRÉPARATION ────────────────────────────────────────────────────
    mode_cle = MODE_MAP[mode_visu]
    data_affichee = data if mode_cle == "continu" else binariser_raster(data, mode_cle)

    if periode_cle == "current":
        titre_carte = f"{espece}  ·  Période actuelle (1970-2000)"
    else:
        titre_carte = f"{espece}  ·  {periode_label}  |  {ssp_choisi}"

    if mode_cle != "continu":
        titre_carte += f"  ·  {mode_visu}  (seuil = {SEUIL_BINARISATION})"

    # Carte interactive + figure composite créées avant l'affichage
    carte = creer_carte_interactive(data_affichee, bounds, titre_carte, mode=mode_cle)
    fig_composite = creer_figure_composite(data_affichee, bounds, titre_carte, mode=mode_cle)

    nom_fichier = (
        espece.replace(" ", "_")
        + "_"
        + periode_label
            .replace("–", "-")
            .replace(" ", "_")
            .replace("(", "")
            .replace(")", "")
    )
    if ssp_choisi:
        nom_fichier += "_" + ssp_choisi.replace(" ", "")

    # ── 4. CARTE INTERACTIVE ──────────────────────────────────────────────
    st_folium(
        carte,
        width="100%",
        height=550,
        returned_objects=[],
    )

    # ── 5. TÉLÉCHARGEMENTS sous la carte ─────────────────────────────────
    st.markdown("#### Télécharger la carte")
    dl1, dl2, dl3, dl4 = st.columns(4)

    with dl1:
        st.download_button(
            label="PNG",
            data=figure_en_bytes(fig_composite, "png"),
            file_name=f"{nom_fichier}.png",
            mime="image/png",
            use_container_width=True,
        )
    with dl2:
        st.download_button(
            label="JPG",
            data=figure_en_bytes(fig_composite, "jpeg"),
            file_name=f"{nom_fichier}.jpg",
            mime="image/jpeg",
            use_container_width=True,
        )
    with dl3:
        st.download_button(
            label="PDF",
            data=figure_en_bytes(fig_composite, "pdf"),
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
