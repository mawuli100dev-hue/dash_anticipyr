from __future__ import annotations

from pathlib import Path

import streamlit as st

from core.translations import t, get_langue_courante


TUTO_IMG_DIR = Path(__file__).parent.parent / "data" / "tutorial"


def render_tutorial() -> None:
    # titre général
    st.markdown("## Tutoriel")

    langue = get_langue_courante()

    # --- Bloc 1 : sidebar ---
    img_sidebar = TUTO_IMG_DIR / f"sidebar_{langue}.png"
    if not img_sidebar.exists():
        img_sidebar = TUTO_IMG_DIR / "sidebar_fr.png"

    col_img, col_txt = st.columns([1, 2], gap="large")

    with col_img:
        st.image(str(img_sidebar), width=380)

    with col_txt:
        st.markdown(
            f"""
            <div style="
                background-color:#ffffff;
                border-radius:10px;
                padding:18px 22px;
                box-shadow:0 1px 3px rgba(15,23,42,0.06);
            ">
                <h3 style="margin-top:0;margin-bottom:8px;">
                    {t('tutorial_sidebar_title')}
                </h3>
                <p style="margin:0 0 8px 0;">
                    {t('tutorial_sidebar_intro')}
                </p>
                <ul style="margin:0 0 0 18px;padding:0;font-size:0.95rem;color:#374151;">
                    <li>{t('tutorial_sidebar_lang')}</li>
                    <li>{t('tutorial_sidebar_species')}</li>
                    <li>{t('tutorial_sidebar_period')}</li>
                    <li>{t('tutorial_sidebar_ssp')}</li>
                    <li>{t('tutorial_sidebar_mode')}</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.divider()

    # --- Bloc 2 : boutons d'action en haut de page ---
    img_header = TUTO_IMG_DIR / f"header_{langue}.png"
    if not img_header.exists():
        img_header = TUTO_IMG_DIR / "header_fr.png"

    st.image(str(img_header), use_container_width=True)

    st.markdown(
        f"""
        <div style="
            background-color:#ffffff;
            border-radius:10px;
            padding:18px 22px;
            box-shadow:0 1px 3px rgba(15,23,42,0.06);
        ">
            <h3 style="margin-top:0;margin-bottom:8px;">
                {t('tutorial_header_title')}
            </h3>
            <p style="margin:0 0 8px 0;">
                {t('tutorial_header_intro')}
            </p>
            <ul style="margin:0 0 0 18px;padding:0;font-size:0.95rem;color:#374151;">
                <li>{t('tutorial_header_prepare_scenario')}</li>
                <li>{t('tutorial_header_prepare_full')}</li>
                <li>{t('tutorial_header_tabs')}</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    # --- Bloc 3 : fond de carte et opacité ---
    img_map = TUTO_IMG_DIR / f"map_{langue}.png"
    if not img_map.exists():
        img_map = TUTO_IMG_DIR / "map_fr.png"

    st.image(str(img_map), use_container_width=True)

    st.markdown(
        f"""
        <div style="
            background-color:#ffffff;
            border-radius:10px;
            padding:18px 22px;
            box-shadow:0 1px 3px rgba(15,23,42,0.06);
        ">
            <h3 style="margin-top:0;margin-bottom:8px;">
                {t('tutorial_map_title')}
            </h3>
            <p style="margin:0 0 8px 0;">
                {t('tutorial_map_intro')}
            </p>
            <ul style="margin:0 0 0 18px;padding:0;font-size:0.95rem;color:#374151;">
                <li>{t('tutorial_map_basemap')}</li>
                <li>{t('tutorial_map_opacity')}</li>
                <li>{t('tutorial_map_recentre')}</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    img_map_plan = TUTO_IMG_DIR / "map_plan.png"
    img_map_sat = TUTO_IMG_DIR / "map_satellite.png"
    img_map_0_1 = TUTO_IMG_DIR / "map_0_1.png"

    col1, col2, col3 = st.columns(3)
    with col1:
        if img_map_plan.exists():
            st.image(str(img_map_plan), use_container_width=True)
    with col2:
        if img_map_sat.exists():
            st.image(str(img_map_sat), use_container_width=True)
    with col3:
        if img_map_0_1.exists():
            st.image(str(img_map_0_1), use_container_width=True)

    st.divider()

        # --- Bloc 4 : téléchargement de la carte sélectionnée ---
    langue = get_langue_courante()
    img_export = TUTO_IMG_DIR / f"export_buttons_{langue}.png"
    if not img_export.exists():
        img_export = TUTO_IMG_DIR / "export_buttons_fr.png"  # fallback français

    if img_export.exists():
        st.image(str(img_export), use_container_width=False)

    st.markdown(
        f"""
        <div style="
            background-color:#ffffff;
            border-radius:10px;
            padding:18px 22px;
            box-shadow:0 1px 3px rgba(15,23,42,0.06);
        ">
            <h3 style="margin-top:0;margin-bottom:8px;">
                {t('tutorial_export_title')}
            </h3>
            <p style="margin:0 0 8px 0;">
                {t('tutorial_export_intro')}
            </p>
            <ul style="margin:0 0 0 18px;padding:0;font-size:0.95rem;color:#374151;">
                <li>{t('tutorial_export_png')}</li>
                <li>{t('tutorial_export_jpg')}</li>
                <li>{t('tutorial_export_pdf')}</li>
                <li>{t('tutorial_export_tif')}</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()