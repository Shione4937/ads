import streamlit as st

st.markdown("#### API連携")
st.caption("各広告媒体のAPI連携状況")

st.write("")

api_items = [
    {
        "name": "Google Ads",
        "color": "#6366f1",
        "status": "未連携",
        "note": "Developer Token + OAuth2 申請が必要",
        "url": "https://developers.google.com/google-ads/api/docs/first-call/overview",
    },
    {
        "name": "Yahoo!広告",
        "color": "#8b5cf6",
        "status": "未連携",
        "note": "Yahoo! JAPAN Developers Network で申請",
        "url": "https://ads-developers.yahoo.co.jp/",
    },
    {
        "name": "Meta 広告",
        "color": "#0ea5e9",
        "status": "未連携",
        "note": "Meta for Developers で Marketing API 申請",
        "url": "https://developers.facebook.com/docs/marketing-apis",
    },
    {
        "name": "TikTok広告",
        "color": "#a78bfa",
        "status": "未連携",
        "note": "TikTok for Business API 申請",
        "url": "https://business-api.tiktok.com/",
    },
]

for item in api_items:
    with st.container(border=True):
        c1, c2, c3 = st.columns([0.6, 7, 2])
        with c1:
            st.markdown(f"""
            <div style="width:36px;height:36px;border-radius:8px;
                        background:{item['color']}15;display:flex;align-items:center;
                        justify-content:center;margin-top:8px;">
                <div style="width:16px;height:16px;border-radius:50%;background:{item['color']};"></div>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div style="padding-top:6px;">
                <div style="display:flex;align-items:center;gap:10px;margin-bottom:2px;">
                    <span style="font-size:15px;font-weight:700;color:#1e1b4b;">{item['name']}</span>
                    <span style="background:#f3f4f6;color:#6b7280;padding:2px 10px;
                                 border-radius:6px;font-size:11px;font-weight:600;">
                        {item['status']}
                    </span>
                </div>
                <div style="color:#6b7280;font-size:12px;">{item['note']}</div>
            </div>
            """, unsafe_allow_html=True)
        with c3:
            if st.button("連携設定", key=f"conn_{item['name']}", use_container_width=True):
                st.info(f"{item['name']} の連携画面を表示（デモ）")

st.write("")

with st.container(border=True):
    st.markdown("**API連携後に利用可能になる機能**")
    st.markdown("""
- データ自動取得（手動CSV不要）
- 日次・時間別データの自動更新
- 予算消化率のリアルタイム監視
- CV・ROAS の自動計算
- 広告の自動入稿・更新
""")
