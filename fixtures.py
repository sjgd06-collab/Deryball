"""
Module de récupération des matchs à venir via api-football (api-sports.io).
Utilise le plan gratuit (100 requêtes/jour) de manière économe.

Usage :
    from fixtures import recuperer_fixtures_a_venir
    df_fixtures = recuperer_fixtures_a_venir(jours=10)
"""
import os
import requests
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path

# ============================================================
# CONFIGURATION
# ============================================================

# Clé API : récupérée depuis la variable d'environnement API_FOOTBALL_KEY
# (définie en local via un fichier .env ou sur GitHub via Secrets)
API_KEY = os.environ.get("API_FOOTBALL_KEY", "")

# URL de base
BASE_URL = "https://v3.football.api-sports.io"
HEADERS = {
    "x-rapidapi-host": "v3.football.api-sports.io",
    "x-rapidapi-key": API_KEY,
}

# ============================================================
# MAPPAGE LIGUES : code interne → (api-football league_id, saison, nom, pays)
# ============================================================
# Saison : api-football utilise l'année de début pour les ligues européennes
# (2025 = 2025-26), et l'année courante pour les ligues en année civile.
#
# Pour vérifier/mettre à jour les IDs :
# https://dashboard.api-football.com/soccer/ids

LIGUES_APIFOOTBALL = {
    # Ligues européennes (saison 2025-26 = 2025)
    "E0":  {"id": 39,  "season": 2025, "name": "Premier League",  "country": "England"},
    "D1":  {"id": 78,  "season": 2025, "name": "Bundesliga",      "country": "Germany"},
    "D2":  {"id": 79,  "season": 2025, "name": "2. Bundesliga",   "country": "Germany"},
    "I1":  {"id": 135, "season": 2025, "name": "Serie A",         "country": "Italy"},
    "SP1": {"id": 140, "season": 2025, "name": "La Liga",         "country": "Spain"},
    "F1":  {"id": 61,  "season": 2025, "name": "Ligue 1",         "country": "France"},
    "N1":  {"id": 88,  "season": 2025, "name": "Eredivisie",      "country": "Netherlands"},
    "P1":  {"id": 94,  "season": 2025, "name": "Primeira Liga",   "country": "Portugal"},
    "T1":  {"id": 203, "season": 2025, "name": "Super Lig",       "country": "Turkey"},
    "G1":  {"id": 197, "season": 2025, "name": "Super League",    "country": "Greece"},
    "SC0": {"id": 179, "season": 2025, "name": "Premiership",     "country": "Scotland"},
    "AUT": {"id": 218, "season": 2025, "name": "Bundesliga",      "country": "Austria"},
    "POL": {"id": 106, "season": 2025, "name": "Ekstraklasa",     "country": "Poland"},
    "SWZ": {"id": 207, "season": 2025, "name": "Super League",    "country": "Switzerland"},
    # Ligues en année civile 2026
    "ARG": {"id": 128, "season": 2026, "name": "Liga Profesional", "country": "Argentina"},
    "BRA": {"id": 71,  "season": 2026, "name": "Serie A",          "country": "Brazil"},
    "MEX": {"id": 262, "season": 2026, "name": "Liga MX",          "country": "Mexico"},
    "NOR": {"id": 103, "season": 2026, "name": "Eliteserien",      "country": "Norway"},
    "USA": {"id": 253, "season": 2026, "name": "MLS",              "country": "USA"},
}


# ============================================================
# CACHE LOCAL (pour économiser les requêtes)
# ============================================================
CACHE_DIR = Path("data/cache")
CACHE_DUREE_HEURES = 12

def _cache_valide(chemin_cache):
    """Vrai si le fichier cache existe et est récent."""
    if not chemin_cache.exists():
        return False
    age_minutes = (datetime.now().timestamp() - chemin_cache.stat().st_mtime) / 60
    return age_minutes < (CACHE_DUREE_HEURES * 60)


# ============================================================
# FONCTIONS API
# ============================================================

def _appel_api(endpoint, params=None):
    """Fait un appel API et retourne la réponse JSON."""
    if not API_KEY:
        raise RuntimeError("API_FOOTBALL_KEY non définie dans l'environnement.")
    url = f"{BASE_URL}/{endpoint}"
    r = requests.get(url, headers=HEADERS, params=params, timeout=30)
    r.raise_for_status()
    data = r.json()
    # Vérifier les erreurs de l'API
    if data.get("errors") and isinstance(data["errors"], dict) and len(data["errors"]) > 0:
        print(f"  ⚠️  Erreur API : {data['errors']}")
    # Log du quota restant (si fourni)
    reste = r.headers.get("x-ratelimit-requests-remaining")
    if reste:
        print(f"    (quota restant aujourd'hui : {reste})")
    return data


def _fixtures_par_ligue(code, info_ligue, date_debut, date_fin):
    """Récupère les fixtures d'une ligue entre 2 dates. Utilise le cache si disponible."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_path = CACHE_DIR / f"fixtures_{code}.json"

    # Vérifier le cache
    if _cache_valide(cache_path):
        print(f"  • {code} ({info_ligue['name']})... 📦 cache")
        return pd.read_json(cache_path, orient="records")

    # Appel API
    print(f"  • {code} ({info_ligue['name']})...", end=" ")
    try:
        data = _appel_api("fixtures", params={
            "league": info_ligue["id"],
            "season": info_ligue["season"],
            "from": date_debut.strftime("%Y-%m-%d"),
            "to": date_fin.strftime("%Y-%m-%d"),
        })
    except Exception as e:
        print(f"✗ {e}")
        return pd.DataFrame()

    # Filtrer : on veut seulement les matchs non joués (status "Not Started" = NS, TBD = To Be Defined)
    # Les statuses "finis" sont FT, AET, PEN. On les ignore car ils sont dans football-data.
    matches = data.get("response", [])
    rows = []
    for m in matches:
        status = m["fixture"]["status"]["short"]
        if status in ("FT", "AET", "PEN"):
            continue  # match fini, on le laisse à football-data
        # Les statuses intéressants : NS (not started), TBD, PST (postponed), CANC
        if status not in ("NS", "TBD", "PST"):
            continue
        rows.append({
            "League": code,
            "LeagueName": info_ligue["name"],
            "Country": info_ligue["country"],
            "Season": f"{info_ligue['season']}-{str(info_ligue['season']+1)[2:]}" if info_ligue['season'] < 2100 else str(info_ligue['season']),
            "Date": m["fixture"]["date"][:10],  # YYYY-MM-DD
            "Time": m["fixture"]["date"][11:16],  # HH:MM (UTC)
            "HomeTeam": m["teams"]["home"]["name"],
            "AwayTeam": m["teams"]["away"]["name"],
            "FTHG": None,  # pas encore joué
            "FTAG": None,
            "FTR": None,
            "Status": status,
            "IsUpcoming": True,
        })
    df = pd.DataFrame(rows)
    print(f"✓ {len(df)} matchs à venir")

    # Sauvegarder dans le cache
    if len(df) > 0:
        df.to_json(cache_path, orient="records", date_format="iso")
    else:
        # Cache vide quand même, pour éviter de re-requêter
        pd.DataFrame().to_json(cache_path, orient="records")
    return df


def recuperer_fixtures_a_venir(jours=10):
    """
    Récupère les matchs à venir dans les `jours` prochains, pour toutes les ligues
    configurées dans LIGUES_APIFOOTBALL. Retourne un DataFrame unique.
    """
    if not API_KEY:
        print("⚠️  API_FOOTBALL_KEY non définie. Aucune fixture récupérée.")
        return pd.DataFrame()

    date_debut = datetime.utcnow().date()
    date_fin = date_debut + timedelta(days=jours)

    print(f"\n📥 Récupération des matchs à venir ({date_debut} → {date_fin})...")
    tous = []
    for code, info in LIGUES_APIFOOTBALL.items():
        df = _fixtures_par_ligue(code, info, date_debut, date_fin)
        if len(df) > 0:
            tous.append(df)

    if not tous:
        print("\n(aucun match à venir trouvé)")
        return pd.DataFrame()

    df_all = pd.concat(tous, ignore_index=True)
    print(f"\n✅ Total : {len(df_all)} matchs à venir toutes ligues confondues")
    return df_all


# ============================================================
# TEST EN LIGNE DE COMMANDE
# ============================================================
if __name__ == "__main__":
    df = recuperer_fixtures_a_venir(jours=10)
    if len(df) > 0:
        print("\nAperçu :")
        print(df.head(10).to_string(index=False))