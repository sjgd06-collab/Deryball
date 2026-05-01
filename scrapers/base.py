"""
Utilitaires partages entre tous les scrapers Deryball.

Fournit :
  - fetch() : telecharge une URL avec rate limit, user-agent, retry
  - load_cache() / save_cache() : cache local pour eviter re-fetch
  - safe_get_text() : extraction sure d'un attribut BeautifulSoup
"""

import time
import json
import requests
from pathlib import Path
from datetime import datetime

USER_AGENT = "Deryball/1.0 (personal football stats project)"
RATE_LIMIT_SECONDS = 1.0  # 1 seconde entre requetes (poli)
CACHE_DIR = Path("data/scraped/_cache")

_last_request_time = [0.0]  # liste pour mutabilite dans la fonction


def fetch(url, timeout=30, max_retries=2):
    """
    Telecharge une URL en respectant le rate limit.
    Retourne le texte HTML ou None si echec apres retries.
    """
    # Rate limit : on attend si la derniere requete etait trop recente
    elapsed = time.time() - _last_request_time[0]
    if elapsed < RATE_LIMIT_SECONDS:
        time.sleep(RATE_LIMIT_SECONDS - elapsed)
    
    headers = {"User-Agent": USER_AGENT}
    
    for attempt in range(max_retries + 1):
        try:
            response = requests.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()
            _last_request_time[0] = time.time()
            return response.text
        except requests.exceptions.RequestException as e:
            if attempt < max_retries:
                wait = 2 ** attempt  # backoff : 1s, 2s
                print(f"    ! Erreur fetch ({e}), retry dans {wait}s...")
                time.sleep(wait)
            else:
                print(f"    !! Echec definitif pour {url}: {e}")
                return None


def get_cache_path(scraper_name, key):
    """
    Retourne le chemin du fichier cache pour une cle donnee.
    Exemple : get_cache_path('hns', 'match_100399910') 
             -> data/scraped/_cache/hns/match_100399910.html
    """
    safe_key = key.replace("/", "_").replace(":", "_")
    cache_path = CACHE_DIR / scraper_name / f"{safe_key}.html"
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    return cache_path


def load_cache(scraper_name, key):
    """Charge depuis le cache. Retourne None si absent."""
    path = get_cache_path(scraper_name, key)
    if path.exists():
        return path.read_text(encoding="utf-8")
    return None


def save_cache(scraper_name, key, content):
    """Sauvegarde dans le cache."""
    path = get_cache_path(scraper_name, key)
    path.write_text(content, encoding="utf-8")


def fetch_with_cache(url, scraper_name, key):
    """
    Combine fetch + cache.
    Si la cle existe en cache, retourne directement.
    Sinon fetch et sauvegarde.
    """
    cached = load_cache(scraper_name, key)
    if cached is not None:
        return cached
    
    content = fetch(url)
    if content is not None:
        save_cache(scraper_name, key, content)
    return content


def safe_text(element, default=""):
    """Retourne le texte d'un element BeautifulSoup, ou default si None."""
    if element is None:
        return default
    return element.get_text(strip=True)


def log(message):
    """Log avec timestamp."""
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {message}")