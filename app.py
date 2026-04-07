import streamlit as st
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))
from loader import get_clients

st.set_page_config(page_title="AdBoard", page_icon="📊", layout="wide")

# ライトモード強制 + 上部タブスタイル
st.markdown("""
<style>
/* ライトモード強制 */
html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background-color: #f5f6fa !important;
    color: #1a1d2e !important;
}
[data-testid="stSidebar"] {
    background-color: #ffffff !important;
}
/* メトリクスカード */
[data-testid="stMetric"] {
    background: #ffffff;
    border: 0.5px solid #e8eaf0;
    border-radius: 10px;
    padding: 8px 12px;
}
[data-testid="stMetricValue"] {
    font-size: 1.4rem !important;
    font-weight: 700 !important;
    color: #1a1d2e !important;
}
[data-testid="stMetricLabel"] {
    color: #6b7280 !important;
}
/* タブスタイル */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: #ffffff;
    border-radius: 10px;
    padding: 4px;
    border: 0.5px solid #e8eaf0;
    gap: 2px;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    border-radius: 7px;
    font-weight: 600;
    font-size: 13px;
    padding: 6px 18px;
    color: #6b7280;
}
[data-testid="stTabs"] [aria-selected="true"] {
    background: #5b6cf6 !important;
    color: #ffffff !important;
}
</style>
""", unsafe_allow_html=True)

ROOT = Path(__file__).parent

# サイドバー
with st.sidebar:
    st.markdown("## 📊 AdBoard")
    st.caption("広告統合管理ダッシュボード")
    st.divider()
    clients = get_clients()
    selected_client = st.selectbox("クライアント", clients)
    period = st.selectbox("期間", ["今月（4月）","先月（3月）","Q1（1〜3月）","直近3ヶ月","直近12ヶ月"])
    st.session_state["client"] = selected_client
    st.session_state["period"] = period
    st.divider()
    st.caption("API連携状況")
    for p, c in [("Google","🟡"),("Yahoo","🟡"),("Meta","🟡"),("TikTok","🟡")]:
        st.caption(f"{c} {p}：未連携")

# 上部タブナビ
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 サマリー",
    "🔍 媒体別詳細",
    "💰 予算管理",
    "📄 レポート",
    "⚙️ 設定",
])

with tab1:
    exec(open(str(ROOT / "1_summary.py"), encoding="utf-8").read())
with tab2:
    exec(open(str(ROOT / "2_platforms.py"), encoding="utf-8").read())
with tab3:
    exec(open(str(ROOT / "3_budget.py"), encoding="utf-8").read())
with tab4:
    exec(open(str(ROOT / "4_report.py"), encoding="utf-8").read())
with tab5:
    exec(open(str(ROOT / "5_settings.py"), encoding="utf-8").read())
