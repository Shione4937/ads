import streamlit as st
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from loader import load_demo, get_budget_progress, TODAY

client = st.session_state.get("client", "A社")

st.markdown("#### 予算設定")
st.caption(f"{client} の月次予算・媒体別配分を設定します")

# セッションで予算データを保持
if "budget_settings" not in st.session_state:
    st.session_state["budget_settings"] = {}

client_budget = st.session_state["budget_settings"].get(client, {
    "total": 1200000,
    "google": 600000,
    "yahoo":  300000,
    "meta":   200000,
    "tiktok": 100000,
})

st.write("")

# ─── 月次総予算 ───
with st.container(border=True):
    st.markdown("**月次総予算**")
    st.caption("当月の広告費総額を設定")
    total_budget = st.number_input(
        "総予算（円）",
        min_value=0,
        value=client_budget["total"],
        step=50000,
        format="%d",
        label_visibility="collapsed",
    )

st.write("")

# ─── 媒体別配分 ───
with st.container(border=True):
    st.markdown("**媒体別配分**")
    st.caption("各媒体への予算配分を設定")

    platforms = [
        ("google", "Google Ads", "#6366f1"),
        ("yahoo",  "Yahoo!広告",  "#8b5cf6"),
        ("meta",   "Meta広告",    "#0ea5e9"),
        ("tiktok", "TikTok広告",  "#a78bfa"),
    ]

    allocations = {}
    for pid, pname, pcolor in platforms:
        col_name, col_slider, col_value = st.columns([2, 5, 2])
        with col_name:
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;padding-top:10px;">
                <div style="width:10px;height:10px;border-radius:50%;background:{pcolor};"></div>
                <span style="font-weight:600;font-size:14px;">{pname}</span>
            </div>
            """, unsafe_allow_html=True)
        with col_slider:
            pct = st.slider(
                f"{pname}配分",
                0, 100,
                int(client_budget[pid] / client_budget["total"] * 100) if client_budget["total"] > 0 else 25,
                label_visibility="collapsed",
                key=f"slider_{pid}",
            )
        with col_value:
            amount = int(total_budget * pct / 100)
            st.markdown(f"""
            <div style="text-align:right;padding-top:10px;">
                <div style="font-size:13px;font-weight:700;color:#1e1b4b;">¥{amount:,}</div>
                <div style="font-size:11px;color:#9ca3af;">{pct}%</div>
            </div>
            """, unsafe_allow_html=True)
        allocations[pid] = amount

    total_allocated = sum(allocations.values())
    if total_allocated != total_budget:
        st.warning(f"配分合計 ¥{total_allocated:,} と総予算 ¥{total_budget:,} が一致しません")

st.write("")

# ─── 期間別予算（Shirofune風カレンダー配分・プレースホルダー） ───
with st.container(border=True):
    st.markdown("**期間別予算配分**")
    st.caption("通常期間と特別期間（セール・キャンペーン期間）を設定できます")

    tab_normal, tab_special = st.tabs(["通常設定", "期間別設定"])
    with tab_normal:
        st.info("月次予算を日割りで均等配分（デフォルト）")
        days_in_month = 30
        daily_budget = total_budget // days_in_month
        st.markdown(f"**日次予算目安：** ¥{daily_budget:,}")
    with tab_special:
        st.caption("特定期間だけ予算を増減させる設定（Phase 2で実装予定）")
        st.markdown("""
        例：
        - セール期間（4/25〜4/30）：予算1.5倍
        - 月末最終日：予算調整なし
        """)
        st.info("カレンダーUIによる期間指定・予算配分機能は今後実装予定")

st.write("")

# ─── 保存ボタン ───
col_s, _ = st.columns([2, 8])
with col_s:
    if st.button("予算を保存", type="primary", use_container_width=True):
        st.session_state["budget_settings"][client] = {
            "total": total_budget,
            **allocations,
        }
        st.success("予算設定を保存しました（デモ）")
