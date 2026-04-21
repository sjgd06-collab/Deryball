"""
Module de récupération des matchs à venir via football-data.org.
Plan gratuit : 12 compétitions majeures, 10 requêtes/minute.

Usage :
    from fixtures import recuperer_fixtures_a_venir
    df_fixtures = recuperer_fixtures_a_venir(jours=10)
"""
import os
import time
import requests
import pandas as pd
from datetime import datetime, timedelta, timezone
from pathlib import Path
from dotenv import load_dotenv
# Import du mapping des noms d'équipes
try:
    from equipes_mapping import MAPPING_EQUIPES
except ImportError:
    MAPPING_EQUIPES = {}
# Charger le .env (en local uniquement ; en prod c'est GitHub Secrets)
load_dotenv()

# ============================================================
# CONFIGURATION
# ============================================================
API_KEY = os.environ.get("FOOTBALL_DATA_KEY", "")
BASE_URL = "https://api.football-data.org/v4"
HEADERS = {"X-Auth-Token": API_KEY}

# ============================================================
# MAPPAGE DES COMPÉTITIONS
# Clés = nos codes internes (comme dans football-data.co.uk)
# Valeurs = (code football-data.org, nom affiché, pays)
# ============================================================
COMPETITIONS = {
    # Nos ligues actuelles disponibles dans le plan gratuit
    "E0":  {"code": "PL",  "name": "Premier League",   "country": "England"},
    "D1":  {"code": "BL1", "name": "Bundesliga",       "country": "Germany"},
    "I1":  {"code": "SA",  "name": "Serie A",          "country": "Italy"},
    "SP1": {"code": "PD",  "name": "La Liga",          "country": "Spain"},
    "F1":  {"code": "FL1", "name": "Ligue 1",          "country": "France"},
    "N1":  {"code": "DED", "name": "Eredivisie",       "country": "Netherlands"},
    "P1":  {"code": "PPL", "name": "Primeira Liga",    "country": "Portugal"},
    "BRA": {"code": "BSA", "name": "Serie A",          "country": "Brazil"},
    # Bonus non couverts par football-data.co.uk
    "CL":  {"code": "CL",  "name": "Champions League", "country": "UEFA"},
    "ELC": {"code": "ELC", "name": "Championship",     "country": "England"},
}

# ============================================================
# CACHE LOCAL (pour économiser les requêtes)
# ============================================================
CACHE_DIR = Path("data/cache")
CACHE_DUREE_HEURES = 12


def _cache_valide(chemin):
    if not chemin.exists():
        return False
    age_min = (datetime.now().timestamp() - chemin.stat().st_mtime) / 60
    return age_min < (CACHE_DUREE_HEURES * 60)


# ============================================================
# FONCTIONS
# ============================================================
def _appel_api(endpoint, params=None):
    """Appel API avec gestion basique des erreurs."""
    if not API_KEY:
        raise RuntimeError("FOOTBALL_DATA_KEY non définie dans l'environnement.")
    url = f"{BASE_URL}/{endpoint}"
    r = requests.get(url, headers=HEADERS, params=params, timeout=30)
    if r.status_code == 429:
        # Rate limit dépassé : attendre et retenter 1x
        print("    ⏸️  Rate limit atteint, pause de 60s...")
        time.sleep(60)
        r = requests.get(url, headers=HEADERS, params=params, timeout=30)
    r.raise_for_status()
    return r.json()


def _fixtures_competition(code_interne, info, date_debut, date_fin):
    """Récupère les fixtures d'une compétition entre 2 dates."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_path = CACHE_DIR / f"fixtures_{code_interne}.json"

    if _cache_valide(cache_path):
        print(f"  • {code_interne} ({info['name']})... 📦 cache")
        return pd.read_json(cache_path, orient="records")

    print(f"  • {code_interne} ({info['name']})...", end=" ")
    try:
        data = _appel_api(
            f"competitions/{info['code']}/matches",
            params={
                "status": "SCHEDULED",
                "dateFrom": date_debut.strftime("%Y-%m-%d"),
                "dateTo": date_fin.strftime("%Y-%m-%d"),
            },
        )
    except Exception as e:
        print(f"✗ {e}")
        return pd.DataFrame()

    matches = data.get("matches", [])
    rows = []
    for m in matches:
        # Date UTC depuis l'API
        utc_date = m["utcDate"]  # format ISO: 2026-04-25T14:00:00Z
        rows.append({
            "League": code_interne,
            "LeagueName": info["name"],
            "Country": info["country"],
            "Date": utc_date[:10],      # YYYY-MM-DD
            "Time": utc_date[11:16],    # HH:MM (UTC)
            "HomeTeam": MAPPING_EQUIPES.get(m["homeTeam"]["name"], m["homeTeam"]["name"]),
            "AwayTeam": MAPPING_EQUIPES.get(m["awayTeam"]["name"], m["awayTeam"]["name"]),
            "FTHG": None,
            "FTAG": None,
            "FTR": None,
            "Status": m["status"],
            "IsUpcoming": True,
        })

    df = pd.DataFrame(rows)
    print(f"✓ {len(df)} matchs à venir")

    # Sauvegarder le cache (même vide pour éviter de re-requêter)
    df.to_json(cache_path, orient="records", date_format="iso")

    # Petite pause pour respecter la limite de 10 req/min (6s entre requêtes = safe)
    time.sleep(7)

    return df


def recuperer_fixtures_a_venir(jours=10):
    """
    Récupère les matchs à venir dans les `jours` prochains pour toutes les compétitions.
    Retourne un DataFrame unique.
    """
    if not API_KEY:
        print("⚠️  FOOTBALL_DATA_KEY non définie. Aucune fixture récupérée.")
        return pd.DataFrame()

    date_debut = datetime.now(timezone.utc).date()
    date_fin = date_debut + timedelta(days=jours)

    print(f"\n📥 Récupération des matchs à venir ({date_debut} → {date_fin})...")
    tous = []
    for code, info in COMPETITIONS.items():
        df = _fixtures_competition(code, info, date_debut, date_fin)
        if len(df) > 0:
            tous.append(df)

    if not tous:
        print("\n(aucun match à venir trouvé)")
        return pd.DataFrame()

    df_all = pd.concat(tous, ignore_index=True)
    print(f"\n✅ Total : {len(df_all)} matchs à venir, toutes compétitions confondues")
    return df_all


# ============================================================
# TEST EN LIGNE DE COMMANDE
# ============================================================
if __name__ == "__main__":
    df = recuperer_fixtures_a_venir(jours=10)
    if len(df) > 0:
        print("\nAperçu :")
        print(df.head(10).to_string(index=False))