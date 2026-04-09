import streamlit as st

st.markdown("#### 通知設定")
st.caption("アラート・通知の配信先と条件を設定します")

st.write("")

if "notif_settings" not in st.session_state:
    st.session_state["notif_settings"] = {
        "email_enabled": True,
        "email_address": "yamada@example.com",
        "slack_enabled": False,
        "slack_webhook": "",
        "alert_budget_90": True,
        "alert_cpa_over": True,
        "alert_daily_report": False,
        "alert_api_error": True,
    }

settings = st.session_state["notif_settings"]

# ─── 配信先 ───
with st.container(border=True):
    st.markdown("**通知の配信先**")
    st.write("")

    col_e1, col_e2 = st.columns([1, 7])
    with col_e1:
        email_on = st.toggle("メール", value=settings["email_enabled"], key="notif_email")
    with col_e2:
        if email_on:
            email_addr = st.text_input(
                "メールアドレス",
                value=settings["email_address"],
                placeholder="例) yamada@example.com",
                label_visibility="collapsed",
            )
            settings["email_address"] = email_addr
    settings["email_enabled"] = email_on

    st.write("")

    col_s1, col_s2 = st.columns([1, 7])
    with col_s1:
        slack_on = st.toggle("Slack", value=settings["slack_enabled"], key="notif_slack")
    with col_s2:
        if slack_on:
            slack_url = st.text_input(
                "Slack Webhook URL",
                value=settings["slack_webhook"],
                placeholder="例) https://hooks.slack.com/services/...",
                label_visibility="collapsed",
            )
            settings["slack_webhook"] = slack_url
    settings["slack_enabled"] = slack_on

st.write("")

# ─── アラート条件 ───
with st.container(border=True):
    st.markdown("**アラート条件**")
    st.caption("通知を送るタイミングを選択")
    st.write("")

    alerts = [
        ("alert_budget_90",    "予算消化率が90%を超えた時",     "予算オーバーを未然に防ぐ"),
        ("alert_cpa_over",     "CPAが目標の1.5倍を超えた時",   "運用パフォーマンスの低下を検知"),
        ("alert_daily_report", "日次サマリーレポート",          "毎朝8時に前日の実績を配信"),
        ("alert_api_error",    "API連携エラー発生時",          "データ取得失敗を即時通知"),
    ]

    for key, title, desc in alerts:
        col_t, col_s = st.columns([8, 2])
        with col_t:
            st.markdown(f"""
            <div style="padding:6px 0;">
                <div style="font-weight:600;color:#1e1b4b;font-size:14px;">{title}</div>
                <div style="color:#6b7280;font-size:12px;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
        with col_s:
            settings[key] = st.toggle("有効", value=settings[key], key=f"toggle_{key}", label_visibility="collapsed")

st.write("")

col_s, _ = st.columns([2, 8])
with col_s:
    if st.button("通知設定を保存", type="primary", use_container_width=True):
        st.session_state["notif_settings"] = settings
        st.success("通知設定を保存しました（デモ）")
