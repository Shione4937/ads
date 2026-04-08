import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
from pathlib import Path
from datetime import date
sys.path.insert(0, str(Path(__file__).parent))
from loader import load_demo, get_summary, get_monthly_trend, TODAY

client = st.session_state.get("client", "船井総研")
period = st.session_state.get("period", "今月（4月）")

PERIOD_MAP = {
    "今月（4月）":    ("2026-04-01", "2026-04-14"),
    "先月（3月）":    ("2026-03-01", "2026-03-31"),
    "Q1（1〜3月）":  ("2026-01-01", "2026-03-31"),
    "直近3ヶ月":     ("2026-01-14", "2026-04-14"),
    "直近12ヶ月":    ("2025-04-14", "2026-04-14"),
}
d_from, d_to = PERIOD_MAP.get(period, ("2026-04-01","2026-04-14"))

df = load_demo(client=client, date_from=d_from, date_to=d_to)
summary = get_summary(df)

COLORS = {"google":"#5b6cf6","yahoo":"#7c3aed","meta":"#06b6d4","tiktok":"#a78bfa"}
PNAMES = {"google":"Google","yahoo":"Yahoo","meta":"Meta","tiktok":"TikTok"}

st.title(f"サマリー — {client}")
st.caption(f"{d_from} 〜 {d_to}")

total_cost = int(df["cost"].sum())
total_imp  = int(df["imp"].sum())
total_click= int(df["click"].sum())
total_cv   = int(df[df["platform"]!="meta"]["cv"].sum())
total_cpa  = int(total_cost/total_cv) if total_cv>0 else 0

c1,c2,c3,c4,c5 = st.columns(5)
c1.metric("総費用",    f"¥{total_cost:,.0f}")
c2.metric("IMP",       f"{total_imp:,.0f}")
c3.metric("クリック",  f"{total_click:,.0f}")
c4.metric("CV",        f"{total_cv:,.0f}")
c5.metric("平均CPA",   f"¥{total_cpa:,.0f}")

st.divider()

# AI分析枠
with st.container(border=True):
    st.markdown("🤖 **AI分析コメント** `Gemini連携予定`")
    st.info(
        f"{client}の{period}実績：総費用¥{total_cost:,.0f}に対しCV{total_cv:,}件・平均CPA¥{total_cpa:,.0f}。"
        "GoogleがCPA効率良好で引き続き重点投資が有効です。"
        "MetaはCV未計測のためAPI連携による計測環境整備を優先推奨します。"
        "YahooはCPAが目標を超過傾向にあり、キャンペーン構成の見直しを検討してください。"
    )

col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("媒体別パフォーマンス")
    disp = summary.copy()
    disp["媒体"] = disp["platform"].map(PNAMES)
    disp["費用"] = disp["cost"].apply(lambda x: f"¥{x:,.0f}")
    disp["IMP"]  = disp["imp"].apply(lambda x: f"{x:,.0f}")
    disp["クリック"] = disp["click"].apply(lambda x: f"{x:,.0f}")
    disp["CV"]   = disp["cv"].apply(lambda x: f"{x:,.0f}" if x>0 else "未計測")
    disp["CPA"]  = disp.apply(lambda r: f"¥{r['cpa']:,.0f}" if pd.notna(r["cpa"]) and r["cpa"]<9999999 else "—", axis=1)
    disp["CTR"]  = disp["ctr"].apply(lambda x: f"{x:.2f}%")
    st.dataframe(disp[["媒体","費用","IMP","クリック","CV","CPA","CTR"]], use_container_width=True, hide_index=True)

with col2:
    st.subheader("費用シェア")
    fig = px.pie(summary, names=summary["platform"].map(PNAMES), values="cost",
                 color="platform", color_discrete_map=COLORS, hole=0.45)
    fig.update_layout(height=250, margin=dict(t=10,b=10,l=10,r=10), showlegend=True,
                      legend=dict(font_size=11))
    st.plotly_chart(fig, use_container_width=True)

# 月次トレンド
st.subheader("月次費用トレンド")
trend_df = load_demo(client=client, date_from="2025-04-01", date_to="2026-04-14")
trend = get_monthly_trend(trend_df)
fig2 = go.Figure()
fig2.add_bar(x=trend["month"], y=trend["cost"], name="費用",
             marker_color="#5b6cf6", opacity=0.8)
fig2.add_scatter(x=trend["month"], y=trend["cv"]*1000, name="CV×1000",
                 mode="lines+markers", line=dict(color="#06b6d4", width=2),
                 yaxis="y2")
fig2.update_layout(
    height=280, margin=dict(t=20,b=20),
    yaxis=dict(title="費用（円）"),
    yaxis2=dict(title="CV", overlaying="y", side="right"),
    legend=dict(orientation="h", y=1.1),
    barmode="group",
)
st.plotly_chart(fig2, use_container_width=True)

# アラート
alerts = []
target_cpa = int(df["target_cpa"].iloc[0]) if len(df)>0 else 5000
for _, row in summary.iterrows():
    if row["platform"]=="meta": alerts.append(("🔴","CV未計測：Meta",f"¥{row['cost']:,.0f}消化中・CV計測なし。API連携で解決可能"))
    elif pd.notna(row["cpa"]) and row["cpa"] > target_cpa * 1.5:
        alerts.append(("🟡",f"CPA超過：{PNAMES[row['platform']]}",f"CPA ¥{row['cpa']:,.0f}（目標¥{target_cpa:,}）"))
if alerts:
    st.subheader(f"アラート（{len(alerts)}件）")
    for icon, title, desc in alerts:
        st.warning(f"**{icon} {title}** — {desc}")
