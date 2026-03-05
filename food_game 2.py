import streamlit as st
import random

# ══════════════════════════════════════════════
# 頁面基本設定
# ══════════════════════════════════════════════
st.set_page_config(page_title="食物分類遊戲 🍽️", layout="wide", initial_sidebar_state="collapsed")

# ─────────────── GitHub 圖片路徑 ───────────────
GITHUB_BASE = "https://raw.githubusercontent.com/HLH2000/Food_Game/main/%E9%A3%9F%E7%89%A9%E5%9C%96/"

def get_image_url(card_name: str) -> str:
    """將卡片名稱對應到 GitHub 圖片 URL（特殊卡去掉★）"""
    from urllib.parse import quote
    base = card_name.lstrip("★").strip()
    return GITHUB_BASE + quote(base, safe="") + ".jpg"

# ─────────────── 遊戲資料 ───────────────
CATEGORIES = ["🥩 肉類/海鮮", "🥦 蔬菜", "🍎 水果", "🧁 甜點/飲料"]

CAT_COLORS = {
    "🥩 肉類/海鮮": "#FECACA",
    "🥦 蔬菜":      "#BBF7D0",
    "🍎 水果":      "#FED7AA",
    "🧁 甜點/飲料": "#E9D5FF",
}

CAT_HEADER_COLORS = {
    "🥩 肉類/海鮮": "#EF4444",
    "🥦 蔬菜":      "#22C55E",
    "🍎 水果":      "#F97316",
    "🧁 甜點/飲料": "#A855F7",
}

CARDS = {
    # 肉類/海鮮
    "培根":   {"valid": ["🥩 肉類/海鮮"], "special": False},
    "牛排":   {"valid": ["🥩 肉類/海鮮"], "special": False},
    "炸雞":   {"valid": ["🥩 肉類/海鮮"], "special": False},
    "烤雞腿": {"valid": ["🥩 肉類/海鮮"], "special": False},
    "熟蝦":   {"valid": ["🥩 肉類/海鮮"], "special": False},
    "鮭魚":   {"valid": ["🥩 肉類/海鮮"], "special": False},
    "鮪魚":   {"valid": ["🥩 肉類/海鮮"], "special": False},
    "龍蝦":   {"valid": ["🥩 肉類/海鮮"], "special": False},
    "螃蟹":   {"valid": ["🥩 肉類/海鮮"], "special": False},
    "扇貝":   {"valid": ["🥩 肉類/海鮮"], "special": False},
    "臘肉":   {"valid": ["🥩 肉類/海鮮"], "special": False},
    "雞排":   {"valid": ["🥩 肉類/海鮮"], "special": False},
    # 蔬菜
    "南瓜":   {"valid": ["🥦 蔬菜"], "special": False},
    "大白菜": {"valid": ["🥦 蔬菜"], "special": False},
    "彩椒":   {"valid": ["🥦 蔬菜"], "special": False},
    "玉米":   {"valid": ["🥦 蔬菜"], "special": False},
    "白蘿蔔": {"valid": ["🥦 蔬菜"], "special": False},
    "紫甘藍": {"valid": ["🥦 蔬菜"], "special": False},
    "茄子":   {"valid": ["🥦 蔬菜"], "special": False},
    "蘆筍":   {"valid": ["🥦 蔬菜"], "special": False},
    "青花菜": {"valid": ["🥦 蔬菜"], "special": False},
    "杏鮑菇": {"valid": ["🥦 蔬菜"], "special": False},
    "蕈菇":   {"valid": ["🥦 蔬菜"], "special": False},
    # 水果
    "奇異果": {"valid": ["🍎 水果"], "special": False},
    "木瓜":   {"valid": ["🍎 水果"], "special": False},
    "橘子":   {"valid": ["🍎 水果"], "special": False},
    "水蜜桃": {"valid": ["🍎 水果"], "special": False},
    "西瓜":   {"valid": ["🍎 水果"], "special": False},
    "藍莓":   {"valid": ["🍎 水果"], "special": False},
    # 甜點/飲料
    "千層派":    {"valid": ["🧁 甜點/飲料"], "special": False},
    "巧克力":    {"valid": ["🧁 甜點/飲料"], "special": False},
    "巧克力豆餅":{"valid": ["🧁 甜點/飲料"], "special": False},
    "甜甜圈":    {"valid": ["🧁 甜點/飲料"], "special": False},
    "湯圓":      {"valid": ["🧁 甜點/飲料"], "special": False},
    "糖果":      {"valid": ["🧁 甜點/飲料"], "special": False},
    "糖葫蘆":    {"valid": ["🧁 甜點/飲料"], "special": False},
    "鯛魚燒":    {"valid": ["🧁 甜點/飲料"], "special": False},
    "優格":      {"valid": ["🧁 甜點/飲料"], "special": False},
    "優酪乳":    {"valid": ["🧁 甜點/飲料"], "special": False},
    "珍珠奶茶":  {"valid": ["🧁 甜點/飲料"], "special": False},
    "爆米花":    {"valid": ["🧁 甜點/飲料"], "special": False},
    # ★ 特殊卡 (多類別)
    "★藍莓起司蛋糕": {"valid": ["🍎 水果", "🧁 甜點/飲料"], "special": True},
    "★披薩":         {"valid": ["🥩 肉類/海鮮", "🥦 蔬菜"], "special": True},
    "★涼拌豆腐":     {"valid": ["🥦 蔬菜", "🧁 甜點/飲料"], "special": True},
    "★滷肉飯":       {"valid": ["🥩 肉類/海鮮", "🥦 蔬菜"], "special": True},
}

BASE_SCORE = 50

# ─────────────── 初始化 Session State ───────────────
if "game_init" not in st.session_state:
    st.session_state.game_init = True
    st.session_state.score = 0
    st.session_state.submit_count = 0
    st.session_state.locked = False
    st.session_state.scored_keys = set()
    st.session_state.selected = set()
    st.session_state.result = {}
    st.session_state.placed = {cat: [] for cat in CATEGORIES}
    st.session_state.message = ""
    st.session_state.message_type = "info"
    deck = list(CARDS.keys())
    random.shuffle(deck)
    st.session_state.deck = deck

# ─────────────── 輔助函數 ───────────────
def get_remaining_cards():
    out = []
    for name in st.session_state.deck:
        info = CARDS[name]
        placed_count = sum(1 for cat in CATEGORIES if name in st.session_state.placed[cat])
        if info["special"]:
            if placed_count < len(info["valid"]):
                out.append(name)
        else:
            if placed_count == 0:
                out.append(name)
    return out

def get_multiplier():
    return 1.0 / (2 ** st.session_state.submit_count)

def get_pts():
    return max(1, round(BASE_SCORE * get_multiplier()))

def total_needed():
    return sum(len(c["valid"]) for c in CARDS.values())

# ─────────────── Callbacks ───────────────
def toggle_select(name):
    if st.session_state.locked:
        return
    if name in st.session_state.selected:
        st.session_state.selected.discard(name)
    else:
        st.session_state.selected.add(name)

def place_selected(target_cat):
    if st.session_state.locked:
        return
    if not st.session_state.selected:
        st.session_state.message = "⚠️ 請先點選手牌卡片！"
        st.session_state.message_type = "warning"
        return
    placed_n, skipped_n = 0, 0
    for name in list(st.session_state.selected):
        info = CARDS[name]
        if name in st.session_state.placed[target_cat]:
            skipped_n += 1
            continue
        if not info["special"]:
            old_cat = next((c for c in CATEGORIES if name in st.session_state.placed[c]), None)
            if old_cat:
                old_key = f"{name}|{old_cat}"
                if old_key in st.session_state.scored_keys:
                    skipped_n += 1
                    continue
                st.session_state.placed[old_cat].remove(name)
                st.session_state.result.pop(old_key, None)
        st.session_state.placed[target_cat].append(name)
        st.session_state.result.pop(f"{name}|{target_cat}", None)
        st.session_state.selected.discard(name)
        placed_n += 1
    if placed_n:
        st.session_state.message = f"✅ 成功放入 {placed_n} 張卡片至【{target_cat}】"
        st.session_state.message_type = "success"
    else:
        st.session_state.message = "⚠️ 所選卡片已在此類別或已鎖定"
        st.session_state.message_type = "warning"

def remove_card(name, from_cat):
    if st.session_state.locked:
        return
    key = f"{name}|{from_cat}"
    if key in st.session_state.scored_keys:
        return
    st.session_state.placed[from_cat].remove(name)
    st.session_state.result.pop(key, None)
    st.session_state.selected.discard(name)

def submit_answers():
    if st.session_state.locked:
        return
    rem = get_remaining_cards()
    if rem:
        st.session_state.message = f"⚠️ 還有 {len(rem)} 張在手牌，請全部放入後再提交！"
        st.session_state.message_type = "warning"
        return
    new_correct, wrong, new_pts = 0, 0, 0
    pts = get_pts()
    for cat in CATEGORIES:
        for name in st.session_state.placed[cat]:
            key = f"{name}|{cat}"
            if cat in CARDS[name]["valid"]:
                st.session_state.result[key] = "correct"
                if key not in st.session_state.scored_keys:
                    st.session_state.scored_keys.add(key)
                    new_pts += pts
                    new_correct += 1
            else:
                st.session_state.result[key] = "wrong"
                wrong += 1
    st.session_state.submit_count += 1
    st.session_state.score += new_pts
    if wrong == 0 and len(st.session_state.scored_keys) >= total_needed():
        st.session_state.locked = True
        st.session_state.message = f"🎉 完美全對！本次獲得 {new_pts} 分，總分 {st.session_state.score} 分！"
        st.session_state.message_type = "success"
    else:
        st.session_state.message = f"批改完成：新答對 {new_correct} 題，答錯 {wrong} 題。獲得 {new_pts} 分。"
        st.session_state.message_type = "info" if wrong == 0 else "warning"

def restart_game():
    for k in list(st.session_state.keys()):
        del st.session_state[k]

# ══════════════════════════════════════════════
# CSS 樣式注入
# ══════════════════════════════════════════════
st.markdown("""
<style>
/* 全頁背景 */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #FFF9F0 0%, #FFF0F5 50%, #F5F0FF 100%);
}
[data-testid="stHeader"] { background: transparent; }

/* 隱藏 Streamlit 預設 padding */
.block-container { padding-top: 1rem !important; }

/* 標題區 */
.game-header {
    background: linear-gradient(135deg, #FF6B6B, #FF922B, #CC5DE8);
    border-radius: 20px;
    padding: 18px 28px;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 8px 32px rgba(255,107,107,0.3);
}
.game-title {
    font-size: 1.8rem;
    font-weight: 900;
    color: white;
    text-shadow: 2px 2px 0 rgba(0,0,0,0.15);
    margin: 0;
}
.stat-row { display: flex; gap: 12px; }
.stat-pill {
    background: rgba(255,255,255,0.25);
    border: 1.5px solid rgba(255,255,255,0.5);
    border-radius: 50px;
    padding: 6px 16px;
    color: white;
    font-weight: 700;
    font-size: 0.85rem;
    backdrop-filter: blur(8px);
}

/* 手牌卡片 */
.card-wrap {
    border-radius: 14px;
    overflow: hidden;
    border: 3px solid #EEE;
    cursor: pointer;
    transition: transform 0.18s, box-shadow 0.18s;
    background: white;
    position: relative;
}
.card-wrap:hover { transform: translateY(-4px); box-shadow: 0 10px 24px rgba(0,0,0,0.12); }
.card-wrap.selected {
    border-color: #FF6B6B !important;
    box-shadow: 0 0 0 3px rgba(255,107,107,0.3);
    transform: translateY(-4px);
}
.card-wrap.special { border-color: #CC5DE8; }
.card-check {
    position: absolute; top: 6px; right: 6px;
    background: #FF6B6B; color: white;
    border-radius: 50%; width: 22px; height: 22px;
    display: flex; align-items: center; justify-content: center;
    font-size: 13px; font-weight: 900;
    box-shadow: 0 2px 6px rgba(255,107,107,0.5);
}
.star-badge {
    position: absolute; top: 6px; left: 6px;
    background: #CC5DE8; color: white;
    border-radius: 5px; padding: 1px 7px;
    font-size: 10px; font-weight: 900;
}
.card-label {
    text-align: center; padding: 6px 4px;
    font-weight: 700; font-size: 0.78rem; color: #333;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.card-label.special-label { color: #9333EA; }

/* 類別區塊 */
.cat-zone {
    border-radius: 18px;
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    margin-bottom: 12px;
    border: 2px solid rgba(0,0,0,0.05);
}
.cat-header-bar {
    padding: 12px 18px;
    font-weight: 800;
    font-size: 1rem;
    color: white;
    text-shadow: 1px 1px 0 rgba(0,0,0,0.15);
}
.cat-body { background: white; padding: 12px; min-height: 80px; }

/* 已放置的卡片 chip */
.placed-chip {
    display: inline-flex; align-items: center; gap: 6px;
    border-radius: 10px; padding: 4px 10px 4px 4px;
    border: 2px solid #EEE; background: #F8F8F8;
    font-size: 0.78rem; font-weight: 600;
    margin: 3px; max-width: 130px;
}
.placed-chip.correct { border-color: #22C55E; background: #F0FDF4; color: #15803D; }
.placed-chip.wrong   { border-color: #EF4444; background: #FFF5F5; color: #B91C1C; }
.placed-chip.locked  { border-color: #22C55E; background: #DCFCE7; color: #15803D; opacity: 0.8; }

/* 進度條 */
.progress-wrap {
    background: #EEE; border-radius: 50px; height: 8px; overflow: hidden; margin: 8px 0;
}
.progress-fill {
    height: 100%; border-radius: 50px;
    background: linear-gradient(90deg, #22C55E, #10B981);
    transition: width 0.5s ease;
}

/* Metric 美化 */
[data-testid="stMetric"] {
    background: white;
    border-radius: 14px;
    padding: 14px 18px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    border: 1.5px solid rgba(0,0,0,0.05);
}

/* 按鈕 */
.stButton > button {
    border-radius: 12px !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    transition: all 0.18s !important;
}
.stButton > button:hover { transform: translateY(-2px); }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# 頂部 Header
# ══════════════════════════════════════════════
rem_cards = get_remaining_cards()
prog_pct = round((len(st.session_state.scored_keys) / total_needed()) * 100)

st.markdown(f"""
<div class="game-header">
  <div class="game-title">🍽️ 食物分類遊戲</div>
  <div class="stat-row">
    <div class="stat-pill">⭐ 總分 {st.session_state.score}</div>
    <div class="stat-pill">🔢 提交 {st.session_state.submit_count} 次</div>
    <div class="stat-pill">💎 每題 {get_pts()} 分</div>
    <div class="stat-pill">🎴 手牌 {len(rem_cards)} 張</div>
  </div>
</div>
""", unsafe_allow_html=True)

# 進度條
st.markdown(f"""
<div class="progress-wrap">
  <div class="progress-fill" style="width:{prog_pct}%"></div>
</div>
<div style="font-size:0.75rem;color:#999;text-align:right;margin-bottom:8px;">完成進度 {prog_pct}% ({len(st.session_state.scored_keys)}/{total_needed()})</div>
""", unsafe_allow_html=True)

# 訊息列
if st.session_state.message:
    msg_type = st.session_state.message_type
    if msg_type == "success":
        st.success(st.session_state.message)
    elif msg_type == "warning":
        st.warning(st.session_state.message)
    else:
        st.info(st.session_state.message)

if st.session_state.locked:
    st.balloons()

st.divider()

# ══════════════════════════════════════════════
# 主體：左側手牌 + 右側分類區
# ══════════════════════════════════════════════
col_hand, col_board = st.columns([1, 2.2], gap="large")

# ─── 左側：手牌 ───
with col_hand:
    st.markdown("### 🎴 手牌區")
    st.caption("點擊卡片選取，再點右方「放入」按鈕")

    if not rem_cards:
        st.success("🎉 手牌已清空！請提交答案。")
    else:
        # 每行 3 張卡片
        COLS_PER_ROW = 3
        for row_start in range(0, len(rem_cards), COLS_PER_ROW):
            row_cards = rem_cards[row_start:row_start + COLS_PER_ROW]
            cols = st.columns(COLS_PER_ROW)
            for col_idx, name in enumerate(row_cards):
                with cols[col_idx]:
                    info = CARDS[name]
                    is_sel = name in st.session_state.selected
                    sel_class = "selected" if is_sel else ""
                    sp_class = "special" if info["special"] else ""
                    check_html = '<div class="card-check">✓</div>' if is_sel else ""
                    star_html = '<div class="star-badge">★</div>' if info["special"] else ""
                    label_class = "special-label" if info["special"] else ""

                    st.markdown(f'<div class="card-wrap {sel_class} {sp_class}">{check_html}{star_html}', unsafe_allow_html=True)
                    st.image(get_image_url(name), width='stretch')
                    st.markdown(f'<div class="card-label {label_class}">{name}</div></div>', unsafe_allow_html=True)

                    btn_label = f"✅ {name}" if is_sel else name
                    st.button(btn_label, key=f"hand_{name}",
                              on_click=toggle_select, args=(name,),
                              use_container_width=True,
                              type="primary" if is_sel else "secondary")

# ─── 右側：分類區 ───
with col_board:
    st.markdown("### 🧺 分類區")

    # 2x2 網格
    cat_row1 = CATEGORIES[:2]
    cat_row2 = CATEGORIES[2:]

    for cat_pair in [cat_row1, cat_row2]:
        pair_cols = st.columns(2, gap="medium")
        for ci, cat in enumerate(cat_pair):
            with pair_cols[ci]:
                hdr_color = CAT_HEADER_COLORS[cat]
                bg_color = CAT_COLORS[cat]

                st.markdown(f"""
                <div class="cat-zone">
                  <div class="cat-header-bar" style="background:{hdr_color};">{cat}</div>
                  <div class="cat-body">
                """, unsafe_allow_html=True)

                # 放入按鈕
                st.button(f"📥 放入【{cat}】", key=f"put_{cat}",
                          on_click=place_selected, args=(cat,),
                          use_container_width=True)

                # 已放置的卡片（圖片 + chip）
                placed = st.session_state.placed[cat]
                if not placed:
                    st.caption("尚無卡片")
                else:
                    # 以 4 欄顯示圖片
                    IMG_COLS = 4
                    for row_start in range(0, len(placed), IMG_COLS):
                        row = placed[row_start:row_start + IMG_COLS]
                        img_cols = st.columns(IMG_COLS)
                        for ci2, pname in enumerate(row):
                            with img_cols[ci2]:
                                key = f"{pname}|{cat}"
                                is_locked = key in st.session_state.scored_keys
                                res = st.session_state.result.get(key)

                                # 外框顏色
                                if is_locked:
                                    border = "3px solid #22C55E"
                                elif res == "wrong":
                                    border = "3px solid #EF4444"
                                elif res == "correct":
                                    border = "3px solid #22C55E"
                                else:
                                    border = "3px solid #DDD"

                                overlay = ""
                                if is_locked:
                                    overlay = "✅"
                                elif res == "wrong":
                                    overlay = "❌"

                                st.markdown(f'<div style="border-radius:10px;overflow:hidden;border:{border};position:relative;">', unsafe_allow_html=True)
                                st.image(get_image_url(pname), width='stretch')
                                st.markdown('</div>', unsafe_allow_html=True)

                                # 名稱 + 狀態
                                label = f"{overlay} {pname}" if overlay else pname
                                st.caption(label)

                                # 退回按鈕
                                if not is_locked and not st.session_state.locked:
                                    st.button("↩", key=f"rm_{pname}_{cat}",
                                              on_click=remove_card, args=(pname, cat),
                                              help=f"退回「{pname}」至手牌")

                st.markdown("</div></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# 底部控制按鈕
# ══════════════════════════════════════════════
st.divider()
b1, b2, b3 = st.columns([2, 1, 1])
with b1:
    st.button("✅ 提交答案", type="primary",
              disabled=st.session_state.locked,
              on_click=submit_answers,
              use_container_width=True)
with b2:
    if st.button("🔄 重新開始"):
        restart_game()
        st.rerun()
with b3:
    # 特殊卡說明
    with st.expander("★ 特殊卡說明"):
        for name, info in CARDS.items():
            if info["special"]:
                cats = " + ".join(info["valid"])
                st.caption(f"{name} → {cats}")
