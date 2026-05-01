"""
Test scraper HNS Semafor pour la HNL croate.
"""

import requests
from bs4 import BeautifulSoup

HNL_COMPETITION_ID = 88712926
SEASON = "2024/2025"

URL = f"https://semafor.hns.family/en/competitions/{HNL_COMPETITION_ID}/supersport-hnl/"

print(f"Fetching: {URL}")
response = requests.get(URL, params={"season": SEASON}, headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0) DerybalTest/0.1"
})
print(f"Status: {response.status_code}, taille: {len(response.text)} caracteres\n")

soup = BeautifulSoup(response.text, "html.parser")

matches = soup.find_all("li", class_="row")
print(f"=== {len(matches)} matchs trouves dans la page ===\n")

for i, m in enumerate(matches[:5]):
    match_id = m.get("data-match")
    round_num = m.get("data-round")
    
    club1 = m.find("div", class_="club1")
    club2 = m.find("div", class_="club2")
    home_name = club1.find("a").get_text(strip=True).split("\n")[0] if club1 else "?"
    away_name = club2.find("a").get_text(strip=True).split("\n")[0] if club2 else "?"
    
    res1 = m.find("div", class_="res1")
    res2 = m.find("div", class_="res2")
    score_h = res1.get_text(strip=True) if res1 else "?"
    score_a = res2.get_text(strip=True) if res2 else "?"
    
    link = m.find("div", class_="link").find("a").get("href") if m.find("div", class_="link") else None
    
    print(f"  Match #{i+1}: {home_name} {score_h}-{score_a} {away_name}")
    print(f"    id={match_id}, round={round_num}")
    print(f"    URL: {link}\n")

if matches:
    first_match = matches[0]
    detail_url = first_match.find("div", class_="link").find("a").get("href")
    
    print(f"\n=== Details du 1er match ===")
    print(f"URL: {detail_url}\n")
    
    detail_response = requests.get(detail_url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0) DerybalTest/0.1"
    })
    print(f"Status: {detail_response.status_code}, taille: {len(detail_response.text)} caracteres\n")
    
    detail_soup = BeautifulSoup(detail_response.text, "html.parser")
    text = detail_soup.get_text()
    
    keywords = ["Date", "Time", "Round", "Stadium", "Referee",
                "First half", "Half time", "Goals", "Cards", "Yellow", "Red",
                "Corners", "Shots", "Possession", "Substitution"]
    
    print("Mots-cles trouves dans la page detail:")
    for kw in keywords:
        if kw.lower() in text.lower():
            print(f"  + {kw}")
        else:
            print(f"  - {kw}")
    
    with open("detail_match_dump.html", "w", encoding="utf-8") as f:
        f.write(detail_response.text)
    print(f"\nHTML detail sauve dans detail_match_dump.html")