import streamlit as st
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from loader import ALL_CLIENTS

# ─── 入稿モード ───
client = st.session_state.get("client", "A社")
step = st.session_state.get("submit_step", 1)
data = st.session_state.get("submit_data", {})

STEPS = [
    (1, "基本情報"),
    (2, "連携設定"),
    (3, "商材登録"),
    (4, "デバイス"),
    (5, "エリア"),
    (6, "ターゲット"),
    (7, "広告文"),
    (8, "確認・送信"),
]

# ─── ヘッダー ───
col_h1, col_h2 = st.columns([8, 2])
with col_h1:
    st.markdown(f"""
    <div class="submit-header">
        <div>
            <span class="submit-title">プロモーション新規作成</span>
            <span style="color:#9ca3af;font-size:13px;margin-left:16px;">対象クライアント：<strong style="color:#6366f1;">{client}</strong></span>
        </div>
    </div>
    """, unsafe_allow_html=True)
with col_h2:
    if st.button("× 作成を中断", key="cancel_submit"):
        st.session_state["submit_step"] = 1
        st.session_state["submit_data"] = {}
        st.session_state["mode"] = "分析"
        st.rerun()

# ─── ステップインジケーター ───
step_html = '<div class="step-indicator">'
for i, (num, label) in enumerate(STEPS):
    if num < step:
        circle_class = "step-circle done"
        label_class = "step-label"
        mark = "✓"
    elif num == step:
        circle_class = "step-circle active"
        label_class = "step-label active"
        mark = str(num)
    else:
        circle_class = "step-circle"
        label_class = "step-label"
        mark = str(num)
    step_html += f'<div class="step-item"><div class="{circle_class}">{mark}</div><div class="{label_class}">{label}</div></div>'
    if i < len(STEPS) - 1:
        connector_class = "step-connector done" if num < step else "step-connector"
        step_html += f'<div class="{connector_class}"></div>'
step_html += "</div>"
st.markdown(step_html, unsafe_allow_html=True)

# ─── Step 1: 基本情報 ───
if step == 1:
    st.markdown("##### 基本情報")
    st.caption("プロモーションの基本情報を設定してください")
    st.write("")

    # プロモーション名
    promo_name = st.text_input(
        "プロモーションの任意の名前（宣伝するサービスの総称/サイト名/店舗名）",
        value=data.get("promo_name", ""),
        placeholder="例）A社公式サイト",
    )

    st.write("")
    st.markdown("**成果指標**")
    st.caption("広告配信で重視する成果を選んでください")

    # 成果指標（3カード・クリックで選択）
    current_kpi = data.get("kpi", "クリック")
    # KPIボタン専用のCSSスコープマーカー
    st.markdown('<div class="kpi-marker"></div>', unsafe_allow_html=True)
    k1, k2, k3 = st.columns(3)

    kpi_options = [
        ("クリック", "🖱️", "Webサイトへのアクセスを重視", "kpi_click"),
        ("コンバージョン", "🎯", "資料請求・購入などWebサイト上での成果を重視", "kpi_cv"),
        ("収益", "💰", "売上金額など1コンバージョン毎の価値を重視", "kpi_revenue"),
    ]

    for col, (name, icon, desc, key) in zip([k1, k2, k3], kpi_options):
        with col:
            is_selected = current_kpi == name
            label = f"{icon}   {name}\n\n{desc}"
            btn_type = "primary" if is_selected else "secondary"
            if st.button(label, key=key, use_container_width=True, type=btn_type):
                data["kpi"] = name
                st.session_state["submit_data"] = data
                st.rerun()

    st.write("")
    st.markdown("**月額予算**")
    budget = st.number_input(
        "月額予算（円）",
        min_value=0,
        value=data.get("budget", 100000),
        step=10000,
        format="%d",
        label_visibility="collapsed",
    )

    st.write("")
    st.divider()

    # ナビゲーションボタン
    nav_l, nav_c, nav_r = st.columns([1, 6, 1])
    with nav_r:
        if st.button("次へ →", type="primary", use_container_width=True, key="next_1"):
            data["promo_name"] = promo_name
            data["budget"] = budget
            if not promo_name:
                st.error("プロモーション名を入力してください")
            else:
                st.session_state["submit_data"] = data
                st.session_state["submit_step"] = 2
                st.rerun()

# ─── Step 2以降: プレースホルダー ───
else:
    step_label = dict(STEPS)[step]
    st.markdown(f"##### {step_label}")
    st.info(f"📝 **{step_label}** の画面は Phase 2 で実装予定です。")

    with st.container(border=True):
        st.markdown("**これまでに入力された内容**")
        if data.get("promo_name"):
            st.write(f"・プロモーション名：**{data['promo_name']}**")
        if data.get("kpi"):
            st.write(f"・成果指標：**{data['kpi']}**")
        if data.get("budget"):
            st.write(f"・月額予算：**¥{data['budget']:,}**")
        st.write(f"・対象クライアント：**{client}**")

    st.write("")
    st.divider()

    # ナビゲーションボタン
    nav_l, nav_c, nav_r = st.columns([1, 6, 1])
    with nav_l:
        if st.button("← 戻る", use_container_width=True, key=f"prev_{step}"):
            st.session_state["submit_step"] = step - 1
            st.rerun()
    with nav_r:
        if step < 8:
            if st.button("次へ →", type="primary", use_container_width=True, key=f"next_{step}"):
                st.session_state["submit_step"] = step + 1
                st.rerun()
        else:
            if st.button("入稿する", type="primary", use_container_width=True, key="submit_final"):
                st.success("✅ 入稿完了（デモ）— API連携後に実際の配信が開始されます")
                st.balloons()
