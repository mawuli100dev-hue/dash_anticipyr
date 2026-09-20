# scripts/wake_streamlit.py
#
# Ouvre une ou plusieurs URLs d'app Streamlit dans un navigateur headless et
# clique sur le bouton "Yes, get this app back up!" si l'app est en sommeil.
#
# Utilisé par le workflow .github/workflows/keep_alive.yml
#
# Usage:
#   python wake_streamlit.py <url1> <url2> ...
#   (si aucune URL n'est passée en argument, utilise APP_URLS depuis l'environnement,
#    séparées par des espaces)

import os
import sys
import time
from playwright.sync_api import sync_playwright

DEFAULT_URLS = [
    "https://dashanticipyr-rdfsittsujgfzbkbd5hxk8.streamlit.app/",
    "https://dashanticipyr-gestion-especes.streamlit.app/",
]

WAKE_BUTTON_TEXT = "Yes, get this app back up!"
TIMEOUT_MS = 30_000


def get_urls() -> list[str]:
    if len(sys.argv) > 1:
        return sys.argv[1:]
    env_urls = os.environ.get("APP_URLS", "")
    if env_urls.strip():
        return env_urls.split()
    return DEFAULT_URLS


def wake_app(page, url: str) -> bool:
    print(f"--- Traitement de {url} ---")
    page.goto(url, timeout=TIMEOUT_MS)

    try:
        button = page.get_by_text(WAKE_BUTTON_TEXT, exact=False)
        button.wait_for(state="visible", timeout=8_000)
        print("App en sommeil detectee, clic sur le bouton de reveil...")
        button.click()
    except Exception:
        print("Bouton de reveil non trouve, l'app est peut-etre deja active.")

    # Laisse le temps a Streamlit de charger apres le clic
    time.sleep(15)

    content = page.content()
    awake = "Zzzz" not in content
    return awake


def main() -> int:
    urls = get_urls()
    results = {}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for url in urls:
            try:
                results[url] = wake_app(page, url)
            except Exception as e:
                print(f"Erreur sur {url}: {e}")
                results[url] = False

        browser.close()

    all_ok = True
    for url, ok in results.items():
        status = "reveillee avec succes" if ok else "echec du reveil"
        print(f"{url} -> {status}")
        if not ok:
            all_ok = False

    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
