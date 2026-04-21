"""
Mapping des noms d'équipes entre football-data.org et football-data.co.uk.
Vérifié manuellement.
"""

MAPPING_EQUIPES = {
    # ============================================================
    # PREMIER LEAGUE (England)
    # ============================================================
    "Arsenal FC": "Arsenal",
    "Aston Villa FC": "Aston Villa",
    "AFC Bournemouth": "Bournemouth",
    "Brentford FC": "Brentford",
    "Brighton & Hove Albion FC": "Brighton",
    "Burnley FC": "Burnley",
    "Chelsea FC": "Chelsea",
    "Crystal Palace FC": "Crystal Palace",
    "Everton FC": "Everton",
    "Fulham FC": "Fulham",
    "Ipswich Town FC": "Ipswich",
    "Leeds United FC": "Leeds",
    "Leicester City FC": "Leicester",
    "Liverpool FC": "Liverpool",
    "Manchester City FC": "Man City",
    "Manchester United FC": "Man United",
    "Newcastle United FC": "Newcastle",
    "Nottingham Forest FC": "Nott'm Forest",
    "Southampton FC": "Southampton",
    "Sunderland AFC": "Sunderland",
    "Tottenham Hotspur FC": "Tottenham",
    "West Ham United FC": "West Ham",
    "Wolverhampton Wanderers FC": "Wolves",

    # ============================================================
    # CHAMPIONSHIP (England - 2nd div)
    # ============================================================
    "Birmingham City FC": "Birmingham",
    "Blackburn Rovers FC": "Blackburn",
    "Bristol City FC": "Bristol City",
    "Charlton Athletic FC": "Charlton",
    "Coventry City FC": "Coventry",
    "Derby County FC": "Derby",
    "Hull City AFC": "Hull",
    "Middlesbrough FC": "Middlesbrough",
    "Millwall FC": "Millwall",
    "Norwich City FC": "Norwich",
    "Oxford United FC": "Oxford",
    "Portsmouth FC": "Portsmouth",
    "Preston North End FC": "Preston",
    "Queens Park Rangers FC": "QPR",
    "Sheffield United FC": "Sheffield United",
    "Sheffield Wednesday FC": "Sheffield Weds",
    "Stoke City FC": "Stoke",
    "Swansea City AFC": "Swansea",
    "Watford FC": "Watford",
    "West Bromwich Albion FC": "West Brom",
    "Wrexham AFC": "Wrexham",

    # ============================================================
    # BUNDESLIGA (Germany)
    # ============================================================
    "1. FC Heidenheim 1846": "Heidenheim",
    "1. FC Köln": "FC Koln",
    "1. FC Union Berlin": "Union Berlin",
    "1. FSV Mainz 05": "Mainz",
    "Bayer 04 Leverkusen": "Leverkusen",
    "Borussia Dortmund": "Dortmund",
    "Borussia Mönchengladbach": "M'gladbach",
    "Eintracht Frankfurt": "Ein Frankfurt",
    "FC Augsburg": "Augsburg",
    "FC Bayern München": "Bayern Munich",
    "FC St. Pauli 1910": "St Pauli",
    "Hamburger SV": "Hamburg",
    "RB Leipzig": "RB Leipzig",
    "SC Freiburg": "Freiburg",
    "SV Werder Bremen": "Werder Bremen",
    "TSG 1899 Hoffenheim": "Hoffenheim",
    "VfB Stuttgart": "Stuttgart",
    "VfL Wolfsburg": "Wolfsburg",

    # ============================================================
    # SERIE A (Italy)
    # ============================================================
    "AC Milan": "Milan",
    "AC Pisa 1909": "Pisa",
    "ACF Fiorentina": "Fiorentina",
    "AS Roma": "Roma",
    "Atalanta BC": "Atalanta",
    "Bologna FC 1909": "Bologna",
    "Cagliari Calcio": "Cagliari",
    "Como 1907": "Como",
    "FC Internazionale Milano": "Inter",
    "Genoa CFC": "Genoa",
    "Hellas Verona FC": "Verona",
    "Juventus FC": "Juventus",
    "Parma Calcio 1913": "Parma",
    "SS Lazio": "Lazio",
    "SSC Napoli": "Napoli",
    "Torino FC": "Torino",
    "US Cremonese": "Cremonese",
    "US Lecce": "Lecce",
    "US Sassuolo Calcio": "Sassuolo",
    "Udinese Calcio": "Udinese",

    # ============================================================
    # LA LIGA (Spain)
    # ============================================================
    "Athletic Club": "Ath Bilbao",
    "CA Osasuna": "Osasuna",
    "Club Atlético de Madrid": "Ath Madrid",
    "Deportivo Alavés": "Alaves",
    "Elche CF": "Elche",
    "FC Barcelona": "Barcelona",
    "Getafe CF": "Getafe",
    "Girona FC": "Girona",
    "Levante UD": "Levante",
    "RC Celta de Vigo": "Celta",
    "RCD Espanyol de Barcelona": "Espanol",
    "RCD Mallorca": "Mallorca",
    "Rayo Vallecano de Madrid": "Vallecano",
    "Real Betis Balompié": "Betis",
    "Real Madrid CF": "Real Madrid",
    "Real Oviedo": "Oviedo",
    "Real Sociedad de Fútbol": "Sociedad",
    "Sevilla FC": "Sevilla",
    "Valencia CF": "Valencia",
    "Villarreal CF": "Villarreal",

    # ============================================================
    # LIGUE 1 (France)
    # ============================================================
    "AJ Auxerre": "Auxerre",
    "AS Monaco FC": "Monaco",
    "Angers SCO": "Angers",
    "FC Lorient": "Lorient",
    "FC Metz": "Metz",
    "FC Nantes": "Nantes",
    "Le Havre AC": "Le Havre",
    "Lille OSC": "Lille",
    "OGC Nice": "Nice",
    "Olympique Lyonnais": "Lyon",
    "Olympique de Marseille": "Marseille",
    "Paris FC": "Paris FC",
    "Paris Saint-Germain FC": "Paris SG",
    "RC Strasbourg Alsace": "Strasbourg",
    "Racing Club de Lens": "Lens",
    "Stade Brestois 29": "Brest",
    "Stade Rennais FC 1901": "Rennes",
    "Toulouse FC": "Toulouse",

    # ============================================================
    # EREDIVISIE (Netherlands)
    # ============================================================
    "AZ": "AZ Alkmaar",
    "Go Ahead Eagles": "Go Ahead Eagles",
    "PEC Zwolle": "Zwolle",
    "PSV": "PSV Eindhoven",
    "Sparta Rotterdam": "Sparta Rotterdam",
    "Telstar 1963": "Telstar",

    # ============================================================
    # PRIMEIRA LIGA (Portugal)
    # ============================================================
    "AVS": "AVS",
    "CD Nacional": "Nacional",
    "CD Santa Clara": "Santa Clara",
    "CD Tondela": "Tondela",
    "CF Estrela da Amadora": "Estrela",
    "Casa Pia AC": "Casa Pia",
    "FC Alverca": "Alverca",
    "FC Arouca": "Arouca",
    "FC Famalicão": "Famalicao",
    "FC Porto": "Porto",
    "GD Estoril Praia": "Estoril",
    "Gil Vicente FC": "Gil Vicente",
    "Moreirense FC": "Moreirense",
    "Rio Ave FC": "Rio Ave",
    "Sport Lisboa e Benfica": "Benfica",
    "Sporting Clube de Braga": "Sp Braga",
    "Sporting Clube de Portugal": "Sp Lisbon",
    "Vitória SC": "Vitoria",

    # ============================================================
    # SERIE A (Brazil)
    # ============================================================
    "CA Mineiro": "Atletico-MG",
    "CA Paranaense": "Athletico-PR",
    "CR Flamengo": "Flamengo RJ",
    "CR Vasco da Gama": "Vasco",
    "Chapecoense AF": "Chapecoense-SC",
    "Clube do Remo": "Remo",
    "Coritiba FBC": "Coritiba",
    "Cruzeiro EC": "Cruzeiro",
    "EC Bahia": "Bahia",
    "EC Vitória": "Vitoria",
    "Botafogo FR": "Botafogo RJ",
    "CR Flamengo": "Flamengo RJ",
    "Fluminense FC": "Fluminense",
    "Grêmio FBPA": "Gremio",
    "Mirassol FC": "Mirassol",
    "RB Bragantino": "Bragantino",
    "SC Corinthians Paulista": "Corinthians",
    "SC Internacional": "Internacional",
    "SE Palmeiras": "Palmeiras",
    "Santos FC": "Santos",
    "São Paulo FC": "Sao Paulo",
}