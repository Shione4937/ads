import streamlit as st
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from loader import ALL_CLIENTS, DEFAULT_SELECTED

st.markdown("#### ⚙️ 設定")

# 表示企業の選択
st.markdown("**表示企業の選択**")
st.caption("全社一覧タブに表示する担当企業を選んでください")

current = st.session_state.get("selected_clients", DEFAULT_SELECTED)

selected = st.multiselect(
    "担当企業",
    options=ALL_CLIENTS,
    default=current,
)

if st.button("💾 保存", type="primary"):
    if len(selected) == 0:
        st.error("1社以上選択してください")
    else:
        st.session_state["selected_clients"] = selected
        st.success(f"✅ {len(selected)}社を設定しました")

st.divider()

# API連携状況
st.markdown("**API連携状況**")

api_items = {
    "Google Ads":  {"note": "Developer Token + OAuth2申請が必要", "color": "#6366f1"},
    "Yahoo!広告":  {"note": "Yahoo! JAPAN Developers Networkで申請", "color": "#8b5cf6"},
    "Meta":        {"note": "Meta for DevelopersでMarketing API申請", "color": "#38bdf8"},
    "TikTok":      {"note": "TikTok for Business API申請", "color": "#a78bfa"},
}

for platform, info in api_items.items():
    with st.expander(f"🔸 {platform} — 未連携"):
        st.markdown(f"**申請方法：** {info['note']}")
        st.markdown("""連携後に利用可能：
- データ自動取得（手動CSV不要）
- 日次・時間別データの自動更新
- CV・ROAS自動計算""")
