# ui/app_style.py
from __future__ import annotations

import streamlit as st
from core.translations import t

from ui.configuration_style import (
    COULEUR_PRINCIPALE,
    COULEUR_PRINCIPALE_CLAIRE,
    COULEUR_BORDURE_ACTIVE,
    COULEUR_TEXTE_DISCRET,
    COULEUR_FOND_SIDEBAR,
    COULEUR_BORDURE,
    TAILLE_TITRE_HEADER,
    TAILLE_SOUS_TITRE,
    TAILLE_ONGLETS,
    ONGLET_GAP,
    ONGLET_RADIUS,
    ONGLET_LARGEUR_MIN,
    ONGLET_COULEUR_ACTIVE,
    ONGLET_FOND_ACTIVE,
    ONGLET_EPAISSEUR_ACTIVE,
    ONGLET_COULEUR_INACTIVE,
    PADDING_HAUT_CONTENU,
    PADDING_BAS_CONTENU,
    POLICE_PRINCIPALE,
    POLICE_TITRES,
    POLICE_ONGLETS,
    GOOGLE_FONTS_URL,
    BOUTON_FOND,
    BOUTON_COULEUR_TEXTE,
    BOUTON_BORDURE,
    BOUTON_RADIUS,
    BOUTON_HAUTEUR_MIN,
    BOUTON_FOND_SURVOL,
    BOUTON_TEXTE_SURVOL,
)


def _css_font(police: str) -> str:
    if not police or police.lower() == "inherit":
        return ""
    return f"font-family: '{police}', sans-serif !important;"


def inject_styles() -> None:
    header_titre = t("page_title")

    if GOOGLE_FONTS_URL:
        st.markdown(
            f'''<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{GOOGLE_FONTS_URL}" rel="stylesheet">''',
            unsafe_allow_html=True,
        )

    css_police_principale = _css_font(POLICE_PRINCIPALE)
    css_police_titres = _css_font(POLICE_TITRES)
    css_police_onglets = _css_font(POLICE_ONGLETS)

    st.markdown(
        f"""
        <style>

            #MainMenu {{visibility: hidden;}}
            footer {{visibility: hidden;}}

            .stAppDeployButton {{visibility: hidden;}}

            [data-testid="stDecoration"] {{display: none;}}

            [data-testid="stStatusWidget"] {{display: none !important;}}

            /* Police globale */
            .block-container, .block-container * {{
                {css_police_principale}
            }}

            /* Sous-titre */
            .main-subtitle {{
                font-size: {TAILLE_SOUS_TITRE} !important;
                color: {COULEUR_TEXTE_DISCRET};
                margin: 0;
                font-style: italic;
                {css_police_principale}
            }}

            /* Boutons standards ET boutons de téléchargement */
            div.stButton > button, [data-testid="stDownloadButton"] button {{
                background-color: {BOUTON_FOND} !important;
                color: {BOUTON_COULEUR_TEXTE} !important;
                border: 1px solid {BOUTON_BORDURE} !important;
                border-radius: {BOUTON_RADIUS} !important;
                font-weight: 600 !important;
                width: 100% !important;
                min-height: {BOUTON_HAUTEUR_MIN} !important;
                white-space: normal !important;
                word-wrap: break-word !important;
                padding: 0.5rem !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
                transition: background-color 0.2s ease, color 0.2s ease !important;
                {css_police_principale}
            }}

            div.stButton > button:hover, [data-testid="stDownloadButton"] button:hover {{
                background-color: {BOUTON_FOND_SURVOL} !important;
                border: 2px solid {BOUTON_FOND_SURVOL} !important;
                color: {BOUTON_TEXTE_SURVOL} !important;
            }}

            [data-testid="stDownloadButton"] button p {{
                color: inherit !important;
                margin: 0 !important;
            }}

            /* Onglets */
            .stTabs [data-baseweb="tab-list"] {{
                gap: {ONGLET_GAP} !important;
                padding-left: 0px !important;
                border-bottom: none !important;
                margin-bottom: 0 !important;
                justify-content: flex-start !important;
            }}

            .stTabs [data-baseweb="tab"] {{
                font-size: {TAILLE_ONGLETS} !important;
                font-weight: 600 !important;
                padding: 10px 32px !important;
                border-radius: {ONGLET_RADIUS} !important;
                color: {ONGLET_COULEUR_INACTIVE} !important;
                background-color: transparent !important;
                border: none !important;
                min-width: {ONGLET_LARGEUR_MIN} !important;
                text-align: center !important;
                {css_police_onglets}
            }}

            .stTabs [aria-selected="true"] {{
                color: {ONGLET_COULEUR_ACTIVE} !important;
                border-bottom: {ONGLET_EPAISSEUR_ACTIVE} solid {ONGLET_COULEUR_ACTIVE} !important;
                background-color: {ONGLET_FOND_ACTIVE} !important;
            }}

            .stTabs [data-baseweb="tab"]:hover {{
                color: {ONGLET_COULEUR_ACTIVE} !important;
                background-color: {ONGLET_FOND_ACTIVE} !important;
            }}

            .stTabs [data-baseweb="tab-highlight"] {{display: none !important;}}
            .stTabs [data-baseweb="tab-border"] {{display: none !important;}}

            /* Sidebar */
            [data-testid="stSidebar"] {{
                background-color: {COULEUR_FOND_SIDEBAR} !important;
                border-right: 1px solid {COULEUR_BORDURE} !important;
            }}

            [data-testid="stSidebar"] * {{
                {css_police_principale}
            }}

            /* Header */
            [data-testid="stHeader"] {{
                background-color: #ffffff !important;
                border-bottom: 1px solid {COULEUR_BORDURE} !important;
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
                font-size: {TAILLE_TITRE_HEADER};
                font-weight: 700;
                color: {COULEUR_PRINCIPALE};
                letter-spacing: 0.01em;
                white-space: nowrap;
                {css_police_titres}
            }}

            [data-testid="stToolbarActions"] {{
                display: none !important;
                visibility: hidden !important;
            }}

            #MainMenu {{display: none !important; visibility: hidden !important;}}

            [data-testid="stDecoration"] {{display: none !important;}}

            .block-container {{
                padding-top: {PADDING_HAUT_CONTENU} !important;
                padding-bottom: {PADDING_BAS_CONTENU} !important;
            }}

            @media print {{
                [data-testid="stSidebar"] {{display: none !important;}}
                [data-testid="stHeader"] {{display: none !important;}}
                [data-testid="stDecoration"] {{display: none !important;}}
                .block-container {{padding-top: 0.5rem !important;}}
            }}

            [data-testid="stDownloadButton"] button,
            [data-testid="stButton"] button {{
                white-space: nowrap !important;
                overflow: hidden;
                text-overflow: ellipsis;
                min-width: 0;
            }}

            div[class^="viewerBadge_container"],
            div[class^="viewerBadge_link"],
            a[href*="streamlit.io/cloud"] {{display: none !important;}}

        </style>
        """,
        unsafe_allow_html=True,
    )