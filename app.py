# dash_anticipyr/app.py

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dash_anticipyr.ui.app_style import inject_styles
from dash_anticipyr.ui.map_section import render_map_section
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

    st.markdown(
        "<p style='color:#6b7280;font-style:italic;margin-bottom:16px;'>"
        "Projection bioclimatique des espèces endémiques pyrénéennes</p>",
        unsafe_allow_html=True,
    )

    espece, periode_label, periode_cle, ssp_choisi, mode_visu = render_sidebar()

    tab_carte, tab_ssp = st.tabs(["Carte de distribution", "Scénarios SSP"])

    with tab_carte:
        render_map_section(espece, periode_label, periode_cle, ssp_choisi, mode_visu)

    with tab_ssp:
        render_ssp_info()


if __name__ == "__main__":
    main()
