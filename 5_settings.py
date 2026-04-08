import streamlit as st
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from loader import ALL_CLIENTS, DEFAULT_SELECTED

st.markdown("#### 設定")

st.markdown("**表示企業の選択**")
st.caption("全社一覧タブに表示する担当企業を選んでください")

current = st.session_state.get("selected_clients", DEFAULT_SELECTED)

selected = st.multiselect(
    "担当企業",
    options=ALL_CLIENTS,
    default=current,
)

if st.button("保存"):
    if len(selected) == 0:
        st.error("1社以上選択してください")
    else:
        st.session_state["selected_clients"] = selected
        st.success(f"{len(selected)}社を設定しました")

st.divider()
st.markdown("**API連携状況**")
for platform, note in {
    "Google Ads":  "Developer Token + OAuth2申請が必要",
    "Yahoo!広告":  "Yahoo! JAPAN Developers Networkで申請",
    "Meta":        "Meta for DevelopersでMarketing API申請",
    "TikTok":      "TikTok for Business API申請",
}.items():
    with st.expander(f"🟡 {platform} — 未連携"):
        st.markdown(f"**申請方法：** {note}")
        st.markdown("連携後に利用可能：\n- データ自動取得\n- リアルタイム更新\n- CV・ROAS自動計算")
