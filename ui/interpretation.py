from __future__ import annotations

from pathlib import Path

import streamlit as st

from dash_anticipyr.core.translations import t


BIO_VARIABLES = [
    ("BIO1",  "Température annuelle moyenne",          "Température annuelle moyenne",                                              "°C"),
    ("BIO2",  "Écart diurne moyen",                    "Moyenne des écarts de température mensuels (Tmax - Tmin)",                  "°C"),
    ("BIO3",  "Isothermalité",                         "(BIO2 / BIO7) (*100) : Proportion de la variation diurne par rapport à la variation annuelle", "%"),
    ("BIO4",  "Saisonnalité de la température",        "Variabilité de la température (écart-type * 100)",                         "°C"),
    ("BIO5",  "Température max du mois le plus chaud", "Température maximale du mois le plus chaud",                               "°C"),
    ("BIO6",  "Température min du mois le plus froid", "Température minimale du mois le plus froid",                               "°C"),
    ("BIO7",  "Écart annuel de température",           "Écart de température annuel (BIO5 - BIO6)",                                "°C"),
    ("BIO8",  "Température moyenne du trimestre le plus humide", "Température moyenne du trimestre le plus humide",                "°C"),
    ("BIO9",  "Température moyenne du trimestre le plus sec",    "Température moyenne du trimestre le plus sec",                   "°C"),
    ("BIO10", "Température moyenne du trimestre le plus chaud",  "Température moyenne du trimestre le plus chaud",                 "°C"),
    ("BIO11", "Température moyenne du trimestre le plus froid",  "Température moyenne du trimestre le plus froid",                 "°C"),
    ("BIO12", "Précipitation annuelle",                "Précipitation annuelle totale",                                            "mm"),
    ("BIO13", "Précipitation du mois le plus humide",  "Précipitation du mois le plus humide",                                    "mm"),
    ("BIO14", "Précipitation du mois le plus sec",     "Précipitation du mois le plus sec",                                       "mm"),
    ("BIO15", "Saisonnalité des précipitations",       "Variabilité des précipitations (coefficient de variation)",                "%"),
    ("BIO16", "Précipitation du trimestre le plus humide", "Précipitation totale du trimestre le plus humide",                    "mm"),
    ("BIO17", "Précipitation du trimestre le plus sec",    "Précipitation totale du trimestre le plus sec",                       "mm"),
    ("BIO18", "Précipitation du trimestre le plus chaud",  "Précipitation totale du trimestre le plus chaud",                     "mm"),
    ("BIO19", "Précipitation du trimestre le plus froid",  "Précipitation totale du trimestre le plus froid",                     "mm"),
]


def render_interpretation() -> None:
    st.markdown(
        """
        L'étude repose sur un outil central de l'écologie contemporaine : les modèles de distribution
        d'espèces (Species Distribution Models, SDM). Dans leur forme la plus complète, les SDM intègrent
        de multiples dimensions écologiques (climat, dispersion, interactions biotiques, génétique).
        Ils caractérisent ainsi où et pourquoi une espèce se maintient.
        """
    )

    st.markdown(
        """
        Les cartes de répartition des espèces pyrénéennes sont construites à partir de variables climatiques,
        en particulier les précipitations et les températures. Elles résultent du croisement entre des données
        de présence (relevés de terrain, spécimens d'herbier, bases de données en ligne) et un ensemble de
        variables environnementales caractérisant les conditions des sites occupés (voir tableau ci-dessous).
        """
    )

    # Tableau des variables bioclimatiques
    lignes_temp = ""
    lignes_prec = ""

    for code, nom, description, unite in BIO_VARIABLES:
        ligne = (
            f"<tr>"
            f"<td><strong>{code}</strong></td>"
            f"<td>{nom}</td>"
            f"<td style='color:#555;font-size:0.85rem;'>{description}</td>"
            f"<td style='text-align:center;'>{unite}</td>"
            f"</tr>"
        )
        if code.startswith("BIO1") and int(code[3:]) <= 11:
            lignes_temp += ligne
        else:
            lignes_prec += ligne

    def bloc_tableau(titre: str, couleur: str, lignes: str) -> str:
        return f"""
        <div style="margin-bottom:24px;">
            <p style="font-weight:700;font-size:1rem;color:{couleur};margin-bottom:6px;">{titre}</p>
            <table style="width:100%;border-collapse:collapse;font-size:0.875rem;">
                <thead>
                    <tr style="background-color:{couleur}18;border-bottom:2px solid {couleur};">
                        <th style="padding:8px;text-align:left;width:70px;">Variable</th>
                        <th style="padding:8px;text-align:left;">Nom</th>
                        <th style="padding:8px;text-align:left;">Description</th>
                        <th style="padding:8px;text-align:center;width:60px;">Unité</th>
                    </tr>
                </thead>
                <tbody>
                    {lignes}
                </tbody>
            </table>
        </div>
        """

    st.markdown(
        bloc_tableau("Variables de température (BIO1 - BIO11)", "#1565c0", lignes_temp)
        + bloc_tableau("Variables de précipitations (BIO12 - BIO19)", "#2e7d32", lignes_prec),
        unsafe_allow_html=True,
    )

    st.divider()

    st.markdown(
        """
        Les modèles permettent de définir les combinaisons climatiques associées à la présence
        (ou l'absence) de l'espèce, et donc les environnements où elle est susceptible de se maintenir.
        Ce portrait établi, il devient possible d'étudier l'évolution de ces conditions sous différents
        climats futurs pour estimer où l'espèce pourrait subsister, migrer ou disparaître.
        """
    )
