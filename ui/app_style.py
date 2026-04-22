from __future__ import annotations

import streamlit as st

from dash_anticipyr.core.translations import t


def inject_styles() -> None:
    header_titre = t("page_title")

    st.markdown(
        f"""
        <style>
            /* Sous-titre */
            .main-subtitle {{
                font-size: 0.9rem !important;
                color: #6b7280;
                margin: 0;
                font-style: italic;
            }}

            /* Bouton Imprimer du haut uniquement */
            .st-key-btn_imprimer_haut button,
            .st-key-btn_imprimer_disabled button {{
                background-color: #1b5e35 !important;
                color: #ffffff !important;
                border: none !important;
                border-radius: 6px !important;
                font-size: 0.82rem !important;
                font-weight: 600 !important;
                width: 100% !important;
                transition: background-color 0.18s ease !important;
            }}

            .st-key-btn_imprimer_haut button:hover,
            .st-key-btn_imprimer_disabled button:hover {{
                background-color: #145228 !important;
                color: #ffffff !important;
            }}

            .st-key-btn_imprimer_haut button p,
            .st-key-btn_imprimer_disabled button p {{
                color: #ffffff !important;
            }}

            /* Les 4 boutons du bas : tous pareils */
            .stDownloadButton > button {{
                border: 1px solid #1b5e35 !important;
                color: #1b5e35 !important;
                background-color: #ffffff !important;
                font-weight: 500 !important;
                border-radius: 6px !important;
                transition: background-color 0.18s ease, color 0.18s ease !important;
            }}

            .stDownloadButton > button:hover {{
                background-color: #1b5e35 !important;
                color: #ffffff !important;
            }}

            .stDownloadButton > button p {{
                color: inherit !important;
            }}

            /* Onglets */
            .stTabs [data-baseweb="tab-list"] {{
                gap: 24px !important;
                padding-left: 0px !important;
                border-bottom: none !important;
                margin-bottom: 0 !important;
                justify-content: flex-start !important;
            }}

            .stTabs [data-baseweb="tab"] {{
                font-size: 1rem !important;
                font-weight: 600 !important;
                padding: 10px 32px !important;
                border-radius: 6px 6px 0 0 !important;
                color: #6b7280 !important;
                background-color: transparent !important;
                border: none !important;
                min-width: 180px !important;
                text-align: center !important;
            }}

            .stTabs [aria-selected="true"] {{
                color: #1b5e35 !important;
                border-bottom: 3px solid #1b5e35 !important;
                background-color: #f0faf3 !important;
            }}

            .stTabs [data-baseweb="tab"]:hover {{
                color: #1b5e35 !important;
                background-color: #f0faf3 !important;
            }}

            .stTabs [data-baseweb="tab-highlight"] {{
                display: none !important;
            }}

            .stTabs [data-baseweb="tab-border"] {{
                display: none !important;
            }}

            /* Sidebar */
            [data-testid="stSidebar"] {{
                background-color: #f8faf9;
                border-right: 1px solid #e5e7eb;
            }}

            /* Header */
            [data-testid="stHeader"] {{
                background-color: #ffffff !important;
                border-bottom: 1px solid #e5e7eb !important;
            }}

            [data-testid="stHeader"]::before {{
                content: "{header_titre}";
                display: block;
                position: absolute;
                left: 0;
                right: 0;
                top: 50%;
                transform: translateY(-50%);
                text-align: center;
                font-size: 1.7rem;
                font-weight: 700;
                color: #1b5e35;
                letter-spacing: 0.01em;
                white-space: nowrap;
            }}

            /* Cache les 3 points + Deploy */
            [data-testid="stToolbarActions"] {{
                display: none !important;
                visibility: hidden !important;
            }}

            #MainMenu {{
                display: none !important;
                visibility: hidden !important;
            }}

            /* Toggle sidebar toujours visible */
            [data-testid="stSidebarCollapsedControl"] {{
                display: flex !important;
                visibility: visible !important;
                opacity: 1 !important;
                z-index: 9999 !important;
            }}

            /* Barre de décoration */
            [data-testid="stDecoration"] {{
                display: none !important;
            }}

            /* Padding global */
            .block-container {{
                padding-top: 4rem !important;
                padding-bottom: 2rem !important;
            }}

            /* Impression */
            @media print {{
                [data-testid="stSidebar"] {{
                    display: none !important;
                }}

                [data-testid="stHeader"] {{
                    display: none !important;
                }}

                [data-testid="stDecoration"] {{
                    display: none !important;
                }}

                [data-testid="stToolbar"] {{
                    display: none !important;
                }}

                .block-container {{
                    padding-top: 0.5rem !important;
                }}
            }}

            /* Bouton d'impression : jamais de retour à la ligne */
            [data-testid="stDownloadButton"] button,
            [data-testid="stButton"] button {{
                white-space: nowrap !important;
                overflow: hidden;
                text-overflow: ellipsis;
                min-width: 0;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )
