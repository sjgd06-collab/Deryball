"""
Deryball — Application Streamlit principale.
"""
import streamlit as st
import pandas as pd
from stats import calculer_tout, stats_forme_match
from cards import CARDS_CSS, rendre_cartes_matchs, rendre_tableau_forme

st.set_page_config(page_title="Deryball", page_icon="⚽", layout="wide")
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
.stSelectbox > div > div {
    min-height: 42px !important;
    padding: 4px 12px !important;
    display: flex !important;
    align-items: center !important;
}
.stSelectbox div[data-baseweb="select"] > div { min-height: 36px !important; }
.stSelectbox div[data-baseweb="select"] > div > div {
    line-height: 1.5 !important;
    overflow: visible !important;
    white-space: nowrap !important;
    padding: 4px 0 !important;
}
.stTextInput > div > div > input {
    padding: 10px 14px !important;
    min-height: 42px !important;
}
.stSelectbox > div > div:hover,
.stTextInput > div > div > input:hover {
    border-color: var(--accent-soft) !important;
    background-color: var(--bg-hover) !important;
}
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
.stCheckbox [role="switch"],
[data-baseweb="checkbox"] [role="checkbox"],
[data-baseweb="switch"] > div {
    background-color: var(--bg-elevated) !important;
    border: 1px solid var(--border-default) !important;
    transition: all 0.2s ease !important;
}
.stCheckbox [role="switch"][aria-checked="true"],
[data-baseweb="checkbox"][aria-checked="true"] [role="checkbox"],
[data-baseweb="switch"][aria-checked="true"] > div {
    background-color: var(--accent) !important;
    border-color: var(--accent-soft) !important;
    box-shadow: 0 0 0 4px rgba(130,102,255,0.20) !important;
}
.stCheckbox [role="switch"] > div,
[data-baseweb="checkbox"] [role="checkbox"] > div {
    background-color: var(--text-muted) !important;
    transition: all 0.2s ease !important;
}
.stCheckbox [role="switch"][aria-checked="true"] > div,
[data-baseweb="checkbox"][aria-checked="true"] [role="checkbox"] > div {
    background-color: white !important;
}
.stCheckbox div[data-testid="stCheckbox"] label > div:first-child[style*="background"] {
    background-color: var(--accent) !important;
}

/* ======================================================
   RADIO (utilisé pour le toggle Vue Tableau/Détaillée)
   ====================================================== */
.stRadio > div[role="radiogroup"] {
    gap: 6px !important;
}
.stRadio label {
    background: var(--bg-elevated) !important;
    border: 1px solid var(--border-default) !important;
    border-radius: 8px !important;
    padding: 8px 14px !important;
    cursor: pointer !important;
    transition: all 0.15s ease !important;
}
.stRadio label:hover {
    border-color: var(--accent-soft) !important;
    background: var(--accent-glow) !important;
}
.stRadio label[data-checked="true"],
.stRadio label:has(input:checked) {
    background: rgba(130,102,255,0.30) !important;
    border-color: var(--accent) !important;
    color: var(--text-strong) !important;
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
   TABLEAUX (DATAFRAME)
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
[data-testid="stExpander"] summary::before,
[data-testid="stExpander"] summary::-webkit-details-marker {
    display: none !important;
}
[data-testid="stExpander"] summary svg {
    fill: var(--text-muted) !important;
    transition: transform 0.2s ease !important;
}
[data-testid="stExpander"] details[open] summary svg {
    transform: rotate(90deg);
}
[data-testid="stExpander"] [data-testid="stExpanderDetails"] {
    padding: 0 14px 14px 14px !important;
    color: var(--text-default) !important;
}
[data-testid="stExpander"] summary span:not([data-testid]) {
    font-size: 0 !important;
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

# CSS spécifique aux cartes (vue détaillée)
st.markdown(CARDS_CSS, unsafe_allow_html=True)

# ============================================================
# DESCRIPTIONS DES COLONNES (tooltips au survol de l'entête)
# ============================================================
DESCRIPTIONS_COLONNES = {
    "Team": "Nom de l'équipe",
    "League": "Ligue / championnat",
    "Season": "Saison concernée",
    "Date": "Date du match",
    "DateNY": "Date du match en heure de New York",
    "TimeNY": "Heure de début du match (heure de New York)",
    "HomeTeam": "Équipe à domicile",
    "AwayTeam": "Équipe à l'extérieur",
    "Score": "Score final du match (ou 'À VENIR' si pas encore joué)",
    "Pos": "Position actuelle au classement",
    "Pts": "Points accumulés cette saison",
    "Form5": "Forme sur les 5 derniers matchs (V=victoire, N=nul, D=défaite)",
    "MP": "Nombre de matchs joués",
    "W": "Victoires", "D": "Matchs nuls", "L": "Défaites",
    "GF_pg": "Buts marqués par match (moyenne)",
    "GA_pg": "Buts encaissés par match (moyenne)",
    "Total_pg": "Total de buts par match (moyenne)",
    "Spark_GF": "Buts marqués sur les 10 derniers matchs (ancien à gauche, récent à droite)",
    "Spark_GA": "Buts encaissés sur les 10 derniers matchs (ancien à gauche, récent à droite)",
    "Spark_Total": "Total de buts par match sur les 10 derniers — utile pour la tendance Over/Under",
    "Over05_pct": "% des matchs avec au moins 1 but",
    "Over15_pct": "% des matchs avec au moins 2 buts",
    "Over25_pct": "% des matchs avec au moins 3 buts (plus de 2.5)",
    "BTTS_pct": "% des matchs où les 2 équipes ont marqué",
    "Count00": "Nombre de matchs terminés 0-0",
    "Pct00": "% des matchs terminés 0-0",
    "CS_pct": "% de matchs où l'équipe n'a pas encaissé (clean sheet)",
    "FTS_pct": "% de matchs où l'équipe n'a pas marqué",
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
    "HomeAttack": "Force offensive à domicile (1.00 = moyenne de la ligue)",
    "HomeDefense": "Force défensive à domicile (1.00 = moyenne, <1 = bon)",
    "AwayAttack": "Force offensive à l'extérieur (1.00 = moyenne)",
    "AwayDefense": "Force défensive à l'extérieur (1.00 = moyenne, <1 = bon)",
    "xG_home": "Buts attendus à domicile (Poisson)",
    "xG_away": "Buts attendus à l'extérieur (Poisson)",
    "H_Pos": "Classement actuel de l'équipe à domicile",
    "H_Form": "Forme sur les 5 derniers matchs (domicile)",
    "H_Over05": "% Over 0.5 de l'équipe à domicile",
    "H_Over15": "% Over 1.5 de l'équipe à domicile",
    "H_Over25": "% Over 2.5 de l'équipe à domicile",
    "H_BTTS": "% BTTS de l'équipe à domicile",
    "H_00_Count": "Nombre de 0-0 de l'équipe à domicile",
    "H_00_Pct": "% de 0-0 de l'équipe à domicile",
    "A_Pos": "Classement actuel de l'équipe à l'extérieur",
    "A_Form": "Forme sur les 5 derniers matchs (extérieur)",
    "A_Over05": "% Over 0.5 de l'équipe à l'extérieur",
    "A_Over15": "% Over 1.5 de l'équipe à l'extérieur",
    "A_Over25": "% Over 2.5 de l'équipe à l'extérieur",
    "A_BTTS": "% BTTS de l'équipe à l'extérieur",
    "A_00_Count": "Nombre de 0-0 de l'équipe à l'extérieur",
    "A_00_Pct": "% de 0-0 de l'équipe à l'extérieur",
    "H_Ligue": "Ligue de l'équipe à domicile",
    "A_Ligue": "Ligue de l'équipe à l'extérieur",
    "Combined_00_Pct": "Moyenne des % de 0-0 des 2 équipes",
    "xG_H": "Buts attendus de l'équipe domicile (modèle Poisson)",
    "xG_A": "Buts attendus de l'équipe extérieur (modèle Poisson)",
    "P_Over05": "Probabilité Poisson qu'il y ait au moins 1 but",
    "P_Over15": "Probabilité Poisson qu'il y ait au moins 2 buts",
    "P_Over25": "Probabilité Poisson qu'il y ait plus de 2.5 buts",
    "P_BTTS": "Probabilité Poisson que les 2 équipes marquent",
    "P_00": "Probabilité Poisson que le match finisse 0-0",
    "H2H_N": "Nombre de confrontations passées entre ces 2 équipes",
    "H2H_AvgGoals": "Moyenne de buts par match dans les confrontations passées",
    "H2H_BTTS_pct": "% BTTS dans les confrontations passées",
    "H2H_O25_pct": "% Over 2.5 dans les confrontations passées",
    "H2H_00_pct": "% de 0-0 dans les confrontations passées",
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
}
# ============================================================
# LABELS COURTS ET LISIBLES POUR LES COLONNES
# ============================================================
LABELS_COLONNES = {
    "HomeTeam": "🏠 Domicile",
    "AwayTeam": "✈️ Extérieur",
    "TimeNY": "⏰ Heure (NY)",
    "DateNY": "📅 Date (NY)",
    "League": "🏆 Ligue",
    "Season": "🗓️ Saison",
    "Team": "⚽ Équipe",
    "Score": "⚡ Score",
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
    "Over05_pct": "O0.5", "Over15_pct": "O1.5", "Over25_pct": "O2.5",
    "BTTS_pct": "BTTS", "Count00": "# 0-0", "Pct00": "% 0-0",
    "CS_pct": "% CS", "FTS_pct": "% FTS",
    "Streak_NoScore": "❌🥅 sans marquer",
    "Streak_NoConcede": "🛡️ sans encaisser",
    "Streak_BTTS": "✅ BTTS", "Streak_NoBTTS": "❌ BTTS",
    "Streak_Over05": "✅ O0.5", "Streak_Over15": "✅ O1.5",
    "Streak_Over25": "✅ O2.5", "Streak_Under25": "✅ U2.5",
    "Streak_No00": "❌ 0-0",
    "Streak_Win": "🏆 V", "Streak_NoWin": "❌ V", "Streak_Loss": "💀 D",
    "L10_Over25_pct": "L10 O2.5", "L10_BTTS_pct": "L10 BTTS",
    "HomeAttack": "🏠⚔️ Attaque", "HomeDefense": "🏠🛡️ Défense",
    "AwayAttack": "✈️⚔️ Attaque", "AwayDefense": "✈️🛡️ Défense",
    "xG_home": "xG 🏠", "xG_away": "xG ✈️",
    "H_Pos": "🏠 #", "H_Form": "🏠 Forme",
    "H_Over05": "🏠 O0.5", "H_Over15": "🏠 O1.5",
    "H_Over25": "🏠 O2.5", "H_BTTS": "🏠 BTTS",
    "H_00_Count": "🏠 # 0-0", "H_00_Pct": "🏠 % 0-0",
    "A_Pos": "✈️ #", "A_Form": "✈️ Forme",
    "A_Over05": "✈️ O0.5", "A_Over15": "✈️ O1.5",
    "A_Over25": "✈️ O2.5", "A_BTTS": "✈️ BTTS",
    "A_00_Count": "✈️ # 0-0", "A_00_Pct": "✈️ % 0-0",
    "H_Ligue": "🏠 Ligue", "A_Ligue": "✈️ Ligue",
    "Combined_00_Pct": "🔗 % 0-0",
    "xG_H": "🎯 xG 🏠", "xG_A": "🎯 xG ✈️",
    "P_Over05": "🎯 O0.5", "P_Over15": "🎯 O1.5",
    "P_Over25": "🎯 O2.5", "P_BTTS": "🎯 BTTS", "P_00": "🎯 0-0",
    "H2H_N": "⚔️ N", "H2H_AvgGoals": "⚔️ Buts/m",
    "H2H_BTTS_pct": "⚔️ BTTS", "H2H_O25_pct": "⚔️ O2.5",
    "H2H_00_pct": "⚔️ 0-0",
    "Shots_pg": "⚽ Tirs/m", "ShotsContre_pg": "🛡️ Tirs reçus/m",
    "ShotsTarget_pg": "🎯 T. cadrés/m",
    "ShotsTargetContre_pg": "🛡️ T. cadrés reçus/m",
    "Corners_pg": "🚩 Corners/m", "CornersContre_pg": "🛡️ Corners reçus/m",
    "CornersTotal_pg": "🚩 Total corners/m",
    "CornersOver95_pct": "🚩 Over 9.5",
    "CornersOver85_pct": "🚩 Over 8.5",
    "CornersOver105_pct": "🚩 Over 10.5",
    "Yellow_pg": "🟨 Jaunes/m", "YellowContre_pg": "🟨 Jaunes adv/m",
    "YellowsTotal_pg": "🟨 Total jaunes/m",
    "YellowsOver35_pct": "🟨 Over 3.5",
    "Red_pg": "🟥 Rouges/m", "RedContre_pg": "🟥 Rouges adv/m",
    "Fouls_pg": "⚠️ Fautes/m", "FoulsContre_pg": "⚠️ Fautes subies/m",
    "H_Shots_pg": "🏠 Tirs/m", "H_ShotsTarget_pg": "🏠 Cadrés/m",
    "H_Corners_pg": "🏠 Corners/m",
    "H_CornersContre_pg": "🏠 Corners reçus/m",
    "H_CornersTotal_pg": "🏠 Total corners/m",
    "H_CornersOver85": "🏠 % O8.5", "H_CornersOver95": "🏠 % O9.5",
    "H_CornersOver105": "🏠 % O10.5",
    "H_Yellow_pg": "🏠 🟨/m", "H_YellowsTotal_pg": "🏠 Total 🟨/m",
    "H_YellowsOver35": "🏠 % O3.5",
    "H_Red_pg": "🏠 🟥/m", "H_Fouls_pg": "🏠 Fautes/m",
    "A_Shots_pg": "✈️ Tirs/m", "A_ShotsTarget_pg": "✈️ Cadrés/m",
    "A_Corners_pg": "✈️ Corners/m",
    "A_CornersContre_pg": "✈️ Corners reçus/m",
    "A_CornersTotal_pg": "✈️ Total corners/m",
    "A_CornersOver85": "✈️ % O8.5", "A_CornersOver95": "✈️ % O9.5",
    "A_CornersOver105": "✈️ % O10.5",
    "A_Yellow_pg": "✈️ 🟨/m", "A_YellowsTotal_pg": "✈️ Total 🟨/m",
    "A_YellowsOver35": "✈️ % O3.5",
    "A_Red_pg": "✈️ 🟥/m", "A_Fouls_pg": "✈️ Fautes/m",
    "H_Signaux": "🏠 🚨", "A_Signaux": "✈️ 🚨",
}

def build_column_config(colonnes):
    """Construit la column_config de Streamlit avec les tooltips et des labels lisibles."""
    config = {}
    for col in colonnes:
        label = LABELS_COLONNES.get(col, col)
        help_text = DESCRIPTIONS_COLONNES.get(col)
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
tr_journal = donnees["tr"]

@st.cache_data(show_spinner="Préparation des stats détaillées...")
def precalculer_stats_complet():
    from stats import calculer_team_stats
    return calculer_team_stats(df_brut)

@st.cache_data(show_spinner="Préparation de l'index H2H...")
def precalculer_index_h2h():
    from stats import construire_index_h2h
    return construire_index_h2h(df_brut)

stats_complet = precalculer_stats_complet()
idx_h2h = precalculer_index_h2h()

# ============================================================
# FONCTIONS UTILITAIRES
# ============================================================
def styler_score_a_venir(val):
    if val == "À VENIR":
        return "background-color: #1e3a5f; color: #60a5fa; font-weight: bold; border-radius: 4px;"
    return ""

def appliquer_couleurs(df, cols):
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

    if "Score" in cols:
        styled = styled.map(styler_score_a_venir, subset=["Score"])
    cols_floats = [c for c in cols if df[c].dtype == "float64"]
    if cols_floats:
        styled = styled.format(formatter="{:.1f}", subset=cols_floats, na_rep="—")
    return styled

def filtrer_saison(df, saison_selection):
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
tab_matchs, tab_matchups = st.tabs([
    "📅 Matchs",
    "🧪 Matchups personnalisés",
])

# Init état pour filtres rapides
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

    # Filtres principaux
    if mode_mobile:
        fcol1 = fcol2 = fcol3 = fcol4 = st.container()
    else:
        fcol1, fcol2, fcol3, fcol4 = st.columns([2, 2, 2, 2])

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
    type_stats_match = "Buts (défaut)"

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

    # ============================================================
    # 🆕 TOGGLE VUE : TABLEAU vs DÉTAILLÉE
    # ============================================================
    col_vue, _ = st.columns([2, 6])
    with col_vue:
        vue_match = st.radio(
            "Mode d'affichage",
            options=["📊 Tableau", "🎴 Détaillée"],
            index=0,
            key="vue_match",
            horizontal=True,
            label_visibility="collapsed",
        )

    # 2b : sélecteurs fenêtre + périmètre pour la vue Tableau
    if vue_match != "🎴 Détaillée":
        colf1, colf2, _ = st.columns([2, 2, 4])
        fenetre_forme = colf1.selectbox("Fenêtre", ["5 derniers", "10 derniers", "Saison"], index=1, key="fenetre_forme")
        perimetre_forme = colf2.selectbox("Périmètre", ["Combiné", "Domicile", "Extérieur"], index=0, key="perimetre_forme")
    else:
        fenetre_forme, perimetre_forme = "10 derniers", "Combiné"


    # ============================================================
    # 🆕 AFFICHAGE CONDITIONNEL : TABLEAU OU CARTES
    # ============================================================
    if vue_match == "🎴 Détaillée":
        # ----- VUE DÉTAILLÉE (cartes) -----
        # Note : la vue détaillée est conçue pour l'analyse des buts (Poisson, BTTS, H2H).
        # Pour les autres types de stats, on garde le tableau (les cartes ne les affichent pas).
        if type_stats_match != "Buts (défaut)":
            st.info(
                "💡 La vue détaillée affiche les stats Poisson et buts. "
                "Pour les stats Tirs/Corners ou Cartons/Fautes, utilise la vue Tableau."
            )
            # On bascule vers le tableau quand même pour ne pas laisser l'écran vide
            colonnes = (
                [
                    "TimeNY", "League", "HomeTeam", "AwayTeam", "Score",
                    "H_Shots_pg", "H_ShotsTarget_pg",
                    "H_Corners_pg", "H_CornersContre_pg",
                    "H_CornersTotal_pg", "H_CornersOver85", "H_CornersOver95", "H_CornersOver105",
                    "A_Shots_pg", "A_ShotsTarget_pg",
                    "A_Corners_pg", "A_CornersContre_pg",
                    "A_CornersTotal_pg", "A_CornersOver85", "A_CornersOver95", "A_CornersOver105",
                ] if type_stats_match == "Tirs & corners"
                else [
                    "TimeNY", "League", "HomeTeam", "AwayTeam", "Score",
                    "H_Yellow_pg", "H_YellowsTotal_pg", "H_YellowsOver35",
                    "H_Red_pg", "H_Fouls_pg",
                    "A_Yellow_pg", "A_YellowsTotal_pg", "A_YellowsOver35",
                    "A_Red_pg", "A_Fouls_pg",
                ]
            )
            colonnes = [c for c in colonnes if c in df_aff.columns]
            st.dataframe(
                appliquer_couleurs(df_aff, colonnes),
                use_container_width=True, hide_index=True, height=600,
                column_config=build_column_config(colonnes),
            )
        else:
            # Tri par heure pour avoir un ordre logique dans les cartes
            df_cartes = df_aff.copy()
            if "TimeNY" in df_cartes.columns:
                df_cartes = df_cartes.sort_values(["DateNY", "TimeNY"])
            if len(df_cartes) > 0:
                df_cartes["FormeStats"] = [
                    stats_forme_match(tr_journal, r["HomeTeam"], r["AwayTeam"],
                                      r["League"], saison_courante.get(r["League"]))
                    for _, r in df_cartes.iterrows()
                ]
            rendre_cartes_matchs(df_cartes, st)
    else:
        # ----- VUE TABLEAU (originale) -----
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
        if type_stats_match == "Buts (défaut)":
            _fmap = {"5 derniers": "5", "10 derniers": "10", "Saison": "saison"}
            _pmap = {"Combiné": "combine", "Domicile": "domicile", "Extérieur": "exterieur"}
            _dff = df_aff.copy()
            _dff["FormeStats"] = [
                stats_forme_match(tr_journal, r["HomeTeam"], r["AwayTeam"],
                                  r["League"], saison_courante.get(r["League"]))
                for _, r in _dff.iterrows()
            ]
            st.markdown(
                rendre_tableau_forme(_dff, _fmap[fenetre_forme], _pmap[perimetre_forme]),
                unsafe_allow_html=True,
            )
        else:
            st.dataframe(
                appliquer_couleurs(df_aff, colonnes),
                use_container_width=True, hide_index=True, height=600,
                column_config=build_column_config(colonnes),
            )
with tab_matchups:
    st.markdown("### 🧪 Créer vos propres matchups")
    st.caption(
        "Sélectionnez 2 équipes de n'importe quelles ligues pour voir les stats "
        "et probabilités Poisson d'un matchup hypothétique. "
        "⚠️ Ces matchups sont exploratoires — les stats sont basées sur les performances "
        "en ligue de chaque équipe, sans contexte de confrontation réelle."
    )

    if "matchups_custom" not in st.session_state:
        st.session_state.matchups_custom = []

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

    st.markdown(f"#### 📋 Ma liste ({len(st.session_state.matchups_custom)} matchups)")

    if not st.session_state.matchups_custom:
        st.info("Aucun matchup pour l'instant. Ajoute ton premier ci-dessus !")
    else:
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

        st.markdown("#### 📊 Stats & Probabilités")

        # Construire le DataFrame de matchups
        rows = []
        today = pd.Timestamp.now().normalize()
        for m in st.session_state.matchups_custom:
            cles_h = [k for k in stats_complet.keys() if k[0] == m["HomeTeam"] and k[1] == m["HomeLeague"]]
            cles_a = [k for k in stats_complet.keys() if k[0] == m["AwayTeam"] and k[1] == m["AwayLeague"]]
            if not cles_h or not cles_a:
                continue
            saison_h = sorted(cles_h, key=lambda k: k[2])[-1][2]
            rows.append({
                "League": "CUSTOM",
                "DisplayLeague": m["HomeLeague"],
                "HomeTeam": m["HomeTeam"],
                "AwayTeam": m["AwayTeam"],
                "Date": today,
                "DateNY": today.strftime("%Y-%m-%d"),
                "Time": "", "TimeNY": "",
                "Season": saison_h,
                "FTHG": 0, "FTAG": 0,
            })

        if rows:
            fx_custom = pd.DataFrame(rows)
            matchups_rows = []
            for _, row in fx_custom.iterrows():
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
                    "League": f"{m_match['HomeLeague']} vs {m_match['AwayLeague']}",
                    "TimeNY": "—",
                    "Score": "",  # Hypothétique
                    "IsUpcoming": True,
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
                    # Stats additionnelles (peuvent être None pour les ligues sans ces données)
                    "H_Shots_pg": h.get("Shots_pg"),
                    "H_ShotsTarget_pg": h.get("ShotsTarget_pg"),
                    "H_Corners_pg": h.get("Corners_pg"),
                    "H_CornersContre_pg": h.get("CornersContre_pg"),
                    "H_CornersTotal_pg": h.get("CornersTotal_pg"),
                    "H_CornersOver85": h.get("CornersOver85_pct"),
                    "H_CornersOver95": h.get("CornersOver95_pct"),
                    "H_CornersOver105": h.get("CornersOver105_pct"),
                    "H_Yellow_pg": h.get("Yellow_pg"),
                    "H_YellowsTotal_pg": h.get("YellowsTotal_pg"),
                    "H_YellowsOver35": h.get("YellowsOver35_pct"),
                    "H_Red_pg": h.get("Red_pg"),
                    "H_Fouls_pg": h.get("Fouls_pg"),
                    "A_Shots_pg": a.get("Shots_pg"),
                    "A_ShotsTarget_pg": a.get("ShotsTarget_pg"),
                    "A_Corners_pg": a.get("Corners_pg"),
                    "A_CornersContre_pg": a.get("CornersContre_pg"),
                    "A_CornersTotal_pg": a.get("CornersTotal_pg"),
                    "A_CornersOver85": a.get("CornersOver85_pct"),
                    "A_CornersOver95": a.get("CornersOver95_pct"),
                    "A_CornersOver105": a.get("CornersOver105_pct"),
                    "A_Yellow_pg": a.get("Yellow_pg"),
                    "A_YellowsTotal_pg": a.get("YellowsTotal_pg"),
                    "A_YellowsOver35": a.get("YellowsOver35_pct"),
                    "A_Red_pg": a.get("Red_pg"),
                    "A_Fouls_pg": a.get("Fouls_pg"),
                    "H2H_N": h2h["H2H_N"],
                    "H2H_AvgGoals": h2h["H2H_AvgGoals"],
                    "H2H_BTTS_pct": h2h["H2H_BTTS_pct"],
                    "H2H_O25_pct": h2h["H2H_O25_pct"],
                    "H2H_00_pct": h2h["H2H_00_pct"],
                })

            if matchups_rows:
                df_display = pd.DataFrame(matchups_rows)

                # 🆕 Toggle Vue Tableau / Détaillée + Type de stats
                col_vue_c, _ = st.columns([2, 6])
                with col_vue_c:
                    vue_custom = st.radio(
                        "Mode d'affichage",
                        options=["📊 Tableau", "🎴 Détaillée"],
                        index=0,
                        key="vue_custom",
                        horizontal=True,
                        label_visibility="collapsed",
                    )
                type_stats_custom = "Buts (défaut)"


                if vue_custom != "🎴 Détaillée":
                    cfc1, cfc2, _ = st.columns([2, 2, 4])
                    fenetre_forme_c = cfc1.selectbox("Fenêtre", ["5 derniers", "10 derniers", "Saison"], index=1, key="fenetre_forme_c")
                    perimetre_forme_c = cfc2.selectbox("Périmètre", ["Combiné", "Domicile", "Extérieur"], index=0, key="perimetre_forme_c")
                else:
                    fenetre_forme_c, perimetre_forme_c = "10 derniers", "Combiné"

                if vue_custom == "🎴 Détaillée":
                    df_display["FormeStats"] = [
                        stats_forme_match(tr_journal, r["HomeTeam"], r["AwayTeam"],
                                          r["H_Ligue"], saison_courante.get(r["H_Ligue"]),
                                          away_league=r["A_Ligue"], saison_away=saison_courante.get(r["A_Ligue"]))
                        for _, r in df_display.iterrows()
                    ]
                    rendre_cartes_matchs(df_display, st)
                else:
                    # Liste de colonnes selon le type de stats
                    if type_stats_custom == "Tirs & corners":
                        colonnes_custom = [
                            "HomeTeam", "H_Ligue", "AwayTeam", "A_Ligue",
                            "H_Shots_pg", "H_ShotsTarget_pg",
                            "H_Corners_pg", "H_CornersContre_pg",
                            "H_CornersTotal_pg", "H_CornersOver85", "H_CornersOver95", "H_CornersOver105",
                            "A_Shots_pg", "A_ShotsTarget_pg",
                            "A_Corners_pg", "A_CornersContre_pg",
                            "A_CornersTotal_pg", "A_CornersOver85", "A_CornersOver95", "A_CornersOver105",
                        ]
                    elif type_stats_custom == "Cartons & fautes":
                        colonnes_custom = [
                            "HomeTeam", "H_Ligue", "AwayTeam", "A_Ligue",
                            "H_Yellow_pg", "H_YellowsTotal_pg", "H_YellowsOver35",
                            "H_Red_pg", "H_Fouls_pg",
                            "A_Yellow_pg", "A_YellowsTotal_pg", "A_YellowsOver35",
                            "A_Red_pg", "A_Fouls_pg",
                        ]
                    else:  # Buts (défaut)
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
                    colonnes_custom = [c for c in colonnes_custom if c in df_display.columns]
                    if type_stats_custom == "Buts (défaut)":
                        _fmapc = {"5 derniers": "5", "10 derniers": "10", "Saison": "saison"}
                        _pmapc = {"Combiné": "combine", "Domicile": "domicile", "Extérieur": "exterieur"}
                        df_display["FormeStats"] = [
                            stats_forme_match(tr_journal, r["HomeTeam"], r["AwayTeam"],
                                              r["H_Ligue"], saison_courante.get(r["H_Ligue"]),
                                              away_league=r["A_Ligue"], saison_away=saison_courante.get(r["A_Ligue"]))
                            for _, r in df_display.iterrows()
                        ]
                        st.markdown(
                            rendre_tableau_forme(df_display, _fmapc[fenetre_forme_c], _pmapc[perimetre_forme_c], custom=True),
                            unsafe_allow_html=True,
                        )
                    else:
                        st.dataframe(
                            appliquer_couleurs(df_display, colonnes_custom),
                            use_container_width=True, hide_index=True, height=400,
                            column_config=build_column_config(colonnes_custom),
                        )