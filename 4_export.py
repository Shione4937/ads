import streamlit as st
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from loader import load_all, get_summary

st.title("出力・設定")

@st.cache_data
def get_data():
    return load_all()

df = get_data()
summary = get_summary(df)

st.subheader("CSVエクスポート")
col1, col2 = st.columns(2)
with col1:
    st.download_button("📥 サマリー CSV", summary.to_csv(index=False, encoding="utf-8-sig"), "ad_summary.csv", "text/csv")
with col2:
    st.download_button("📥 全データ CSV", df.to_csv(index=False, encoding="utf-8-sig"), "ad_all.csv", "text/csv")

st.divider()
st.subheader("API連携状況")

for platform, note in {
    "Google Ads": "Developer Token + OAuth2 申請が必要",
    "Yahoo!広告": "Yahoo! JAPAN Developers Network で申請",
    "Meta": "Meta for Developers でMarketing API申請",
    "TikTok": "TikTok for Business API 申請",
}.items():
    with st.expander(f"🔴 {platform} — 未連携"):
        st.markdown(f"**申請方法：** {note}")
        st.markdown("API連携後に利用可能になる機能：")
        st.markdown("- データ自動取得（手動CSV不要）\n- 日次・時間別データの自動更新\n- 予算消化率のリアルタイム監視\n- CV・ROAS の自動計算")

st.divider()
st.subheader("データ更新方法（現在）")
st.markdown("""
各媒体の管理画面からCSVをエクスポートし、リポジトリに上書きしてください。

| 媒体 | ファイル名 | エンコード |
|---|---|---|
| Google Ads | `google.csv` | UTF-8（2行ヘッダー） |
| Yahoo!広告 | `yahoo.csv` | UTF-16・タブ区切り |
| Meta | `meta.csv` | UTF-8 |
| TikTok | `tiktok.csv` | Shift-JIS |
""")
