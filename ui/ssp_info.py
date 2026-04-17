# dash_anticipyr/ui/ssp_info.py

from __future__ import annotations

from pathlib import Path

import streamlit as st

ARTICLE_URL = "https://nsojournals.onlinelibrary.wiley.com/doi/10.1002/ecog.08067?af=R"

AUTHORS = [
    "Noèmie Collette",
    "Sébastien Pinel",
    "Valérie Delorme-Hinoux",
    "Joris A. M. Bertrand",
]

# Chemin vers le graphique SSP (issu de la Figure 2 du rapport)
FIGURE_SSP = Path(__file__).parent.parent / "data" / "figures" / "ssp_projections.png"

SSP_DATA = [
    {
        "ssp": "SSP 126",
        "label": "Faibles émissions",
        "description": "Scénario optimiste : forte mitigation climatique, émissions proches de zéro avant 2100.",
        "dt": "+2,16 °C",
        "dp": "-3,56 mm",
        "couleur": "#2e7d32",
    },
    {
        "ssp": "SSP 245",
        "label": "Émissions intermédiaires",
        "description": "Scénario intermédiaire : politiques climatiques partielles, stabilisation en cours de siècle.",
        "dt": "+3,29 °C",
        "dp": "-52,6 mm",
        "couleur": "#f9a825",
    },
    {
        "ssp": "SSP 370",
        "label": "Émissions élevées",
        "description": "Scénario pessimiste : faible coopération internationale, émissions en hausse continue.",
        "dt": "+4,6 °C",
        "dp": "-97,98 mm",
        "couleur": "#e65100",
    },
    {
        "ssp": "SSP 585",
        "label": "Émissions très élevées",
        "description": "Scénario extrême : dépendance massive aux énergies fossiles, aucune mitigation.",
        "dt": "+6,14 °C",
        "dp": "-132,36 mm",
        "couleur": "#b71c1c",
    },
]


def render_ssp_info() -> None:
    st.markdown("## Scénarios climatiques (SSPs)")
    st.markdown(
        "Les **SSPs** (Shared Socioeconomic Pathways) décrivent des trajectoires "
        "socio-économiques menant à différents niveaux d'émissions de gaz à effet de serre. "
        "Ce tableau de bord utilise quatre scénarios pour projeter l'évolution des habitats "
        "des espèces pyrénéennes jusqu'en 2090."
    )

    # ── Cartes SSP ────────────────────────────────────────────────────────
    cols = st.columns(4)
    for col, ssp in zip(cols, SSP_DATA):
        with col:
            st.markdown(
                f"""
                <div style="
                    border-left: 5px solid {ssp['couleur']};
                    padding: 12px 16px;
                    background-color: #f9f9f9;
                    border-radius: 6px;
                ">
                    <p style="font-size:1.1rem; font-weight:700; margin:0; color:{ssp['couleur']}">
                        {ssp['ssp']}
                    </p>
                    <p style="font-size:0.85rem; font-weight:600; color:#444; margin:4px 0;">
                        {ssp['label']}
                    </p>
                    <p style="font-size:0.82rem; color:#666; margin:8px 0;">
                        {ssp['description']}
                    </p>
                    <p style="margin:4px 0; font-size:0.85rem;">
                        <strong>Temperature (2090) :</strong> {ssp['dt']}
                    </p>
                    <p style="margin:4px 0; font-size:0.85rem;">
                        <strong>Precipitations (2090) :</strong> {ssp['dp']}
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.divider()

    # ── Graphique projections climatiques ─────────────────────────────────
    if FIGURE_SSP.exists():
        st.image(
            str(FIGURE_SSP),
            caption="Figure 2 — Projections de température et précipitations annuelles moyennes "
                    "par scénario SSP (Collette, 2024)",
            use_container_width=True,
        )
    else:
        st.info(
            f"Graphique non trouvé : `{FIGURE_SSP}`  \n"
            "Placez le fichier image dans `dash_anticipyr/data/figures/`."
        )

    st.divider()

    # ── Tableau récapitulatif ─────────────────────────────────────────────
    st.markdown("### Recapitulatif a l'horizon 2090")
    st.markdown(
        "| SSP | Emissions | Delta T (°C) | Delta P (mm) |\n"
        "|---|---|---|---|\n"
        + "\n".join(
            f"| **{s['ssp']}** | {s['label']} | {s['dt']} | {s['dp']} |"
            for s in SSP_DATA
        )
    )

    st.divider()

    # ── Références ────────────────────────────────────────────────────────
    st.markdown("### References")
    st.markdown(
        f"**Article :** [{ARTICLE_URL}]({ARTICLE_URL})  \n"
        "**Auteurs :** " + " · ".join(AUTHORS) + "  \n"
        "**Tableau de bord :** Ayi AMAVIGAN"
    )
