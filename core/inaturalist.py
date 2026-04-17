# dash_anticipyr/core/inaturalist.py

from __future__ import annotations

import requests
import streamlit as st


def _get_wikipedia_summary(nom_scientifique: str, wikipedia_url: str | None) -> str | None:
    """
    Cherche un résumé Wikipedia en 2 étapes :
    1. Si wikipedia_url pointe vers Wikipedia, on l'utilise directement.
    2. Sinon, on cherche par nom scientifique (EN puis FR).
    """
    if wikipedia_url and "wikipedia.org/wiki/" in wikipedia_url:
        titre = wikipedia_url.rstrip("/").split("/wiki/")[-1]
        for langue in ("en", "fr"):
            try:
                resp = requests.get(
                    f"https://{langue}.wikipedia.org/api/rest_v1/page/summary/{titre}",
                    timeout=5,
                )
                if resp.status_code == 200:
                    extrait = resp.json().get("extract")
                    if extrait:
                        return extrait
            except requests.exceptions.RequestException:
                continue

    titre_recherche = nom_scientifique.replace(" ", "_")
    for langue in ("en", "fr"):
        try:
            resp = requests.get(
                f"https://{langue}.wikipedia.org/api/rest_v1/page/summary/{titre_recherche}",
                timeout=5,
            )
            if resp.status_code == 200:
                extrait = resp.json().get("extract")
                if extrait:
                    return extrait
        except requests.exceptions.RequestException:
            continue

    return None


@st.cache_data(ttl=3600)
def get_infos_espece(nom_scientifique: str) -> dict:
    """
    Appelle l'API iNaturalist et retourne :
      - photo_url (str | None)
      - description (str | None)
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
        return {"photo_url": None, "description": None}

    if response.status_code != 200:
        return {"photo_url": None, "description": None}

    resultats = response.json().get("results", [])
    if not resultats:
        return {"photo_url": None, "description": None}

    taxon = resultats[0]

    photo_url = None
    default_photo = taxon.get("default_photo")
    if default_photo:
        photo_url = default_photo.get("medium_url")

    description = taxon.get("wikipedia_summary") or None
    if not description:
        wikipedia_url = taxon.get("wikipedia_url")
        description = _get_wikipedia_summary(nom_scientifique, wikipedia_url)

    return {"photo_url": photo_url, "description": description}


def get_photo_espece(nom_scientifique: str) -> str | None:
    """
    Compatibilité avec l'ancien code.
    """
    return get_infos_espece(nom_scientifique)["photo_url"]
