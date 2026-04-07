import streamlit as st
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))
from loader import get_clients

st.set_page_config(page_title="AdBoard", page_icon="📊", layout="wide")

st.markdown("""
<style>
[data-testid="stMetric"] {
    border: 0.5px solid rgba(128,128,128,0.2);
    border-radius: 10px;
    padding: 8px 12px;
}
[data-testid="stMetricValue"] {
    font-size: 1.4rem !important;
    font-weight: 700 !important;
}
</style>
""", unsafe_allow_html=True)

ROOT = Path(__file__).parent

pg = st.navigation([
    st.Page(str(ROOT / "1_summary.py"),   title="サマリー",   icon="📊"),
    st.Page(str(ROOT / "2_platforms.py"), title="媒体別詳細", icon="🔍"),
    st.Page(str(ROOT / "3_budget.py"),    title="予算管理",   icon="💰"),
    st.Page(str(ROOT / "4_report.py"),    title="レポート",   icon="📄"),
    st.Page(str(ROOT / "5_settings.py"),  title="設定",       icon="⚙️"),
])

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

pg.run()
