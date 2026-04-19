# dash_anticipyr/ui/map_section.py

from __future__ import annotations

from io import BytesIO
from pathlib import Path
from urllib.request import urlopen

import streamlit as st
from PIL import Image
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

from dash_anticipyr.core.paths import data_cartographies_root
from dash_anticipyr.core.raster import (
    charger_raster,
    construire_chemin,
    creer_figure,
    figure_en_bytes,
)
from dash_anticipyr.core.inaturalist import get_photo_espece


# ─────────────────────────────────────────────────────────────────────────────
# Utilitaires PDF
# ─────────────────────────────────────────────────────────────────────────────

def _telecharger_image(url: str) -> BytesIO | None:
    try:
        with urlopen(url, timeout=10) as response:
            return BytesIO(response.read())
    except Exception:
        return None


def _generer_pdf_complet(
    espece: str,
    periode_label: str,
    ssp_choisi: str | None,
    photo_url: str | None,
    attribution: str | None,
    fig,
) -> bytes:
    buffer_pdf = BytesIO()
    c = canvas.Canvas(buffer_pdf, pagesize=(595, 842))
    largeur_page, hauteur_page = 595, 842
    marge = 40

    y = hauteur_page - marge
    c.setFont("Helvetica-Bold", 16)
    c.setFillColorRGB(0.106, 0.369, 0.208)
    c.drawString(marge, y, "Flore Pyrénéenne - Simulation des Habitats")

    y -= 22
    c.setFont("Helvetica-Oblique", 10)
    c.setFillColorRGB(0.42, 0.45, 0.50)
    c.drawString(marge, y, "Projection bioclimatique des espèces endémiques pyrénéennes")

    y -= 18
    c.setStrokeColorRGB(0.85, 0.85, 0.85)
    c.line(marge, y, largeur_page - marge, y)
    y -= 20

    photo_largeur_max = 190
    photo_hauteur_max = 145
    x_photo = marge
    x_texte = marge + photo_largeur_max + 20

    if photo_url:
        image_stream = _telecharger_image(photo_url)
        if image_stream is not None:
            try:
                image_pil = Image.open(image_stream).convert("RGB")
                ratio = image_pil.width / image_pil.height
                largeur_aff = photo_largeur_max
                hauteur_aff = largeur_aff / ratio
                if hauteur_aff > photo_hauteur_max:
                    hauteur_aff = photo_hauteur_max
                    largeur_aff = hauteur_aff * ratio
                y_photo = y - hauteur_aff
                c.drawImage(
                    ImageReader(image_pil),
                    x_photo, y_photo,
                    width=largeur_aff, height=hauteur_aff,
                    preserveAspectRatio=True,
                    mask="auto",
                )
                legende = espece
                if attribution:
                    auteur = attribution.lstrip("© ").lstrip("(c) ")
                    legende += f" © {auteur}"
                c.setFont("Helvetica-Oblique", 7)
                c.setFillColorRGB(0.42, 0.45, 0.50)
                c.drawString(x_photo, y_photo - 11, legende[:80])
            except Exception:
                pass

    c.setFont("Helvetica-BoldOblique", 16)
    c.setFillColorRGB(0.106, 0.369, 0.208)
    c.drawString(x_texte, y - 16, espece)

    y_info = y - 50
    c.setFont("Helvetica-Bold", 11)
    c.setFillColorRGB(0.22, 0.22, 0.22)
    c.drawString(x_texte, y_info, "Période :")
    c.setFont("Helvetica", 11)
    c.drawString(x_texte + 58, y_info, periode_label)

    y_info -= 22
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x_texte, y_info, "Scénario :")
    c.setFont("Helvetica", 11)
    c.drawString(x_texte + 63, y_info, ssp_choisi if ssp_choisi else "Période actuelle")

    y_separateur = y - photo_hauteur_max - 28
    c.setStrokeColorRGB(0.85, 0.85, 0.85)
    c.line(marge, y_separateur, largeur_page - marge, y_separateur)

    y_carte = y_separateur - 14
    img_carte_bytes = BytesIO(figure_en_bytes(fig, "png"))
    image_carte = Image.open(img_carte_bytes).convert("RGB")

    largeur_max = largeur_page - 2 * marge
    hauteur_max = y_carte - marge
    ratio_carte = image_carte.width / image_carte.height

    largeur_aff = largeur_max
    hauteur_aff = largeur_aff / ratio_carte
    if hauteur_aff > hauteur_max:
        hauteur_aff = hauteur_max
        largeur_aff = hauteur_aff * ratio_carte

    x_carte = (largeur_page - largeur_aff) / 2
    y_carte_img = y_carte - hauteur_aff
    c.drawImage(
        ImageReader(image_carte),
        x_carte, y_carte_img,
        width=largeur_aff, height=hauteur_aff,
        preserveAspectRatio=True,
        mask="auto",
    )

    c.showPage()
    c.save()
    buffer_pdf.seek(0)
    return buffer_pdf.getvalue()


def _construire_nom_fichier(
    espece: str,
    periode_label: str,
    ssp_choisi: str | None,
    est_binaire: bool,
) -> str:
    nom = (
        espece.replace(" ", "_")
        + "_"
        + periode_label.replace("–", "-").replace(" ", "_").replace("(", "").replace(")", "")
    )
    if ssp_choisi:
        nom += "_" + ssp_choisi.replace(" ", "")
    if est_binaire:
        nom += "_absence_presence"
    return nom


# ─────────────────────────────────────────────────────────────────────────────
# Pré-génération du PDF dans session_state (appelée AVANT l'affichage du bouton)
# ─────────────────────────────────────────────────────────────────────────────

def generer_pdf_session(
    espece: str,
    periode_label: str,
    periode_cle: str,
    ssp_choisi: str | None,
    mode_visu: str,
) -> None:
    """
    Génère silencieusement le PDF complet et le stocke dans st.session_state.
    Appelée dans app.py AVANT d'afficher le bouton de téléchargement.
    Ne produit aucun rendu visible dans la page.
    """
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
        titre_carte = f"{espece}  ·  Période actuelle (1970-2000)"
    else:
        titre_carte = f"{espece}  ·  {periode_label} | {ssp_choisi}"
    if est_binaire:
        titre_carte += "  ·  Absence/Présence"

    mode_figure = "binaire" if est_binaire else "continu"
    fig = creer_figure(data, bounds, titre_carte, mode=mode_figure)

    photo_url, attribution = get_photo_espece(espece)

    pdf_bytes = _generer_pdf_complet(
        espece=espece,
        periode_label=periode_label,
        ssp_choisi=ssp_choisi,
        photo_url=photo_url,
        attribution=attribution,
        fig=fig,
    )

    nom_fichier = _construire_nom_fichier(espece, periode_label, ssp_choisi, est_binaire)
    st.session_state["pdf_complet_bytes"] = pdf_bytes
    st.session_state["pdf_complet_nom"]   = f"{nom_fichier}_complet.pdf"


# ─────────────────────────────────────────────────────────────────────────────
# Fonction principale d'affichage
# ─────────────────────────────────────────────────────────────────────────────

def render_map_section(
    espece: str,
    periode_label: str,
    periode_cle: str,
    ssp_choisi: str | None,
    mode_visu: str,
) -> None:

    # ── 1. PHOTO iNaturalist ──────────────────────────────────────────────────
    PHOTO_WIDTH_PX = 400
    photo_url, attribution = get_photo_espece(espece)

    if photo_url:
        col_photo, col_info = st.columns([1, 3])
        with col_photo:
            st.markdown(
                f'<img src="{photo_url}" width="{PHOTO_WIDTH_PX}" '
                f'style="border-radius:8px;max-width:100%;" '
                f'alt="{espece}"/>',
                unsafe_allow_html=True,
            )
            legende_html = f"<em>{espece}</em>"
            if attribution:
                auteur = attribution.lstrip("© ").lstrip("(c) ")
                legende_html += f" © {auteur}"
            st.markdown(
                f'<p style="font-size:0.75rem;color:#6b7280;margin-top:4px;">'
                f'{legende_html}</p>',
                unsafe_allow_html=True,
            )
        with col_info:
            st.markdown(
                f"<h3 style='margin-bottom:8px;'><em>{espece}</em></h3>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"**Période :** {periode_label}  \n"
                f"**Scénario :** {ssp_choisi if ssp_choisi else 'Période actuelle'}"
            )
    else:
        st.markdown(
            f"<h3 style='margin-bottom:8px;'><em>{espece}</em></h3>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"**Période :** {periode_label}  \n"
            f"**Scénario :** {ssp_choisi if ssp_choisi else 'Période actuelle'}"
        )
        st.info("Aucune photo disponible sur iNaturalist pour cette espèce.")

    st.divider()

    # ── 2. CHEMIN RASTER ─────────────────────────────────────────────────────
    est_binaire = (mode_visu == "Absence/Présence")
    racine = data_cartographies_root()

    try:
        chemin_tif = construire_chemin(
            racine, espece, periode_cle, ssp_choisi, binaire=est_binaire
        )
    except ValueError as e:
        st.warning(str(e))
        return

    if not chemin_tif.exists():
        st.warning(
            f"**Fichier introuvable :** \n`{chemin_tif}` \n\n"
            "Vérifiez que les prédictions ont bien été générées pour cette combinaison."
        )
        st.stop()

    # ── 3. CHARGEMENT DU RASTER ───────────────────────────────────────────────
    try:
        data, bounds = charger_raster(str(chemin_tif))
    except Exception as e:
        st.error(f"Erreur lors de la lecture du fichier TIF : \n`{e}`")
        st.stop()

    # ── 4. FIGURE ─────────────────────────────────────────────────────────────
    if periode_cle == "current":
        titre_carte = f"{espece}  ·  Période actuelle (1970-2000)"
    else:
        titre_carte = f"{espece}  ·  {periode_label} | {ssp_choisi}"
    if est_binaire:
        titre_carte += "  ·  Absence/Présence"

    mode_figure = "binaire" if est_binaire else "continu"
    fig = creer_figure(data, bounds, titre_carte, mode=mode_figure)
    st.pyplot(fig, use_container_width=True)

    # ── 5. TÉLÉCHARGEMENTS (zone carte - sans PDF complet, déjà en haut) ─────
    st.markdown("#### Télécharger la carte sélectionnée")

    nom_fichier = _construire_nom_fichier(espece, periode_label, ssp_choisi, est_binaire)

    dl1, dl2, dl3, dl4 = st.columns(4)

    with dl1:
        st.download_button(
            label="PNG",
            data=figure_en_bytes(fig, "png"),
            file_name=f"{nom_fichier}.png",
            mime="image/png",
            use_container_width=True,
        )
    with dl2:
        st.download_button(
            label="JPG",
            data=figure_en_bytes(fig, "jpeg"),
            file_name=f"{nom_fichier}.jpg",
            mime="image/jpeg",
            use_container_width=True,
        )
    with dl3:
        st.download_button(
            label="PDF",
            data=figure_en_bytes(fig, "pdf"),
            file_name=f"{nom_fichier}.pdf",
            mime="application/pdf",
            use_container_width=True,
        )
    with dl4:
        with open(chemin_tif, "rb") as f:
            tif_brut = f.read()
        st.download_button(
            label="TIF",
            data=tif_brut,
            file_name=f"{nom_fichier}.tif",
            mime="image/tiff",
            use_container_width=True,
        )
