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
    cols_s = [c for c in cols_s if c in df_s.columns]
    st.dataframe(appliquer_couleurs(df_s, cols_s), use_container_width=True, hide_index=True, height=600)

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
    cols_p = [c for c in cols_p if c in df_p.columns]
    st.dataframe(appliquer_couleurs(df_p, cols_p), use_container_width=True, hide_index=True, height=600)

# ============================================================
# ONGLET MATCHS
# ============================================================
with tab4:
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
                colonnes_custom = [c for c in colonnes_custom if c in df_display.columns]
                st.dataframe(
                    appliquer_couleurs(df_display, colonnes_custom),
                    use_container_width=True,
                    hide_index=True,
                    height=400,
                )
            else:
                st.warning("Aucun matchup valide. Vérifie que les équipes ont des stats disponibles.")