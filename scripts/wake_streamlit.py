# scripts/wake_streamlit.py
#
# Ouvre l'URL de l'app Streamlit dans un navigateur headless et clique
# sur le bouton "Yes, get this app back up!" si l'app est en sommeil.
#
# Utilisé par le workflow .github/workflows/keep_alive.yml

import os
import sys
import time
from playwright.sync_api import sync_playwright

APP_URL = os.environ.get("APP_URL", "https://dashanticipyr-rdfsittsujgfzbkbd5hxk8.streamlit.app/")
WAKE_BUTTON_TEXT = "Yes, get this app back up!"
TIMEOUT_MS = 30_000


def wake_app(url: str) -> bool:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
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

        # Verifie que l'app a bien demarre (absence du message Zzzz)
        content = page.content()
        awake = "Zzzz" not in content

        browser.close()
        return awake


if __name__ == "__main__":
    success = wake_app(APP_URL)
    if success:
        print("Application reveillee avec succes.")
        sys.exit(0)
    else:
        print("Echec du reveil de l'application.")
        sys.exit(1)