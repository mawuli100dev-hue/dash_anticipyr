"""
onboarding.py - Sidebar repositionnée comme modal centré.
Boutons natifs st.button dans st.sidebar = toujours fonctionnels.
"""
from __future__ import annotations
import streamlit as st

STEPS = [
    {"titre": "Bienvenue sur ANTICI'PYR",
     "desc": "Ce tableau de bord vous permet d'explorer l'impact du changement climatique sur la flore pyrénéenne endémique. Ce guide rapide vous présente les fonctionnalités essentielles en 5 étapes.",
     "emoji": "🌿"},
    {"titre": "Choisir une espèce et un scénario",
     "desc": "Utilisez le panneau latéral pour sélectionner une espèce cible, un scénario climatique et une période future. Toutes les visualisations se mettent à jour automatiquement.",
     "emoji": "⚙️"},
    {"titre": "Lire la carte de distribution",
     "desc": "L'onglet Carte affiche l'aire d'habitat adéquat actuelle et projetée. Changez le fond de carte, ajustez l'opacité et zoomez sur les zones d'intérêt.",
     "emoji": "🗺️"},
    {"titre": "Comprendre les scénarios SSP",
     "desc": "L'onglet Info SSP explique chaque scénario d'émission. L'onglet Interprétation donne une lecture guidée des résultats.",
     "emoji": "📊"},
    {"titre": "Exporter vos résultats",
     "desc": "Générez un PDF de la session courante ou un rapport complet par espèce depuis les boutons en haut de page.",
     "emoji": "📄"},
]
N = len(STEPS)


def render_onboarding() -> bool:
    """
    Retourne True si le modal d'onboarding est actif.
    Dans ce cas, main() doit skipper render_sidebar().
    """
    if st.session_state.get("_onboarding_done", False):
        return False

    step = st.session_state.get("_onboarding_step", 0)
    s    = STEPS[step]

    # --- Dots ---
    dots = ""
    for i in range(N):
        if i == step:      w, bg, bc = "24px", "#1b5e20", "#1b5e20"
        elif i < step:     w, bg, bc = "8px",  "#c8e6c9", "#1b5e20"
        else:              w, bg, bc = "8px",  "#dcdcdc", "#cfcfcf"
        dots += (f"<span style='display:inline-block;width:{w};height:8px;"
                 f"border-radius:999px;background:{bg};border:1px solid {bc};'></span>")

    # --- CSS ---
    # blur overlay : pointer-events:none -> ne bloque PAS les clics sur le modal
    # sidebar modal : z-index très élevé + pointer-events:auto sur tout
    st.markdown("""<style>
#ob-blur-overlay {
    position: fixed; inset: 0;
    background: rgba(0,0,0,.42);
    backdrop-filter: blur(5px);
    -webkit-backdrop-filter: blur(5px);
    z-index: 998;
    pointer-events: none;
}
section[data-testid="stSidebar"] {
    position: fixed !important;
    top: 50% !important; left: 50% !important;
    transform: translate(-50%,-50%) !important;
    width: min(480px,90vw) !important;
    min-width: unset !important;
    height: auto !important; min-height: unset !important;
    max-height: 90vh !important;
    background: #ffffff !important;
    border-radius: 18px !important;
    box-shadow: 0 24px 64px rgba(0,0,0,.30) !important;
    z-index: 99999 !important;
    overflow: hidden !important;
    padding: 0 !important;
}
section[data-testid="stSidebar"] > div:first-child {
    padding: 0 !important;
    background: transparent !important;
    overflow: visible !important;
}
section[data-testid="stSidebar"],
section[data-testid="stSidebar"] * {
    pointer-events: auto !important;
}
div[data-testid="collapsedControl"],
button[data-testid="stSidebarCollapseButton"],
div[data-testid="stSidebarResizeHandle"] {
    display: none !important;
}
</style>
<div id="ob-blur-overlay"></div>""", unsafe_allow_html=True)

    # --- Contenu du modal dans le sidebar ---
    with st.sidebar:
        st.markdown(f"""
<div style="background:linear-gradient(135deg,#e8f5e9,#f5fbf5);height:160px;
display:flex;align-items:center;justify-content:center;font-size:72px;position:relative">
{s['emoji']}
<span style="position:absolute;top:12px;right:14px;background:rgba(255,255,255,.92);
border:1px solid #d8d8d8;border-radius:999px;padding:3px 10px;
font-size:12px;font-weight:700;color:#666">{step+1} / {N}</span>
</div>
<div style="padding:20px 24px 0">
<p style="font-size:1.05rem;font-weight:700;color:#111;margin:0 0 8px">{s['titre']}</p>
<p style="font-size:.87rem;color:#555;line-height:1.65;margin:0">{s['desc']}</p>
</div>
<div style="display:flex;justify-content:center;gap:7px;padding:14px 0 6px">{dots}</div>
""", unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        with c1:
            prev = st.button("← Précédent", key="ob_prev",
                             use_container_width=True, disabled=(step == 0))
        with c2:
            skip = st.button("Passer", key="ob_skip", use_container_width=True)
        with c3:
            label = "Commencer →" if step == N - 1 else "Suivant →"
            nxt   = st.button(label, key="ob_next",
                              type="primary", use_container_width=True)

        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    # --- Traitement des clics ---
    if prev and step > 0:
        st.session_state["_onboarding_step"] = step - 1
        st.rerun()
    if skip:
        st.session_state["_onboarding_done"] = True
        st.session_state["_onboarding_step"] = 0
        st.rerun()
    if nxt:
        if step < N - 1:
            st.session_state["_onboarding_step"] = step + 1
            st.rerun()
        else:
            st.session_state["_onboarding_done"] = True
            st.session_state["_onboarding_step"] = 0
            st.rerun()

    return True
