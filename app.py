from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
# Permet d'importer `dash_anticipyr.*` même si `streamlit run` est lancé depuis `dash_anticipyr/`.
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dash_anticipyr.ui.map_section import render_map_section
from dash_anticipyr.ui.sidebar import render_sidebar
from dash_anticipyr.ui.ssp_info import render_ssp_info


def main() -> None:
    st.set_page_config(
        page_title="Flore Pyrénéenne — Habitats",
        page_icon="H",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.markdown(
        '<p class="main-title">Flore Pyrénéenne — Modélisation des Habitats</p>',
        unsafe_allow_html=True,
    )

    # Styles légers (optionnel)
    st.markdown(
        """
        <style>
            .main-title  { font-size:2rem; font-weight:700; color:#1b5e35; margin-bottom:0; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    espece, periode_label, periode_cle, ssp_choisi = render_sidebar()

    tab_carte, tab_ssp = st.tabs(["Carte", "SSPs"])

    with tab_carte:
        render_map_section(espece, periode_label, periode_cle, ssp_choisi)

    with tab_ssp:
        render_ssp_info()


if __name__ == "__main__":
    main()

