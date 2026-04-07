import streamlit as st
import pandas as pd
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from loader import load_demo, get_summary

client = st.session_state.get("client", "東信自動車")
PNAMES = {"google":"Google","yahoo":"Yahoo","meta":"Meta","tiktok":"TikTok"}

st.title(f"レポート — {client}")

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

with st.container(border=True):
    st.markdown("🤖 **AI期間比較コメント** `Gemini連携予定`")
    cost_a = int(df_a["cost"].sum()); cost_b = int(df_b["cost"].sum())
    cv_a = int(df_a["cv"].sum()); cv_b = int(df_b["cv"].sum())
    st.info(
        f"期間A（{d_from_a}〜{d_to_a}）vs 期間B（{d_from_b}〜{d_to_b}）の比較：\n\n"
        f"費用：¥{cost_a:,.0f} → ¥{cost_b:,.0f}、"
        f"CV：{cv_a:,}件 → {cv_b:,}件。"
        "詳細な改善提案はGemini API連携後に自動生成されます。"
    )

st.subheader("期間比較テーブル")
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

st.subheader("CSVエクスポート")
c1, c2 = st.columns(2)
with c1:
    all_df = load_demo(client=client)
    st.download_button("📥 全期間データ CSV", all_df.to_csv(index=False, encoding="utf-8-sig"),
                       f"{client}_all.csv", "text/csv")
with c2:
    st.download_button("📥 サマリー CSV", get_summary(all_df).to_csv(index=False, encoding="utf-8-sig"),
                       f"{client}_summary.csv", "text/csv")
