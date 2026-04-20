from __future__ import annotations

from typing import Dict, List

# Correspondance : libellé affiché -> clé interne (current ou année de projection)
PERIODES: Dict[str, str] = {
    "1970–2000": "current",
    "2021–2040": "2030",
    "2041–2060": "2050",
    "2061–2080": "2070",
    "2081–2100": "2090",
}

SSP_LIST: List[str] = ["SSP 126", "SSP 245", "SSP 370", "SSP 585"]

MODE_MAP: Dict[str, str] = {
    "Continu":  "continu",
    "Absence":  "absence",
    "Présence": "presence",
}

# Seuil par défaut pour la binarisation (modifiable ici uniquement)
SEUIL_BINARISATION: float = 0.5
