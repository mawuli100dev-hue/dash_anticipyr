from __future__ import annotations

import streamlit as st

from dash_anticipyr.core.locales.fr import TEXTES_FR
from dash_anticipyr.core.locales.en import TEXTES_EN
from dash_anticipyr.core.locales.es import TEXTES_ES
from dash_anticipyr.core.locales.ca import TEXTES_CA

# ---------------------------------------------------------------------------
# Assemblage
# ---------------------------------------------------------------------------

TEXTES: dict[str, dict[str, str]] = {
    "fr": TEXTES_FR,
    "en": TEXTES_EN,
    "es": TEXTES_ES,
    "ca": TEXTES_CA,
}

LANGUES = {
    "fr": "🇫🇷 Français",
    "en": "🇬🇧 English",
    "es": "🇪🇸 Español",
    "ca": "🏴 Català",
}

# ---------------------------------------------------------------------------
# API publique - identique à avant, rien à changer dans les autres fichiers
# ---------------------------------------------------------------------------

def init_langue() -> None:
    if "langue" not in st.session_state:
        st.session_state["langue"] = "fr"


def t(cle: str, **kwargs) -> str:
    langue = st.session_state.get("langue", "fr")
    textes_langue = TEXTES.get(langue, TEXTES["fr"])
    texte = textes_langue.get(cle, TEXTES["fr"].get(cle, cle))
    if kwargs:
        try:
            texte = texte.format(**kwargs)
        except KeyError:
            pass
    return texte


def get_langue_courante() -> str:
    return st.session_state.get("langue", "fr")
