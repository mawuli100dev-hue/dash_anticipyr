TEXTES_CA: dict[str, str] = {

    # --- app.py ---
    "page_title":               "Flora Pirinenca - mapes de distribució",
    "main_subtitle":            "Projecció de la distribució de les condicions climàtiques favorables i desfavorables per a les espècies pirinenques.",
    "btn_imprimer":             "Imprimir",
    "btn_imprimer_help":        "Descarregar l'informe PDF complet",
    "btn_imprimer_loading":     "Carregant...",
    "tab_carte":                "Mapa de distribució",
    "tab_ssp":                  "Escenaris SSP",
    "btn_imprimer_scenario":     "Imprimir la fitxa escenari seleccionat",
    "btn_imprimer_help":         "Imprimir la fitxa d'espècie per a l'escenari seleccionat",
    "btn_imprimer_complet":      "Imprimir la fitxa completa de l'espècie",
    "btn_imprimer_complet_help": "Imprimir la fitxa completa amb tots els períodes i els 4 escenaris SSP",
    "btn_preparer_scenario":      "Preparar fitxa d'escenari",
    "btn_preparer_complet":      "Preparar fitxa completa",
    "msg_generation_pdf":       "Generant PDF...",


    # --- sidebar.py ---
    "sidebar_titre":            "Flora Pirinenca",
    "sidebar_sous_titre":       "Seleccioneu una espècie, un període i un escenari",
    "sidebar_espece_label":     "Espècie estudiada",
    "sidebar_espece_caption":   "{n} espècie(s) disponible(s)",
    "sidebar_espece_error":     "No s'han trobat espècies.",
    "sidebar_espece_warning":   "Seleccioneu una espècie de la llista.",
    "sidebar_espece_help":      "Escriviu després d'obrir per filtrar la llista.",
    "sidebar_periode_label":    "Període de projecció",
    "sidebar_current_info":     "<strong>Període actual (1970-2000)</strong><br>Cap escenari SSP - dades climàtiques de referència.",
    "sidebar_ssp_label":        "Escenari climàtic (SSP)",
    "sidebar_mode_label":       "Mode de visualització",
    "sidebar_mode_help":        "Continu: probabilitat de presència entre 0 i 1  |  Desfavorable/Favorable: mapa binaritzat (dades ja 0/1)",
    "sidebar_footer":           "ANTICI'PYR",
    "ssp_126_desc":             "Optimista",
    "ssp_245_desc":             "Intermedi",
    "ssp_370_desc":             "Pessimista",
    "ssp_585_desc":             "Molt pessimista",
    "mode_continu":             "Continu",
    "mode_binaire":             "Desfavorable/Favorable",

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
    "map_titre_binaire":        "  ·  Desfavorable/Favorable",
    "ssp_manquant":             "`ssp` ha d'especificar-se per a un període futur.",

    # --- raster.py ---
    "cbar_continu_label":       "Probabilitat de presència",
    "cbar_continu_min":         "0.0\n(No favorable)",
    "cbar_continu_max":         "1.0\n(Molt favorable)",
    "cbar_binaire_label":       "Favorable / No favorable",
    "cbar_binaire_0":           "No favorable (0)",
    "cbar_binaire_1":           "Favorable (1)",
    "legende_continu_titre":    "Adequació climàtica",
    "legende_continu_min":      "No favorable",
    "legende_continu_max":      "Molt favorable",
    "legende_binaire_titre":    "Condicions climatiques",
    "legende_binaire_0":        "Desfavorable",
    "legende_binaire_1":        "Favorable",
    "btn_recentrer":            "Recentrar als Pirineus",

    # --- ssp_info.py ---
    "ssp_page_titre":           "## Escenaris climàtics (SSPs)",
    "ssp_intro":                "Els **SSPs** (Shared Socioeconomic Pathways) descriuen trajectòries socioeconòmiques que condueixen a diferents nivells d'emissions de gasos d'efecte hivernacle. Aquest tauler presenta les condicions climàtiques favorables per a les espècies pirinenques, projectades segons quatre escenaris climàtics fins al període 2081-2100.",
    "ssp_recap_titre":          "### Resum de les condicions climàtiques projectades per a l'horitzó 2081-2100, mitjançades sobre la serralada dels Pirineus.",
    "ssp_recap_col_ssp":        "SSP",
    "ssp_recap_col_emissions":  "Emissions",
    "ssp_recap_col_dt":         "Delta T (°C)",
    "ssp_recap_col_dp":         "Delta P (mm)",
    "ssp_ref_titre":            "### Referències",
    "ssp_ref_article":          "Article:",
    "ssp_ref_auteurs":          "Autors:",
    "ssp_ref_dashboard":        "Tauler:",
    "ssp_figure_caption":       "Projecció mitjana de temperatures i precipitacions als Pirineus a l'horitzó 2081-2100 segons diferents escenaris climàtics (Shared Socioeconomic Pathways, SSP), a partir de les dades WorldClim 2.1 i del conjunt de models de circulació general (2030, 2050, 2070 & 2090 corresponents als períodes 2021-2040, 2041-2060, 2061-2080 i 2081-2100).",
    "ssp_figure_manquant":      "Gràfic no trobat: `{chemin}`\nCol·loqueu el fitxer d'imatge a `dash_anticipyr/data/figures/`.",
    "ssp_126_label":            "Baixes emissions",
    "ssp_245_label":            "Emissions intermèdies",
    "ssp_370_label":            "Emissions elevades",
    "ssp_585_label":            "Emissions molt elevades",
    "ssp_126_description": "Escenari optimista amb polítiques climàtiques fortes, que condueix a emissions molt baixes abans de 2100.",
    "ssp_245_description": "Escenari intermedi amb polítiques climàtiques limitades, que dona lloc a una estabilització progressiva de les emissions.",
    "ssp_370_description": "Escenari pessimista marcat per una baixa cooperació internacional i un augment continu de les emissions.",
    "ssp_585_description": "Escenari extrem caracteritzat per una forta dependència dels combustibles fòssils i emissions molt elevades.",
    "ssp_temperature":        "Temperatura (2090):",
    "ssp_precipitations":       "Precipitacions (2090):",
    "ssp_valeurs_moyennes": "Valors mitjans estimats per a la serralada dels Pirineus",

    # --- interpretation.py ---
    "tab_interpretation": "Interpretació",
    "interp_intro_1": (
        "L'estudi es basa en una eina central de l'ecologia contemporània: "
        "els models de distribució d'espècies (Species Distribution Models, SDM). "
        "En la seva forma més completa, els SDM integren múltiples dimensions ecològiques "
        "(clima, dispersió, interaccions biòtiques, genètica), i permeten caracteritzar "
        "on i per què una espècie es manté."
    ),
    "interp_intro_2": (
        "Els mapes de distribució de les espècies pirinenques es construeixen a partir "
        "de variables climàtiques, en particular la precipitació i la temperatura. "
        "Resulten de la combinació de dades de presència (prospectes de camp, espècimens "
        "d'herbari, bases de dades en línia) amb un conjunt de variables ambientals que "
        "caracteritzen les condicions dels punts ocupats (vegeu la taula següent)."
    ),
    "interp_conclusion": (
        "Els models permeten definir les combinacions climàtiques associades a la presència "
        "(o absència) de l'espècie i, per tant, els ambients on és probable que es mantingui. "
        "Un cop traçat aquest retrat, és possible estudiar l'evolució d'aquestes condicions "
        "sota diferents climes futurs per estimar on l'espècie podria persistir, desplaçar-se "
        "o desaparèixer."
    ),

    "interp_col_description": "Descripció",
    "interp_col_unite": "Unitat",

    "interp_titre_temp": "Variables de temperatura (BIO1 - BIO11)",
    "interp_titre_prec": "Variables de precipitació (BIO12 - BIO19)",

    "interp_worldclim_titre": (
        "Taula A1: definicions de les variables bioclimàtiques de WorldClim 2.1."
    ),
    "interp_worldclim_caption": (
        "La base de dades pública WorldClim 2.1 (Fick & Hijmans, 2017) proporciona "
        "19 variables bioclimàtiques en format ràster, incloent-ne 11 relacionades amb "
        "la temperatura i 8 amb la precipitació. Aquestes variables es deriven de dades "
        "climàtiques mensuals mitjanes interpolades, recollides a partir d'estacions "
        "meteorològiques."
    ),

    "bio1_nom":  "Temperatura mitjana anual",
    "bio1_desc": "Temperatura mitjana anual",

    "bio2_nom":  "Rang diurn mitjà",
    "bio2_desc": "Mitjana dels rangs de temperatura mensuals (Tmax - Tmin)",

    "bio3_nom":  "Isotermalitat",
    "bio3_desc": "(BIO2 / BIO7) (*100): proporció de la variació diurna respecte de la variació anual",

    "bio4_nom":  "Estacionalitat de la temperatura",
    "bio4_desc": "Variabilitat de la temperatura (desviació estàndard * 100)",

    "bio5_nom":  "Temperatura màx. del mes més càlid",
    "bio5_desc": "Temperatura màxima del mes més càlid",

    "bio6_nom":  "Temperatura mín. del mes més fred",
    "bio6_desc": "Temperatura mínima del mes més fred",

    "bio7_nom":  "Rang anual de temperatura",
    "bio7_desc": "Rang anual de temperatura (BIO5 - BIO6)",

    "bio8_nom":  "Temperatura mitjana del trimestre més plujós",
    "bio8_desc": "Temperatura mitjana del trimestre més plujós",

    "bio9_nom":  "Temperatura mitjana del trimestre més sec",
    "bio9_desc": "Temperatura mitjana del trimestre més sec",

    "bio10_nom": "Temperatura mitjana del trimestre més càlid",
    "bio10_desc": "Temperatura mitjana del trimestre més càlid",

    "bio11_nom": "Temperatura mitjana del trimestre més fred",
    "bio11_desc":"Temperatura mitjana del trimestre més fred",

    "bio12_nom": "Precipitació anual",
    "bio12_desc":"Precipitació anual total",

    "bio13_nom": "Precipitació del mes més plujós",
    "bio13_desc":"Precipitació del mes més plujós",

    "bio14_nom": "Precipitació del mes més sec",
    "bio14_desc":"Precipitació del mes més sec",

    "bio15_nom": "Estacionalitat de la precipitació",
    "bio15_desc":"Variabilitat de la precipitació (coeficient de variació)",

    "bio16_nom": "Precipitació del trimestre més plujós",
    "bio16_desc":"Precipitació total del trimestre més plujós",

    "bio17_nom": "Precipitació del trimestre més sec",
    "bio17_desc":"Precipitació total del trimestre més sec",

    "bio18_nom": "Precipitació del trimestre més càlid",
    "bio18_desc":"Precipitació total del trimestre més càlid",

    "bio19_nom": "Precipitació del trimestre més fred",
    "bio19_desc":"Precipitació total del trimestre més fred",

    "legende_binaire_titre": "Condicions climàtiques",

    # --- tutorial.py ---

    "tab_tutorial": "Tutorial",

    "tutorial_sidebar_title": "Entendre la barra lateral",
    "tutorial_sidebar_intro": (
        "La barra lateral reuneix tots els paràmetres que controlen el mapa: "
        "idioma, espècie estudiada, període de projecció i escenari climàtic (SSP). "
        "Cada elecció modifica directament el mapa mostrat al centre de la pantalla."
    ),
    "tutorial_sidebar_lang": (
        "A la part superior, trieu l'idioma de visualització de l'aplicació."
    ),
    "tutorial_sidebar_species": (
        "A continuació, seleccioneu l'espècie estudiada a la llista desplegable. "
        "El nombre d'espècies disponibles s'indica just a sobre."
    ),
    "tutorial_sidebar_period": (
        "Trieu el període de projecció (per exemple 2021–2040)."
    ),
    "tutorial_sidebar_ssp": (
        "Després, escolliu un escenari climàtic (SSP 126, 245, 370 o 585). "
        "Els botons de colors van del més optimista (verd) al més pessimista (vermell)."
    ),
    "tutorial_sidebar_mode": (
        "Finalment, el mode de visualització permet mostrar una probabilitat de presència "
        "contínua o bé un mapa binari No favorable/Favorable."
    ),


    "tutorial_header_title": "Entendre els botons d'acció",
    "tutorial_header_intro": (
        "A la part superior de la pàgina, dos botons permeten preparar i imprimir "
        "fitxes en format PDF per a l'espècie seleccionada."
    ),
    "tutorial_header_prepare_scenario": (
        "Preparar la fitxa d'escenari: genera una fitxa per a la combinació actual "
        "de període i escenari climàtic."
    ),
    "tutorial_header_prepare_full": (
        "Preparar la fitxa completa: genera una fitxa que reuneix tots els períodes "
        "i els quatre escenaris SSP per a l'espècie escollida."
    ),
    "tutorial_header_tabs": (
        "Les pestanyes Mapa de distribució, Escenaris SSP, Interpretació i Tutorial "
        "permeten passar d'una vista a una altra de l'eina."
    ),


    "tutorial_map_title": "Fons de mapa i opacitat",
    "tutorial_map_intro": (
        "El mapa interactiu mostra la predicció de presència de l'espècie superposada "
        "a un fons de mapa (pla o satèl·lit)."
    ),
    "tutorial_map_basemap": (
        "Fons de mapa: trieu Pla (mapa de carreteres detallat) o Satèl·lit "
        "per visualitzar millor el relleu i l'ocupació del sòl."
    ),
    "tutorial_map_opacity": (
        "Opacitat de la predicció: el control lliscant ajusta la transparència de la capa "
        "de predicció. Una opacitat baixa deixa veure més el fons de mapa, una opacitat alta "
        "ressalta les zones favorables o desfavorables."
    ),
    "tutorial_map_recentre": (
        "Recentrar als Pirineus: recentra automàticament el mapa sobre tota la serralada."
    ),


    "tutorial_export_title": "Descarregar el mapa seleccionat",
    "tutorial_export_intro": (
        "Un cop mostrat el mapa (espècie, període, escenari i mode de visualització triats), "
        "el podeu exportar en diversos formats."
    ),
    "tutorial_export_png": (
        "PNG: imatge de bona qualitat, adequada per a la visualització en pantalla o en diapositives."
    ),
    "tutorial_export_jpg": (
        "JPG: imatge comprimida, pràctica per obtenir fitxers més lleugers (web, correus, etc.)."
    ),
    "tutorial_export_pdf": (
        "PDF: document pràctic per a la impressió o per incloure en informes."
    ),
    "tutorial_export_tif": (
        "TIF: fitxer ràster georeferenciat pensat per a l'ús en programes SIG (QGIS, etc.)."
    ),
}
