# dash_anticipyr/ui/sidebar.py

from __future__ import annotations

import streamlit as st

from dash_anticipyr.core.constants import PERIODES, SSP_LIST
from dash_anticipyr.core.paths import data_cartographies_root
from dash_anticipyr.core.raster import lister_especes
from dash_anticipyr.ui.sidebar_style import inject_sidebar_styles, SSP_COULEURS


SSP_DESCRIPTIONS = {
    "SSP 126": "Optimiste",
    "SSP 245": "Intermédiaire",
    "SSP 370": "Pessimiste",
    "SSP 585": "Très pessimiste",
}

MODES_VISU = ["Continu", "Absence/Présence"]


def render_sidebar() -> tuple[str, str, str, str | None, str]:

    # Initialisation session_state
    if "ssp_choisi" not in st.session_state:
        st.session_state.ssp_choisi = SSP_LIST[0]

    # On initialise mode_visu UNE SEULE FOIS au démarrage.
    # Streamlit gère ensuite la mise à jour automatiquement via key="mode_visu".
    if "mode_visu" not in st.session_state:
        st.session_state["mode_visu"] = MODES_VISU[0]

    inject_sidebar_styles(ssp_actif=st.session_state.ssp_choisi)

    with st.sidebar:

        # ── Titre ─────────────────────────────────────────────────────────
        st.markdown(
            """
            <div style="padding:16px 8px 8px 8px; margin-bottom:4px;">
                <p style="font-size:1.2rem;font-weight:700;color:#1b5e35;margin:0;">
                    Flore Pyrénéenne
                </p>
                <p style="font-size:0.78rem;color:#9ca3af;margin:2px 0 0 0;">
                    Sélectionnez une espèce, une période et un scénario
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.divider()

        # ── Espèce ────────────────────────────────────────────────────────
        st.markdown(
            "<p style='font-size:0.82rem;font-weight:600;color:#374151;margin-bottom:4px;'>"
            "Espèce étudiée</p>",
            unsafe_allow_html=True,
        )

        dossier_racine_defaut = str(data_cartographies_root())
        especes = lister_especes(dossier_racine_defaut)

        if not especes:
            st.error("Aucune espèce trouvée. Vérifiez dash_anticipyr/data/cartographies/.")
            st.stop()

        st.caption(f"{len(especes)} espèce(s) disponible(s)")

        especes_options = [""] + especes

        if "espece_selectionnee" not in st.session_state:
            st.session_state.espece_selectionnee = especes[0]

        index = (
            especes_options.index(st.session_state.espece_selectionnee)
            if st.session_state.espece_selectionnee in especes
            else 1
        )

        col_icon, col_select = st.columns([1, 9])

        with col_icon:
            st.markdown(
                """
                <div class="search-icon-col">
                    <svg xmlns="http://www.w3.org/2000/svg"
                         width="16" height="16" viewBox="0 0 24 24"
                         fill="none" stroke="currentColor" stroke-width="2"
                         stroke-linecap="round" stroke-linejoin="round"
                         aria-hidden="true">
                        <circle cx="11" cy="11" r="8"></circle>
                        <path d="m21 21-4.3-4.3"></path>
                    </svg>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col_select:
            espece = st.selectbox(
                "Nom de l'espèce",
                options=especes_options,
                index=index,
                key="espece_selectionnee",
                help="Tapez après ouverture pour filtrer la liste.",
                label_visibility="collapsed",
            )

        if not espece:
            st.warning("Sélectionnez une espèce dans la liste.")
            st.stop()

        st.markdown(
            f"<p style='font-size:0.78rem;color:#6b7280;font-style:italic;margin-top:2px;'>"
            f"{espece}</p>",
            unsafe_allow_html=True,
        )
        st.divider()

        # ── Période ───────────────────────────────────────────────────────
        st.markdown(
            "<p style='font-size:0.82rem;font-weight:600;color:#374151;margin-bottom:4px;'>"
            "Période de projection</p>",
            unsafe_allow_html=True,
        )
        periode_label = st.selectbox(
            "Période",
            options=list(PERIODES.keys()),
            label_visibility="collapsed",
        )
        periode_cle = PERIODES[periode_label]
        st.divider()

        # ── SSP ───────────────────────────────────────────────────────────
        if periode_cle == "current":
            st.markdown(
                """
                <div style="background-color:#f0faf3;border-left:4px solid #1b5e35;
                    border-radius:4px;padding:10px 12px;font-size:0.82rem;color:#374151;">
                    <strong>Période actuelle (1970-2000)</strong><br>
                    Aucun scénario SSP - données de référence climatique.
                </div>
                """,
                unsafe_allow_html=True,
            )
            ssp_choisi = None

        else:
            st.markdown(
                "<p style='font-size:0.82rem;font-weight:600;color:#374151;margin-bottom:6px;'>"
                "Scénario climatique (SSP)</p>",
                unsafe_allow_html=True,
            )

            for ligne in [(SSP_LIST[0], SSP_LIST[1]), (SSP_LIST[2], SSP_LIST[3])]:
                col_g, col_d = st.columns(2, gap="small")
                for ssp, col in zip(ligne, [col_g, col_d]):
                    ancre_id = "ancre-" + ssp.lower().replace(" ", "-")
                    desc     = SSP_DESCRIPTIONS[ssp]
                    with col:
                        st.markdown(
                            f'<span id="{ancre_id}" style="display:none;"></span>',
                            unsafe_allow_html=True,
                        )
                        if st.button(
                            f"{ssp}\n{desc}",
                            key=f"ssp_{ssp.replace(' ', '_')}",
                            use_container_width=True,
                        ):
                            st.session_state.ssp_choisi = ssp
                            st.rerun()

            ssp_choisi = st.session_state.ssp_choisi

        st.divider()

        # ── Mode de visualisation ─────────────────────────────────────────
        st.markdown(
            "<p style='font-size:0.82rem;font-weight:600;color:#374151;margin-bottom:4px;'>"
            "Mode de visualisation</p>",
            unsafe_allow_html=True,
        )

        # Pas de index= : on laisse Streamlit gérer seul via key=
        # key="mode_visu" : Streamlit lit et écrit st.session_state["mode_visu"]
        # Le radio reprend automatiquement la bonne valeur après chaque st.rerun()
        st.radio(
            "Mode",
            options=MODES_VISU,
            key="mode_visu",
            label_visibility="collapsed",
            help=(
                "Continu : probabilité de présence entre 0 et 1  |  "
                "Absence/Présence : carte binarisée (données déjà 0/1)"
            ),
        )
        mode_visu = st.session_state["mode_visu"]

        st.divider()

        st.markdown(
            """
            <div style="font-size:0.72rem;color:#9ca3af;text-align:center;padding:8px 0 4px 0;">
                ANTICI'PYR · Flore Pyrénéenne<br>
                Université de Perpignan Via Domitia
            </div>
            """,
            unsafe_allow_html=True,
        )

    return espece, periode_label, periode_cle, ssp_choisi, mode_visu
