# =============================================================================
# configuration_style.py
# Fichier centralisé de configuration du tableau de bord
# Modifiez ce fichier pour personnaliser l'apparence sans toucher au code
# =============================================================================


# ─────────────────────────────────────────────────────────────────────────────
# POLICES D'ÉCRITURE
# ─────────────────────────────────────────────────────────────────────────────
#
# Pour changer une police, remplacez simplement le nom entre guillemets.
# Quelques polices disponibles sans installation (Google Fonts) :
#
#   Sans-serif (modernes, lisibles) :
#       "Roboto", "Open Sans", "Lato", "Nunito", "Poppins",
#       "Inter", "Montserrat", "Raleway", "Source Sans 3"
#
#   Serif (classiques, élégants) :
#       "Merriweather", "Playfair Display", "Lora", "EB Garamond"
#
#   Monospace (technique, code) :
#       "Roboto Mono", "Source Code Pro", "JetBrains Mono"
#
#   Valeur spéciale "inherit" = police par défaut de Streamlit (sans changement)
#
# IMPORTANT : si vous choisissez une police Google Fonts, elle sera chargée
# automatiquement. Pas besoin d'installation.
# ─────────────────────────────────────────────────────────────────────────────

# Police principale : corps du texte, labels, boutons, sidebar
#       "Roboto", "Open Sans", "Lato", "Nunito", "Poppins",
POLICE_PRINCIPALE = "Times New Roman"

# Police des titres : header principal, titres de section
POLICE_TITRES = "Times New Roman"

# Police des onglets
POLICE_ONGLETS = "Times New Roman"

# Pour désactiver une police personnalisée et revenir au défaut Streamlit,
# remplacez sa valeur par : "inherit"


# ─────────────────────────────────────────────────────────────────────────────
# COULEURS PRINCIPALES
# ─────────────────────────────────────────────────────────────────────────────

# Couleur verte principale (titres, bordures actives, accents)
COULEUR_PRINCIPALE = "#1b5e35"

# Variante plus claire pour les survols et fonds légers
COULEUR_PRINCIPALE_CLAIRE = "#f0faf3"

# Bordure légère autour des éléments actifs
COULEUR_BORDURE_ACTIVE = "#d1e7d6"

# Couleur du texte discret (sous-titres, légendes)
COULEUR_TEXTE_DISCRET = "#6b7280"

# Couleur du texte standard dans la sidebar et les labels
COULEUR_TEXTE_STANDARD = "#374151"

# Couleur des textes secondaires très discrets (footer, mentions)
COULEUR_TEXTE_FOOTER = "#9ca3af"

# Fond de la sidebar et de l'en-tête
COULEUR_FOND_SIDEBAR = "#f8faf9"

# Couleur de la bordure séparatrice
COULEUR_BORDURE = "#e5e7eb"

# ─────────────────────────────────────────────────────────────────────────────
# COULEURS DES SCÉNARIOS SSP
# ─────────────────────────────────────────────────────────────────────────────

SSP_COULEURS = {
    "SSP 126": "#2e7d32",   # vert foncé
    "SSP 245": "#f9a825",   # ambre
    "SSP 370": "#e65100",   # orange foncé
    "SSP 585": "#b71c1c",   # rouge foncé
}

# Couleur du texte sur fond SSP (blanc ou noir selon contraste)
SSP_COULEURS_TEXTE = {
    "SSP 126": "#ffffff",
    "SSP 245": "#1a1a1a",
    "SSP 370": "#ffffff",
    "SSP 585": "#ffffff",
}


# ─────────────────────────────────────────────────────────────────────────────
# TYPOGRAPHIE - TAILLES
# ─────────────────────────────────────────────────────────────────────────────

# Taille du titre principal dans l'en-tête
TAILLE_TITRE_HEADER = "1.7rem"

# Taille du sous-titre principal (sous le header)
TAILLE_SOUS_TITRE = "0.9rem"

# Taille des labels de section dans la sidebar
TAILLE_LABEL_SIDEBAR = "0.82rem"

# Taille du titre de navigation (nom de l'application) dans la sidebar
TAILLE_TITRE_SIDEBAR = "1.2rem"

# Taille du sous-titre de la sidebar
TAILLE_SOUS_TITRE_SIDEBAR = "0.78rem"

# Taille du texte d'espèce sélectionnée (affiché en italique)
TAILLE_TEXTE_ESPECE = "0.78rem"

# Taille des onglets
TAILLE_ONGLETS = "1rem"

# Taille du texte des boutons SSP
TAILLE_BOUTON_SSP = "0.82rem"

# Taille du texte du footer sidebar
TAILLE_FOOTER_SIDEBAR = "0.72rem"

# Taille du texte des références dans le footer
TAILLE_REFS_FOOTER = "0.70rem"


# ─────────────────────────────────────────────────────────────────────────────
# BOUTONS GÉNÉRAUX
# ─────────────────────────────────────────────────────────────────────────────

# Couleur du texte des boutons
BOUTON_COULEUR_TEXTE = "#1b5e20"

# Fond des boutons (au repos)
BOUTON_FOND = "white"

# Couleur de bordure des boutons
BOUTON_BORDURE = "#1b5e20"

# Rayon de courbure des boutons
BOUTON_RADIUS = "6px"

# Hauteur minimale des boutons
BOUTON_HAUTEUR_MIN = "2.8em"

# Fond au survol des boutons
BOUTON_FOND_SURVOL = "#1b5e20"

# Couleur du texte au survol des boutons
BOUTON_TEXTE_SURVOL = "white"


# ─────────────────────────────────────────────────────────────────────────────
# BOUTONS SSP
# ─────────────────────────────────────────────────────────────────────────────

# Rayon des boutons SSP
SSP_BOUTON_RADIUS = "8px"

# Hauteur minimale des boutons SSP
SSP_BOUTON_HAUTEUR_MIN = "56px"

# Taille de la bordure des boutons SSP
SSP_BOUTON_EPAISSEUR_BORDURE = "2px"


# ─────────────────────────────────────────────────────────────────────────────
# ONGLETS
# ─────────────────────────────────────────────────────────────────────────────

# Espacement horizontal entre les onglets
ONGLET_GAP = "24px"

# Rayon des onglets (haut uniquement)
ONGLET_RADIUS = "6px 6px 0 0"

# Largeur minimale des onglets
ONGLET_LARGEUR_MIN = "180px"

# Couleur de l'onglet actif
ONGLET_COULEUR_ACTIVE = "#1b5e35"

# Fond de l'onglet actif
ONGLET_FOND_ACTIVE = "#f0faf3"

# Épaisseur du soulignement de l'onglet actif
ONGLET_EPAISSEUR_ACTIVE = "3px"

# Couleur des onglets inactifs
ONGLET_COULEUR_INACTIVE = "#6b7280"


# ─────────────────────────────────────────────────────────────────────────────
# ESPACEMENTS ET DIMENSIONS
# ─────────────────────────────────────────────────────────────────────────────

# Padding du contenu principal (haut)
PADDING_HAUT_CONTENU = "4rem"

# Padding du contenu principal (bas)
PADDING_BAS_CONTENU = "2rem"

# Hauteur de l'espace entre le sous-titre et le reste du contenu
ESPACE_SOUS_TITRE = "12px"




# Hauteur maximale des logos partenaires
LOGO_HAUTEUR_MAX = "56px"


# ─────────────────────────────────────────────────────────────────────────────
# CHARGEMENT AUTOMATIQUE DES POLICES GOOGLE FONTS
# ─────────────────────────────────────────────────────────────────────────────
# Ne pas modifier cette section - elle génère automatiquement le lien
# vers Google Fonts en fonction des polices choisies ci-dessus.
# ─────────────────────────────────────────────────────────────────────────────

def _google_fonts_url() -> str:
    """Génère l'URL Google Fonts pour les polices configurées."""
    polices = set()
    for p in [POLICE_PRINCIPALE, POLICE_TITRES, POLICE_ONGLETS]:
        if p and p.lower() != "inherit":
            polices.add(p)
    if not polices:
        return ""
    params = "&".join(
        f"family={p.replace(' ', '+')}:wght@300;400;500;600;700"
        for p in sorted(polices)
    )
    return f"https://fonts.googleapis.com/css2?{params}&display=swap"

GOOGLE_FONTS_URL = _google_fonts_url()