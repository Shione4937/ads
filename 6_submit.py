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
    (3, "デバイス"),
    (4, "エリア"),
    (5, "ターゲット"),
    (6, "広告文"),
    (7, "確認・送信"),
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
        mark = str(num)
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


# ========================================
# Step 1: 基本情報
# ========================================
if step == 1:
    st.markdown("##### 基本情報")
    st.caption("プロモーションの基本情報を設定してください")
    st.write("")

    promo_name = st.text_input(
        "プロモーションの任意の名前（宣伝するサービスの総称/サイト名/店舗名）",
        value=data.get("promo_name", ""),
        placeholder="例）A社公式サイト",
    )

    st.write("")
    st.markdown("**成果指標**")
    st.caption("広告配信で重視する成果を選んでください")

    current_kpi = data.get("kpi", "クリック")
    st.markdown('<div class="kpi-marker"></div>', unsafe_allow_html=True)
    k1, k2, k3 = st.columns(3)

    kpi_options = [
        ("クリック", "Webサイトへのアクセスを重視", "kpi_click"),
        ("コンバージョン", "資料請求・購入などWebサイト上での成果を重視", "kpi_cv"),
        ("収益", "売上金額など1コンバージョン毎の価値を重視", "kpi_revenue"),
    ]

    for col, (name, desc, key) in zip([k1, k2, k3], kpi_options):
        with col:
            is_selected = current_kpi == name
            label = f"{name}\n\n{desc}"
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


# ========================================
# Step 2: 連携設定
# ========================================
elif step == 2:
    st.markdown("##### 連携設定")
    st.caption("広告配信する媒体のAPIを連携してください（デモ版では連携状態をシミュレートします）")
    st.write("")

    connections = data.get("connections", {"google": False, "yahoo": False, "meta": False, "tiktok": False})

    platforms = [
        ("google", "Google Ads", "#6366f1", "検索・ディスプレイ・YouTube・ショッピング広告"),
        ("yahoo",  "Yahoo!広告",  "#8b5cf6", "検索連動型・ディスプレイ広告（YDA）"),
        ("meta",   "Meta広告",    "#38bdf8", "Facebook・Instagram・Messenger広告"),
        ("tiktok", "TikTok広告",  "#a78bfa", "インフィード・トップビュー広告"),
    ]

    for pid, pname, pcolor, pdesc in platforms:
        is_connected = connections.get(pid, False)
        with st.container(border=True):
            c1, c2, c3 = st.columns([0.5, 6, 2])
            with c1:
                st.markdown(f"""
                <div style="width:36px;height:36px;border-radius:8px;
                            background:{pcolor}15;display:flex;align-items:center;
                            justify-content:center;margin-top:6px;">
                    <div style="width:16px;height:16px;border-radius:50%;background:{pcolor};"></div>
                </div>
                """, unsafe_allow_html=True)
            with c2:
                badge_color = "#10b981" if is_connected else "#9ca3af"
                badge_bg = "#d1fae5" if is_connected else "#f3f4f6"
                badge_text = "連携済" if is_connected else "未連携"
                st.markdown(f"""
                <div style="padding-top:4px;">
                    <div style="display:flex;align-items:center;gap:10px;margin-bottom:2px;">
                        <span style="font-size:15px;font-weight:700;color:#1e1b4b;">{pname}</span>
                        <span style="background:{badge_bg};color:{badge_color};
                                     padding:2px 10px;border-radius:6px;font-size:11px;font-weight:600;">
                            {badge_text}
                        </span>
                    </div>
                    <div style="color:#6b7280;font-size:12px;">{pdesc}</div>
                </div>
                """, unsafe_allow_html=True)
            with c3:
                if is_connected:
                    if st.button("解除", key=f"disconnect_{pid}", use_container_width=True):
                        connections[pid] = False
                        data["connections"] = connections
                        st.session_state["submit_data"] = data
                        st.rerun()
                else:
                    if st.button("連携する", key=f"connect_{pid}", type="primary", use_container_width=True):
                        connections[pid] = True
                        data["connections"] = connections
                        st.session_state["submit_data"] = data
                        st.rerun()

    st.write("")
    connected_count = sum(1 for v in connections.values() if v)
    if connected_count == 0:
        st.warning("最低1つの媒体を連携してください（デモ版では「連携する」ボタンで疑似連携できます）")

    st.divider()
    nav_l, _, nav_r = st.columns([1, 6, 1])
    with nav_l:
        if st.button("← 戻る", use_container_width=True, key="prev_2"):
            st.session_state["submit_step"] = 1
            st.rerun()
    with nav_r:
        if st.button("次へ →", type="primary", use_container_width=True, key="next_2",
                     disabled=(connected_count == 0)):
            st.session_state["submit_step"] = 3
            st.rerun()


# ========================================
# Step 3: デバイス
# ========================================
elif step == 3:
    st.markdown("##### デバイス")
    st.caption("広告を配信するデバイスを選択してください")
    st.write("")

    devices = data.get("devices", {"pc": True, "smartphone": True, "tablet": True})

    st.markdown('<div class="kpi-marker"></div>', unsafe_allow_html=True)
    d1, d2, d3 = st.columns(3)

    device_options = [
        ("pc",         "PC",           "デスクトップ・ノートPC", "dev_pc"),
        ("smartphone", "スマートフォン", "iPhone・Android",       "dev_sp"),
        ("tablet",     "タブレット",    "iPad・Androidタブレット", "dev_tab"),
    ]

    for col, (did, name, desc, key) in zip([d1, d2, d3], device_options):
        with col:
            is_selected = devices.get(did, True)
            label = f"{name}\n\n{desc}"
            btn_type = "primary" if is_selected else "secondary"
            if st.button(label, key=key, use_container_width=True, type=btn_type):
                devices[did] = not is_selected
                data["devices"] = devices
                st.session_state["submit_data"] = data
                st.rerun()

    st.write("")
    selected_count = sum(1 for v in devices.values() if v)
    st.caption(f"現在 **{selected_count}** デバイス選択中")

    st.divider()
    nav_l, _, nav_r = st.columns([1, 6, 1])
    with nav_l:
        if st.button("← 戻る", use_container_width=True, key="prev_3"):
            st.session_state["submit_step"] = 2
            st.rerun()
    with nav_r:
        if st.button("次へ →", type="primary", use_container_width=True, key="next_3",
                     disabled=(selected_count == 0)):
            st.session_state["submit_step"] = 4
            st.rerun()


# ========================================
# Step 4: エリア
# ========================================
elif step == 4:
    st.markdown("##### エリア")
    st.caption("広告出稿対象のエリアを指定してください")
    st.write("")

    area_mode = data.get("area_mode", "指定しない")

    # エリアモード選択（3カード）
    st.markdown('<div class="kpi-marker"></div>', unsafe_allow_html=True)
    a1, a2, a3 = st.columns(3)

    area_options = [
        ("店舗集客",    "店舗に集客したい方",   "店舗を指定してピンポイント配信", "area_store"),
        ("都道府県指定", "都道府県で指定",      "配信する都道府県を選択",       "area_pref"),
        ("指定しない",   "指定しない",         "全国配信",                   "area_none"),
    ]

    for col, (mode_name, name, desc, key) in zip([a1, a2, a3], area_options):
        with col:
            is_selected = area_mode == mode_name
            label = f"{name}\n\n{desc}"
            btn_type = "primary" if is_selected else "secondary"
            if st.button(label, key=key, use_container_width=True, type=btn_type):
                data["area_mode"] = mode_name
                st.session_state["submit_data"] = data
                st.rerun()

    st.write("")

    # 選択モードに応じた詳細入力
    if area_mode == "店舗集客":
        with st.container(border=True):
            st.markdown("**店舗情報**")
            s1, s2 = st.columns(2)
            with s1:
                store_name = st.text_input("店舗名", value=data.get("store_name",""), placeholder="例）渋谷本店")
                store_zip = st.text_input("郵便番号", value=data.get("store_zip",""), placeholder="例）150-0002")
                store_addr = st.text_input("住所", value=data.get("store_addr",""), placeholder="例）東京都渋谷区渋谷1-1-1")
            with s2:
                store_phone = st.text_input("電話番号", value=data.get("store_phone",""), placeholder="例）03-1234-5678")
                store_radius = st.number_input("配信範囲（km）", min_value=1, max_value=100,
                                                value=data.get("store_radius", 15), step=1)
            data["store_name"] = store_name
            data["store_zip"]  = store_zip
            data["store_addr"] = store_addr
            data["store_phone"]= store_phone
            data["store_radius"]= store_radius

    elif area_mode == "都道府県指定":
        with st.container(border=True):
            st.markdown("**配信する都道府県を選択**")
            st.caption("複数選択可")
            selected_prefs = data.get("selected_prefs", [])

            regions = {
                "北海道・東北": ["北海道","青森県","岩手県","宮城県","秋田県","山形県","福島県"],
                "関東":        ["茨城県","栃木県","群馬県","埼玉県","千葉県","東京都","神奈川県"],
                "甲信越・北陸": ["新潟県","富山県","石川県","福井県","山梨県","長野県"],
                "東海":        ["岐阜県","静岡県","愛知県","三重県"],
                "関西":        ["滋賀県","京都府","大阪府","兵庫県","奈良県","和歌山県"],
                "中国":        ["鳥取県","島根県","岡山県","広島県","山口県"],
                "四国":        ["徳島県","香川県","愛媛県","高知県"],
                "九州・沖縄":   ["福岡県","佐賀県","長崎県","熊本県","大分県","宮崎県","鹿児島県","沖縄県"],
            }

            new_selected = []
            for region, prefs in regions.items():
                st.markdown(f"**{region}**")
                cols = st.columns(7)
                for i, pref in enumerate(prefs):
                    with cols[i % 7]:
                        checked = pref in selected_prefs
                        if st.checkbox(pref, value=checked, key=f"pref_{pref}"):
                            new_selected.append(pref)
                st.write("")
            data["selected_prefs"] = new_selected

    else:
        st.info("全国に広告を配信します")

    st.session_state["submit_data"] = data
    st.divider()
    nav_l, _, nav_r = st.columns([1, 6, 1])
    with nav_l:
        if st.button("← 戻る", use_container_width=True, key="prev_4"):
            st.session_state["submit_step"] = 3
            st.rerun()
    with nav_r:
        if st.button("次へ →", type="primary", use_container_width=True, key="next_4"):
            st.session_state["submit_step"] = 5
            st.rerun()


# ========================================
# Step 5: ターゲット
# ========================================
elif step == 5:
    st.markdown("##### ターゲット設定")
    st.caption("広告を配信するユーザー属性を設定してください")
    st.write("")

    col_age, col_gender = st.columns(2)
    with col_age:
        st.markdown("**年齢**")
        age_range = st.slider("age_range", 18, 65,
                               value=data.get("age_range", (25, 54)),
                               label_visibility="collapsed")
        st.caption(f"{age_range[0]}歳 〜 {age_range[1]}歳")

    with col_gender:
        st.markdown("**性別**")
        gender = st.radio("gender",
                          ["すべて", "男性", "女性"],
                          index=["すべて","男性","女性"].index(data.get("gender","すべて")),
                          horizontal=True,
                          label_visibility="collapsed")

    st.write("")
    st.markdown("**興味関心カテゴリ**")
    st.caption("複数選択可")
    interest_options = [
        "ビジネス・経済", "IT・テクノロジー", "ファッション", "美容・コスメ",
        "グルメ・料理", "旅行・レジャー", "スポーツ", "エンタメ・音楽",
        "教育・学習", "健康・フィットネス", "自動車", "不動産・住宅",
        "金融・投資", "育児・子育て", "ペット",
    ]
    interests = st.multiselect(
        "興味関心",
        options=interest_options,
        default=data.get("interests", []),
        label_visibility="collapsed",
    )

    st.write("")
    st.markdown("**配信時間帯**")
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        time_start = st.time_input("開始時刻",
                                    value=data.get("time_start"),
                                    key="time_start_input")
    with col_t2:
        time_end = st.time_input("終了時刻",
                                  value=data.get("time_end"),
                                  key="time_end_input")

    data["age_range"] = age_range
    data["gender"] = gender
    data["interests"] = interests
    data["time_start"] = time_start
    data["time_end"] = time_end
    st.session_state["submit_data"] = data

    st.divider()
    nav_l, _, nav_r = st.columns([1, 6, 1])
    with nav_l:
        if st.button("← 戻る", use_container_width=True, key="prev_5"):
            st.session_state["submit_step"] = 4
            st.rerun()
    with nav_r:
        if st.button("次へ →", type="primary", use_container_width=True, key="next_5"):
            st.session_state["submit_step"] = 6
            st.rerun()


# ========================================
# Step 6: 広告文作成
# ========================================
elif step == 6:
    st.markdown("##### 広告文作成")
    st.caption("広告の見出しと説明文を入力してください")
    st.write("")

    col_left, col_right = st.columns([3, 2])

    with col_left:
        main_title = st.text_input(
            "メインタイトル（30文字以内）",
            value=data.get("main_title", ""),
            max_chars=30,
            placeholder="例）初心者でもプロの広告運用",
        )
        sub_title = st.text_input(
            "サブタイトル（30文字以内）",
            value=data.get("sub_title", ""),
            max_chars=30,
            placeholder="例）受け身でできる広告運用ツール",
        )
        ad_description = st.text_area(
            "説明文（90文字以内）",
            value=data.get("ad_description", ""),
            max_chars=90,
            placeholder="例）時間やコストを極力かけずに、高い成果を目指すならAdBoard。2ヶ月無料・Googleアナリティクス連携・事前の学習/経験不要",
            height=100,
        )
        st.write("")
        st.markdown("**遷移先URL**（広告クリック後のリンク先）")
        landing_url = st.text_input(
            "遷移先URL",
            value=data.get("landing_url", ""),
            placeholder="例）https://example.com/lp",
            label_visibility="collapsed",
        )
        display_url = st.text_input(
            "表示URL（広告上に表示される短縮URL）",
            value=data.get("display_url", ""),
            placeholder="例）example.com/adboard",
        )

    with col_right:
        st.markdown("**プレビュー**")
        preview_title = main_title or "メインタイトル"
        preview_sub = sub_title or "サブタイトル"
        preview_desc = ad_description or "説明文がここに表示されます"
        preview_url = display_url or "example.com"

        st.markdown(f"""
        <div style="border:1px solid #e5e7eb;border-radius:10px;padding:16px;background:#ffffff;">
            <div style="color:#1a0dab;font-size:16px;font-weight:500;margin-bottom:2px;line-height:1.4;">
                {preview_title} | {preview_sub}
            </div>
            <div style="display:flex;align-items:center;gap:6px;margin-bottom:6px;">
                <span style="background:#f3f4f6;color:#6b7280;font-size:10px;font-weight:700;
                             padding:1px 5px;border-radius:3px;">広告</span>
                <span style="color:#006621;font-size:12px;">{preview_url}</span>
            </div>
            <div style="color:#4d5156;font-size:13px;line-height:1.5;">
                {preview_desc}
            </div>
        </div>
        <div style="color:#9ca3af;font-size:11px;margin-top:8px;">※ 検索広告のプレビュー</div>
        """, unsafe_allow_html=True)

    data["main_title"] = main_title
    data["sub_title"] = sub_title
    data["ad_description"] = ad_description
    data["landing_url"] = landing_url
    data["display_url"] = display_url
    st.session_state["submit_data"] = data

    st.divider()
    nav_l, _, nav_r = st.columns([1, 6, 1])
    with nav_l:
        if st.button("← 戻る", use_container_width=True, key="prev_6"):
            st.session_state["submit_step"] = 5
            st.rerun()
    with nav_r:
        if st.button("次へ →", type="primary", use_container_width=True, key="next_6"):
            if not main_title or not ad_description or not landing_url:
                st.error("メインタイトル・説明文・遷移先URLは必須です")
            else:
                st.session_state["submit_step"] = 7
                st.rerun()


# ========================================
# Step 7: 確認・送信
# ========================================
elif step == 7:
    st.markdown("##### 入稿内容の確認")
    st.caption("以下の内容で広告を入稿します。内容に誤りがないかご確認ください")
    st.write("")

    def field(label, value):
        st.markdown(f"""
        <div style="display:flex;padding:10px 0;border-bottom:1px solid #f3f4f6;">
            <div style="width:180px;color:#6b7280;font-size:13px;font-weight:600;">{label}</div>
            <div style="flex:1;color:#1e1b4b;font-size:14px;">{value}</div>
        </div>
        """, unsafe_allow_html=True)

    # 基本情報
    with st.container(border=True):
        st.markdown("**基本情報**")
        field("対象クライアント", client)
        field("プロモーション名", data.get("promo_name", "—"))
        field("成果指標", data.get("kpi", "—"))
        field("月額予算", f"¥{data.get('budget', 0):,}")

    # 連携媒体
    with st.container(border=True):
        st.markdown("**連携媒体**")
        conns = data.get("connections", {})
        conn_names = {"google":"Google Ads","yahoo":"Yahoo!広告","meta":"Meta広告","tiktok":"TikTok広告"}
        connected = [conn_names[k] for k, v in conns.items() if v]
        field("連携済み媒体", "、".join(connected) if connected else "—")

    # 配信設定
    with st.container(border=True):
        st.markdown("**配信設定**")
        devs = data.get("devices", {})
        dev_labels = {"pc":"PC","smartphone":"スマートフォン","tablet":"タブレット"}
        dev_list = [dev_labels[k] for k, v in devs.items() if v]
        field("デバイス", "、".join(dev_list) if dev_list else "—")

        area_mode = data.get("area_mode", "—")
        if area_mode == "店舗集客":
            area_text = f"{area_mode}（{data.get('store_name','')} / 半径{data.get('store_radius',0)}km）"
        elif area_mode == "都道府県指定":
            prefs = data.get("selected_prefs", [])
            area_text = f"{area_mode}（{len(prefs)}都道府県）" if prefs else area_mode
        else:
            area_text = area_mode
        field("エリア", area_text)

        age_range = data.get("age_range", (25, 54))
        field("年齢", f"{age_range[0]}歳 〜 {age_range[1]}歳")
        field("性別", data.get("gender", "—"))
        interests = data.get("interests", [])
        field("興味関心", "、".join(interests) if interests else "指定なし")

    # 広告文
    with st.container(border=True):
        st.markdown("**広告文**")
        field("メインタイトル", data.get("main_title", "—"))
        field("サブタイトル", data.get("sub_title", "—"))
        field("説明文", data.get("ad_description", "—"))
        field("遷移先URL", data.get("landing_url", "—"))
        field("表示URL", data.get("display_url", "—"))

    st.write("")

    # 最終確認
    confirmed = st.checkbox("上記の内容で間違いないことを確認しました")

    st.divider()
    nav_l, _, nav_r = st.columns([1, 6, 1])
    with nav_l:
        if st.button("← 戻る", use_container_width=True, key="prev_7"):
            st.session_state["submit_step"] = 6
            st.rerun()
    with nav_r:
        if st.button("入稿する", type="primary", use_container_width=True,
                     key="submit_final", disabled=not confirmed):
            st.session_state["submit_completed"] = True
            st.rerun()

    # 完了表示
    if st.session_state.get("submit_completed"):
        st.success("**入稿完了しました**（デモ版）")
        st.info("実際のAPI連携後は、各媒体に自動入稿され配信が開始されます。")
        st.balloons()
        if st.button("新しい入稿を作成", key="new_submit"):
            st.session_state["submit_step"] = 1
            st.session_state["submit_data"] = {}
            st.session_state["submit_completed"] = False
            st.rerun()


