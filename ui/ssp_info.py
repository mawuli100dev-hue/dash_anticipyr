from __future__ import annotations

from pathlib import Path

import streamlit as st

from dash_anticipyr.core.translations import t


ARTICLE_URL = "https://nsojournals.onlinelibrary.wiley.com/doi/10.1002/ecog.08067?af=R"

AUTHORS = [
    "Noèmie Collette",
    "Sébastien Pinel",
    "Valérie Delorme-Hinoux",
    "Joris A. M. Bertrand",
]

FIGURE_SSP = Path(__file__).parent.parent / "data" / "figures" / "ssp_projections.png"

# Données numériques uniquement - labels/descriptions viennent de t()
SSP_DATA = [
    {"ssp": "SSP 126", "cle": "126", "dt": "+2,16 °C", "dp": "-3,56 mm",   "couleur": "#2e7d32"},
    {"ssp": "SSP 245", "cle": "245", "dt": "+3,29 °C", "dp": "-52,6 mm",   "couleur": "#f9a825"},
    {"ssp": "SSP 370", "cle": "370", "dt": "+4,6 °C",  "dp": "-97,98 mm",  "couleur": "#e65100"},
    {"ssp": "SSP 585", "cle": "585", "dt": "+6,14 °C", "dp": "-132,36 mm", "couleur": "#b71c1c"},
]


def render_ssp_info() -> None:
    st.markdown(t("ssp_page_titre"))
    st.markdown(t("ssp_intro"))

    # Cartes SSP
    cols = st.columns(4)
    for col, ssp in zip(cols, SSP_DATA):
        label = t(f"ssp_{ssp['cle']}_label")
        description = t(f"ssp_{ssp['cle']}_description")
        with col:
            st.markdown(
                f"""
                <div style="
                    border-left: 5px solid {ssp['couleur']};
                    padding: 12px 16px;
                    background-color: #f9f9f9;
                    border-radius: 6px;
                ">
                    <p style="font-size:1.1rem;font-weight:700;margin:0;
                              color:{ssp['couleur']}">
                        {ssp['ssp']}
                    </p>
                    <p style="font-size:0.85rem;font-weight:600;color:#444;margin:4px 0;">
                        {label}
                    </p>
                    <p style="font-size:0.82rem;color:#666;margin:8px 0;">
                        {description}
                    </p>
                    <p style="margin:4px 0;font-size:0.85rem;">
                        <strong>{t("ssp_temperature")}</strong> {ssp['dt']}
                    </p>
                    <p style="margin:4px 0;font-size:0.85rem;">
                        <strong>{t("ssp_precipitations")}</strong> {ssp['dp']}
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.divider()

    # Graphique projections climatiques
    if FIGURE_SSP.exists():
        st.image(
            str(FIGURE_SSP),
            caption=t("ssp_figure_caption"),
            use_container_width=True,
        )
    else:
        st.info(t("ssp_figure_manquant", chemin=FIGURE_SSP))

    st.divider()

    # Tableau récapitulatif
    st.markdown(t("ssp_recap_titre"))
    col_ssp = t("ssp_recap_col_ssp")
    col_emis = t("ssp_recap_col_emissions")
    col_dt = t("ssp_recap_col_dt")
    col_dp = t("ssp_recap_col_dp")

    lignes = "\n".join(
        f"| **{s['ssp']}** | {t('ssp_' + s['cle'] + '_label')} | {s['dt']} | {s['dp']} |"
        for s in SSP_DATA
    )

    st.markdown(
        f"| {col_ssp} | {col_emis} | {col_dt} | {col_dp} |\n"
        "|---|---|---|---|\n"
        + lignes
    )

    st.divider()

    # Références
    st.markdown(t("ssp_ref_titre"))
    st.markdown(
        f"{t('ssp_ref_article')} [{ARTICLE_URL}]({ARTICLE_URL})  \n"
        f"{t('ssp_ref_auteurs')} " + " · ".join(AUTHORS) + "  \n"
        f"{t('ssp_ref_dashboard')} Ayi AMAVIGAN"
    )
