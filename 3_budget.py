import streamlit as st
import plotly.graph_objects as go
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from loader import get_budget_progress, TODAY

client = st.session_state.get("client", "A社")
PNAMES = {"google":"Google","yahoo":"Yahoo","meta":"Meta","tiktok":"TikTok"}
COLORS = {"google":"#3b82f6","yahoo":"#60a5fa","meta":"#93c5fd","tiktok":"#bfdbfe"}

st.markdown(f"#### 予算管理 — {client}")
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
          "予算内" if total_projected <= total_budget else f"超過 ¥{total_projected-total_budget:,.0f}")

st.divider()

# AI予測コメント
over = total_projected > total_budget
st.markdown(f"""
<div style="background:linear-gradient(135deg, #f5f3ff 0%, #eef2ff 50%, #f0f9ff 100%);
            border:1px solid rgba(124,107,246,0.15);border-radius:12px;padding:18px 22px;margin-bottom:16px;">
    <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
        <span style="font-size:18px;"></span>
        <span style="font-weight:700;color:#4338ca;">AI予測コメント</span>
        <span class="gemini-badge">Gemini連携予定</span>
    </div>
    <p style="color:#374151;font-size:14px;line-height:1.7;margin:0;">
        現在の消化ペース（¥{total_pace:,.0f}/日）が続いた場合、月末着地は¥{total_projected:,.0f}と
        予算¥{total_budget:,.0f}{'を超過する見込みです。配分の見直しを推奨します。' if over else 'の範囲内で着地する見込みです。'}
        残{days_remaining}日で日次¥{total_target:,.0f}が目安です。
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("**媒体別 予算進捗**")
for _, row in bp.iterrows():
    pname = PNAMES[row["platform"]]
    color = COLORS[row["platform"]]

    with st.container(border=True):
        col1, col2 = st.columns([1.5, 3])
        with col1:
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;">
                <div style="width:10px;height:10px;border-radius:50%;background:{color};"></div>
                <span style="font-weight:700;font-size:15px;color:#1a1b3e;">{pname}</span>
            </div>
            """, unsafe_allow_html=True)
            st.caption(f"予算 ¥{row['budget']:,.0f}")
        with col2:
            pct = row["pct_used"]
            st.progress(min(pct/100, 1.0))
            c1,c2,c3,c4 = st.columns(4)
            c1.metric("消化済",   f"¥{row['cost_used']:,.0f}", f"{pct}%")
            c2.metric("残予算",   f"¥{row['remaining']:,.0f}")
            c3.metric("日次目安", f"¥{row['per_day_target']:,.0f}")
            c4.metric("着地予測", f"¥{row['projected']:,.0f}")

# 消化ペース比較グラフ
st.markdown("**消化ペース（理想 vs 実績）**")
ideal_daily = [total_budget / days_in_month * d for d in range(1, days_elapsed+1)]
actual_cumulative = []
running = 0
for d in range(1, days_elapsed+1):
    running += total_pace
    actual_cumulative.append(running)

fig = go.Figure()
fig.add_scatter(x=list(range(1, days_elapsed+1)), y=ideal_daily,
                name="理想ペース", line=dict(color="#bfdbfe", dash="dash", width=2))
fig.add_scatter(x=list(range(1, days_elapsed+1)), y=actual_cumulative,
                name="実績", line=dict(color="#3b82f6", width=2.5),
                fill="tozeroy", fillcolor="rgba(124,107,246,0.08)")
fig.update_layout(
    height=280, margin=dict(t=20,b=20,l=10,r=10),
    xaxis_title="日付（4月）", yaxis_title="累計費用（円）",
    legend=dict(orientation="h", y=1.12),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(gridcolor="rgba(124,107,246,0.06)"),
    yaxis=dict(gridcolor="rgba(124,107,246,0.06)"),
)
st.plotly_chart(fig, use_container_width=True)
