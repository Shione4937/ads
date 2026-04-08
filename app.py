import streamlit as st
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))
from loader import get_clients, ALL_CLIENTS, DEFAULT_SELECTED

st.set_page_config(page_title="AdBoard", page_icon="📊", layout="wide")

# ─── グローバルCSS ───
st.markdown("""
<style>
/* ===== フォント・ベース ===== */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Sans+JP:wght@400;500;600;700&display=swap');
html, body, [class*="css"] {
    font-family: 'Inter', 'Noto Sans JP', sans-serif;
}

/* ===== ページ余白調整 ===== */
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 1rem !important;
}

/* ===== ヘッダー ===== */
.adboard-title {
    font-size: 26px;
    font-weight: 700;
    color: #4338ca;
    margin: 0;
    letter-spacing: 0.3px;
}
.adboard-subtitle {
    color: #6b7280;
    font-size: 14px;
    margin: 2px 0 8px 0;
}

/* ===== タブスタイル ===== */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: linear-gradient(90deg, #f0edff 0%, #e8ecff 50%, #edf4ff 100%);
    border-radius: 12px;
    padding: 5px 6px;
    gap: 4px;
    border: 1px solid rgba(124,107,246,0.1);
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    border-radius: 9px;
    font-weight: 600;
    font-size: 13px;
    padding: 8px 20px;
    color: #5b5e8a;
    transition: all 0.2s ease;
}
[data-testid="stTabs"] [aria-selected="true"] {
    background: linear-gradient(135deg, #7c6bf6, #6366f1) !important;
    color: #ffffff !important;
    box-shadow: 0 2px 8px rgba(99,102,241,0.25);
}
[data-testid="stTabs"] [data-baseweb="tab"]:hover {
    background: rgba(124,107,246,0.08);
}

/* ===== メトリックカード ===== */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, #ffffff 0%, #f8f7ff 100%);
    border: 1px solid rgba(124,107,246,0.12);
    border-radius: 12px;
    padding: 14px 16px;
    box-shadow: 0 2px 8px rgba(124,107,246,0.06);
    transition: all 0.2s ease;
}
[data-testid="stMetric"]:hover {
    box-shadow: 0 4px 16px rgba(124,107,246,0.12);
    border-color: rgba(124,107,246,0.25);
    transform: translateY(-1px);
}
[data-testid="stMetricLabel"] {
    color: #7c7ea8 !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
[data-testid="stMetricValue"] {
    color: #1a1b3e !important;
    font-weight: 700 !important;
}
[data-testid="stMetricDelta"] {
    font-weight: 600 !important;
}

/* ===== コンテナ（カード） ===== */
[data-testid="stExpander"],
div[data-testid="stVerticalBlockBorderWrapper"]:has(> div > div[data-testid="stVerticalBlock"] > div.stMarkdown) {
    border-radius: 12px !important;
}
div[data-testid="stVerticalBlockBorderWrapper"] > div {
    border-color: rgba(124,107,246,0.12) !important;
    border-radius: 12px !important;
}

/* ===== st.container(border=True) のスタイル ===== */
[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 12px !important;
    overflow: hidden;
}

/* ===== プログレスバー ===== */
[data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg, #a78bfa, #7c6bf6, #60a5fa) !important;
    border-radius: 8px !important;
}
[data-testid="stProgress"] {
    border-radius: 8px;
}

/* ===== セレクトボックス ===== */
[data-baseweb="select"] {
    border-radius: 10px !important;
}
[data-baseweb="select"] > div {
    border-color: rgba(124,107,246,0.2) !important;
    border-radius: 10px !important;
    background: #ffffff;
}
[data-baseweb="select"] > div:hover {
    border-color: rgba(124,107,246,0.4) !important;
}

/* ===== ボタン ===== */
.stButton > button {
    border-radius: 10px;
    font-weight: 600;
    border: 1px solid rgba(124,107,246,0.2);
    transition: all 0.2s ease;
}
.stButton > button:hover {
    border-color: #7c6bf6;
    box-shadow: 0 2px 8px rgba(124,107,246,0.15);
}
.stButton > button[kind="primary"],
.stButton > button[data-testid="baseButton-primary"] {
    background: linear-gradient(135deg, #7c6bf6, #6366f1) !important;
    color: white !important;
    border: none !important;
}

/* ===== ダウンロードボタン ===== */
.stDownloadButton > button {
    border-radius: 10px;
    font-weight: 600;
    background: linear-gradient(135deg, #f0edff, #edf0ff) !important;
    border: 1px solid rgba(124,107,246,0.15) !important;
    color: #5b4dc7 !important;
}
.stDownloadButton > button:hover {
    background: linear-gradient(135deg, #e8e3ff, #e3e8ff) !important;
    box-shadow: 0 2px 8px rgba(124,107,246,0.15);
}

/* ===== データフレーム ===== */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid rgba(124,107,246,0.1);
}

/* ===== 情報・警告ボックス ===== */
[data-testid="stAlert"] {
    border-radius: 10px;
}

/* ===== Divider ===== */
hr {
    border-color: rgba(124,107,246,0.1) !important;
}

/* ===== マルチセレクト ===== */
[data-baseweb="tag"] {
    background: linear-gradient(135deg, #7c6bf6, #6366f1) !important;
    border-radius: 8px !important;
}

/* ===== Expander ===== */
[data-testid="stExpander"] {
    border: 1px solid rgba(124,107,246,0.12) !important;
    border-radius: 12px !important;
}

/* ===== サイドバー非表示（全ページタブ方式のため） ===== */
[data-testid="stSidebar"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)

ROOT = Path(__file__).parent

if "selected_clients" not in st.session_state:
    st.session_state["selected_clients"] = DEFAULT_SELECTED
if "client" not in st.session_state:
    st.session_state["client"] = DEFAULT_SELECTED[0]
if "period" not in st.session_state:
    st.session_state["period"] = "今月（4月）"

# ─── ヘッダー + 会社選択（同じ行） ───
col_title, col_client = st.columns([8, 2])
with col_title:
    st.markdown("""
    <p class="adboard-title">AdBoard</p>
    <p class="adboard-subtitle">広告統合管理ダッシュボード</p>
    """, unsafe_allow_html=True)
with col_client:
    selected_client = st.selectbox(
        "クライアント選択", get_clients(),
        index=get_clients().index(st.session_state["client"]),
        label_visibility="collapsed"
    )
    st.session_state["client"] = selected_client

# ─── タブナビ ───
tab0, tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "全社一覧", "サマリー", "媒体別詳細", "予算管理", "レポート", "設定",
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
    exec(open(str(ROOT / "3_budget.py"), encoding="utf-8").read())
with tab4:
    exec(open(str(ROOT / "4_report.py"), encoding="utf-8").read())
with tab5:
    exec(open(str(ROOT / "5_settings.py"), encoding="utf-8").read())
