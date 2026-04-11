import streamlit as st
import pandas as pd
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from loader import load_demo, get_summary, get_monthly_trend, TODAY

client = st.session_state.get("client", "A社")

st.markdown("#### AI分析")
st.caption(f"{client} の広告パフォーマンスをAIが分析します")

# ─── 深掘り分析 ───
with st.container(border=True):
    st.markdown("**トレンド・季節性分析**")
    st.caption("過去12ヶ月のデータからAIがパターンを検出")

    df = load_demo(client=client, date_from="2025-04-01", date_to="2026-04-14")
    trend = get_monthly_trend(df)

    # 簡易サマリ（AI接続前のデモ表示）
    total_cost = int(df["cost"].sum())
    total_cv = int(df["cv"].sum())
    avg_cpa = int(total_cost / total_cv) if total_cv > 0 else 0

    c1, c2, c3 = st.columns(3)
    c1.metric("12ヶ月 総費用", f"¥{total_cost:,.0f}")
    c2.metric("12ヶ月 総CV", f"{total_cv:,}")
    c3.metric("12ヶ月 平均CPA", f"¥{avg_cpa:,}")

    st.markdown("""
    <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;padding:16px;margin-top:12px;">
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
            <span style="font-weight:700;color:#6366f1;">AI分析コメント</span>
            <span class="gemini-badge">Gemini連携予定</span>
        </div>
        <p style="color:#64748b;font-size:13px;line-height:1.7;margin:0;">
            Gemini APIが接続されると、以下のような分析が自動生成されます：<br>
            ・月次トレンドの変動要因の推察<br>
            ・季節性パターンの検出（年末繁忙期、夏季閑散期など）<br>
            ・媒体間のパフォーマンス相関分析<br>
            ・異常値の検出と原因仮説の提示
        </p>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# ─── キャンペーンランキング ───
with st.container(border=True):
    st.markdown("**キャンペーンパフォーマンスランキング**")
    st.caption("CPA効率が良い/悪いキャンペーンを自動抽出")

    df_month = load_demo(client=client, date_from="2026-04-01", date_to="2026-04-14")
    camp = df_month.groupby(["platform", "campaign"]).agg(
        cost=("cost", "sum"), cv=("cv", "sum"), click=("click", "sum"), imp=("imp", "sum")
    ).reset_index()
    camp["cpa"] = (camp["cost"] / camp["cv"].replace(0, float("nan"))).round(0)
    camp["ctr"] = (camp["click"] / camp["imp"].replace(0, 1) * 100).round(2)

    PNAMES = {"google": "Google", "yahoo": "Yahoo", "meta": "Meta", "tiktok": "TikTok"}
    camp["媒体"] = camp["platform"].map(PNAMES)

    # CPA TOP5（良い順）
    st.markdown("**CPA効率 TOP 5**（低い方が良い）")
    top5 = camp.dropna(subset=["cpa"]).nsmallest(5, "cpa").copy()
    top5["CPA"] = top5["cpa"].apply(lambda x: f"¥{x:,.0f}")
    top5["費用"] = top5["cost"].apply(lambda x: f"¥{x:,.0f}")
    st.dataframe(
        top5[["媒体", "campaign", "費用", "cv", "CPA", "ctr"]].rename(
            columns={"campaign": "キャンペーン", "cv": "CV", "ctr": "CTR%"}
        ),
        use_container_width=True, hide_index=True,
    )

    # CPA ワースト5
    st.markdown("**CPA要改善 TOP 5**（高い方から）")
    worst5 = camp.dropna(subset=["cpa"]).nlargest(5, "cpa").copy()
    worst5["CPA"] = worst5["cpa"].apply(lambda x: f"¥{x:,.0f}")
    worst5["費用"] = worst5["cost"].apply(lambda x: f"¥{x:,.0f}")
    st.dataframe(
        worst5[["媒体", "campaign", "費用", "cv", "CPA", "ctr"]].rename(
            columns={"campaign": "キャンペーン", "cv": "CV", "ctr": "CTR%"}
        ),
        use_container_width=True, hide_index=True,
    )

    st.markdown("""
    <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;padding:16px;margin-top:12px;">
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
            <span style="font-weight:700;color:#6366f1;">AI改善提案</span>
            <span class="gemini-badge">Gemini連携予定</span>
        </div>
        <p style="color:#64748b;font-size:13px;line-height:1.7;margin:0;">
            Gemini APIが接続されると、以下のような提案が自動生成されます：<br>
            ・ワーストキャンペーンの具体的な改善案<br>
            ・予算配分の最適化提案（効率の良いキャンペーンに予算シフト）<br>
            ・キーワード/ターゲティングの改善方向性
        </p>
    </div>
    """, unsafe_allow_html=True)
