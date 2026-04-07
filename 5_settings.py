import streamlit as st
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from loader import get_clients

st.title("設定")

st.subheader("クライアント管理")
st.info("本番環境ではGoogleスプレッドシートと連携してクライアント一覧・アカウントIDを管理します。")

clients_data = {
    "船井自動車販売":       {"google_id":"—","yahoo_id":"—","meta_id":"—","tiktok_id":"—","target_cpa":5000,"target_cv":200},
    "フナイモータース":{"google_id":"—","yahoo_id":"—","meta_id":"—","tiktok_id":"—","target_cpa":8000,"target_cv":150},
    "カーライフ船井":    {"google_id":"—","yahoo_id":"—","meta_id":"—","tiktok_id":"—","target_cpa":6000,"target_cv":120},
}
import pandas as pd
df = pd.DataFrame(clients_data).T.reset_index()
df.columns = ["クライアント名","Google ID","Yahoo ID","Meta ID","TikTok ID","目標CPA","目標CV/月"]
st.dataframe(df, use_container_width=True, hide_index=True)

st.divider()
st.subheader("API連携状況")
for platform, note in {
    "Google Ads":  "Developer Token + OAuth2申請が必要",
    "Yahoo!広告":  "Yahoo! JAPAN Developers Networkで申請",
    "Meta":        "Meta for DevelopersでMarketing API申請",
    "TikTok":      "TikTok for Business API申請",
}.items():
    with st.expander(f"🟡 {platform} — 未連携"):
        st.markdown(f"**申請方法：** {note}")
        st.markdown("連携後に利用可能になる機能：\n- データ自動取得（CSV不要）\n- リアルタイム更新\n- CV・ROAS自動計算\n- 予算消化アラート")
