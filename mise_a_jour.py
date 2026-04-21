"""
Script de mise à jour automatique des données Deryball.
Télécharge les CSVs de football-data.co.uk pour chaque ligue suivie,
les combine en un seul fichier, et le sauvegarde dans data/.

Ce script est exécuté automatiquement par GitHub Actions chaque jour.
"""
import pandas as pd
import requests
from io import StringIO
from pathlib import Path
from datetime import datetime

# ============================================================
# CONFIGURATION DES LIGUES SUIVIES
# ============================================================
# Format : (code_ligue, nom_ligue, pays, saison_url)
# saison_url est le code 4 chiffres pour l'URL : "2526" = saison 2025-26
LIGUES = [
    # Ligues européennes (saison 2025-26)
    ("E0",  "Premier League",  "England",     "2526"),
    ("D1",  "Bundesliga",      "Germany",     "2526"),
    ("D2",  "2. Bundesliga",   "Germany",     "2526"),
    ("I1",  "Serie A",         "Italy",       "2526"),
    ("SP1", "La Liga",         "Spain",       "2526"),
    ("F1",  "Ligue 1",         "France",      "2526"),
    ("N1",  "Eredivisie",      "Netherlands", "2526"),
    ("P1",  "Primeira Liga",   "Portugal",    "2526"),
    ("T1",  "Super Lig",       "Turkey",      "2526"),
    ("G1",  "Super League",    "Greece",      "2526"),
    ("SC0", "Premiership",     "Scotland",    "2526"),
]

# Ligues en "format extra" (calendrier civil, autre URL)
LIGUES_EXTRA = [
    # (code, nom, pays)
    ("ARG", "Liga Profesional", "Argentina"),
    ("AUT", "Bundesliga",       "Austria"),
    ("BRA", "Serie A",          "Brazil"),
    ("MEX", "Liga MX",          "Mexico"),
    ("NOR", "Eliteserien",      "Norway"),
    ("POL", "Ekstraklasa",      "Poland"),
    ("SWZ", "Super League",     "Switzerland"),
    ("USA", "MLS",              "USA"),
]

BASE_URL_MAIN = "https://www.football-data.co.uk/mmz4281"
BASE_URL_EXTRA = "https://www.football-data.co.uk/new"

FICHIER_SORTIE = Path("data/All_Leagues_2025-26.csv")


def telecharger_csv_principal(code, saison):
    """Télécharge un CSV de ligue européenne."""
    url = f"{BASE_URL_MAIN}/{saison}/{code}.csv"
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        # football-data.co.uk utilise parfois latin-1
        try:
            return pd.read_csv(StringIO(r.content.decode("utf-8")))
        except UnicodeDecodeError:
            return pd.read_csv(StringIO(r.content.decode("latin-1")))
    except Exception as e:
        print(f"  ⚠️  Erreur pour {code}: {e}")
        return None


def telecharger_csv_extra(code):
    """Télécharge un CSV de ligue 'extra' (calendrier civil)."""
    url = f"{BASE_URL_EXTRA}/{code}.csv"
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        try:
            return pd.read_csv(StringIO(r.content.decode("utf-8")))
        except UnicodeDecodeError:
            return pd.read_csv(StringIO(r.content.decode("latin-1")))
    except Exception as e:
        print(f"  ⚠️  Erreur pour {code}: {e}")
        return None


def normaliser_principal(df, code, nom, pays):
    """Harmonise les colonnes d'une ligue principale."""
    if df is None or len(df) == 0:
        return None
    df = df.copy()
    # Noms de colonnes attendus par Deryball
    df["League"] = code
    df["LeagueName"] = nom
    df["Country"] = pays
    df["Season"] = "2025-26"
    # Convertir Date au format ISO (football-data.co.uk utilise DD/MM/YYYY)
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce").dt.strftime("%Y-%m-%d")
    # Calculer TotalGoals et Is_00
    if "FTHG" in df.columns and "FTAG" in df.columns:
        df["TotalGoals"] = df["FTHG"] + df["FTAG"]
        df["Is_00"] = (df["FTHG"] == 0) & (df["FTAG"] == 0)
    # Garder uniquement les colonnes utiles
    cols_voulues = ["League", "LeagueName", "Country", "Season", "Date", "Time",
                    "HomeTeam", "AwayTeam", "FTHG", "FTAG", "FTR",
                    "HTHG", "HTAG", "TotalGoals", "Is_00",
                    "AvgCH", "AvgCD", "AvgCA", "AvgC>2.5", "AvgC<2.5"]
    cols_existantes = [c for c in cols_voulues if c in df.columns]
    df = df[cols_existantes].copy()
    # Renommer pour coller au format All_Leagues
    df = df.rename(columns={"AvgC>2.5": "AvgCOver25", "AvgC<2.5": "AvgCUnder25"})
    return df


def normaliser_extra(df, code, nom, pays):
    """Harmonise les colonnes d'une ligue extra."""
    if df is None or len(df) == 0:
        return None
    df = df.copy()
    # Les fichiers extra utilisent Home/Away/HG/AG/Res
    mapping = {
        "Home": "HomeTeam", "Away": "AwayTeam",
        "HG": "FTHG", "AG": "FTAG", "Res": "FTR",
    }
    for old, new in mapping.items():
        if old in df.columns and new not in df.columns:
            df = df.rename(columns={old: new})
    df["League"] = code
    df["LeagueName"] = nom
    df["Country"] = pays
    # Season reste tel quel s'il existe
    if "Season" not in df.columns:
        df["Season"] = ""
    # Convertir Date
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce").dt.strftime("%Y-%m-%d")
    # TotalGoals et Is_00
    if "FTHG" in df.columns and "FTAG" in df.columns:
        df["TotalGoals"] = df["FTHG"] + df["FTAG"]
        df["Is_00"] = (df["FTHG"] == 0) & (df["FTAG"] == 0)
    # Harmoniser les colonnes de cotes
    cote_map = {"AvgCH": "AvgCH", "AvgCD": "AvgCD", "AvgCA": "AvgCA"}
    cols_voulues = ["League", "LeagueName", "Country", "Season", "Date", "Time",
                    "HomeTeam", "AwayTeam", "FTHG", "FTAG", "FTR",
                    "HTHG", "HTAG", "TotalGoals", "Is_00",
                    "AvgCH", "AvgCD", "AvgCA"]
    cols_existantes = [c for c in cols_voulues if c in df.columns]
    df = df[cols_existantes].copy()
    # Pour les extras, pas de AvgCOver25/Under25 directs — on les laisse vides
    df["AvgCOver25"] = None
    df["AvgCUnder25"] = None
    return df


def main():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Début de la mise à jour Deryball")
    tous_les_df = []

    print("\n📥 Téléchargement des ligues principales...")
    for code, nom, pays, saison in LIGUES:
        print(f"  • {code} ({nom}, {pays})...", end=" ")
        df = telecharger_csv_principal(code, saison)
        df_norm = normaliser_principal(df, code, nom, pays)
        if df_norm is not None:
            print(f"✓ {len(df_norm)} matchs")
            tous_les_df.append(df_norm)
        else:
            print("✗")

    print("\n📥 Téléchargement des ligues extra...")
    for code, nom, pays in LIGUES_EXTRA:
        print(f"  • {code} ({nom}, {pays})...", end=" ")
        df = telecharger_csv_extra(code)
        df_norm = normaliser_extra(df, code, nom, pays)
        if df_norm is not None:
            print(f"✓ {len(df_norm)} matchs")
            tous_les_df.append(df_norm)
        else:
            print("✗")

    if not tous_les_df:
        print("\n❌ Aucune donnée téléchargée. Abandon.")
        return

    # Combiner tout
    df_combine = pd.concat(tous_les_df, ignore_index=True)
    # Nettoyer : retirer les lignes sans Date ou sans équipes
    df_combine = df_combine.dropna(subset=["Date", "HomeTeam", "AwayTeam"])
    # Filtrer pour ne garder que les 2 dernières saisons (2024-25 et 2025-26)
    df_combine["Date_dt"] = pd.to_datetime(df_combine["Date"], errors="coerce")
    df_combine = df_combine.dropna(subset=["Date_dt"])
    # On garde tout ce qui est à partir du 1er juillet 2024
    df_combine = df_combine[df_combine["Date_dt"] >= "2024-07-01"]
    df_combine = df_combine.drop(columns=["Date_dt"])
    print(f"\n🔍 Filtrage : conservation des saisons 2024-25 et 2025-26 uniquement")
    print(f"   Matchs après filtrage : {len(df_combine)}")
    # Créer le dossier data si nécessaire
    FICHIER_SORTIE.parent.mkdir(parents=True, exist_ok=True)

    # Sauvegarder
    df_combine.to_csv(FICHIER_SORTIE, index=False)
    print(f"\n✅ Sauvegardé : {FICHIER_SORTIE}")
    print(f"   Total : {len(df_combine)} matchs, {df_combine['League'].nunique()} ligues")
    print(f"   Période : {df_combine['Date'].min()} → {df_combine['Date'].max()}")
# ============================================================
    # RÉCUPÉRATION DES FIXTURES À VENIR (via football-data.org)
    # ============================================================
    try:
        from fixtures import recuperer_fixtures_a_venir
        df_fixtures = recuperer_fixtures_a_venir(jours=10)
        if len(df_fixtures) > 0:
            fichier_fixtures = Path("data/fixtures_a_venir.csv")
            df_fixtures.to_csv(fichier_fixtures, index=False)
            print(f"\n✅ Fixtures sauvegardés : {fichier_fixtures}")
            print(f"   Total : {len(df_fixtures)} matchs à venir")
        else:
            print("\n(aucun fixture à venir récupéré)")
    except Exception as e:
        print(f"\n⚠️  Erreur lors de la récupération des fixtures : {e}")
        print("   (Deryball continuera avec seulement les données football-data.co.uk)")

if __name__ == "__main__":
    main()