# dash_anticipyr/ui/app_style.py

from __future__ import annotations

import streamlit as st


def inject_styles() -> None:
    """Injecte le CSS global de l'application."""
    st.markdown(
        """
        <style>
            /*  Sous-titre  */
            .main-subtitle {
                font-size: 0.85rem;
                color: #6b7280;
                margin-top: 0;
                margin-bottom: 1.2rem;
                font-style: italic;
            }

            /*  Onglets  */
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

            /*  Supprime les 2 traits gris sous les onglets  */
            .stTabs [data-baseweb="tab-highlight"] { display: none !important; }
            .stTabs [data-baseweb="tab-border"]    { display: none !important; }

            /*  Sidebar  */
            [data-testid="stSidebar"] {
                background-color: #f8faf9;
                border-right: 1px solid #e5e7eb;
            }

            /*  Boutons de téléchargement  */
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

            /*  Header  */
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
                font-size: 1.7rem;
                font-weight: 700;
                color: #1b5e35;
                letter-spacing: 0.01em;
                white-space: nowrap;
            }

            /*  Toolbar : cache les boutons internes SAUF le bouton sidebar  */
            [data-testid="stToolbar"] {
                background-color: transparent !important;
            }
            /* Cache le menu hamburger (3 points) et le bouton étoile */
            [data-testid="stToolbarActions"] {
                display: none !important;
            }
            /* Garde uniquement le bouton de toggle sidebar visible */
            [data-testid="stSidebarCollapsedControl"] {
                display: flex !important;
                z-index: 999 !important;
            }

            /*  Supprime la barre de décoration colorée en haut  */
            [data-testid="stDecoration"] { display: none !important; }

            /*  Padding global  */
            .block-container {
                padding-top: 4rem !important;
                padding-bottom: 2rem !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
