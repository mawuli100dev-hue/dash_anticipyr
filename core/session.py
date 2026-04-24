from __future__ import annotations

import streamlit as st

from dash_anticipyr.core.constants import PERIODES, SSP_LIST, B2_BUCKET
from dash_anticipyr.core.inaturalist import get_photo_espece
from dash_anticipyr.core.pdf import construire_nom_fichier, generer_pdf_complet, generer_pdf_multi_periodes
from dash_anticipyr.core.raster import charger_raster, construire_cle, creer_figure, _get_s3


def _fichier_existe(cle: str) -> bool:
    try:
        _get_s3().head_object(Bucket=B2_BUCKET, Key=cle)
        return True
    except Exception:
        return False


def generer_pdf_session(
    espece: str,
    periode_label: str,
    periode_cle: str,
    ssp_choisi: str | None,
    mode_visu: str,
    fond: str = "plan",
    opacite=0.7
) -> None:
    est_binaire = (mode_visu == "Défavorable/Favorable")

    try:
        cle_tif = construire_cle(espece, periode_cle, ssp_choisi, binaire=est_binaire)
    except ValueError:
        st.session_state["pdf_complet_bytes"] = None
        return

    if not _fichier_existe(cle_tif):
        st.session_state["pdf_complet_bytes"] = None
        return

    try:
        data, bounds = charger_raster(cle_tif)
    except Exception:
        st.session_state["pdf_complet_bytes"] = None
        return

    if periode_cle == "current":
        titre_carte = f"{espece}  · (1970-2000)"
    else:
        titre_carte = f"{espece}  ·  {periode_label} | {ssp_choisi}"
    if est_binaire:
        titre_carte += "  ·  Défavorable/Favorable"

    mode_figure = "binaire" if est_binaire else "continu"
    fig = creer_figure(data, bounds, titre_carte, mode=mode_figure, fond=fond, opacite=opacite)

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
    st.session_state["pdf_complet_nom"] = f"{nom}_scenario.pdf"


def generer_pdf_espece_complet(
    espece: str,
    mode_visu: str,
    fond: str = "plan",
    opacite=0.7
) -> None:
    est_binaire = (mode_visu == "Défavorable/Favorable")
    mode_figure = "binaire" if est_binaire else "continu"

    PERIODES_FUTURES = {
        label: cle
        for label, cle in PERIODES.items()
        if cle != "current"
    }

    # --- Page 1 : période actuelle ---
    fig_current = None
    cle_current = construire_cle(espece, "current", None, binaire=est_binaire)
    if _fichier_existe(cle_current):
        try:
            data, bounds = charger_raster(cle_current)
            titre = f"{espece}  · (1970-2000)"
            if est_binaire:
                titre += "  ·  Défavorable/Favorable"
            fig_current = creer_figure(data, bounds, titre, mode=mode_figure, fond=fond, opacite=opacite)
        except Exception:
            pass

    # --- Pages 2-5 : grilles SSP par période ---
    pages_futures = []
    for periode_label, periode_cle in PERIODES_FUTURES.items():
        figs_ssp = []
        for ssp in SSP_LIST:
            try:
                cle = construire_cle(espece, periode_cle, ssp, binaire=est_binaire)
            except ValueError:
                continue
            if not _fichier_existe(cle):
                continue
            try:
                data, bounds = charger_raster(cle)
                titre = f"{espece}  ·  {periode_label} | {ssp}"
                if est_binaire:
                    titre += "  ·  Défavorable/Favorable"
                figs_ssp.append(creer_figure(data, bounds, titre, mode=mode_figure, fond=fond, opacite=opacite))
            except Exception:
                continue
        if figs_ssp:
            pages_futures.append((periode_label, figs_ssp))

    if fig_current is None and not pages_futures:
        st.session_state["pdf_espece_bytes"] = None
        return

    photo_url, attribution = get_photo_espece(espece)
    pdf_bytes = generer_pdf_multi_periodes(
        espece=espece,
        photo_url=photo_url,
        attribution=attribution,
        fig_current=fig_current,
        pages_futures=pages_futures,
        est_binaire=est_binaire,
    )

    st.session_state["pdf_espece_bytes"] = pdf_bytes
    st.session_state["pdf_espece_nom"] = f"{espece}_fiche_complete.pdf"
