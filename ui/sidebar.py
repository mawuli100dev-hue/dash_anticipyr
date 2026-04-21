from __future__ import annotations

import base64
from pathlib import Path

import streamlit as st

from dash_anticipyr.core.constants import PERIODES, SSP_LIST
from dash_anticipyr.core.paths import data_cartographies_root
from dash_anticipyr.core.raster import lister_especes
from dash_anticipyr.core.translations import init_langue, t
from dash_anticipyr.ui.sidebar_style import inject_sidebar_styles


_FLAGS_DIR = Path(__file__).resolve().parent.parent / "data" / "flags"

ARTICLE_URL = "https://nsojournals.onlinelibrary.wiley.com/doi/10.1002/ecog.08067?af=R"

AUTHORS = [
    "Noèmie Collette",
    "Sébastien Pinel",
    "Valérie Delorme-Hinoux",
    "Joris A. M. Bertrand",
]

_LANGUE_LABELS = {
    "fr": "Français",
    "en": "English",
    "es": "Español",
    "ca": "Català",
}


def _lire_drapeau_b64(code: str) -> str:
    chemin = _FLAGS_DIR / f"{code}.png"
    if not chemin.exists():
        return ""
    with open(chemin, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def _render_selecteur_langue() -> None:
    langue_active = st.session_state.get("langue", "fr")
    codes = list(_LANGUE_LABELS.keys())
    index = codes.index(langue_active) if langue_active in codes else 0

    b64 = _lire_drapeau_b64(langue_active)
    if b64:
        st.markdown(
            f"""
            <div style="display:flex;align-items:center;gap:7px;margin-bottom:4px;">
                <div style="display:inline-flex;align-items:center;justify-content:center;
                    background:#f0faf3;border:1px solid #d1fae5;border-radius:6px;
                    padding:3px 7px 3px 5px;gap:6px;">
                    <img src="data:image/png;base64,{b64}"
                         width="24" height="16"
                         style="border-radius:3px;object-fit:cover;display:block;flex-shrink:0;"
                         alt="{langue_active}" />
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    code_choisi = st.selectbox(
        "Langue",
        options=codes,
        index=index,
        format_func=lambda c: _LANGUE_LABELS[c],
        key="_selecteur_langue_widget",
        label_visibility="collapsed",
    )

    if code_choisi != langue_active:
        st.session_state["langue"] = code_choisi
        st.session_state["mode_visu"] = t("mode_continu")
        st.query_params["langue"] = code_choisi
        st.rerun()

    code_depuis_url = st.query_params.get("langue", code_choisi)
    if code_depuis_url in codes and code_depuis_url != st.session_state.get("langue", "fr"):
        st.session_state["langue"] = code_depuis_url
        st.session_state["mode_visu"] = t("mode_continu")
        st.rerun()


def render_sidebar() -> tuple[str, str, str, str | None, str]:

    init_langue()

    if "ssp_choisi" not in st.session_state:
        st.session_state.ssp_choisi = SSP_LIST[0]

    MODES_VISU = [t("mode_continu"), t("mode_binaire")]

    if "mode_visu" not in st.session_state:
        st.session_state["mode_visu"] = MODES_VISU[0]

    inject_sidebar_styles(ssp_actif=st.session_state.ssp_choisi)

    with st.sidebar:

        _render_selecteur_langue()

        st.markdown(
            "<hr style='margin: 4px 0 8px 0; border: none; "
            "border-top: 1px solid #e5e7eb;' />",
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div style="padding:8px 8px 8px 8px; margin-bottom:4px;">
                <p style="font-size:1.2rem;font-weight:700;color:#1b5e35;margin:0;">
                    {t("sidebar_titre")}
                </p>
                <p style="font-size:0.78rem;color:#9ca3af;margin:2px 0 0 0;">
                    {t("sidebar_sous_titre")}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.divider()

        st.markdown(
            f"<p style='font-size:0.82rem;font-weight:600;color:#374151;margin-bottom:4px;'>"
            f"{t('sidebar_espece_label')}</p>",
            unsafe_allow_html=True,
        )

        dossier_racine_defaut = str(data_cartographies_root())
        especes = lister_especes(dossier_racine_defaut)

        if not especes:
            st.error(t("sidebar_espece_error"))
            st.stop()

        st.caption(t("sidebar_espece_caption", n=len(especes)))

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
                t("sidebar_espece_label"),
                options=especes_options,
                index=index,
                key="espece_selectionnee",
                help=t("sidebar_espece_help"),
                label_visibility="collapsed",
            )

        if not espece:
            st.warning(t("sidebar_espece_warning"))
            st.stop()

        st.markdown(
            f"<p style='font-size:0.78rem;color:#6b7280;font-style:italic;margin-top:2px;'>"
            f"{espece}</p>",
            unsafe_allow_html=True,
        )
        st.divider()

        st.markdown(
            f"<p style='font-size:0.82rem;font-weight:600;color:#374151;margin-bottom:4px;'>"
            f"{t('sidebar_periode_label')}</p>",
            unsafe_allow_html=True,
        )
        periode_label = st.selectbox(
            t("sidebar_periode_label"),
            options=list(PERIODES.keys()),
            label_visibility="collapsed",
        )
        periode_cle = PERIODES[periode_label]
        st.divider()

        if periode_cle == "current":
            st.markdown(
                f"""
                <div style="background-color:#f0faf3;border-left:4px solid #1b5e35;
                    border-radius:4px;padding:10px 12px;font-size:0.82rem;color:#374151;">
                    {t("sidebar_current_info")}
                </div>
                """,
                unsafe_allow_html=True,
            )
            ssp_choisi = None
        else:
            st.markdown(
                f"<p style='font-size:0.82rem;font-weight:600;color:#374151;margin-bottom:6px;'>"
                f"{t('sidebar_ssp_label')}</p>",
                unsafe_allow_html=True,
            )

            ssp_descriptions = {
                "SSP 126": t("ssp_126_desc"),
                "SSP 245": t("ssp_245_desc"),
                "SSP 370": t("ssp_370_desc"),
                "SSP 585": t("ssp_585_desc"),
            }

            for ligne in [(SSP_LIST[0], SSP_LIST[1]), (SSP_LIST[2], SSP_LIST[3])]:
                col_g, col_d = st.columns(2, gap="small")
                for ssp, col in zip(ligne, [col_g, col_d]):
                    ancre_id = "ancre-" + ssp.lower().replace(" ", "-")
                    desc = ssp_descriptions[ssp]
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
                            st.session_state["mode_visu"] = st.session_state.get(
                                "mode_visu", MODES_VISU[0]
                            )
                            st.rerun()

            ssp_choisi = st.session_state.ssp_choisi

        st.divider()

        st.markdown(
            f"<p style='font-size:0.82rem;font-weight:600;color:#374151;margin-bottom:4px;'>"
            f"{t('sidebar_mode_label')}</p>",
            unsafe_allow_html=True,
        )

        idx_mode = 1 if st.session_state.get("mode_visu") == MODES_VISU[1] else 0

        mode_selectionne = st.radio(
            t("sidebar_mode_label"),
            options=MODES_VISU,
            index=idx_mode,
            label_visibility="collapsed",
            help=t("sidebar_mode_help"),
        )
        st.session_state["mode_visu"] = mode_selectionne
        mode_visu = mode_selectionne

        st.divider()

        st.markdown(
            f"""
            <div style="font-size:0.72rem;color:#9ca3af;text-align:center;padding:8px 0 4px 0;">
                {t("sidebar_footer")}
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Références
        st.markdown(
            f"""
            <div style="font-size:0.70rem;color:#9ca3af;padding:6px 0 4px 0;
                        border-top:1px solid #e5e7eb;margin-top:4px;">
                {t('ssp_ref_article')} <a href="{ARTICLE_URL}" target="_blank"
                style="color:#6b7280;word-break:break-all;">{ARTICLE_URL}</a><br>
                {t('ssp_ref_auteurs')} {" · ".join(AUTHORS)}<br>
                {t('ssp_ref_dashboard')} Ayi AMAVIGAN
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Logos partenaires - 2 lignes de 4
        _LOGOS_DIR = Path(__file__).resolve().parent.parent / "data" / "logos"
        logos = sorted(_LOGOS_DIR.glob("*.png"), key=lambda p: p.name)

        if logos:
            st.markdown(
                "<hr style='margin: 6px 0 8px 0; border: none; "
                "border-top: 1px solid #e5e7eb;' />",
                unsafe_allow_html=True,
            )
            for i in range(0, len(logos), 4):
                cols = st.columns(4)
                for col, logo_path in zip(cols, logos[i:i+4]):
                    with open(logo_path, "rb") as f:
                        b64 = base64.b64encode(f.read()).decode("utf-8")
                    with col:
                        st.markdown(
                            f'<img src="data:image/png;base64,{b64}" '
                            f'style="width:100%;max-height:36px;object-fit:contain;" '
                            f'alt="{logo_path.stem}" />',
                            unsafe_allow_html=True,
                        )

    return espece, periode_label, periode_cle, ssp_choisi, mode_visu
