from __future__ import annotations

import json
import streamlit as st
import streamlit.components.v1 as components

from dash_anticipyr.core.translations import t


def inject_shepherd_tour() -> None:
    """
    Tour guidé Shepherd.js - s'affiche au premier chargement.
    Relancer via : st.session_state["start_tour"] = True + st.rerun()
    """

    if "tour_seen" not in st.session_state:
        st.session_state["start_tour"] = True
        st.session_state["tour_seen"] = True

    if not st.session_state.get("start_tour", False):
        return

    st.session_state["start_tour"] = False

    # Définition des étapes en Python pur - pas de .format() imbriqué
    steps = [
        {
            "selector": "section[data-testid='stSidebar'] div.stSelectbox:first-of-type",
            "titre":    t("howto_step1_titre"),
            "texte":    t("howto_step1_desc"),
            "position": "right",
        },
        {
            "selector": "section[data-testid='stSidebar'] div.stSelectbox:nth-of-type(2)",
            "titre":    t("howto_step2_titre"),
            "texte":    t("howto_step2_desc"),
            "position": "right",
        },
        {
            "selector": "section[data-testid='stSidebar'] div.stRadio",
            "titre":    t("howto_step3_titre"),
            "texte":    t("howto_step3_desc"),
            "position": "right",
        },
        {
            "selector": "div[data-baseweb='tab-list']",
            "titre":    t("howto_step4_titre"),
            "texte":    t("howto_step4_desc"),
            "position": "bottom",
        },
        {
            "selector": "div[data-testid='stDownloadButton']",
            "titre":    t("howto_step5_titre"),
            "texte":    t("howto_step5_desc"),
            "position": "top",
        },
    ]

    # Sérialise les étapes en JSON pour injection JS sans conflit d'accolades
    steps_json  = json.dumps(steps, ensure_ascii=False)
    label_next  = json.dumps(t("howto_next"),   ensure_ascii=False)
    label_prev  = json.dumps(t("howto_prev"),   ensure_ascii=False)
    label_fin   = json.dumps(t("howto_fermer"), ensure_ascii=False)
    total       = len(steps)

    html = f"""<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet"
        href="https://cdn.jsdelivr.net/npm/shepherd.js@11/dist/css/shepherd.css"/>
  <style>
    body {{ margin:0; background:transparent; }}

    .shepherd-theme-custom {{ border-radius:10px; box-shadow:0 8px 32px rgba(0,0,0,.18); max-width:340px; }}
    .shepherd-theme-custom .shepherd-header {{ background:#01696f; border-radius:8px 8px 0 0; padding:12px 16px; }}
    .shepherd-theme-custom .shepherd-title  {{ color:#fff; font-weight:700; font-size:15px; font-family:sans-serif; }}
    .shepherd-theme-custom .shepherd-cancel-icon {{ color:rgba(255,255,255,.8); }}
    .shepherd-theme-custom .shepherd-text   {{ padding:16px; font-size:14px; font-family:sans-serif; color:#28251d; line-height:1.5; }}
    .shepherd-theme-custom .shepherd-footer {{ padding:8px 16px 14px; display:flex; justify-content:flex-end; gap:8px; }}

    .shepherd-theme-custom .shepherd-button {{
      background:#01696f; color:#fff; border:none;
      border-radius:6px; padding:7px 16px;
      font-size:13px; font-weight:600; cursor:pointer;
    }}
    .shepherd-theme-custom .shepherd-button:hover {{ background:#0c4e54; }}
    .shepherd-theme-custom .shepherd-btn-secondary {{
      background:transparent; color:#01696f;
      border:1px solid #01696f; border-radius:6px;
      padding:7px 16px; font-size:13px; font-weight:600; cursor:pointer;
    }}
    .shepherd-theme-custom .shepherd-btn-secondary:hover {{ background:#cedcd8; }}

    .shepherd-highlight {{
      box-shadow:0 0 0 4px #01696f88, 0 0 0 9px #01696f22 !important;
      border-radius:6px; transition:box-shadow .3s;
    }}
    .shepherd-progress {{ display:flex; gap:6px; align-items:center; padding:0 16px 10px; }}
    .shepherd-dot {{ width:7px; height:7px; border-radius:50%; background:#cedcd8; transition:background .2s; }}
    .shepherd-dot.active {{ background:#01696f; }}
  </style>
</head>
<body>
<script src="https://cdn.jsdelivr.net/npm/shepherd.js@11/dist/js/shepherd.min.js"></script>
<script>
(function() {{
  var STEPS      = {steps_json};
  var LABEL_NEXT = {label_next};
  var LABEL_PREV = {label_prev};
  var LABEL_FIN  = {label_fin};
  var TOTAL      = {total};

  var parentDoc = window.parent.document;

  var tour = new Shepherd.Tour({{
    useModalOverlay: true,
    defaultStepOptions: {{
      classes: 'shepherd-theme-custom',
      scrollTo: {{ behavior: 'smooth', block: 'center' }},
      modalOverlayOpeningPadding: 8,
      modalOverlayOpeningRadius: 8
    }}
  }});

  function highlightEl(selector) {{
    var prev = parentDoc.querySelector('.shepherd-highlight');
    if (prev) prev.classList.remove('shepherd-highlight');
    if (selector) {{
      var el = parentDoc.querySelector(selector);
      if (el) el.classList.add('shepherd-highlight');
    }}
  }}

  function clearHighlight() {{
    var el = parentDoc.querySelector('.shepherd-highlight');
    if (el) el.classList.remove('shepherd-highlight');
  }}

  function addProgressDots(stepEl, idx) {{
    var existing = stepEl.querySelector('.shepherd-progress');
    if (existing) existing.remove();
    var footer = stepEl.querySelector('.shepherd-footer');
    if (!footer) return;
    var prog = document.createElement('div');
    prog.className = 'shepherd-progress';
    for (var i = 0; i < TOTAL; i++) {{
      var dot = document.createElement('div');
      dot.className = 'shepherd-dot' + (i === idx ? ' active' : '');
      prog.appendChild(dot);
    }}
    footer.insertAdjacentElement('beforebegin', prog);
  }}

  STEPS.forEach(function(s, idx) {{
    var isLast = idx === TOTAL - 1;

    var buttons = [];
    if (idx > 0) {{
      buttons.push({{
        text: LABEL_PREV,
        classes: 'shepherd-btn-secondary',
        action: function() {{ tour.back(); }}
      }});
    }}
    buttons.push({{
      text: isLast ? LABEL_FIN : LABEL_NEXT,
      action: function() {{ isLast ? tour.complete() : tour.next(); }}
    }});

    tour.addStep({{
      id: 'step-' + idx,
      title: s.titre,
      text: s.texte,
      attachTo: {{ element: s.selector, on: s.position }},
      cancelIcon: {{ enabled: true }},
      buttons: buttons
    }});
  }});

  tour.on('show', function(e) {{
    var idx = tour.steps.indexOf(e.step);
    highlightEl(STEPS[idx] ? STEPS[idx].selector : null);
    setTimeout(function() {{
      if (e.step.el) addProgressDots(e.step.el, idx);
    }}, 50);
  }});

  tour.on('complete', clearHighlight);
  tour.on('cancel',   clearHighlight);

  setTimeout(function() {{ tour.start(); }}, 900);
}})();
</script>
</body>
</html>"""

    components.html(html, height=0, scrolling=False)
