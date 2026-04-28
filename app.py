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
    --bg-base: #0E0E18;
    --bg-surface: #15151F;
    --bg-elevated: #1C1C2A;
    --bg-hover: #232333;
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
.stApp, .stApp p, .stApp span:not(.flag), .stApp label, .stApp div {
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
    background: var(--bg-surface);
    border: 1px solid var(--border-default);
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
    color: var(--accent) !important;
    border-bottom: 2px solid var(--accent) !important;
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
    font-size: 13.5px !important;
    font-weight: 500 !important;
    padding: 6px 10px !important;
    transition: all 0.15s ease !important;
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
   TOGGLE
   ====================================================== */
.stCheckbox > label > div {
    background: var(--bg-elevated) !important;
    border: 1px solid var(--border-default) !important;
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
}

def build_column_config(colonnes):
    """Construit la column_config de Streamlit avec les tooltips et des labels lisibles."""
    import streamlit as st
    config = {}
    for col in colonnes:
        label = LABELS_COLONNES.get(col, col)  # nom court si disponible, sinon nom technique
        help_text = DESCRIPTIONS_COLONNES.get(col)  # description pour tooltip
        config[col] = st.column_config.Column(
            label,
            help=help_text,
        )
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
        styled = styled.background_gradient(subset=cols_streak, cmap="YlOrRd", vmin=0, vmax=10)
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
    mode_mobile = st.toggle("📱 Mode mobile", value=False,
                             help="Simplifie l'affichage pour les écrans étroits")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Matchs", f"{len(df_brut):,}".replace(",", " "))
with col2:
    st.metric("Équipes-saisons", len(team_stats))
with col3:
    st.metric("Ligues", df_brut["DisplayLeague"].nunique())
with col4:
    st.metric("Dernier match", df_brut["Date"].max().strftime("%Y-%m-%d"))

st.divider()

# ============================================================
# ONGLETS
# ============================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Stats équipes",
    "🔥 Séquences en cours",
    "🎯 Force Poisson",
    "📅 Matchs",
    "🧪 Matchups personnalisés",
])

# ============================================================
# ONGLET STATS ÉQUIPES
# ============================================================
with tab1:
    st.caption("Statistiques cumulées par équipe et par saison.")
    fcol1, fcol2, fcol3, fcol4 = st.columns([2, 2, 2, 2])
    with fcol1:
        opt_saison = ["En cours (par défaut)", "Toutes les saisons"] + sorted(team_stats["Season"].unique().tolist())
        saison_sel = st.selectbox("Saison", options=opt_saison, index=0, key="teams_season")
    with fcol2:
        opt_ligue = ["Toutes les ligues"] + sorted(team_stats["League"].unique().tolist())
        ligue_sel = st.selectbox("Ligue", options=opt_ligue, index=0, key="teams_league")
    with fcol3:
        recherche_t = st.text_input("Rechercher équipe", placeholder="ex: Arsenal...", key="teams_search")
    with fcol4:
        type_stats = st.selectbox("Type de stats",
                                   options=["Buts (défaut)", "Tirs & corners", "Cartons & fautes"],
                                   index=0, key="teams_type")

    df_t = filtrer_saison(team_stats, saison_sel)
    if ligue_sel != "Toutes les ligues":
        df_t = df_t[df_t["League"] == ligue_sel]
    if recherche_t:
        df_t = df_t[df_t["Team"].str.lower().str.contains(recherche_t.lower())]

    st.caption(f"{len(df_t)} équipe(s)")

    # Choisir les colonnes selon le type de stats sélectionné
    if type_stats == "Tirs & corners":
        cols_t = [
            "Team", "League", "Season", "Pos", "MP",
            "Shots_pg", "ShotsContre_pg",
            "ShotsTarget_pg", "ShotsTargetContre_pg",
            "Corners_pg", "CornersContre_pg", "CornersTotal_pg",
            "CornersOver85_pct", "CornersOver95_pct", "CornersOver105_pct",
        ]
    elif type_stats == "Cartons & fautes":
        cols_t = [
            "Team", "League", "Season", "Pos", "MP",
            "Yellow_pg", "YellowContre_pg", "YellowsTotal_pg", "YellowsOver35_pct",
            "Red_pg", "RedContre_pg",
            "Fouls_pg", "FoulsContre_pg",
        ]
    else:  # Buts (défaut)
        cols_t = [
            "Team", "League", "Season", "Pos", "Pts", "Form5", "MP", "W", "D", "L",
            "GF_pg", "GA_pg", "Total_pg",
            "Over05_pct", "Over15_pct", "Over25_pct", "BTTS_pct",
            "Count00", "Pct00", "CS_pct", "FTS_pct",
        ]
        # En mode mobile, on réduit aux colonnes essentielles
    if mode_mobile:
        if type_stats == "Tirs & corners":
            cols_t = ["Team", "League", "Pos", "Shots_pg", "Corners_pg", "CornersOver95_pct"]
        elif type_stats == "Cartons & fautes":
            cols_t = ["Team", "League", "Pos", "Yellow_pg", "YellowsOver35_pct", "Red_pg"]
        else:
            cols_t = ["Team", "League", "Pos", "Over05_pct", "Over15_pct", "Over25_pct", "Pct00"]
    cols_t = [c for c in cols_t if c in df_t.columns]
    df_t_sorted = df_t.sort_values(["League", "Pos"], na_position="last")
    st.dataframe(
        appliquer_couleurs(df_t_sorted, cols_t),
        use_container_width=True,
        hide_index=True,
        height=600,
        column_config=build_column_config(cols_t),
    )

# ============================================================
# ONGLET SÉQUENCES EN COURS
# ============================================================
with tab2:
    st.caption("Séquences actives en cours pour chaque équipe (basées sur leurs derniers matchs consécutifs).")
    fcol1, fcol2, fcol3 = st.columns([2, 2, 2])
    with fcol1:
        opt_saison_s = ["En cours (par défaut)", "Toutes les saisons"] + sorted(team_stats["Season"].unique().tolist())
        saison_sel_s = st.selectbox("Saison", options=opt_saison_s, index=0, key="seq_season")
    with fcol2:
        opt_ligue_s = ["Toutes les ligues"] + sorted(team_stats["League"].unique().tolist())
        ligue_sel_s = st.selectbox("Ligue", options=opt_ligue_s, index=0, key="seq_league")
    with fcol3:
        recherche_s = st.text_input("Rechercher équipe", placeholder="ex: Arsenal...", key="seq_search")

    df_s = filtrer_saison(team_stats, saison_sel_s)
    if ligue_sel_s != "Toutes les ligues":
        df_s = df_s[df_s["League"] == ligue_sel_s]
    if recherche_s:
        df_s = df_s[df_s["Team"].str.lower().str.contains(recherche_s.lower())]

    st.caption(f"{len(df_s)} équipe(s)")
    cols_s = [
        "Team", "League", "Season", "Pos", "Form5", "MP",
        "Streak_NoScore", "Streak_NoConcede",
        "Streak_BTTS", "Streak_NoBTTS",
        "Streak_Over05", "Streak_Over15", "Streak_Over25", "Streak_Under25",
        "Streak_No00",
        "Streak_Win", "Streak_NoWin", "Streak_Loss",
        "L10_Over25_pct", "L10_BTTS_pct",
    ]
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
# ONGLET FORCE POISSON
# ============================================================
with tab3:
    st.caption("Forces d'attaque/défense normalisées par la moyenne de la ligue (1.00 = moyenne).")
    fcol1, fcol2, fcol3 = st.columns([2, 2, 2])
    with fcol1:
        opt_saison_p = ["En cours (par défaut)", "Toutes les saisons"] + sorted(team_stats["Season"].unique().tolist())
        saison_sel_p = st.selectbox("Saison", options=opt_saison_p, index=0, key="pois_season")
    with fcol2:
        opt_ligue_p = ["Toutes les ligues"] + sorted(team_stats["League"].unique().tolist())
        ligue_sel_p = st.selectbox("Ligue", options=opt_ligue_p, index=0, key="pois_league")
    with fcol3:
        recherche_p = st.text_input("Rechercher équipe", placeholder="ex: Arsenal...", key="pois_search")

    df_p = filtrer_saison(team_stats, saison_sel_p)
    if ligue_sel_p != "Toutes les ligues":
        df_p = df_p[df_p["League"] == ligue_sel_p]
    if recherche_p:
        df_p = df_p[df_p["Team"].str.lower().str.contains(recherche_p.lower())]

    st.caption(f"{len(df_p)} équipe(s)")
    cols_p = [
        "Team", "League", "Season", "Pos", "MP",
        "HomeAttack", "HomeDefense", "AwayAttack", "AwayDefense",
        "xG_home", "xG_away",
    ]
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
# ONGLET MATCHS
# ============================================================
with tab4:
    # ============================================================
    # CHIPS DE FILTRES RAPIDES
    # ============================================================
    from datetime import date, timedelta
    aujourdhui = date.today()
    demain = aujourdhui + timedelta(days=1)
    # Trouver le prochain samedi (0=lundi, 5=samedi, 6=dimanche)
    jours_jusquau_samedi = (5 - aujourdhui.weekday()) % 7
    if jours_jusquau_samedi == 0:  # si on est samedi, le "week-end" commence aujourd'hui
        jours_jusquau_samedi = 0
    prochain_samedi = aujourdhui + timedelta(days=jours_jusquau_samedi)
    prochain_dimanche = prochain_samedi + timedelta(days=1)

    # Init session state pour garder le filtre actif
    if "filtre_rapide" not in st.session_state:
        st.session_state.filtre_rapide = None
    if "dates_filtrees" not in st.session_state:
        st.session_state.dates_filtrees = None

    # En mode mobile, on laisse plus d'espace aux chips
    if mode_mobile:
        chip0, chip1, chip2, chip3, chip4, chip5 = st.columns(6)
    else:
        chip0, chip1, chip2, chip3, chip4, chip5, _ = st.columns([1, 1.2, 1, 1.3, 1.5, 0.8, 2.2])
    with chip0:
        if st.button("⬅️ Hier", use_container_width=True, key="chip_yesterday"):
            hier = aujourdhui - timedelta(days=1)
            st.session_state.filtre_rapide = "yesterday"
            st.session_state.dates_filtrees = [hier.strftime("%Y-%m-%d")]
    with chip1:
        if st.button("🕐 Aujourd'hui", use_container_width=True, key="chip_today"):
            st.session_state.filtre_rapide = "today"
            st.session_state.dates_filtrees = [aujourdhui.strftime("%Y-%m-%d")]
    with chip2:
        if st.button("➡️ Demain", use_container_width=True, key="chip_tomorrow"):
            st.session_state.filtre_rapide = "tomorrow"
            st.session_state.dates_filtrees = [demain.strftime("%Y-%m-%d")]
    with chip3:
        if st.button("🎯 Ce week-end", use_container_width=True, key="chip_weekend"):
            st.session_state.filtre_rapide = "weekend"
            st.session_state.dates_filtrees = [
                prochain_samedi.strftime("%Y-%m-%d"),
                prochain_dimanche.strftime("%Y-%m-%d"),
            ]
    with chip4:
        if st.button("📅 7 prochains jours", use_container_width=True, key="chip_week"):
            st.session_state.filtre_rapide = "week"
            st.session_state.dates_filtrees = [
                (aujourdhui + timedelta(days=i)).strftime("%Y-%m-%d")
                for i in range(8)
            ]
    with chip5:
        if st.button("🔙 Tout", use_container_width=True, key="chip_reset"):
            st.session_state.filtre_rapide = None
            st.session_state.dates_filtrees = None

    # Afficher le filtre actif
    if st.session_state.filtre_rapide:
        labels = {"yesterday": "Hier", "today": "Aujourd'hui", "tomorrow": "Demain",
                  "weekend": "Ce week-end", "week": "7 prochains jours"}
        st.caption(f"🔍 Filtre actif : **{labels[st.session_state.filtre_rapide]}** — cliquez sur 🔙 Tout pour retirer.")
    # En mode mobile, empiler verticalement avec des colonnes de 1 (prend toute la largeur)
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

    # Si un chip est actif, on filtre sur plusieurs dates possibles
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

    # Afficher clairement la période couverte par le tableau
    if st.session_state.dates_filtrees:
        labels = {"yesterday": "Hier", "today": "Aujourd'hui", "tomorrow": "Demain",
                  "weekend": "Ce week-end", "week": "7 prochains jours"}
        label = labels.get(st.session_state.filtre_rapide, "Période sélectionnée")

        # Construire le résumé des dates couvertes
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

    colonnes = [
        "TimeNY", "League", "HomeTeam", "AwayTeam", "Score",
        "H_Pos", "H_Form", "H_Over05", "H_Over15", "H_Over25", "H_BTTS", "H_00_Count", "H_00_Pct",
        "A_Pos", "A_Form", "A_Over05", "A_Over15", "A_Over25", "A_BTTS", "A_00_Count", "A_00_Pct",
        "Combined_00_Pct", "xG_H", "xG_A",
        "P_Over05", "P_Over15", "P_Over25", "P_BTTS", "P_00",
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
# ONGLET 5 — MATCHUPS PERSONNALISÉS
# ============================================================
with tab5:
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
                from stats import probs_match, h2h_stats
                lam_h = h["HomeAttack"] * a["AwayDefense"] * h["_lg_h"]
                lam_a = a["AwayAttack"] * h["HomeDefense"] * a["_lg_a"]
                probs = probs_match(lam_h, lam_a)
                h2h = h2h_stats(idx_h2h, m_match["HomeTeam"], m_match["AwayTeam"], today)

                matchups_rows.append({
                    "HomeTeam": m_match["HomeTeam"],
                    "H_Ligue": m_match["HomeLeague"],
                    "AwayTeam": m_match["AwayTeam"],
                    "A_Ligue": m_match["AwayLeague"],
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
                    "H_Pos", "H_Form", "H_Over05", "H_Over15", "H_Over25", "H_BTTS",
                    "H_00_Count", "H_00_Pct",
                    "A_Pos", "A_Form", "A_Over05", "A_Over15", "A_Over25", "A_BTTS",
                    "A_00_Count", "A_00_Pct",
                    "Combined_00_Pct", "xG_H", "xG_A",
                    "P_Over05", "P_Over15", "P_Over25", "P_BTTS", "P_00",
                    "H2H_N", "H2H_AvgGoals", "H2H_BTTS_pct", "H2H_O25_pct",
                ]
                if mode_mobile:
                    colonnes_custom = ["HomeTeam", "AwayTeam",
                                       "H_Over05", "A_Over05", "H_Over15", "A_Over15",
                                       "P_Over05", "P_Over15", "P_00"]
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