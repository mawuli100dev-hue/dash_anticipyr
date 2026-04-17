# dash_anticipyr/core/inaturalist.py

import requests
import streamlit as st


@st.cache_data(ttl=3600)  # cache 1h pour ne pas refaire l'appel à chaque interaction
def get_photo_espece(nom_scientifique: str) -> str | None:
    """
    Appelle l'API iNaturalist et retourne l'URL de la photo
    de représentation de l'espèce, ou None si introuvable.
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
        return None  # pas de crash si pas de réseau

    if response.status_code != 200:
        return None

    resultats = response.json().get("results", [])

    if not resultats:
        return None

    taxon = resultats[0]
    default_photo = taxon.get("default_photo")

    if default_photo:
        return default_photo.get("medium_url")

    return None
