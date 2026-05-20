TEXTES_FR: dict[str, str] = {

    # --- app.py ---
    "page_title":               "Flore Pyrénéenne - cartes de répartition",
    "main_subtitle":            "Projection de la répartition des conditions climatiques favorables et défavorables aux espèces pyrénéennes",
    "btn_imprimer":             "Imprimer",
    "btn_imprimer_loading":     "Chargement en cours...",
    "tab_carte":                "Carte de répartition",
    "tab_ssp":                  "Scénarios SSP",
    "btn_imprimer_scenario":     "Imprimer la fiche scénario sélectionné",
    "btn_imprimer_help":         "Imprimer la fiche espèce pour le scénario sélectionné",
    "btn_imprimer_complet":      "Imprimer la fiche espèce complète",
    "btn_imprimer_complet_help": "Imprimer la fiche espèce complète avec toutes les périodes et les 4 scénarios SSP",
    "sidebar_toggle_label": "Afficher / Masquer",
    "btn_preparer_scenario":      "Préparer la fiche scénario",
    "btn_preparer_complet":      "Préparer la fiche complète",
    "msg_generation_pdf":       "Génération du PDF en cours...",


    # --- sidebar.py ---
    "sidebar_titre":            "Flore Pyrénéenne",
    "sidebar_sous_titre":       "Sélectionnez une espèce, une période et un scénario",
    "sidebar_espece_label":     "Espèce étudiée",
    "sidebar_espece_caption":   "{n} espèce(s) disponible(s)",
    "sidebar_espece_error":     "Aucune espèce trouvée.",
    "sidebar_espece_warning":   "Sélectionnez une espèce dans la liste.",
    "sidebar_espece_help":      "Tapez après ouverture pour filtrer la liste.",
    "sidebar_periode_label":    "Période de projection",
    "sidebar_current_info":     "<strong>Période actuelle (1970-2000)</strong><br>Aucun scénario SSP - données de référence climatique.",
    "sidebar_ssp_label":        "Scénario climatique (SSP)",
    "sidebar_mode_label":       "Mode de visualisation",
    "sidebar_mode_help":        "Continu : probabilité de présence entre 0 et 1  |  Défavorable/Favorable : carte binarisée (données déjà 0/1)",
    "sidebar_footer":           "ANTICI'PYR",
    "ssp_126_desc":             "Optimiste",
    "ssp_245_desc":             "Intermédiaire",
    "ssp_370_desc":             "Pessimiste",
    "ssp_585_desc":             "Très pessimiste",
    "mode_continu":             "Continu",
    "mode_binaire":             "Défavorable/Favorable",

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
    "map_titre_binaire":        "  ·  Défavorable/Favorable",
    "ssp_manquant":             "`ssp` doit être renseigné pour une période future.",

    # --- raster.py ---
    "cbar_continu_label":       "Probabilité de présence",
    "cbar_continu_min":         "0.0\n(Pas favorable)",
    "cbar_continu_max":         "1.0\n(Très favorable)",
    "cbar_binaire_label":       "Favorable / Pas favorable",
    "cbar_binaire_0":           "Pas favorable (0)",
    "cbar_binaire_1":           "Favorable (1)",
    "legende_continu_titre":    "Adéquation climatique",
    "legende_continu_min":      "Pas favorable",
    "legende_continu_max":      "Très favorable",
    "legende_binaire_titre":    "Conditions climatiques",
    "legende_binaire_0":        "Défavorable",
    "legende_binaire_1":        "Favorable",
    "btn_recentrer":            "Recentrer sur les Pyrénées",

    # --- ssp_info.py ---
    "ssp_page_titre":           "## Scénarios climatiques (SSPs)",
    "ssp_intro":                "Les **SSPs** (Shared Socioeconomic Pathways) décrivent des trajectoires socio-économiques menant à différents niveaux d'émissions de gaz à effet de serre. Ce tableau de bord présente les conditions climatiques favorables aux espèces pyrénéennes, projetées selon quatre scénarios climatiques jusqu’à la période 2081–2100.",
    "ssp_recap_titre":          "### Récapitulatif des conditions climatiques projetée à l'horizon 2081-2100, en moyenne sur la chaine des Pyrénées",
    "ssp_recap_col_ssp":        "SSP",
    "ssp_recap_col_emissions":  "Émissions",
    "ssp_recap_col_dt":         "Delta T (°C)",
    "ssp_recap_col_dp":         "Delta P (mm)",
    "ssp_ref_titre":            "### Références",
    "ssp_ref_article":          "Article :",
    "ssp_ref_auteurs":          "Auteurs :",
    "ssp_ref_dashboard":        "Tableau de bord :",
    "ssp_figure_caption":       "Projection moyenne des températures et des précipitations dans les Pyrénées à l'horizon 2081-2100 selon différents scénarios climatiques (Shared Socioeconomic Pathways, SSP), à partir des données WorldClim 2.1 et de l'ensemble des modèles de circulation générale (2030, 2050, 2070 & 2090 correspondant aux périodes 2021-2040, 2041-2060, 2061-2080 et 2081-2100).",
    "ssp_figure_manquant":      "Graphique non trouvé : `{chemin}`\nPlacez le fichier image dans `dash_anticipyr/data/figures/`.",
    "ssp_126_label":            "Faibles émissions",
    "ssp_245_label":            "Émissions intermédiaires",
    "ssp_370_label":            "Émissions élevées",
    "ssp_585_label":            "Émissions très élevées",
    "ssp_126_description": "Scénario optimiste avec politiques climatiques fortes, conduisant à des émissions très faibles d'ici 2100.",
    "ssp_245_description": "Scénario intermédiaire avec des politiques climatiques limitées, entraînant une stabilisation progressive des émissions.",
    "ssp_370_description": "Scénario pessimiste marqué par une faible coopération internationale et une augmentation continue des émissions.",
    "ssp_585_description": "Scénario extrême caractérisé par une forte dépendance aux énergies fossiles et des émissions très élevées.",
    "ssp_temperature":          "Température (2090) :",
    "ssp_precipitations":       "Précipitations (2090) :",
    "ssp_valeurs_moyennes": "Valeurs moyennes estimées pour la chaîne des Pyrénées",


    # --- interpretation.py ---
    "tab_interpretation": "Interprétation",
    "interp_intro_1":       "L'étude repose sur un outil central de l'écologie contemporaine : les modèles de distribution d'espèces (Species Distribution Models, SDM). Dans leur forme la plus complète, les SDM intègrent de multiples dimensions écologiques (climat, dispersion, interactions biotiques, génétique). Ils caractérisent ainsi où et pourquoi une espèce se maintient.",
    "interp_intro_2":       "Les cartes de répartition des espèces pyrénéennes sont construites à partir de variables climatiques, en particulier les précipitations et les températures. Elles résultent du croisement entre des données de présence (relevés de terrain, spécimens d'herbier, bases de données en ligne) et un ensemble de variables environnementales caractérisant les conditions des sites occupés (voir tableau ci-dessous).",
    "interp_conclusion":    "Les modèles permettent de définir les combinaisons climatiques associées à la présence (ou l'absence) de l'espèce, et donc les environnements où elle est susceptible de se maintenir. Ce portrait établi, il devient possible d'étudier l'évolution de ces conditions sous différents climats futurs pour estimer où l'espèce pourrait subsister, migrer ou disparaître.",
    "interp_col_variable":  "Variable",
    "interp_col_nom":       "Nom",
    "interp_col_description": "Description",
    "interp_col_unite":     "Unité",
    "interp_titre_temp":    "Variables de température (BIO1 - BIO11)",
    "interp_titre_prec":    "Variables de précipitations (BIO12 - BIO19)",
    "interp_worldclim_titre":   "Tableau A1 : Définitions des variables bioclimatiques WorldClim 2.1.",
    "interp_worldclim_caption": "La base de données publique WorldClim 2.1 (Fick & Hijmans, 2017) fournit 19 variables bioclimatiques au format raster, dont 11 liées à la température et 8 aux précipitations. Ces variables sont dérivées de données climatiques mensuelles moyennes interpolées, collectées à partir de stations météorologiques.",
    "bio1_nom":  "Température annuelle moyenne",
    "bio1_desc": "Température annuelle moyenne",
    "bio2_nom":  "Écart diurne moyen",
    "bio2_desc": "Moyenne des écarts de température mensuels (Tmax - Tmin)",
    "bio3_nom":  "Isothermalité",
    "bio3_desc": "(BIO2 / BIO7) (*100) : Proportion de la variation diurne par rapport à la variation annuelle",
    "bio4_nom":  "Saisonnalité de la température",
    "bio4_desc": "Variabilité de la température (écart-type * 100)",
    "bio5_nom":  "Température max du mois le plus chaud",
    "bio5_desc": "Température maximale du mois le plus chaud",
    "bio6_nom":  "Température min du mois le plus froid",
    "bio6_desc": "Température minimale du mois le plus froid",
    "bio7_nom":  "Écart annuel de température",
    "bio7_desc": "Écart de température annuel (BIO5 - BIO6)",
    "bio8_nom":  "Température moyenne du trimestre le plus humide",
    "bio8_desc": "Température moyenne du trimestre le plus humide",
    "bio9_nom":  "Température moyenne du trimestre le plus sec",
    "bio9_desc": "Température moyenne du trimestre le plus sec",
    "bio10_nom": "Température moyenne du trimestre le plus chaud",
    "bio10_desc":"Température moyenne du trimestre le plus chaud",
    "bio11_nom": "Température moyenne du trimestre le plus froid",
    "bio11_desc":"Température moyenne du trimestre le plus froid",
    "bio12_nom": "Précipitation annuelle",
    "bio12_desc":"Précipitation annuelle totale",
    "bio13_nom": "Précipitation du mois le plus humide",
    "bio13_desc":"Précipitation du mois le plus humide",
    "bio14_nom": "Précipitation du mois le plus sec",
    "bio14_desc":"Précipitation du mois le plus sec",
    "bio15_nom": "Saisonnalité des précipitations",
    "bio15_desc":"Variabilité des précipitations (coefficient de variation)",
    "bio16_nom": "Précipitation du trimestre le plus humide",
    "bio16_desc":"Précipitation totale du trimestre le plus humide",
    "bio17_nom": "Précipitation du trimestre le plus sec",
    "bio17_desc":"Précipitation totale du trimestre le plus sec",
    "bio18_nom": "Précipitation du trimestre le plus chaud",
    "bio18_desc":"Précipitation totale du trimestre le plus chaud",
    "bio19_nom": "Précipitation du trimestre le plus froid",
    "bio19_desc":"Précipitation totale du trimestre le plus froid",

    # --- tutorial.py ---

    "tab_tutorial": "Tutoriel",

    "tutorial_sidebar_title": "Comprendre la barre latérale",
    "tutorial_sidebar_intro": (
        "La barre latérale regroupe tous les réglages qui contrôlent la carte : "
        "langue, espèce étudiée, période de projection et scénario climatique (SSP). "
        "Chaque choix modifie directement la carte affichée au centre de l'écran."
    ),
    "tutorial_sidebar_lang": (
        "En haut, choisissez la langue d'affichage de l'application."
    ),
    "tutorial_sidebar_species": (
        "Sélectionnez ensuite l'espèce étudiée dans la liste déroulante. "
        "Le nombre d'espèces disponibles est indiqué juste au-dessus."
    ),
    "tutorial_sidebar_period": (
        "Choisissez la période de projection (par exemple 2021–2040)."
    ),
    "tutorial_sidebar_ssp": (
        "Choisissez ensuite un scénario climatique (SSP 126, 245, 370 ou 585). "
        "Les boutons colorés vont du plus optimiste (vert) au plus pessimiste (rouge)."
    ),
    "tutorial_sidebar_mode": (
        "Enfin, le mode de visualisation permet d'afficher soit une probabilité de présence "
        "continue, soit une carte binaire Défavorabe/Favorable."
    ),


    "tutorial_header_title": "Comprendre les boutons d'action",
    "tutorial_header_intro": (
        "En haut de la page, deux boutons permettent de préparer et d'imprimer "
        "des fiches au format PDF pour l'espèce sélectionnée."
    ),
    "tutorial_header_prepare_scenario": (
        "Préparer la fiche scénario : génère une fiche pour la combinaison "
        "période + scénario climatique actuellement sélectionnée."
    ),
    "tutorial_header_prepare_full": (
        "Préparer la fiche complète : génère une fiche regroupant toutes les périodes "
        "et les quatre scénarios SSP pour l'espèce choisie."
    ),
    "tutorial_header_tabs": (
        "Les onglets Carte de répartition, Scénarios SSP, Interprétation et Tutoriel "
        "permettent de passer d’une vue à l’autre de l’outil."
    ),


    "tutorial_map_title": "Fond de carte et opacité",
    "tutorial_map_intro": (
        "La carte interactive affiche la prédiction de présence de l'espèce superposée "
        "à un fond de carte (plan ou satellite)."
    ),
    "tutorial_map_basemap": (
        "Fond de carte : choisissez Plan (carte routière détaillée) ou Satellite "
        "pour mieux voir le relief et l'occupation du sol."
    ),
    "tutorial_map_opacity": (
        "Opacité de la prédiction : le curseur règle la transparence de la couche "
        "de prédiction. Une opacité faible laisse davantage apparaître le fond de carte, "
        "une opacité élevée met en avant les zones favorables ou défavorables."
    ),
    "tutorial_map_recentre": (
        "Recentrer sur les Pyrénées : recentre automatiquement la carte sur l'ensemble du massif."
    ),


    "tutorial_export_title": "Télécharger la carte sélectionnée",
    "tutorial_export_intro": (
        "Une fois la carte affichée (espèce, période, scénario et mode de visualisation choisis), "
        "vous pouvez l’exporter dans plusieurs formats."
    ),
    "tutorial_export_png": (
        "PNG : image de bonne qualité, adaptée à l’affichage à l’écran ou dans des diapositives."
    ),
    "tutorial_export_jpg": (
        "JPG : image compressée, pratique pour des fichiers plus légers (web, mails, etc.)."
    ),
    "tutorial_export_pdf": (
        "PDF : document pratique pour l’impression ou l’intégration dans des rapports."
    ),
    "tutorial_export_tif": (
        "TIF : fichier raster géoréférencé destiné à un usage dans des logiciels SIG (QGIS, etc.)."
    ),
}
