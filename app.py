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
        "primary":       "#10b981",
        "primary_dark":  "#059669",
        "primary_light": "#d1fae5",
        "primary_50":    "#f0fdf4",
        "gradient":      "linear-gradient(135deg, #34d399, #10b981)",
        "gradient_soft": "linear-gradient(90deg, #d1fae5 0%, #ccfbf1 50%, #dcfce7 100%)",
        "underline":     "linear-gradient(90deg, #6ee7b7, #34d399, #14b8a6)",
        "shadow":        "rgba(16,185,129,0.3)",
        "shadow_light":  "rgba(16,185,129,0.08)",
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

.block-container {{
    padding-top: 1.2rem !important;
    padding-bottom: 1rem !important;
}}

/* ===== ロゴ ===== */
.adboard-logo-big {{
    font-size: 32px;
    font-weight: 800;
    background: linear-gradient(135deg, #7c3aed, #6366f1, #0ea5e9);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.5px;
    line-height: 1.1;
}}
.adboard-sub-big {{
    color: #9ca3af;
    font-size: 13px;
    margin-top: 2px;
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

/* トップナビ用ボタンのCSSスコープマーカー */
[data-testid="stVerticalBlock"] > div:has(> div > div > .topnav-marker) + div [data-testid="column"] .stButton > button {{
    min-height: 60px !important;
    height: 60px !important;
    padding: 8px 18px !important;
    border-radius: 12px !important;
    text-align: left !important;
    font-size: 16px !important;
    font-weight: 700 !important;
    border: 1px solid transparent !important;
    background: transparent !important;
    color: #6b7280 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: flex-start !important;
    line-height: 1 !important;
    box-shadow: none !important;
}}
[data-testid="stVerticalBlock"] > div:has(> div > div > .topnav-marker) + div [data-testid="column"] .stButton > button > div,
[data-testid="stVerticalBlock"] > div:has(> div > div > .topnav-marker) + div [data-testid="column"] .stButton > button p {{
    display: inline !important;
    margin: 0 !important;
    font-size: 16px !important;
    font-weight: 700 !important;
    line-height: 1 !important;
}}
[data-testid="stVerticalBlock"] > div:has(> div > div > .topnav-marker) + div [data-testid="column"] .stButton > button:hover {{
    background: #f9fafb !important;
    color: #1e1b4b !important;
    border-color: #e5e7eb !important;
}}
[data-testid="stVerticalBlock"] > div:has(> div > div > .topnav-marker) + div [data-testid="column"] .stButton > button[kind="primary"] {{
    background: {THEME["primary_light"]} !important;
    color: {THEME["primary_dark"]} !important;
    border: 1px solid {THEME["primary_light"]} !important;
}}

/* ===== タブ ===== */
[data-testid="stTabs"] [data-baseweb="tab-list"] {{
    background: {THEME["gradient_soft"]};
    border-radius: 10px;
    padding: 4px 5px;
    gap: 3px;
    border: 1px solid {THEME["shadow_light"]};
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
    background: #ffffff;
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

# 各ナビアイテムのカラムインデックス（col_n1=2, col_n2=3, col_n3=4, col_n4=5 ※1始まり）
# ※ nth-of-typeで指定するため、ロゴ列が1番目、ナビ1が2番目...という位置を使う
nav_icon_css = ""
for idx, name in enumerate(SECTIONS):
    b64 = ICONS_B64.get(name, "")
    if not b64:
        continue
    # idx=0 → 2番目のカラム（col_n1）, idx=1 → 3番目 ...
    col_nth = idx + 2
    nav_icon_css += f"""
[data-testid="stVerticalBlock"] > div:has(> div > div > .topnav-marker) + div [data-testid="column"]:nth-of-type({col_nth}) .stButton > button::before {{
    content: '';
    display: inline-block;
    width: 38px;
    height: 38px;
    background-image: url('data:image/png;base64,{b64}');
    background-size: contain;
    background-repeat: no-repeat;
    background-position: center;
    margin-right: 10px;
    flex-shrink: 0;
}}
"""

st.markdown(f"<style>{nav_icon_css}</style>", unsafe_allow_html=True)

# ロゴ (col1) + 4ナビ (col2-5) + クライアント (col6) を1行に
col_logo, col_n1, col_n2, col_n3, col_n4, col_client = st.columns([2.4, 1.4, 1.6, 1.6, 1.6, 1.4])

with col_logo:
    st.markdown("""
    <div style="padding:8px 0 0 0;">
        <div class="adboard-logo-big">AdBoard</div>
        <div class="adboard-sub-big">広告統合管理ダッシュボード</div>
    </div>
    """, unsafe_allow_html=True)

# トップナビマーカー（CSSスコープ用）
st.markdown('<div class="topnav-marker"></div>', unsafe_allow_html=True)

# 各ナビボタンを配置
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
        if st.button(name, key=f"nav_{name}", use_container_width=True, type=btn_type):
            if st.session_state["section"] != name:
                st.session_state["section"] = name
                st.rerun()

with col_client:
    st.write("")
    selected_client = st.selectbox(
        "クライアント選択", get_clients(),
        index=get_clients().index(st.session_state["client"]),
        label_visibility="collapsed"
    )
    st.session_state["client"] = selected_client

st.write("")

# ─── セクション別ルーティング ───
section = st.session_state["section"]

if section == "分析":
    # 分析サブタブ
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
    # 広告管理サブタブ
    tab_list, tab_new = st.tabs(["広告一覧", "新規入稿"])
    with tab_list:
        exec(open(str(ROOT / "7_ads_list.py"), encoding="utf-8").read())
    with tab_new:
        exec(open(str(ROOT / "6_submit.py"), encoding="utf-8").read())

elif section == "予算設定":
    # 予算設定サブタブ
    tab_view, tab_edit = st.tabs(["予算状況", "予算設定"])
    with tab_view:
        exec(open(str(ROOT / "3_budget.py"), encoding="utf-8").read())
    with tab_edit:
        exec(open(str(ROOT / "8_budget_edit.py"), encoding="utf-8").read())

elif section == "全体設定":
    # 全体設定サブタブ
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
