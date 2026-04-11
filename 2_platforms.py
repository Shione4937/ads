import streamlit as st
import plotly.express as px
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from loader import load_demo

client = st.session_state.get("client", "A社")
period = st.session_state.get("period", "今月（4月）")
PERIOD_MAP = {
    "今月（4月）":   ("2026-04-01","2026-04-14"),
    "先月（3月）":   ("2026-03-01","2026-03-31"),
    "Q1（1〜3月）": ("2026-01-01","2026-03-31"),
    "直近3ヶ月":    ("2026-01-14","2026-04-14"),
    "直近12ヶ月":   ("2025-04-14","2026-04-14"),
}
d_from, d_to = PERIOD_MAP.get(period, ("2026-04-01","2026-04-14"))

# カラーパレット（ブランドカラー）
COLORS = {"google":"#4684ec","yahoo":"#ff0132","meta":"#0b76ed","tiktok":"#4fe5e2"}
PNAMES = {"google":"Google Ads","yahoo":"Yahoo!広告","meta":"Meta広告","tiktok":"TikTok広告"}

# 媒体タブにブランドカラーを適用
st.markdown("""
<style>
[role="tabpanel"] [data-testid="stTabs"] [data-baseweb="tab"]:nth-of-type(1)[aria-selected="true"] {
    background: linear-gradient(135deg, #4684ec, #34a451) !important;
    color: #fff !important;
}
[role="tabpanel"] [data-testid="stTabs"] [data-baseweb="tab"]:nth-of-type(2)[aria-selected="true"] {
    background: #ff0132 !important;
    color: #fff !important;
}
[role="tabpanel"] [data-testid="stTabs"] [data-baseweb="tab"]:nth-of-type(3)[aria-selected="true"] {
    background: #0b76ed !important;
    color: #fff !important;
}
[role="tabpanel"] [data-testid="stTabs"] [data-baseweb="tab"]:nth-of-type(4)[aria-selected="true"] {
    background: linear-gradient(135deg, #4fe5e2, #e62b58) !important;
    color: #fff !important;
}
[role="tabpanel"] [data-testid="stTabs"] [data-baseweb="tab-highlight"] {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown(f"#### 媒体別詳細 — {client}")
st.caption(f"{d_from} 〜 {d_to}")

df = load_demo(client=client, date_from=d_from, date_to=d_to)
tabs = st.tabs([PNAMES[p] for p in ["google","yahoo","meta","tiktok"]])

for tab, platform in zip(tabs, ["google","yahoo","meta","tiktok"]):
    with tab:
        pf = df[df["platform"]==platform]
        c1,c2,c3,c4 = st.columns(4)
        c1.metric("費用",    f"¥{int(pf['cost'].sum()):,.0f}")
        c2.metric("IMP",     f"{int(pf['imp'].sum()):,.0f}")
        c3.metric("クリック", f"{int(pf['click'].sum()):,.0f}")
        c4.metric("CV",      f"{int(pf['cv'].sum()):,.0f}")

        camp = pf.groupby("campaign").agg(cost=("cost","sum"),imp=("imp","sum"),
               click=("click","sum"),cv=("cv","sum")).reset_index()
        camp = camp[camp["cost"]>0].sort_values("cost",ascending=False)
        camp["cpa"] = (camp["cost"]/camp["cv"].replace(0,float("nan"))).round(0)

        fig = px.bar(camp.sort_values("cost",ascending=True), x="cost", y="campaign",
                     orientation="h", color_discrete_sequence=[COLORS[platform]],
                     labels={"cost":"費用（円）","campaign":""})
        fig.update_traces(texttemplate="¥%{x:,.0f}", textposition="outside",
                          marker_line_width=0, opacity=0.9)
        fig.update_layout(
            height=max(200, len(camp)*50+60),
            margin=dict(t=10,b=10,l=10,r=10),
            showlegend=False,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(gridcolor="rgba(124,107,246,0.06)"),
            yaxis=dict(gridcolor="rgba(124,107,246,0.06)"),
        )
        st.plotly_chart(fig, use_container_width=True)

        camp_disp = camp.copy()
        camp_disp["cost"] = camp_disp["cost"].apply(lambda x: f"¥{x:,.0f}")
        camp_disp["cpa"]  = camp_disp["cpa"].apply(lambda x: f"¥{x:,.0f}" if str(x)!="nan" else "—")
        camp_disp.columns = ["キャンペーン","費用","IMP","クリック","CV","CPA"]
        st.dataframe(camp_disp, use_container_width=True, hide_index=True)
