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
        if row["LeagueName"] in ambigus:
            return f"{row['LeagueName']} ({PAYS_COURT.get(row['Country'], row['Country'][:3].upper())})"
        return row["LeagueName"]
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

    return df

# ============================================================
# 2. STATS PAR ÉQUIPE
# ============================================================

def construire_team_rows(df):
    home = df[["League", "DisplayLeague", "Season", "Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG"]].rename(
        columns={"HomeTeam": "Team", "AwayTeam": "Opponent", "FTHG": "GF", "FTAG": "GA"}
    )
    home["Venue"] = "H"
    away = df[["League", "DisplayLeague", "Season", "Date", "AwayTeam", "HomeTeam", "FTAG", "FTHG"]].rename(
        columns={"AwayTeam": "Team", "HomeTeam": "Opponent", "FTAG": "GF", "FTHG": "GA"}
    )
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
            "HomeAttack": round(home_attack, 2), "HomeDefense": round(home_defense, 2),
            "AwayAttack": round(away_attack, 2), "AwayDefense": round(away_defense, 2),
            "xG_home": round(home_attack * lg_h, 2),
            "xG_away": round(away_attack * lg_a, 2),
            "_lg_h": lg_h, "_lg_a": lg_a,
        }
    return stats

# ============================================================
# 3. PROBABILITÉS POISSON ET MATCHUPS
# ============================================================

def poisson_pmf(k, lam):
    if lam <= 0:
        return 1.0 if k == 0 else 0.0
    return (lam ** k * math.exp(-lam)) / math.factorial(k)

def probs_match(lam_h, lam_a, max_g=10):
    p = {"p00": 0, "over05": 0, "over15": 0, "over25": 0, "btts": 0}
    for i in range(max_g):
        for j in range(max_g):
            pr = poisson_pmf(i, lam_h) * poisson_pmf(j, lam_a)
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

def h2h_stats(df, home_team, away_team, jusqu_a_date):
    masque_duel = (((df["HomeTeam"] == home_team) & (df["AwayTeam"] == away_team)) |
                   ((df["HomeTeam"] == away_team) & (df["AwayTeam"] == home_team)))
    past = df[masque_duel & (df["Date"] < jusqu_a_date)]
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

def construire_matchups(df, team_stats):
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
        h2h = h2h_stats(df, row["HomeTeam"], row["AwayTeam"], row["Date"])

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
            **h2h,
        })
    return pd.DataFrame(matchups)

# ============================================================
# 4. ORCHESTRATEUR
# ============================================================

def calculer_tout(chemin_csv):
    df = charger_et_preparer(chemin_csv)
    stats = calculer_team_stats(df)
    team_df = pd.DataFrame([{k: v for k, v in s.items() if not k.startswith("_")}
                            for s in stats.values()])
    matchups_df = construire_matchups(df, stats)
    courante = df.sort_values("Date").groupby("DisplayLeague").tail(1).set_index("DisplayLeague")["Season"].to_dict()
    return {
        "df": df,
        "team_stats": team_df,
        "matchups": matchups_df,
        "saison_courante": courante,
    }