from __future__ import annotations

import io
from io import BytesIO
from urllib.request import urlopen

import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Image as RLImage, Paragraph, Spacer, PageBreak

from PIL import Image
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

from dash_anticipyr.core.raster import figure_en_bytes
from dash_anticipyr.core.translations import t

from pathlib import Path
from dash_anticipyr.core.translations import get_langue_courante


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




def _page_ssp(c, largeur_page: int, hauteur_page: int, marge: int, figure_ssp_langue: Path | None = None, figure_ssp_projections: Path | None = None,) -> None:
    """Page SSP : tableau des 4 scénarios avec températures et précipitations."""
    from dash_anticipyr.core.translations import t

    SSP_DATA = [
        {"ssp": "SSP 126", "couleur": (0.18, 0.49, 0.20), "dt": "+2,16 °C",  "dp": "-3,56 mm"},
        {"ssp": "SSP 245", "couleur": (0.87, 0.59, 0.04), "dt": "+3,29 °C",  "dp": "-52,6 mm"},
        {"ssp": "SSP 370", "couleur": (0.90, 0.32, 0.00), "dt": "+4,6 °C",   "dp": "-97,98 mm"},
        {"ssp": "SSP 585", "couleur": (0.72, 0.11, 0.11), "dt": "+6,14 °C",  "dp": "-132,36 mm"},
    ]

    y = hauteur_page - marge

    # Titre
    c.setFont("Helvetica-Bold", 16)
    c.setFillColorRGB(0.106, 0.369, 0.208)
    c.drawString(marge, y, t("page_title"))

    y -= 22
    c.setFont("Helvetica-Bold", 13)
    c.setFillColorRGB(0.22, 0.22, 0.22)
    c.drawString(marge, y, t("ssp_page_titre").lstrip("#").strip())

    y -= 16
    c.setFont("Helvetica", 9)
    c.setFillColorRGB(0.42, 0.45, 0.50)

    # Intro (wrap simple)
    intro = t("ssp_intro")
    mots = intro.split()
    ligne = ""
    for mot in mots:
        test = ligne + " " + mot if ligne else mot
        if c.stringWidth(test, "Helvetica", 9) < largeur_page - 2 * marge:
            ligne = test
        else:
            c.drawString(marge, y, ligne)
            y -= 13
            ligne = mot
    if ligne:
        c.drawString(marge, y, ligne)
        y -= 18

    c.setStrokeColorRGB(0.85, 0.85, 0.85)
    c.line(marge, y, largeur_page - marge, y)
    y -= 16

    # Cartes SSP
    card_w = (largeur_page - 2 * marge - 9) // 4
    card_h = 160
    x = marge

    for ssp in SSP_DATA:
        r, g, b = ssp["couleur"]
        # Bordure gauche colorée
        c.setFillColorRGB(r, g, b)
        c.rect(x, y - card_h, 4, card_h, fill=1, stroke=0)

        # Fond carte
        c.setFillColorRGB(0.976, 0.976, 0.976)
        c.rect(x + 4, y - card_h, card_w - 4, card_h, fill=1, stroke=0)

        # Titre SSP
        c.setFillColorRGB(r, g, b)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(x + 10, y - 16, ssp["ssp"])

        # Label
        label = t(f"ssp_{ssp['ssp'].replace('SSP ', '')}_label")
        c.setFillColorRGB(0.27, 0.27, 0.27)
        c.setFont("Helvetica-Bold", 8)
        # wrap label sur 2 lignes max
        mots_l = label.split()
        l1, l2 = "", ""
        for mot in mots_l:
            test = l1 + " " + mot if l1 else mot
            if c.stringWidth(test, "Helvetica-Bold", 8) < card_w - 14:
                l1 = test
            else:
                l2 = (l2 + " " + mot).strip()
        c.drawString(x + 10, y - 30, l1)
        if l2:
            c.drawString(x + 10, y - 41, l2)

        # Description
        desc = t(f"ssp_{ssp['ssp'].replace('SSP ', '')}_description")
        c.setFont("Helvetica", 7)
        c.setFillColorRGB(0.40, 0.40, 0.40)
        mots_d = desc.split()
        yl = y - 56
        ligne_d = ""
        for mot in mots_d:
            test = ligne_d + " " + mot if ligne_d else mot
            if c.stringWidth(test, "Helvetica", 7) < card_w - 14:
                ligne_d = test
            else:
                if yl > y - card_h + 30:
                    c.drawString(x + 10, yl, ligne_d)
                    yl -= 10
                ligne_d = mot
        if ligne_d and yl > y - card_h + 30:
            c.drawString(x + 10, yl, ligne_d)

        # Valeurs T et P - empilées verticalement pour éviter le chevauchement
        c.setFont("Helvetica-Bold", 7)
        c.setFillColorRGB(0.22, 0.22, 0.22)
        c.drawString(x + 10, y - card_h + 36, t("ssp_temperature"))
        c.setFont("Helvetica", 8)
        c.drawString(x + 10, y - card_h + 26, ssp["dt"])

        c.setFont("Helvetica-Bold", 7)
        c.setFillColorRGB(0.22, 0.22, 0.22)
        c.drawString(x + 10, y - card_h + 16, t("ssp_precipitations"))
        c.setFont("Helvetica", 8)
        c.drawString(x + 10, y - card_h + 6, ssp["dp"])

        x += card_w + 3

    y -= card_h + 20

    # Tableau récap
    c.setStrokeColorRGB(0.85, 0.85, 0.85)
    c.line(marge, y, largeur_page - marge, y)
    y -= 14

        # Figures SSP (reproduites depuis l'onglet SSP INFO)
    y -= 10

    def _inserer_image(chemin: Path, largeur_max: int, hauteur_max: int, x_centre: int):
        nonlocal y
        if chemin is None or not chemin.exists():
            return
        try:
            img_orig  = Image.open(str(chemin)).convert("RGBA")

            fond_blanc = Image.new("RGBA", img_orig.size, (255, 255, 255, 255))
            fond_blanc.paste(img_orig, mask=img_orig.split()[3])  # canal alpha comme masque

            img = fond_blanc.convert("RGB")

            ratio = img.width / img.height
            larg = min(largeur_max, hauteur_max * ratio)
            haut = larg / ratio
            if haut > hauteur_max:
                haut = hauteur_max
                larg = haut * ratio
            x_pos = x_centre - larg / 2
            c.drawImage(
                ImageReader(img),
                x_pos, y - haut,
                width=larg, height=haut,
                preserveAspectRatio=True,
                mask="auto",
            )
            y -= haut + 8
        except Exception:
            pass

    largeur_dispo = largeur_page - 2 * marge
    x_centre = largeur_page // 2

    # Figure 1 : ssp_{langue}.png (centrée, largeur réduite comme dans l'onglet)
    _inserer_image(figure_ssp_langue, largeur_dispo // 2, 160, x_centre)

    # Figure 2 : ssp_projections.png (pleine largeur)
    _inserer_image(figure_ssp_projections, largeur_dispo, 200, x_centre)

    c.setFont("Helvetica-Bold", 10)
    c.setFillColorRGB(0.106, 0.369, 0.208)
    titre_recap = t("ssp_recap_titre").lstrip("#").strip()
    largeur_max_titre = largeur_page - 2 * marge
    # Coupe le titre sur deux lignes si trop long
    mots_titre = titre_recap.split()
    ligne1, ligne2 = "", ""
    for mot in mots_titre:
        test = ligne1 + " " + mot if ligne1 else mot
        if c.stringWidth(test, "Helvetica-Bold", 10) <= largeur_max_titre:
            ligne1 = test
        else:
            ligne2 = (ligne2 + " " + mot).strip()
    c.drawString(marge, y, ligne1)
    if ligne2:
        y -= 13
        c.drawString(marge, y, ligne2)
    y -= 14

    # En-tête tableau
    col_w = [(largeur_page - 2 * marge) * p for p in [0.12, 0.38, 0.25, 0.25]]
    cols_x = [marge]
    for w in col_w[:-1]:
        cols_x.append(cols_x[-1] + w)

    headers = [
        t("ssp_recap_col_ssp"),
        t("ssp_recap_col_emissions"),
        t("ssp_recap_col_dt"),
        t("ssp_recap_col_dp"),
    ]
    c.setFillColorRGB(0.90, 0.95, 0.91)
    c.rect(marge, y - 14, largeur_page - 2 * marge, 14, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 9)
    c.setFillColorRGB(0.10, 0.10, 0.10)
    for i, h in enumerate(headers):
        c.drawString(cols_x[i] + 4, y - 10, h)
    y -= 14

    couleurs_ssp = [
        (0.18, 0.49, 0.20),
        (0.87, 0.59, 0.04),
        (0.90, 0.32, 0.00),
        (0.72, 0.11, 0.11),
    ]
    for idx, ssp in enumerate(SSP_DATA):
        bg = 0.97 if idx % 2 == 0 else 1.0
        c.setFillColorRGB(bg, bg, bg)
        c.rect(marge, y - 14, largeur_page - 2 * marge, 14, fill=1, stroke=0)

        r, g, b = couleurs_ssp[idx]
        c.setFont("Helvetica-Bold", 9)
        c.setFillColorRGB(r, g, b)
        c.drawString(cols_x[0] + 4, y - 10, ssp["ssp"])

        c.setFont("Helvetica", 9)
        c.setFillColorRGB(0.22, 0.22, 0.22)
        label = t(f"ssp_{ssp['ssp'].replace('SSP ', '')}_label")
        c.drawString(cols_x[1] + 4, y - 10, label[:45])
        c.drawString(cols_x[2] + 4, y - 10, ssp["dt"])
        c.drawString(cols_x[3] + 4, y - 10, ssp["dp"])
        y -= 14

    # Ligne de séparation finale
    c.setStrokeColorRGB(0.85, 0.85, 0.85)
    c.line(marge, y, largeur_page - marge, y)


def _page_interpretation(c, largeur_page: int, hauteur_page: int, marge: int) -> None:
    """Page interprétation : tableau des 19 variables bioclimatiques."""
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

    y = hauteur_page - marge

    # Titre
    c.setFont("Helvetica-Bold", 16)
    c.setFillColorRGB(0.106, 0.369, 0.208)
    c.drawString(marge, y, t("page_title"))

    y -= 22
    c.setFont("Helvetica-Bold", 13)
    c.setFillColorRGB(0.22, 0.22, 0.22)
    c.drawString(marge, y, "Interprétation")

    y -= 14
    c.setFont("Helvetica", 9)
    c.setFillColorRGB(0.42, 0.45, 0.50)
    largeur_max_intro = largeur_page - 2 * marge

    def _wrap_text(c, texte, x, y, largeur, police, taille, interligne=11):
        mots = texte.split()
        ligne = ""
        for mot in mots:
            test = ligne + " " + mot if ligne else mot
            if c.stringWidth(test, police, taille) <= largeur:
                ligne = test
            else:
                c.drawString(x, y, ligne)
                y -= interligne
                ligne = mot
        if ligne:
            c.drawString(x, y, ligne)
            y -= interligne
        return y

    intro1 = t("interp_intro_1").lstrip("#").strip()
    y = _wrap_text(c, intro1, marge, y, largeur_max_intro, "Helvetica", 9)
    y -= 4
    intro2 = t("interp_intro_2").lstrip("#").strip()
    y = _wrap_text(c, intro2, marge, y, largeur_max_intro, "Helvetica", 9)
    y -= 8

    c.setStrokeColorRGB(0.85, 0.85, 0.85)
    c.line(marge, y, largeur_page - marge, y)
    y -= 12

    # Colonnes du tableau
    col_w = [(largeur_page - 2 * marge) * p for p in [0.09, 0.26, 0.55, 0.10]]
    cols_x = [marge]
    for w in col_w[:-1]:
        cols_x.append(cols_x[-1] + w)

    def dessiner_section(titre: str, couleur_rgb: tuple, variables: list, y: float) -> float:
        r, g, b = couleur_rgb
        c.setFont("Helvetica-Bold", 10)
        c.setFillColorRGB(r, g, b)
        c.drawString(marge, y, titre)
        y -= 12

        # En-tête
        c.setFillColorRGB(r * 0.15 + 0.85, g * 0.15 + 0.85, b * 0.15 + 0.85)
        c.rect(marge, y - 12, largeur_page - 2 * marge, 12, fill=1, stroke=0)
        headers = [
            t("interp_col_variable"),
            t("interp_col_nom"),
            t("interp_col_description"),
            t("interp_col_unite"),
        ]
        c.setFont("Helvetica-Bold", 8)
        c.setFillColorRGB(0.10, 0.10, 0.10)
        for i, h in enumerate(headers):
            c.drawString(cols_x[i] + 3, y - 9, h)
        y -= 12

        for idx, (code, cle_nom, cle_desc, unite) in enumerate(variables):
            row_h = 13
            bg = 0.97 if idx % 2 == 0 else 1.0
            c.setFillColorRGB(bg, bg, bg)
            c.rect(marge, y - row_h, largeur_page - 2 * marge, row_h, fill=1, stroke=0)

            c.setFont("Helvetica-Bold", 8)
            c.setFillColorRGB(r, g, b)
            c.drawString(cols_x[0] + 3, y - 9, code)

            c.setFont("Helvetica", 8)
            c.setFillColorRGB(0.22, 0.22, 0.22)
            c.drawString(cols_x[1] + 3, y - 9, t(cle_nom)[:30])

            desc = t(cle_desc)
            c.drawString(cols_x[2] + 3, y - 9, desc[:70])

            c.drawString(cols_x[3] + 3, y - 9, unite)
            y -= row_h

        return y - 20

    temp_vars = [(c, n, d, u) for c, n, d, u in BIO_VARIABLES if int(c[3:]) <= 11]
    prec_vars = [(c, n, d, u) for c, n, d, u in BIO_VARIABLES if int(c[3:]) > 11]

    y = dessiner_section(t("interp_titre_temp"), (0.08, 0.40, 0.75), temp_vars, y)
    y = dessiner_section(t("interp_titre_prec"), (0.18, 0.49, 0.20), prec_vars, y)

    # Conclusion avec wrap automatique
    conclusion = t("interp_conclusion").lstrip("#").strip()
    if conclusion and y > marge + 14:
        c.setFont("Helvetica-Oblique", 8)
        c.setFillColorRGB(0.42, 0.45, 0.50)
        largeur_max_conc = largeur_page - 2 * marge
        mots_conc = conclusion.split()
        y -= 10
        ligne_conc = ""
        for mot in mots_conc:
            test = ligne_conc + " " + mot if ligne_conc else mot
            if c.stringWidth(test, "Helvetica-Oblique", 8) <= largeur_max_conc:
                ligne_conc = test
            else:
                if y > marge:
                    c.drawString(marge, y, ligne_conc)
                    y -= 11
                ligne_conc = mot
        if ligne_conc and y > marge:
            c.drawString(marge, y, ligne_conc)

def generer_pdf_multi_periodes(
    espece: str,
    photo_url: str | None,
    attribution: str | None,
    fig_current: plt.Figure | None,
    pages_futures: list[tuple[str, list[plt.Figure]]],
    est_binaire: bool = False,
) -> bytes:
    """
    Génère un PDF multi-pages :
    - Page 1 : photo + infos + carte période actuelle
    - Pages 2-5 : une page par période future avec grille 2x2 des 4 SSP
    """
    buffer_pdf = BytesIO()
    c = canvas.Canvas(buffer_pdf, pagesize=(595, 842))
    largeur_page, hauteur_page = 595, 842
    marge = 40

    # ----------------------------------------------------------------
    # PAGE 1 : période actuelle
    # ----------------------------------------------------------------
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

    y_info = y - 50
    c.setFont("Helvetica-Bold", 11)
    c.setFillColorRGB(0.22, 0.22, 0.22)
    c.drawString(x_texte, y_info, t("map_periode_label") + " :")
    c.setFont("Helvetica", 11)
    c.drawString(x_texte + 58, y_info, "1970–2000")

    y_info -= 22
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x_texte, y_info, t("map_scenario_label") + " :")
    c.setFont("Helvetica", 11)
    c.drawString(x_texte + 63, y_info, t("map_periode_actuelle"))

    if est_binaire:
        y_info -= 22
        c.setFont("Helvetica-Oblique", 10)
        c.setFillColorRGB(0.42, 0.45, 0.50)
        c.drawString(x_texte, y_info, "Absence / Présence")

    y_separateur = y - photo_hauteur_max - 28
    c.setStrokeColorRGB(0.85, 0.85, 0.85)
    c.line(marge, y_separateur, largeur_page - marge, y_separateur)

    if fig_current is not None:
        y_carte = y_separateur - 14
        img_carte_bytes = BytesIO(figure_en_bytes(fig_current, "png"))
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

    # ----------------------------------------------------------------
    # PAGES SUIVANTES : une page par période, 4 cartes SSP empilées verticalement
    # ----------------------------------------------------------------
    # Hauteur disponible par carte = (hauteur_page - marge_haut - marge_bas - en_tete) / 4
    hauteur_entete = 60  # titre page + nom espece + separateur
    hauteur_dispo_totale = hauteur_page - marge - hauteur_entete - marge
    hauteur_par_carte = hauteur_dispo_totale / 4
    largeur_max = largeur_page - 2 * marge

    for periode_label, figs_ssp in pages_futures:
        c.showPage()

        # En-tête de la page
        y = hauteur_page - marge
        c.setFont("Helvetica-Bold", 14)
        c.setFillColorRGB(0.106, 0.369, 0.208)
        c.drawString(marge, y, t("page_title"))

        y -= 22
        c.setFont("Helvetica-BoldOblique", 13)
        c.setFillColorRGB(0.22, 0.22, 0.22)
        c.drawString(marge, y, f"{espece}  ·  {periode_label}")

        if est_binaire:
            y -= 16
            c.setFont("Helvetica-Oblique", 10)
            c.setFillColorRGB(0.42, 0.45, 0.50)
            c.drawString(marge, y, "Absence / Présence")

        y -= 12
        c.setStrokeColorRGB(0.85, 0.85, 0.85)
        c.line(marge, y, largeur_page - marge, y)
        y -= 6

        # 4 cartes empilées verticalement
        for fig_ssp in figs_ssp[:4]:
            img_bytes = BytesIO(figure_en_bytes(fig_ssp, "png"))
            image_carte = Image.open(img_bytes).convert("RGB")

            ratio_carte = image_carte.width / image_carte.height
            largeur_aff = largeur_max
            hauteur_aff = largeur_aff / ratio_carte

            # Si la carte depasse le slot, on la reduit
            if hauteur_aff > hauteur_par_carte - 4:
                hauteur_aff = hauteur_par_carte - 4
                largeur_aff = hauteur_aff * ratio_carte

            x_carte = (largeur_page - largeur_aff) / 2
            c.drawImage(
                ImageReader(image_carte),
                x_carte, y - hauteur_aff,
                width=largeur_aff, height=hauteur_aff,
                preserveAspectRatio=True,
                mask="auto",
            )
            y -= hauteur_par_carte

    # ----------------------------------------------------------------
    # PAGE SSP
    # ----------------------------------------------------------------
    c.showPage()

    SSP_FIG_DIR = Path(__file__).parent.parent / "data" / "SSP_fig"
    FIGURE_SSP  = Path(__file__).parent.parent / "data" / "figures" / "ssp_projections.png"

    langue = get_langue_courante()
    figure_langue = SSP_FIG_DIR / f"ssp_{langue}.png"
    if not figure_langue.exists():
        figure_langue = SSP_FIG_DIR / "ssp_fr.png"

    _page_ssp(c, largeur_page, hauteur_page, marge,
        figure_ssp_langue=figure_langue,
        figure_ssp_projections=FIGURE_SSP,)

    # ----------------------------------------------------------------
    # PAGE INTERPRETATION
    # ----------------------------------------------------------------
    c.showPage()
    _page_interpretation(c, largeur_page, hauteur_page, marge)

    c.showPage()
    c.save()
    buffer_pdf.seek(0)
    return buffer_pdf.getvalue()
