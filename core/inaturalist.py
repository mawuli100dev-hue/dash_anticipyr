# dash_anticipyr/core/inaturalist.py

from __future__ import annotations

import requests
import streamlit as st


@st.cache_data(ttl=3600)
def get_photo_espece(nom_scientifique: str) -> tuple[str | None, str | None]:
    """
    Appelle l'API iNaturalist et retourne un tuple (photo_url, attribution).

    - photo_url   : URL de la photo medium, ou None si introuvable
    - attribution : texte de copyright de l'auteur, ex. "(c) Jean Dupont, some rights reserved"
                    ou None si indisponible

    L'API iNaturalist fournit l'attribution dans default_photo["attribution"].
    On la reformate en "© Auteur" pour l'affichage en légende.
    """
    url = "https://api.inaturalist.org/v1/taxa"
    params = {
        "q": nom_scientifique,
        "rank": "species",
        "per_page": 1,
    }

    try:
        response = requests.get(url, params=params, timeout=5)
    except requests.exceptions.RequestException:
        return None, None

    if response.status_code != 200:
        return None, None

    resultats = response.json().get("results", [])
    if not resultats:
        return None, None

    taxon = resultats[0]

    photo_url = None
    default_photo = taxon.get("default_photo")

    if not default_photo:
        return None, None

    photo_url   = default_photo.get("medium_url")
    attribution = default_photo.get("attribution")  # ex: "(c) Jean Dupont, some rights reserved"

    # Reformatage : "(c) Jean Dupont, ..." -> "© Jean Dupont, ..."
    if attribution:
        attribution = attribution.replace("(c)", "©").replace("(C)", "©")
        attribution = attribution.split(",")[0].strip()

    return photo_url, attribution
