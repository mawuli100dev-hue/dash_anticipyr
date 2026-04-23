# ui\interpretation.py
from __future__ import annotations

from pathlib import Path

import streamlit as st

from dash_anticipyr.core.translations import t


BIO_VARIABLES = [
    ("BIO1",  "bio1_nom",  "bio1_desc",  "°C"),
    ("BIO2",  "bio2_nom",  "bio2_desc",  "°C"),
    ("BIO3",  "bio3_nom",  "bio3_desc",  "%"),
    ("BIO4",  "bio4_nom",  "bio4_desc",  "°C"),
    ("BIO5",  "bio5_nom",  "bio5_desc",  "°C"),
    ("BIO6",  "bio6_nom",  "bio6_desc",  "°C"),
    ("BIO7",  "bio7_nom",  "bio7_desc",  "°C"),
    ("BIO8",  "bio8_nom",  "bio8_desc",  "°C"),
    ("BIO9",  "bio9_nom",  "bio9_desc",  "°C"),
    ("BIO10", "bio10_nom", "bio10_desc", "°C"),
    ("BIO11", "bio11_nom", "bio11_desc", "°C"),
    ("BIO12", "bio12_nom", "bio12_desc", "mm"),
    ("BIO13", "bio13_nom", "bio13_desc", "mm"),
    ("BIO14", "bio14_nom", "bio14_desc", "mm"),
    ("BIO15", "bio15_nom", "bio15_desc", "%"),
    ("BIO16", "bio16_nom", "bio16_desc", "mm"),
    ("BIO17", "bio17_nom", "bio17_desc", "mm"),
    ("BIO18", "bio18_nom", "bio18_desc", "mm"),
    ("BIO19", "bio19_nom", "bio19_desc", "mm"),
]


def render_interpretation() -> None:
    st.markdown(t("interp_intro_1"))
    st.markdown(t("interp_intro_2"))

    col_variable = t("interp_col_variable")
    col_nom      = t("interp_col_nom")
    col_desc     = t("interp_col_description")
    col_unite    = t("interp_col_unite")
    titre_temp   = t("interp_titre_temp")
    titre_prec   = t("interp_titre_prec")

    lignes_temp = ""
    lignes_prec = ""

    for code, cle_nom, cle_desc, unite in BIO_VARIABLES:
        ligne = (
            f"<tr>"
            f"<td><strong>{code}</strong></td>"
            f"<td>{t(cle_nom)}</td>"
            f"<td style='color:#555;font-size:0.85rem;'>{t(cle_desc)}</td>"
            f"<td style='text-align:center;'>{unite}</td>"
            f"</tr>"
        )
        num = int(code[3:])
        if num <= 11:
            lignes_temp += ligne
        else:
            lignes_prec += ligne

    def bloc_tableau(titre: str, couleur: str, lignes: str) -> str:
        return f"""
        <div style="margin-bottom:24px;">
            <p style="font-weight:700;font-size:1rem;color:{couleur};margin-bottom:6px;">
                {titre}
            </p>
            <table style="width:100%;border-collapse:collapse;font-size:0.875rem;">
                <thead>
                    <tr style="background-color:{couleur}18;border-bottom:2px solid {couleur};">
                        <th style="padding:8px;text-align:left;width:70px;">{col_variable}</th>
                        <th style="padding:8px;text-align:left;">{col_nom}</th>
                        <th style="padding:8px;text-align:left;">{col_desc}</th>
                        <th style="padding:8px;text-align:center;width:60px;">{col_unite}</th>
                    </tr>
                </thead>
                <tbody>
                    {lignes}
                </tbody>
            </table>
        </div>
        """

    st.markdown(
        bloc_tableau(titre_temp, "#1565c0", lignes_temp)
        + bloc_tableau(titre_prec, "#2e7d32", lignes_prec),
        unsafe_allow_html=True,
    )

    st.divider()

    st.markdown(t("interp_conclusion"))
