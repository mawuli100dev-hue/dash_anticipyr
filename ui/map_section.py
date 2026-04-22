# ui\map_section.py
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
from dash_anticipyr.core.translations import t, get_langue_courante


def _bytes_export(chemin_str: str, titre: str, mode: str, fmt: str, fond: str, langue: str, opacite: float) -> bytes:
    data, bounds = charger_raster(chemin_str)
    fig = creer_figure(data, bounds, titre, mode=mode, fond=fond, opacite=opacite)
    return figure_en_bytes(fig, fmt)


def render_map_section(
    espece: str,
    periode_label: str,
    periode_cle: str,
    ssp_choisi: str | None,
    mode_visu: str,
) -> None:
    PHOTO_WIDTH_PX = 400
    photo_url, attribution = get_photo_espece(espece)

    if photo_url:
        col_photo, col_info = st.columns([1, 3])
        with col_photo:
            st.markdown(
                f'<img src="{photo_url}" width="{PHOTO_WIDTH_PX}" '
                f'style="border-radius:8px;max-width:100%;" '
                f'alt="{espece}"/>',
                unsafe_allow_html=True,
            )
            legende_html = ""
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
                f"**{t('map_periode_label')} :** {periode_label}  \n"
                f"**{t('map_scenario_label')} :** "
                f"{ssp_choisi if ssp_choisi else t('map_periode_actuelle')}"
            )
    else:
        st.markdown(
            f"<h3 style='margin-bottom:8px;'><em>{espece}</em></h3>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"**{t('map_periode_label')} :** {periode_label}  \n"
            f"**{t('map_scenario_label')} :** "
            f"{ssp_choisi if ssp_choisi else t('map_periode_actuelle')}"
        )
        st.info(t("map_no_photo"))

    st.divider()

    est_binaire = mode_visu == t("mode_binaire")
    racine = data_cartographies_root()

    try:
        chemin_tif = construire_chemin(
            racine, espece, periode_cle, ssp_choisi, binaire=est_binaire
        )
    except ValueError as e:
        st.warning(str(e))
        return

    if not chemin_tif.exists():
        st.warning(t("map_fichier_introuvable", chemin=chemin_tif))
        st.stop()

    try:
        data, bounds = charger_raster(str(chemin_tif))
    except Exception as e:
        st.error(t("map_erreur_tif", e=e))
        st.stop()

    if periode_cle == "current":
        titre_carte = t("map_titre_carte_current", espece=espece)
    else:
        titre_carte = t(
            "map_titre_carte_futur",
            espece=espece,
            periode=periode_label,
            ssp=ssp_choisi,
        )
    if est_binaire:
        titre_carte += t("map_titre_binaire")

    mode_figure = "binaire" if est_binaire else "continu"

    st.markdown(f"#### {t('map_titre')}")

    col_fond, col_opacite = st.columns([1, 2])

    OPTIONS_FOND = {
        "plan": t("map_fond_plan"),
        "satellite": t("map_fond_satellite"),
    }

    with col_fond:
        fond_cle = st.radio(
            label=t("map_fond_label"),
            options=list(OPTIONS_FOND.keys()),
            format_func=lambda k: OPTIONS_FOND[k],
            index=0,
            horizontal=True,
            key=f"fond_carte_{espece}_{periode_cle}_{ssp_choisi}",
        )

    with col_opacite:
        opacite = st.slider(
            label=t("map_opacite_label"),
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.05,
            key=f"opacite_{espece}_{periode_cle}_{ssp_choisi}",
        )

    carte = creer_carte_folium(
        data,
        bounds,
        mode=mode_figure,
        fond=fond_cle,
        opacite=opacite,
        langue=get_langue_courante(),
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
        key=f"folium_{espece}_{periode_cle}_{ssp_choisi}_{mode_figure}_{fond_cle}_{get_langue_courante()}",
    )

    st.divider()

    st.markdown(f"#### {t('map_download_titre')}")

    nom_fichier = construire_nom_fichier(espece, periode_label, ssp_choisi, est_binaire)
    chemin_str = str(chemin_tif)
    langue = get_langue_courante()

    dl1, dl2, dl3, dl4 = st.columns(4)

    with dl1:
        with st.spinner(t("map_export_spinner")):
            png_data = _bytes_export(chemin_str, titre_carte, mode_figure, "png", fond_cle, langue, opacite)
        st.download_button(
            label="PNG",
            data=png_data,
            file_name=f"{nom_fichier}.png",
            mime="image/png",
            use_container_width=True,
        )

    with dl2:
        with st.spinner(t("map_export_spinner")):
            jpg_data = _bytes_export(chemin_str, titre_carte, mode_figure, "jpeg", fond_cle, langue, opacite)
        st.download_button(
            label="JPG",
            data=jpg_data,
            file_name=f"{nom_fichier}.jpg",
            mime="image/jpeg",
            use_container_width=True,
        )

    with dl3:
        with st.spinner(t("map_export_spinner")):
            pdf_data = _bytes_export(chemin_str, titre_carte, mode_figure, "pdf", fond_cle, langue, opacite)
        st.download_button(
            label="PDF",
            data=pdf_data,
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
