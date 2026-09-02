"""
Composants de cartes (vue détaillée) pour Deryball.
Génère du HTML pour afficher chaque match comme une carte pliable.
"""
import html
import pandas as pd
from stats import matrice_scores


# ============================================================
# CSS INJECTÉ POUR LES CARTES
# ============================================================
CARDS_CSS = """
<style>
/* ======================================================
   CARTES DE MATCH (Vue Détaillée)
   ====================================================== */
.db-cards-container {
    display: flex;
    flex-direction: column;
    gap: 8px;
    margin-top: 12px;
}

.db-card {
    background: var(--bg-surface);
    border: 1px solid var(--border-default);
    border-radius: 10px;
    overflow: hidden;
    transition: border-color 0.15s ease;
}
.db-card:hover { border-color: var(--border-strong); }

/* HEADER (toujours visible) */
.db-card > summary {
    list-style: none;
    cursor: pointer;
    padding: 14px 16px;
    display: grid;
    grid-template-columns: 110px 1fr 130px;
    align-items: center;
    gap: 16px;
    user-select: none;
}
.db-card > summary::-webkit-details-marker { display: none; }
.db-card > summary::marker { display: none; }
.db-card > summary:hover { background: var(--bg-elevated); }

.db-card-meta {
    display: flex; flex-direction: column; gap: 2px;
}
.db-card-time {
    font-family: 'JetBrains Mono', monospace;
    font-size: 14px; font-weight: 600;
    color: var(--text-strong);
    font-variant-numeric: tabular-nums;
}
.db-card-league {
    font-size: 11px;
    color: var(--text-muted);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.db-card-teams {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 14px;
    flex-wrap: wrap;
}
.db-card-team-name {
    font-family: 'Bricolage Grotesque', sans-serif !important;
    font-weight: 600;
    font-size: 15px;
    color: var(--text-strong) !important;
}
.db-card-pos {
    font-size: 11px;
    color: var(--text-faint) !important;
    font-family: 'JetBrains Mono', monospace !important;
}
.db-card-score {
    font-family: 'Bricolage Grotesque', sans-serif !important;
    font-size: 20px;
    font-weight: 700;
    color: var(--text-strong) !important;
    font-variant-numeric: tabular-nums;
    letter-spacing: -0.02em;
    min-width: 70px;
    text-align: center;
}
.db-card-score.upcoming {
    font-size: 11px;
    font-weight: 600;
    color: var(--info) !important;
    background: rgba(96,165,250,0.15);
    border: 1px solid rgba(96,165,250,0.3);
    padding: 4px 9px;
    border-radius: 5px;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}
.db-card-signaux {
    display: inline-flex;
    gap: 2px;
    font-size: 11px;
    margin-left: 2px;
}

.db-card-right {
    display: flex; align-items: center; justify-content: flex-end; gap: 12px;
}
.db-card-pred {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 13px;
    color: var(--accent) !important;
    font-weight: 600;
    font-variant-numeric: tabular-nums;
}
.db-card-arrow {
    font-size: 14px;
    color: var(--text-muted) !important;
    transition: transform 0.2s;
}
.db-card[open] .db-card-arrow { transform: rotate(180deg); }

/* BODY (déplié) */
.db-card-body {
    padding: 18px 16px 16px;
    border-top: 1px solid var(--border-subtle);
    background: var(--bg-base);
}

.db-section-title {
    font-family: 'Bricolage Grotesque', sans-serif !important;
    font-size: 13px;
    font-weight: 600;
    color: var(--accent) !important;
    margin-bottom: 10px;
    margin-top: 16px;
    display: flex; align-items: center; gap: 7px;
}
.db-section-title:first-child { margin-top: 0; }

/* Section POISSON (5 cellules + xG) */
.db-poisson-row {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 12px;
    background: var(--bg-elevated);
    border: 1px solid var(--accent-deep);
    border-left: 3px solid var(--accent);
    border-radius: 8px;
    padding: 14px;
    margin-bottom: 12px;
}
.db-pois-cell { display: flex; flex-direction: column; gap: 5px; }
.db-pois-label {
    font-size: 11px;
    color: var(--text-muted) !important;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}
.db-pois-value {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 17px; font-weight: 600;
    color: var(--text-strong) !important;
    font-variant-numeric: tabular-nums;
}
.db-pois-bar {
    height: 4px;
    background: var(--bg-deep);
    border-radius: 2px;
    overflow: hidden;
}
.db-pois-bar-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--accent-soft), var(--accent));
    border-radius: 2px;
}
.db-xg-line {
    display: flex;
    justify-content: space-between;
    padding: 12px 14px 0;
    margin-top: 4px;
    border-top: 1px dashed var(--border-default);
    font-size: 12.5px;
    color: var(--text-muted) !important;
}
.db-xg-line span { color: var(--text-muted) !important; }
.db-xg-num {
    font-family: 'JetBrains Mono', monospace !important;
    color: var(--text-strong) !important;
    font-weight: 600;
}

/* COMPARAISON ÉQUIPES (2 cartes côte à côte) */
.db-compare-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin-bottom: 12px;
}
.db-compare-card {
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: 8px;
    padding: 14px;
}
.db-compare-card.home { border-left: 3px solid var(--success); }
.db-compare-card.away { border-left: 3px solid var(--info); }
.db-compare-head {
    display: flex; align-items: center; gap: 8px;
    margin-bottom: 12px;
    flex-wrap: wrap;
}
.db-compare-name {
    font-weight: 600; font-size: 14px;
    color: var(--text-strong) !important;
    font-family: 'Bricolage Grotesque', sans-serif !important;
}
.db-compare-badge {
    font-size: 9.5px;
    padding: 2px 6px;
    border-radius: 4px;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}
.db-compare-badge.home {
    background: rgba(74,222,128,0.15);
    color: var(--success) !important;
}
.db-compare-badge.away {
    background: rgba(96,165,250,0.15);
    color: var(--info) !important;
}
.db-compare-signaux {
    font-size: 12px;
    color: var(--warning) !important;
    margin-left: auto;
    font-weight: 500;
}

.db-form-line {
    display: flex; gap: 3px; margin-bottom: 10px;
}
.db-form-pill {
    width: 18px; height: 18px;
    border-radius: 4px;
    display: flex; align-items: center; justify-content: center;
    font-size: 9.5px; font-weight: 700;
    font-family: 'JetBrains Mono', monospace !important;
}
.db-form-pill.W,
.db-form-pill.V { background: rgba(74,222,128,0.15); color: var(--success) !important; }
.db-form-pill.D,
.db-form-pill.N { background: rgba(251,191,36,0.15); color: var(--warning) !important; }
.db-form-pill.L { background: rgba(244,63,94,0.15); color: var(--danger) !important; }

.db-metric-line {
    display: grid;
    grid-template-columns: 1fr 60px 50px;
    align-items: center;
    padding: 5px 0;
    font-size: 12.5px;
    gap: 8px;
}
.db-metric-line + .db-metric-line { border-top: 1px solid var(--border-subtle); }
.db-metric-name { color: var(--text-muted) !important; }
.db-metric-val {
    font-family: 'JetBrains Mono', monospace !important;
    font-weight: 600;
    color: var(--text-strong) !important;
    text-align: right;
    font-variant-numeric: tabular-nums;
}
.db-metric-bar {
    height: 4px;
    background: var(--bg-deep);
    border-radius: 2px;
    overflow: hidden;
}
.db-metric-bar-fill {
    height: 100%;
    background: var(--accent);
    border-radius: 2px;
}
.db-metric-bar-fill.success { background: var(--success); }
.db-metric-bar-fill.warning { background: var(--warning); }
.db-metric-bar-fill.danger { background: var(--danger); }
/* Stats détaillées (mini-section) */
.db-extras-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin-bottom: 12px;
}
.db-extras-block {
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: 8px;
    padding: 12px;
}
.db-extras-title {
    font-size: 11px;
    color: var(--text-muted) !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    font-weight: 600;
    margin-bottom: 8px;
}
.db-extras-teams {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
    padding-bottom: 8px;
    margin-bottom: 8px;
    border-bottom: 1px dashed var(--border-default);
}
.db-extras-team {
    display: flex; flex-direction: column; gap: 1px;
}
.db-extras-team-label {
    font-size: 10px;
    color: var(--text-faint) !important;
    font-weight: 500;
}
.db-extras-team-val {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 14px;
    font-weight: 600;
    color: var(--text-strong) !important;
    font-variant-numeric: tabular-nums;
}
.db-extras-summary {
    display: flex;
    flex-direction: column;
    gap: 4px;
    font-size: 12px;
}
.db-extras-summary-line {
    display: flex; justify-content: space-between;
}
.db-extras-summary-name {
    color: var(--text-muted) !important;
}
.db-extras-summary-val {
    font-family: 'JetBrains Mono', monospace !important;
    color: var(--text-strong) !important;
    font-weight: 600;
    font-variant-numeric: tabular-nums;
}
.db-extras-empty {
    color: var(--text-faint) !important;
    font-size: 11.5px;
    font-style: italic;
    text-align: center;
    padding: 8px;
}
/* Heatmap Poisson */
.db-heat-row {
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-left: 3px solid var(--accent);
    border-radius: 8px;
    padding: 14px;
    margin-bottom: 12px;
}
.db-heat-summary {
    display: flex;
    flex-direction: column;
    gap: 4px;
    font-size: 12.5px;
    margin-bottom: 12px;
    padding-bottom: 10px;
    border-bottom: 1px dashed var(--border-default);
}
.db-heat-summary-line {
    color: var(--text-muted) !important;
}
.db-heat-summary-line strong {
    color: var(--text-strong) !important;
    font-family: 'JetBrains Mono', monospace;
    font-variant-numeric: tabular-nums;
    font-weight: 600;
}
.db-heat-summary-line .accent {
    color: var(--accent) !important;
    font-weight: 600;
}
.db-heat-table-wrap {
    overflow-x: auto;
}
.db-heat-table {
    border-collapse: collapse;
    margin: 0 auto;
    font-family: 'JetBrains Mono', monospace !important;
    font-variant-numeric: tabular-nums;
}
.db-heat-table th,
.db-heat-table td {
    padding: 6px 9px;
    text-align: center;
    font-size: 11.5px;
    border: 1px solid var(--border-subtle);
}
.db-heat-table th {
    background: var(--bg-elevated);
    color: var(--text-muted) !important;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    font-size: 10px;
}
.db-heat-table td {
    color: var(--text-default) !important;
    font-weight: 500;
    min-width: 48px;
}
.db-heat-table td.heat-best {
    outline: 2px solid var(--accent);
    outline-offset: -2px;
    font-weight: 700;
    color: var(--text-strong) !important;
}
.db-heat-caption {
    text-align: center;
    color: var(--text-muted) !important;
    font-size: 10.5px;
    margin-top: 6px;
    font-style: italic;
}
/* H2H */
.db-h2h-row {
    display: grid;
    grid-template-columns: auto 1fr;
    gap: 14px;
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-left: 3px solid var(--accent);
    border-radius: 8px;
    padding: 14px;
    align-items: center;
}
.db-h2h-big {
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    background: var(--bg-deep);
    border: 1px solid var(--border-default);
    border-radius: 6px;
    padding: 10px 18px;
}
.db-h2h-big-num {
    font-family: 'Bricolage Grotesque', sans-serif !important;
    font-size: 26px; font-weight: 700;
    color: var(--accent) !important;
    line-height: 1;
}
.db-h2h-big-lab {
    font-size: 9px;
    color: var(--text-muted) !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 3px;
    font-weight: 600;
}
.db-h2h-stats {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;
}
.db-h2h-stats > div {
    text-align: left;
}
.db-h2h-st-val {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 14px; font-weight: 600;
    color: var(--text-strong) !important;
    font-variant-numeric: tabular-nums;
}
.db-h2h-st-lab {
    font-size: 10px;
    color: var(--text-muted) !important;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    font-weight: 500;
    margin-top: 1px;
}
.db-h2h-empty {
    color: var(--text-muted) !important;
    font-size: 12px;
    font-style: italic;
    padding: 12px;
    text-align: center;
    background: var(--bg-surface);
    border: 1px dashed var(--border-default);
    border-radius: 8px;
}

/* RESPONSIVE */
@media (max-width: 900px) {
    .db-card > summary {
        grid-template-columns: 1fr;
        gap: 10px;
    }
    .db-card-meta { flex-direction: row; gap: 12px; align-items: center; }
    .db-card-right { justify-content: flex-start; }
    .db-poisson-row { grid-template-columns: repeat(3, 1fr); }
    .db-compare-row { grid-template-columns: 1fr; }
    .db-h2h-row { grid-template-columns: 1fr; }
    .db-h2h-big { padding: 8px 14px; }
    .db-h2h-big-num { font-size: 22px; }
}
</style>
"""


# ============================================================
# HELPERS
# ============================================================
def _safe_pct(v):
    """Convertit en float et clamp [0,100], ou None si invalide."""
    if v is None or pd.isna(v):
        return None
    try:
        f = float(v)
        return max(0.0, min(100.0, f))
    except (ValueError, TypeError):
        return None


def _fmt_pos(pos):
    """Formate la position : 1 -> '1er', 2 -> '2e', etc."""
    if pos is None or pd.isna(pos):
        return "—"
    try:
        p = int(pos)
        if p == 1:
            return "1er"
        return f"{p}e"
    except (ValueError, TypeError):
        return "—"


def _esc(s):
    """Échappe le HTML pour éviter les soucis avec apostrophes/<>."""
    if s is None:
        return ""
    return html.escape(str(s))


def _minify_html(s):
    """
    Supprime les espaces en début de ligne ET les sauts de ligne.
    INDISPENSABLE : Streamlit utilise Markdown, qui interprète toute ligne
    commençant par 4 espaces ou plus comme un BLOC DE CODE et l'affiche tel quel.
    En mettant tout sur une seule ligne, on contourne ce comportement.
    """
    return "".join(line.strip() for line in s.split("\n"))


def _heat_forme(rate):
    """Dégradé divergent rouge→vert en 5 paliers selon le taux [0..1]."""
    if rate is None:
        return ("transparent", "#c9c9d4")
    if rate < 0.20:
        return ("#E0685F", "#ffffff")   # 0-19  : rouge
    if rate < 0.40:
        return ("#EE9F4C", "#3f2200")   # 20-39 : orange
    if rate < 0.60:
        return ("#F1CE52", "#463800")   # 40-59 : jaune
    if rate < 0.80:
        return ("#9FCB63", "#1b3606")   # 60-79 : vert pâle
    return ("#2E7D32", "#ffffff")       # 80-100: vert foncé


def _cellule_compte(m, key):
    """Cellule 'x/N' avec chaleur selon x/N."""
    n = m.get("N", 0)
    if not n:
        return '<td style="padding:6px 3px;text-align:center;color:#7a7a88;">—</td>'
    x = m.get(key, 0)
    bg, col = _heat_forme(x / n if n else None)
    poids = "font-weight:600;" if bg != "transparent" else ""
    return (f'<td style="padding:6px 3px;text-align:center;font-variant-numeric:tabular-nums;'
            f'background:{bg};color:{col};{poids}">{x}/{n}</td>')


def _cellule_moy(m, key, heat=True):
    """Cellule moyenne (BM/BE). Chaleur verte sur BM seulement (heat=True)."""
    v = m.get(key)
    if v is None:
        return '<td style="padding:6px 3px;text-align:center;color:#7a7a88;">—</td>'
    if heat:
        bg, col = _heat_forme(min(v / 2.5, 1.0))
    else:
        bg, col = ("transparent", "#c9c9d4")
    poids = "font-weight:600;" if bg != "transparent" else ""
    return (f'<td style="padding:6px 3px;text-align:center;font-variant-numeric:tabular-nums;'
            f'background:{bg};color:{col};{poids}">{v:.2f}</td>')


def _section_forme(row):
    """Grille de forme : 3 fenêtres (5/10/saison) x 3 périmètres (combiné/dom/ext) x 6 stats.
    Lit row['FormeStats'] (dict produit par stats_forme_match). Rien si absent."""
    forme = row.get("FormeStats")
    if not isinstance(forme, dict) or not forme:
        return ""

    home = _esc(row.get("HomeTeam", "Domicile"))
    away = _esc(row.get("AwayTeam", "Extérieur"))
    perimetres = [
        ("combine", "Combiné 2 éq.", "#8b7bd8"),
        ("domicile", f"{home} (dom)", "#4db6ac"),
        ("exterieur", f"{away} (ext)", "#e6a06b"),
    ]
    fenetres = [("5", "5 derniers matchs"), ("10", "10 derniers matchs"), ("saison", "Saison totale")]
    entetes = ["BTTS", "O0.5", "O1.5", "O2.5", "BM", "BE"]

    blocs = ""
    for fen_key, fen_lab in fenetres:
        data = forme.get(fen_key, {})
        th = "".join(f'<th style="padding:5px 3px;font-weight:500;color:#7a7a88;'
                     f'text-align:center;font-size:11px;">{h}</th>' for h in entetes)
        corps = ""
        for peri_key, peri_lab, couleur in perimetres:
            m = data.get(peri_key, {"N": 0})
            pastille = (f'<span style="display:inline-block;width:8px;height:8px;border-radius:2px;'
                        f'background:{couleur};margin-right:6px;vertical-align:1px;"></span>')
            corps += (
                f'<tr style="border-top:0.5px solid rgba(255,255,255,0.06);">'
                f'<td style="padding:6px 3px;color:#d7d7de;white-space:nowrap;">{pastille}{peri_lab}</td>'
                f'{_cellule_compte(m, "BTTS")}{_cellule_compte(m, "O05")}'
                f'{_cellule_compte(m, "O15")}{_cellule_compte(m, "O25")}'
                f'{_cellule_moy(m, "BM", heat=False)}{_cellule_moy(m, "BE", heat=False)}'
                f'</tr>'
            )
        blocs += (
            f'<div style="font-size:11px;letter-spacing:.04em;text-transform:uppercase;'
            f'color:#9a9aa8;margin:12px 0 4px;">{fen_lab}</div>'
            f'<table style="width:100%;border-collapse:collapse;font-size:12.5px;table-layout:fixed;">'
            f'<colgroup><col style="width:34%"><col><col><col><col><col style="width:11%"><col style="width:11%"></colgroup>'
            f'<thead><tr><th></th>{th}</tr></thead><tbody>{corps}</tbody></table>'
        )

    return (
        '<div class="db-section-title">📊 Forme (même compétition)</div>'
        f'{blocs}'
        '<div style="font-size:11px;color:#7a7a88;margin-top:6px;">'
        'Comptages « x / N » · BM = buts marqués/match · BE = buts encaissés/match · '
        'vert = tendance aux buts plus forte.</div>'
    )


def rendre_tableau_forme(df, fen, peri, custom=False):
    """Table condensée : colonnes de base + 6 stats de forme (fenêtre + périmètre choisis), avec chaleur.
    custom=True : matchups perso (Domicile / Ligue / Extérieur / Ligue, sans Heure ni Score)."""
    if custom:
        base_h = ["Domicile", "Ligue", "Extérieur", "Ligue"]
        base_keys = ["HomeTeam", "H_Ligue", "AwayTeam", "A_Ligue"]
    else:
        base_h = ["Heure", "Ligue", "Domicile", "Extérieur", "Score"]
        base_keys = ["TimeNY", "League", "HomeTeam", "AwayTeam", "__score__"]
    th = "".join(
        f'<th style="padding:7px 6px;text-align:left;font-weight:500;color:#7a7a88;'
        f'font-size:12px;white-space:nowrap;">{h}</th>' for h in base_h
    )
    th += "".join(
        f'<th style="padding:7px 4px;text-align:center;font-weight:500;color:#7a7a88;'
        f'font-size:12px;">{h}</th>' for h in ["BTTS", "O0.5", "O1.5", "O2.5", "BM", "BE"]
    )
    lignes = ""
    for _, row in df.iterrows():
        forme = row.get("FormeStats") or {}
        m = forme.get(fen, {}).get(peri, {"N": 0})
        base_vals = []
        for k in base_keys:
            if k == "__score__":
                hg = row.get("FTHG")
                ag = row.get("FTAG")
                if row.get("IsUpcoming") is True or hg is None or (isinstance(hg, float) and hg != hg):
                    base_vals.append('<span style="color:#8b7bd8;">À venir</span>')
                else:
                    base_vals.append(f"{int(hg)}-{int(ag)}")
            else:
                base_vals.append(_esc(str(row.get(k, "") or "")))
        tds = "".join(
            f'<td style="padding:7px 6px;color:#d7d7de;white-space:nowrap;">{v}</td>'
            for v in base_vals
        )
        tds += (
            _cellule_compte(m, "BTTS") + _cellule_compte(m, "O05")
            + _cellule_compte(m, "O15") + _cellule_compte(m, "O25")
            + _cellule_moy(m, "BM", heat=False) + _cellule_moy(m, "BE", heat=False)
        )
        lignes += f'<tr style="border-top:0.5px solid rgba(255,255,255,0.06);">{tds}</tr>'
    html = (
        '<table style="width:100%;border-collapse:collapse;font-size:12.5px;">'
        f"<thead><tr>{th}</tr></thead><tbody>{lignes}</tbody></table>"
    )
    return _minify_html(html)


def rendre_carte_match_html(row, mode_compact=False):
    """Génère le HTML <details>/<summary> d'une carte de match : en-tête (heure, ligue,
    équipes, positions, score, prédiction O2.5) + grille Forme."""
    is_upcoming = (
        (row.get("Score") == "À VENIR")
        or bool(row.get("IsUpcoming", False))
        or row.get("Score") in (None, "")
    )

    score_raw = row.get("Score", "")
    if is_upcoming:
        score_html = '<span class="db-card-score upcoming">À venir</span>'
    else:
        score_aff = _esc(str(score_raw).replace("-", " — "))
        score_html = f'<span class="db-card-score">{score_aff}</span>'

    h_pos_aff = _fmt_pos(row.get("H_Pos"))
    a_pos_aff = _fmt_pos(row.get("A_Pos"))

    p_o25 = _safe_pct(row.get("P_Over25"))
    pred_html = f'<span class="db-card-pred">{p_o25:.0f}% O2.5</span>' if p_o25 is not None else ""

    time_aff = _esc(row.get("TimeNY") or row.get("Time") or "—")
    league_aff = _esc(row.get("League", ""))

    return _minify_html(f"""<details class="db-card">
    <summary>
        <div class="db-card-meta">
            <div class="db-card-time">{time_aff}</div>
            <div class="db-card-league">{league_aff}</div>
        </div>
        <div class="db-card-teams">
            <span class="db-card-team-name">{_esc(row.get('HomeTeam', ''))}</span>
            <span class="db-card-pos">{h_pos_aff}</span>
            {score_html}
            <span class="db-card-pos">{a_pos_aff}</span>
            <span class="db-card-team-name">{_esc(row.get('AwayTeam', ''))}</span>
        </div>
        <div class="db-card-right">
            {pred_html}
            <span class="db-card-arrow">▾</span>
        </div>
    </summary>
    <div class="db-card-body">
        {_section_forme(row)}
    </div>
</details>""")


def rendre_cartes_matchs(df, st_module):
    """Affiche tout le HTML des cartes en un seul appel st.markdown (perf)."""
    if df is None or len(df) == 0:
        st_module.info("Aucun match à afficher avec ces filtres.")
        return

    cartes = "\n".join(rendre_carte_match_html(row) for _, row in df.iterrows())
    st_module.markdown(
        f'<div class="db-cards-container">{cartes}</div>',
        unsafe_allow_html=True,
    )
