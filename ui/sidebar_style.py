# ui\sidebar_style.py
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


# DROPDOWN_CSS conservé pour usage éventuel ailleurs, mais n'est plus
# utilisé par le sélecteur de langue (remplacé par st.selectbox natif).
DROPDOWN_CSS = """
    * { box-sizing: border-box; margin: 0; padding: 0; }

    body {
        background: transparent;
        overflow: hidden;
    }

    .dropdown {
        position: relative;
        width: 100%;
        user-select: none;
    }

    .sel {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 6px 28px 6px 9px;
        background: #f8faf9;
        border: 1px solid #d1d5db;
        border-radius: 6px;
        cursor: pointer;
        font-size: 0.82rem;
        color: #374151;
        transition: border-color 0.15s ease, box-shadow 0.15s ease;
    }

    .sel:hover {
        border-color: #1b5e35;
    }

    .sel.open {
        border-color: #1b5e35;
        box-shadow: 0 0 0 2px rgba(27,94,53,0.18);
        border-bottom-left-radius: 0;
        border-bottom-right-radius: 0;
    }

    .arrow {
        position: absolute;
        right: 9px;
        top: 50%;
        transform: translateY(-50%);
        color: #6b7280;
        font-size: 10px;
        pointer-events: none;
        transition: transform 0.15s ease;
    }

    .sel.open ~ .arrow {
        transform: translateY(-50%) rotate(180deg);
    }

    .menu {
        display: none;
        position: absolute;
        top: 100%;
        left: 0;
        right: 0;
        background: #ffffff;
        border: 1px solid #1b5e35;
        border-top: none;
        border-bottom-left-radius: 6px;
        border-bottom-right-radius: 6px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.10);
        z-index: 999;
        overflow: hidden;
    }

    .menu.visible {
        display: block;
    }

    .option {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 7px 10px;
        font-size: 0.82rem;
        color: #374151;
        cursor: pointer;
        transition: background 0.1s ease;
    }

    .option:hover {
        background: #f0faf3;
        color: #1b5e35;
    }

    .option-active {
        background: #e8f5e9;
        color: #1b5e35;
        font-weight: 600;
    }

    #sel-label {
        flex: 1;
    }
"""


def inject_sidebar_styles(ssp_actif: str | None = None) -> None:

    regles_ssp = ""
    for ssp, couleur in SSP_COULEURS.items():
        ancre_id = "ancre-" + ssp.lower().replace(" ", "-")
        slug = ssp.lower().replace(" ", "-")
        actif = ssp == ssp_actif
        bg = couleur if actif else f"{couleur}1a"
        texte = _SSP_TEXTE[ssp] if actif else couleur
        poids = "700" if actif else "500"
        ombre = f"0 0 0 3px {couleur}44" if actif else "none"

        regles_ssp += f"""
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
            [data-testid="stSidebar"] {{
                background-color: #f8faf9;
                border-right: 1px solid #e5e7eb;
            }}

            [data-testid="stSidebar"] hr {{
                border-color: #e5e7eb !important;
                margin: 8px 0 !important;
            }}

            /* Supprime la marge basse sous le selectbox langue (1er selectbox) */
            [data-testid="stSidebar"] [data-testid="stSelectbox"]:first-of-type {{
                margin-bottom: 0 !important;
            }}

            [data-testid="stSidebar"] [data-testid="stSelectbox"]:first-of-type
            > div:first-child {{
                margin-bottom: 0 !important;
                padding-bottom: 0 !important;
            }}

            /* Supprime le padding-bottom du bloc stElementContainer autour du selectbox langue */
            [data-testid="stSidebar"] [data-testid="stElementContainer"]:has(
                [data-testid="stSelectbox"]:first-of-type
            ) {{
                margin-bottom: 0 !important;
                padding-bottom: 0 !important;
            }}

            [data-testid="stSidebar"] [role="radiogroup"] label div:first-child {{
                border-color: {VERT} !important;
            }}

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

            /* Style italic pour tous les selectbox de la sidebar */
            [data-testid="stSidebar"] [data-testid="stSelectbox"]
            [data-baseweb="select"] * {{
                font-style: italic !important;
            }}

            [data-baseweb="popover"] [role="option"] *,
            [data-baseweb="popover"] [role="option"],
            ul[role="listbox"] li,
            ul[role="listbox"] li * {{
                font-style: italic !important;
            }}

            [data-testid="stSidebar"] [data-testid="stSelectbox"] input {{
                font-style: italic !important;
            }}

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

            function colorierSSP() {{
                var sidebar = document.querySelector('[data-testid="stSidebar"]');
                if (!sidebar) return;
                sidebar.querySelectorAll('button').forEach(function(btn) {{
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

            colorierSSP();

            var observer = new MutationObserver(colorierSSP);
            var cible = document.querySelector('[data-testid="stSidebar"]') || document.body;
            observer.observe(cible, {{ childList: true, subtree: true }});

            var n = 0;
            var timer = setInterval(function() {{
                colorierSSP();
                if (++n >= 17) clearInterval(timer);
            }}, 300);
        }})();
        </script>
        """,
        unsafe_allow_html=True,
    )
