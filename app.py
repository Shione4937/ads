import streamlit as st
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))
from loader import get_clients, ALL_CLIENTS, DEFAULT_SELECTED

st.set_page_config(page_title="AdBoard", page_icon="📊", layout="wide")

st.markdown("""
<style>
[data-testid="stMetric"] {
    border: 0.5px solid rgba(124,58,237,0.15);
    border-radius: 10px;
    padding: 8px 12px;
}
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    border-radius: 10px;
    padding: 4px;
    gap: 2px;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    border-radius: 7px;
    font-weight: 600;
    font-size: 13px;
    padding: 6px 18px;
}
.block-container {
    padding-top: 1rem !important;
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

# ヘッダー：コンパクトに
header_l, header_r = st.columns([5, 1])
with header_l:
    st.markdown("**AdBoard** — 広告統合管理")
with header_r:
    selected_client = st.selectbox(
        "", get_clients(),
        index=get_clients().index(st.session_state["client"]),
        label_visibility="collapsed"
    )
    st.session_state["client"] = selected_client

# タブナビ
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
