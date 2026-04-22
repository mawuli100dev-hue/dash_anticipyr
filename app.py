# app.py

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dash_anticipyr.ui.app_style import inject_styles
from dash_anticipyr.ui.map_section import render_map_section
from dash_anticipyr.core.session import generer_pdf_session, generer_pdf_espece_complet
from dash_anticipyr.ui.sidebar import render_sidebar
from dash_anticipyr.ui.ssp_info import render_ssp_info
from dash_anticipyr.ui.interpretation import render_interpretation
from dash_anticipyr.core.translations import init_langue, t


def main() -> None:
    init_langue()

    st.set_page_config(
        page_title=t("page_title"),
        page_icon="🌿",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    inject_styles()

    if "fond_carte" not in st.session_state:
        st.session_state["fond_carte"] = "plan"

    espece, periode_label, periode_cle, ssp_choisi, mode_visu = render_sidebar()

    fond_actuel = st.session_state.get("fond_carte", "plan")
    opacite_actuelle = st.session_state.get("opacite_carte", 0.7)

    # PDF scénario sélectionné
    generer_pdf_session(espece, periode_label, periode_cle, ssp_choisi, mode_visu, fond=fond_actuel, opacite=opacite_actuelle)

    # PDF fiche complète toutes périodes
    generer_pdf_espece_complet(espece, mode_visu, fond=fond_actuel, opacite=opacite_actuelle)

    st.markdown(
        f'<p class="main-subtitle">{t("main_subtitle")}</p>',
        unsafe_allow_html=True,
    )

    pdf_scenario_bytes = st.session_state.get("pdf_complet_bytes")
    pdf_scenario_nom   = st.session_state.get("pdf_complet_nom", "export_scenario.pdf")
    pdf_espece_bytes   = st.session_state.get("pdf_espece_bytes")
    pdf_espece_nom     = st.session_state.get("pdf_espece_nom", "export_espece_complet.pdf")

    _, col_btn1, col_btn2 = st.columns([5, 2, 2])

    with col_btn1:
        if pdf_scenario_bytes:
            st.download_button(
                label=t("btn_imprimer_scenario"),
                data=pdf_scenario_bytes,
                file_name=pdf_scenario_nom,
                mime="application/pdf",
                key="btn_scenario",
                help=t("btn_imprimer_help"),
                use_container_width=True,
            )
        else:
            st.button(
                t("btn_imprimer_scenario"),
                key="btn_scenario_off",
                disabled=True,
                use_container_width=True,
            )

    with col_btn2:
        if pdf_espece_bytes:
            st.download_button(
                label=t("btn_imprimer_complet"),
                data=pdf_espece_bytes,
                file_name=pdf_espece_nom,
                mime="application/pdf",
                key="btn_espece_complet",
                help=t("btn_imprimer_complet_help"),
                use_container_width=True,
            )
        else:
            st.button(
                t("btn_imprimer_complet"),
                key="btn_espece_complet_off",
                disabled=True,
                use_container_width=True,
            )

    tab_carte, tab_ssp, tab_interp = st.tabs([t("tab_carte"), t("tab_ssp"), "Interprétation"])

    with tab_carte:
        render_map_section(espece, periode_label, periode_cle, ssp_choisi, mode_visu)
    with tab_ssp:
        render_ssp_info()
    with tab_interp:
        render_interpretation()


if __name__ == "__main__":
    main()
