TEXTES_EN: dict[str, str] = {

    # --- app.py ---
    "page_title":               "Pyrenean Flora - distribution maps",
    "main_subtitle":            "Projection of the distribution of favourable and unfavourable climatic conditions for Pyrenean species.",
    "btn_imprimer":             "Print",
    "btn_imprimer_loading":     "Loading...",
    "tab_carte":                "Distribution map",
    "tab_ssp":                  "SSP Scenarios",
    "btn_imprimer_scenario":     "Print the selected scenario sheet",
    "btn_imprimer_help":         "Print the species sheet for the selected scenario",
    "btn_imprimer_complet":      "Print the complete species sheet",
    "btn_imprimer_complet_help": "Print the complete species sheet with all periods and 4 SSP scenarios",
    "btn_preparer_scenario":      "Prepare scenario sheet",
    "btn_preparer_complet":      "Prepare full sheet",
    "msg_generation_pdf":       "PDF generation in progress...",

    # --- sidebar.py ---
    "sidebar_titre":            "Pyrenean Flora",
    "sidebar_sous_titre":       "Select a species, a period and a scenario",
    "sidebar_espece_label":     "Species",
    "sidebar_espece_caption":   "{n} species available",
    "sidebar_espece_error":     "No species found.",
    "sidebar_espece_warning":   "Please select a species from the list.",
    "sidebar_espece_help":      "Type after opening to filter the list.",
    "sidebar_periode_label":    "Projection period",
    "sidebar_current_info":     "<strong>Current period (1970-2000)</strong><br>No SSP scenario - baseline climate data.",
    "sidebar_ssp_label":        "Climate scenario (SSP)",
    "sidebar_mode_label":       "Visualisation mode",
    "sidebar_mode_help":        "Continuous: presence probability between 0 and 1  |  Unfavourable/Favourable: binarised map (0/1 data)",
    "sidebar_footer":           "ANTICI'PYR",
    "ssp_126_desc":             "Optimistic",
    "ssp_245_desc":             "Intermediate",
    "ssp_370_desc":             "Pessimistic",
    "ssp_585_desc":             "Very pessimistic",
    "mode_continu":             "Continuous",
    "mode_binaire":             "Unfavourable/Favourable",

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
    "map_titre_binaire":        "  ·  Unfavourable/Favourable",
    "ssp_manquant":             "`ssp` must be provided for a future period.",

    # --- raster.py ---
    "cbar_continu_label":       "Probability of presence",
    "cbar_continu_min":         "0.0\n(Unsuitable)",
    "cbar_continu_max":         "1.0\n(Highly suitable)",
    "cbar_binaire_label":       "Suitable / Unsuitable",
    "cbar_binaire_0":           "Unsuitable (0)",
    "cbar_binaire_1":           "Suitable (1)",
    "legende_continu_titre":  "Climatic suitability",
    "legende_continu_min":      "Unsuitable",
    "legende_continu_max":      "Highly suitable",
    "legende_binaire_titre":  "Climate conditions",
    "legende_binaire_0":      "Unfavourable",
    "legende_binaire_1":      "Favourable",
    "btn_recentrer":          "Recenter on the Pyrenees",

    # --- ssp_info.py ---
    "ssp_page_titre":           "## Climate scenarios (SSPs)",
    "ssp_intro":                "**SSPs** (Shared Socioeconomic Pathways) describe socioeconomic trajectories leading to different levels of greenhouse gas emissions. This dashboard presents the climatic conditions favourable to Pyrenean species, projected under four climate scenarios up to the period 2081-2100.",
    "ssp_recap_titre":          "### Summary of projected climatic conditions for the 2081-2100 horizon, averaged across the Pyrenean range",
    "ssp_recap_col_ssp":        "SSP",
    "ssp_recap_col_emissions":  "Emissions",
    "ssp_recap_col_dt":         "Delta T (°C)",
    "ssp_recap_col_dp":         "Delta P (mm)",
    "ssp_ref_titre":            "### References",
    "ssp_ref_article":          "Article:",
    "ssp_ref_auteurs":          "Authors:",
    "ssp_ref_dashboard":        "Dashboard:",
    "ssp_figure_caption":       "Mean projected temperature and precipitation in the Pyrenees at the 2081-2100 horizon under different climate scenarios (Shared Socioeconomic Pathways, SSP), based on WorldClim 2.1 data and the full ensemble of general circulation models (2030, 2050, 2070 & 2090 corresponding to the periods 2021-2040, 2041-2060, 2061-2080 and 2081-2100).",
    "ssp_figure_manquant":      "Figure not found: `{chemin}`\nPlace the image file in `dash_anticipyr/data/figures/`.",
    "ssp_126_label":            "Low emissions",
    "ssp_245_label":            "Intermediate emissions",
    "ssp_370_label":            "High emissions",
    "ssp_585_label":            "Very high emissions",
    "ssp_126_description": "Optimistic scenario with strong climate policies, leading to very low emissions by 2100.",
    "ssp_245_description": "Intermediate scenario with limited climate policies, resulting in a gradual stabilisation of emissions.",
    "ssp_370_description": "Pessimistic scenario marked by low international cooperation and a continuous rise in emissions.",
    "ssp_585_description": "Extreme scenario characterised by heavy dependence on fossil fuels and very high emissions.",
    "ssp_temperature":          "Temperature (2090):",
    "ssp_precipitations":       "Precipitation (2090):",
    "ssp_valeurs_moyennes": "Estimated mean values for the Pyrenean range",

    # --- interpretation.py ---

    "tab_interpretation": "Interpretation",
    "interp_intro_1":       "This study relies on a central tool of contemporary ecology: Species Distribution Models (SDMs). In their most complete form, SDMs integrate multiple ecological dimensions (climate, dispersal, biotic interactions, genetics), characterising where and why a species persists.",
    "interp_intro_2":       "Distribution maps of Pyrenean species are built from climatic variables, particularly precipitation and temperature. They result from the combination of presence data (field surveys, herbarium specimens, online databases) with a set of environmental variables characterising the conditions at occupied sites (see table below).",
    "interp_conclusion":    "Models define the climatic combinations associated with the presence (or absence) of the species, and therefore the environments where it is likely to persist. Once this portrait is established, it becomes possible to study how these conditions evolve under different future climates to estimate where the species could survive, migrate or disappear.",
    "interp_col_variable":  "Variable",
    "interp_col_nom":       "Name",
    "interp_col_description": "Description",
    "interp_col_unite":     "Unit",
    "interp_titre_temp":    "Temperature variables (BIO1 - BIO11)",
    "interp_titre_prec":    "Precipitation variables (BIO12 - BIO19)",
    "interp_worldclim_titre":   "Table A1: Definitions of WorldClim 2.1 bioclimatic variables.",
    "interp_worldclim_caption": "The WorldClim 2.1 public database (Fick & Hijmans, 2017) provides 19 bioclimatic variables in a raster layer format, including 11 related to temperature and 8 to precipitation. These variables are derived from interpolated average monthly climate data collected from weather stations.",
    "bio1_nom":  "Annual mean temperature",
    "bio1_desc": "Annual mean temperature",
    "bio2_nom":  "Mean diurnal range",
    "bio2_desc": "Mean of monthly temperature ranges (Tmax - Tmin)",
    "bio3_nom":  "Isothermality",
    "bio3_desc": "(BIO2 / BIO7) (*100): Ratio of diurnal to annual temperature variation",
    "bio4_nom":  "Temperature seasonality",
    "bio4_desc": "Temperature variability (standard deviation * 100)",
    "bio5_nom":  "Max temperature of warmest month",
    "bio5_desc": "Maximum temperature of the warmest month",
    "bio6_nom":  "Min temperature of coldest month",
    "bio6_desc": "Minimum temperature of the coldest month",
    "bio7_nom":  "Temperature annual range",
    "bio7_desc": "Annual temperature range (BIO5 - BIO6)",
    "bio8_nom":  "Mean temperature of wettest quarter",
    "bio8_desc": "Mean temperature of the wettest quarter",
    "bio9_nom":  "Mean temperature of driest quarter",
    "bio9_desc": "Mean temperature of the driest quarter",
    "bio10_nom": "Mean temperature of warmest quarter",
    "bio10_desc":"Mean temperature of the warmest quarter",
    "bio11_nom": "Mean temperature of coldest quarter",
    "bio11_desc":"Mean temperature of the coldest quarter",
    "bio12_nom": "Annual precipitation",
    "bio12_desc":"Total annual precipitation",
    "bio13_nom": "Precipitation of wettest month",
    "bio13_desc":"Precipitation of the wettest month",
    "bio14_nom": "Precipitation of driest month",
    "bio14_desc":"Precipitation of the driest month",
    "bio15_nom": "Precipitation seasonality",
    "bio15_desc":"Precipitation variability (coefficient of variation)",
    "bio16_nom": "Precipitation of wettest quarter",
    "bio16_desc":"Total precipitation of the wettest quarter",
    "bio17_nom": "Precipitation of driest quarter",
    "bio17_desc":"Total precipitation of the driest quarter",
    "bio18_nom": "Precipitation of warmest quarter",
    "bio18_desc":"Total precipitation of the warmest quarter",
    "bio19_nom": "Precipitation of coldest quarter",
    "bio19_desc":"Total precipitation of the coldest quarter",

    # --- tutorial.py ---

    "tab_tutorial": "Tutorial",

    "tutorial_sidebar_title": "Understanding the sidebar",
    "tutorial_sidebar_intro": (
        "The sidebar groups all the settings that control the map: "
        "language, species, projection period and climate scenario (SSP). "
        "Each choice directly changes the map displayed in the centre of the screen."
    ),
    "tutorial_sidebar_lang": (
        "At the top, choose the display language of the application."
    ),
    "tutorial_sidebar_species": (
        "Then select the study species from the dropdown list. "
        "The number of available species is shown just above."
    ),
    "tutorial_sidebar_period": (
        "Choose the projection period (for example 2021–2040)."
    ),
    "tutorial_sidebar_ssp": (
        "Next, choose a climate scenario (SSP 126, 245, 370 or 585). "
        "The coloured buttons go from the most optimistic (green) to the most pessimistic (red)."
    ),
    "tutorial_sidebar_mode": (
        "Finally, the visualisation mode lets you display either a continuous "
        "probability of presence or a binary Unsuitable/Suitable map."
    ),


    "tutorial_header_title": "Understanding the action buttons",
    "tutorial_header_intro": (
        "At the top of the page, two buttons let you prepare and print "
        "PDF sheets for the selected species."
    ),
    "tutorial_header_prepare_scenario": (
        "Prepare scenario sheet: generates a sheet for the current "
        "combination of period and climate scenario."
    ),
    "tutorial_header_prepare_full": (
        "Prepare full sheet: generates a sheet that gathers all periods "
        "and the four SSP scenarios for the chosen species."
    ),
    "tutorial_header_tabs": (
        "The tabs Distribution map, SSP scenarios, Interpretation and Tutorial "
        "allow you to switch between the different views of the tool."
    ),


    "tutorial_map_title": "Basemap and opacity",
    "tutorial_map_intro": (
        "The interactive map displays the predicted presence of the species overlaid "
        "on a basemap (plan or satellite)."
    ),
    "tutorial_map_basemap": (
        "Basemap: choose Map (detailed road map) or Satellite "
        "to better see relief and land cover."
    ),
    "tutorial_map_opacity": (
        "Prediction opacity: the slider controls the transparency of the prediction layer. "
        "Low opacity reveals more of the basemap, high opacity highlights suitable or unsuitable areas."
    ),
    "tutorial_map_recentre": (
        "Recenter on the Pyrenees: automatically recentres the map on the whole mountain range."
    ),


    "tutorial_export_title": "Download the selected map",
    "tutorial_export_intro": (
        "Once the map is displayed (species, period, scenario and visualisation mode chosen), "
        "you can export it in several formats."
    ),
    "tutorial_export_png": (
        "PNG: good-quality image, suitable for screen display or slides."
    ),
    "tutorial_export_jpg": (
        "JPG: compressed image, useful for lighter files (web, emails, etc.)."
    ),
    "tutorial_export_pdf": (
        "PDF: convenient document for printing or including in reports."
    ),
    "tutorial_export_tif": (
        "TIF: georeferenced raster file for use in GIS software (QGIS, etc.)."
    ),
}
