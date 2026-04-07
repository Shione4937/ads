import streamlit as st
import plotly.express as px
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from loader import load_demo

client = st.session_state.get("client", "東信自動車")
period = st.session_state.get("period", "今月（4月）")
PERIOD_MAP = {
    "今月（4月）":   ("2026-04-01","2026-04-14"),
    "先月（3月）":   ("2026-03-01","2026-03-31"),
    "Q1（1〜3月）": ("2026-01-01","2026-03-31"),
    "直近3ヶ月":    ("2026-01-14","2026-04-14"),
    "直近12ヶ月":   ("2025-04-14","2026-04-14"),
}
d_from, d_to = PERIOD_MAP.get(period, ("2026-04-01","2026-04-14"))
COLORS = {"google":"#5b6cf6","yahoo":"#7c3aed","meta":"#06b6d4","tiktok":"#a78bfa"}
PNAMES = {"google":"Google Ads","yahoo":"Yahoo!広告","meta":"Meta広告","tiktok":"TikTok広告"}

st.title(f"媒体別詳細 — {client}")
st.caption(f"{d_from} 〜 {d_to}")

df = load_demo(client=client, date_from=d_from, date_to=d_to)
tabs = st.tabs(["🔵 Google","🟣 Yahoo","🔷 Meta","⚫ TikTok"])

for tab, platform in zip(tabs, ["google","yahoo","meta","tiktok"]):
    with tab:
        pf = df[df["platform"]==platform]
        c1,c2,c3,c4 = st.columns(4)
        c1.metric("費用",   f"¥{int(pf['cost'].sum()):,.0f}")
        c2.metric("IMP",    f"{int(pf['imp'].sum()):,.0f}")
        c3.metric("クリック",f"{int(pf['click'].sum()):,.0f}")
        c4.metric("CV",     f"{int(pf['cv'].sum()):,.0f}" if platform!="meta" else "未計測")
        if platform=="meta":
            st.info("MetaはCSVエクスポートにCV列が含まれません。API連携後に取得可能になります。")
        camp = pf.groupby("campaign").agg(cost=("cost","sum"),imp=("imp","sum"),
               click=("click","sum"),cv=("cv","sum")).reset_index()
        camp = camp[camp["cost"]>0].sort_values("cost",ascending=False)
        camp["cpa"] = (camp["cost"]/camp["cv"].replace(0,float("nan"))).round(0)
        fig = px.bar(camp.sort_values("cost",ascending=True), x="cost", y="campaign",
                     orientation="h", color_discrete_sequence=[COLORS[platform]],
                     labels={"cost":"費用（円）","campaign":""})
        fig.update_traces(texttemplate="¥%{x:,.0f}", textposition="outside")
        fig.update_layout(height=max(200, len(camp)*50+60), margin=dict(t=10,b=10), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        camp["cost"] = camp["cost"].apply(lambda x: f"¥{x:,.0f}")
        camp["cpa"]  = camp["cpa"].apply(lambda x: f"¥{x:,.0f}" if str(x)!="nan" else "—")
        camp.columns = ["キャンペーン","費用","IMP","クリック","CV","CPA"]
        st.dataframe(camp, use_container_width=True, hide_index=True)
