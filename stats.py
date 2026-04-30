"""
Calculs de statistiques pour Deryball.
Ce fichier charge les CSVs, calcule les stats par équipe, et produit
les matchups avec probabilités Poisson et historique H2H.
"""
import pandas as pd
import math
from datetime import datetime
from zoneinfo import ZoneInfo

# ============================================================
# 1. CHARGEMENT ET NETTOYAGE DES DONNÉES
# ============================================================

PAYS_COURT = {
    "Germany": "ALL", "Austria": "AUT", "Italy": "ITA", "Brazil": "BRE",
    "Switzerland": "SUI", "Greece": "GRE", "Spain": "ESP", "England": "ANG",
    "France": "FRA", "Portugal": "POR", "Netherlands": "PAY", "Turkey": "TUR",
    "Scotland": "ECO", "USA": "USA", "Mexico": "MEX", "Argentina": "ARG",
    "Norway": "NOR", "Poland": "POL",
}
# Codes pays courts (3 lettres) pour préfixer le nom des ligues
CODES_PAYS = {
    "England":     "ANG",
    "Scotland":    "ECO",
    "Germany":     "ALL",
    "Italy":       "ITA",
    "Spain":       "ESP",
    "France":      "FRA",
    "Netherlands": "PAY",
    "Portugal":    "POR",
    "Turkey":      "TUR",
    "Greece":      "GRE",
    "Belgium":     "BEL",
    "Austria":     "AUT",
    "Switzerland": "SUI",
    "Poland":      "POL",
    "Norway":      "NOR",
    "Argentina":   "ARG",
    "Brazil":      "BRE",
    "Mexico":      "MEX",
    "USA":         "USA",
    "UEFA":        "UEFA",
}

LIGUES_ANNEE_CIVILE = {"ARG", "BRA", "NOR", "USA"}
LIGUES_DOUBLE_SAISON = {"MEX"}

def inferer_saison(code_ligue, date):
    y, m = date.year, date.month
    if code_ligue in LIGUES_ANNEE_CIVILE:
        return str(y)
    if code_ligue in LIGUES_DOUBLE_SAISON:
        if m >= 7:
            return f"{y}/{y+1} Ap."
        return f"{y-1}/{y} Cl."
    if m >= 7:
        return f"{y}-{str(y+1)[2:]}"
    return f"{y-1}-{str(y)[2:]}"

def charger_et_preparer(chemin_csv):
    df = pd.read_csv(chemin_csv)
    df = df.dropna(subset=["FTHG", "FTAG"]).copy()
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date"]).sort_values("Date").reset_index(drop=True)
    df["FTHG"] = df["FTHG"].astype(int)
    df["FTAG"] = df["FTAG"].astype(int)

    compte_noms = df.groupby("LeagueName")["Country"].nunique()
    ambigus = compte_noms[compte_noms > 1].index.tolist()
    def designer(row):
        code = CODES_PAYS.get(row["Country"], row["Country"][:3].upper())
        return f"[{code}] {row['LeagueName']}"
    df["DisplayLeague"] = df.apply(designer, axis=1)

    df["Season"] = df.apply(lambda r: inferer_saison(r["League"], r["Date"]), axis=1)

    uk_tz = ZoneInfo("Europe/London")
    ny_tz = ZoneInfo("America/New_York")
    def vers_ny_heure(date, heure):
        if pd.isna(heure) or not heure or pd.isna(date):
            return ""
        try:
            dt = datetime.strptime(f"{date.strftime('%Y-%m-%d')} {heure}", "%Y-%m-%d %H:%M").replace(tzinfo=uk_tz)
            return dt.astimezone(ny_tz).strftime("%H:%M")
        except Exception:
            return heure
    def vers_ny_date(date, heure):
        if pd.isna(heure) or not heure or pd.isna(date):
            return date.strftime("%Y-%m-%d")
        try:
            dt = datetime.strptime(f"{date.strftime('%Y-%m-%d')} {heure}", "%Y-%m-%d %H:%M").replace(tzinfo=uk_tz)
            return dt.astimezone(ny_tz).strftime("%Y-%m-%d")
        except Exception:
            return date.strftime("%Y-%m-%d")
    df["TimeNY"] = df.apply(lambda r: vers_ny_heure(r["Date"], r["Time"]), axis=1)
    df["DateNY"] = df.apply(lambda r: vers_ny_date(r["Date"], r["Time"]), axis=1)
    df["IsUpcoming"] = False  # Par défaut tous les matchs de ce fichier sont joués

    return df
# ============================================================
# 2. STATS PAR ÉQUIPE
# ============================================================

def construire_team_rows(df):
    # Colonnes de stats additionnelles (peuvent être absentes pour les ligues extra)
    # H* = valeur domicile, A* = valeur extérieur
    cols_extra = ["HS", "AS", "HST", "AST", "HC", "AC", "HY", "AY", "HR", "AR", "HF", "AF"]
    cols_extra_dispo = [c for c in cols_extra if c in df.columns]

    # Base home : on construit les colonnes de base + les extras si dispo
    cols_base_home = ["League", "DisplayLeague", "Season", "Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG"] + cols_extra_dispo
    home = df[cols_base_home].copy()
    home = home.rename(columns={"HomeTeam": "Team", "AwayTeam": "Opponent", "FTHG": "GF", "FTAG": "GA"})
    # Pour les stats extra, on renomme H* en "Pour" (fait) et A* en "Contre" (subi)
    renames_home = {}
    for c in cols_extra_dispo:
        if c.startswith("H"):
            renames_home[c] = c[1:] + "_pour"  # HS -> S_pour
        elif c.startswith("A"):
            renames_home[c] = c[1:] + "_contre"  # AS -> S_contre
    home = home.rename(columns=renames_home)
    home["Venue"] = "H"

    # Base away : on fait pareil en inversant
    cols_base_away = ["League", "DisplayLeague", "Season", "Date", "AwayTeam", "HomeTeam", "FTAG", "FTHG"] + cols_extra_dispo
    away = df[cols_base_away].copy()
    away = away.rename(columns={"AwayTeam": "Team", "HomeTeam": "Opponent", "FTAG": "GF", "FTHG": "GA"})
    # Pour l'away, les stats sont inversées : A* = pour soi, H* = pour l'adversaire
    renames_away = {}
    for c in cols_extra_dispo:
        if c.startswith("A"):
            renames_away[c] = c[1:] + "_pour"  # AS -> S_pour
        elif c.startswith("H"):
            renames_away[c] = c[1:] + "_contre"  # HS -> S_contre
    away = away.rename(columns=renames_away)
    away["Venue"] = "A"

    tr = pd.concat([home, away], ignore_index=True).sort_values(["Team", "Date"]).reset_index(drop=True)
    tr["Total"] = tr["GF"] + tr["GA"]
    tr["BTTS"] = (tr["GF"] > 0) & (tr["GA"] > 0)
    tr["Over05"] = tr["Total"] > 0.5
    tr["Over15"] = tr["Total"] > 1.5
    tr["Over25"] = tr["Total"] > 2.5
    tr["Is00"] = (tr["GF"] == 0) & (tr["GA"] == 0)
    tr["NoScore"] = tr["GF"] == 0
    tr["NoConcede"] = tr["GA"] == 0
    tr["Win"] = tr["GF"] > tr["GA"]
    tr["Draw"] = tr["GF"] == tr["GA"]
    tr["Loss"] = tr["GF"] < tr["GA"]
    tr["Points"] = tr["Win"] * 3 + tr["Draw"] * 1
    tr["GD"] = tr["GF"] - tr["GA"]
    return tr

def streak_courante(s):
    c = 0
    for v in reversed(s.tolist()):
        if v:
            c += 1
        else:
            break
    return c

def forme_derniers_n(grp, n=5):
    last = grp.tail(n)
    return "".join(["V" if r["Win"] else "N" if r["Draw"] else "D" for _, r in last.iterrows()])

def calculer_team_stats(df):
    tr = construire_team_rows(df)
    moy_dom = tr[tr["Venue"] == "H"].groupby(["DisplayLeague", "Season"])["GF"].mean().to_dict()
    moy_ext = tr[tr["Venue"] == "A"].groupby(["DisplayLeague", "Season"])["GF"].mean().to_dict()

    classements = {}
    for (lg, saison), rows in tr.groupby(["DisplayLeague", "Season"]):
        agg = rows.groupby("Team").agg(
            MP=("GF", "count"), Pts=("Points", "sum"), GD=("GD", "sum"), GF=("GF", "sum")
        ).reset_index()
        agg = agg.sort_values(["Pts", "GD", "GF"], ascending=[False, False, False]).reset_index(drop=True)
        agg["Position"] = agg.index + 1
        classements[(lg, saison)] = dict(zip(agg["Team"], zip(agg["Position"], agg["Pts"], agg["GD"])))

    stats = {}
    for (team, lg, saison), grp in tr.groupby(["Team", "DisplayLeague", "Season"]):
        grp = grp.sort_values("Date")
        if len(grp) < 3:
            continue
        h = grp[grp["Venue"] == "H"]
        a = grp[grp["Venue"] == "A"]
        lg_h = moy_dom.get((lg, saison), 1.4)
        lg_a = moy_ext.get((lg, saison), 1.1)
        home_attack = (h["GF"].mean() / lg_h) if len(h) > 0 and lg_h > 0 else 1.0
        home_defense = (h["GA"].mean() / lg_a) if len(h) > 0 and lg_a > 0 else 1.0
        away_attack = (a["GF"].mean() / lg_a) if len(a) > 0 and lg_a > 0 else 1.0
        away_defense = (a["GA"].mean() / lg_h) if len(a) > 0 and lg_h > 0 else 1.0
        pos, pts, gd = classements.get((lg, saison), {}).get(team, (None, None, None))
        last10 = grp.tail(10)
        last5 = grp.tail(5)

        # Stats récentes vs saison (pour détection d'anomalies)
        gf_pg_5 = last5["GF"].mean() if len(last5) > 0 else None
        ga_pg_5 = last5["GA"].mean() if len(last5) > 0 else None
        over25_5 = 100 * last5["Over25"].mean() if len(last5) > 0 else None
        btts_5 = 100 * last5["BTTS"].mean() if len(last5) > 0 else None

        gf_pg_10 = last10["GF"].mean() if len(last10) > 0 else None
        ga_pg_10 = last10["GA"].mean() if len(last10) > 0 else None
        over25_10 = 100 * last10["Over25"].mean() if len(last10) > 0 else None
        btts_10 = 100 * last10["BTTS"].mean() if len(last10) > 0 else None
        stats[(team, lg, saison)] = {
            "Team": team, "League": lg, "Season": saison, "MP": len(grp),
            "Pos": pos, "Pts": pts, "W": int(grp["Win"].sum()),
            "D": int(grp["Draw"].sum()), "L": int(grp["Loss"].sum()),
            "GF_pg": round(grp["GF"].mean(), 2), "GA_pg": round(grp["GA"].mean(), 2),
            "Total_pg": round(grp["Total"].mean(), 2),
            "Over05_pct": round(100 * grp["Over05"].mean(), 1),
            "Over15_pct": round(100 * grp["Over15"].mean(), 1),
            "Over25_pct": round(100 * grp["Over25"].mean(), 1),
            "BTTS_pct": round(100 * grp["BTTS"].mean(), 1),
            "Count00": int(grp["Is00"].sum()),
            "Pct00": round(100 * grp["Is00"].mean(), 1),
            "CS_pct": round(100 * grp["NoConcede"].mean(), 1),
            "FTS_pct": round(100 * grp["NoScore"].mean(), 1),
            "Form5": forme_derniers_n(grp, 5),
            "Streak_NoScore": streak_courante(grp["NoScore"]),
            "Streak_NoConcede": streak_courante(grp["NoConcede"]),
            "Streak_BTTS": streak_courante(grp["BTTS"]),
            "Streak_NoBTTS": streak_courante(~grp["BTTS"]),
            "Streak_Over05": streak_courante(grp["Over05"]),
            "Streak_Over15": streak_courante(grp["Over15"]),
            "Streak_Over25": streak_courante(grp["Over25"]),
            "Streak_Under25": streak_courante(~grp["Over25"]),
            "Streak_No00": streak_courante(~grp["Is00"]),
            "Streak_Win": streak_courante(grp["Win"]),
            "Streak_NoWin": streak_courante(~grp["Win"]),
            "Streak_Loss": streak_courante(grp["Loss"]),
            "L10_Over25_pct": round(100 * last10["Over25"].mean(), 1),
            "L10_BTTS_pct": round(100 * last10["BTTS"].mean(), 1),
            # Stats sur 5 derniers et 10 derniers (pour anomalies)
            "L5_GF_pg": round(gf_pg_5, 2) if gf_pg_5 is not None else None,
            "L5_GA_pg": round(ga_pg_5, 2) if ga_pg_5 is not None else None,
            "L5_Over25_pct": round(over25_5, 1) if over25_5 is not None else None,
            "L5_BTTS_pct": round(btts_5, 1) if btts_5 is not None else None,
            "L10_GF_pg": round(gf_pg_10, 2) if gf_pg_10 is not None else None,
            "L10_GA_pg": round(ga_pg_10, 2) if ga_pg_10 is not None else None,
            "HomeAttack": round(home_attack, 2), "HomeDefense": round(home_defense, 2),
            "AwayAttack": round(away_attack, 2), "AwayDefense": round(away_defense, 2),
            "xG_home": round(home_attack * lg_h, 2),
            "xG_away": round(away_attack * lg_a, 2),
            "_lg_h": lg_h, "_lg_a": lg_a,
        }
# Sparklines : 10 derniers matchs (chronologique : ancien → récent)
        recent_10 = grp.tail(10)
        stats[(team, lg, saison)]["Spark_GF"] = recent_10["GF"].astype(int).tolist()
        stats[(team, lg, saison)]["Spark_GA"] = recent_10["GA"].astype(int).tolist()
        stats[(team, lg, saison)]["Spark_Total"] = (
            recent_10["GF"] + recent_10["GA"]
        ).astype(int).tolist()
        # Stats additionnelles (si colonnes disponibles)
        for prefix, libelle in [("S", "Shots"), ("ST", "ShotsTarget"), ("C", "Corners"),
                                 ("Y", "Yellow"), ("R", "Red"), ("F", "Fouls")]:
            col_pour = f"{prefix}_pour"
            col_contre = f"{prefix}_contre"
            if col_pour in grp.columns and grp[col_pour].notna().any():
                stats[(team, lg, saison)][f"{libelle}_pg"] = round(grp[col_pour].mean(), 2)
                stats[(team, lg, saison)][f"{libelle}Contre_pg"] = round(grp[col_contre].mean(), 2)

        # Stats corners : Over 9.5 (seuil classique pour les paris)
        if "C_pour" in grp.columns and grp["C_pour"].notna().any():
            corners_total = grp["C_pour"].fillna(0) + grp["C_contre"].fillna(0)
            stats[(team, lg, saison)]["CornersTotal_pg"] = round(corners_total.mean(), 2)
            stats[(team, lg, saison)]["CornersOver95_pct"] = round(100 * (corners_total > 9.5).mean(), 1)
            stats[(team, lg, saison)]["CornersOver85_pct"] = round(100 * (corners_total > 8.5).mean(), 1)
            stats[(team, lg, saison)]["CornersOver105_pct"] = round(100 * (corners_total > 10.5).mean(), 1)

        # Stats cartons : Over 3.5 jaunes dans le match (équipe + adversaire)
        if "Y_pour" in grp.columns and grp["Y_pour"].notna().any():
            cartons_jaunes_total = grp["Y_pour"].fillna(0) + grp["Y_contre"].fillna(0)
            stats[(team, lg, saison)]["YellowsTotal_pg"] = round(cartons_jaunes_total.mean(), 2)
            stats[(team, lg, saison)]["YellowsOver35_pct"] = round(100 * (cartons_jaunes_total > 3.5).mean(), 1)

    return stats

# ============================================================
# 3. PROBABILITÉS POISSON ET MATCHUPS
# ============================================================

def poisson_pmf(k, lam):
    if lam <= 0:
        return 1.0 if k == 0 else 0.0
    return (lam ** k * math.exp(-lam)) / math.factorial(k)


def tau_correction(x, y, lam_h, lam_a, rho):
    """
    Facteur de correction Dixon-Coles pour les 4 scores faibles.
    Modélise la corrélation observée entre buts H et A (Poisson assume indépendance).

    rho < 0 (typique en foot) : ↑ P(0-0) et P(1-1), ↓ P(1-0) et P(0-1).
    rho = 0 : retombe sur Poisson indépendant classique.
    """
    if x == 0 and y == 0:
        return 1 - lam_h * lam_a * rho
    elif x == 0 and y == 1:
        return 1 + lam_h * rho
    elif x == 1 and y == 0:
        return 1 + lam_a * rho
    elif x == 1 and y == 1:
        return 1 - rho
    return 1.0


def probs_match(lam_h, lam_a, max_g=10, rho=-0.10):
    """
    Probabilités d'événements (Poisson + correction Dixon-Coles).
    rho=-0.10 par défaut (valeur empirique standard en littérature foot).
    rho=0 → Poisson pur sans correction.
    """
    p = {"p00": 0, "over05": 0, "over15": 0, "over25": 0, "btts": 0}
    for i in range(max_g):
        for j in range(max_g):
            tau = tau_correction(i, j, lam_h, lam_a, rho) if rho != 0 else 1.0
            pr = tau * poisson_pmf(i, lam_h) * poisson_pmf(j, lam_a)
            t = i + j
            if i == 0 and j == 0:
                p["p00"] += pr
            if t >= 1:
                p["over05"] += pr
            if t >= 2:
                p["over15"] += pr
            if t >= 3:
                p["over25"] += pr
            if i > 0 and j > 0:
                p["btts"] += pr
    return p
def matrice_scores(lam_h, lam_a, max_g=6, rho=-0.10):
    """
    Calcule la matrice max_g x max_g des probabilités de chaque score exact
    (avec correction Dixon-Coles). Retourne aussi top 3 scores et marges 1X2.

    Note : la matrice est tronquée à max_g buts/équipe, donc la somme des
    probas est < 1. Les marges 1X2 sont re-normalisées pour sommer à 100%.
    """
    matrice = [[0.0] * max_g for _ in range(max_g)]
    total = 0.0
    for i in range(max_g):
        for j in range(max_g):
            tau = tau_correction(i, j, lam_h, lam_a, rho) if rho != 0 else 1.0
            p = tau * poisson_pmf(i, lam_h) * poisson_pmf(j, lam_a)
            matrice[i][j] = p
            total += p

    # Top 3 scores les plus probables
    scores_plats = [(i, j, matrice[i][j]) for i in range(max_g) for j in range(max_g)]
    scores_plats.sort(key=lambda x: x[2], reverse=True)
    top3 = scores_plats[:3]

    # Marges 1X2 (re-normalisées sur la matrice tronquée)
    p_home = sum(matrice[i][j] for i in range(max_g) for j in range(max_g) if i > j)
    p_draw = sum(matrice[i][i] for i in range(max_g))
    p_away = sum(matrice[i][j] for i in range(max_g) for j in range(max_g) if i < j)
    if total > 0:
        p_home, p_draw, p_away = p_home / total, p_draw / total, p_away / total

    return {
        "matrice": matrice,
        "top3": top3,
        "p_home": p_home,
        "p_draw": p_draw,
        "p_away": p_away,
        "couverture": total,  # somme avant normalisation, indique si on couvre ≥95%
    }

def recalculer_probs_avec_rho(matchups_df, rho):
    """
    Recalcule P_* pour un rho donné en partant des xG_H/xG_A déjà calculés.
    Utile pour comparer DC vs Poisson pur dans la validation.
    """
    df = matchups_df.copy()
    new_rows = []
    for _, row in df.iterrows():
        lam_h = row.get("xG_H")
        lam_a = row.get("xG_A")
        if pd.isna(lam_h) or pd.isna(lam_a):
            new_rows.append({"P_Over05": None, "P_Over15": None,
                             "P_Over25": None, "P_BTTS": None, "P_00": None})
            continue
        probs = probs_match(lam_h, lam_a, rho=rho)
        new_rows.append({
            "P_Over05": round(100 * probs["over05"], 1),
            "P_Over15": round(100 * probs["over15"], 1),
            "P_Over25": round(100 * probs["over25"], 1),
            "P_BTTS":   round(100 * probs["btts"], 1),
            "P_00":     round(100 * probs["p00"], 1),
        })
    np_df = pd.DataFrame(new_rows)
    for col in ["P_Over05", "P_Over15", "P_Over25", "P_BTTS", "P_00"]:
        df[col] = np_df[col].values
    return df
def construire_index_h2h(df):
    """
    Pré-calcule un index des confrontations par paire d'équipes.
    Retourne un dict {frozenset({team_a, team_b}): DataFrame des matchs entre ces 2 équipes}
    """
    index = {}
    for _, row in df.iterrows():
        cle = frozenset({row["HomeTeam"], row["AwayTeam"]})
        if cle not in index:
            index[cle] = []
        index[cle].append({
            "Date": row["Date"],
            "FTHG": row["FTHG"],
            "FTAG": row["FTAG"],
        })
    # Convertir les listes en DataFrames une seule fois
    return {k: pd.DataFrame(v) for k, v in index.items()}


def h2h_stats(index_h2h, home_team, away_team, jusqu_a_date):
    """Stats d'historique entre deux équipes (utilise l'index pré-calculé)."""
    cle = frozenset({home_team, away_team})
    past = index_h2h.get(cle)
    if past is None or len(past) == 0:
        return {"H2H_N": 0, "H2H_AvgGoals": None, "H2H_BTTS_pct": None,
                "H2H_O25_pct": None, "H2H_00_pct": None}
    past = past[past["Date"] < jusqu_a_date]
    if len(past) == 0:
        return {"H2H_N": 0, "H2H_AvgGoals": None, "H2H_BTTS_pct": None,
                "H2H_O25_pct": None, "H2H_00_pct": None}
    total = past["FTHG"] + past["FTAG"]
    return {
        "H2H_N": int(len(past)),
        "H2H_AvgGoals": round(total.mean(), 2),
        "H2H_BTTS_pct": round(100 * ((past["FTHG"] > 0) & (past["FTAG"] > 0)).mean(), 1),
        "H2H_O25_pct": round(100 * (total > 2.5).mean(), 1),
        "H2H_00_pct": round(100 * ((past["FTHG"] == 0) & (past["FTAG"] == 0)).mean(), 1),
    }
def detecter_anomalies(stats):
    """
    Compare les stats récentes (5 et 10 derniers) avec la saison entière.
    Retourne (emojis, détails_texte) pour utilisation en tooltip.
    """
    if not stats:
        return "", ""

    SEUIL = 20  # points de pourcentage
    SEUIL_BUTS = 0.6  # buts/match

    signaux = []
    details = []

    # Stats saison
    gf_saison = stats.get("GF_pg")
    ga_saison = stats.get("GA_pg")
    over25_saison = stats.get("Over25_pct")
    btts_saison = stats.get("BTTS_pct")

    # Stats récentes (5 derniers - prioritaires) avec fallback 10 derniers
    gf_recent = stats.get("L5_GF_pg") or stats.get("L10_GF_pg")
    ga_recent = stats.get("L5_GA_pg") or stats.get("L10_GA_pg")
    over25_recent = stats.get("L5_Over25_pct") or stats.get("L10_Over25_pct")
    btts_recent = stats.get("L5_BTTS_pct") or stats.get("L10_BTTS_pct")
    fenetre = "5 derniers" if stats.get("L5_GF_pg") is not None else "10 derniers"

    # 1. Surforme attaque
    if gf_saison is not None and gf_recent is not None:
        if gf_recent - gf_saison >= SEUIL_BUTS:
            signaux.append("📈")
            details.append(f"📈 Surforme attaque : {gf_recent:.1f} buts/m sur {fenetre} vs {gf_saison:.1f} en saison")
        elif gf_saison - gf_recent >= SEUIL_BUTS:
            signaux.append("📉")
            details.append(f"📉 Sousforme attaque : {gf_recent:.1f} buts/m sur {fenetre} vs {gf_saison:.1f} en saison")

    # 2. Surforme/sousforme défense
    if ga_saison is not None and ga_recent is not None:
        if ga_saison - ga_recent >= SEUIL_BUTS:
            signaux.append("🛡️")
            details.append(f"🛡️ Surforme défense : {ga_recent:.1f} encaissés/m sur {fenetre} vs {ga_saison:.1f} en saison")
        elif ga_recent - ga_saison >= SEUIL_BUTS:
            signaux.append("⚠️")
            details.append(f"⚠️ Sousforme défense : {ga_recent:.1f} encaissés/m sur {fenetre} vs {ga_saison:.1f} en saison")

    # 3. Tendance Over/Under
    if over25_saison is not None and over25_recent is not None:
        if over25_recent - over25_saison >= SEUIL:
            signaux.append("🔥")
            details.append(f"🔥 Tendance Over : {over25_recent:.0f}% O2.5 sur {fenetre} vs {over25_saison:.0f}% en saison")
        elif over25_saison - over25_recent >= SEUIL:
            signaux.append("🧊")
            details.append(f"🧊 Tendance Under : {over25_recent:.0f}% O2.5 sur {fenetre} vs {over25_saison:.0f}% en saison")

    # 4. Tendance BTTS
    if btts_saison is not None and btts_recent is not None:
        if btts_recent - btts_saison >= SEUIL:
            signaux.append("💥")
            details.append(f"💥 Tendance BTTS : {btts_recent:.0f}% BTTS sur {fenetre} vs {btts_saison:.0f}% en saison")
        elif btts_saison - btts_recent >= SEUIL:
            signaux.append("🚫")
            details.append(f"🚫 Anti-BTTS : {btts_recent:.0f}% BTTS sur {fenetre} vs {btts_saison:.0f}% en saison")

    # Construire un mini-résumé chiffré pour l'affichage compact
    resume_chiffre = []
    if gf_saison is not None and gf_recent is not None:
        diff_gf = gf_recent - gf_saison
        if abs(diff_gf) >= SEUIL_BUTS:
            signe = "+" if diff_gf > 0 else ""
            resume_chiffre.append(f"{signe}{diff_gf:.1f} BM")
    if ga_saison is not None and ga_recent is not None:
        diff_ga = ga_recent - ga_saison
        if abs(diff_ga) >= SEUIL_BUTS:
            signe = "+" if diff_ga > 0 else ""
            resume_chiffre.append(f"{signe}{diff_ga:.1f} BE")

    affichage_court = "".join(signaux)
    if resume_chiffre:
        affichage_court += " " + " ".join(resume_chiffre)

    return affichage_court, " | ".join(details)
def construire_matchups(df, team_stats):
    index_h2h = construire_index_h2h(df)  # ← AJOUTER CETTE LIGNE
    matchups = []
    for _, row in df.iterrows():
        hk = (row["HomeTeam"], row["DisplayLeague"], row["Season"])
        ak = (row["AwayTeam"], row["DisplayLeague"], row["Season"])
        h = team_stats.get(hk)
        a = team_stats.get(ak)
        if not h or not a:
            continue
        lam_h = h["HomeAttack"] * a["AwayDefense"] * h["_lg_h"]
        lam_a = a["AwayAttack"] * h["HomeDefense"] * a["_lg_a"]
        probs = probs_match(lam_h, lam_a)
        h2h = h2h_stats(index_h2h, row["HomeTeam"], row["AwayTeam"], row["Date"])
# Stats additionnelles si dispo (peuvent être None pour ligues extra)
        h_extra = {
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
        }
        a_extra = {
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
        }
        # Anomalies (forme récente vs saison)
        h_emojis, h_details = detecter_anomalies(h)
        a_emojis, a_details = detecter_anomalies(a)
        matchups.append({
            "Date": row["Date"].strftime("%Y-%m-%d"),
            "DateNY": row["DateNY"],
            "Time": row["Time"] if pd.notna(row["Time"]) else "",
            "TimeNY": row["TimeNY"],
            "League": row["DisplayLeague"],
            "Season": row["Season"],
            "HomeTeam": row["HomeTeam"],
            "AwayTeam": row["AwayTeam"],
            "Score": f"{int(row['FTHG'])}-{int(row['FTAG'])}",
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
            **h_extra,
            **a_extra,
            "H_Signaux": h_emojis,
            "H_Signaux_detail": h_details if h_details else "Aucune anomalie détectée",
            "A_Signaux": a_emojis,
            "A_Signaux_detail": a_details if a_details else "Aucune anomalie détectée",
            **h2h,
        })
    return pd.DataFrame(matchups)

# ============================================================
# 4. ORCHESTRATEUR
# ============================================================
def construire_matchups_avec_historique(df_a_traiter, team_stats, df_historique):
    """
    Construit des matchups pour df_a_traiter, mais utilise df_historique pour calculer le H2H.
    Utile pour les fixtures à venir : on veut le H2H basé sur tous les matchs joués.
    """
    index_h2h = construire_index_h2h(df_historique)
    matchups = []
    for _, row in df_a_traiter.iterrows():
        hk = (row["HomeTeam"], row["DisplayLeague"], row["Season"])
        ak = (row["AwayTeam"], row["DisplayLeague"], row["Season"])
        h = team_stats.get(hk)
        a = team_stats.get(ak)
        if not h or not a:
            continue
        lam_h = h["HomeAttack"] * a["AwayDefense"] * h["_lg_h"]
        lam_a = a["AwayAttack"] * h["HomeDefense"] * a["_lg_a"]
        probs = probs_match(lam_h, lam_a)
        h2h = h2h_stats(index_h2h, row["HomeTeam"], row["AwayTeam"], row["Date"])
# Stats additionnelles si dispo (peuvent être None pour ligues extra)
        h_extra = {
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
        }
        a_extra = {
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
        }
        # Anomalies (forme récente vs saison)
        h_emojis, h_details = detecter_anomalies(h)
        a_emojis, a_details = detecter_anomalies(a)
        matchups.append({
            "Date": row["Date"].strftime("%Y-%m-%d"),
            "DateNY": row["DateNY"],
            "Time": row["Time"] if pd.notna(row["Time"]) else "",
            "TimeNY": row["TimeNY"],
            "League": row["DisplayLeague"],
            "Season": row["Season"],
            "HomeTeam": row["HomeTeam"],
            "AwayTeam": row["AwayTeam"],
            "Score": f"{int(row['FTHG'])}-{int(row['FTAG'])}",
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
            **h_extra,
            **a_extra,
            "H_Signaux": h_emojis,
            "H_Signaux_detail": h_details if h_details else "Aucune anomalie détectée",
            "A_Signaux": a_emojis,
            "A_Signaux_detail": a_details if a_details else "Aucune anomalie détectée",
            **h2h,
        })
    return pd.DataFrame(matchups)
def charger_fixtures_a_venir(chemin_fixtures, df_historique, stats_ref):
    """
    Charge les fixtures à venir et les transforme en matchups,
    en réutilisant les stats d'équipes (calculées sur les matchs joués).
    """
    from pathlib import Path
    if not Path(chemin_fixtures).exists():
        return pd.DataFrame()

    fx = pd.read_csv(chemin_fixtures)
    if len(fx) == 0:
        return pd.DataFrame()

    # Harmoniser pour pouvoir passer dans construire_matchups
    fx["Date"] = pd.to_datetime(fx["Date"], errors="coerce")
    fx = fx.dropna(subset=["Date"])

    # Appliquer le drapeau aux noms de ligues
    def designer(row):
        code = CODES_PAYS.get(row["Country"], row["Country"][:3].upper())
        return f"[{code}] {row['LeagueName']}"
    fx["DisplayLeague"] = fx.apply(designer, axis=1)

    # Inférer la saison
    fx["Season"] = fx.apply(lambda r: inferer_saison(r["League"], r["Date"]), axis=1)

    # Heures NY
    uk_tz = ZoneInfo("Europe/London")
    ny_tz = ZoneInfo("America/New_York")
    def vers_ny(date, heure, fmt):
        if pd.isna(heure) or not heure or pd.isna(date):
            return date.strftime("%Y-%m-%d") if fmt == "%Y-%m-%d" else ""
        try:
            # football-data.org renvoie en UTC, pas UK
            dt = datetime.strptime(f"{date.strftime('%Y-%m-%d')} {heure}", "%Y-%m-%d %H:%M").replace(tzinfo=ZoneInfo("UTC"))
            return dt.astimezone(ny_tz).strftime(fmt)
        except Exception:
            return heure if fmt != "%Y-%m-%d" else date.strftime("%Y-%m-%d")
    fx["TimeNY"] = fx.apply(lambda r: vers_ny(r["Date"], r["Time"], "%H:%M"), axis=1)
    fx["DateNY"] = fx.apply(lambda r: vers_ny(r["Date"], r["Time"], "%Y-%m-%d"), axis=1)
    fx["IsUpcoming"] = True

    # Faire passer ces fixtures dans la même machinerie que les matchs joués
    # On met des valeurs bidon pour FTHG/FTAG (ne seront pas affichées)
    fx["FTHG"] = 0
    fx["FTAG"] = 0
    # Utiliser l'historique complet (df_historique) pour le H2H, pas juste les fixtures
    matchups_fx = construire_matchups_avec_historique(fx, stats_ref, df_historique)
    if len(matchups_fx) > 0:
        matchups_fx["Score"] = "À VENIR"
        matchups_fx["IsUpcoming"] = True
    return matchups_fx

def calculer_tout(chemin_csv, chemin_fixtures=None):
    df = charger_et_preparer(chemin_csv)
    stats = calculer_team_stats(df)
    team_df = pd.DataFrame([{k: v for k, v in s.items() if not k.startswith("_")}
                            for s in stats.values()])

    # Matchups des matchs joués
    matchups_df = construire_matchups(df, stats)
    matchups_df["IsUpcoming"] = False

    # Ajouter les fixtures à venir si le fichier existe
    if chemin_fixtures:
        matchups_fx = charger_fixtures_a_venir(chemin_fixtures, df, stats)
        if len(matchups_fx) > 0:
            matchups_df = pd.concat([matchups_df, matchups_fx], ignore_index=True)
            print(f"  ➕ {len(matchups_fx)} matchs à venir ajoutés aux matchups")

    courante = df.sort_values("Date").groupby("DisplayLeague").tail(1).set_index("DisplayLeague")["Season"].to_dict()
    return {
        "df": df,
        "team_stats": team_df,
        "matchups": matchups_df,
        "saison_courante": courante,
    }
    # ============================================================
# 5. VALIDATION POISSON (compare prédictions vs résultats réels)
# ============================================================

def calculer_validation_poisson(matchups_df):
    """
    Filtre aux matchs joués et ajoute des colonnes Real_* (0/1) pour chaque marché.
    """
    df = matchups_df.copy()
    if "IsUpcoming" in df.columns:
        df = df[df["IsUpcoming"] != True]

    def parse_score(s):
        try:
            h, a = str(s).split("-")
            return int(h), int(a)
        except Exception:
            return None, None

    parsed = df["Score"].apply(parse_score)
    df["Actual_H"] = [p[0] for p in parsed]
    df["Actual_A"] = [p[1] for p in parsed]
    df = df.dropna(subset=["Actual_H", "Actual_A"]).copy()
    df["Actual_H"] = df["Actual_H"].astype(int)
    df["Actual_A"] = df["Actual_A"].astype(int)
    df["Actual_Total"] = df["Actual_H"] + df["Actual_A"]

    df["Real_Over05"] = (df["Actual_Total"] >= 1).astype(int)
    df["Real_Over15"] = (df["Actual_Total"] >= 2).astype(int)
    df["Real_Over25"] = (df["Actual_Total"] >= 3).astype(int)
    df["Real_BTTS"] = ((df["Actual_H"] > 0) & (df["Actual_A"] > 0)).astype(int)
    df["Real_00"] = ((df["Actual_H"] == 0) & (df["Actual_A"] == 0)).astype(int)
    return df


def metriques_calibration(df_validation):
    """
    Pour chaque marché, calcule : taux prédit moyen, taux réel, écart, Brier, accuracy.
    """
    marches = [
        ("Over 0.5", "P_Over05", "Real_Over05"),
        ("Over 1.5", "P_Over15", "Real_Over15"),
        ("Over 2.5", "P_Over25", "Real_Over25"),
        ("BTTS",     "P_BTTS",   "Real_BTTS"),
        ("0-0",      "P_00",     "Real_00"),
    ]
    rows = []
    for nom, col_pred, col_real in marches:
        if col_pred not in df_validation.columns or col_real not in df_validation.columns:
            continue
        sub = df_validation[[col_pred, col_real]].dropna()
        if len(sub) == 0:
            continue
        pred = sub[col_pred] / 100.0   # convertir % en proba [0,1]
        real = sub[col_real]
        brier = ((pred - real) ** 2).mean()
        accuracy = ((pred > 0.5).astype(int) == real).mean()
        rows.append({
            "Marché": nom,
            "N matchs": int(len(sub)),
            "% prédit moy": round(100 * pred.mean(), 1),
            "% réel": round(100 * real.mean(), 1),
            "Écart (pp)": round(100 * (pred.mean() - real.mean()), 1),
            "Brier": round(brier, 4),
            "Accuracy": round(100 * accuracy, 1),
        })
    return pd.DataFrame(rows)


def calibration_par_buckets(df_validation, col_pred, col_real):
    """
    Découpe les prédictions en tranches fixes de 10 points et compare au réel.
    """
    sub = df_validation[[col_pred, col_real]].dropna().copy()
    if len(sub) == 0:
        return pd.DataFrame()
    bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100.01]
    labels = ["0-10%", "10-20%", "20-30%", "30-40%", "40-50%",
              "50-60%", "60-70%", "70-80%", "80-90%", "90-100%"]
    sub["Tranche"] = pd.cut(sub[col_pred], bins=bins, labels=labels, include_lowest=True)
    agg = sub.groupby("Tranche", observed=True).agg(
        N=(col_pred, "size"),
        Pred_moyen=(col_pred, "mean"),
        Real_pct=(col_real, "mean"),
    ).reset_index()
    agg["Pred_moyen"] = agg["Pred_moyen"].round(1)
    agg["Real_pct"] = (agg["Real_pct"] * 100).round(1)
    agg["Écart (pp)"] = (agg["Pred_moyen"] - agg["Real_pct"]).round(1)
    return agg.rename(columns={"Pred_moyen": "% prédit moy", "Real_pct": "% réel"})


def plus_grandes_surprises(df_validation, col_pred, col_real, n=10):
    """
    Renvoie les n matchs où la prédiction était la plus loin du résultat (en pp).
    """
    df = df_validation.copy()
    df["Écart (pp)"] = (df[col_pred] - df[col_real] * 100).round(1)
    df = df.reindex(df["Écart (pp)"].abs().sort_values(ascending=False).index).head(n)
    cols = ["Date", "League", "HomeTeam", "AwayTeam", "Score", col_pred, col_real, "Écart (pp)"]
    cols = [c for c in cols if c in df.columns]
    return df[cols].rename(columns={col_pred: "% prédit", col_real: "Réel (0/1)"})