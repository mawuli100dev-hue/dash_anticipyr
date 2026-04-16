# =============================================================================
# dashboard_botanique.py
# Tableau de bord — Modélisation des Habitats Botaniques Pyrénéens
# BUT2 Science des Données — Stage ANTICI'PYR
# =============================================================================

import streamlit as st
import rasterio
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import io
from pathlib import Path

# ─── 1. CONFIGURATION DE LA PAGE ─────────────────────────────────────────────
st.set_page_config(
    page_title="Flore Pyrénéenne — Habitats",
    page_icon="H",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styles CSS
st.markdown("""
<style>
    .block-container { padding-top: 1.2rem; padding-bottom: 2rem; }
    .main-title  { font-size:2rem; font-weight:700; color:#1b5e35; margin-bottom:0; }
    .subtitle    { color:#5a8f72; font-size:0.95rem; margin-top:0; margin-bottom:1rem; }
    .info-badge  { background:#e8f5e9; border-left:4px solid #388e3c;
                   padding:8px 14px; border-radius:0 6px 6px 0;
                   font-size:0.88rem; color:#1b5e35; }
    div[data-testid="stMetric"] { background:#f4faf6; border-radius:8px;
                                  padding:6px 12px; }
    div[data-testid="stDownloadButton"] > button {
        width:100%; border-radius:6px; font-weight:600;
    }
</style>
""", unsafe_allow_html=True)


# ─── 2. CONSTANTES ────────────────────────────────────────────────────────────

# Correspondance : label affiché → clé interne ("current" ou année de projection)
PERIODES = {
    "1970–2000  (Actuelle)": "current",
    "2021–2040":             "2030",
    "2041–2060":             "2050",
    "2061–2080":             "2070",
    "2081–2100":             "2090",
}

# Scénarios climatiques disponibles
SSP_LIST = ["SSP 126", "SSP 245", "SSP 370", "SSP 585"]


# ─── 3. FONCTIONS UTILITAIRES ─────────────────────────────────────────────────

@st.cache_data
def lister_especes(dossier_racine: str) -> list:
    """
    Parcourt le dossier racine et retourne la liste triée
    des espèces (= sous-dossiers).
    Le décorateur @st.cache_data évite de re-scanner le disque à chaque clic.
    """
    racine = Path(dossier_racine)
    if not racine.exists():
        return []
    return sorted([d.name for d in racine.iterdir() if d.is_dir()])


def construire_chemin(racine: Path, espece: str,
                      periode_cle: str, ssp: str) -> Path:
    """
    Construit le chemin vers le fichier .tif selon les paramètres choisis.

    Exemples de chemins construits :
      • période actuelle  → <espece>/Median_current_projection.tif
      • 2021-2040, SSP126 → <espece>/pred_maps_futur_2030/126_2030_median.tif
    """
    base = racine / espece

    if periode_cle == "current":
        return base / "Median_current_projection.tif"

    # Extraire le numéro SSP : "SSP 126" → "126"
    ssp_num = ssp.replace("SSP ", "")
    dossier = f"pred_maps_futur_{periode_cle}"       # ex. pred_maps_futur_2030
    fichier = f"{ssp_num}_{periode_cle}_median.tif"  # ex. 126_2030_median.tif
    return base / dossier / fichier


@st.cache_data
def charger_raster(chemin_str: str):
    """
    Charge un raster GeoTIFF avec rasterio.
    Retourne :
        data   → tableau numpy 2D (valeurs entre 0 et 1)
        bounds → étendue géographique (left, bottom, right, top)

    Note : on passe chemin_str (str) et non Path car cache_data
    sérialise les arguments pour les comparer ; Path fonctionne aussi
    mais str est plus sûr.
    """
    with rasterio.open(chemin_str) as src:
        data   = src.read(1).astype(float)   # Lire la première bande
        bounds = src.bounds                  # Coordonnées géographiques
        nodata = src.nodata                  # Valeur "hors zone"

    # Remplacer la valeur nodata par NaN (non affiché sur la carte)
    if nodata is not None:
        data[data == nodata] = np.nan

    return data, bounds


def creer_figure(data: np.ndarray, bounds, titre: str) -> plt.Figure:
    """
    Crée la figure matplotlib de la carte de distribution.
    Palette viridis (bleu → jaune) : recommandée pour les daltoniens.
    """
    fig, ax = plt.subplots(figsize=(11, 7))

    # Masquer les NaN pour l'affichage (pixels hors zone d'étude)
    masked = np.ma.masked_invalid(data)

    # Affichage du raster
    img = ax.imshow(
        masked,
        cmap="viridis",
        extent=[bounds.left, bounds.right, bounds.bottom, bounds.top],
        origin="upper",
        vmin=0.0,
        vmax=1.0,
        interpolation="nearest"
    )

    # ── Légende (barre de couleur) ──────────────────────────────
    cbar = fig.colorbar(img, ax=ax, fraction=0.034, pad=0.02)
    cbar.set_label("Probabilité de présence", fontsize=11, labelpad=10)
    cbar.set_ticks([0.0, 0.25, 0.5, 0.75, 1.0])
    cbar.set_ticklabels(["0.0\n(Absent)", "0.25", "0.50", "0.75", "1.0\n(Présent)"],
                        fontsize=9)

    # ── Axes ────────────────────────────────────────────────────
    ax.set_xlabel("Longitude (°)", fontsize=10)
    ax.set_ylabel("Latitude (°)",  fontsize=10)
    ax.set_title(titre, fontsize=13, fontweight="bold", pad=12)
    ax.tick_params(labelsize=8)
    ax.grid(True, linewidth=0.3, alpha=0.4, color="white")

    fig.tight_layout()
    return fig


def figure_en_bytes(fig: plt.Figure, fmt: str, dpi: int = 150) -> bytes:
    """
    Convertit une figure matplotlib en flux d'octets
    pour le téléchargement via st.download_button.
    """
    buf = io.BytesIO()
    fig.savefig(buf, format=fmt, dpi=dpi, bbox_inches="tight")
    buf.seek(0)
    return buf.read()


# ─── 4. INTERFACE UTILISATEUR ─────────────────────────────────────────────────

# ── En-tête ────────────────────────────────────────────────────────────────────
st.markdown('<p class="main-title">Flore Pyrénéenne — Modélisation des Habitats</p>',
            unsafe_allow_html=True)
 


# ── SIDEBAR : sélection de l'espèce ───────────────────────────────────────────
with st.sidebar:
    st.header("Espèce étudiée")

    # --- Chemin en dur vers les cartes ---
    dossier_racine_defaut = str(
        (Path(__file__).resolve().parent / "data" / "cartographies")
    )

    # --- Liste des espèces ---
    especes = lister_especes(dossier_racine_defaut)

    if not especes:
        st.error("Aucune espèce trouvée.\n"
                 "Vérifiez que les dossiers existent dans `dash_anticipyr/data/cartographies/`.")
        st.stop()

    st.caption(f"**{len(especes)}** espèce(s) disponible(s)")

    # --- Liste déroulante "recherchable" (Streamlit) ---
    # La recherche se fait en ouvrant la liste puis en tapant dans la boîte.
    # L'option vide permet "d'effacer" la sélection.
    especes_options = [""] + especes
    st.caption("Cliquez puis commencez à taper pour filtrer.")

    if "espece_selectionnee" not in st.session_state:
        st.session_state.espece_selectionnee = especes[0]

    index = especes_options.index(st.session_state.espece_selectionnee) if st.session_state.espece_selectionnee in especes else 1

    espece = st.selectbox(
        "Nom de l'espèce",
        options=especes_options,
        index=index,
        key="espece_selectionnee",
        help="Tapez après ouverture pour filtrer la liste."
    )

    if not espece:
        st.warning("Sélectionnez une espèce dans la liste.")
        st.stop()

    # --- Sélection période + scénario ---
    st.divider()
    periode_label = st.selectbox(
        "Période de projection",
        options=list(PERIODES.keys())
    )
    periode_cle = PERIODES[periode_label]

    if periode_cle == "current":
        st.info(
            "**Pas de scénario SSP pour la période 1970–2000.**  \n"
            "Ces données correspondent aux observations climatiques actuelles."
        )
        ssp_choisi = None
    else:
        ssp_choisi = st.selectbox(
            "Scénario climatique (SSP)",
            options=SSP_LIST,
            help="SSP 126 = scénario optimiste  ·  SSP 585 = scénario pessimiste"
        )


# ── CHARGEMENT DU RASTER ──────────────────────────────────────────────────────
racine = Path(__file__).resolve().parent / "data" / "cartographies"
chemin_tif = construire_chemin(racine, espece, periode_cle, ssp_choisi)

if not chemin_tif.exists():
    st.warning(
        f"**Fichier introuvable :**  \n`{chemin_tif}`  \n\n"
        "Vérifiez que les prédictions ont bien été générées pour cette combinaison."
    )
    st.stop()

try:
    data, bounds = charger_raster(str(chemin_tif))
except Exception as e:
    st.error(f"Erreur lors de la lecture du fichier TIF :  \n`{e}`")
    st.stop()


# ── CONSTRUCTION DU TITRE ─────────────────────────────────────────────────────
if periode_cle == "current":
    titre_carte = f"{espece}  ·  Période actuelle (1970–2000)"
else:
    titre_carte = f"{espece}  ·  {periode_label}  |  {ssp_choisi}"


# ── AFFICHAGE DE LA CARTE ─────────────────────────────────────────────────────
fig = creer_figure(data, bounds, titre_carte)
st.pyplot(fig, use_container_width=True)


# ── TÉLÉCHARGEMENT ────────────────────────────────────────────────────────────
st.markdown("#### Télécharger la carte sélectionnée")

# Construction du nom de fichier propre (sans espaces ni caractères spéciaux)
nom_fichier = (
    espece.replace(" ", "_")
    + "_"
    + periode_label.replace("–", "-").replace(" ", "_").replace("(", "").replace(")", "")
)
if ssp_choisi:
    nom_fichier += "_" + ssp_choisi.replace(" ", "")

dl1, dl2, dl3, dl4 = st.columns(4)

with dl1:
    st.download_button(
        label="PNG",
        data=figure_en_bytes(fig, "png"),
        file_name=f"{nom_fichier}.png",
        mime="image/png",
        use_container_width=True
    )

with dl2:
    st.download_button(
        label="JPG",
        data=figure_en_bytes(fig, "jpeg"),
        file_name=f"{nom_fichier}.jpg",
        mime="image/jpeg",
        use_container_width=True
    )

with dl3:
    st.download_button(
        label="PDF",
        data=figure_en_bytes(fig, "pdf"),
        file_name=f"{nom_fichier}.pdf",
        mime="application/pdf",
        use_container_width=True
    )

with dl4:
    # Le TIF original est fourni tel quel (sans re-traitement)
    with open(chemin_tif, "rb") as f:
        tif_brut = f.read()
    st.download_button(
        label="TIF (original)",
        data=tif_brut,
        file_name=f"{nom_fichier}.tif",
        mime="image/tiff",
        use_container_width=True
    )

# Libération mémoire
plt.close(fig)
