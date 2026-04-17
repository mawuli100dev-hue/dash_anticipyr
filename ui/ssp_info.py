from __future__ import annotations

import streamlit as st


ARTICLE_URL = "https://nsojournals.onlinelibrary.wiley.com/doi/10.1002/ecog.08067?af=R"

AUTHORS = [
    "Noèmie Collette",
    "Sébastien Pinel",
    "Valérie Delorme-Hinoux",
    "Joris A. M. Bertrand",
]


def render_ssp_info() -> None:
    st.title("Scénarios climatiques (SSPs)")

    st.markdown(
        """
Les **SSPs** (Shared Socioeconomic Pathways) décrivent des trajectoires socio-économiques menant à différents niveaux d'émissions.
L'article de référence utilise **SSP126, SSP245, SSP370 et SSP585** pour projeter l'évolution des conditions bioclimatiques dans les Pyrénées.

> Note : les scénarios ne sont pas fournis avec une “probabilité” statistique unique (ça dépend des hypothèses). Ci-dessous, on donne une lecture qualitative “plus ou moins fortes” en termes d'émissions, et des champs prêts à accueillir les valeurs exactes (°C et mm) reportées par l'article.
"""
    )

    st.markdown("## Article méthodologique")
    st.markdown(f"- Lien : {ARTICLE_URL}")
    st.markdown("## Auteurs (article)")
    st.markdown("- " + ", ".join(AUTHORS))

    st.markdown("## Concepteurs du tableau de bord")
    st.markdown("- Concepteurs : Ayi AMAVIGAN")

    st.divider()

    st.markdown("## Résumé rapide par scénario")

    with st.expander("Valeurs ΔT (°C) et ΔP (mm) à renseigner (depuis l'article)"):
        cols = st.columns(4)
        # On garde des valeurs sous forme de texte (plus simple pour coller des valeurs + unités).
        defaults = {
            "SSP 126": {"dt": "—", "dp": "—"},
            "SSP 245": {"dt": "—", "dp": "—"},
            "SSP 370": {"dt": "—", "dp": "—"},
            "SSP 585": {"dt": "—", "dp": "—"},
        }

        for i, ssp in enumerate(["SSP 126", "SSP 245", "SSP 370", "SSP 585"]):
            with cols[i]:
                st.markdown(f"**{ssp}**")
                st.session_state.setdefault(f"ssp_{ssp}_dt", defaults[ssp]["dt"])
                st.session_state.setdefault(f"ssp_{ssp}_dp", defaults[ssp]["dp"])
                dt = st.text_input(
                    "ΔT (°C)",
                    value=st.session_state[f"ssp_{ssp}_dt"],
                    key=f"ssp_{ssp}_dt_input",
                )
                dp = st.text_input(
                    "ΔP (mm)",
                    value=st.session_state[f"ssp_{ssp}_dp"],
                    key=f"ssp_{ssp}_dp_input",
                )
                st.session_state[f"ssp_{ssp}_dt"] = dt
                st.session_state[f"ssp_{ssp}_dp"] = dp

    def dt(ssp: str) -> str:
        return st.session_state.get(f"ssp_{ssp}_dt", "—")

    def dp(ssp: str) -> str:
        return st.session_state.get(f"ssp_{ssp}_dp", "—")

    st.markdown(
        """
| SSP | Lecture émissions (qualitative) | ΔT (°C) | ΔP (mm) |
|---|---|---|---|
| SSP 126 | Trajectoire de mitigation (faibles émissions) | {dt126} | {dp126} |
| SSP 245 | Émissions intermédiaires | {dt245} | {dp245} |
| SSP 370 | Émissions élevées | {dt370} | {dp370} |
| SSP 585 | Émissions très élevées | {dt585} | {dp585} |
""".format(
            dt126=dt("SSP 126"),
            dp126=dp("SSP 126"),
            dt245=dt("SSP 245"),
            dp245=dp("SSP 245"),
            dt370=dt("SSP 370"),
            dp370=dp("SSP 370"),
            dt585=dt("SSP 585"),
            dp585=dp("SSP 585"),
        )
    )

