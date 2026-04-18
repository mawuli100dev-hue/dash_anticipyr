# dash_anticipyr/ui/sidebar_style.py

from __future__ import annotations

import streamlit as st

VERT = "#1b5e35"

SSP_COULEURS = {
    "SSP 126": "#2e7d32",
    "SSP 245": "#f9a825",
    "SSP 370": "#e65100",
    "SSP 585": "#b71c1c",
}

_SSP_TEXTE = {
    "SSP 126": "#ffffff",
    "SSP 245": "#1a1a1a",
    "SSP 370": "#ffffff",
    "SSP 585": "#ffffff",
}


def inject_sidebar_styles(ssp_actif: str | None = None) -> None:

    regles_ssp = ""
    for ssp, couleur in SSP_COULEURS.items():
        ancre_id = "ancre-" + ssp.lower().replace(" ", "-")
        slug     = ssp.lower().replace(" ", "-")
        actif    = (ssp == ssp_actif)
        bg       = couleur if actif else f"{couleur}1a"
        texte    = _SSP_TEXTE[ssp] if actif else couleur
        poids    = "700"    if actif else "500"
        ombre    = f"0 0 0 3px {couleur}44" if actif else "none"

        regles_ssp += f"""
            /* ── {ssp} ── */
            div[data-testid="stColumn"]:has(#{ancre_id}) button {{
                background-color: {bg} !important;
                border: 2px solid {couleur} !important;
                color: {texte} !important;
                font-weight: {poids} !important;
                box-shadow: {ombre} !important;
                border-radius: 8px !important;
                padding: 8px 4px !important;
                min-height: 56px !important;
                width: 100% !important;
                font-size: 0.82rem !important;
                line-height: 1.35 !important;
                white-space: pre-line !important;
                transition: opacity 0.15s ease !important;
                cursor: pointer !important;
                pointer-events: auto !important;
            }}
            div[data-testid="stColumn"]:has(#{ancre_id}) button p {{
                color: {texte} !important;
                font-weight: {poids} !important;
            }}
            div[data-testid="stColumn"]:has(#{ancre_id}) button:hover {{
                opacity: 0.85 !important;
            }}
            button.ssp-btn-{slug} {{
                background-color: {bg} !important;
                border: 2px solid {couleur} !important;
                color: {texte} !important;
                font-weight: {poids} !important;
                box-shadow: {ombre} !important;
                border-radius: 8px !important;
                padding: 8px 4px !important;
                min-height: 56px !important;
                font-size: 0.82rem !important;
                line-height: 1.35 !important;
                white-space: pre-line !important;
                cursor: pointer !important;
                pointer-events: auto !important;
            }}
            button.ssp-btn-{slug} p {{
                color: {texte} !important;
                font-weight: {poids} !important;
            }}
            button.ssp-btn-{slug}:hover {{
                opacity: 0.85 !important;
            }}
        """

    mapping_js = "{\n"
    for ssp in SSP_COULEURS:
        slug = ssp.lower().replace(" ", "-")
        mapping_js += f'        "{ssp}": "ssp-btn-{slug}",\n'
    mapping_js += "    }"

    st.markdown(
        f"""
        <style>
            /* ── Fond sidebar ── */
            [data-testid="stSidebar"] {{
                background-color: #f8faf9;
                border-right: 1px solid #e5e7eb;
            }}
            [data-testid="stSidebar"] hr {{
                border-color: #e5e7eb !important;
                margin: 8px 0 !important;
            }}

            /* ── Radio accent vert ── */
            [data-testid="stSidebar"] [role="radiogroup"] label div:first-child {{
                border-color: {VERT} !important;
            }}

            /* ── Icône loupe : colonne gauche centrée verticalement ── */
            [data-testid="stSidebar"] .search-icon-col {{
                display: flex;
                align-items: center;
                justify-content: center;
                height: 38px;
                padding-bottom: 15px;
                color: #6b7280;
            }}
            [data-testid="stSidebar"] [data-testid="stHorizontalBlock"]:has(.search-icon-col) {{
                gap: 4px !important;
                align-items: center !important;
            }}
            [data-testid="stSidebar"] [data-testid="stHorizontalBlock"]:has(.search-icon-col)
            > [data-testid="stColumn"]:first-child {{
                padding-right: 0 !important;
                flex: 0 0 28px !important;
                min-width: 28px !important;
                max-width: 28px !important;
            }}

            /* ── Espèces en italique dans le selectbox ── */
            [data-testid="stSidebar"] [data-baseweb="select"] [role="option"] span,
            [data-testid="stSidebar"] [data-baseweb="select"] [data-testid="stSelectboxContainer"] span {{
                font-style: italic !important;
            }}

            /* ── Couleurs SSP ── */
            {regles_ssp}
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <script>
        (function() {{
            var MAPPING = {mapping_js};

            function appliquer() {{
                var sidebar = document.querySelector('[data-testid="stSidebar"]');
                if (!sidebar) return;
                var boutons = sidebar.querySelectorAll('button');
                boutons.forEach(function(btn) {{
                    var texte = (btn.innerText || btn.textContent || '').trim();
                    for (var ssp in MAPPING) {{
                        if (texte.indexOf(ssp) !== -1) {{
                            var toRemove = [];
                            btn.classList.forEach(function(c) {{
                                if (c.indexOf('ssp-btn-') === 0) toRemove.push(c);
                            }});
                            toRemove.forEach(function(c) {{ btn.classList.remove(c); }});
                            btn.classList.add(MAPPING[ssp]);
                            break;
                        }}
                    }}
                }});
            }}

            appliquer();

            var observer = new MutationObserver(appliquer);
            var cible = document.querySelector('[data-testid="stSidebar"]') || document.body;
            observer.observe(cible, {{ childList: true, subtree: true }});

            var n = 0;
            var timer = setInterval(function() {{
                appliquer();
                if (++n >= 17) clearInterval(timer);
            }}, 300);
        }})();
        </script>
        """,
        unsafe_allow_html=True,
    )
