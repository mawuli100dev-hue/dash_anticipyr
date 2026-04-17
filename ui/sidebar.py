from __future__ import annotations

from pathlib import Path

import streamlit as st

from dash_anticipyr.core.constants import PERIODES, SSP_LIST
from dash_anticipyr.core.paths import data_cartographies_root
from dash_anticipyr.core.raster import lister_especes


def render_sidebar() -> tuple[str, str, str, str | None]:
    """
    Rend toute la sidebar et retourne les paramètres de sélection.

    Retour :
      - espece (str)
      - periode_label (str)
      - periode_cle (str)
      - ssp_choisi (str | None)
    """
    with st.sidebar:
        st.header("Espèce étudiée")

        dossier_racine_defaut = str(data_cartographies_root())
        especes = lister_especes(dossier_racine_defaut)
        if not especes:
            st.error(
                "Aucune espèce trouvée.\n"
                "Vérifiez que les dossiers existent dans `dash_anticipyr/data/cartographies/`."
            )
            st.stop()

        st.caption(f"{len(especes)} espèce(s) disponible(s)")

        # Dropdown "recherchable" : on clique puis on tape pour filtrer.
        especes_options = [""] + especes
        st.caption("Cliquez puis commencez à taper pour filtrer.")

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
            help="Tapez après ouverture pour filtrer la liste."
        )

        if not espece:
            st.warning("Sélectionnez une espèce dans la liste.")
            st.stop()

        st.divider()
        periode_label = st.selectbox(
            "Période de projection",
            options=list(PERIODES.keys()),
        )
        periode_cle = PERIODES[periode_label]

        if periode_cle == "current":
            st.info(
                "**Pas de scénario SSP pour la période 1970–2000.**  \n"
                "Ces données correspondent aux observations climatiques actuelles."
            )
            ssp_choisi = None
        else:
            ssp_choisi = st.selectbox(
                "Scénario climatique (SSP)",
                options=SSP_LIST,
                help="SSP 126 = scénario optimiste  ·  SSP 585 = scénario pessimiste",
            )

    return espece, periode_label, periode_cle, ssp_choisi

