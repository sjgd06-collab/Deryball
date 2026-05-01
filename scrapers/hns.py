"""
Scraper pour la HNL croate (1ere division) via hns.family Semafor.

Phase 1 : recuperer la liste des matchs d'une saison.
"""

from bs4 import BeautifulSoup
from scrapers.base import fetch_with_cache, safe_text, log

# IDs du site Semafor
HNL_COMPETITION_ID = 88712926

# Saison qu'on cible
SEASON = "2025/2026"
SEASON_LABEL = "2025-26"  # format Deryball


def fetch_match_list(season=SEASON):
    """
    Recupere la liste de tous les matchs d'une saison HNL.
    Retourne une liste de dicts, un par match.
    """
    url = f"https://semafor.hns.family/en/competitions/{HNL_COMPETITION_ID}/supersport-hnl/?season={season}"
    cache_key = f"matchlist_{season.replace('/', '-')}"
    
    log(f"Fetching liste des matchs HNL saison {season}...")
    html = fetch_with_cache(url, "hns", cache_key)
    if html is None:
        log("!! Impossible de recuperer la page de competition")
        return []
    
    soup = BeautifulSoup(html, "html.parser")
    matches_raw = soup.find_all("li", class_="row")
    
    matches = []
    for m in matches_raw:
        match_id = m.get("data-match")
        round_num = m.get("data-round")
        
        if not match_id:
            continue
        
        # Equipes (les noms peuvent contenir des sous-elements comme l'image, on prend le texte direct du <a>)
        club1 = m.find("div", class_="club1")
        club2 = m.find("div", class_="club2")
        if not club1 or not club2:
            continue
        
        a1 = club1.find("a")
        a2 = club2.find("a")
        if not a1 or not a2:
            continue
        
        # Le nom est le texte du <a> en enlevant les sauts de ligne et le contenu du <div class="logo">
        # On prend le texte avant le premier saut de ligne (c'est le nom de l'equipe)
        home_name = a1.get_text(strip=True).split("\n")[0]
        away_name = a2.get_text(strip=True).split("\n")[0]
        
        # Score
        res1 = m.find("div", class_="res1")
        res2 = m.find("div", class_="res2")
        score_h = safe_text(res1)
        score_a = safe_text(res2)
        
        # URL detail (on la garde pour la phase 2)
        link_div = m.find("div", class_="link")
        detail_url = None
        if link_div and link_div.find("a"):
            detail_url = link_div.find("a").get("href")
        # Debug : on regarde si le match est de la bonne saison
        # via la classe ou un attribut HTML qu'on rate peut-etre
        competition_div = m.find("div", class_="competition")
        competition_text = safe_text(competition_div)
        matches.append({
            "match_id": match_id,
            "round": round_num,
            "home": home_name,
            "away": away_name,
            "score_home": score_h,
            "score_away": score_a,
            "detail_url": detail_url,
            "competition": competition_text,
        })
    
    log(f"  {len(matches)} matchs extraits")
    return matches


def main():
    """Test : recupere et affiche les 10 premiers matchs."""
    matches = fetch_match_list()
    if not matches:
        log("Aucun match recupere.")
        return
    
    log(f"Total : {len(matches)} matchs trouves")
    log("Apercu des 10 premiers :")
    for m in matches[:10]:
        score = f"{m['score_home']}-{m['score_away']}" if m['score_home'] else "(pas joue)"
        print(f"  [{m['competition']}] J{m['round']:>2} | {m['home']:<25} {score:>5} {m['away']:<25} | id={m['match_id']}")
    
    # Compter par competition
    from collections import Counter
    by_comp = Counter(m['competition'] for m in matches)
    log("Repartition par competition :")
    for comp, count in by_comp.most_common():
        print(f"  {count:>4} matchs : {comp}")
    
    # Stats utiles
    played = sum(1 for m in matches if m['score_home'])
    not_played = len(matches) - played
    log(f"Matchs joues : {played}, a jouer : {not_played}")


if __name__ == "__main__":
    main()