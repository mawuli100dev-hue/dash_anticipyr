from __future__ import annotations

from pathlib import Path


def data_cartographies_root() -> Path:
    """
    Répertoire contenant un sous-dossier par espèce :
      dash_anticipyr/data/cartographies/<espece>/...
    """
    return Path(__file__).resolve().parent.parent / "data" / "cartographies"

