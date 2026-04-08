import streamlit as st
import pandas as pd
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from loader import load_demo, get_summary

client = st.session_state.get("client", "A社")
PNAMES = {"google":"Google","yahoo":"Yahoo","meta":"Meta","tiktok":"TikTok"}

st.markdown(f"#### レポート — {client}")

col1, col2 = st.columns(2)
with col1:
    st.markdown("**比較期間A**")
    d_from_a = st.date_input("開始", value=pd.to_datetime("2026-03-01"))
    d_to_a   = st.date_input("終了", value=pd.to_datetime("2026-03-31"))
with col2:
    st.markdown("**比較期間B**")
    d_from_b = st.date_input("開始 ", value=pd.to_datetime("2026-04-01"))
    d_to_b   = st.date_input("終了 ", value=pd.to_datetime("2026-04-14"))

df_a = load_demo(client=client, date_from=str(d_from_a), date_to=str(d_to_a))
df_b = load_demo(client=client, date_from=str(d_from_b), date_to=str(d_to_b))
sum_a = get_summary(df_a)
sum_b = get_summary(df_b)

# AI期間比較コメント
cost_a = int(df_a["cost"].sum()); cost_b = int(df_b["cost"].sum())
cv_a = int(df_a["cv"].sum()); cv_b = int(df_b["cv"].sum())

st.markdown(f"""
<div style="background:linear-gradient(135deg, #f5f3ff 0%, #eef2ff 50%, #f0f9ff 100%);
            border:1px solid rgba(124,107,246,0.15);border-radius:12px;padding:18px 22px;margin:16px 0;">
    <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
        <span style="font-size:18px;">🤖</span>
        <span style="font-weight:700;color:#4338ca;">AI期間比較コメント</span>
        <span style="background:linear-gradient(135deg,#7c6bf6,#60a5fa);color:#fff;font-size:10px;
                     padding:2px 8px;border-radius:6px;font-weight:600;">Gemini連携予定</span>
    </div>
    <p style="color:#374151;font-size:14px;line-height:1.7;margin:0;">
        期間A（{d_from_a}〜{d_to_a}）vs 期間B（{d_from_b}〜{d_to_b}）の比較：
        費用 ¥{cost_a:,.0f} → ¥{cost_b:,.0f}、CV {cv_a:,}件 → {cv_b:,}件。
        詳細な改善提案はGemini API連携後に自動生成されます。
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("**期間比較テーブル**")
merged = sum_a[["platform","cost","imp","click","cv","cpa"]].merge(
    sum_b[["platform","cost","imp","click","cv","cpa"]], on="platform", suffixes=("_A","_B"))
merged["費用変化"] = ((merged["cost_B"]-merged["cost_A"])/merged["cost_A"].replace(0,1)*100).round(1)
merged["媒体"] = merged["platform"].map(PNAMES)
disp = merged[["媒体","cost_A","cost_B","費用変化","cv_A","cv_B"]].copy()
disp.columns = ["媒体","費用A","費用B","費用変化%","CV_A","CV_B"]
disp["費用A"] = disp["費用A"].apply(lambda x: f"¥{x:,.0f}")
disp["費用B"] = disp["費用B"].apply(lambda x: f"¥{x:,.0f}")
disp["費用変化%"] = disp["費用変化%"].apply(lambda x: f"{x:+.1f}%")
st.dataframe(disp, use_container_width=True, hide_index=True)

st.divider()

st.markdown("**CSVエクスポート**")
c1, c2 = st.columns(2)
with c1:
    all_df = load_demo(client=client)
    st.download_button("📥 全期間データ CSV", all_df.to_csv(index=False, encoding="utf-8-sig"),
                       f"{client}_all.csv", "text/csv")
with c2:
    st.download_button("📥 サマリー CSV", get_summary(all_df).to_csv(index=False, encoding="utf-8-sig"),
                       f"{client}_summary.csv", "text/csv")
