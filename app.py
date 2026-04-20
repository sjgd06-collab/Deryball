"""
Deryball — Application Streamlit principale.
"""
import streamlit as st
import pandas as pd
from stats import calculer_tout

st.set_page_config(page_title="Deryball", page_icon="⚽", layout="wide")

# ============================================================
# CHARGEMENT DES DONNÉES (avec cache)
# ============================================================
@st.cache_data(show_spinner="Calcul des stats en cours... (peut prendre ~1 minute au premier lancement)")
def charger():
    return calculer_tout("data/All_Leagues_2025-26.csv")

donnees = charger()
df_brut = donnees["df"]
team_stats = donnees["team_stats"]
matchups = donnees["matchups"]
saison_courante = donnees["saison_courante"]

# ============================================================
# FONCTIONS UTILITAIRES
# ============================================================
def appliquer_couleurs(df, cols):
    """Applique les dégradés de couleurs aux colonnes d'un tableau."""
    cols_pct_haut = [c for c in cols if c in [
        "H_Over05", "H_Over15", "H_Over25", "H_BTTS",
        "A_Over05", "A_Over15", "A_Over25", "A_BTTS",
        "P_Over05", "P_Over15", "P_Over25", "P_BTTS",
        "H2H_BTTS_pct", "H2H_O25_pct",
        "Over05_pct", "Over15_pct", "Over25_pct", "BTTS_pct",
        "CS_pct", "L10_Over25_pct", "L10_BTTS_pct",
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
tab_teams, tab_sequences, tab_poisson, tab_matchs = st.tabs(
    ["📊 Stats équipes", "🔥 Séquences en cours", "🎯 Force Poisson", "📅 Matchs"]
)

# ============================================================
# ONGLET STATS ÉQUIPES
# ============================================================
with tab_teams:
    st.caption("Statistiques cumulées par équipe et par saison.")
    fcol1, fcol2, fcol3 = st.columns([2, 2, 2])
    with fcol1:
        opt_saison = ["En cours (par défaut)", "Toutes les saisons"] + sorted(team_stats["Season"].unique().tolist())
        saison_sel = st.selectbox("Saison", options=opt_saison, index=0, key="teams_season")
    with fcol2:
        opt_ligue = ["Toutes les ligues"] + sorted(team_stats["League"].unique().tolist())
        ligue_sel = st.selectbox("Ligue", options=opt_ligue, index=0, key="teams_league")
    with fcol3:
        recherche_t = st.text_input("Rechercher équipe", placeholder="ex: Arsenal...", key="teams_search")

    df_t = filtrer_saison(team_stats, saison_sel)
    if ligue_sel != "Toutes les ligues":
        df_t = df_t[df_t["League"] == ligue_sel]
    if recherche_t:
        df_t = df_t[df_t["Team"].str.lower().str.contains(recherche_t.lower())]

    st.caption(f"{len(df_t)} équipe(s)")
    cols_t = [
        "Team", "League", "Season", "Pos", "Pts", "Form5", "MP", "W", "D", "L",
        "GF_pg", "GA_pg", "Total_pg",
        "Over05_pct", "Over15_pct", "Over25_pct", "BTTS_pct",
        "Count00", "Pct00", "CS_pct", "FTS_pct",
    ]
    cols_t = [c for c in cols_t if c in df_t.columns]
    df_t_sorted = df_t.sort_values(["League", "Pos"], na_position="last")
    st.dataframe(appliquer_couleurs(df_t_sorted, cols_t), use_container_width=True, hide_index=True, height=600)

# ============================================================
# ONGLET SÉQUENCES EN COURS
# ============================================================
with tab_sequences:
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
    cols_s = [c for c in cols_s if c in df_s.columns]
    st.dataframe(appliquer_couleurs(df_s, cols_s), use_container_width=True, hide_index=True, height=600)

# ============================================================
# ONGLET FORCE POISSON
# ============================================================
with tab_poisson:
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
    cols_p = [c for c in cols_p if c in df_p.columns]
    st.dataframe(appliquer_couleurs(df_p, cols_p), use_container_width=True, hide_index=True, height=600)

# ============================================================
# ONGLET MATCHS
# ============================================================
with tab_matchs:
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

    st.caption(f"{len(df_aff)} match(s) le {date_selectionnee}")

    colonnes = [
        "TimeNY", "League", "HomeTeam", "AwayTeam", "Score",
        "H_Pos", "H_Form", "H_Over05", "H_Over15", "H_Over25", "H_BTTS", "H_00_Count", "H_00_Pct",
        "A_Pos", "A_Form", "A_Over05", "A_Over15", "A_Over25", "A_BTTS", "A_00_Count", "A_00_Pct",
        "Combined_00_Pct", "xG_H", "xG_A",
        "P_Over05", "P_Over15", "P_Over25", "P_BTTS", "P_00",
        "H2H_N", "H2H_AvgGoals", "H2H_BTTS_pct", "H2H_O25_pct",
    ]
    colonnes = [c for c in colonnes if c in df_aff.columns]
    st.dataframe(appliquer_couleurs(df_aff, colonnes), use_container_width=True, hide_index=True, height=600)