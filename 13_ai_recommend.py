import streamlit as st
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from loader import load_demo, get_summary

client = st.session_state.get("client", "A社")

st.markdown("#### おすすめ広告設定")
st.caption(f"AIが {client} に最適な広告設定を提案します")

# ─── Step 1: 目的を選ぶ ───
st.markdown("**広告の目的を選んでください**")

st.markdown('<div class="kpi-marker"></div>', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)

goal = st.session_state.get("ai_goal", "")

goals = [
    ("売上を増やしたい", "CVを最大化し、費用対効果の高い広告配信を行います", "goal_sales", c1),
    ("認知度を上げたい", "インプレッションとリーチを最大化する設定を提案します", "goal_awareness", c2),
    ("来店を増やしたい", "エリアターゲティングと来店促進に特化した設定を提案します", "goal_visit", c3),
]

for name, desc, key, col in goals:
    with col:
        is_selected = goal == name
        btn_type = "primary" if is_selected else "secondary"
        if st.button(f"{name}\n\n{desc}", key=key, use_container_width=True, type=btn_type):
            st.session_state["ai_goal"] = name
            st.rerun()

st.write("")

# ─── Step 2: AI提案（デモ） ───
if goal:
    # 過去データから簡易分析
    df = load_demo(client=client, date_from="2025-04-01", date_to="2026-04-14")
    summary = get_summary(df)

    best_platform = summary.loc[summary["cpa"].idxmin(), "platform"] if len(summary) > 0 else "google"
    PNAMES = {"google": "Google Ads", "yahoo": "Yahoo!広告", "meta": "Meta広告", "tiktok": "TikTok広告"}

    with st.container(border=True):
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:12px;">
            <span style="font-weight:700;font-size:16px;color:#1e1b4b;">
                {client} へのAI提案
            </span>
            <span class="gemini-badge">Gemini連携予定</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"**目的:** {goal}")
        st.write("")

        if goal == "売上を増やしたい":
            st.markdown("**推奨設定（デモ）**")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                - **推奨媒体:** {PNAMES[best_platform]}（過去CPA最良）
                - **推奨予算配分:** {PNAMES[best_platform]} 60% / その他 40%
                - **成果指標:** コンバージョン
                - **入札戦略:** 目標CPA ¥5,000
                """)
            with col2:
                st.markdown("""
                - **ターゲット:** 25-54歳 / すべて
                - **デバイス:** PC + スマートフォン
                - **エリア:** 全国
                - **推奨キャンペーン:** P-MAX
                """)
        elif goal == "認知度を上げたい":
            st.markdown("**推奨設定（デモ）**")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("""
                - **推奨媒体:** Meta広告 + TikTok広告
                - **推奨予算配分:** Meta 50% / TikTok 30% / Google 20%
                - **成果指標:** クリック（リーチ重視）
                - **広告種類:** 動画広告 + フィード広告
                """)
            with col2:
                st.markdown("""
                - **ターゲット:** 18-34歳
                - **デバイス:** スマートフォン優先
                - **エリア:** 全国
                - **興味関心:** 自動最適化
                """)
        else:
            st.markdown("**推奨設定（デモ）**")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("""
                - **推奨媒体:** Google Ads（ローカル検索）
                - **推奨予算配分:** Google 70% / Yahoo 30%
                - **成果指標:** コンバージョン（来店）
                - **広告種類:** 検索広告 + ローカルキャンペーン
                """)
            with col2:
                st.markdown("""
                - **ターゲット:** 25-54歳
                - **デバイス:** スマートフォン優先
                - **エリア:** 店舗から半径10km
                - **入札戦略:** 来店数の最大化
                """)

        st.write("")

        st.markdown("""
        <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;padding:14px;margin:8px 0;">
            <p style="color:#64748b;font-size:13px;line-height:1.7;margin:0;">
                Gemini API連携後は、過去の実績データを元に最適な設定を自動計算します。
                推奨媒体・予算配分・ターゲティングの根拠も詳細に説明されます。
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.write("")
        col_a, col_b, _ = st.columns([2, 2, 6])
        with col_a:
            if st.button("この設定で入稿する", type="primary", use_container_width=True, key="ai_apply"):
                # 新規入稿にデータを流し込み
                st.session_state["submit_data"] = {
                    "promo_name": f"{client} {goal}キャンペーン",
                    "kpi": "コンバージョン" if goal == "売上を増やしたい" else "クリック",
                    "budget": 500000,
                }
                st.session_state["submit_step"] = 1
                st.success("新規入稿タブにデータをセットしました")
        with col_b:
            if st.button("設定をカスタマイズ", use_container_width=True, key="ai_customize"):
                st.info("新規入稿タブで詳細を調整できます")
else:
    st.info("上のボタンから広告の目的を選んでください。AIが最適な設定を提案します。")
