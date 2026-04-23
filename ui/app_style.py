from __future__ import annotations

import streamlit as st

from dash_anticipyr.core.translations import t


def inject_styles() -> None:
    header_titre = t("page_title")
    toggle_label = t("sidebar_toggle_label")

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

            /* Texte toujours visible à droite de l'icône sidebar */
            .sidebar-toggle-label {{
                position: fixed;
                top: 0.95rem;
                left: 3.6rem;
                z-index: 99999;
                font-size: 0.72rem;
                font-weight: 600;
                color: #1b5e35;
                background: rgba(240, 250, 243, 0.98);
                border: 1px solid #d1e7d6;
                border-radius: 8px;
                padding: 4px 10px;
                line-height: 1.1;
                white-space: nowrap;
                pointer-events: none;
                box-shadow: 0 1px 2px rgba(0, 0, 0, 0.06);
            }}

            @media (max-width: 768px) {{
                .sidebar-toggle-label {{
                    top: 0.9rem;
                    left: 3.2rem;
                    font-size: 0.66rem;
                    padding: 3px 8px;
                }}
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

            /* Boutons : jamais de retour à la ligne */
            [data-testid="stDownloadButton"] button,
            [data-testid="stButton"] button {{
                white-space: nowrap !important;
                overflow: hidden;
                text-overflow: ellipsis;
                min-width: 0;
            }}
        </style>

        <div class="sidebar-toggle-label">{toggle_label}</div>
        """,
        unsafe_allow_html=True,
    )
