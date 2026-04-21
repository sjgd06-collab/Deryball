"""
Script à exécuter UNE FOIS pour générer le mapping entre les noms d'équipes
de football-data.org (longs) et ceux de football-data.co.uk (courts).

Utilise rapidfuzz pour trouver les correspondances floues.
Le résultat est sauvegardé dans equipes_mapping.py.
"""
import pandas as pd
from rapidfuzz import process, fuzz
from pathlib import Path

# Charger les deux sources
df_historique = pd.read_csv("data/All_Leagues_2025-26.csv")
df_fixtures = pd.read_csv("data/fixtures_a_venir.csv")

# Jeux de noms
noms_courts = sorted(set(df_historique["HomeTeam"]) | set(df_historique["AwayTeam"]))
noms_longs = sorted(set(df_fixtures["HomeTeam"]) | set(df_fixtures["AwayTeam"]))

print(f"Noms courts (football-data.co.uk) : {len(noms_courts)}")
print(f"Noms longs (football-data.org)    : {len(noms_longs)}")
print()

# Pour chaque nom long, trouver le meilleur nom court correspondant
mapping = {}
non_trouves = []

for nom_long in noms_longs:
    # rapidfuzz cherche le nom court le plus similaire
    resultat = process.extractOne(
        nom_long,
        noms_courts,
        scorer=fuzz.token_sort_ratio,  # Bon pour ignorer "FC", "AC", articles, etc.
        score_cutoff=50,               # Seuil minimum de similarité (0-100)
    )
    if resultat:
        nom_match, score, _ = resultat
        mapping[nom_long] = (nom_match, score)
    else:
        non_trouves.append(nom_long)

# Afficher le mapping, trié par score (les moins sûrs en haut pour vérification)
print("=" * 70)
print("MAPPING PROPOSÉ (trié du moins sûr au plus sûr)")
print("=" * 70)
mapping_tries = sorted(mapping.items(), key=lambda x: x[1][1])
for nom_long, (nom_court, score) in mapping_tries:
    marqueur = "⚠️ " if score < 75 else "  "
    print(f"{marqueur}[{score:3.0f}] {nom_long:35s} → {nom_court}")

if non_trouves:
    print()
    print("=" * 70)
    print("NON TROUVÉS (aucune correspondance au-dessus du seuil)")
    print("=" * 70)
    for nom in non_trouves:
        print(f"  • {nom}")

# Générer le fichier equipes_mapping.py
contenu = '"""\nMapping des noms d\'équipes entre football-data.org et football-data.co.uk.\nGénéré automatiquement par generer_mapping.py.\n"""\n\n'
contenu += "MAPPING_EQUIPES = {\n"
for nom_long, (nom_court, score) in sorted(mapping.items()):
    commentaire = f"  # score={score:.0f}"
    contenu += f'    "{nom_long}": "{nom_court}",{commentaire}\n'
contenu += "}\n"

with open("equipes_mapping.py", "w", encoding="utf-8") as f:
    f.write(contenu)

print()
print(f"✅ Fichier 'equipes_mapping.py' généré avec {len(mapping)} correspondances.")
print("   Ouvre ce fichier et vérifie manuellement les correspondances marquées ⚠️ (score < 75).")