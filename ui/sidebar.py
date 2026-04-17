# dash_anticipyr/ui/sidebar.py

from __future__ import annotations

import streamlit as st

from dash_anticipyr.core.constants import PERIODES, SSP_LIST
from dash_anticipyr.core.paths import data_cartographies_root
from dash_anticipyr.core.raster import lister_especes
from dash_anticipyr.ui.sidebar_style import inject_sidebar_styles

SSP_COULEURS = {
    "SSP 126": "#2e7d32",
    "SSP 245": "#f9a825",
    "SSP 370": "#e65100",
    "SSP 585": "#b71c1c",
}


def render_sidebar() -> tuple[str, str, str, str | None, str]:
    """
    Retour :
      - espece (str)
      - periode_label (str)
      - periode_cle (str)
      - ssp_choisi (str | None)
      - mode_visu (str)
    """
    inject_sidebar_styles()

    with st.sidebar:

        # ── Titre ─────────────────────────────────────────────────────────
        st.markdown(
            """
            <div style="padding:16px 8px 8px 8px; margin-bottom:4px;">
                <p style="font-size:1.2rem; font-weight:700; color:#1b5e35; margin:0; letter-spacing:0.02em;">
                    Flore Pyrénéenne
                </p>
                <p style="font-size:0.78rem; color:#9ca3af; margin:2px 0 0 0;">
                    Sélectionnez une espèce, une période et un scénario
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.divider()

        # ── Espèce ────────────────────────────────────────────────────────
        st.markdown(
            "<p style='font-size:0.82rem; font-weight:600; color:#374151; margin-bottom:4px;'>"
            "Espèce étudiée</p>",
            unsafe_allow_html=True,
        )

        dossier_racine_defaut = str(data_cartographies_root())
        especes = lister_especes(dossier_racine_defaut)

        if not especes:
            st.error(
                "Aucune espèce trouvée.\n"
                "Vérifiez que les dossiers existent dans `dash_anticipyr/data/cartographies/`."
            )
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
            f"<p style='font-size:0.78rem; color:#6b7280; font-style:italic; margin-top:2px;'>"
            f"{espece}</p>",
            unsafe_allow_html=True,
        )

        st.divider()

        # ── Période ───────────────────────────────────────────────────────
        st.markdown(
            "<p style='font-size:0.82rem; font-weight:600; color:#374151; margin-bottom:4px;'>"
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
                <div style="
                    background-color:#f0faf3;
                    border-left:4px solid #1b5e35;
                    border-radius:4px;
                    padding:10px 12px;
                    font-size:0.82rem;
                    color:#374151;
                ">
                    <strong>Période actuelle (1970–2000)</strong><br>
                    Aucun scénario SSP — ces données correspondent
                    aux observations climatiques de référence.
                </div>
                """,
                unsafe_allow_html=True,
            )
            ssp_choisi = None

        else:
            st.markdown(
                "<p style='font-size:0.82rem; font-weight:600; color:#374151; margin-bottom:4px;'>"
                "Scénario climatique (SSP)</p>",
                unsafe_allow_html=True,
            )

            ssp_choisi = st.selectbox(
                "SSP",
                options=SSP_LIST,
                help="SSP 126 = optimiste  ·  SSP 585 = pessimiste",
                label_visibility="collapsed",
            )

            couleur = SSP_COULEURS.get(ssp_choisi, "#6b7280")
            st.markdown(
                f"""
                <div style="
                    display:inline-block;
                    background-color:{couleur}18;
                    border:1px solid {couleur};
                    border-radius:12px;
                    padding:3px 12px;
                    font-size:0.78rem;
                    font-weight:600;
                    color:{couleur};
                    margin-top:4px;
                ">
                    {ssp_choisi}
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.divider()

        # ── Mode de visualisation ─────────────────────────────────────────
        st.markdown(
            "<p style='font-size:0.82rem; font-weight:600; color:#374151; margin-bottom:4px;'>"
            "Mode de visualisation</p>",
            unsafe_allow_html=True,
        )

        mode_visu = st.radio(
            "Mode",
            options=["Continu", "Absence", "Présence"],
            index=0,
            label_visibility="collapsed",
            help=(
                "Continu : probabilité 0→1  |  "
                "Absence : zones sous le seuil  |  "
                "Présence : zones au-dessus du seuil"
            ),
        )

        st.divider()

        # ── Pied de sidebar ───────────────────────────────────────────────
        st.markdown(
            """
            <div style="font-size:0.72rem; color:#9ca3af; text-align:center; padding:8px 0 4px 0;">
                ANTICI'PYR · Flore Pyrénéenne<br>
                Université de Perpignan Via Domitia
            </div>
            """,
            unsafe_allow_html=True,
        )

    return espece, periode_label, periode_cle, ssp_choisi, mode_visu
