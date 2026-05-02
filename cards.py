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


def _safe_num(v):
    """Convertit en float ou None."""
    if v is None or pd.isna(v):
        return None
    try:
        return float(v)
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


def _form_pills(form_str):
    """Génère le HTML des pastilles V/N/D."""
    if not form_str:
        return ""
    return "".join(
        f'<div class="db-form-pill {c}">{c}</div>'
        for c in str(form_str)
    )


def _pois_cell(label, value):
    """Cellule individuelle de la zone Poisson."""
    v = _safe_pct(value)
    if v is None:
        return f"""<div class="db-pois-cell">
            <div class="db-pois-label">{label}</div>
            <div class="db-pois-value">—</div>
            <div class="db-pois-bar"></div>
        </div>"""
    return f"""<div class="db-pois-cell">
        <div class="db-pois-label">{label}</div>
        <div class="db-pois-value">{v:.1f}%</div>
        <div class="db-pois-bar"><div class="db-pois-bar-fill" style="width:{v:.0f}%"></div></div>
    </div>"""


def _metric_line(label, value, is_low_good=False):
    """Ligne de métrique avec barre dans la zone comparaison."""
    v = _safe_pct(value)
    if v is None:
        return f"""<div class="db-metric-line">
            <span class="db-metric-name">{label}</span>
            <span class="db-metric-bar"></span>
            <span class="db-metric-val">—</span>
        </div>"""

    # Couleur de la barre selon contexte
    if is_low_good:
        # Pour % 0-0 : bas = bon, haut = warning
        if v <= 10:
            cls = "success"
        elif v >= 25:
            cls = "warning"
        else:
            cls = ""
    else:
        # Pour Over/BTTS : haut = bon
        if v >= 70:
            cls = "success"
        elif v < 40:
            cls = "danger"
        else:
            cls = ""

    return f"""<div class="db-metric-line">
        <span class="db-metric-name">{label}</span>
        <span class="db-metric-bar"><span class="db-metric-bar-fill {cls}" style="width:{v:.0f}%"></span></span>
        <span class="db-metric-val">{v:.1f}%</span>
    </div>"""

def _section_extras(row):
    """
    Mini-section avec les stats détaillées (corners, cartons) si disponibles.
    Retourne du HTML vide si aucune stat n'est dispo.
    """
    h_corners = _safe_num(row.get("H_Corners_pg"))
    a_corners = _safe_num(row.get("A_Corners_pg"))
    h_corners_total = _safe_num(row.get("H_CornersTotal_pg"))
    a_corners_total = _safe_num(row.get("A_CornersTotal_pg"))
    h_corners_o95 = _safe_pct(row.get("H_CornersOver95"))
    a_corners_o95 = _safe_pct(row.get("A_CornersOver95"))

    h_yellow = _safe_num(row.get("H_Yellow_pg"))
    a_yellow = _safe_num(row.get("A_Yellow_pg"))
    h_yellow_total = _safe_num(row.get("H_YellowsTotal_pg"))
    a_yellow_total = _safe_num(row.get("A_YellowsTotal_pg"))
    h_yellow_o35 = _safe_pct(row.get("H_YellowsOver35"))
    a_yellow_o35 = _safe_pct(row.get("A_YellowsOver35"))

    has_corners = any(v is not None for v in [h_corners, a_corners, h_corners_total, a_corners_total])
    has_cartons = any(v is not None for v in [h_yellow, a_yellow, h_yellow_total, a_yellow_total])

    if not has_corners and not has_cartons:
        return ""  # rien à afficher

    # Helpers pour valeurs vides
    def fnum(v, suffix=""):
        return f"{v:.1f}{suffix}" if v is not None else "—"

    def fpct(v):
        return f"{v:.0f}%" if v is not None else "—"

    # Moyenne des totaux des 2 équipes (estimation Over)
    corners_total_moy = None
    if h_corners_total is not None and a_corners_total is not None:
        corners_total_moy = (h_corners_total + a_corners_total) / 2
    elif h_corners_total is not None:
        corners_total_moy = h_corners_total
    elif a_corners_total is not None:
        corners_total_moy = a_corners_total

    yellows_total_moy = None
    if h_yellow_total is not None and a_yellow_total is not None:
        yellows_total_moy = (h_yellow_total + a_yellow_total) / 2
    elif h_yellow_total is not None:
        yellows_total_moy = h_yellow_total
    elif a_yellow_total is not None:
        yellows_total_moy = a_yellow_total

    # Moyenne des % Over (estimation pour le match)
    corners_o95_moy = None
    if h_corners_o95 is not None and a_corners_o95 is not None:
        corners_o95_moy = (h_corners_o95 + a_corners_o95) / 2
    elif h_corners_o95 is not None:
        corners_o95_moy = h_corners_o95
    elif a_corners_o95 is not None:
        corners_o95_moy = a_corners_o95

    yellows_o35_moy = None
    if h_yellow_o35 is not None and a_yellow_o35 is not None:
        yellows_o35_moy = (h_yellow_o35 + a_yellow_o35) / 2
    elif h_yellow_o35 is not None:
        yellows_o35_moy = h_yellow_o35
    elif a_yellow_o35 is not None:
        yellows_o35_moy = a_yellow_o35

    # Bloc Corners
    if has_corners:
        corners_block = f"""
        <div class="db-extras-block">
            <div class="db-extras-title">🚩 Corners par match</div>
            <div class="db-extras-teams">
                <div class="db-extras-team">
                    <span class="db-extras-team-label">🏠 Domicile</span>
                    <span class="db-extras-team-val">{fnum(h_corners)}</span>
                </div>
                <div class="db-extras-team">
                    <span class="db-extras-team-label">✈️ Extérieur</span>
                    <span class="db-extras-team-val">{fnum(a_corners)}</span>
                </div>
            </div>
            <div class="db-extras-summary">
                <div class="db-extras-summary-line">
                    <span class="db-extras-summary-name">Total moyen/match</span>
                    <span class="db-extras-summary-val">{fnum(corners_total_moy)}</span>
                </div>
                <div class="db-extras-summary-line">
                    <span class="db-extras-summary-name">Over 9.5 (moyenne)</span>
                    <span class="db-extras-summary-val">{fpct(corners_o95_moy)}</span>
                </div>
            </div>
        </div>"""
    else:
        corners_block = '<div class="db-extras-block"><div class="db-extras-title">🚩 Corners</div><div class="db-extras-empty">Données non disponibles</div></div>'

    # Bloc Cartons
    if has_cartons:
        cartons_block = f"""
        <div class="db-extras-block">
            <div class="db-extras-title">🟨 Cartons jaunes par match</div>
            <div class="db-extras-teams">
                <div class="db-extras-team">
                    <span class="db-extras-team-label">🏠 Domicile</span>
                    <span class="db-extras-team-val">{fnum(h_yellow)}</span>
                </div>
                <div class="db-extras-team">
                    <span class="db-extras-team-label">✈️ Extérieur</span>
                    <span class="db-extras-team-val">{fnum(a_yellow)}</span>
                </div>
            </div>
            <div class="db-extras-summary">
                <div class="db-extras-summary-line">
                    <span class="db-extras-summary-name">Total moyen/match</span>
                    <span class="db-extras-summary-val">{fnum(yellows_total_moy)}</span>
                </div>
                <div class="db-extras-summary-line">
                    <span class="db-extras-summary-name">Over 3.5 (moyenne)</span>
                    <span class="db-extras-summary-val">{fpct(yellows_o35_moy)}</span>
                </div>
            </div>
        </div>"""
    else:
        cartons_block = '<div class="db-extras-block"><div class="db-extras-title">🟨 Cartons</div><div class="db-extras-empty">Données non disponibles</div></div>'

    return f"""
    <div class="db-section-title">🏟️ Stats détaillées</div>
    <div class="db-extras-row">
        {corners_block}
        {cartons_block}
    </div>"""
def _heat_color(p_pct):
    """Retourne une couleur de fond selon la probabilité (en %).
    Gradient jaune → orange → rouge."""
    if p_pct < 0.5:
        return "rgba(255,255,255,0.02)"
    elif p_pct < 2:
        return "rgba(254,224,144,0.25)"
    elif p_pct < 5:
        return "rgba(253,174,97,0.35)"
    elif p_pct < 8:
        return "rgba(244,109,67,0.5)"
    elif p_pct < 12:
        return "rgba(215,48,39,0.6)"
    else:
        return "rgba(165,0,38,0.75)"


def _section_heatmap(row):
    """Génère la heatmap Poisson 6x6 + résumé top 3 / 1X2 / xG en HTML pur."""
    xg_h = _safe_num(row.get("xG_H"))
    xg_a = _safe_num(row.get("xG_A"))
    if xg_h is None or xg_a is None:
        return ""

    try:
        res = matrice_scores(xg_h, xg_a)
    except Exception:
        return ""

    matrice = res["matrice"]
    top3 = res["top3"]
    p_home = res["p_home"]
    p_draw = res["p_draw"]
    p_away = res["p_away"]

    home_team = _esc(row.get("HomeTeam", "🏠"))
    away_team = _esc(row.get("AwayTeam", "✈️"))

    # Top 3 scores
    top3_html = " · ".join(
        f'<span class="accent">{i}-{j}</span> <strong>({100*p:.1f}%)</strong>'
        for i, j, p in top3
    )

    # Trouver la case la plus probable (pour la surligner)
    max_p = max(matrice[i][j] for i in range(6) for j in range(6))

    # Construire la table HTML 6x6
    head = '<th></th>' + "".join(f'<th>✈️ {j}</th>' for j in range(6))
    rows_html = ""
    for i in range(6):
        row_cells = f'<th>🏠 {i}</th>'
        for j in range(6):
            p = matrice[i][j]
            p_pct = 100 * p
            bg = _heat_color(p_pct)
            is_best = "heat-best" if p == max_p else ""
            row_cells += f'<td class="{is_best}" style="background:{bg};">{p_pct:.1f}</td>'
        rows_html += f'<tr>{row_cells}</tr>'

    return f"""
    <div class="db-section-title">🎯 Heatmap Poisson des scores</div>
    <div class="db-heat-row">
        <div class="db-heat-summary">
            <div class="db-heat-summary-line">🏆 <strong>Top 3 :</strong> {top3_html}</div>
            <div class="db-heat-summary-line">⚖️ <strong>1X2 :</strong> 🏠 {home_team} <strong>{100*p_home:.0f}%</strong> · ⚖️ Nul <strong>{100*p_draw:.0f}%</strong> · ✈️ {away_team} <strong>{100*p_away:.0f}%</strong></div>
            <div class="db-heat-summary-line">🎯 <strong>xG :</strong> 🏠 <strong>{xg_h:.2f}</strong> · ✈️ <strong>{xg_a:.2f}</strong></div>
        </div>
        <div class="db-heat-table-wrap">
            <table class="db-heat-table">
                <thead><tr>{head}</tr></thead>
                <tbody>{rows_html}</tbody>
            </table>
        </div>
        <div class="db-heat-caption">Probabilités en % · cellule la plus probable surlignée · couvre {100*res['couverture']:.0f}% des scores</div>
    </div>"""
# ============================================================
# RENDU D'UNE CARTE
# ============================================================
def rendre_carte_match_html(row, mode_compact=False):
    """
    Génère le HTML <details>/<summary> pour une carte de match.
    Le header contient : heure, ligue, équipes + score + positions, prédiction.
    Le body contient : Poisson, comparaison équipes, H2H.
    """
    is_upcoming = (
        (row.get("Score") == "À VENIR")
        or bool(row.get("IsUpcoming", False))
        or row.get("Score") in (None, "")
    )

    score_raw = row.get("Score", "")
    if is_upcoming:
        score_html = '<span class="db-card-score upcoming">À venir</span>'
    else:
        # Format "1-2" -> "1 — 2" pour respirer
        score_aff = _esc(str(score_raw).replace("-", " — "))
        score_html = f'<span class="db-card-score">{score_aff}</span>'

    h_pos_aff = _fmt_pos(row.get("H_Pos"))
    a_pos_aff = _fmt_pos(row.get("A_Pos"))

    # Prédiction la plus marquante en header (Over 2.5)
    p_o25 = _safe_pct(row.get("P_Over25"))
    pred_html = f'<span class="db-card-pred">{p_o25:.0f}% O2.5</span>' if p_o25 is not None else ""

    # Signaux d'anomalies (à côté des noms si présents)
    h_sig = _esc(row.get("H_Signaux", "")).strip()
    a_sig = _esc(row.get("A_Signaux", "")).strip()
    h_sig_html = f' <span class="db-card-signaux">{h_sig}</span>' if h_sig else ""
    a_sig_html = f' <span class="db-card-signaux">{a_sig}</span>' if a_sig else ""

    # Heure & ligue
    time_aff = _esc(row.get("TimeNY") or row.get("Time") or "—")
    league_aff = _esc(row.get("League", ""))

    # ---- POISSON ----
    poisson_html = f"""
    <div class="db-section-title">🎯 Indice Poisson</div>
    <div class="db-poisson-row">
        {_pois_cell("Over 0.5", row.get("P_Over05"))}
        {_pois_cell("Over 1.5", row.get("P_Over15"))}
        {_pois_cell("Over 2.5", row.get("P_Over25"))}
        {_pois_cell("BTTS",     row.get("P_BTTS"))}
        {_pois_cell("0-0",      row.get("P_00"))}
    </div>"""

    xg_h = _safe_num(row.get("xG_H"))
    xg_a = _safe_num(row.get("xG_A"))
    if xg_h is not None and xg_a is not None:
        xg_html = f"""
        <div class="db-xg-line">
            <span>xG Domicile : <span class="db-xg-num">{xg_h:.2f}</span></span>
            <span>xG Extérieur : <span class="db-xg-num">{xg_a:.2f}</span></span>
        </div>"""
    else:
        xg_html = ""

    # ---- COMPARAISON ÉQUIPES ----
    home_card = f"""
    <div class="db-compare-card home">
        <div class="db-compare-head">
            <div class="db-compare-name">{_esc(row.get('HomeTeam', ''))}</div>
            <div class="db-compare-badge home">Domicile</div>
            {f'<div class="db-compare-signaux">{h_sig}</div>' if h_sig else ''}
        </div>
        <div class="db-form-line">{_form_pills(row.get('H_Form', ''))}</div>
        {_metric_line("Over 0.5", row.get("H_Over05"))}
        {_metric_line("Over 1.5", row.get("H_Over15"))}
        {_metric_line("Over 2.5", row.get("H_Over25"))}
        {_metric_line("BTTS",     row.get("H_BTTS"))}
        {_metric_line("% 0-0",    row.get("H_00_Pct"), is_low_good=True)}
    </div>"""

    away_card = f"""
    <div class="db-compare-card away">
        <div class="db-compare-head">
            <div class="db-compare-name">{_esc(row.get('AwayTeam', ''))}</div>
            <div class="db-compare-badge away">Extérieur</div>
            {f'<div class="db-compare-signaux">{a_sig}</div>' if a_sig else ''}
        </div>
        <div class="db-form-line">{_form_pills(row.get('A_Form', ''))}</div>
        {_metric_line("Over 0.5", row.get("A_Over05"))}
        {_metric_line("Over 1.5", row.get("A_Over15"))}
        {_metric_line("Over 2.5", row.get("A_Over25"))}
        {_metric_line("BTTS",     row.get("A_BTTS"))}
        {_metric_line("% 0-0",    row.get("A_00_Pct"), is_low_good=True)}
    </div>"""

    compare_html = f"""
    <div class="db-section-title">⚖️ Comparaison équipes</div>
    <div class="db-compare-row">
        {home_card}
        {away_card}
    </div>"""

    # ---- H2H ----
    h2h_n_raw = row.get("H2H_N", 0)
    try:
        h2h_n = int(h2h_n_raw) if not pd.isna(h2h_n_raw) else 0
    except (ValueError, TypeError):
        h2h_n = 0

    if h2h_n > 0:
        h2h_avg = _safe_num(row.get("H2H_AvgGoals"))
        h2h_o25 = _safe_pct(row.get("H2H_O25_pct"))
        h2h_btts = _safe_pct(row.get("H2H_BTTS_pct"))
        h2h_00 = _safe_pct(row.get("H2H_00_pct"))

        avg_aff = f"{h2h_avg:.2f}" if h2h_avg is not None else "—"
        o25_aff = f"{h2h_o25:.1f}%" if h2h_o25 is not None else "—"
        btts_aff = f"{h2h_btts:.1f}%" if h2h_btts is not None else "—"
        z00_aff = f"{h2h_00:.1f}%" if h2h_00 is not None else "—"

        h2h_html = f"""
        <div class="db-section-title">⚔️ Confrontations directes</div>
        <div class="db-h2h-row">
            <div class="db-h2h-big">
                <div class="db-h2h-big-num">{h2h_n}</div>
                <div class="db-h2h-big-lab">matchs</div>
            </div>
            <div class="db-h2h-stats">
                <div><div class="db-h2h-st-val">{avg_aff}</div><div class="db-h2h-st-lab">Buts/match</div></div>
                <div><div class="db-h2h-st-val">{o25_aff}</div><div class="db-h2h-st-lab">Over 2.5</div></div>
                <div><div class="db-h2h-st-val">{btts_aff}</div><div class="db-h2h-st-lab">BTTS</div></div>
                <div><div class="db-h2h-st-val">{z00_aff}</div><div class="db-h2h-st-lab">0-0</div></div>
            </div>
        </div>"""
    else:
        h2h_html = """
        <div class="db-section-title">⚔️ Confrontations directes</div>
        <div class="db-h2h-empty">Aucune confrontation passée trouvée entre ces 2 équipes.</div>"""

    # ---- ASSEMBLAGE ----
    return _minify_html(f"""<details class="db-card">
    <summary>
        <div class="db-card-meta">
            <div class="db-card-time">{time_aff}</div>
            <div class="db-card-league">{league_aff}</div>
        </div>
        <div class="db-card-teams">
            <span class="db-card-team-name">{_esc(row.get('HomeTeam', ''))}</span>{h_sig_html}
            <span class="db-card-pos">{h_pos_aff}</span>
            {score_html}
            <span class="db-card-pos">{a_pos_aff}</span>
            <span class="db-card-team-name">{_esc(row.get('AwayTeam', ''))}</span>{a_sig_html}
        </div>
        <div class="db-card-right">
            {pred_html}
            <span class="db-card-arrow">▾</span>
        </div>
    </summary>
    <div class="db-card-body">
        {poisson_html}
        {xg_html}
        {compare_html}
        {_section_extras(row)}
        {_section_heatmap(row)}
        {h2h_html}
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
