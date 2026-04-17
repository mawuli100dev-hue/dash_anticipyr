# dash_anticipyr/ui/sidebar_style.py

from __future__ import annotations

import streamlit as st

VERT = "#1b5e35"


def inject_sidebar_styles() -> None:
    """Injecte tous les styles CSS de la sidebar."""
    st.markdown(
        f"""
        <style>
            /* ── Fond et bordure sidebar ── */
            [data-testid="stSidebar"] {{
                background-color: #f8faf9;
                border-right: 1px solid #e5e7eb;
            }}

            /* ── Dividers ── */
            [data-testid="stSidebar"] hr {{
                border-color: #e5e7eb !important;
                margin: 8px 0 !important;
            }}

            /* ── Radio : cercle non sélectionné ── */
            [data-testid="stSidebar"] [role="radiogroup"] label div:first-child {{
                border-color: {VERT} !important;
            }}

            /* ── Radio : cercle sélectionné (rempli) ── */
            [data-testid="stSidebar"] [role="radiogroup"] label [data-testid="stMarkdownContainer"] + div {{
                background-color: {VERT} !important;
                border-color: {VERT} !important;
            }}

            /* ── Radio : texte de l'option sélectionnée ── */
            [data-testid="stSidebar"] [role="radiogroup"] label input:checked ~ div p {{
                color: {VERT} !important;
                font-weight: 600 !important;
            }}

            /* ── Selectbox : bordure focus ── */
            [data-testid="stSidebar"] [data-baseweb="select"] {{
                border-color: {VERT} !important;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )
