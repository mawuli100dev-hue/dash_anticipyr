# dash_anticipyr/app.py

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dash_anticipyr.ui.app_style import inject_styles
from dash_anticipyr.ui.map_section import render_map_section, generer_pdf_session
from dash_anticipyr.ui.sidebar import render_sidebar
from dash_anticipyr.ui.ssp_info import render_ssp_info


def main() -> None:
    st.set_page_config(
        page_title="Flore Pyrénéenne - Habitats",
        page_icon="🌿",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    inject_styles()

    espece, periode_label, periode_cle, ssp_choisi, mode_visu = render_sidebar()

    generer_pdf_session(espece, periode_label, periode_cle, ssp_choisi, mode_visu)

    col_titre, col_btn = st.columns([8, 1])

    with col_titre:
        st.markdown(
            '<p class="main-subtitle">Projection bioclimatique des espèces endémiques pyrénéennes</p>',
            unsafe_allow_html=True,
        )

    with col_btn:
        pdf_bytes = st.session_state.get("pdf_complet_bytes")
        nom_pdf = st.session_state.get("pdf_complet_nom", "export_complet.pdf")

        if pdf_bytes is not None:
            st.download_button(
                label="Imprimer",
                data=pdf_bytes,
                file_name=nom_pdf,
                mime="application/pdf",
                key="btn_imprimer_haut",
                help="Télécharger la fiche PDF complète (photo + carte)",
                use_container_width=True,
            )
        else:
            st.button(
                "Imprimer",
                key="btn_imprimer_disabled",
                disabled=True,
                help="Chargement en cours...",
                use_container_width=True,
            )

    tab_carte, tab_ssp = st.tabs(["Carte de distribution", "Scenarios SSP"])

    with tab_carte:
        render_map_section(espece, periode_label, periode_cle, ssp_choisi, mode_visu)

    with tab_ssp:
        render_ssp_info()


if __name__ == "__main__":
    main()
