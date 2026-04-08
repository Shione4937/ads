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

/* ===== メトリックカード（KPIカード） ===== */
[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 10px;
    padding: 14px 16px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    transition: box-shadow 0.15s ease;
}
[data-testid="stMetric"]:hover {
    box-shadow: 0 3px 12px rgba(99,102,241,0.1);
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

/* ===== モード切替ラジオ ===== */
div[data-testid="stRadio"] > label {
    display: none;
}
div[data-testid="stRadio"] [role="radiogroup"] {
    background: #f3f4f6;
    border-radius: 10px;
    padding: 4px;
    gap: 2px;
    border: 1px solid #e5e7eb;
    margin-top: 22px;
}
div[data-testid="stRadio"] [role="radiogroup"] label {
    background: transparent;
    padding: 6px 22px;
    border-radius: 7px;
    font-weight: 600;
    font-size: 13px;
    color: #6b7280;
    cursor: pointer;
    transition: all 0.15s ease;
    margin: 0 !important;
}
div[data-testid="stRadio"] [role="radiogroup"] label:has(input:checked) {
    background: linear-gradient(135deg, #7c3aed, #6366f1);
    color: #ffffff;
    box-shadow: 0 2px 6px rgba(99,102,241,0.25);
}
div[data-testid="stRadio"] [role="radiogroup"] label > div:first-child {
    display: none;
}

/* ===== 入稿モード用スタイル ===== */
.submit-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px 0 12px 0;
    border-bottom: 1px solid #e5e7eb;
    margin-bottom: 24px;
}
.submit-title {
    font-size: 20px;
    font-weight: 700;
    color: #1e1b4b;
}
.step-indicator {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 0;
    padding: 20px 0 32px 0;
}
.step-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    min-width: 100px;
}
.step-circle {
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
}
.step-circle.active {
    background: linear-gradient(135deg, #7c3aed, #6366f1);
    color: #ffffff;
    box-shadow: 0 2px 8px rgba(99,102,241,0.3);
}
.step-circle.done {
    background: #6366f1;
    color: #ffffff;
}
.step-label {
    font-size: 12px;
    font-weight: 600;
    color: #9ca3af;
}
.step-label.active {
    color: #6366f1;
}
.step-connector {
    flex: 1;
    height: 2px;
    background: #e5e7eb;
    margin: 14px -30px 0 -30px;
    max-width: 80px;
}
.step-connector.done {
    background: #6366f1;
}

/* ===== 成果指標カード ===== */
.kpi-card {
    border: 2px solid #e5e7eb;
    border-radius: 10px;
    padding: 20px 24px;
    cursor: pointer;
    transition: all 0.2s ease;
    background: #ffffff;
    height: 100%;
}
.kpi-card:hover {
    border-color: #a5b4fc;
    background: #fafbff;
}
.kpi-card.selected {
    border-color: #6366f1;
    background: #f5f3ff;
    box-shadow: 0 2px 12px rgba(99,102,241,0.12);
}
.kpi-icon {
    font-size: 28px;
    margin-bottom: 8px;
}
.kpi-title {
    font-size: 16px;
    font-weight: 700;
    color: #1e1b4b;
    margin-bottom: 4px;
}
.kpi-desc {
    font-size: 12px;
    color: #6b7280;
    line-height: 1.5;
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
if "mode" not in st.session_state:
    st.session_state["mode"] = "分析"
if "submit_step" not in st.session_state:
    st.session_state["submit_step"] = 1
if "submit_data" not in st.session_state:
    st.session_state["submit_data"] = {}

# ─── ヘッダー + モード切替 + 会社選択 ───
col_title, col_mode, col_client = st.columns([5, 3, 2])
with col_title:
    st.markdown("""
    <div class="adboard-header">
        <div class="adboard-logo">AdBoard</div>
        <div class="adboard-sub">広告統合管理ダッシュボード</div>
    </div>
    """, unsafe_allow_html=True)
with col_mode:
    mode = st.radio(
        "モード", ["分析", "入稿"],
        index=["分析","入稿"].index(st.session_state["mode"]),
        horizontal=True,
        label_visibility="collapsed",
        key="mode_radio",
    )
    st.session_state["mode"] = mode
with col_client:
    selected_client = st.selectbox(
        "クライアント選択", get_clients(),
        index=get_clients().index(st.session_state["client"]),
        label_visibility="collapsed"
    )
    st.session_state["client"] = selected_client

# ─── モードに応じて画面切替 ───
if st.session_state["mode"] == "入稿":
    exec(open(str(ROOT / "6_submit.py"), encoding="utf-8").read())
else:
    # ─── 分析モード：タブナビ ───
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
