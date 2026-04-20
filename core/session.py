# core\session.py
from __future__ import annotations

import streamlit as st

from dash_anticipyr.core.inaturalist import get_photo_espece
from dash_anticipyr.core.paths import data_cartographies_root
from dash_anticipyr.core.pdf import construire_nom_fichier, generer_pdf_complet
from dash_anticipyr.core.raster import charger_raster, construire_chemin, creer_figure


def generer_pdf_session(
    espece: str,
    periode_label: str,
    periode_cle: str,
    ssp_choisi: str | None,
    mode_visu: str,
) -> None:
    est_binaire = (mode_visu == "Absence/Présence")
    racine = data_cartographies_root()

    try:
        chemin_tif = construire_chemin(
            racine, espece, periode_cle, ssp_choisi, binaire=est_binaire
        )
    except ValueError:
        st.session_state["pdf_complet_bytes"] = None
        return

    if not chemin_tif.exists():
        st.session_state["pdf_complet_bytes"] = None
        return

    try:
        data, bounds = charger_raster(str(chemin_tif))
    except Exception:
        st.session_state["pdf_complet_bytes"] = None
        return

    if periode_cle == "current":
        titre_carte = f"{espece}  · (1970-2000)"
    else:
        titre_carte = f"{espece}  ·  {periode_label} | {ssp_choisi}"
    if est_binaire:
        titre_carte += "  ·  Absence/Présence"

    mode_figure = "binaire" if est_binaire else "continu"
    fig = creer_figure(data, bounds, titre_carte, mode=mode_figure)

    photo_url, attribution = get_photo_espece(espece)

    pdf_bytes = generer_pdf_complet(
        espece=espece,
        periode_label=periode_label,
        ssp_choisi=ssp_choisi,
        photo_url=photo_url,
        attribution=attribution,
        fig=fig,
    )

    nom = construire_nom_fichier(espece, periode_label, ssp_choisi, est_binaire)
    st.session_state["pdf_complet_bytes"] = pdf_bytes
    st.session_state["pdf_complet_nom"] = f"{nom}_complet.pdf"
