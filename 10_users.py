import streamlit as st

st.markdown("#### ユーザー管理")
st.caption("AdBoardにアクセスできるユーザーの管理")

st.write("")

# デモ用ユーザーデータ
if "users_list" not in st.session_state:
    st.session_state["users_list"] = [
        {"name": "瀬尾",   "email": "seo@example.com",     "role": "管理者",   "last_login": "2026-04-14"},
        {"name": "森田",   "email": "morita@example.com",  "role": "運用者",   "last_login": "2026-04-13"},
        {"name": "大久保", "email": "okubo@example.com",   "role": "閲覧のみ", "last_login": "2026-04-10"},
    ]

# ─── 新規追加ボタン ───
col_info, col_add = st.columns([7, 2])
with col_info:
    st.caption(f"登録ユーザー：{len(st.session_state['users_list'])}名")
with col_add:
    if st.button("ユーザーを追加", type="primary", use_container_width=True):
        st.info("ユーザー追加フォームを表示（デモ）")

st.write("")

# ─── ユーザーリスト ───
ROLE_STYLES = {
    "管理者":   {"bg": "#ede9fe", "color": "#6d28d9"},
    "運用者":   {"bg": "#dbeafe", "color": "#1d4ed8"},
    "閲覧のみ": {"bg": "#f3f4f6", "color": "#6b7280"},
}

for user in st.session_state["users_list"]:
    rstyle = ROLE_STYLES.get(user["role"], ROLE_STYLES["閲覧のみ"])
    with st.container(border=True):
        c1, c2, c3, c4 = st.columns([3, 3, 2, 2])
        with c1:
            st.markdown(f"""
            <div style="padding-top:4px;">
                <div style="font-weight:700;color:#1e1b4b;font-size:14px;">{user['name']}</div>
                <div style="color:#6b7280;font-size:12px;">{user['email']}</div>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div style="padding-top:10px;">
                <span style="background:{rstyle['bg']};color:{rstyle['color']};padding:4px 12px;
                             border-radius:6px;font-size:12px;font-weight:600;">
                    {user['role']}
                </span>
            </div>
            """, unsafe_allow_html=True)
        with c3:
            st.markdown(f"""
            <div style="padding-top:8px;color:#6b7280;font-size:12px;">
                最終ログイン<br>
                <span style="color:#1e1b4b;font-weight:600;">{user['last_login']}</span>
            </div>
            """, unsafe_allow_html=True)
        with c4:
            b1, b2 = st.columns(2)
            with b1:
                if st.button("編集", key=f"edit_{user['email']}", use_container_width=True):
                    st.info("編集フォーム（デモ）")
            with b2:
                if st.button("削除", key=f"del_{user['email']}", use_container_width=True):
                    st.session_state["users_list"] = [
                        u for u in st.session_state["users_list"] if u["email"] != user["email"]
                    ]
                    st.rerun()

st.write("")
st.caption("権限レベル：管理者＝全機能 / 運用者＝閲覧＋入稿 / 閲覧のみ＝ダッシュボード閲覧のみ")
