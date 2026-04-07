import streamlit as st
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from loader import load_all, get_summary

st.title("アラート")
st.caption("データに基づく自動検知")

@st.cache_data
def get_data():
    return load_all()

df = get_data()
summary = get_summary(df)

alerts = []
CPA_THRESHOLD = 5000

for _, row in summary.iterrows():
    if row["cv"] > 0 and row["cpa"] > CPA_THRESHOLD:
        alerts.append({"level": "warning", "title": f"CPA超過：{row['platform']}", "detail": f"CPA ¥{row['cpa']:,.0f} — 目標 ¥{CPA_THRESHOLD:,} を超過しています"})

for _, row in summary.iterrows():
    if row["cv"] == 0 and row["cost"] > 0:
        alerts.append({"level": "error", "title": f"CV未計測：{row['platform']}", "detail": f"費用 ¥{row['cost']:,.0f} を消化していますがCVが計測されていません。タグ・API設定を確認してください。"})

avg_ctr = summary["ctr"].mean()
for _, row in summary.iterrows():
    if row["ctr"] < avg_ctr * 0.5 and row["imp"] > 10000:
        alerts.append({"level": "warning", "title": f"CTR低下：{row['platform']}", "detail": f"CTR {row['ctr']:.2f}% — 全媒体平均 {avg_ctr:.2f}% の半分以下です"})

alerts.append({"level": "info", "title": "Meta：CV自動取得未対応", "detail": "現在はCSVエクスポートのためCV列が取得できません。Meta Marketing APIを連携することで自動取得・リアルタイム更新が可能になります。"})
alerts.append({"level": "info", "title": "API連携で自動化可能な項目", "detail": "各媒体のAPI連携により、①データ自動取得（手動CSV不要）、②日次自動更新、③予算消化リアルタイム監視、④CV・ROAS自動計算が実現できます。"})

errors = [a for a in alerts if a["level"] == "error"]
warnings = [a for a in alerts if a["level"] == "warning"]
infos = [a for a in alerts if a["level"] == "info"]

if errors:
    st.markdown("### 要対応")
    for a in errors:
        st.error(f"**{a['title']}**\n\n{a['detail']}")
if warnings:
    st.markdown("### 注意")
    for a in warnings:
        st.warning(f"**{a['title']}**\n\n{a['detail']}")
if infos:
    st.markdown("### API連携で改善できる項目")
    for a in infos:
        st.info(f"**{a['title']}**\n\n{a['detail']}")
