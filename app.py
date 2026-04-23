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
from dash_anticipyr.core.session import generer_pdf_session
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

    espece, periode_label, periode_cle, ssp_choisi, mode_visu = render_sidebar()

    generer_pdf_session(espece, periode_label, periode_cle, ssp_choisi, mode_visu)

    st.markdown(
        f'<p class="main-subtitle">{t("main_subtitle")}</p>',
        unsafe_allow_html=True,
    )

    pdf_bytes = st.session_state.get("pdf_complet_bytes")
    nom_pdf = st.session_state.get("pdf_complet_nom", "export_complet.pdf")

    _, col_btn = st.columns([8, 1])

    with col_btn:
        if pdf_bytes is not None:
            st.download_button(
                label=t("btn_imprimer"),
                data=pdf_bytes,
                file_name=nom_pdf,
                mime="application/pdf",
                key="btn_imprimer_haut",
                help=t("btn_imprimer_help"),
                use_container_width=True,
            )
        else:
            st.button(
                t("btn_imprimer"),
                key="btn_imprimer_disabled",
                disabled=True,
                help=t("btn_imprimer_loading"),
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
