import streamlit as st
import pandas as pd
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from loader import get_all_clients_summary, ALL_CLIENTS

selected = st.session_state.get("selected_clients", ALL_CLIENTS[:5])

st.markdown("#### 📋 全社一覧")
st.caption("2026-04-01 〜 2026-04-14　｜　設定タブで表示企業を選択できます")

df = get_all_clients_summary(selected, "2026-04-01", "2026-04-14")

PNAMES = {"google":"Google","yahoo":"Yahoo","meta":"Meta","tiktok":"TikTok"}

for _, row in df.iterrows():
    # アラートバッジ
    badges = ""
    if "予算90%超" in row["alerts"]:
        badges += '<span style="background:#fee2e2;color:#dc2626;padding:2px 8px;border-radius:6px;font-size:11px;font-weight:600;margin-left:6px;">予算90%超</span>'
    if "CPA超過" in row["alerts"]:
        badges += '<span style="background:#fef3c7;color:#d97706;padding:2px 8px;border-radius:6px;font-size:11px;font-weight:600;margin-left:6px;">CPA超過</span>'
    if "Meta未計測" in row["alerts"]:
        badges += '<span style="background:#e0f2fe;color:#0284c7;padding:2px 8px;border-radius:6px;font-size:11px;font-weight:600;margin-left:6px;">Meta未計測</span>'

    with st.container(border=True):
        c1, c2, c3, c4, c5, c6, c7 = st.columns([2, 2.5, 2, 1, 2, 1.5, 1])
        with c1:
            st.markdown(f"**{row['client']}**", unsafe_allow_html=True)
            if badges:
                st.markdown(badges, unsafe_allow_html=True)
        c2.metric("費用",      f"¥{row['cost']:,.0f}")
        c3.metric("IMP",       f"{row['imp']:,.0f}")
        c4.metric("CV",        f"{int(row['cv']):,}")
        c5.metric("CPA",       f"¥{row['cpa']:,.0f}" if row['cpa'] else "—")
        c6.metric("予算消化率", f"{row['pct_used']}%")
        if c7.button("詳細 →", key=f"btn_{row['client']}"):
            st.session_state["client"] = row["client"]
            st.rerun()
