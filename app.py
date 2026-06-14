import streamlit as st
import json, os, requests
from datetime import datetime

st.set_page_config(
    page_title="White Family In France · World Cup 2026",
    page_icon="⚽",
    layout="wide",
)

# ─────────────────────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;500;600;700&family=Space+Mono:wght@400;700&display=swap');
*, *::before, *::after { box-sizing: border-box; }
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    font-family: 'Inter', sans-serif !important;
    background: #08080f !important;
    color: #e8e4dc !important;
}
[data-testid="stSidebar"] { display: none !important; }
.block-container { padding: 0 0 6rem 0 !important; max-width: 100% !important; }
[data-testid="stMain"] { padding-top: 0 !important; }

.hero {
    width: 100%;
    min-height: 320px;
    position: relative;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #08080f;
}
.hero::before {
    content: '';
    position: absolute;
    inset: 0;
    background: repeating-linear-gradient(
        180deg,
        rgba(16,80,30,0.55) 0px, rgba(16,80,30,0.55) 44px,
        rgba(12,60,22,0.55) 44px, rgba(12,60,22,0.55) 88px
    );
    z-index: 0;
}
.hero::after {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse 80% 70% at 50% 50%,
        transparent 30%,
        rgba(8,8,15,0.85) 100%);
    z-index: 1;
}
.hero-inner {
    position: relative;
    z-index: 5;
    text-align: center;
    padding: 3rem 2rem 3.5rem;
    width: 100%;
}
.hero-eyebrow {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.38em;
    text-transform: uppercase;
    color: rgba(255,255,255,0.35);
    margin-bottom: 1.1rem;
}
.hero-badge {
    display: inline-flex;
    flex-direction: column;
    align-items: center;
}
.hero-family {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(3.2rem, 9vw, 7rem);
    color: #ffffff;
    letter-spacing: 0.04em;
    line-height: 0.88;
    text-shadow: 0 4px 40px rgba(0,0,0,0.8);
}
.hero-accent-bar {
    width: 100%;
    height: 5px;
    border-radius: 2px;
    background: linear-gradient(90deg,
        #002395 0%, #002395 33%,
        #ffffff 33%, #ffffff 66%,
        #ED2939 66%, #ED2939 100%);
    margin: 6px 0 8px;
}
.hero-subtitle {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(1.4rem, 3.5vw, 2.4rem);
    color: rgba(255,220,80,0.9);
    letter-spacing: 0.18em;
    line-height: 1;
}
.hero-flags {
    font-size: 1.5rem;
    letter-spacing: 0.55rem;
    margin-top: 1rem;
    opacity: 0.7;
}
.nalex-stamp {
    position: absolute;
    bottom: 16px;
    right: 22px;
    z-index: 6;
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 1px;
}
.nalex-by {
    font-family: 'Space Mono', monospace;
    font-size: 0.5rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: rgba(0, 70, 140, 1);
}
.nalex-name {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.15rem;
    letter-spacing: 0.22em;
    color: rgba(0, 70, 140, 1);
    line-height: 1;
}

.stat-strip-wrap {
    max-width: 1120px;
    margin: 0 auto;
    padding: 1rem 1.4rem 0;
}
.stat-strip {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    align-items: center;
    padding: 0.8rem 1.1rem;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px;
    margin-bottom: 1.6rem;
}
.s-chip {
    display: flex;
    align-items: baseline;
    gap: 5px;
    padding: 3px 12px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 100px;
}
.s-val {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.1rem;
    letter-spacing: 0.06em;
    color: #fff;
}
.s-val.live-col { color: #4ade80; }
.s-lbl {
    font-size: 0.68rem;
    color: rgba(255,255,255,0.28);
    letter-spacing: 0.06em;
}
.api-ok  { font-size: 0.68rem; color: #4ade80; letter-spacing: 0.08em; text-transform: uppercase; font-family: 'Space Mono', monospace; }
.api-err { font-size: 0.68rem; color: #f87171; letter-spacing: 0.08em; text-transform: uppercase; font-family: 'Space Mono', monospace; }

.s-head {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    font-weight: 700;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: rgba(255,255,255,0.22);
    margin-bottom: 0.9rem;
    padding-bottom: 0.45rem;
    border-bottom: 1px solid rgba(255,255,255,0.06);
}
.lb {
    border-radius: 16px;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.07);
    margin-bottom: 1.8rem;
    background: rgba(0,0,0,0.3);
}
.lb-r {
    display: flex;
    align-items: center;
    padding: 14px 18px;
    gap: 13px;
    border-bottom: 1px solid rgba(255,255,255,0.04);
}
.lb-r:last-child { border-bottom: none; }
.lb-r.top1 { background: rgba(245,193,20,0.05); }
.lb-num {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.3rem;
    letter-spacing: 0.06em;
    width: 26px;
    text-align: center;
    color: rgba(255,255,255,0.15);
}
.lb-num.n1 { color: #f5c114; }
.lb-num.n2 { color: #9ca3af; }
.lb-num.n3 { color: #b45309; }
.lb-av {
    width: 40px; height: 40px;
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1rem;
}
.lb-name {
    flex: 1;
    font-size: 0.95rem;
    font-weight: 600;
    color: #e8e4dc;
}
.lb-bar-wrap { flex: 1.8; }
.lb-bar-bg { height: 3px; background: rgba(255,255,255,0.07); border-radius: 2px; overflow: hidden; }
.lb-bar-fill { height: 3px; border-radius: 2px; transition: width 0.5s ease; }
.lb-pts-wrap { min-width: 62px; text-align: right; }
.lb-pts {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.7rem;
    letter-spacing: 0.04em;
    color: #f5c114;
    line-height: 1;
}
.lb-ptslbl {
    font-size: 0.58rem;
    color: rgba(255,255,255,0.2);
    letter-spacing: 0.08em;
    margin-left: 2px;
}
.pred-card {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 1.4rem 1.3rem 1rem;
    margin-bottom: 1.8rem;
}
.match-hero {
    text-align: center;
    padding: 0.9rem 0 1.1rem;
}
.match-hero-teams {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(1.6rem, 4vw, 2.4rem);
    color: #fff;
    letter-spacing: 0.06em;
    line-height: 1.05;
}
.match-hero-vs {
    font-family: 'Space Mono', monospace;
    font-size: 0.58rem;
    color: rgba(255,255,255,0.2);
    background: rgba(255,255,255,0.05);
    padding: 2px 9px;
    border-radius: 100px;
    margin: 0 10px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}
.match-hero-date {
    font-family: 'Space Mono', monospace;
    font-size: 0.62rem;
    color: rgba(255,255,255,0.25);
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-top: 5px;
}
.p-chip {
    display: inline-block;
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 6px;
    border: 1px solid;
    letter-spacing: 0.04em;
    margin: 2px 3px 2px 0;
}
.c-win  { background: rgba(74,222,128,0.08); color: #4ade80; border-color: rgba(74,222,128,0.22); }
.c-lose { background: rgba(248,113,113,0.08); color: #f87171; border-color: rgba(248,113,113,0.22); }
.c-pend { background: rgba(255,255,255,0.04); color: rgba(255,255,255,0.32); border-color: rgba(255,255,255,0.09); }

.stage-hd {
    font-family: 'Space Mono', monospace;
    font-size: 0.58rem;
    font-weight: 700;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: rgba(255,255,255,0.18);
    margin: 1.5rem 0 0.5rem;
    display: flex;
    align-items: center;
    gap: 0.8rem;
}
.stage-hd::after { content: ''; flex: 1; height: 1px; background: rgba(255,255,255,0.06); }
.m-card {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.06);
    border-left: 3px solid rgba(255,255,255,0.06);
    border-radius: 10px;
    padding: 10px 14px;
    margin-bottom: 6px;
}
.m-card.m-live {
    border-left-color: #4ade80;
    background: rgba(5,20,10,0.6);
}
.m-card.m-done {
    border-left-color: rgba(245,193,20,0.3);
    opacity: 0.8;
}
.m-row { display: flex; align-items: center; justify-content: space-between; gap: 8px; }
.m-teams {
    font-size: 0.88rem;
    font-weight: 600;
    color: #c8c4bc;
}
.m-sep {
    font-size: 0.58rem;
    color: rgba(255,255,255,0.18);
    background: rgba(255,255,255,0.04);
    padding: 1px 7px;
    border-radius: 100px;
    margin: 0 5px;
    font-family: 'Space Mono', monospace;
}
.m-score {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.1rem;
    letter-spacing: 0.1em;
    color: #f5c114;
    background: rgba(245,193,20,0.07);
    border: 1px solid rgba(245,193,20,0.14);
    padding: 2px 12px;
    border-radius: 6px;
    white-space: nowrap;
}
.m-upcoming {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    color: rgba(255,255,255,0.22);
    white-space: nowrap;
}
.m-grp { font-size: 0.58rem; color: rgba(245,193,20,0.3); margin-left: 5px; font-family: 'Space Mono', monospace; }
.live-dot {
    display: inline-block;
    width: 6px; height: 6px;
    background: #4ade80;
    border-radius: 50%;
    margin-right: 5px;
    vertical-align: middle;
    animation: pulse 1.5s infinite;
}
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.15} }
.m-preds { margin-top: 7px; display: flex; flex-wrap: wrap; gap: 3px; }

div[data-testid="stSelectbox"] > label,
div[data-testid="stRadio"] > label {
    color: rgba(255,255,255,0.35) !important;
    font-size: 0.65rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.16em !important;
    font-family: 'Space Mono', monospace !important;
    font-weight: 700 !important;
}
div[data-testid="stSelectbox"] > div > div {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: #e8e4dc !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
}
div[data-testid="stRadio"] label {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.09) !important;
    border-radius: 10px !important;
    padding: 10px 16px !important;
    color: #ffffff !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    text-transform: none !important;
    letter-spacing: 0 !important;
    font-family: 'Inter', sans-serif !important;
}
div[data-testid="stRadio"] label[data-selected="true"],
div[data-testid="stRadio"] label[aria-checked="true"] {
    background: rgba(245,193,20,0.1) !important;
    border-color: rgba(245,193,20,0.35) !important;
    color: #f5c114 !important;
}
div[data-testid="stRadio"] div[role="radiogroup"] { gap: 8px !important; }
.stButton > button {
    background: #f5c114 !important;
    color: #0a0a0a !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 1.1rem !important;
    letter-spacing: 0.14em !important;
    padding: 12px 28px !important;
}
.stButton > button:hover { opacity: 0.88 !important; }
div[data-testid="stExpander"] {
    background: rgba(0,0,0,0.22) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 12px !important;
}
hr { border-color: rgba(255,255,255,0.05) !important; margin: 1.4rem 0 !important; }

.grp-wrap {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
    gap: 0.75rem;
    margin-bottom: 1.8rem;
}
.grp-card {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    overflow: hidden;
}
.grp-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 0.95rem;
    letter-spacing: 0.18em;
    color: rgba(245,193,20,0.85);
    padding: 8px 14px 7px;
    background: rgba(245,193,20,0.05);
    border-bottom: 1px solid rgba(245,193,20,0.1);
}
.grp-table {
    width: 100%;
    border-collapse: collapse;
}
.grp-table th {
    font-family: 'Space Mono', monospace;
    font-size: 0.52rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: rgba(255,255,255,0.2);
    padding: 5px 8px;
    text-align: center;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}
.grp-table th.th-team { text-align: left; padding-left: 14px; }
.grp-table td {
    font-size: 0.78rem;
    color: rgba(255,255,255,0.6);
    padding: 7px 8px;
    text-align: center;
    border-bottom: 1px solid rgba(255,255,255,0.03);
    font-family: 'Space Mono', monospace;
}
.grp-table tr:last-child td { border-bottom: none; }
.grp-table td.td-team {
    text-align: left;
    padding-left: 14px;
    font-family: 'Inter', sans-serif;
    font-size: 0.82rem;
    font-weight: 600;
    color: #e8e4dc;
}
.grp-table td.td-pts {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1rem;
    color: #f5c114;
    letter-spacing: 0.06em;
}
.grp-table tr.grp-qualify { background: rgba(74,222,128,0.04); }
.grp-pos {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 0.85rem;
    color: rgba(255,255,255,0.18);
    width: 18px;
    text-align: right;
    padding-right: 6px !important;
}
.grp-pos.gp1, .grp-pos.gp2 { color: rgba(74,222,128,0.5); }
</style>
""", unsafe_allow_html=True)

PLAYERS = ["Alex", "Dad", "Elena", "Mum"]
COLORS = {
    "Alex":  {"bg": "#0f2050", "tx": "#7ab0f5", "bar": "#3b82f6"},
    "Elena": {"bg": "#062b1e", "tx": "#5dce9a", "bar": "#10b981"},
    "Mum":   {"bg": "#3d1005", "tx": "#f5a87a", "bar": "#f97316"},
    "Dad":   {"bg": "#280e40", "tx": "#c09ef5", "bar": "#a855f7"},
}
RANK_CLS = ["n1", "n2", "n3", ""]
RANK_SYMS = ["1", "2", "3", "4"]
DATA_FILE = "data.json"   # only used for local dev fallback
API_BASE = "https://api.football-data.org/v4"

# ─────────────────────────────────────────────────────────────────────────────
# PERSISTENT STORAGE VIA GITHUB GIST
# Reads GIST_ID and GITHUB_TOKEN from st.secrets (set these in Streamlit Cloud
# settings) or from environment variables (for local dev).
# The Gist must contain a file called data.json.
# ─────────────────────────────────────────────────────────────────────────────

def _gist_creds():
    """Return (gist_id, token) from st.secrets or env."""
    try:
        gist_id = st.secrets["GIST_ID"]
        token   = st.secrets["GITHUB_TOKEN"]
    except Exception:
        gist_id = os.environ.get("GIST_ID", "")
        token   = os.environ.get("GITHUB_TOKEN", "")
    return gist_id.strip(), token.strip()

def load():
    """Load predictions from GitHub Gist, falling back to local file."""
    gist_id, token = _gist_creds()
    empty = {"predictions": {}, "points": {p: 0 for p in PLAYERS}}

    if gist_id and token:
        try:
            r = requests.get(
                f"https://api.github.com/gists/{gist_id}",
                headers={
                    "Authorization": f"token {token}",
                    "Accept": "application/vnd.github+json",
                },
                timeout=10,
            )
            if r.status_code == 200:
                raw_content = r.json()["files"]["data.json"]["content"]
                return json.loads(raw_content)
            else:
                st.warning(f"Gist load failed ({r.status_code}), using local fallback.")
        except Exception as e:
            st.warning(f"Gist load error: {e}, using local fallback.")

    # Local fallback (works in VS Code / local dev even without Gist creds)
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            return json.load(f)
    return empty

def save(d):
    """Save predictions to GitHub Gist (cloud) and local file (local dev)."""
    gist_id, token = _gist_creds()
    payload = json.dumps(d, indent=2)

    if gist_id and token:
        try:
            r = requests.patch(
                f"https://api.github.com/gists/{gist_id}",
                headers={
                    "Authorization": f"token {token}",
                    "Accept": "application/vnd.github+json",
                    "Content-Type": "application/json",
                },
                data=json.dumps({
                    "files": {
                        "data.json": {"content": payload}
                    }
                }),
                timeout=10,
            )
            if r.status_code not in (200, 201):
                st.warning(f"Gist save failed ({r.status_code}).")
        except Exception as e:
            st.warning(f"Gist save error: {e}.")

    # Always keep a local copy too (harmless in cloud, useful locally)
    with open(DATA_FILE, "w") as f:
        f.write(payload)

# ─────────────────────────────────────────────────────────────────────────────

if "selected_match_id" not in st.session_state:
    st.session_state.selected_match_id = None
if "selected_player" not in st.session_state:
    st.session_state.selected_player = PLAYERS[0]
if "selected_outcome" not in st.session_state:
    st.session_state.selected_outcome = "home"

def get_api_key():
    try:
        return st.secrets["FOOTBALL_API_KEY"].strip()
    except Exception:
        pass
    key = os.environ.get("FOOTBALL_API_KEY", "")
    if not key and os.path.exists(".env"):
        with open(".env") as f:
            for line in f:
                if line.startswith("FOOTBALL_API_KEY="):
                    key = line.strip().split("=", 1)[1]
    return key.strip()

@st.cache_data(ttl=120)
def fetch_matches():
    key = get_api_key()
    if not key:
        return None, "No API key"
    try:
        r = requests.get(
            f"{API_BASE}/competitions/WC/matches?season=2026",
            headers={"X-Auth-Token": key},
            timeout=10,
        )
        if r.status_code == 200:
            return r.json().get("matches", []), None
        return None, f"Error {r.status_code}"
    except Exception as e:
        return None, str(e)

def parse_match(m):
    home = m["homeTeam"].get("name") or m["homeTeam"].get("shortName", "TBD")
    away = m["awayTeam"].get("name") or m["awayTeam"].get("shortName", "TBD")
    full = m.get("score", {}).get("fullTime", {})
    try:
        ds = datetime.strptime(m.get("utcDate", "")[:10], "%Y-%m-%d").strftime("%d %b")
    except:
        ds = m.get("utcDate", "")[:10]

    grp_raw = m.get("group", "") or ""
    grp_short = grp_raw.replace("GROUP_", "") if grp_raw else ""

    return {
        "id": m["id"],
        "home": home,
        "away": away,
        "date": ds,
        "status": m.get("status", "SCHEDULED"),
        "hs": full.get("home"),
        "as": full.get("away"),
        "stage": m.get("stage", "GROUP_STAGE"),
        "group": grp_short
    }

def result(h, a):
    if h is None or a is None:
        return None
    return "home" if h > a else ("away" if a > h else "draw")

def calc_pts(pred, m):
    actual = result(m["hs"], m["as"])
    if not actual:
        return 0
    pts = 0
    if pred["outcome"] == actual:
        pts += 3
        if pred.get("hs") == m["hs"] and pred.get("as") == m["as"]:
            pts += 1
    return pts

def recalc(data, matches):
    totals = {p: 0 for p in PLAYERS}
    for m in matches:
        if m["status"] != "FINISHED":
            continue
        for p in PLAYERS:
            pr = data["predictions"].get(f"{m['id']}:{p}")
            if pr:
                totals[p] += calc_pts(pr, m)
    data["points"] = totals

def build_group_standings(matches):
    """Build group standings from finished match results."""
    groups = {}
    for m in matches:
        grp = m.get("group")
        if not grp or m.get("stage") != "GROUP_STAGE":
            continue
        if grp not in groups:
            groups[grp] = {}
        for team, opp, gs, ga in [
            (m["home"], m["away"], m["hs"], m["as"]),
            (m["away"], m["home"], m["as"], m["hs"]),
        ]:
            if team not in groups[grp]:
                groups[grp][team] = {"P": 0, "W": 0, "D": 0, "L": 0, "GF": 0, "GA": 0, "GD": 0, "Pts": 0}
            row = groups[grp][team]
            if m["status"] == "FINISHED" and gs is not None and ga is not None:
                row["P"] += 1
                row["GF"] += gs
                row["GA"] += ga
                row["GD"] += gs - ga
                if gs > ga:
                    row["W"] += 1
                    row["Pts"] += 3
                elif gs == ga:
                    row["D"] += 1
                    row["Pts"] += 1
                else:
                    row["L"] += 1
    # Sort each group by Pts desc, then GD desc, then GF desc
    sorted_groups = {}
    for grp, teams in sorted(groups.items()):
        sorted_groups[grp] = sorted(
            teams.items(),
            key=lambda x: (x[1]["Pts"], x[1]["GD"], x[1]["GF"]),
            reverse=True
        )
    return sorted_groups

def ol(o):
    return {"home": "Home wins", "away": "Away wins", "draw": "Draw"}.get(o, o)

data = load()
raw, api_err = fetch_matches()

if not raw:
    st.error(f"Could not load live matches: {api_err}")
    st.stop()

matches = [parse_match(m) for m in raw]
recalc(data, matches)
save(data)

played = sum(1 for m in matches if m["status"] == "FINISHED")
live_now = sum(1 for m in matches if m["status"] in ("IN_PLAY", "PAUSED"))
upcoming = sum(1 for m in matches if m["status"] in ("SCHEDULED", "TIMED"))
top_pts = max(data["points"].values()) if any(data["points"].values()) else 0

st.markdown("""
<div class="hero">
  <div class="hero-inner">
    <div class="hero-eyebrow">White Family In France · World Cup 2026 </div>
    <div class="hero-badge">
      <div class="hero-family">WHITE FAMILY</div>
      <div class="hero-accent-bar"></div>
      <div class="hero-subtitle">World Cup 2026 · Predictor</div>
  </div>
  <div class="nalex-stamp">
    <span class="nalex-by">Made by</span>
    <span class="nalex-name">NALEX</span>
  </div>
</div>
""", unsafe_allow_html=True)

api_ind = '<span class="api-ok">✔ Live data</span>'
st.markdown(f"""
<div class="stat-strip-wrap">
<div class="stat-strip">
  <div class="s-chip"><span class="s-val">{played}</span><span class="s-lbl">played</span></div>
  <div class="s-chip"><span class="s-val live-col">{live_now}</span><span class="s-lbl">live</span></div>
  <div class="s-chip"><span class="s-val">{upcoming}</span><span class="s-lbl">upcoming</span></div>
  <div class="s-chip"><span class="s-val">{top_pts}</span><span class="s-lbl">top pts</span></div>
  {api_ind}
</div>
</div>
""", unsafe_allow_html=True)

col_l, col_r = st.columns([1, 1], gap="large")

with col_l:
    st.markdown('<div class="s-head">Standings</div>', unsafe_allow_html=True)
    ranked = sorted(PLAYERS, key=lambda p: data["points"][p], reverse=True)
    rows = ""
    for i, p in enumerate(ranked):
        pts = data["points"][p]
        c = COLORS[p]
        pct = int(pts / top_pts * 100) if top_pts else 0
        top_cls = "top1" if i == 0 else ""
        rows += f"""
        <div class="lb-r {top_cls}">
          <div class="lb-num {RANK_CLS[i]}">{RANK_SYMS[i]}</div>
          <div class="lb-av" style="background:{c['bg']};color:{c['tx']};border:1px solid {c['bar']}33">{p[:2].upper()}</div>
          <div class="lb-name">{p}</div>
          <div class="lb-bar-wrap">
            <div class="lb-bar-bg">
              <div class="lb-bar-fill" style="width:{pct}%;background:{c['bar']}"></div>
            </div>
          </div>
          <div class="lb-pts-wrap">
            <span class="lb-pts">{pts}</span><span class="lb-ptslbl">pts</span>
          </div>
        </div>"""
    st.markdown(f'<div class="lb">{rows}</div>', unsafe_allow_html=True)

    with st.expander("Match-by-match breakdown"):
        for p in PLAYERS:
            c = COLORS[p]
            st.markdown(
                f"<span style='color:{c['tx']};font-family:Bebas Neue,sans-serif;font-size:1.1rem;letter-spacing:0.08em'>{p}</span>"
                f" <span style='color:rgba(255,255,255,0.22);font-size:0.78rem'>— {data['points'][p]} pts</span>",
                unsafe_allow_html=True
            )
            chips = []
            for m in matches:
                pr = data["predictions"].get(f"{m['id']}:{p}")
                if not pr:
                    continue
                if m["status"] == "FINISHED":
                    pe = calc_pts(pr, m)
                    chips.append(f'<span class="p-chip {"c-win" if pe > 0 else "c-lose"}">{m["home"][:3]} v {m["away"][:3]} +{pe}</span>')
                else:
                    chips.append(f'<span class="p-chip c-pend">{m["home"][:3]} v {m["away"][:3]}</span>')
            if chips:
                st.markdown('<div style="margin:4px 0 12px">' + ' '.join(chips) + '</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div style="color:rgba(255,255,255,0.2);font-size:0.78rem;margin-bottom:12px">No predictions yet</div>', unsafe_allow_html=True)

    st.markdown('<div class="s-head">Make a Prediction</div>', unsafe_allow_html=True)

    predictable = [m for m in matches if m["status"] in ("SCHEDULED", "TIMED", "IN_PLAY", "PAUSED")]

    if not predictable:
        st.error("API returned matches, but none are currently scheduled/timed/live. Check the API response.")
    else:
        match_ids = [m["id"] for m in predictable]
        if st.session_state.selected_match_id not in match_ids:
            st.session_state.selected_match_id = match_ids[0]
        default_index = match_ids.index(st.session_state.selected_match_id)

        labels = [
            f"{'🔴 ' if m['status'] in ('IN_PLAY','PAUSED') else ''}{m['home']} vs {m['away']} · {m['date']}"
            for m in predictable
        ]

        c1, c2 = st.columns(2)
        with c1:
            sel_player = st.selectbox(
                "Your name",
                PLAYERS,
                index=PLAYERS.index(st.session_state.selected_player),
                key="player_picker",
            )
            st.session_state.selected_player = sel_player

        with c2:
            chosen_lbl = st.selectbox(
                "Match",
                labels,
                index=default_index,
                key="match_picker",
            )
            sel_match = predictable[labels.index(chosen_lbl)]
            st.session_state.selected_match_id = sel_match["id"]

        st.markdown('<div class="pred-card">', unsafe_allow_html=True)
        m = sel_match
        live_tag = '<span class="live-dot"></span>' if m["status"] in ("IN_PLAY", "PAUSED") else ""
        st.markdown(f"""
        <div class="match-hero">
          <div class="match-hero-date">{live_tag}{m['date']}</div>
          <div class="match-hero-teams">
            {m['home']}<span class="match-hero-vs">vs</span>{m['away']}
          </div>
        </div>
        """, unsafe_allow_html=True)

        outcome_choice = st.radio(
            "Your prediction",
            options=["home", "draw", "away"],
            format_func=lambda o: {
                "home": f"🏠  {m['home']} wins",
                "draw": "🤝  Draw",
                "away": f"✈️  {m['away']} wins",
            }[o],
            horizontal=True,
            key="selected_outcome",
        )

        pred_key = f"{m['id']}:{sel_player}"
        existing = data["predictions"].get(pred_key)
        if existing:
            st.info(f"You already picked **{ol(existing['outcome'])}** — saving overwrites it.")

        if st.button("⚽  Save Prediction", use_container_width=True):
            data["predictions"][pred_key] = {"outcome": outcome_choice}
            recalc(data, matches)
            save(data)
            st.success(f"Saved! {sel_player} → {ol(outcome_choice)} · {m['home']} vs {m['away']}")
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div style="height:0.4rem"></div>', unsafe_allow_html=True)
    st.markdown('<div class="s-head">Group Standings</div>', unsafe_allow_html=True)

    group_standings = build_group_standings(matches)
    if group_standings:
        grp_html = '<div class="grp-wrap">'
        for grp, teams in group_standings.items():
            grp_html += f'''
            <div class="grp-card">
              <div class="grp-title">Group {grp}</div>
              <table class="grp-table">
                <thead>
                  <tr>
                    <th></th>
                    <th class="th-team">Team</th>
                    <th>P</th>
                    <th>W</th>
                    <th>D</th>
                    <th>L</th>
                    <th>GD</th>
                    <th>Pts</th>
                  </tr>
                </thead>
                <tbody>'''
            for i, (team, row) in enumerate(teams):
                qualify_cls = "grp-qualify" if i < 2 else ""
                pos_cls = f"gp{i+1}" if i < 2 else ""
                gd = f"+{row['GD']}" if row['GD'] > 0 else str(row['GD'])
                grp_html += f'''
                  <tr class="{qualify_cls}">
                    <td class="grp-pos {pos_cls}">{i+1}</td>
                    <td class="td-team">{team}</td>
                    <td>{row['P']}</td>
                    <td>{row['W']}</td>
                    <td>{row['D']}</td>
                    <td>{row['L']}</td>
                    <td>{gd}</td>
                    <td class="td-pts">{row['Pts']}</td>
                  </tr>'''
            grp_html += '</tbody></table></div>'
        grp_html += '</div>'
        st.markdown(grp_html, unsafe_allow_html=True)
    else:
        st.markdown('<div style="color:rgba(255,255,255,0.2);font-size:0.78rem;margin-bottom:12px">Group stage matches not started yet.</div>', unsafe_allow_html=True)

with col_r:
    st.markdown('<div class="s-head">All Matches</div>', unsafe_allow_html=True)
    if st.button("↺ Refresh scores", key="rb"):
        st.cache_data.clear()
        st.rerun()

    for m in matches:
        st.write(f"{m['home']} vs {m['away']} — ID: {m['id']}")

    STAGE_ORDER = ["GROUP_STAGE", "ROUND_OF_32", "LAST_16", "QUARTER_FINALS", "SEMI_FINALS", "THIRD_PLACE", "FINAL"]
    STAGE_LABELS = {
        "GROUP_STAGE": "Group Stage",
        "ROUND_OF_32": "Round of 32",
        "LAST_16": "Round of 16",
        "QUARTER_FINALS": "Quarter-finals",
        "SEMI_FINALS": "Semi-finals",
        "THIRD_PLACE": "3rd Place",
        "FINAL": "Final",
    }

    for stage in STAGE_ORDER:
        sms = [m for m in matches if m.get("stage") == stage]
        if not sms:
            continue
        st.markdown(f'<div class="stage-hd">{STAGE_LABELS.get(stage, stage)}</div>', unsafe_allow_html=True)
        for m in sms:
            is_live = m["status"] in ("IN_PLAY", "PAUSED")
            is_done = m["status"] == "FINISHED"
            cls = "m-live" if is_live else ("m-done" if is_done else "")

            if is_done or is_live:
                hs = m["hs"] if m["hs"] is not None else "–"
                as_ = m["as"] if m["as"] is not None else "–"
                right = f'<span class="m-score">{hs} – {as_}</span>'
            else:
                right = f'<span class="m-upcoming">{m["date"]}</span>'

            ld = '<span class="live-dot"></span>' if is_live else ""
            grp = f'<span class="m-grp">Group {m["group"]}</span>' if m.get("group") else ""

            pred_chips = ""
            for p in PLAYERS:
                pr = data["predictions"].get(f"{m['id']}:{p}")
                if pr:
                    if is_done:
                        pe = calc_pts(pr, m)
                        pred_chips += f'<span class="p-chip {"c-win" if pe > 0 else "c-lose"}">{p} +{pe}</span> '
                    else:
                        pred_chips += f'<span class="p-chip c-pend">{p}</span> '

            preds_row = f'<div class="m-preds">{pred_chips}</div>' if pred_chips else ""

            st.markdown(f"""
            <div class="m-card {cls}">
              <div class="m-row">
                <div class="m-teams">{ld}{m['home']}<span class="m-sep">vs</span>{m['away']}{grp}</div>
                {right}
              </div>
              {preds_row}
            </div>
            """, unsafe_allow_html=True)
