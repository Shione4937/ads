import streamlit as st
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))
from loader import get_clients, ALL_CLIENTS, DEFAULT_SELECTED

st.set_page_config(page_title="AdBoard", layout="wide")

# ─── グローバルCSS ───
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Sans+JP:wght@400;500;600;700&display=swap');
html, body, [class*="css"] {
    font-family: 'Inter', 'Noto Sans JP', sans-serif;
}

/* ===== Streamlit デフォルトヘッダー非表示 ===== */
header[data-testid="stHeader"] {
    display: none !important;
}

/* ===== ページ余白 ===== */
.block-container {
    padding-top: 1.2rem !important;
    padding-bottom: 1rem !important;
}

/* ===== ヘッダー ===== */
.adboard-header {
    padding: 10px 0 14px 0;
    border-bottom: 2px solid transparent;
    border-image: linear-gradient(90deg, #c4b5fd, #818cf8, #7dd3fc) 1;
    margin-bottom: 6px;
}
.adboard-logo {
    font-size: 24px;
    font-weight: 700;
    background: linear-gradient(135deg, #7c3aed, #6366f1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.adboard-sub {
    color: #9ca3af;
    font-size: 13px;
    margin-top: 1px;
}

/* ===== タブ（グラデーション背景・ピル型） ===== */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: linear-gradient(90deg, #ede9fe 0%, #e0e7ff 50%, #dbeafe 100%);
    border-radius: 10px;
    padding: 4px 5px;
    gap: 3px;
    border: 1px solid rgba(129,140,248,0.12);
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    border-radius: 8px;
    font-weight: 600;
    font-size: 13px;
    padding: 7px 20px;
    color: #6b7280;
    transition: all 0.2s ease;
    background: transparent !important;
}
[data-testid="stTabs"] [aria-selected="true"] {
    background: linear-gradient(135deg, #7c3aed, #6366f1) !important;
    color: #ffffff !important;
    box-shadow: 0 2px 8px rgba(99,102,241,0.3);
}
[data-testid="stTabs"] [data-baseweb="tab"]:hover {
    background: rgba(124,58,237,0.06) !important;
}

/* ===== メトリックカード ===== */
[data-testid="stMetric"] {
    background: transparent;
    border: none;
    border-radius: 0;
    padding: 8px 4px;
    box-shadow: none;
}
[data-testid="stMetric"]:hover {
    box-shadow: none;
    transform: none;
}
[data-testid="stMetricLabel"] {
    color: #9ca3af !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
[data-testid="stMetricValue"] {
    color: #1e1b4b !important;
    font-weight: 700 !important;
}
[data-testid="stMetricDelta"] {
    font-weight: 500 !important;
}

/* ===== コンテナ（カード） ===== */
div[data-testid="stVerticalBlockBorderWrapper"] > div {
    border-color: #e5e7eb !important;
    border-radius: 10px !important;
}
[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 10px !important;
    overflow: hidden;
    transition: box-shadow 0.15s ease;
}
[data-testid="stVerticalBlockBorderWrapper"]:hover {
    box-shadow: 0 2px 12px rgba(99,102,241,0.07);
}

/* ===== プログレスバー ===== */
[data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg, #c4b5fd, #818cf8, #7dd3fc) !important;
    border-radius: 6px !important;
}

/* ===== セレクトボックス ===== */
[data-baseweb="select"] > div {
    border-color: #e5e7eb !important;
    border-radius: 8px !important;
    background: #ffffff;
}
[data-baseweb="select"] > div:hover {
    border-color: #a5b4fc !important;
}

/* ===== ボタン ===== */
.stButton > button {
    border-radius: 8px;
    font-weight: 600;
    font-size: 13px;
    border: 1px solid #e5e7eb;
    color: #6366f1;
}
.stButton > button:hover {
    border-color: #a5b4fc;
    background: #f5f3ff;
}
.stButton > button[kind="primary"],
.stButton > button[data-testid="baseButton-primary"] {
    background: #6366f1 !important;
    color: white !important;
    border: none !important;
}

/* ===== ダウンロードボタン ===== */
.stDownloadButton > button {
    border-radius: 8px;
    font-weight: 600;
    background: #f5f3ff !important;
    border: 1px solid #e0e7ff !important;
    color: #4f46e5 !important;
}

/* ===== データフレーム ===== */
[data-testid="stDataFrame"] {
    border-radius: 10px;
    overflow: hidden;
    border: 1px solid #e5e7eb;
}

/* ===== アラート ===== */
[data-testid="stAlert"] { border-radius: 8px; }

/* ===== Divider ===== */
hr { border-color: #f3f4f6 !important; }

/* ===== マルチセレクト ===== */
[data-baseweb="tag"] {
    background: #6366f1 !important;
    border-radius: 6px !important;
}

/* ===== Expander ===== */
[data-testid="stExpander"] {
    border: 1px solid #e5e7eb !important;
    border-radius: 10px !important;
}

/* ===== サイドバー非表示 ===== */
[data-testid="stSidebar"] { display: none; }
</style>
""", unsafe_allow_html=True)

ROOT = Path(__file__).parent

if "selected_clients" not in st.session_state:
    st.session_state["selected_clients"] = DEFAULT_SELECTED
if "client" not in st.session_state:
    st.session_state["client"] = DEFAULT_SELECTED[0]
if "period" not in st.session_state:
    st.session_state["period"] = "今月（4月）"

# ─── ヘッダー + 会社選択 ───
col_title, col_client = st.columns([8, 2])
with col_title:
    st.markdown("""
    <div class="adboard-header">
        <div class="adboard-logo">AdBoard</div>
        <div class="adboard-sub">広告統合管理ダッシュボード</div>
    </div>
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
