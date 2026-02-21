import streamlit as st
import random
import os

# ══════════════════════════════════════════════
# 頁面基本設定
# ══════════════════════════════════════════════
st.set_page_config(page_title="食物分類遊戲", layout="wide", initial_sidebar_state="expanded")

# ─────────────── 遊戲資料 ───────────────
CATEGORIES = ["🥩 肉類", "🥦 蔬菜", "🍎 水果", "🧁 甜點"]

CARDS = {
    "牛排": {"color": "#FECACA", "valid": ["🥩 肉類"], "special": False},
    "雞腿": {"color": "#FED7AA", "valid": ["🥩 肉類"], "special": False},
    "培根": {"color": "#FCA5A5", "valid": ["🥩 肉類"], "special": False},
    "蝦子": {"color": "#FDBA74", "valid": ["🥩 肉類"], "special": False},
    "青花椰": {"color": "#86EFAC", "valid": ["🥦 蔬菜"], "special": False},
    "紅蘿蔔": {"color": "#FCA5A5", "valid": ["🥦 蔬菜"], "special": False},
    "玉米": {"color": "#FDE68A", "valid": ["🥦 蔬菜"], "special": False},
    "番茄": {"color": "#FCA5A5", "valid": ["🥦 蔬菜"], "special": False},
    "蘋果": {"color": "#FCA5A5", "valid": ["🍎 水果"], "special": False},
    "香蕉": {"color": "#FDE68A", "valid": ["🍎 水果"], "special": False},
    "草莓": {"color": "#FECDD3", "valid": ["🍎 水果"], "special": False},
    "西瓜": {"color": "#BBF7D0", "valid": ["🍎 水果"], "special": False},
    "蛋糕": {"color": "#E9D5FF", "valid": ["🧁 甜點"], "special": False},
    "冰淇淋": {"color": "#BFDBFE", "valid": ["🧁 甜點"], "special": False},
    "餅乾": {"color": "#FDE68A", "valid": ["🧁 甜點"], "special": False},
    "★草莓蛋糕": {"color": "#F5D0FE", "valid": ["🍎 水果", "🧁 甜點"], "special": True},
    "★玉米濃湯": {"color": "#D1FAE5", "valid": ["🥦 蔬菜", "🥩 肉類"], "special": True},
    "★水果冰淇淋": {"color": "#BAE6FD", "valid": ["🍎 水果", "🧁 甜點"], "special": True},
    "★番茄炒蛋": {"color": "#FED7AA", "valid": ["🥦 蔬菜", "🥩 肉類"], "special": True},
}

BASE_SCORE = 50

# ─────────────── 初始化 Session State (遊戲狀態管理) ───────────────
if "init" not in st.session_state:
    st.session_state.init = True
    st.session_state.score = 0
    st.session_state.submit_count = 0
    st.session_state.locked = False
    st.session_state.scored_keys = set()
    st.session_state.selected = set()
    st.session_state.result = {}
    
    # 紀錄每個類別放了哪些卡片
    st.session_state.placed = {cat: [] for cat in CATEGORIES}
    
    # 建立牌堆並洗牌
    deck = list(CARDS.keys())
    random.shuffle(deck)
    st.session_state.deck = deck
    
    st.session_state.message = "點選手牌選擇卡片，再點類別放入"

# ─────────────── 輔助與邏輯函數 ───────────────
def get_image_path(card_name):
    """尋找本地圖片，若無則回傳 None"""
    img_dir = "images"
    if not os.path.exists(img_dir):
        return None
    for ext in [".jpg", ".jpeg", ".png", ".webp"]:
        path = os.path.join(img_dir, f"{card_name}{ext}")
        if os.path.exists(path):
            return path
    return None

def get_remaining_cards():
    """計算還沒被放完的手牌"""
    out = []
    for c_name in st.session_state.deck:
        c_info = CARDS[c_name]
        # 計算這張牌目前被放在幾個類別中
        placed_count = sum([1 for cat in CATEGORIES if c_name in st.session_state.placed[cat]])
        
        if not c_info["special"] and placed_count == 0:
            out.append(c_name)
        elif c_info["special"] and placed_count < len(c_info["valid"]):
            out.append(c_name)
    return out

def get_multiplier():
    return 1.0 / (2 ** st.session_state.submit_count)

def get_pts_per_correct():
    return max(1, round(BASE_SCORE * get_multiplier()))

# ─────────────── 互動回呼函數 (Callbacks) ───────────────
def toggle_select(card_name):
    if st.session_state.locked: return
    if card_name in st.session_state.selected:
        st.session_state.selected.remove(card_name)
    else:
        st.session_state.selected.add(card_name)

def place_selected(target_cat):
    if st.session_state.locked: return
    if not st.session_state.selected:
        st.session_state.message = "⚠️ 請先點選左側手牌"
        return

    placed_n = 0
    skipped_n = 0
    
    for c_name in list(st.session_state.selected):
        c_info = CARDS[c_name]
        
        # 如果該卡片已經在這個類別，跳過
        if c_name in st.session_state.placed[target_cat]:
            skipped_n += 1
            continue
            
        # 如果不是特殊卡，且已經在其他類別，需要先從舊類別移除
        if not c_info["special"]:
            # 尋找舊類別
            old_cat = next((cat for cat in CATEGORIES if c_name in st.session_state.placed[cat]), None)
            if old_cat:
                old_key = f"{c_name}|{old_cat}"
                # 如果舊位置已經得分鎖定，不允許移動
                if old_key in st.session_state.scored_keys:
                    skipped_n += 1
                    continue
                # 允許移動，移除舊位置
                st.session_state.placed[old_cat].remove(c_name)
                st.session_state.result.pop(old_key, None)

        # 放入新類別
        st.session_state.placed[target_cat].append(c_name)
        st.session_state.result.pop(f"{c_name}|{target_cat}", None)
        st.session_state.selected.remove(c_name)
        placed_n += 1

    if placed_n:
        st.session_state.message = f"✅ 成功放入 {placed_n} 張卡片至【{target_cat}】"
    else:
        st.session_state.message = "⚠️ 所選卡片已在此類別或已鎖定"

def remove_card(card_name, from_cat):
    if st.session_state.locked: return
    key = f"{card_name}|{from_cat}"
    if key in st.session_state.scored_keys:
        return # 已得分不可退回
    
    st.session_state.placed[from_cat].remove(card_name)
    st.session_state.result.pop(key, None)
    if card_name in st.session_state.selected:
        st.session_state.selected.remove(card_name)

def submit_answers():
    if st.session_state.locked: return
    rem = get_remaining_cards()
    if rem:
        st.warning(f"還有 {len(rem)} 張在手牌，請全部放入後再提交！")
        return

    new_correct = 0
    wrong = 0
    pts_per = get_pts_per_correct()
    new_pts = 0

    for cat in CATEGORIES:
        for c_name in st.session_state.placed[cat]:
            c_info = CARDS[c_name]
            key = f"{c_name}|{cat}"
            
            if cat in c_info["valid"]:
                st.session_state.result[key] = "correct"
                if key not in st.session_state.scored_keys:
                    st.session_state.scored_keys.add(key)
                    new_pts += pts_per
                    new_correct += 1
            else:
                st.session_state.result[key] = "wrong"
                wrong += 1

    st.session_state.submit_count += 1
    st.session_state.score += new_pts

    # 判斷是否全對
    total_needed = sum(len(c["valid"]) for c in CARDS.values())
    if wrong == 0 and len(st.session_state.scored_keys) >= total_needed:
        st.session_state.locked = True
        st.session_state.message = f"🎉 完美全對！得分已鎖定！本次獲得 {new_pts} 分。"
        st.balloons()
    else:
        st.session_state.message = f"批改完成：新答對 {new_correct} 題，答錯 {wrong} 題。獲得 {new_pts} 分。"

def restart_game():
    for key in list(st.session_state.keys()):
        del st.session_state[key]


# ══════════════════════════════════════════════
# 繪製 UI 介面
# ══════════════════════════════════════════════

# ── 頂部資訊 ──
col_title, col_stat1, col_stat2, col_stat3 = st.columns([2, 1, 1, 1])
with col_title:
    st.title("🍔 食物分類遊戲")
with col_stat1:
    st.metric("總分", st.session_state.score)
with col_stat2:
    st.metric("提交次數", st.session_state.submit_count)
with col_stat3:
    pts = get_pts_per_correct()
    st.metric("目前每題得分", f"{pts} 分")

if st.session_state.get("message"):
    st.info(st.session_state.message)

st.divider()

# ── 遊戲主體 ──
col_hand, col_board = st.columns([1, 2.5])

# 左側：手牌區
with col_hand:
    rem_cards = get_remaining_cards()
    st.subheader(f"🎴 手牌 (剩 {len(rem_cards)} 張)")
    
    if rem_cards:
        # 手牌用 2 欄顯示
        h_cols = st.columns(2)
        for i, c_name in enumerate(rem_cards):
            with h_cols[i % 2]:
                is_sel = c_name in st.session_state.selected
                
                # 顯示圖片
                img_path = get_image_path(c_name)
                if img_path:
                    st.image(img_path, use_container_width=True)
                else:
                    st.markdown(f"<div style='background-color:{CARDS[c_name]['color']}; padding:20px; text-align:center; border-radius:10px;'>無圖片</div>", unsafe_allow_html=True)
                
                # 選擇按鈕
                btn_label = f"✅ {c_name}" if is_sel else c_name
                st.button(btn_label, key=f"hand_{c_name}_{i}", on_click=toggle_select, args=(c_name,), use_container_width=True)
    else:
        st.success("手牌已清空！")
        
    st.divider()
    st.markdown("💡 **操作方式**：\n1. 點擊上方手牌選擇卡片\n2. 點擊右方的「📥 放入」按鈕")

# 右側：分類區
with col_board:
    st.subheader("🧺 分類區")
    
    # 建立 2x2 的網格來放類別
    cat_cols = st.columns(2)
    for i, cat in enumerate(CATEGORIES):
        with cat_cols[i % 2]:
            st.markdown(f"### {cat}")
            # 放入按鈕
            st.button(f"📥 將選取的卡片放入【{cat}】", key=f"put_{cat}", on_click=place_selected, args=(cat,), use_container_width=True)
            
            # 顯示已經放入的卡片
            placed_cards = st.session_state.placed[cat]
            if not placed_cards:
                st.caption("尚無卡片")
            else:
                for c_name in placed_cards:
                    key = f"{c_name}|{cat}"
                    status = st.session_state.result.get(key)
                    
                    # 狀態標示
                    if key in st.session_state.scored_keys:
                        status_ui = "🟩 (已答對鎖定)"
                    elif status == "wrong":
                        status_ui = "🟥 (錯誤)"
                    else:
                        status_ui = "⬜ (尚未批改)"
                        
                    p_cols = st.columns([3, 1])
                    with p_cols[0]:
                        st.markdown(f"**{c_name}** {status_ui}")
                    with p_cols[1]:
                        if key not in st.session_state.scored_keys and not st.session_state.locked:
                            st.button("↩ 退回", key=f"rm_{c_name}_{cat}", on_click=remove_card, args=(c_name, cat))
            st.write("---")

# ── 底部控制按鈕 ──
st.divider()
b_col1, b_col2, b_col3, b_col4 = st.columns(4)

with b_col1:
    if st.button("✅ 提交答案", type="primary", disabled=st.session_state.locked, use_container_width=True):
        submit_answers()
with b_col2:
    if st.button("🔄 重新開始", use_container_width=True):
        restart_game()
        st.rerun()
