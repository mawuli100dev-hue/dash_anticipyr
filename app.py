# dash_anticipyr/app.py

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

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

    st.markdown(
        """
        <style>
            /* ── Sous-titre ── */
            .main-subtitle {
                font-size: 0.85rem;
                color: #6b7280;
                margin-top: 0;
                margin-bottom: 1.2rem;
                font-style: italic;
            }

            /* ── Onglets ── */
            .stTabs [data-baseweb="tab-list"] {
                gap: 24px !important;
                padding-left: 0px !important;
                border-bottom: none !important;
                margin-bottom: 0 !important;
                justify-content: flex-start !important;
            }
            .stTabs [data-baseweb="tab"] {
                font-size: 1rem !important;
                font-weight: 600 !important;
                padding: 10px 32px !important;
                border-radius: 6px 6px 0 0 !important;
                color: #6b7280 !important;
                background-color: transparent !important;
                border: none !important;
                min-width: 180px !important;
                text-align: center !important;
            }
            .stTabs [aria-selected="true"] {
                color: #1b5e35 !important;
                border-bottom: 3px solid #1b5e35 !important;
                background-color: #f0faf3 !important;
            }
            .stTabs [data-baseweb="tab"]:hover {
                color: #1b5e35 !important;
                background-color: #f0faf3 !important;
            }

            /* ── Supprime les 2 traits gris sous les onglets ── */
            .stTabs [data-baseweb="tab-highlight"] {
                display: none !important;
            }
            .stTabs [data-baseweb="tab-border"] {
                display: none !important;
            }

            /* ── Sidebar ── */
            [data-testid="stSidebar"] {
                background-color: #f8faf9;
                border-right: 1px solid #e5e7eb;
            }

            /* ── Boutons de téléchargement ── */
            .stDownloadButton > button {
                border: 1px solid #1b5e35 !important;
                color: #1b5e35 !important;
                background-color: white !important;
                font-weight: 500 !important;
                border-radius: 6px !important;
            }
            .stDownloadButton > button:hover {
                background-color: #1b5e35 !important;
                color: white !important;
            }

            /* ── Header ── */
            [data-testid="stHeader"] {
                background-color: #ffffff !important;
                border-bottom: 1px solid #e5e7eb !important;
            }
            [data-testid="stHeader"]::before {
                content: "Flore Pyrénéenne - Simulation des Habitats";
                display: block;
                position: absolute;
                left: 1.5rem;
                top: 50%;
                transform: translateY(-50%);
                font-size: 1rem;
                font-weight: 700;
                color: #1b5e35;
                letter-spacing: 0.01em;
                white-space: nowrap;
            }
            [data-testid="stToolbar"] {
                display: none !important;
            }
            [data-testid="stDecoration"] {
                display: none !important;
            }

            /* ── Padding global ── */
            .block-container {
                padding-top: 4rem !important;
                padding-bottom: 2rem !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        "<p class=\"main-subtitle\">Projection bioclimatique des espèces endémiques pyrénéennes</p>",
        unsafe_allow_html=True,
    )

    espece, periode_label, periode_cle, ssp_choisi = render_sidebar()

    tab_carte, tab_ssp = st.tabs(["Carte de distribution", "Scenarios SSP"])

    with tab_carte:
        render_map_section(espece, periode_label, periode_cle, ssp_choisi)

    with tab_ssp:
        render_ssp_info()


if __name__ == "__main__":
    main()
