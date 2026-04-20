from __future__ import annotations

import streamlit as st
from streamlit_folium import st_folium

from dash_anticipyr.core.inaturalist import get_photo_espece
from dash_anticipyr.core.paths import data_cartographies_root
from dash_anticipyr.core.pdf import construire_nom_fichier
from dash_anticipyr.core.raster import (
    charger_raster,
    construire_chemin,
    creer_figure,
    creer_carte_folium,
    figure_en_bytes,
)


@st.cache_data(show_spinner="Génération de la carte export...")
def _bytes_export(chemin_str: str, titre: str, mode: str, fmt: str) -> bytes:
    """
    Génère et retourne les bytes d'export dans le format demandé.
    Cache basé sur : chemin TIF + titre + mode + format.
    Aucun objet Cartopy n'est mis en cache, seulement des bytes.
    """
    data, bounds = charger_raster(chemin_str)
    fig = creer_figure(data, bounds, titre, mode=mode)
    return figure_en_bytes(fig, fmt)


def render_map_section(
    espece: str,
    periode_label: str,
    periode_cle: str,
    ssp_choisi: str | None,
    mode_visu: str,
) -> None:
    """
    Rendu de la section carte - V2d.

    Correction par rapport à V2c :
    - Suppression du @st.cache_data sur la figure matplotlib (incompatible
      avec Cartopy CRS -> TypeError au pickle)
    - Cache déplacé sur _bytes_export() qui ne stocke que des bytes
    """
    PHOTO_WIDTH_PX = 400
    photo_url, attribution = get_photo_espece(espece)

    # ------------------------------------------------------------------
    # Bloc photo + infos espèce
    # ------------------------------------------------------------------
    if photo_url:
        col_photo, col_info = st.columns([1, 3])
        with col_photo:
            st.markdown(
                f'<img src="{photo_url}" width="{PHOTO_WIDTH_PX}" '
                f'style="border-radius:8px;max-width:100%;" '
                f'alt="{espece}"/>',
                unsafe_allow_html=True,
            )
            legende_html = f"<em>{espece}</em>"
            if attribution:
                auteur = attribution.lstrip("© ").lstrip("(c) ")
                legende_html += f" © {auteur}"
            st.markdown(
                f'<p style="font-size:0.75rem;color:#6b7280;margin-top:4px;">'
                f'{legende_html}</p>',
                unsafe_allow_html=True,
            )
        with col_info:
            st.markdown(
                f"<h3 style='margin-bottom:8px;'><em>{espece}</em></h3>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"**Période :** {periode_label}  \n"
                f"**Scénario :** {ssp_choisi if ssp_choisi else 'Période actuelle'}"
            )
    else:
        st.markdown(
            f"<h3 style='margin-bottom:8px;'><em>{espece}</em></h3>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"**Période :** {periode_label}  \n"
            f"**Scénario :** {ssp_choisi if ssp_choisi else 'Période actuelle'}"
        )
        st.info("Aucune photo disponible sur iNaturalist pour cette espèce.")

    st.divider()

    # ------------------------------------------------------------------
    # Résolution du chemin TIF
    # ------------------------------------------------------------------
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

    # ------------------------------------------------------------------
    # Chargement du raster
    # ------------------------------------------------------------------
    try:
        data, bounds = charger_raster(str(chemin_tif))
    except Exception as e:
        st.error(f"Erreur lors de la lecture du fichier TIF : \n`{e}`")
        st.stop()

    # ------------------------------------------------------------------
    # Titre pour les exports
    # ------------------------------------------------------------------
    if periode_cle == "current":
        titre_carte = f"{espece}  ·  Période actuelle (1970-2000)"
    else:
        titre_carte = f"{espece}  ·  {periode_label} | {ssp_choisi}"
    if est_binaire:
        titre_carte += "  ·  Absence/Présence"

    mode_figure = "binaire" if est_binaire else "continu"

    # ------------------------------------------------------------------
    # Sélecteur de fond de carte (radio Streamlit)
    # ------------------------------------------------------------------
    st.markdown("#### Carte interactive")

    col_fond, col_opacite = st.columns([1, 2])

    with col_fond:
        fond_choisi = st.radio(
            label="Fond de carte",
            options=["Plan", "Satellite"],
            index=0,
            horizontal=True,
            key=f"fond_carte_{espece}_{periode_cle}_{ssp_choisi}",
        )

    with col_opacite:
        opacite = st.slider(
            label="Opacité de la prédiction",
            min_value=0.0,
            max_value=1.0,
            value=0.7,          # valeur par défaut
            step=0.05,
            key=f"opacite_{espece}_{periode_cle}_{ssp_choisi}",
        )

    # ------------------------------------------------------------------
    # Carte Folium interactive - sans LayerControl
    # ------------------------------------------------------------------
    carte = creer_carte_folium(
        data,
        bounds,
        mode=mode_figure,
        fond=fond_choisi,
        opacite=opacite,      # nouveau paramètre
    )

    st.markdown(
        """
        <style>
        iframe[title="streamlit_folium.st_folium"] {
            border-radius: 12px;
            overflow: hidden;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st_folium(
        carte,
        use_container_width=True,
        height=600,
        returned_objects=[],
    )

    st.divider()

    # ------------------------------------------------------------------
    # Téléchargements
    # Les bytes sont mis en cache par _bytes_export()
    # La figure Cartopy est créée et détruite à l'intérieur de la
    # fonction, jamais exposée au système de cache de Streamlit
    # ------------------------------------------------------------------
    st.markdown("#### Télécharger la carte sélectionnée")

    nom_fichier = construire_nom_fichier(espece, periode_label, ssp_choisi, est_binaire)
    chemin_str  = str(chemin_tif)

    dl1, dl2, dl3, dl4 = st.columns(4)

    with dl1:
        st.download_button(
            label="PNG",
            data=_bytes_export(chemin_str, titre_carte, mode_figure, "png"),
            file_name=f"{nom_fichier}.png",
            mime="image/png",
            use_container_width=True,
        )
    with dl2:
        st.download_button(
            label="JPG",
            data=_bytes_export(chemin_str, titre_carte, mode_figure, "jpeg"),
            file_name=f"{nom_fichier}.jpg",
            mime="image/jpeg",
            use_container_width=True,
        )
    with dl3:
        st.download_button(
            label="PDF",
            data=_bytes_export(chemin_str, titre_carte, mode_figure, "pdf"),
            file_name=f"{nom_fichier}.pdf",
            mime="application/pdf",
            use_container_width=True,
        )
    with dl4:
        with open(chemin_tif, "rb") as f:
            tif_brut = f.read()
        st.download_button(
            label="TIF",
            data=tif_brut,
            file_name=f"{nom_fichier}.tif",
            mime="image/tiff",
            use_container_width=True,
        )
