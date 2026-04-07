import streamlit as st
import plotly.graph_objects as go
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from loader import get_budget_progress, TODAY

client = st.session_state.get("client", "船井自動車販売")
PNAMES = {"google":"Google","yahoo":"Yahoo","meta":"Meta","tiktok":"TikTok"}
COLORS = {"google":"#5b6cf6","yahoo":"#7c3aed","meta":"#06b6d4","tiktok":"#a78bfa"}

st.title(f"予算管理 — {client}")
st.caption(f"基準日：{TODAY}（4月14日）")

bp = get_budget_progress(client)
days_elapsed   = int(bp["days_elapsed"].iloc[0])
days_remaining = int(bp["days_remaining"].iloc[0])
days_in_month  = int(bp["days_in_month"].iloc[0])

total_budget   = int(bp["budget"].sum())
total_used     = int(bp["cost_used"].sum())
total_remaining= int(bp["remaining"].sum())
total_projected= int(bp["projected"].sum())
total_pace     = int(bp["daily_pace"].sum())
total_target   = int(bp["per_day_target"].sum())

c1,c2,c3,c4,c5 = st.columns(5)
c1.metric("当月予算合計",   f"¥{total_budget:,.0f}")
c2.metric("消化済",         f"¥{total_used:,.0f}",    f"{total_used/total_budget*100:.1f}%")
c3.metric("残予算",         f"¥{total_remaining:,.0f}", f"残{days_remaining}日")
c4.metric("日次按分目安",   f"¥{total_target:,.0f}",  f"現状¥{total_pace:,.0f}/日")
c5.metric("月末着地予測",   f"¥{total_projected:,.0f}",
          "予算内✓" if total_projected <= total_budget else f"超過¥{total_projected-total_budget:,.0f}")

st.divider()

with st.container(border=True):
    st.markdown("🤖 **AI予測コメント** `Gemini連携予定`")
    over = total_projected > total_budget
    st.info(
        f"現在の消化ペース（¥{total_pace:,.0f}/日）が続いた場合、月末着地は¥{total_projected:,.0f}と"
        f"予算¥{total_budget:,.0f}{'を超過する見込みです。配分の見直しを推奨します。' if over else 'の範囲内で着地する見込みです。'}"
        f"残{days_remaining}日で日次¥{total_target:,.0f}が目安です。"
    )

st.subheader("媒体別 予算進捗")
for _, row in bp.iterrows():
    pname = PNAMES[row["platform"]]
    col1, col2 = st.columns([2,3])
    with col1:
        st.markdown(f"**{pname}**")
        st.caption(f"予算 ¥{row['budget']:,.0f}")
    with col2:
        pct = row["pct_used"]
        color = "#ef4444" if pct>85 else "#f59e0b" if pct>70 else COLORS[row["platform"]]
        st.progress(min(pct/100, 1.0))
        c1,c2,c3,c4 = st.columns(4)
        c1.metric("消化済",     f"¥{row['cost_used']:,.0f}", f"{pct}%")
        c2.metric("残予算",     f"¥{row['remaining']:,.0f}")
        c3.metric("日次目安",   f"¥{row['per_day_target']:,.0f}")
        c4.metric("着地予測",   f"¥{row['projected']:,.0f}")
    st.divider()

# 月次ペース比較グラフ
st.subheader("消化ペース（理想 vs 実績）")
ideal_daily = [total_budget / days_in_month * d for d in range(1, days_elapsed+1)]
actual_cumulative = []
running = 0
for d in range(1, days_elapsed+1):
    running += total_pace
    actual_cumulative.append(running)

fig = go.Figure()
fig.add_scatter(x=list(range(1, days_elapsed+1)), y=ideal_daily,
                name="理想ペース", line=dict(color="#9ca3af", dash="dash"))
fig.add_scatter(x=list(range(1, days_elapsed+1)), y=actual_cumulative,
                name="実績", line=dict(color="#5b6cf6", width=2), fill="tozeroy",
                fillcolor="rgba(91,108,246,0.1)")
fig.update_layout(height=260, margin=dict(t=20,b=20),
                  xaxis_title="日付（4月）", yaxis_title="累計費用（円）",
                  legend=dict(orientation="h", y=1.1))
st.plotly_chart(fig, use_container_width=True)
