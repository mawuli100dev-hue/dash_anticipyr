from __future__ import annotations

import streamlit as st


# ---------------------------------------------------------------------------
# Dictionnaire de traductions
# 4 langues : français (fr), anglais (en), espagnol (es), catalan (ca)
# ---------------------------------------------------------------------------

TEXTES: dict[str, dict[str, str]] = {

    "fr": {

        # --- app.py ---
        "page_title":               "Flore Pyrénéenne - Habitats",
        "main_subtitle":            "Projection bioclimatique des espèces endémiques pyrénéennes",
        "btn_imprimer":             "Imprimer",
        "btn_imprimer_help":        "Télécharger la fiche PDF complète ou Ctrl+P",
        "btn_imprimer_loading":     "Chargement en cours...",
        "tab_carte":                "Carte de distribution",
        "tab_ssp":                  "Scénarios SSP",

        # --- sidebar.py ---
        "sidebar_titre":            "Flore Pyrénéenne",
        "sidebar_sous_titre":       "Sélectionnez une espèce, une période et un scénario",
        "sidebar_espece_label":     "Espèce étudiée",
        "sidebar_espece_caption":   "{n} espèce(s) disponible(s)",
        "sidebar_espece_error":     "Aucune espèce trouvée. Vérifiez dash_anticipyr/data/cartographies/.",
        "sidebar_espece_warning":   "Sélectionnez une espèce dans la liste.",
        "sidebar_espece_help":      "Tapez après ouverture pour filtrer la liste.",
        "sidebar_periode_label":    "Période de projection",
        "sidebar_current_info":     "<strong>Période actuelle (1970-2000)</strong><br>Aucun scénario SSP - données de référence climatique.",
        "sidebar_ssp_label":        "Scénario climatique (SSP)",
        "sidebar_mode_label":       "Mode de visualisation",
        "sidebar_mode_help":        "Continu : probabilité de présence entre 0 et 1  |  Absence/Présence : carte binarisée (données déjà 0/1)",
        "sidebar_footer":           "ANTICI'PYR · Flore Pyrénéenne<br>Université de Perpignan Via Domitia",
        "ssp_126_desc":             "Optimiste",
        "ssp_245_desc":             "Intermédiaire",
        "ssp_370_desc":             "Pessimiste",
        "ssp_585_desc":             "Très pessimiste",
        "mode_continu":             "Continu",
        "mode_binaire":             "Absence/Présence",

        # --- map_section.py ---
        "map_titre":                "Carte interactive",
        "map_caption":              "Zoom avant libre jusqu'aux villages. Zoom arrière limité à la région pyrénéenne.",
        "map_fond_label":           "Fond de carte",
        "map_fond_plan":            "Plan",
        "map_fond_satellite":       "Satellite",
        "map_opacite_label":        "Opacité de la prédiction",
        "map_periode_label":        "Période",
        "map_scenario_label":       "Scénario",
        "map_periode_actuelle":     "Période actuelle",
        "map_periode_ref":          "(1970-2000)",
        "map_download_titre":       "Télécharger la carte sélectionnée",
        "map_no_photo":             "Aucune photo disponible sur iNaturalist pour cette espèce.",
        "map_fichier_introuvable":  "**Fichier introuvable :**\n`{chemin}`\n\nVérifiez que les prédictions ont bien été générées pour cette combinaison.",
        "map_erreur_tif":           "Erreur lors de la lecture du fichier TIF :\n`{e}`",
        "map_export_spinner":       "Génération de la carte export...",
        "map_titre_carte_current":  "{espece}  ·  (1970-2000)",
        "map_titre_carte_futur":    "{espece}  ·  {periode} | {ssp}",
        "map_titre_binaire":        "  ·  Absence/Présence",
        "ssp_manquant":             "`ssp` doit être renseigné pour une période future.",

        # --- raster.py ---
        "cbar_continu_label":       "Probabilité de présence",
        "cbar_continu_min":         "0.0\n(Pas favorable)",
        "cbar_continu_max":         "1.0\n(Très favorable)",
        "cbar_binaire_label":       "Favorable / Pas favorable",
        "cbar_binaire_0":           "Pas favorable (0)",
        "cbar_binaire_1":           "Favorable (1)",

        # --- ssp_info.py ---
        "ssp_page_titre":           "## Scénarios climatiques (SSPs)",
        "ssp_intro":                "Les **SSPs** (Shared Socioeconomic Pathways) décrivent des trajectoires socio-économiques menant à différents niveaux d'émissions de gaz à effet de serre. Ce tableau de bord utilise quatre scénarios pour projeter l'évolution des habitats des espèces pyrénéennes jusqu'en 2090.",
        "ssp_recap_titre":          "### Récapitulatif à l'horizon 2090",
        "ssp_recap_col_ssp":        "SSP",
        "ssp_recap_col_emissions":  "Émissions",
        "ssp_recap_col_dt":         "Delta T (°C)",
        "ssp_recap_col_dp":         "Delta P (mm)",
        "ssp_ref_titre":            "### Références",
        "ssp_ref_article":          "**Article :**",
        "ssp_ref_auteurs":          "**Auteurs :**",
        "ssp_ref_dashboard":        "**Tableau de bord :**",
        "ssp_figure_caption":       "Projection moyenne des températures et des précipitations dans les Pyrénées à l'horizon 2081-2100 selon différents scénarios climatiques (Shared Socioeconomic Pathways, SSP), à partir des données WorldClim 2.1 et de l'ensemble des modèles de circulation générale (2030, 2050, 2070 & 2090 correspondant aux périodes 2021-2040, 2041-2060, 2061-2080 et 2081-2100).",
        "ssp_figure_manquant":      "Graphique non trouvé : `{chemin}`\nPlacez le fichier image dans `dash_anticipyr/data/figures/`.",
        "ssp_126_label":            "Faibles émissions",
        "ssp_245_label":            "Émissions intermédiaires",
        "ssp_370_label":            "Émissions élevées",
        "ssp_585_label":            "Émissions très élevées",
        "ssp_126_description":      "Scénario optimiste : forte mitigation climatique, émissions proches de zéro avant 2100.",
        "ssp_245_description":      "Scénario intermédiaire : politiques climatiques partielles, stabilisation en cours de siècle.",
        "ssp_370_description":      "Scénario pessimiste : faible coopération internationale, émissions en hausse continue.",
        "ssp_585_description":      "Scénario extrême : dépendance massive aux énergies fossiles, aucune mitigation.",
        "ssp_temperature":          "Température (2090) :",
        "ssp_precipitations":       "Précipitations (2090) :",
    },

    "en": {

        # --- app.py ---
        "page_title":               "Pyrenean Flora - Habitats",
        "main_subtitle":            "Bioclimatic projection of endemic Pyrenean species",
        "btn_imprimer":             "Print",
        "btn_imprimer_help":        "Download the full PDF report or Ctrl+P",
        "btn_imprimer_loading":     "Loading...",
        "tab_carte":                "Distribution map",
        "tab_ssp":                  "SSP Scenarios",

        # --- sidebar.py ---
        "sidebar_titre":            "Pyrenean Flora",
        "sidebar_sous_titre":       "Select a species, a period and a scenario",
        "sidebar_espece_label":     "Species",
        "sidebar_espece_caption":   "{n} species available",
        "sidebar_espece_error":     "No species found. Check dash_anticipyr/data/cartographies/.",
        "sidebar_espece_warning":   "Please select a species from the list.",
        "sidebar_espece_help":      "Type after opening to filter the list.",
        "sidebar_periode_label":    "Projection period",
        "sidebar_current_info":     "<strong>Current period (1970-2000)</strong><br>No SSP scenario - baseline climate data.",
        "sidebar_ssp_label":        "Climate scenario (SSP)",
        "sidebar_mode_label":       "Visualisation mode",
        "sidebar_mode_help":        "Continuous: presence probability between 0 and 1  |  Absence/Presence: binarised map (already 0/1 data)",
        "sidebar_footer":           "ANTICI'PYR · Pyrenean Flora<br>University of Perpignan Via Domitia",
        "ssp_126_desc":             "Optimistic",
        "ssp_245_desc":             "Intermediate",
        "ssp_370_desc":             "Pessimistic",
        "ssp_585_desc":             "Very pessimistic",
        "mode_continu":             "Continuous",
        "mode_binaire":             "Absence/Presence",

        # --- map_section.py ---
        "map_titre":                "Interactive map",
        "map_caption":              "Free zoom in to villages. Zoom out limited to the Pyrenean region.",
        "map_fond_label":           "Basemap",
        "map_fond_plan":            "Map",
        "map_fond_satellite":       "Satellite",
        "map_opacite_label":        "Prediction opacity",
        "map_periode_label":        "Period",
        "map_scenario_label":       "Scenario",
        "map_periode_actuelle":     "Current period",
        "map_periode_ref":          "(1970-2000)",
        "map_download_titre":       "Download selected map",
        "map_no_photo":             "No photo available on iNaturalist for this species.",
        "map_fichier_introuvable":  "**File not found:**\n`{chemin}`\n\nCheck that predictions have been generated for this combination.",
        "map_erreur_tif":           "Error reading TIF file:\n`{e}`",
        "map_export_spinner":       "Generating export map...",
        "map_titre_carte_current":  "{espece}  ·  (1970-2000)",
        "map_titre_carte_futur":    "{espece}  ·  {periode} | {ssp}",
        "map_titre_binaire":        "  ·  Absence/Presence",
        "ssp_manquant":             "`ssp` must be provided for a future period.",

        # --- raster.py ---
        "cbar_continu_label":       "Probability of presence",
        "cbar_continu_min":         "0.0\n(Unsuitable)",
        "cbar_continu_max":         "1.0\n(Highly suitable)",
        "cbar_binaire_label":       "Suitable / Unsuitable",
        "cbar_binaire_0":           "Unsuitable (0)",
        "cbar_binaire_1":           "Suitable (1)",

        # --- ssp_info.py ---
        "ssp_page_titre":           "## Climate scenarios (SSPs)",
        "ssp_intro":                "**SSPs** (Shared Socioeconomic Pathways) describe socioeconomic trajectories leading to different greenhouse gas emission levels. This dashboard uses four scenarios to project the evolution of Pyrenean endemic species habitats up to 2090.",
        "ssp_recap_titre":          "### Summary at 2090 horizon",
        "ssp_recap_col_ssp":        "SSP",
        "ssp_recap_col_emissions":  "Emissions",
        "ssp_recap_col_dt":         "Delta T (°C)",
        "ssp_recap_col_dp":         "Delta P (mm)",
        "ssp_ref_titre":            "### References",
        "ssp_ref_article":          "**Article:**",
        "ssp_ref_auteurs":          "**Authors:**",
        "ssp_ref_dashboard":        "**Dashboard:**",
        "ssp_figure_caption":       "Mean projected temperature and precipitation in the Pyrenees at the 2081-2100 horizon under different climate scenarios (Shared Socioeconomic Pathways, SSP), based on WorldClim 2.1 data and the full ensemble of general circulation models (2030, 2050, 2070 & 2090 corresponding to the periods 2021-2040, 2041-2060, 2061-2080 and 2081-2100).",
        "ssp_figure_manquant":      "Figure not found: `{chemin}`\nPlace the image file in `dash_anticipyr/data/figures/`.",
        "ssp_126_label":            "Low emissions",
        "ssp_245_label":            "Intermediate emissions",
        "ssp_370_label":            "High emissions",
        "ssp_585_label":            "Very high emissions",
        "ssp_126_description":      "Optimistic scenario: strong climate mitigation, emissions near zero before 2100.",
        "ssp_245_description":      "Intermediate scenario: partial climate policies, stabilisation during the century.",
        "ssp_370_description":      "Pessimistic scenario: low international cooperation, continuously rising emissions.",
        "ssp_585_description":      "Extreme scenario: massive fossil fuel dependency, no mitigation.",
        "ssp_temperature":          "Temperature (2090):",
        "ssp_precipitations":       "Precipitation (2090):",
    },

    "es": {

        # --- app.py ---
        "page_title":               "Flora Pirenaica - Hábitats",
        "main_subtitle":            "Proyección bioclimática de las especies endémicas pirenaicas",
        "btn_imprimer":             "Imprimir",
        "btn_imprimer_help":        "Descargar el informe PDF completo o Ctrl+P",
        "btn_imprimer_loading":     "Cargando...",
        "tab_carte":                "Mapa de distribución",
        "tab_ssp":                  "Escenarios SSP",

        # --- sidebar.py ---
        "sidebar_titre":            "Flora Pirenaica",
        "sidebar_sous_titre":       "Seleccione una especie, un período y un escenario",
        "sidebar_espece_label":     "Especie estudiada",
        "sidebar_espece_caption":   "{n} especie(s) disponible(s)",
        "sidebar_espece_error":     "No se encontraron especies. Verifique dash_anticipyr/data/cartographies/.",
        "sidebar_espece_warning":   "Seleccione una especie de la lista.",
        "sidebar_espece_help":      "Escriba tras abrir para filtrar la lista.",
        "sidebar_periode_label":    "Período de proyección",
        "sidebar_current_info":     "<strong>Período actual (1970-2000)</strong><br>Sin escenario SSP - datos climáticos de referencia.",
        "sidebar_ssp_label":        "Escenario climático (SSP)",
        "sidebar_mode_label":       "Modo de visualización",
        "sidebar_mode_help":        "Continuo: probabilidad de presencia entre 0 y 1  |  Ausencia/Presencia: mapa binarizado (datos ya 0/1)",
        "sidebar_footer":           "ANTICI'PYR · Flora Pirenaica<br>Universidad de Perpiñán Via Domitia",
        "ssp_126_desc":             "Optimista",
        "ssp_245_desc":             "Intermedio",
        "ssp_370_desc":             "Pesimista",
        "ssp_585_desc":             "Muy pesimista",
        "mode_continu":             "Continuo",
        "mode_binaire":             "Ausencia/Presencia",

        # --- map_section.py ---
        "map_titre":                "Mapa interactivo",
        "map_caption":              "Zoom libre hasta los pueblos. Zoom alejado limitado a la región pirenaica.",
        "map_fond_label":           "Mapa base",
        "map_fond_plan":            "Mapa",
        "map_fond_satellite":       "Satélite",
        "map_opacite_label":        "Opacidad de la predicción",
        "map_periode_label":        "Período",
        "map_scenario_label":       "Escenario",
        "map_periode_actuelle":     "Período actual",
        "map_periode_ref":          "(1970-2000)",
        "map_download_titre":       "Descargar el mapa seleccionado",
        "map_no_photo":             "No hay foto disponible en iNaturalist para esta especie.",
        "map_fichier_introuvable":  "**Archivo no encontrado:**\n`{chemin}`\n\nVerifique que las predicciones han sido generadas para esta combinación.",
        "map_erreur_tif":           "Error al leer el archivo TIF:\n`{e}`",
        "map_export_spinner":       "Generando mapa de exportación...",
        "map_titre_carte_current":  "{espece}  ·  (1970-2000)",
        "map_titre_carte_futur":    "{espece}  ·  {periode} | {ssp}",
        "map_titre_binaire":        "  ·  Ausencia/Presencia",
        "ssp_manquant":             "`ssp` debe especificarse para un período futuro.",

        # --- raster.py ---
        "cbar_continu_label":       "Probabilidad de presencia",
        "cbar_continu_min":         "0.0\n(No favorable)",
        "cbar_continu_max":         "1.0\n(Muy favorable)",
        "cbar_binaire_label":       "Favorable / No favorable",
        "cbar_binaire_0":           "No favorable (0)",
        "cbar_binaire_1":           "Favorable (1)",

        # --- ssp_info.py ---
        "ssp_page_titre":           "## Escenarios climáticos (SSPs)",
        "ssp_intro":                "Los **SSPs** (Shared Socioeconomic Pathways) describen trayectorias socioeconómicas que conducen a diferentes niveles de emisiones de gases de efecto invernadero. Este panel utiliza cuatro escenarios para proyectar la evolución de los hábitats de las especies pirenaicas hasta 2090.",
        "ssp_recap_titre":          "### Resumen a horizonte 2090",
        "ssp_recap_col_ssp":        "SSP",
        "ssp_recap_col_emissions":  "Emisiones",
        "ssp_recap_col_dt":         "Delta T (°C)",
        "ssp_recap_col_dp":         "Delta P (mm)",
        "ssp_ref_titre":            "### Referencias",
        "ssp_ref_article":          "**Artículo:**",
        "ssp_ref_auteurs":          "**Autores:**",
        "ssp_ref_dashboard":        "**Panel:**",
        "ssp_figure_caption":       "Proyección media de temperaturas y precipitaciones en los Pirineos al horizonte 2081-2100 según distintos escenarios climáticos (Shared Socioeconomic Pathways, SSP), a partir de los datos WorldClim 2.1 y del conjunto de modelos de circulación general (2030, 2050, 2070 & 2090 correspondientes a los períodos 2021-2040, 2041-2060, 2061-2080 y 2081-2100).",
        "ssp_figure_manquant":      "Gráfico no encontrado: `{chemin}`\nColoque el archivo de imagen en `dash_anticipyr/data/figures/`.",
        "ssp_126_label":            "Bajas emisiones",
        "ssp_245_label":            "Emisiones intermedias",
        "ssp_370_label":            "Emisiones elevadas",
        "ssp_585_label":            "Emisiones muy elevadas",
        "ssp_126_description":      "Escenario optimista: fuerte mitigación climática, emisiones próximas a cero antes de 2100.",
        "ssp_245_description":      "Escenario intermedio: políticas climáticas parciales, estabilización a mitad de siglo.",
        "ssp_370_description":      "Escenario pesimista: escasa cooperación internacional, emisiones en aumento continuo.",
        "ssp_585_description":      "Escenario extremo: dependencia masiva de combustibles fósiles, sin mitigación.",
        "ssp_temperature":          "Temperatura (2090):",
        "ssp_precipitations":       "Precipitaciones (2090):",
    },

    "ca": {

        # --- app.py ---
        "page_title":               "Flora Pirinenca - Hàbitats",
        "main_subtitle":            "Projecció bioclimàtica de les espècies endèmiques pirinenques",
        "btn_imprimer":             "Imprimir",
        "btn_imprimer_help":        "Descarregar l'informe PDF complet o Ctrl+P",
        "btn_imprimer_loading":     "Carregant...",
        "tab_carte":                "Mapa de distribució",
        "tab_ssp":                  "Escenaris SSP",

        # --- sidebar.py ---
        "sidebar_titre":            "Flora Pirinenca",
        "sidebar_sous_titre":       "Seleccioneu una espècie, un període i un escenari",
        "sidebar_espece_label":     "Espècie estudiada",
        "sidebar_espece_caption":   "{n} espècie(s) disponible(s)",
        "sidebar_espece_error":     "No s'han trobat espècies. Verifiqueu dash_anticipyr/data/cartographies/.",
        "sidebar_espece_warning":   "Seleccioneu una espècie de la llista.",
        "sidebar_espece_help":      "Escriviu després d'obrir per filtrar la llista.",
        "sidebar_periode_label":    "Període de projecció",
        "sidebar_current_info":     "<strong>Període actual (1970-2000)</strong><br>Cap escenari SSP - dades climàtiques de referència.",
        "sidebar_ssp_label":        "Escenari climàtic (SSP)",
        "sidebar_mode_label":       "Mode de visualització",
        "sidebar_mode_help":        "Continu: probabilitat de presència entre 0 i 1  |  Absència/Presència: mapa binaritzat (dades ja 0/1)",
        "sidebar_footer":           "ANTICI'PYR · Flora Pirinenca<br>Universitat de Perpinyà Via Domitia",
        "ssp_126_desc":             "Optimista",
        "ssp_245_desc":             "Intermedi",
        "ssp_370_desc":             "Pessimista",
        "ssp_585_desc":             "Molt pessimista",
        "mode_continu":             "Continu",
        "mode_binaire":             "Absència/Presència",

        # --- map_section.py ---
        "map_titre":                "Mapa interactiu",
        "map_caption":              "Zoom lliure fins als pobles. Zoom allunyat limitat a la regió pirinenca.",
        "map_fond_label":           "Mapa base",
        "map_fond_plan":            "Mapa",
        "map_fond_satellite":       "Satèl·lit",
        "map_opacite_label":        "Opacitat de la predicció",
        "map_periode_label":        "Període",
        "map_scenario_label":       "Escenari",
        "map_periode_actuelle":     "Període actual",
        "map_periode_ref":          "(1970-2000)",
        "map_download_titre":       "Descarregar el mapa seleccionat",
        "map_no_photo":             "No hi ha cap foto disponible a iNaturalist per a aquesta espècie.",
        "map_fichier_introuvable":  "**Fitxer no trobat:**\n`{chemin}`\n\nVerifiqueu que les prediccions han estat generades per a aquesta combinació.",
        "map_erreur_tif":           "Error en llegir el fitxer TIF:\n`{e}`",
        "map_export_spinner":       "Generant mapa d'exportació...",
        "map_titre_carte_current":  "{espece}  ·  (1970-2000)",
        "map_titre_carte_futur":    "{espece}  ·  {periode} | {ssp}",
        "map_titre_binaire":        "  ·  Absència/Presència",
        "ssp_manquant":             "`ssp` ha d'especificar-se per a un període futur.",

        # --- raster.py ---
        "cbar_continu_label":       "Probabilitat de presència",
        "cbar_continu_min":         "0.0\n(No favorable)",
        "cbar_continu_max":         "1.0\n(Molt favorable)",
        "cbar_binaire_label":       "Favorable / No favorable",
        "cbar_binaire_0":           "No favorable (0)",
        "cbar_binaire_1":           "Favorable (1)",

        # --- ssp_info.py ---
        "ssp_page_titre":           "## Escenaris climàtics (SSPs)",
        "ssp_intro":                "Els **SSPs** (Shared Socioeconomic Pathways) descriuen trajectòries socioeconòmiques que condueixen a diferents nivells d'emissions de gasos d'efecte hivernacle. Aquest tauler utilitza quatre escenaris per projectar l'evolució dels hàbitats de les espècies pirinenques fins al 2090.",
        "ssp_recap_titre":          "### Resum a l'horitzó 2090",
        "ssp_recap_col_ssp":        "SSP",
        "ssp_recap_col_emissions":  "Emissions",
        "ssp_recap_col_dt":         "Delta T (°C)",
        "ssp_recap_col_dp":         "Delta P (mm)",
        "ssp_ref_titre":            "### Referències",
        "ssp_ref_article":          "**Article:**",
        "ssp_ref_auteurs":          "**Autors:**",
        "ssp_ref_dashboard":        "**Tauler:**",
        "ssp_figure_caption":       "Projecció mitjana de temperatures i precipitacions als Pirineus a l'horitzó 2081-2100 segons diferents escenaris climàtics (Shared Socioeconomic Pathways, SSP), a partir de les dades WorldClim 2.1 i del conjunt de models de circulació general (2030, 2050, 2070 & 2090 corresponents als períodes 2021-2040, 2041-2060, 2061-2080 i 2081-2100).",
        "ssp_figure_manquant":      "Gràfic no trobat: `{chemin}`\nCol·loqueu el fitxer d'imatge a `dash_anticipyr/data/figures/`.",
        "ssp_126_label":            "Baixes emissions",
        "ssp_245_label":            "Emissions intermèdies",
        "ssp_370_label":            "Emissions elevades",
        "ssp_585_label":            "Emissions molt elevades",
        "ssp_126_description":      "Escenari optimista: forta mitigació climàtica, emissions properes a zero abans del 2100.",
        "ssp_245_description":      "Escenari intermedi: polítiques climàtiques parcials, estabilització a mitjan segle.",
        "ssp_370_description":      "Escenari pessimista: escassa cooperació internacional, emissions en augment continu.",
        "ssp_585_description":      "Escenari extrem: dependència massiva dels combustibles fòssils, sense mitigació.",
        "ssp_temperature":          "Temperatura (2090):",
        "ssp_precipitations":       "Precipitacions (2090):",
    },
}


# ---------------------------------------------------------------------------
# Initialisation de la langue dans session_state
# ---------------------------------------------------------------------------

# Drapeaux affichés dans le sélecteur de langue
LANGUES = {
    "fr": "🇫🇷 Français",
    "en": "🇬🇧 English",
    "es": "🇪🇸 Español",
    "ca": "🏴 Català",
}


def init_langue() -> None:
    """
    Initialise st.session_state["langue"] à "fr" si absent.
    A appeler une seule fois au démarrage dans app.py, avant tout rendu.
    """
    if "langue" not in st.session_state:
        st.session_state["langue"] = "fr"


# ---------------------------------------------------------------------------
# Fonction de traduction principale
# ---------------------------------------------------------------------------

def t(cle: str, **kwargs) -> str:
    """
    Retourne le texte traduit pour la clé donnée, dans la langue active.

    Utilisation simple :
        t("map_titre")
        -> "Carte interactive" (fr) | "Interactive map" (en)
        -> "Mapa interactivo" (es)  | "Mapa interactiu" (ca)

    Utilisation avec variables :
        t("sidebar_espece_caption", n=42)
        -> "42 espèce(s) disponible(s)"  (fr)
        -> "42 espècie(s) disponible(s)" (ca)

    Fallbacks :
    - Langue inconnue  -> "fr"
    - Clé introuvable  -> version "fr" de la clé
    - Clé absente de "fr" aussi -> retourne la clé brute (débogage)
    """
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
