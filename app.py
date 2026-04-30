"""
Deryball — Application Streamlit principale.
"""
import streamlit as st
import pandas as pd
from stats import calculer_tout

st.set_page_config(page_title="Deryball", page_icon="⚽", layout="wide")
# ============================================================
# THÈME PERSONNALISÉ — Style Linear / FM24 (gris-mauve)
# ============================================================
# ============================================================
# THÈME PERSONNALISÉ — Style Linear / FM24 (gris-mauve)
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,600;12..96,700&family=Manrope:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');
:root {
    --bg-deep: #0A0A12;
    --bg-base: #11111B;
    --bg-surface: #1A1830;
    --bg-elevated: #211F3A;
    --bg-hover: #2A2848;
    --border-subtle: #25253A;
    --border-default: #35354F;
    --border-strong: #4A4A6A;
    --text-strong: #F0F0F8;
    --text-default: #C8C8D5;
    --text-muted: #8B8BA0;
    --text-faint: #5C5C70;
    --accent: #8266FF;
    --accent-soft: #6E5FE6;
    --accent-deep: #4A3FA8;
    --accent-glow: rgba(130,102,255,0.18);
    --success: #4ADE80;
    --danger: #F43F5E;
    --warning: #FBBF24;
    --info: #60A5FA;
}

/* FOND GLOBAL avec dégradés mauve visibles */
.stApp {
    background: var(--bg-deep) !important;
    font-family: 'Manrope', sans-serif !important;
}
[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 1000px 700px at 0% 0%, rgba(130,102,255,0.18) 0%, transparent 50%),
        radial-gradient(ellipse 900px 600px at 100% 100%, rgba(130,102,255,0.10) 0%, transparent 50%),
        radial-gradient(ellipse 600px 400px at 50% 50%, rgba(110,95,230,0.04) 0%, transparent 70%),
        var(--bg-deep) !important;
}

/* Tous les textes par défaut */
.stApp, .stApp p, .stApp span, .stApp label, .stApp div {
    font-family: 'Manrope', sans-serif;
    color: var(--text-default);
}

/* TITRES */
h1, h2, h3, h4, h5, h6,
.stApp h1, .stApp h2, .stApp h3, .stApp h4 {
    font-family: 'Bricolage Grotesque', sans-serif !important;
    color: var(--text-strong) !important;
    letter-spacing: -0.02em !important;
    font-weight: 600 !important;
}
h1 { font-size: 38px !important; font-weight: 700 !important; letter-spacing: -0.025em !important; }
h4 { font-size: 16px !important; }

/* st.metric */
[data-testid="stMetricValue"] {
    font-family: 'Bricolage Grotesque', sans-serif !important;
    color: var(--text-strong) !important;
    font-size: 32px !important;
    font-weight: 600 !important;
    letter-spacing: -0.02em !important;
    font-variant-numeric: tabular-nums !important;
}
[data-testid="stMetricLabel"] {
    color: var(--text-muted) !important;
    font-size: 13px !important;
    font-weight: 500 !important;
}

/* CONTAINER PRINCIPAL */
.block-container {
    padding-top: 2.5rem !important;
    padding-bottom: 4rem !important;
    max-width: 1480px !important;
}

/* ======================================================
   ENCADRER LES BLOCS HORIZONTAUX (filtres, chips)
   ====================================================== */

/* Le truc malin : on encadre les st.columns horizontaux contenant des selects/inputs/buttons */
[data-testid="stHorizontalBlock"]:has(> div [data-testid="stSelectbox"]),
[data-testid="stHorizontalBlock"]:has(> div [data-testid="stTextInput"]) {
    background:
        linear-gradient(135deg, rgba(130,102,255,0.06) 0%, rgba(130,102,255,0.02) 100%),
        var(--bg-surface);
    border: 1px solid rgba(130,102,255,0.20);
    border-radius: 12px;
    padding: 14px 16px;
    margin-bottom: 16px;
}

/* ======================================================
   ONGLETS — look propre avec underline mauve
   ====================================================== */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px !important;
    border-bottom: 1px solid var(--border-default) !important;
    background: transparent !important;
    padding-bottom: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-muted) !important;
    border-bottom: 2px solid transparent !important;
    border-radius: 0 !important;
    padding: 12px 18px !important;
    font-weight: 500 !important;
    font-size: 14px !important;
    transition: all 0.15s ease !important;
    margin-bottom: -1px !important;
}
.stTabs [data-baseweb="tab"]:hover {
    color: var(--text-default) !important;
    background: rgba(130,102,255,0.05) !important;
}
.stTabs [aria-selected="true"] {
    color: var(--text-strong) !important;
    border-bottom: 2px solid var(--accent) !important;
    background: rgba(130,102,255,0.22) !important;
    border-radius: 8px 8px 0 0 !important;
    background: rgba(130,102,255,0.50) !important;
}
.stTabs [data-baseweb="tab-panel"] { padding-top: 24px !important; }

/* ======================================================
   INPUTS, SELECTS, TEXT
   ====================================================== */
.stSelectbox label, .stTextInput label {
    color: var(--text-muted) !important;
    font-size: 11.5px !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
    margin-bottom: 4px !important;
}
.stSelectbox > div > div,
.stTextInput > div > div > input {
    background-color: var(--bg-elevated) !important;
    border: 1px solid var(--border-default) !important;
    border-radius: 8px !important;
    color: var(--text-strong) !important;
    font-family: 'Manrope', sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    transition: all 0.15s ease !important;
}

/* Hauteur et padding cohérents pour les selectbox */
.stSelectbox > div > div {
    min-height: 42px !important;
    padding: 4px 12px !important;
    display: flex !important;
    align-items: center !important;
}

/* Le conteneur du texte affiché (BaseWeb) */
.stSelectbox div[data-baseweb="select"] > div {
    min-height: 36px !important;
}

/* Le texte de la valeur sélectionnée */
.stSelectbox div[data-baseweb="select"] > div > div {
    line-height: 1.5 !important;
    overflow: visible !important;
    white-space: nowrap !important;
    padding: 4px 0 !important;
}

/* Padding spécifique des inputs texte */
.stTextInput > div > div > input {
    padding: 10px 14px !important;
    min-height: 42px !important;
}
.stSelectbox > div > div:hover,
.stTextInput > div > div > input:hover {
    border-color: var(--accent-soft) !important;
    background-color: var(--bg-hover) !important;
}

/* Popover des selects */
[data-baseweb="popover"] [role="listbox"] {
    background: var(--bg-elevated) !important;
    border: 1px solid var(--border-default) !important;
    border-radius: 8px !important;
}
[data-baseweb="popover"] [role="option"] {
    background: var(--bg-elevated) !important;
    color: var(--text-default) !important;
    font-family: 'Manrope', sans-serif !important;
}
[data-baseweb="popover"] [role="option"]:hover {
    background: var(--accent-glow) !important;
    color: var(--text-strong) !important;
}

/* ======================================================
   BOUTONS (les chips)
   ====================================================== */
.stButton > button {
    background: var(--bg-elevated) !important;
    border: 1px solid var(--border-default) !important;
    border-radius: 8px !important;
    color: var(--text-default) !important;
    font-family: 'Manrope', sans-serif !important;
    font-weight: 500 !important;
    font-size: 13px !important;
    padding: 8px 14px !important;
    transition: all 0.12s ease !important;
}
.stButton > button:hover {
    border-color: var(--accent-soft) !important;
    color: var(--text-strong) !important;
    background: var(--accent-glow) !important;
    transform: translateY(-1px);
}
.stButton > button:active { transform: translateY(0); }
.stButton > button[kind="primary"] {
    background: linear-gradient(180deg, var(--accent-soft) 0%, var(--accent-deep) 100%) !important;
    border-color: var(--accent) !important;
    color: white !important;
    box-shadow: 0 1px 6px rgba(130,102,255,0.3) !important;
}

/* ======================================================
   TOGGLE / SWITCH (st.toggle) — couleur mauve assumée
   ====================================================== */

/* Le rail (track) du toggle — état OFF */
.stCheckbox [role="switch"],
[data-baseweb="checkbox"] [role="checkbox"],
[data-baseweb="switch"] > div {
    background-color: var(--bg-elevated) !important;
    border: 1px solid var(--border-default) !important;
    transition: all 0.2s ease !important;
}

/* Le rail — état ON (mauve plein) */
.stCheckbox [role="switch"][aria-checked="true"],
[data-baseweb="checkbox"][aria-checked="true"] [role="checkbox"],
[data-baseweb="switch"][aria-checked="true"] > div {
    background-color: var(--accent) !important;
    border-color: var(--accent-soft) !important;
    box-shadow: 0 0 0 4px rgba(130,102,255,0.20) !important;
}

/* Le knob (petit bouton rond qui glisse) — état OFF */
.stCheckbox [role="switch"] > div,
[data-baseweb="checkbox"] [role="checkbox"] > div {
    background-color: var(--text-muted) !important;
    transition: all 0.2s ease !important;
}

/* Le knob — état ON (blanc) */
.stCheckbox [role="switch"][aria-checked="true"] > div,
[data-baseweb="checkbox"][aria-checked="true"] [role="checkbox"] > div {
    background-color: white !important;
}

/* Override la couleur primaire bleue par défaut de Streamlit */
.stCheckbox div[data-testid="stCheckbox"] label > div:first-child[style*="background"] {
    background-color: var(--accent) !important;
}

/* ======================================================
   CAPTIONS et DIVIDERS
   ====================================================== */
[data-testid="stCaptionContainer"] {
    color: var(--text-muted) !important;
    font-size: 12.5px !important;
}
hr {
    border: none !important;
    border-top: 1px solid var(--border-default) !important;
    margin: 18px 0 !important;
}

/* ======================================================
   TABLEAUX (DATAFRAME) — la grosse partie
   ====================================================== */
.stDataFrame, [data-testid="stDataFrame"] {
    border-radius: 12px !important;
    overflow: hidden !important;
    border: 1px solid var(--border-default) !important;
    background: var(--bg-surface) !important;
    box-shadow: 0 4px 16px rgba(0,0,0,0.2) !important;
}
.stDataFrame thead tr th {
    background: var(--bg-elevated) !important;
    color: var(--text-muted) !important;
    font-family: 'Manrope', sans-serif !important;
    font-weight: 600 !important;
    font-size: 11px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
    border-bottom: 1px solid var(--border-default) !important;
    padding: 14px 10px !important;
}
.stDataFrame tbody tr td {
    color: var(--text-default);
    font-family: 'JetBrains Mono', monospace !important;
    font-variant-numeric: tabular-nums !important;
    font-size: 13px !important;
    border-bottom: 1px solid var(--border-subtle) !important;
    padding: 10px 10px !important;
}
.stDataFrame tbody tr:hover td { filter: brightness(1.15); }
.stDataFrame tbody tr td:first-child,
.stDataFrame tbody tr td:nth-child(2),
.stDataFrame tbody tr td:nth-child(3) {
    font-family: 'Manrope', sans-serif !important;
    font-weight: 500 !important;
}

/* ======================================================
   ALERTES (st.info, st.warning, etc.)
   ====================================================== */
.stAlert {
    background: var(--bg-surface) !important;
    border: 1px solid var(--border-default) !important;
    border-left: 3px solid var(--accent) !important;
    border-radius: 8px !important;
}
/* ======================================================
   EXPANDERS (st.expander)
   ====================================================== */
[data-testid="stExpander"] {
    background: var(--bg-surface) !important;
    border: 1px solid var(--border-default) !important;
    border-radius: 8px !important;
    margin-bottom: 12px !important;
}
[data-testid="stExpander"] summary,
[data-testid="stExpander"] details > summary {
    color: var(--text-default) !important;
    font-family: 'Manrope', sans-serif !important;
    font-size: 13.5px !important;
    font-weight: 500 !important;
    padding: 10px 14px !important;
    cursor: pointer !important;
    list-style: none !important;
}
[data-testid="stExpander"] summary:hover {
    color: var(--text-strong) !important;
    background: var(--bg-elevated) !important;
}

/* Cacher TOUTES les variantes d'icônes Material qui peuvent fuiter en texte */
[data-testid="stExpander"] summary [class*="material-symbols"],
[data-testid="stExpander"] summary [class*="material-icons"],
[data-testid="stExpander"] summary [class*="MaterialIcon"],
[data-testid="stExpander"] summary [data-testid="stIconMaterial"],
[data-testid="stExpander"] summary [data-testid*="Icon"],
[data-testid="stExpander"] summary [aria-hidden="true"]:not(svg) {
    font-size: 0 !important;
    line-height: 0 !important;
    width: 0 !important;
    height: 0 !important;
    overflow: hidden !important;
    color: transparent !important;
}

/* Pseudo-éléments natifs du <details> */
[data-testid="stExpander"] summary::before,
[data-testid="stExpander"] summary::-webkit-details-marker {
    display: none !important;
}

/* Garder le SVG s'il est présent */
[data-testid="stExpander"] summary svg {
    fill: var(--text-muted) !important;
    transition: transform 0.2s ease !important;
}
[data-testid="stExpander"] details[open] summary svg {
    transform: rotate(90deg);
}

/* Le contenu interne */
[data-testid="stExpander"] [data-testid="stExpanderDetails"] {
    padding: 0 14px 14px 14px !important;
    color: var(--text-default) !important;
}
[data-testid="stExpander"] summary:hover {
    color: var(--text-strong) !important;
    background: var(--bg-elevated) !important;
}
/* Icône flèche : on cache le texte parasite et on garde l'SVG */
[data-testid="stExpander"] summary span:not([data-testid]) {
    font-size: 0 !important;
}
[data-testid="stExpander"] summary svg {
    fill: var(--text-muted) !important;
    transition: transform 0.2s ease !important;
}
[data-testid="stExpander"] details[open] summary svg {
    transform: rotate(90deg);
}
/* Pseudo-éléments éventuels */
[data-testid="stExpander"] summary::before,
[data-testid="stExpander"] summary::-webkit-details-marker {
    display: none !important;
}
/* Le contenu interne */
[data-testid="stExpander"] [data-testid="stExpanderDetails"] {
    padding: 0 14px 14px 14px !important;
    color: var(--text-default) !important;
}
/* ======================================================
   SCROLLBARS personnalisées
   ====================================================== */
::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-track { background: var(--bg-base); }
::-webkit-scrollbar-thumb {
    background: var(--border-default);
    border-radius: 5px;
}
::-webkit-scrollbar-thumb:hover { background: var(--border-strong); }
</style>
""", unsafe_allow_html=True)
# ============================================================
# DESCRIPTIONS DES COLONNES (tooltips au survol de l'entête)
# ============================================================
DESCRIPTIONS_COLONNES = {
    # Colonnes de base
    "Team": "Nom de l'équipe",
    "League": "Ligue / championnat",
    "Season": "Saison concernée",
    "Date": "Date du match",
    "DateNY": "Date du match en heure de New York",
    "TimeNY": "Heure de début du match (heure de New York)",
    "HomeTeam": "Équipe à domicile",
    "AwayTeam": "Équipe à l'extérieur",
    "Score": "Score final du match (ou 'À VENIR' si pas encore joué)",

    # Classement et forme
    "Pos": "Position actuelle au classement",
    "Pts": "Points accumulés cette saison",
    "Form5": "Forme sur les 5 derniers matchs (V=victoire, N=nul, D=défaite)",
    "MP": "Nombre de matchs joués",
    "W": "Victoires",
    "D": "Matchs nuls",
    "L": "Défaites",
    "GF_pg": "Buts marqués par match (moyenne)",
    "GA_pg": "Buts encaissés par match (moyenne)",
    "Total_pg": "Total de buts par match (moyenne)",
    "Spark_GF": "Buts marqués sur les 10 derniers matchs (ancien à gauche, récent à droite)",
    "Spark_GA": "Buts encaissés sur les 10 derniers matchs (ancien à gauche, récent à droite)",
    "Spark_Total": "Total de buts par match sur les 10 derniers — utile pour la tendance Over/Under",
    # Pourcentages généraux
    "Over05_pct": "% des matchs avec au moins 1 but",
    "Over15_pct": "% des matchs avec au moins 2 buts",
    "Over25_pct": "% des matchs avec au moins 3 buts (plus de 2.5)",
    "BTTS_pct": "% des matchs où les 2 équipes ont marqué",
    "Count00": "Nombre de matchs terminés 0-0",
    "Pct00": "% des matchs terminés 0-0",
    "CS_pct": "% de matchs où l'équipe n'a pas encaissé (clean sheet)",
    "FTS_pct": "% de matchs où l'équipe n'a pas marqué",

    # Séquences en cours
    "Streak_NoScore": "Nombre de matchs consécutifs sans marquer",
    "Streak_NoConcede": "Matchs consécutifs sans encaisser",
    "Streak_BTTS": "Matchs consécutifs où les 2 équipes ont marqué",
    "Streak_NoBTTS": "Matchs consécutifs où au moins une équipe n'a pas marqué",
    "Streak_Over05": "Matchs consécutifs avec au moins 1 but",
    "Streak_Over15": "Matchs consécutifs avec au moins 2 buts",
    "Streak_Over25": "Matchs consécutifs avec plus de 2.5 buts",
    "Streak_Under25": "Matchs consécutifs avec moins de 2.5 buts",
    "Streak_No00": "Matchs consécutifs sans 0-0",
    "Streak_Win": "Victoires consécutives",
    "Streak_NoWin": "Matchs consécutifs sans victoire",
    "Streak_Loss": "Défaites consécutives",
    "L10_Over25_pct": "% Over 2.5 sur les 10 derniers matchs",
    "L10_BTTS_pct": "% BTTS sur les 10 derniers matchs",

    # Force Poisson
    "HomeAttack": "Force offensive à domicile (1.00 = moyenne de la ligue)",
    "HomeDefense": "Force défensive à domicile (1.00 = moyenne, <1 = bon)",
    "AwayAttack": "Force offensive à l'extérieur (1.00 = moyenne)",
    "AwayDefense": "Force défensive à l'extérieur (1.00 = moyenne, <1 = bon)",
    "xG_home": "Buts attendus à domicile (Poisson)",
    "xG_away": "Buts attendus à l'extérieur (Poisson)",

    # Colonnes matchup — Domicile (H_)
    "H_Pos": "Classement actuel de l'équipe à domicile",
    "H_Form": "Forme sur les 5 derniers matchs (domicile)",
    "H_Over05": "% Over 0.5 de l'équipe à domicile",
    "H_Over15": "% Over 1.5 de l'équipe à domicile",
    "H_Over25": "% Over 2.5 de l'équipe à domicile",
    "H_BTTS": "% BTTS de l'équipe à domicile",
    "H_00_Count": "Nombre de 0-0 de l'équipe à domicile",
    "H_00_Pct": "% de 0-0 de l'équipe à domicile",

    # Colonnes matchup — Extérieur (A_)
    "A_Pos": "Classement actuel de l'équipe à l'extérieur",
    "A_Form": "Forme sur les 5 derniers matchs (extérieur)",
    "A_Over05": "% Over 0.5 de l'équipe à l'extérieur",
    "A_Over15": "% Over 1.5 de l'équipe à l'extérieur",
    "A_Over25": "% Over 2.5 de l'équipe à l'extérieur",
    "A_BTTS": "% BTTS de l'équipe à l'extérieur",
    "A_00_Count": "Nombre de 0-0 de l'équipe à l'extérieur",
    "A_00_Pct": "% de 0-0 de l'équipe à l'extérieur",

    # Ligues (pour matchups personnalisés)
    "H_Ligue": "Ligue de l'équipe à domicile",
    "A_Ligue": "Ligue de l'équipe à l'extérieur",

    # Combiné
    "Combined_00_Pct": "Moyenne des % de 0-0 des 2 équipes",

    # Poisson (P_)
    "xG_H": "Buts attendus de l'équipe domicile (modèle Poisson)",
    "xG_A": "Buts attendus de l'équipe extérieur (modèle Poisson)",
    "P_Over05": "Probabilité Poisson qu'il y ait au moins 1 but",
    "P_Over15": "Probabilité Poisson qu'il y ait au moins 2 buts",
    "P_Over25": "Probabilité Poisson qu'il y ait plus de 2.5 buts",
    "P_BTTS": "Probabilité Poisson que les 2 équipes marquent",
    "P_00": "Probabilité Poisson que le match finisse 0-0",

    # Head to Head (H2H_)
    "H2H_N": "Nombre de confrontations passées entre ces 2 équipes",
    "H2H_AvgGoals": "Moyenne de buts par match dans les confrontations passées",
    "H2H_BTTS_pct": "% BTTS dans les confrontations passées",
    "H2H_O25_pct": "% Over 2.5 dans les confrontations passées",
    "H2H_00_pct": "% de 0-0 dans les confrontations passées",

    # Stats additionnelles (tirs, corners, cartons, fautes)
    "Shots_pg": "Tirs par match (moyenne)",
    "ShotsContre_pg": "Tirs concédés par match (moyenne)",
    "ShotsTarget_pg": "Tirs cadrés par match (moyenne)",
    "ShotsTargetContre_pg": "Tirs cadrés concédés par match (moyenne)",
    "Corners_pg": "Corners par match (moyenne)",
    "CornersContre_pg": "Corners concédés par match (moyenne)",
    "CornersTotal_pg": "Total de corners dans les matchs de l'équipe (moyenne)",
    "CornersOver95_pct": "% de matchs avec plus de 9.5 corners au total",
    "CornersOver85_pct": "% de matchs avec plus de 8.5 corners au total",
    "CornersOver105_pct": "% de matchs avec plus de 10.5 corners au total",
    "Yellow_pg": "Cartons jaunes reçus par match",
    "YellowContre_pg": "Cartons jaunes reçus par l'adversaire par match",
    "YellowsTotal_pg": "Total de jaunes dans les matchs (2 équipes)",
    "YellowsOver35_pct": "% de matchs avec plus de 3.5 jaunes au total",
    "Red_pg": "Cartons rouges par match",
    "RedContre_pg": "Cartons rouges concédés par match",
    "Fouls_pg": "Fautes commises par match",
    "FoulsContre_pg": "Fautes subies par match",
    # Stats additionnelles dans Matchs/Matchups — Domicile
    "H_Shots_pg": "Tirs par match (équipe à domicile)",
    "H_ShotsTarget_pg": "Tirs cadrés par match (équipe à domicile)",
    "H_Corners_pg": "Corners par match (équipe à domicile)",
    "H_CornersContre_pg": "Corners concédés par match (équipe à domicile)",
    "H_CornersTotal_pg": "Total de corners dans les matchs (équipe à domicile)",
    "H_CornersOver85": "% matchs avec plus de 8.5 corners (équipe à domicile)",
    "H_CornersOver95": "% matchs avec plus de 9.5 corners (équipe à domicile)",
    "H_CornersOver105": "% matchs avec plus de 10.5 corners (équipe à domicile)",
    "H_Yellow_pg": "Cartons jaunes par match (équipe à domicile)",
    "H_YellowsTotal_pg": "Total jaunes dans les matchs (équipe à domicile)",
    "H_YellowsOver35": "% matchs avec plus de 3.5 jaunes (équipe à domicile)",
    "H_Red_pg": "Cartons rouges par match (équipe à domicile)",
    "H_Fouls_pg": "Fautes par match (équipe à domicile)",

    # Stats additionnelles dans Matchs/Matchups — Extérieur
    "A_Shots_pg": "Tirs par match (équipe à l'extérieur)",
    "A_ShotsTarget_pg": "Tirs cadrés par match (équipe à l'extérieur)",
    "A_Corners_pg": "Corners par match (équipe à l'extérieur)",
    "A_CornersContre_pg": "Corners concédés par match (équipe à l'extérieur)",
    "A_CornersTotal_pg": "Total de corners dans les matchs (équipe à l'extérieur)",
    "A_CornersOver85": "% matchs avec plus de 8.5 corners (équipe à l'extérieur)",
    "A_CornersOver95": "% matchs avec plus de 9.5 corners (équipe à l'extérieur)",
    "A_CornersOver105": "% matchs avec plus de 10.5 corners (équipe à l'extérieur)",
    "A_Yellow_pg": "Cartons jaunes par match (équipe à l'extérieur)",
    "A_YellowsTotal_pg": "Total jaunes dans les matchs (équipe à l'extérieur)",
    "A_YellowsOver35": "% matchs avec plus de 3.5 jaunes (équipe à l'extérieur)",
    "A_Red_pg": "Cartons rouges par match (équipe à l'extérieur)",
    "A_Fouls_pg": "Fautes par match (équipe à l'extérieur)",
    "H_Signaux": "Anomalies détectées chez l'équipe à domicile (forme récente vs saison)",
    "A_Signaux": "Anomalies détectées chez l'équipe à l'extérieur (forme récente vs saison)",
}
# ============================================================
# LABELS COURTS ET LISIBLES POUR LES COLONNES
# ============================================================
LABELS_COLONNES = {
    # Base
    "HomeTeam": "🏠 Domicile",
    "AwayTeam": "✈️ Extérieur",
    "TimeNY": "⏰ Heure (NY)",
    "DateNY": "📅 Date (NY)",
    "League": "🏆 Ligue",
    "Season": "🗓️ Saison",
    "Team": "⚽ Équipe",
    "Score": "⚡ Score",

    # Classement & forme globale
    "Pos": "#",
    "Pts": "Pts",
    "MP": "J",
    "W": "V", "D": "N", "L": "D",
    "Form5": "📈 Forme",
    "GF_pg": "⚽ BM/m",
    "GA_pg": "🛡️ BE/m",
    "Total_pg": "Total/m",
    "Spark_GF": "📈 BM 10d",
    "Spark_GA": "📉 BE 10d",
    "Spark_Total": "📊 Total 10d",
    "Over05_pct": "O0.5",
    "Over15_pct": "O1.5",
    "Over25_pct": "O2.5",
    "BTTS_pct": "BTTS",
    "Count00": "# 0-0",
    "Pct00": "% 0-0",
    "CS_pct": "% CS",
    "FTS_pct": "% FTS",

    # Séquences
    "Streak_NoScore": "❌🥅 sans marquer",
    "Streak_NoConcede": "🛡️ sans encaisser",
    "Streak_BTTS": "✅ BTTS",
    "Streak_NoBTTS": "❌ BTTS",
    "Streak_Over05": "✅ O0.5",
    "Streak_Over15": "✅ O1.5",
    "Streak_Over25": "✅ O2.5",
    "Streak_Under25": "✅ U2.5",
    "Streak_No00": "❌ 0-0",
    "Streak_Win": "🏆 V",
    "Streak_NoWin": "❌ V",
    "Streak_Loss": "💀 D",
    "L10_Over25_pct": "L10 O2.5",
    "L10_BTTS_pct": "L10 BTTS",

    # Force Poisson
    "HomeAttack": "🏠⚔️ Attaque",
    "HomeDefense": "🏠🛡️ Défense",
    "AwayAttack": "✈️⚔️ Attaque",
    "AwayDefense": "✈️🛡️ Défense",
    "xG_home": "xG 🏠",
    "xG_away": "xG ✈️",

    # Zone DOMICILE (vert)
    "H_Pos": "🏠 #",
    "H_Form": "🏠 Forme",
    "H_Over05": "🏠 O0.5",
    "H_Over15": "🏠 O1.5",
    "H_Over25": "🏠 O2.5",
    "H_BTTS": "🏠 BTTS",
    "H_00_Count": "🏠 # 0-0",
    "H_00_Pct": "🏠 % 0-0",

    # Zone EXTÉRIEUR (bleu)
    "A_Pos": "✈️ #",
    "A_Form": "✈️ Forme",
    "A_Over05": "✈️ O0.5",
    "A_Over15": "✈️ O1.5",
    "A_Over25": "✈️ O2.5",
    "A_BTTS": "✈️ BTTS",
    "A_00_Count": "✈️ # 0-0",
    "A_00_Pct": "✈️ % 0-0",

    # Ligues pour matchup perso
    "H_Ligue": "🏠 Ligue",
    "A_Ligue": "✈️ Ligue",

    # Combiné
    "Combined_00_Pct": "🔗 % 0-0",

    # Zone POISSON (jaune)
    "xG_H": "🎯 xG 🏠",
    "xG_A": "🎯 xG ✈️",
    "P_Over05": "🎯 O0.5",
    "P_Over15": "🎯 O1.5",
    "P_Over25": "🎯 O2.5",
    "P_BTTS": "🎯 BTTS",
    "P_00": "🎯 0-0",

    # Zone H2H (violet)
    "H2H_N": "⚔️ N",
    "H2H_AvgGoals": "⚔️ Buts/m",
    "H2H_BTTS_pct": "⚔️ BTTS",
    "H2H_O25_pct": "⚔️ O2.5",
    "H2H_00_pct": "⚔️ 0-0",

    # Stats additionnelles
    "Shots_pg": "⚽ Tirs/m",
    "ShotsContre_pg": "🛡️ Tirs reçus/m",
    "ShotsTarget_pg": "🎯 T. cadrés/m",
    "ShotsTargetContre_pg": "🛡️ T. cadrés reçus/m",
    "Corners_pg": "🚩 Corners/m",
    "CornersContre_pg": "🛡️ Corners reçus/m",
    "CornersTotal_pg": "🚩 Total corners/m",
    "CornersOver95_pct": "🚩 Over 9.5",
    "CornersOver85_pct": "🚩 Over 8.5",
    "CornersOver105_pct": "🚩 Over 10.5",
    "Yellow_pg": "🟨 Jaunes/m",
    "YellowContre_pg": "🟨 Jaunes adv/m",
    "YellowsTotal_pg": "🟨 Total jaunes/m",
    "YellowsOver35_pct": "🟨 Over 3.5",
    "Red_pg": "🟥 Rouges/m",
    "RedContre_pg": "🟥 Rouges adv/m",
    "Fouls_pg": "⚠️ Fautes/m",
    "FoulsContre_pg": "⚠️ Fautes subies/m",
    # Stats additionnelles — Domicile (H_*)
    "H_Shots_pg": "🏠 Tirs/m",
    "H_ShotsTarget_pg": "🏠 Cadrés/m",
    "H_Corners_pg": "🏠 Corners/m",
    "H_CornersContre_pg": "🏠 Corners reçus/m",
    "H_CornersTotal_pg": "🏠 Total corners/m",
    "H_CornersOver85": "🏠 % O8.5",
    "H_CornersOver95": "🏠 % O9.5",
    "H_CornersOver105": "🏠 % O10.5",
    "H_Yellow_pg": "🏠 🟨/m",
    "H_YellowsTotal_pg": "🏠 Total 🟨/m",
    "H_YellowsOver35": "🏠 % O3.5",
    "H_Red_pg": "🏠 🟥/m",
    "H_Fouls_pg": "🏠 Fautes/m",

    # Stats additionnelles — Extérieur (A_*)
    "A_Shots_pg": "✈️ Tirs/m",
    "A_ShotsTarget_pg": "✈️ Cadrés/m",
    "A_Corners_pg": "✈️ Corners/m",
    "A_CornersContre_pg": "✈️ Corners reçus/m",
    "A_CornersTotal_pg": "✈️ Total corners/m",
    "A_CornersOver85": "✈️ % O8.5",
    "A_CornersOver95": "✈️ % O9.5",
    "A_CornersOver105": "✈️ % O10.5",
    "A_Yellow_pg": "✈️ 🟨/m",
    "A_YellowsTotal_pg": "✈️ Total 🟨/m",
    "A_YellowsOver35": "✈️ % O3.5",
    "A_Red_pg": "✈️ 🟥/m",
    "A_Fouls_pg": "✈️ Fautes/m",
    "H_Signaux": "🏠 🚨",
    "A_Signaux": "✈️ 🚨",
}

def build_column_config(colonnes):
    """Construit la column_config de Streamlit avec les tooltips et des labels lisibles."""
    import streamlit as st
    config = {}
    for col in colonnes:
        label = LABELS_COLONNES.get(col, col)
        help_text = DESCRIPTIONS_COLONNES.get(col)
        # Sparklines : barres horizontales (chaque barre = 1 match)
        if col in ("Spark_GF", "Spark_GA"):
            config[col] = st.column_config.BarChartColumn(
                label, help=help_text, y_min=0, y_max=5,
            )
        elif col == "Spark_Total":
            config[col] = st.column_config.BarChartColumn(
                label, help=help_text, y_min=0, y_max=8,
            )
        else:
            config[col] = st.column_config.Column(label, help=help_text)
    return config
# ============================================================
# CHARGEMENT DES DONNÉES (avec cache)
# ============================================================
@st.cache_data(show_spinner="Calcul des stats en cours... (peut prendre ~1 minute au premier lancement)")
def charger():
    return calculer_tout(
        "data/All_Leagues_2025-26.csv",
        chemin_fixtures="data/fixtures_a_venir.csv"
    )

donnees = charger()
df_brut = donnees["df"]
team_stats = donnees["team_stats"]
matchups = donnees["matchups"]
saison_courante = donnees["saison_courante"]

# Fonctions de pré-calcul mises en cache pour l'onglet Matchups personnalisés
@st.cache_data(show_spinner="Préparation des stats détaillées...")
def precalculer_stats_complet():
    """Re-calcule le dict stats complet (avec _lg_h, _lg_a) une seule fois."""
    from stats import calculer_team_stats
    return calculer_team_stats(df_brut)

@st.cache_data(show_spinner="Préparation de l'index H2H...")
def precalculer_index_h2h():
    """Construit l'index H2H une seule fois."""
    from stats import construire_index_h2h
    return construire_index_h2h(df_brut)

stats_complet = precalculer_stats_complet()
idx_h2h = precalculer_index_h2h()

# ============================================================
# FONCTIONS UTILITAIRES
# ============================================================
def styler_score_a_venir(val):
    """Applique un fond bleu au texte 'À VENIR' dans la colonne Score."""
    if val == "À VENIR":
        return "background-color: #1e3a5f; color: #60a5fa; font-weight: bold; border-radius: 4px;"
    return ""
def appliquer_couleurs(df, cols):
    """Applique les dégradés de couleurs aux colonnes d'un tableau."""
    cols_pct_haut = [c for c in cols if c in [
        "H_Over05", "H_Over15", "H_Over25", "H_BTTS",
        "A_Over05", "A_Over15", "A_Over25", "A_BTTS",
        "P_Over05", "P_Over15", "P_Over25", "P_BTTS",
        "H2H_BTTS_pct", "H2H_O25_pct",
        "Over05_pct", "Over15_pct", "Over25_pct", "BTTS_pct",
        "CS_pct", "L10_Over25_pct", "L10_BTTS_pct",
        "CornersOver85_pct", "CornersOver95_pct", "CornersOver105_pct",
        "YellowsOver35_pct",
    ]]
    cols_pct_bas = [c for c in cols if c in [
        "H_00_Pct", "A_00_Pct", "Combined_00_Pct", "P_00", "H2H_00_pct",
        "Pct00", "FTS_pct",
    ]]
    cols_streak = [c for c in cols if c.startswith("Streak_")]
    cols_xg = [c for c in ["xG_H", "xG_A", "xG_home", "xG_away"] if c in cols]
    cols_rating_haut = [c for c in ["HomeAttack", "AwayAttack"] if c in cols]
    cols_rating_bas = [c for c in ["HomeDefense", "AwayDefense"] if c in cols]

    styled = df[cols].style
    if cols_pct_haut:
        styled = styled.background_gradient(subset=cols_pct_haut, cmap="Greens", vmin=0, vmax=100)
    if cols_pct_bas:
        styled = styled.background_gradient(subset=cols_pct_bas, cmap="Oranges", vmin=0, vmax=30)
    if cols_streak:
        styled = styled.background_gradient(subset=cols_streak, cmap="RdYlGn", vmin=0, vmax=10)
    if cols_xg:
        styled = styled.background_gradient(subset=cols_xg, cmap="Blues", vmin=0, vmax=3)
    if cols_rating_haut:
        styled = styled.background_gradient(subset=cols_rating_haut, cmap="Greens", vmin=0.5, vmax=1.8)
    if cols_rating_bas:
        styled = styled.background_gradient(subset=cols_rating_bas, cmap="Greens_r", vmin=0.5, vmax=1.8)

    # Badge "À VENIR" sur la colonne Score
    if "Score" in cols:
        styled = styled.map(styler_score_a_venir, subset=["Score"])
    # Formater tous les floats avec 1 décimale maximum
    cols_floats = [c for c in cols if df[c].dtype == "float64"]
    if cols_floats:
        styled = styled.format(formatter="{:.1f}", subset=cols_floats, na_rep="—")
        
    return styled

def filtrer_saison(df, saison_selection):
    """Applique le filtre de saison (en cours / toutes / spécifique)."""
    if saison_selection == "En cours (par défaut)":
        return df[df.apply(lambda r: r["Season"] == saison_courante.get(r["League"]), axis=1)]
    elif saison_selection == "Toutes les saisons":
        return df
    else:
        return df[df["Season"] == saison_selection]

# ============================================================
# EN-TÊTE
# ============================================================
st.title("⚽ Deryball")
st.caption("Plateforme de stats et de prédictions Poisson pour le football")
# Toggle mode mobile / compact
col_mode, _ = st.columns([1, 4])
with col_mode:
    mode_mobile_etat = st.session_state.get("toggle_mobile", False)
    label_toggle = "🖥️ Mode bureau" if mode_mobile_etat else "📱 Mode mobile"
    mode_mobile = st.toggle(label_toggle, value=mode_mobile_etat, key="toggle_mobile",
                             help="Simplifie l'affichage pour les écrans étroits")

# ============================================================
# ONGLETS
# ============================================================
tab_matchs, tab_matchups, tab_teams, tab_poisson, tab_sequences, tab_validation = st.tabs([
    "📅 Matchs",
    "🧪 Matchups personnalisés",
    "📊 Stats équipes",
    "🎯 Force Poisson",
    "🔥 Séquences en cours",
    "✅ Validation Poisson",
])

# ============================================================
# INITIALISATION ÉTAT POUR FILTRES RAPIDES (chips)
# ============================================================
if "dates_filtrees" not in st.session_state:
    st.session_state.dates_filtrees = []
if "filtre_rapide" not in st.session_state:
    st.session_state.filtre_rapide = None

# ============================================================
# ONGLET MATCHS
# ============================================================
with tab_matchs:
    # Chips de filtres rapides
    chip0, chip1, chip2, chip3, chip4, chip5, _ = st.columns([1, 1.2, 1, 1.3, 1.5, 0.8, 2.2])
    today = pd.Timestamp.now().normalize()

    with chip0:
        if st.button("⬅️ Hier", key="chip_hier"):
            st.session_state.dates_filtrees = [(today - pd.Timedelta(days=1)).strftime("%Y-%m-%d")]
            st.session_state.filtre_rapide = "yesterday"
    with chip1:
        if st.button("🕐 Aujourd'hui", key="chip_today"):
            st.session_state.dates_filtrees = [today.strftime("%Y-%m-%d")]
            st.session_state.filtre_rapide = "today"
    with chip2:
        if st.button("➡️ Demain", key="chip_tomorrow"):
            st.session_state.dates_filtrees = [(today + pd.Timedelta(days=1)).strftime("%Y-%m-%d")]
            st.session_state.filtre_rapide = "tomorrow"
    with chip3:
        if st.button("🎯 Ce week-end", key="chip_we"):
            jours_avant_sam = (5 - today.dayofweek) % 7
            sam = today + pd.Timedelta(days=jours_avant_sam)
            dim = sam + pd.Timedelta(days=1)
            st.session_state.dates_filtrees = [sam.strftime("%Y-%m-%d"), dim.strftime("%Y-%m-%d")]
            st.session_state.filtre_rapide = "weekend"
    with chip4:
        if st.button("📅 7 prochains jours", key="chip_week"):
            st.session_state.dates_filtrees = [(today + pd.Timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]
            st.session_state.filtre_rapide = "week"
    with chip5:
        if st.button("🔙 Tout", key="chip_reset"):
            st.session_state.dates_filtrees = []
            st.session_state.filtre_rapide = None

    # Filtres principaux (avec sélecteur Type de stats)
    if mode_mobile:
        fcol1 = fcol2 = fcol3 = fcol4 = fcol5 = st.container()
    else:
        fcol1, fcol2, fcol3, fcol4, fcol5 = st.columns([2, 2, 2, 2, 2])

    with fcol1:
        dates_dispo = sorted(matchups["DateNY"].unique(), reverse=True)
        date_selectionnee = st.selectbox("Date (NY)", options=dates_dispo, index=0, key="m_date")

    with fcol2:
        options_saison = ["En cours (par défaut)", "Toutes les saisons"] + sorted(matchups["Season"].unique().tolist())
        saison_selectionnee = st.selectbox("Saison", options=options_saison, index=0, key="m_season")

    with fcol3:
        ligues = ["Toutes les ligues"] + sorted(matchups["League"].unique().tolist())
        ligue_selectionnee = st.selectbox("Ligue", options=ligues, index=0, key="m_league")

    with fcol4:
        recherche = st.text_input("Rechercher équipe", placeholder="ex: Arsenal...", key="m_search")

    with fcol5:
        type_stats_match = st.selectbox(
            "Type de stats",
            options=["Buts (défaut)", "Tirs & corners", "Cartons & fautes"],
            index=0,
            key="m_type_stats"
        )

    # Filtrage
    if st.session_state.dates_filtrees:
        df_aff = matchups[matchups["DateNY"].isin(st.session_state.dates_filtrees)].copy()
    else:
        df_aff = matchups[matchups["DateNY"] == date_selectionnee].copy()
    df_aff = filtrer_saison(df_aff, saison_selectionnee)
    if ligue_selectionnee != "Toutes les ligues":
        df_aff = df_aff[df_aff["League"] == ligue_selectionnee]
    if recherche:
        r_lower = recherche.lower()
        df_aff = df_aff[
            df_aff["HomeTeam"].str.lower().str.contains(r_lower) |
            df_aff["AwayTeam"].str.lower().str.contains(r_lower)
        ]

    # Bandeau résumé
    if st.session_state.dates_filtrees:
        labels = {"yesterday": "Hier", "today": "Aujourd'hui", "tomorrow": "Demain",
                  "weekend": "Ce week-end", "week": "7 prochains jours"}
        label = labels.get(st.session_state.filtre_rapide, "Période sélectionnée")
        dates_cov = sorted(st.session_state.dates_filtrees)
        if len(dates_cov) == 1:
            resume_dates = dates_cov[0]
        elif len(dates_cov) == 2:
            resume_dates = f"{dates_cov[0]} et {dates_cov[1]}"
        else:
            resume_dates = f"du {dates_cov[0]} au {dates_cov[-1]}"
        st.markdown(
            f"#### 📅 {label} — {resume_dates}  \n"
            f"**{len(df_aff)}** match(s) dans cette période"
        )
    else:
        st.markdown(
            f"#### 📅 {date_selectionnee}  \n"
            f"**{len(df_aff)}** match(s) ce jour-là"
        )
# Légende des signaux d'anomalies (uniquement en vue Buts)
    if type_stats_match == "Buts (défaut)":
        if "afficher_legende_matchs" not in st.session_state:
            st.session_state.afficher_legende_matchs = False

        col_legende, _ = st.columns([2, 8])
        with col_legende:
            label = "🚨 Masquer la légende des signaux" if st.session_state.afficher_legende_matchs else "🚨 Afficher la légende des signaux"
            if st.button(label, key="btn_legende_matchs"):
                st.session_state.afficher_legende_matchs = not st.session_state.afficher_legende_matchs
                st.rerun()

        if st.session_state.afficher_legende_matchs:
            st.markdown("""
            Comparaison **forme récente** (5-10 derniers) vs **saison**.

            | Emoji | Signification |
            |---|---|
            | 📈 / 📉 | Attaque en surforme / sousforme |
            | 🛡️ / ⚠️ | Défense en surforme / sousforme |
            | 🔥 / 🧊 | Tendance Over / Under 2.5 |
            | 💥 / 🚫 | Tendance BTTS / Anti-BTTS |

            **+X.X BM** = buts marqués/match en plus que la saison · **+X.X BE** = buts encaissés/match en plus
            """)
    # Sélection des colonnes selon le type de stats
    if type_stats_match == "Tirs & corners":
        colonnes = [
            "TimeNY", "League", "HomeTeam", "AwayTeam", "Score",
            "H_Shots_pg", "H_ShotsTarget_pg",
            "H_Corners_pg", "H_CornersContre_pg",
            "H_CornersTotal_pg", "H_CornersOver85", "H_CornersOver95", "H_CornersOver105",
            "A_Shots_pg", "A_ShotsTarget_pg",
            "A_Corners_pg", "A_CornersContre_pg",
            "A_CornersTotal_pg", "A_CornersOver85", "A_CornersOver95", "A_CornersOver105",
        ]
    elif type_stats_match == "Cartons & fautes":
        colonnes = [
            "TimeNY", "League", "HomeTeam", "AwayTeam", "Score",
            "H_Yellow_pg", "H_YellowsTotal_pg", "H_YellowsOver35",
            "H_Red_pg", "H_Fouls_pg",
            "A_Yellow_pg", "A_YellowsTotal_pg", "A_YellowsOver35",
            "A_Red_pg", "A_Fouls_pg",
        ]
    else:  # Buts (défaut)
        colonnes = [
            "TimeNY", "League", "HomeTeam", "AwayTeam", "Score",
            "H_Signaux", "A_Signaux",
            "xG_H", "xG_A",
            "P_Over05", "P_Over15", "P_Over25", "P_BTTS", "P_00",
            "H_Pos", "H_Form", "H_Over05", "H_Over15", "H_Over25", "H_BTTS", "H_00_Count", "H_00_Pct",
            "A_Pos", "A_Form", "A_Over05", "A_Over15", "A_Over25", "A_BTTS", "A_00_Count", "A_00_Pct",
            "Combined_00_Pct",
            "H2H_N", "H2H_AvgGoals", "H2H_BTTS_pct", "H2H_O25_pct",
        ]

    if mode_mobile:
        colonnes = ["TimeNY", "HomeTeam", "AwayTeam", "Score",
                    "H_Over05", "A_Over05", "H_Over15", "A_Over15",
                    "P_Over05", "P_Over15", "P_00"]
    colonnes = [c for c in colonnes if c in df_aff.columns]
    st.dataframe(
        appliquer_couleurs(df_aff, colonnes),
        use_container_width=True,
        hide_index=True,
        height=600,
        column_config=build_column_config(colonnes),
    )

# ============================================================
# ONGLET STATS ÉQUIPES (revient à l'original simple)
# ============================================================
with tab_teams:
    st.caption("Statistiques cumulées par équipe et par saison.")

    fcol1, fcol2, fcol3, fcol4 = st.columns([2, 2, 2, 2])
    with fcol1:
        options_saison = ["En cours (par défaut)", "Toutes les saisons"] + sorted(team_stats["Season"].unique().tolist())
        saison_t = st.selectbox("Saison", options=options_saison, index=0, key="t_season")
    with fcol2:
        ligues_t = ["Toutes les ligues"] + sorted(team_stats["League"].unique().tolist())
        ligue_t = st.selectbox("Ligue", options=ligues_t, index=0, key="t_league")
    with fcol3:
        recherche_t = st.text_input("Rechercher équipe", placeholder="ex: Arsenal...", key="t_search")
    with fcol4:
        type_t = st.selectbox(
            "Type de stats",
            options=["Buts (défaut)", "Tirs & corners", "Cartons & fautes"],
            index=0,
            key="t_type_stats"
        )

    # Filtrage saison équipes (basé sur DisplayLeague pour respecter les saisons par ligue)
    if saison_t == "En cours (par défaut)":
        df_t = team_stats[team_stats.apply(
            lambda r: r["Season"] == saison_courante.get(r["League"]), axis=1)].copy()
    elif saison_t == "Toutes les saisons":
        df_t = team_stats.copy()
    else:
        df_t = team_stats[team_stats["Season"] == saison_t].copy()
    if ligue_t != "Toutes les ligues":
        df_t = df_t[df_t["League"] == ligue_t]
    if recherche_t:
        df_t = df_t[df_t["Team"].str.lower().str.contains(recherche_t.lower())]

    st.caption(f"**{len(df_t)}** équipe(s)")

    if type_t == "Tirs & corners":
        cols_t = ["Team", "League", "Season", "Pos", "MP",
                  "Shots_pg", "ShotsContre_pg", "ShotsTarget_pg", "ShotsTargetContre_pg",
                  "Corners_pg", "CornersContre_pg", "CornersTotal_pg",
                  "CornersOver85_pct", "CornersOver95_pct", "CornersOver105_pct"]
    elif type_t == "Cartons & fautes":
        cols_t = ["Team", "League", "Season", "Pos", "MP",
                  "Yellow_pg", "YellowContre_pg", "YellowsTotal_pg", "YellowsOver35_pct",
                  "Red_pg", "RedContre_pg", "Fouls_pg", "FoulsContre_pg"]
    else:  # Buts
        cols_t = ["Team", "League", "Season", "Pos", "Pts", "Form5", "MP", "W", "D", "L",
                  "GF_pg", "Spark_GF", "GA_pg", "Spark_GA", "Total_pg", "Spark_Total",
                  "Over05_pct", "Over15_pct", "Over25_pct", "BTTS_pct",
                  "Count00", "Pct00", "CS_pct", "FTS_pct"]

    if mode_mobile:
        if type_t == "Tirs & corners":
            cols_t = ["Team", "League", "Pos", "Shots_pg", "Corners_pg", "CornersOver95_pct"]
        elif type_t == "Cartons & fautes":
            cols_t = ["Team", "League", "Pos", "Yellow_pg", "YellowsOver35_pct", "Red_pg"]
        else:
            cols_t = ["Team", "League", "Pos", "Form5", "Spark_Total", "Over25_pct", "BTTS_pct"]

    cols_t = [c for c in cols_t if c in df_t.columns]
    st.dataframe(
        appliquer_couleurs(df_t, cols_t),
        use_container_width=True,
        hide_index=True,
        height=600,
        column_config=build_column_config(cols_t),
    )

# ============================================================
# ONGLET FORCE POISSON
# ============================================================
with tab_poisson:
    st.caption("Forces d'attaque/défense relatives à la moyenne de la ligue (1.0 = moyenne).")
    fcol1, fcol2 = st.columns([2, 2])
    with fcol1:
        options_saison_p = ["En cours (par défaut)", "Toutes les saisons"] + sorted(team_stats["Season"].unique().tolist())
        saison_p = st.selectbox("Saison", options=options_saison_p, index=0, key="p_season")
    with fcol2:
        ligues_p = ["Toutes les ligues"] + sorted(team_stats["League"].unique().tolist())
        ligue_p = st.selectbox("Ligue", options=ligues_p, index=0, key="p_league")

    if saison_p == "En cours (par défaut)":
        df_p = team_stats[team_stats.apply(
            lambda r: r["Season"] == saison_courante.get(r["League"]), axis=1)].copy()
    elif saison_p == "Toutes les saisons":
        df_p = team_stats.copy()
    else:
        df_p = team_stats[team_stats["Season"] == saison_p].copy()
    if ligue_p != "Toutes les ligues":
        df_p = df_p[df_p["League"] == ligue_p]

    cols_p = ["Team", "League", "Season", "Pos",
              "HomeAttack", "HomeDefense", "AwayAttack", "AwayDefense",
              "xG_home", "xG_away"]
    if mode_mobile:
        cols_p = ["Team", "League", "Pos", "HomeAttack", "AwayAttack", "xG_home"]
    cols_p = [c for c in cols_p if c in df_p.columns]
    st.dataframe(
        appliquer_couleurs(df_p, cols_p),
        use_container_width=True,
        hide_index=True,
        height=600,
        column_config=build_column_config(cols_p),
    )

# ============================================================
# ONGLET SÉQUENCES EN COURS
# ============================================================
with tab_sequences:
    st.caption("Séquences actuelles : nombre de matchs consécutifs avec une caractéristique.")
    fcol1, fcol2 = st.columns([2, 2])
    with fcol1:
        options_saison_s = ["En cours (par défaut)", "Toutes les saisons"] + sorted(team_stats["Season"].unique().tolist())
        saison_s = st.selectbox("Saison", options=options_saison_s, index=0, key="s_season")
    with fcol2:
        ligues_s = ["Toutes les ligues"] + sorted(team_stats["League"].unique().tolist())
        ligue_s = st.selectbox("Ligue", options=ligues_s, index=0, key="s_league")

    if saison_s == "En cours (par défaut)":
        df_s = team_stats[team_stats.apply(
            lambda r: r["Season"] == saison_courante.get(r["League"]), axis=1)].copy()
    elif saison_s == "Toutes les saisons":
        df_s = team_stats.copy()
    else:
        df_s = team_stats[team_stats["Season"] == saison_s].copy()
    if ligue_s != "Toutes les ligues":
        df_s = df_s[df_s["League"] == ligue_s]

    cols_s = ["Team", "League", "Season", "Form5",
              "Streak_NoScore", "Streak_NoConcede", "Streak_BTTS", "Streak_NoBTTS",
              "Streak_Over05", "Streak_Over15", "Streak_Over25", "Streak_Under25",
              "Streak_No00", "Streak_Win", "Streak_NoWin", "Streak_Loss"]
    if mode_mobile:
        cols_s = ["Team", "League", "Form5",
                  "Streak_Over25", "Streak_BTTS", "Streak_No00", "Streak_Win"]
    cols_s = [c for c in cols_s if c in df_s.columns]
    st.dataframe(
        appliquer_couleurs(df_s, cols_s),
        use_container_width=True,
        hide_index=True,
        height=600,
        column_config=build_column_config(cols_s),
    )
    
# ============================================================
# ONGLET 5 — MATCHUPS PERSONNALISÉS
# ============================================================
with tab_matchups:
    st.markdown("### 🧪 Créer vos propres matchups")
    st.caption(
        "Sélectionnez 2 équipes de n'importe quelles ligues pour voir les stats "
        "et probabilités Poisson d'un matchup hypothétique. "
        "⚠️ Ces matchups sont exploratoires — les stats sont basées sur les performances "
        "en ligue de chaque équipe, sans contexte de confrontation réelle."
    )

    # Initialiser la liste de matchups en session state (garde entre les interactions)
    if "matchups_custom" not in st.session_state:
        st.session_state.matchups_custom = []

    # Préparer la structure ligue → équipes
    team_stats = team_stats
    ligues_dispo = sorted(team_stats["League"].dropna().unique().tolist())

    def get_teams_pour_ligue(ligue):
        return sorted(team_stats[team_stats["League"] == ligue]["Team"].unique().tolist())

    # Formulaire d'ajout
    st.markdown("#### ➕ Ajouter un matchup")
    col_h1, col_h2, col_a1, col_a2 = st.columns(4)

    with col_h1:
        ligue_h = st.selectbox("Ligue domicile", ligues_dispo, key="ligue_h_custom")
    with col_h2:
        teams_h = get_teams_pour_ligue(ligue_h)
        team_h = st.selectbox("Équipe domicile", teams_h, key="team_h_custom")

    with col_a1:
        ligue_a = st.selectbox("Ligue extérieur", ligues_dispo, key="ligue_a_custom",
                                index=min(1, len(ligues_dispo)-1))
    with col_a2:
        teams_a = get_teams_pour_ligue(ligue_a)
        team_a = st.selectbox("Équipe extérieur", teams_a, key="team_a_custom")

    col_add, col_vider, _ = st.columns([1, 1, 3])
    with col_add:
        if st.button("➕ Ajouter à ma liste", type="primary"):
            if team_h == team_a and ligue_h == ligue_a:
                st.warning("Une équipe ne peut pas jouer contre elle-même 😄")
            else:
                nouveau = {
                    "HomeTeam": team_h, "HomeLeague": ligue_h,
                    "AwayTeam": team_a, "AwayLeague": ligue_a,
                }
                if nouveau not in st.session_state.matchups_custom:
                    st.session_state.matchups_custom.append(nouveau)
                    st.rerun()
                else:
                    st.info("Ce matchup est déjà dans ta liste")
    with col_vider:
        if st.button("🗑️ Vider tout"):
            st.session_state.matchups_custom = []
            st.rerun()

    # Afficher la liste actuelle
    st.markdown(f"#### 📋 Ma liste ({len(st.session_state.matchups_custom)} matchups)")

    if not st.session_state.matchups_custom:
        st.info("Aucun matchup pour l'instant. Ajoute ton premier ci-dessus !")
    else:
        # Liste compacte avec bouton supprimer par ligne
        for i, m in enumerate(st.session_state.matchups_custom):
            col_txt, col_sup = st.columns([5, 1])
            with col_txt:
                st.markdown(
                    f"**{m['HomeTeam']}** ({m['HomeLeague']}) vs "
                    f"**{m['AwayTeam']}** ({m['AwayLeague']})"
                )
            with col_sup:
                if st.button("🗑️", key=f"sup_{i}"):
                    st.session_state.matchups_custom.pop(i)
                    st.rerun()

        # Construire le tableau de stats pour tous les matchups de la liste
        st.markdown("#### 📊 Stats & Probabilités")

        import pandas as pd

        # Construire un mini-DataFrame avec les matchups demandés
        rows = []
        today = pd.Timestamp.now().normalize()
        for m in st.session_state.matchups_custom:
            # Trouver la saison courante pour chaque équipe
            cles_h = [k for k in stats_complet.keys() if k[0] == m["HomeTeam"] and k[1] == m["HomeLeague"]]
            cles_a = [k for k in stats_complet.keys() if k[0] == m["AwayTeam"] and k[1] == m["AwayLeague"]]
            if not cles_h or not cles_a:
                continue
            # Prendre la saison la plus récente
            saison_h = sorted(cles_h, key=lambda k: k[2])[-1][2]
            saison_a = sorted(cles_a, key=lambda k: k[2])[-1][2]
            rows.append({
                "League": "CUSTOM",
                "DisplayLeague": m["HomeLeague"],  # On utilise celle du domicile
                "HomeTeam": m["HomeTeam"],
                "AwayTeam": m["AwayTeam"],
                "Date": today,
                "DateNY": today.strftime("%Y-%m-%d"),
                "Time": "",
                "TimeNY": "",
                "Season": saison_h,
                "FTHG": 0, "FTAG": 0,
            })

        if rows:
            fx_custom = pd.DataFrame(rows)
            # Pour les matchups inter-ligues, il faut bidouiller un peu :
            # on force la ligue de chaque équipe individuellement dans les stats
            # Le plus simple : on construit le matchup à la main
            matchups_rows = []
            for _, row in fx_custom.iterrows():
                cles_h = [k for k in stats_complet.keys() if k[0] == row["HomeTeam"] and k[1] == m.get("HomeLeague", row["DisplayLeague"])]
                # On récupère les stats de chaque équipe dans SA ligue respective
                m_match = next((mm for mm in st.session_state.matchups_custom
                                if mm["HomeTeam"] == row["HomeTeam"] and mm["AwayTeam"] == row["AwayTeam"]), None)
                if not m_match:
                    continue
                cles_h = [k for k in stats_complet.keys()
                          if k[0] == m_match["HomeTeam"] and k[1] == m_match["HomeLeague"]]
                cles_a = [k for k in stats_complet.keys()
                          if k[0] == m_match["AwayTeam"] and k[1] == m_match["AwayLeague"]]
                if not cles_h or not cles_a:
                    continue
                hk = sorted(cles_h, key=lambda k: k[2])[-1]
                ak = sorted(cles_a, key=lambda k: k[2])[-1]
                h = stats_complet[hk]
                a = stats_complet[ak]

                # Calcul Poisson (même logique que construire_matchups)
                from stats import probs_match, h2h_stats, detecter_anomalies
                lam_h = h["HomeAttack"] * a["AwayDefense"] * h["_lg_h"]
                lam_a = a["AwayAttack"] * h["HomeDefense"] * a["_lg_a"]
                probs = probs_match(lam_h, lam_a)
                h2h = h2h_stats(idx_h2h, m_match["HomeTeam"], m_match["AwayTeam"], today)
                h_emojis, h_details = detecter_anomalies(h)
                a_emojis, a_details = detecter_anomalies(a)

                matchups_rows.append({
                    "HomeTeam": m_match["HomeTeam"],
                    "H_Ligue": m_match["HomeLeague"],
                    "AwayTeam": m_match["AwayTeam"],
                    "A_Ligue": m_match["AwayLeague"],
                    "H_Signaux": h_emojis,
                    "A_Signaux": a_emojis,
                    "H_Pos": h["Pos"], "H_Form": h["Form5"],
                    "H_Over05": h["Over05_pct"], "H_Over15": h["Over15_pct"],
                    "H_Over25": h["Over25_pct"], "H_BTTS": h["BTTS_pct"],
                    "H_00_Count": h["Count00"], "H_00_Pct": h["Pct00"],
                    "A_Pos": a["Pos"], "A_Form": a["Form5"],
                    "A_Over05": a["Over05_pct"], "A_Over15": a["Over15_pct"],
                    "A_Over25": a["Over25_pct"], "A_BTTS": a["BTTS_pct"],
                    "A_00_Count": a["Count00"], "A_00_Pct": a["Pct00"],
                    "Combined_00_Pct": round((h["Pct00"] + a["Pct00"]) / 2, 1),
                    "xG_H": round(lam_h, 2), "xG_A": round(lam_a, 2),
                    "P_Over05": round(100 * probs["over05"], 1),
                    "P_Over15": round(100 * probs["over15"], 1),
                    "P_Over25": round(100 * probs["over25"], 1),
                    "P_BTTS": round(100 * probs["btts"], 1),
                    "P_00": round(100 * probs["p00"], 1),
                    "H2H_N": h2h["H2H_N"],
                    "H2H_AvgGoals": h2h["H2H_AvgGoals"],
                    "H2H_BTTS_pct": h2h["H2H_BTTS_pct"],
                    "H2H_O25_pct": h2h["H2H_O25_pct"],
                    "H2H_00_pct": h2h["H2H_00_pct"],
                })

            if matchups_rows:
                df_display = pd.DataFrame(matchups_rows)
                colonnes_custom = [
                    "HomeTeam", "H_Ligue", "AwayTeam", "A_Ligue",
                    "H_Signaux", "A_Signaux",
                    "xG_H", "xG_A",
                    "P_Over05", "P_Over15", "P_Over25", "P_BTTS", "P_00",
                    "Combined_00_Pct",
                    "H_Pos", "H_Form", "H_Over05", "H_Over15", "H_Over25", "H_BTTS",
                    "H_00_Count", "H_00_Pct",
                    "A_Pos", "A_Form", "A_Over05", "A_Over15", "A_Over25", "A_BTTS",
                    "A_00_Count", "A_00_Pct",
                    "H2H_N", "H2H_AvgGoals", "H2H_BTTS_pct", "H2H_O25_pct",
                ]
                if mode_mobile:
                    colonnes_custom = ["HomeTeam", "AwayTeam",
                                       "H_Over05", "A_Over05", "H_Over15", "A_Over15",
                                       "P_Over05", "P_Over15", "P_00"]
                # Légende des signaux
                if "afficher_legende_matchups" not in st.session_state:
                    st.session_state.afficher_legende_matchups = False

                col_leg, _ = st.columns([2, 8])
                with col_leg:
                    label = "🚨 Masquer légende" if st.session_state.afficher_legende_matchups else "🚨 Afficher légende"
                    if st.button(label, key="btn_legende_matchups"):
                        st.session_state.afficher_legende_matchups = not st.session_state.afficher_legende_matchups
                        st.rerun()

                if st.session_state.afficher_legende_matchups:
                    st.markdown("""
                    | Emoji | Signification |
                    |---|---|
                    | 📈 / 📉 | Attaque en surforme / sousforme |
                    | 🛡️ / ⚠️ | Défense en surforme / sousforme |
                    | 🔥 / 🧊 | Tendance Over / Under 2.5 |
                    | 💥 / 🚫 | Tendance BTTS / Anti-BTTS |

                    Format : **+X.X BM/BE** = différence buts marqués/encaissés vs saison.
                    """)
                colonnes_custom = [c for c in colonnes_custom if c in df_display.columns]
                st.dataframe(
                    appliquer_couleurs(df_display, colonnes_custom),
                    use_container_width=True,
                    hide_index=True,
                    height=400,
                    column_config=build_column_config(colonnes_custom),
                )
            else:
                st.warning("Aucun matchup valide. Vérifie que les équipes ont des stats disponibles.")
                # ============================================================
# ONGLET VALIDATION POISSON
# ============================================================
with tab_validation:
    from stats import (
        calculer_validation_poisson, metriques_calibration,
        calibration_par_buckets, plus_grandes_surprises,
    )

    st.markdown("### ✅ Validation du modèle Poisson")
    st.caption(
        "Compare les probabilités Poisson prédites aux résultats réels des matchs joués. "
        "Permet de voir où le modèle se trompe et de quel côté."
    )

    with st.expander("ℹ️ À lire avant d'interpréter ces chiffres"):
        st.markdown("""
        **Biais important :** les stats utilisées par Poisson (HomeAttack, AwayDefense…)
        sont calculées sur **toute la saison**, incluant les matchs qu'on cherche à prédire.
        Les métriques ci-dessous sont donc **optimistes** par rapport à une vraie performance
        prédictive.

        **Ce que ces chiffres permettent quand même de voir :**
        - 📊 **Calibration** : est-ce que les tranches "60-70% prédit" donnent ~65% de réussite ?
        - ⚖️ **Biais systématiques** : le modèle sur-prédit-il les Over 2.5 ?
        - 🏆 **Comparaison entre marchés** : Poisson est-il meilleur sur BTTS ou sur 0-0 ?

        Une vraie validation **walk-forward** (recalculer les stats à chaque date du calendrier)
        est prévue dans une prochaine itération.

        ---

        ### 🎯 Le Brier score, c'est quoi ?

        C'est une mesure de qualité d'une prédiction probabiliste. Pour chaque match,
        on calcule l'écart au carré entre la proba prédite (ex. 0.65) et le résultat
        réel (1 si l'évènement est arrivé, 0 sinon). Puis on moyenne sur tous les matchs.

        - **0.000** = parfait (impossible en pratique)
        - **0.250** = équivalent à pile-ou-face
        - Plus c'est **bas**, mieux c'est.
        - Bon pour comparer **deux modèles** sur le même jeu de matchs (ex. DC vs Poisson pur).

        ### 🔬 Dixon-Coles (DC), c'est quoi ?

        Le Poisson "pur" suppose que les buts à domicile et à l'extérieur sont
        **indépendants**. En réalité, en foot, on observe que les scores faibles
        (**0-0**, **1-1**) arrivent un peu plus souvent que prédit, et **1-0 / 0-1**
        un peu moins. La correction Dixon-Coles ajoute un paramètre **ρ (rho)** qui
        ajuste les probas des 4 cases basses (0-0, 0-1, 1-0, 1-1) pour coller à cette
        réalité empirique. Ici on utilise **ρ = -0.10**, valeur standard en littérature foot.

        ⚠️ **Conséquence importante** : DC ne touche que les 4 cases basses, donc
        **Over 2.5 est identique** entre DC et Poisson pur (les cases concernées
        ont toutes un total < 3). Seuls **BTTS, 0-0, Over 0.5 et Over 1.5** changent
        — et de quelques points seulement.
        """)

    # Filtres
    fcol1, fcol2 = st.columns([2, 2])
    with fcol1:
        options_saison_v = ["En cours (par défaut)", "Toutes les saisons"] + sorted(matchups["Season"].unique().tolist())
        saison_v = st.selectbox("Saison", options=options_saison_v, index=0, key="v_season")
    with fcol2:
        ligues_v = ["Toutes les ligues"] + sorted(matchups["League"].unique().tolist())
        ligue_v = st.selectbox("Ligue", options=ligues_v, index=0, key="v_league")

    # Filtrage
    df_v = matchups.copy()
    if "IsUpcoming" in df_v.columns:
        df_v = df_v[df_v["IsUpcoming"] != True]
    if saison_v == "En cours (par défaut)":
        df_v = df_v[df_v.apply(lambda r: r["Season"] == saison_courante.get(r["League"]), axis=1)]
    elif saison_v != "Toutes les saisons":
        df_v = df_v[df_v["Season"] == saison_v]
    if ligue_v != "Toutes les ligues":
        df_v = df_v[df_v["League"] == ligue_v]

    df_validation = calculer_validation_poisson(df_v)

    if len(df_validation) == 0:
        st.warning("Aucun match joué dans cette sélection.")
    else:
        st.markdown(f"#### 📊 {len(df_validation)} matchs analysés")

        # Métriques par marché avec couleurs
        metriques = metriques_calibration(df_validation)
        styled_metriques = (
            metriques.style
            .background_gradient(subset=["Brier"], cmap="RdYlGn_r", vmin=0, vmax=0.30)
            .background_gradient(subset=["Accuracy"], cmap="Greens", vmin=50, vmax=85)
            .background_gradient(subset=["Écart (pp)"], cmap="RdBu", vmin=-15, vmax=15)
            .format({"Brier": "{:.4f}", "Accuracy": "{:.1f}",
                     "% prédit moy": "{:.1f}", "% réel": "{:.1f}", "Écart (pp)": "{:+.1f}"})
        )
        st.dataframe(styled_metriques, use_container_width=True, hide_index=True)
        st.caption(
            "💡 **Brier score** : plus c'est bas, mieux c'est (0 = parfait, 0.25 = pile/face). "
            "**Écart** : positif = modèle sur-prédit, négatif = sous-prédit."
        )

        # Calibration par tranche
        # ============================================================
        # COMPARAISON DIXON-COLES vs POISSON PUR
        # ============================================================
        st.markdown("---")
        st.markdown("#### 🔬 Comparaison Dixon-Coles vs Poisson pur")
        comparer_dc = st.toggle(
            "Afficher la comparaison côte à côte",
            value=False,
            key="v_compare_dc",
            help="Recalcule les probas en mode Poisson pur (ρ=0) pour comparer avec DC (ρ=-0.10).",
        )

        if comparer_dc:
            from stats import recalculer_probs_avec_rho

            with st.spinner("Recalcul en mode Poisson pur (ρ=0)..."):
                df_v_pur = recalculer_probs_avec_rho(df_v, rho=0.0)
                df_validation_pur = calculer_validation_poisson(df_v_pur)
                metriques_pur = metriques_calibration(df_validation_pur)

            col_dc, col_pur = st.columns(2)
            with col_dc:
                st.markdown("##### ✅ Dixon-Coles (ρ=-0.10)")
                styled_dc = (
                    metriques.style
                    .background_gradient(subset=["Brier"], cmap="RdYlGn_r", vmin=0, vmax=0.30)
                    .background_gradient(subset=["Écart (pp)"], cmap="RdBu", vmin=-15, vmax=15)
                    .format({"Brier": "{:.4f}", "Accuracy": "{:.1f}",
                             "% prédit moy": "{:.1f}", "% réel": "{:.1f}",
                             "Écart (pp)": "{:+.1f}"})
                )
                st.dataframe(styled_dc, use_container_width=True, hide_index=True)
            with col_pur:
                st.markdown("##### ➖ Poisson pur (ρ=0)")
                styled_pur = (
                    metriques_pur.style
                    .background_gradient(subset=["Brier"], cmap="RdYlGn_r", vmin=0, vmax=0.30)
                    .background_gradient(subset=["Écart (pp)"], cmap="RdBu", vmin=-15, vmax=15)
                    .format({"Brier": "{:.4f}", "Accuracy": "{:.1f}",
                             "% prédit moy": "{:.1f}", "% réel": "{:.1f}",
                             "Écart (pp)": "{:+.1f}"})
                )
                st.dataframe(styled_pur, use_container_width=True, hide_index=True)
            st.caption(
                "💡 Compare les Brier scores et les écarts. Brier plus bas = meilleur. "
                "DC devrait améliorer BTTS et 1-1, mais peut légèrement empirer 0-0."
            )
        st.markdown("---")
        st.markdown("#### 🎯 Calibration par tranche de probabilité")

        marches_dict = {
            "Over 2.5": ("P_Over25", "Real_Over25"),
            "BTTS":     ("P_BTTS",   "Real_BTTS"),
            "Over 1.5": ("P_Over15", "Real_Over15"),
            "Over 0.5": ("P_Over05", "Real_Over05"),
            "0-0":      ("P_00",     "Real_00"),
        }
        marche_sel = st.selectbox("Marché à analyser", options=list(marches_dict.keys()), key="v_marche")
        col_pred, col_real = marches_dict[marche_sel]

        buckets = calibration_par_buckets(df_validation, col_pred, col_real)
        if len(buckets) > 0:
            styled_buckets = (
                buckets.style
                .background_gradient(subset=["Écart (pp)"], cmap="RdBu", vmin=-25, vmax=25)
                .format({"% prédit moy": "{:.1f}", "% réel": "{:.1f}", "Écart (pp)": "{:+.1f}"})
            )
            st.dataframe(styled_buckets, use_container_width=True, hide_index=True)
            st.caption(
                "💡 Si le modèle est bien calibré, **% prédit moy** ≈ **% réel** dans chaque tranche. "
                "L'écart est en points de pourcentage (pp)."
            )
        else:
            st.info("Pas assez de données pour bucketer ce marché.")

        # Top surprises
        st.markdown("---")
        st.markdown(f"#### 😱 Top 10 — où le modèle s'est le plus trompé ({marche_sel})")
        surprises = plus_grandes_surprises(df_validation, col_pred, col_real, n=10)
        st.dataframe(surprises, use_container_width=True, hide_index=True)
        st.caption(
            "Écart positif = modèle prédisait haut mais c'est arrivé en bas (ou inversement). "
            "0/1 dans la colonne Réel = est-ce que l'évènement s'est produit."
        )