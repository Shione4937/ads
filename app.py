import streamlit as st
from pathlib import Path
import sys
import base64
sys.path.insert(0, str(Path(__file__).parent))
from loader import get_clients, ALL_CLIENTS, DEFAULT_SELECTED

st.set_page_config(page_title="AdBoard", layout="wide")

ROOT = Path(__file__).parent

# ─── アイコン画像をbase64化 ───
def load_icon_b64(filename):
    path = ROOT / "assets" / "icons" / filename
    if path.exists():
        return base64.b64encode(path.read_bytes()).decode("utf-8")
    return ""

ICONS_B64 = {
    "分析":     load_icon_b64("nav_analytics.png"),
    "広告管理": load_icon_b64("nav_campaign.png"),
    "予算設定": load_icon_b64("nav_budget.png"),
    "全体設定": load_icon_b64("nav_settings.png"),
}

# ─── セッションステート初期化 ───
if "selected_clients" not in st.session_state:
    st.session_state["selected_clients"] = DEFAULT_SELECTED
if "client" not in st.session_state:
    st.session_state["client"] = DEFAULT_SELECTED[0]
if "period" not in st.session_state:
    st.session_state["period"] = "今月（4月）"
if "section" not in st.session_state:
    st.session_state["section"] = "分析"
if "submit_step" not in st.session_state:
    st.session_state["submit_step"] = 1
if "submit_data" not in st.session_state:
    st.session_state["submit_data"] = {}

# ─── セクション別カラーパレット ───
SECTION_THEMES = {
    "分析": {
        "primary":       "#6366f1",
        "primary_dark":  "#4f46e5",
        "primary_light": "#f5f3ff",
        "primary_50":    "#fafbff",
        "gradient":      "linear-gradient(135deg, #7c3aed, #6366f1)",
        "gradient_soft": "linear-gradient(90deg, #ede9fe 0%, #e0e7ff 50%, #dbeafe 100%)",
        "underline":     "linear-gradient(90deg, #c4b5fd, #818cf8, #7dd3fc)",
        "shadow":        "rgba(99,102,241,0.3)",
        "shadow_light":  "rgba(99,102,241,0.08)",
        "icon":          "analytics",
    },
    "広告管理": {
        "primary":       "#0ea5e9",
        "primary_dark":  "#0284c7",
        "primary_light": "#e0f2fe",
        "primary_50":    "#f0f9ff",
        "gradient":      "linear-gradient(135deg, #38bdf8, #0ea5e9)",
        "gradient_soft": "linear-gradient(90deg, #e0f2fe 0%, #cffafe 50%, #e0f7fa 100%)",
        "underline":     "linear-gradient(90deg, #7dd3fc, #38bdf8, #06b6d4)",
        "shadow":        "rgba(14,165,233,0.3)",
        "shadow_light":  "rgba(14,165,233,0.08)",
        "icon":          "campaign",
    },
    "予算設定": {
        "primary":       "#f59e0b",
        "primary_dark":  "#d97706",
        "primary_light": "#fef3c7",
        "primary_50":    "#fffbeb",
        "gradient":      "linear-gradient(135deg, #fbbf24, #f59e0b)",
        "gradient_soft": "linear-gradient(90deg, #fef3c7 0%, #fed7aa 50%, #fef9c3 100%)",
        "underline":     "linear-gradient(90deg, #fcd34d, #f59e0b, #f97316)",
        "shadow":        "rgba(245,158,11,0.3)",
        "shadow_light":  "rgba(245,158,11,0.08)",
        "icon":          "savings",
    },
    "全体設定": {
        "primary":       "#64748b",
        "primary_dark":  "#475569",
        "primary_light": "#f1f5f9",
        "primary_50":    "#f8fafc",
        "gradient":      "linear-gradient(135deg, #94a3b8, #64748b)",
        "gradient_soft": "linear-gradient(90deg, #f1f5f9 0%, #e2e8f0 50%, #f1f5f9 100%)",
        "underline":     "linear-gradient(90deg, #cbd5e1, #94a3b8, #64748b)",
        "shadow":        "rgba(100,116,139,0.3)",
        "shadow_light":  "rgba(100,116,139,0.08)",
        "icon":          "settings",
    },
}

THEME = SECTION_THEMES[st.session_state["section"]]

# ─── グローバルCSS（テーマ適用） ───
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Sans+JP:wght@400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/icon?family=Material+Icons');

html, body, [class*="css"] {{
    font-family: 'Inter', 'Noto Sans JP', sans-serif;
}}

header[data-testid="stHeader"] {{
    display: none !important;
}}

/* ===== 背景色（全幅2層：上=白 / 下=グレー） ===== */
/* ブラウザ全幅で上は白、下は #f4f7fa を出すために linear-gradient を使用 */
.stApp {{
    background: linear-gradient(to bottom, #ffffff 0px, #ffffff 130px, #f4f7fa 130px, #f4f7fa 100%) !important;
    background-attachment: fixed !important;
}}
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.main {{
    background: transparent !important;
}}

.block-container {{
    padding-top: 0 !important;
    padding-bottom: 1rem !important;
    margin-top: 0 !important;
    background: transparent !important;
}}
/* Streamlitのデフォルト上部スペースを削除 */
[data-testid="stAppViewContainer"] > .main {{
    padding-top: 0 !important;
}}
[data-testid="stMain"] > div:first-child {{
    padding-top: 0 !important;
    margin-top: 0 !important;
}}

/* タブコンテンツ内は透明（背後のグレーが透ける） */
[role="tabpanel"] {{
    background: transparent !important;
    padding-top: 12px !important;
}}

/* ===== ロゴ（Ad紫+Board青） ===== */
.adboard-logo-wrap {{
    display: inline-block;
    padding: 0;
}}
.adboard-logo-text {{
    font-size: 30px;
    font-weight: 900;
    letter-spacing: -1px;
    line-height: 1;
    font-family: 'Inter', sans-serif;
}}
.adboard-logo-ad {{
    color: #7c3aed;
    font-weight: 900;
}}
.adboard-logo-board {{
    color: #3b82f6;
    font-weight: 700;
}}
.adboard-sub-big {{
    color: #9ca3af;
    font-size: 10px;
    margin-top: 4px;
    letter-spacing: 0.2px;
}}

/* ===== トップナビゲーション ===== */
.top-nav {{
    display: flex;
    gap: 4px;
    padding: 6px;
    background: #f9fafb;
    border-radius: 14px;
    border: 1px solid #e5e7eb;
    justify-content: center;
}}

/* ===== トップナビゲーション ===== */
/* ナビのネストされたカラムのgapを削除（アイコンと文字を近く） */
[data-testid="column"] > div > [data-testid="stHorizontalBlock"] {{
    gap: 0.5rem !important;
}}

/* 最大specificityで既存スタイルを強制上書き */
html body .stApp div.st-key-nav_analytics button,
html body .stApp div.st-key-nav_campaign button,
html body .stApp div.st-key-nav_budget button,
html body .stApp div.st-key-nav_settings button {{
    min-height: 44px !important;
    height: 44px !important;
    width: fit-content !important;
    min-width: 0 !important;
    padding: 0 !important;
    margin: 0 !important;
    border: 0 !important;
    border-radius: 0 !important;
    background-color: transparent !important;
    color: #94a3b8 !important;
    font-size: 14px !important;
    font-weight: 700 !important;
    box-shadow: none !important;
    text-align: left !important;
    outline: none !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: flex-start !important;
}}
html body .stApp div.st-key-nav_analytics button:hover,
html body .stApp div.st-key-nav_campaign button:hover,
html body .stApp div.st-key-nav_budget button:hover,
html body .stApp div.st-key-nav_settings button:hover {{
    color: #475569 !important;
    background-color: transparent !important;
    border: 0 !important;
    box-shadow: none !important;
}}
html body .stApp div.st-key-nav_analytics button:focus,
html body .stApp div.st-key-nav_campaign button:focus,
html body .stApp div.st-key-nav_budget button:focus,
html body .stApp div.st-key-nav_settings button:focus,
html body .stApp div.st-key-nav_analytics button:active,
html body .stApp div.st-key-nav_campaign button:active,
html body .stApp div.st-key-nav_budget button:active,
html body .stApp div.st-key-nav_settings button:active {{
    background-color: transparent !important;
    border: 0 !important;
    box-shadow: none !important;
    outline: none !important;
}}
html body .stApp div.st-key-nav_analytics button[kind="primary"],
html body .stApp div.st-key-nav_campaign button[kind="primary"],
html body .stApp div.st-key-nav_budget button[kind="primary"],
html body .stApp div.st-key-nav_settings button[kind="primary"] {{
    color: #475569 !important;
    background-color: transparent !important;
    border: 0 !important;
    border-radius: 0 !important;
    box-shadow: none !important;
}}
/* ナビ内のアイコン画像を縦中央揃え・小さめに */
[data-testid="column"] [data-testid="column"] [data-testid="stImage"] {{
    display: flex;
    align-items: center;
    justify-content: flex-end;
    height: 44px;
    margin: 0 !important;
    padding: 0 !important;
}}
[data-testid="column"] [data-testid="column"] [data-testid="stImage"] > div {{
    height: 44px;
    display: flex;
    align-items: center;
}}
[data-testid="column"] [data-testid="column"] [data-testid="stImage"] img {{
    width: 30px !important;
    height: 30px !important;
    max-width: 30px !important;
    object-fit: contain;
}}

/* ===== クライアントセレクター（タブバー右端に固定配置） ===== */
[data-testid="stHorizontalBlock"]:has(div.st-key-client_select_top) {{
    height: 0 !important;
    min-height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
    overflow: visible !important;
}}
div.st-key-client_select_top {{
    position: fixed !important;
    top: 76px !important;
    right: 2rem !important;
    z-index: 100 !important;
    width: 160px !important;
}}
div.st-key-client_select_top [data-baseweb="select"] > div {{
    background: #ffffff !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06) !important;
    font-size: 13px !important;
    min-height: 34px !important;
    height: 34px !important;
    border-radius: 8px !important;
}}

/* ===== タブ（全幅） ===== */
[data-testid="stTabs"] {{
    margin-top: 0 !important;
}}
/* タブの選択下線をTHEME色に */
[data-testid="stTabs"] [data-baseweb="tab-highlight"] {{
    background-color: {THEME["primary"]} !important;
}}
[data-testid="stTabs"] [data-baseweb="tab-list"] {{
    background: {THEME["gradient_soft"]};
    border-radius: 0;
    padding: 6px max(calc(50vw - 50% - 10px), 1rem);
    gap: 3px;
    border: none;
    border-top: 1px solid {THEME["shadow_light"]};
    border-bottom: 1px solid {THEME["shadow_light"]};
    width: 100vw;
    position: relative;
    left: 50%;
    right: 50%;
    margin-left: -50vw;
    margin-right: -50vw;
    margin-top: 0 !important;
}}
[data-testid="stTabs"] [data-baseweb="tab"] {{
    border-radius: 8px;
    font-weight: 600;
    font-size: 13px;
    padding: 7px 20px;
    color: #6b7280;
    transition: all 0.2s ease;
    background: transparent !important;
}}
[data-testid="stTabs"] [aria-selected="true"] {{
    background: {THEME["gradient"]} !important;
    color: #ffffff !important;
    box-shadow: 0 2px 8px {THEME["shadow"]};
}}
[data-testid="stTabs"] [data-baseweb="tab"]:hover {{
    background: {THEME["shadow_light"]} !important;
}}

/* ===== メトリックカード ===== */
[data-testid="stMetric"] {{
    background-color: #ffffff !important;
    border: 1px solid #e5e7eb;
    border-radius: 10px;
    padding: 14px 16px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    transition: box-shadow 0.15s ease;
}}
[data-testid="stMetric"]:hover {{
    box-shadow: 0 3px 12px {THEME["shadow_light"]};
}}
[data-testid="stMetricLabel"] {{
    color: #9ca3af !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}
[data-testid="stMetricValue"] {{
    color: #1e1b4b !important;
    font-weight: 700 !important;
    font-size: 20px !important;
}}
[data-testid="stMetricDelta"] {{
    font-weight: 500 !important;
}}

/* ===== コンテナ ===== */
div[data-testid="stVerticalBlockBorderWrapper"] > div {{
    border-color: #e5e7eb !important;
    border-radius: 10px !important;
}}
[data-testid="stVerticalBlockBorderWrapper"] {{
    border-radius: 10px !important;
    overflow: hidden;
    transition: box-shadow 0.15s ease;
}}
[data-testid="stVerticalBlockBorderWrapper"]:hover {{
    box-shadow: 0 2px 12px {THEME["shadow_light"]};
}}

/* ===== プログレスバー ===== */
[data-testid="stProgress"] > div > div {{
    background: {THEME["gradient"]} !important;
    border-radius: 6px !important;
}}

/* ===== セレクトボックス ===== */
[data-baseweb="select"] > div {{
    border-color: #e5e7eb !important;
    border-radius: 8px !important;
    background: #ffffff;
}}
[data-baseweb="select"] > div:hover {{
    border-color: {THEME["primary"]} !important;
}}

/* ===== ボタン（一般） ===== */
.stButton > button {{
    border-radius: 8px;
    font-weight: 600;
    font-size: 13px;
    border: 1px solid #e5e7eb;
    color: {THEME["primary"]};
}}
.stButton > button:hover {{
    border-color: {THEME["primary"]};
    background: {THEME["primary_light"]};
}}
.stButton > button[kind="primary"],
.stButton > button[data-testid="baseButton-primary"] {{
    background: {THEME["primary"]} !important;
    color: white !important;
    border: none !important;
}}
.stButton > button[kind="primary"]:hover {{
    background: {THEME["primary_dark"]} !important;
}}

/* ===== ダウンロードボタン ===== */
.stDownloadButton > button {{
    border-radius: 8px;
    font-weight: 600;
    background: {THEME["primary_light"]} !important;
    border: 1px solid {THEME["shadow_light"]} !important;
    color: {THEME["primary_dark"]} !important;
}}

/* ===== データフレーム ===== */
[data-testid="stDataFrame"] {{
    border-radius: 10px;
    overflow: hidden;
    border: 1px solid #e5e7eb;
}}

[data-testid="stAlert"] {{ border-radius: 8px; }}
hr {{ border-color: #f3f4f6 !important; }}

[data-baseweb="tag"] {{
    background: {THEME["primary"]} !important;
    border-radius: 6px !important;
}}

[data-testid="stExpander"] {{
    border: 1px solid #e5e7eb !important;
    border-radius: 10px !important;
}}

/* ===== 入稿モード用スタイル ===== */
.submit-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px 0 12px 0;
    border-bottom: 1px solid #e5e7eb;
    margin-bottom: 24px;
}}
.submit-title {{
    font-size: 20px;
    font-weight: 700;
    color: #1e1b4b;
}}
.step-indicator {{
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 0;
    padding: 20px 0 32px 0;
}}
.step-item {{
    display: flex;
    flex-direction: column;
    align-items: center;
    min-width: 100px;
}}
.step-circle {{
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background: #e5e7eb;
    color: #9ca3af;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 6px;
    transition: all 0.2s ease;
}}
.step-circle.active {{
    background: {THEME["gradient"]};
    color: #ffffff;
    box-shadow: 0 2px 8px {THEME["shadow"]};
}}
.step-circle.done {{
    background: {THEME["primary"]};
    color: #ffffff;
}}
.step-label {{
    font-size: 12px;
    font-weight: 600;
    color: #9ca3af;
}}
.step-label.active {{
    color: {THEME["primary"]};
}}
.step-connector {{
    flex: 1;
    height: 2px;
    background: #e5e7eb;
    margin: 14px -30px 0 -30px;
    max-width: 80px;
}}
.step-connector.done {{
    background: {THEME["primary"]};
}}

/* ===== KPIカード（クリック選択式） ===== */
[data-testid="stVerticalBlock"] > div:has(> div > div > .kpi-marker) + div [data-testid="column"] .stButton > button {{
    min-height: 120px !important;
    padding: 20px !important;
    border-radius: 10px !important;
    text-align: left !important;
    white-space: pre-line !important;
    line-height: 1.7 !important;
    font-size: 14px !important;
    border: 2px solid #e5e7eb !important;
    background: #ffffff !important;
    color: #1e1b4b !important;
    font-weight: 500 !important;
    display: block !important;
}}
[data-testid="stVerticalBlock"] > div:has(> div > div > .kpi-marker) + div [data-testid="column"] .stButton > button:hover {{
    border-color: {THEME["primary"]} !important;
    background: {THEME["primary_50"]} !important;
    box-shadow: 0 2px 8px {THEME["shadow_light"]} !important;
}}
[data-testid="stVerticalBlock"] > div:has(> div > div > .kpi-marker) + div [data-testid="column"] .stButton > button[kind="primary"] {{
    border: 2px solid {THEME["primary"]} !important;
    background: {THEME["primary_light"]} !important;
    color: #1e1b4b !important;
    box-shadow: 0 2px 12px {THEME["shadow"]} !important;
}}

[data-testid="stSidebar"] {{ display: none; }}
</style>
""", unsafe_allow_html=True)

# ─── ヘッダー（ロゴ + 4ナビ + クライアント を1行に） ───
SECTIONS = ["分析", "広告管理", "予算設定", "全体設定"]
ICON_FILES = {
    "分析":     "nav_analytics.png",
    "広告管理": "nav_campaign.png",
    "予算設定": "nav_budget.png",
    "全体設定": "nav_settings.png",
}
NAV_KEYS = {
    "分析":     "nav_analytics",
    "広告管理": "nav_campaign",
    "予算設定": "nav_budget",
    "全体設定": "nav_settings",
}

# ナビボタン用に各アイコンをbase64化してCSSのbackground-imageに埋め込む
nav_bg_css = ""
for name, b64_key in [("分析", "nav_analytics"), ("広告管理", "nav_campaign"),
                      ("予算設定", "nav_budget"), ("全体設定", "nav_settings")]:
    b64 = ICONS_B64.get(name, "")
    if b64:
        nav_bg_css += f"""
html body .stApp div.st-key-{b64_key} button {{
    background-image: url('data:image/png;base64,{b64}') !important;
    background-repeat: no-repeat !important;
    background-position: 8px center !important;
    background-size: 24px 24px !important;
    padding-left: 38px !important;
    padding-right: 10px !important;
}}
html body .stApp div.st-key-{b64_key} button[kind="primary"] {{
    background-image:
        url('data:image/png;base64,{b64}'),
        {THEME["underline"]} !important;
    background-repeat: no-repeat, no-repeat !important;
    background-position: 8px center, 0 100% !important;
    background-size: 24px 24px, 100% 2px !important;
    padding-left: 38px !important;
    padding-right: 10px !important;
}}
html body .stApp div.st-key-{b64_key} button > div,
html body .stApp div.st-key-{b64_key} button p {{
    text-align: left !important;
    margin: 0 !important;
    padding: 0 !important;
}}
"""
st.markdown(f"<style>{nav_bg_css}</style>", unsafe_allow_html=True)

# ロゴ + 3ナビ（左寄せ） + スペーサー + 全体設定（右端）
col_logo, col_n1, col_n2, col_n3, _, col_n4 = st.columns([2.2, 1.1, 1.3, 1.3, 2.8, 1.3])

with col_logo:
    st.markdown("""
    <div class="adboard-logo-wrap">
        <div class="adboard-logo-text">
            <span class="adboard-logo-ad">Ad</span><span class="adboard-logo-board">Board</span>
        </div>
        <div class="adboard-sub-big">広告統合管理ダッシュボード</div>
    </div>
    """, unsafe_allow_html=True)

# 各ナビボタン（アイコンは背景画像としてボタンに埋め込み）
nav_data = [
    (col_n1, "分析"),
    (col_n2, "広告管理"),
    (col_n3, "予算設定"),
    (col_n4, "全体設定"),
]
for col, name in nav_data:
    with col:
        is_active = st.session_state["section"] == name
        btn_type = "primary" if is_active else "secondary"
        if st.button(name, key=NAV_KEYS[name], use_container_width=True, type=btn_type):
            if st.session_state["section"] != name:
                st.session_state["section"] = name
                st.rerun()

# ─── セクション別ルーティング ───
section = st.session_state["section"]

def render_client_selector():
    """タブバーの右側にクライアント選択を配置"""
    _, col_client = st.columns([7.5, 2.5])
    with col_client:
        selected_client = st.selectbox(
            "クライアント選択", get_clients(),
            index=get_clients().index(st.session_state["client"]),
            label_visibility="collapsed",
            key="client_select_top",
        )
        st.session_state["client"] = selected_client

if section == "分析":
    render_client_selector()
    tab0, tab1, tab2, tab3 = st.tabs([
        "全社一覧", "サマリー", "媒体別詳細", "レポート",
    ])

    PERIOD_MAP = {
        "今月（4月）":   ("2026-04-01","2026-04-14"),
        "先月（3月）":   ("2026-03-01","2026-03-31"),
        "Q1（1〜3月）": ("2026-01-01","2026-03-31"),
        "直近3ヶ月":    ("2026-01-14","2026-04-14"),
        "直近12ヶ月":   ("2025-04-14","2026-04-14"),
    }

    with tab0:
        exec(open(str(ROOT / "0_overview.py"), encoding="utf-8").read())
    with tab1:
        col_period, _ = st.columns([2, 8])
        with col_period:
            period = st.selectbox("期間", list(PERIOD_MAP.keys()),
                                  index=list(PERIOD_MAP.keys()).index(st.session_state["period"]),
                                  key="period_summary")
            st.session_state["period"] = period
        exec(open(str(ROOT / "1_summary.py"), encoding="utf-8").read())
    with tab2:
        col_period2, _ = st.columns([2, 8])
        with col_period2:
            period = st.selectbox("期間", list(PERIOD_MAP.keys()),
                                  index=list(PERIOD_MAP.keys()).index(st.session_state["period"]),
                                  key="period_platforms")
            st.session_state["period"] = period
        exec(open(str(ROOT / "2_platforms.py"), encoding="utf-8").read())
    with tab3:
        exec(open(str(ROOT / "4_report.py"), encoding="utf-8").read())

elif section == "広告管理":
    render_client_selector()
    tab_list, tab_new = st.tabs(["広告一覧", "新規入稿"])
    with tab_list:
        exec(open(str(ROOT / "7_ads_list.py"), encoding="utf-8").read())
    with tab_new:
        exec(open(str(ROOT / "6_submit.py"), encoding="utf-8").read())

elif section == "予算設定":
    render_client_selector()
    tab_view, tab_edit = st.tabs(["予算状況", "予算設定"])
    with tab_view:
        exec(open(str(ROOT / "3_budget.py"), encoding="utf-8").read())
    with tab_edit:
        exec(open(str(ROOT / "8_budget_edit.py"), encoding="utf-8").read())

elif section == "全体設定":
    tab_clients, tab_api, tab_users, tab_notif = st.tabs([
        "担当企業", "API連携", "ユーザー管理", "通知設定",
    ])
    with tab_clients:
        exec(open(str(ROOT / "5_settings.py"), encoding="utf-8").read())
    with tab_api:
        exec(open(str(ROOT / "9_api_settings.py"), encoding="utf-8").read())
    with tab_users:
        exec(open(str(ROOT / "10_users.py"), encoding="utf-8").read())
    with tab_notif:
        exec(open(str(ROOT / "11_notifications.py"), encoding="utf-8").read())
