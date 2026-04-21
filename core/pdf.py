# core\pdf.py
from __future__ import annotations

from io import BytesIO
from urllib.request import urlopen

from PIL import Image
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

from dash_anticipyr.core.raster import figure_en_bytes
from dash_anticipyr.core.translations import t


def telecharger_image(url: str) -> BytesIO | None:
    try:
        with urlopen(url, timeout=10) as response:
            return BytesIO(response.read())
    except Exception:
        return None


def construire_nom_fichier(
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


def generer_pdf_complet(
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
    c.drawString(marge, y, t("page_title"))

    y -= 22
    c.setFont("Helvetica-Oblique", 10)
    c.setFillColorRGB(0.42, 0.45, 0.50)
    c.drawString(marge, y, t("main_subtitle"))

    y -= 18
    c.setStrokeColorRGB(0.85, 0.85, 0.85)
    c.line(marge, y, largeur_page - marge, y)
    y -= 20

    photo_largeur_max = 190
    photo_hauteur_max = 145
    x_photo = marge
    x_texte = marge + photo_largeur_max + 20

    if photo_url:
        image_stream = telecharger_image(photo_url)
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

    label_periode  = t("map_periode_label") + " :"
    label_scenario = t("map_scenario_label") + " :"
    valeur_scenario = ssp_choisi if ssp_choisi else t("map_periode_actuelle")

    y_info = y - 50
    c.setFont("Helvetica-Bold", 11)
    c.setFillColorRGB(0.22, 0.22, 0.22)
    c.drawString(x_texte, y_info, label_periode)
    c.setFont("Helvetica", 11)
    c.drawString(x_texte + 58, y_info, periode_label)

    y_info -= 22
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x_texte, y_info, label_scenario)
    c.setFont("Helvetica", 11)
    c.drawString(x_texte + 63, y_info, valeur_scenario)

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
    c.drawImage(
        ImageReader(image_carte),
        x_carte, y_carte - hauteur_aff,
        width=largeur_aff, height=hauteur_aff,
        preserveAspectRatio=True,
        mask="auto",
    )

    c.showPage()
    c.save()
    buffer_pdf.seek(0)
    return buffer_pdf.getvalue()
