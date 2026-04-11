import streamlit as st
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from loader import load_demo

client = st.session_state.get("client", "A社")

st.markdown("#### 広告一覧")
st.caption(f"{client} の既存広告キャンペーン")

# ─── session_stateで広告リストを管理 ───
if "ads_list" not in st.session_state:
    # デモ用の初期データ（A社のPMAXメインをサンプルとして登録）
    st.session_state["ads_list"] = {
        "A社": [
            {
                "id": "ad_001",
                "name": "4月キャンペーン",
                "platform": "google",
                "platform_name": "Google Ads",
                "ad_type": "PMAX（P-MAX キャンペーン）",
                "campaign": "【PMAX】メイン",
                "status": "配信中",
                "budget": 600000,
                "kpi": "コンバージョン",
                "target_cpa": 5000,
                "created_at": "2026-04-01",
                "main_title": "A社の新商品はこちら",
                "sub_title": "春の新作ラインナップ",
                "description": "A社が自信を持ってお届けする2026年春の新商品。今なら期間限定で送料無料。",
                "landing_url": "https://a-sha.example.com/spring",
                "display_url": "a-sha.example.com/spring",
                "age_range": (25, 54),
                "gender": "すべて",
                "devices": ["PC", "スマートフォン", "タブレット"],
                "area": "全国",
                "interests": ["ファッション", "ライフスタイル"],
            }
        ]
    }

ads = st.session_state["ads_list"].get(client, [])

st.caption(f"登録広告：{len(ads)}件")

st.write("")

# ─── 広告リスト表示 ───
if not ads:
    with st.container(border=True):
        st.markdown("""
        <div style="text-align:center;padding:40px 20px;">
            <div style="color:#9ca3af;font-size:14px;margin-bottom:12px;">
                まだ登録されている広告はありません
            </div>
            <div style="color:#6b7280;font-size:13px;">
                「新規入稿」タブから広告を作成してください
            </div>
        </div>
        """, unsafe_allow_html=True)
else:
    PLATFORM_COLORS = {
        "google": "#6366f1",
        "yahoo":  "#8b5cf6",
        "meta":   "#0ea5e9",
        "tiktok": "#a78bfa",
    }
    STATUS_STYLES = {
        "配信中":   {"bg": "#d1fae5", "color": "#059669"},
        "審査中":   {"bg": "#fef3c7", "color": "#d97706"},
        "停止中":   {"bg": "#fee2e2", "color": "#dc2626"},
        "下書き":   {"bg": "#f3f4f6", "color": "#6b7280"},
    }

    for ad in ads:
        pcolor = PLATFORM_COLORS.get(ad["platform"], "#6b7280")
        sstyle = STATUS_STYLES.get(ad["status"], STATUS_STYLES["下書き"])

        with st.container(border=True):
            # 上段：名前・ステータス・媒体
            head_l, head_r = st.columns([7, 3])
            with head_l:
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px;">
                    <div style="width:8px;height:8px;border-radius:50%;background:{pcolor};"></div>
                    <span style="font-size:16px;font-weight:700;color:#1e1b4b;">{ad['name']}</span>
                    <span style="background:{sstyle['bg']};color:{sstyle['color']};padding:2px 10px;
                                border-radius:6px;font-size:11px;font-weight:600;">
                        {ad['status']}
                    </span>
                </div>
                <div style="color:#6b7280;font-size:12px;">
                    {ad['platform_name']} / {ad['ad_type']} ・ 作成日 {ad['created_at']}
                </div>
                """, unsafe_allow_html=True)

            with head_r:
                btn_col1, btn_col2, btn_col3 = st.columns(3)
                with btn_col1:
                    if st.button("詳細", key=f"detail_{ad['id']}", use_container_width=True):
                        st.session_state[f"show_detail_{ad['id']}"] = not st.session_state.get(f"show_detail_{ad['id']}", False)
                        st.rerun()
                with btn_col2:
                    if st.button("複製", key=f"copy_{ad['id']}", use_container_width=True):
                        # 新規入稿のデータとしてコピー
                        st.session_state["submit_data"] = {
                            "promo_name": f"{ad['name']}（コピー）",
                            "kpi": ad["kpi"],
                            "budget": ad["budget"],
                            "main_title": ad["main_title"],
                            "sub_title": ad["sub_title"],
                            "ad_description": ad["description"],
                            "landing_url": ad["landing_url"],
                            "display_url": ad["display_url"],
                            "age_range": ad["age_range"],
                            "gender": ad["gender"],
                            "interests": ad["interests"],
                            "devices": {"pc": "PC" in ad["devices"],
                                        "smartphone": "スマートフォン" in ad["devices"],
                                        "tablet": "タブレット" in ad["devices"]},
                            "area_mode": "指定しない" if ad["area"]=="全国" else "都道府県指定",
                        }
                        st.session_state["submit_step"] = 1
                        st.success(f"「{ad['name']}」の内容をコピーしました。「新規入稿」タブで編集できます。")
                with btn_col3:
                    if st.button("削除", key=f"delete_{ad['id']}", use_container_width=True):
                        st.session_state["ads_list"][client] = [
                            a for a in ads if a["id"] != ad["id"]
                        ]
                        st.rerun()

            # 下段：KPI情報
            st.write("")
            m1, m2, m3, m4, m5 = st.columns(5)
            m1.metric("月額予算",   f"¥{ad['budget']:,}")
            m2.metric("目標CPA",    f"¥{ad['target_cpa']:,}")
            m3.metric("成果指標",   ad["kpi"])
            m4.metric("配信エリア", ad["area"])
            m5.metric("性別",      ad["gender"])

            # 詳細展開
            if st.session_state.get(f"show_detail_{ad['id']}", False):
                st.write("")
                st.markdown("**広告文**")
                st.markdown(f"""
                <div style="border:1px solid #e5e7eb;border-radius:10px;padding:16px;background:#ffffff;">
                    <div style="color:#1a0dab;font-size:16px;font-weight:500;margin-bottom:2px;">
                        {ad['main_title']} | {ad['sub_title']}
                    </div>
                    <div style="display:flex;align-items:center;gap:6px;margin-bottom:6px;">
                        <span style="background:#f3f4f6;color:#6b7280;font-size:10px;font-weight:700;
                                     padding:1px 5px;border-radius:3px;">広告</span>
                        <span style="color:#006621;font-size:12px;">{ad['display_url']}</span>
                    </div>
                    <div style="color:#4d5156;font-size:13px;line-height:1.5;">
                        {ad['description']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.write("")
                d1, d2 = st.columns(2)
                with d1:
                    st.markdown(f"**遷移先URL**")
                    st.caption(ad["landing_url"])
                    st.markdown(f"**年齢**")
                    st.caption(f"{ad['age_range'][0]}歳 〜 {ad['age_range'][1]}歳")
                with d2:
                    st.markdown(f"**配信デバイス**")
                    st.caption("、".join(ad["devices"]))
                    st.markdown(f"**興味関心**")
                    st.caption("、".join(ad["interests"]) if ad["interests"] else "指定なし")
