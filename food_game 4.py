import streamlit as st
import random
from urllib.parse import quote

# ══════════════════════════════════════════════
# 頁面設定
# ══════════════════════════════════════════════
st.set_page_config(
    page_title="食物分類遊戲 🍽️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────── GitHub 圖片 ───────────────
GITHUB_BASE = "https://raw.githubusercontent.com/HLH2000/Food_Game/main/%E9%A3%9F%E7%89%A9%E5%9C%96/"

def get_image_url(card_name: str) -> str:
    base = card_name.lstrip("★").strip()
    return GITHUB_BASE + quote(base, safe="") + ".jpg"

# ─────────────── 遊戲資料 ───────────────
CATEGORIES = ["🥩 肉類/海鮮", "🥦 蔬菜", "🍎 水果", "🧁 甜點/飲料"]

CAT_STYLE = {
    "🥩 肉類/海鮮": {"hdr": "#EF4444", "bg": "#FFF5F5", "border": "#FECACA"},
    "🥦 蔬菜":      {"hdr": "#16A34A", "bg": "#F0FDF4", "border": "#BBF7D0"},
    "🍎 水果":      {"hdr": "#EA580C", "bg": "#FFF7ED", "border": "#FED7AA"},
    "🧁 甜點/飲料": {"hdr": "#9333EA", "bg": "#FAF5FF", "border": "#E9D5FF"},
}

CARDS = {
    "培根":       {"valid": ["🥩 肉類/海鮮"], "special": False},
    "牛排":       {"valid": ["🥩 肉類/海鮮"], "special": False},
    "炸雞":       {"valid": ["🥩 肉類/海鮮"], "special": False},
    "烤雞腿":     {"valid": ["🥩 肉類/海鮮"], "special": False},
    "熟蝦":       {"valid": ["🥩 肉類/海鮮"], "special": False},
    "鮭魚":       {"valid": ["🥩 肉類/海鮮"], "special": False},
    "鮪魚":       {"valid": ["🥩 肉類/海鮮"], "special": False},
    "龍蝦":       {"valid": ["🥩 肉類/海鮮"], "special": False},
    "螃蟹":       {"valid": ["🥩 肉類/海鮮"], "special": False},
    "扇貝":       {"valid": ["🥩 肉類/海鮮"], "special": False},
    "臘肉":       {"valid": ["🥩 肉類/海鮮"], "special": False},
    "雞排":       {"valid": ["🥩 肉類/海鮮"], "special": False},
    "南瓜":       {"valid": ["🥦 蔬菜"], "special": False},
    "大白菜":     {"valid": ["🥦 蔬菜"], "special": False},
    "彩椒":       {"valid": ["🥦 蔬菜"], "special": False},
    "玉米":       {"valid": ["🥦 蔬菜"], "special": False},
    "白蘿蔔":     {"valid": ["🥦 蔬菜"], "special": False},
    "紫甘藍":     {"valid": ["🥦 蔬菜"], "special": False},
    "茄子":       {"valid": ["🥦 蔬菜"], "special": False},
    "蘆筍":       {"valid": ["🥦 蔬菜"], "special": False},
    "青花菜":     {"valid": ["🥦 蔬菜"], "special": False},
    "杏鮑菇":     {"valid": ["🥦 蔬菜"], "special": False},
    "蕈菇":       {"valid": ["🥦 蔬菜"], "special": False},
    "奇異果":     {"valid": ["🍎 水果"], "special": False},
    "木瓜":       {"valid": ["🍎 水果"], "special": False},
    "橘子":       {"valid": ["🍎 水果"], "special": False},
    "水蜜桃":     {"valid": ["🍎 水果"], "special": False},
    "西瓜":       {"valid": ["🍎 水果"], "special": False},
    "藍莓":       {"valid": ["🍎 水果"], "special": False},
    "千層派":     {"valid": ["🧁 甜點/飲料"], "special": False},
    "巧克力":     {"valid": ["🧁 甜點/飲料"], "special": False},
    "巧克力豆餅": {"valid": ["🧁 甜點/飲料"], "special": False},
    "甜甜圈":     {"valid": ["🧁 甜點/飲料"], "special": False},
    "湯圓":       {"valid": ["🧁 甜點/飲料"], "special": False},
    "糖果":       {"valid": ["🧁 甜點/飲料"], "special": False},
    "糖葫蘆":     {"valid": ["🧁 甜點/飲料"], "special": False},
    "鯛魚燒":     {"valid": ["🧁 甜點/飲料"], "special": False},
    "優格":       {"valid": ["🧁 甜點/飲料"], "special": False},
    "優酪乳":     {"valid": ["🧁 甜點/飲料"], "special": False},
    "珍珠奶茶":   {"valid": ["🧁 甜點/飲料"], "special": False},
    "爆米花":     {"valid": ["🧁 甜點/飲料"], "special": False},
    "★藍莓起司蛋糕": {"valid": ["🍎 水果", "🧁 甜點/飲料"], "special": True},
    "★披薩":         {"valid": ["🥩 肉類/海鮮", "🥦 蔬菜"], "special": True},
    "★涼拌豆腐":     {"valid": ["🥦 蔬菜", "🧁 甜點/飲料"], "special": True},
    "★滷肉飯":       {"valid": ["🥩 肉類/海鮮", "🥦 蔬菜"], "special": True},
}

BASE_SCORE = 50

# ─────────────── 初始化 ───────────────
def init_game():
    st.session_state.game_init            = True
    st.session_state.score                = 0
    st.session_state.submit_count         = 0
    st.session_state.locked               = False
    st.session_state.scored_keys          = set()
    st.session_state.selected             = set()
    st.session_state.result               = {}
    st.session_state.placed               = {cat: [] for cat in CATEGORIES}
    st.session_state.message              = ""
    st.session_state.message_type         = "info"
    # None=尚未批改, True=可用, False=已用過
    st.session_state.return_wrong_avail   = None
    deck = list(CARDS.keys())
    random.shuffle(deck)
    st.session_state.deck = deck

if "game_init" not in st.session_state:
    init_game()

# ─────────────── 輔助 ───────────────
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

def get_pts():
    return max(1, round(BASE_SCORE / (2 ** st.session_state.submit_count)))

def total_needed():
    return sum(len(c["valid"]) for c in CARDS.values())

def get_wrong_pairs():
    pairs = []
    for cat in CATEGORIES:
        for name in st.session_state.placed[cat]:
            key = f"{name}|{cat}"
            if st.session_state.result.get(key) == "wrong":
                pairs.append((name, cat))
    return pairs

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
    placed_n = 0
    for name in list(st.session_state.selected):
        info = CARDS[name]
        if name in st.session_state.placed[target_cat]:
            continue
        if not info["special"]:
            old_cat = next((c for c in CATEGORIES if name in st.session_state.placed[c]), None)
            if old_cat:
                old_key = f"{name}|{old_cat}"
                if old_key in st.session_state.scored_keys:
                    continue
                st.session_state.placed[old_cat].remove(name)
                st.session_state.result.pop(old_key, None)
        st.session_state.placed[target_cat].append(name)
        st.session_state.result.pop(f"{name}|{target_cat}", None)
        st.session_state.selected.discard(name)
        placed_n += 1
    if placed_n:
        st.session_state.message = f"✅ 成功放入 {placed_n} 張至【{target_cat}】"
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
        st.session_state.return_wrong_avail = None
    else:
        wrong_pairs = get_wrong_pairs()
        wrong_names = "、".join([n for n, _ in wrong_pairs[:6]])
        if len(wrong_pairs) > 6:
            wrong_names += "…"
        st.session_state.message = (
            f"批改完成：✅ 答對 {new_correct} 題　❌ 答錯 {wrong} 題　＋{new_pts} 分"
            + (f"\n錯誤：{wrong_names}" if wrong_pairs else "")
        )
        st.session_state.message_type = "info" if wrong == 0 else "warning"
        st.session_state.return_wrong_avail = True if wrong > 0 else None

def return_all_wrong():
    pairs = get_wrong_pairs()
    count = 0
    for name, cat in pairs:
        key = f"{name}|{cat}"
        if key not in st.session_state.scored_keys:
            st.session_state.placed[cat].remove(name)
            st.session_state.result.pop(key, None)
            count += 1
    st.session_state.return_wrong_avail = False
    st.session_state.message = f"↩ 已退回 {count} 張錯誤卡牌至手牌，請重新整理後再提交！"
    st.session_state.message_type = "info"

def restart_game():
    for k in list(st.session_state.keys()):
        del st.session_state[k]

# ══════════════════════════════════════════════
# CSS
# ══════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700;900&display=swap');
* { font-family: 'Noto Sans TC', sans-serif !important; }

[data-testid="stAppViewContainer"] {
    background: #F8F7FF;
    background-image:
        radial-gradient(ellipse at 0% 0%, rgba(239,68,68,0.07) 0%, transparent 50%),
        radial-gradient(ellipse at 100% 100%, rgba(147,51,234,0.07) 0%, transparent 50%);
}
[data-testid="stHeader"] { background: transparent !important; }
.block-container { padding-top: 0.5rem !important; padding-bottom: 2rem !important; }

/* ── Header ── */
.game-header {
    background: linear-gradient(120deg, #FF6B6B 0%, #FF922B 45%, #CC5DE8 100%);
    border-radius: 22px;
    padding: 18px 28px;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 8px 36px rgba(255,107,107,0.25);
    flex-wrap: wrap;
    gap: 10px;
}
.game-title {
    font-size: 1.8rem;
    font-weight: 900;
    color: white;
    text-shadow: 2px 3px 0 rgba(0,0,0,0.12);
    letter-spacing: -0.5px;
}
.stat-row { display: flex; gap: 8px; flex-wrap: wrap; }
.stat-pill {
    background: rgba(255,255,255,0.22);
    border: 1.5px solid rgba(255,255,255,0.42);
    border-radius: 50px;
    padding: 5px 14px;
    color: white;
    font-weight: 700;
    font-size: 0.8rem;
    backdrop-filter: blur(10px);
    white-space: nowrap;
}
.stat-pill b { font-size: 0.95rem; }

/* ── Progress ── */
.prog-wrap {
    background: #E5E7EB;
    border-radius: 50px;
    height: 10px;
    overflow: hidden;
    margin: 8px 0 2px;
    box-shadow: inset 0 1px 3px rgba(0,0,0,0.08);
}
.prog-fill {
    height: 100%;
    border-radius: 50px;
    background: linear-gradient(90deg, #22C55E, #10B981, #06B6D4);
    transition: width 0.6s cubic-bezier(.4,0,.2,1);
    box-shadow: 0 1px 4px rgba(34,197,94,0.35);
}
.prog-label { font-size: 0.72rem; color: #9CA3AF; text-align: right; margin-bottom: 8px; }

/* ── Section titles ── */
.panel-title {
    font-size: 1rem;
    font-weight: 800;
    color: #374151;
    padding-bottom: 10px;
    border-bottom: 2px solid #F3F4F6;
    margin-bottom: 10px;
}

/* ── Hand cards ── */
.card-outer {
    position: relative;
    cursor: pointer;
    transition: transform 0.18s ease;
}
.card-outer:hover { transform: translateY(-4px); }
.card-inner {
    border-radius: 12px;
    overflow: hidden;
    border: 3px solid #E5E7EB;
    background: white;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    transition: border-color 0.15s, box-shadow 0.15s;
}
.card-inner.sel {
    border-color: #FF6B6B;
    box-shadow: 0 0 0 3px rgba(255,107,107,0.22), 0 6px 18px rgba(255,107,107,0.18);
}
.card-inner.sp { border-color: #A855F7; }
.badge-sel {
    position: absolute; top: -8px; right: -8px; z-index: 10;
    background: #FF6B6B; color: white;
    border-radius: 50%; width: 26px; height: 26px;
    display: flex; align-items: center; justify-content: center;
    font-size: 13px; font-weight: 900;
    box-shadow: 0 2px 8px rgba(255,107,107,0.5);
    border: 2px solid white;
}
.badge-star {
    position: absolute; top: 6px; left: 6px; z-index: 10;
    background: linear-gradient(135deg, #A855F7, #7C3AED);
    color: white; border-radius: 6px;
    padding: 2px 6px; font-size: 9px; font-weight: 900;
    box-shadow: 0 2px 5px rgba(124,58,237,0.4);
}
.card-name {
    text-align: center;
    padding: 5px 3px 6px;
    font-size: 0.72rem;
    font-weight: 700;
    color: #374151;
    background: white;
    border-top: 1px solid #F3F4F6;
}
.card-name.sp-name { color: #7C3AED; }

/* ── Category zones ── */
.cat-zone {
    border-radius: 18px;
    overflow: hidden;
    box-shadow: 0 4px 18px rgba(0,0,0,0.07);
    margin-bottom: 14px;
    border: 2px solid transparent;
}
.cat-hdr {
    padding: 12px 16px;
    font-weight: 800;
    font-size: 0.95rem;
    color: white;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.cat-cnt {
    background: rgba(255,255,255,0.28);
    border-radius: 50px;
    padding: 2px 10px;
    font-size: 0.76rem;
    font-weight: 700;
}
.cat-body { background: white; padding: 10px; min-height: 88px; }
.cat-empty { color: #D1D5DB; font-size: 0.8rem; padding: 18px 0 8px; text-align: center; }

/* ── Placed cards ── */
.pcard {
    border-radius: 10px;
    overflow: hidden;
    border: 3px solid #E5E7EB;
    background: white;
    position: relative;
}
.pcard.pc { border-color: #22C55E; }
.pcard.pw { border-color: #EF4444; }
.pcard-ov {
    position: absolute; top: 4px; right: 4px;
    width: 20px; height: 20px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 10px; font-weight: 900;
    border: 2px solid white;
}
.pcard-ov.c { background: #22C55E; color: white; }
.pcard-ov.w { background: #EF4444; color: white; }
.pcard-lbl {
    font-size: 0.66rem;
    font-weight: 700;
    text-align: center;
    padding: 3px 2px;
    color: #374151;
    background: white;
    border-top: 1px solid #F3F4F6;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.pcard-lbl.lc { color: #15803D; background: #F0FDF4; }
.pcard-lbl.lw { color: #B91C1C; background: #FFF5F5; }

/* ── One-click return banner ── */
.return-banner {
    background: linear-gradient(135deg, #FFF5F5 0%, #FFFBFB 100%);
    border: 2px solid #FCA5A5;
    border-radius: 18px;
    padding: 16px 20px;
    margin: 4px 0 14px;
    display: flex;
    align-items: center;
    gap: 16px;
    box-shadow: 0 4px 16px rgba(239,68,68,0.1);
    animation: pulseBorder 2.2s ease-in-out infinite;
}
@keyframes pulseBorder {
    0%, 100% { border-color: #FCA5A5; }
    50%       { border-color: #EF4444; box-shadow: 0 4px 20px rgba(239,68,68,0.18); }
}
.return-icon { font-size: 2.2rem; line-height: 1; }
.return-info { flex: 1; }
.return-count { font-size: 1.25rem; font-weight: 900; color: #EF4444; line-height: 1.2; }
.return-desc  { font-size: 0.8rem; color: #6B7280; margin-top: 2px; line-height: 1.5; }
.return-once  { font-size: 0.72rem; color: #EF4444; font-weight: 700; margin-top: 3px; }

/* ── Buttons ── */
.stButton > button {
    border-radius: 12px !important;
    font-weight: 800 !important;
    font-size: 0.88rem !important;
    transition: all 0.18s ease !important;
}
.stButton > button:hover:not([disabled]) {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 20px rgba(0,0,0,0.14) !important;
}
.stButton > button[disabled] { opacity: 0.42 !important; }
hr { border-color: #F3F4F6 !important; margin: 10px 0 !important; }
div[data-testid="stAlert"] { border-radius: 14px !important; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# Header & Progress
# ══════════════════════════════════════════════
rem_cards   = get_remaining_cards()
prog_pct    = round((len(st.session_state.scored_keys) / total_needed()) * 100)
wrong_pairs = get_wrong_pairs()

st.markdown(f"""
<div class="game-header">
  <div class="game-title">🍽️ 食物分類遊戲</div>
  <div class="stat-row">
    <div class="stat-pill">⭐ 總分 <b>{st.session_state.score}</b></div>
    <div class="stat-pill">🔢 提交 <b>{st.session_state.submit_count}</b> 次</div>
    <div class="stat-pill">💎 每題 <b>{get_pts()}</b> 分</div>
    <div class="stat-pill">🎴 手牌 <b>{len(rem_cards)}</b> 張</div>
  </div>
</div>
<div class="prog-wrap"><div class="prog-fill" style="width:{prog_pct}%"></div></div>
<div class="prog-label">完成進度 {prog_pct}%　({len(st.session_state.scored_keys)}/{total_needed()} 題已鎖定)</div>
""", unsafe_allow_html=True)

# 訊息（自訂樣式，避免 Streamlit 原生黃底）
if st.session_state.message:
    t = st.session_state.message_type
    _msg_styles = {
        "success": ("🎉", "#F0FDF4", "#16A34A", "#BBF7D0", "#15803D"),
        "warning": ("📋", "#F8F9FA", "#374151", "#E5E7EB", "#374151"),
        "info":    ("📋", "#F8F9FA", "#374151", "#E5E7EB", "#374151"),
    }
    icon, bg, accent, border, text = _msg_styles.get(t, _msg_styles["info"])
    # 把換行轉成 <br>
    msg_html = st.session_state.message.replace("\n", "<br>")
    st.markdown(f"""
    <div style="
        background:{bg};
        border:1.5px solid {border};
        border-left:4px solid {accent};
        border-radius:14px;
        padding:12px 18px;
        margin:6px 0 4px;
        font-size:0.88rem;
        font-weight:500;
        color:{text};
        line-height:1.6;
        display:flex;
        align-items:flex-start;
        gap:10px;
    ">
      <span style="font-size:1.1rem;line-height:1.5;">{icon}</span>
      <span>{msg_html}</span>
    </div>
    """, unsafe_allow_html=True)

if st.session_state.locked:
    st.balloons()

# ══════════════════════════════════════════════
# 一鍵退回 Banner（批改後有錯 & 尚未使用）
# ══════════════════════════════════════════════
if st.session_state.return_wrong_avail is True and wrong_pairs:
    n_wrong = len(wrong_pairs)
    col_info, col_btn = st.columns([3.5, 1])
    with col_info:
        st.markdown(f"""
        <div class="return-banner">
          <div class="return-icon">↩️</div>
          <div class="return-info">
            <div class="return-count">❌ 發現 {n_wrong} 張錯誤卡牌！</div>
            <div class="return-desc">批改後出現錯誤，可一鍵將所有錯誤卡牌退回手牌，重新放置後再提交。</div>
            <div class="return-once">⚠️ 每次批改後僅能使用一次，使用後不可復原</div>
          </div>
        </div>
        """, unsafe_allow_html=True)
    with col_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        st.button(
            f"↩ 一鍵退回 {n_wrong} 張",
            key="return_wrong_btn",
            on_click=return_all_wrong,
            use_container_width=True,
            type="primary",
        )

st.divider()

# ══════════════════════════════════════════════
# 主體
# ══════════════════════════════════════════════
col_hand, col_board = st.columns([1, 2.5], gap="large")

# ─── 左：手牌 ───
with col_hand:
    st.markdown(f'<div class="panel-title">🎴 手牌區　<span style="color:#9CA3AF;font-weight:500;font-size:0.82rem;">剩 {len(rem_cards)} 張</span></div>', unsafe_allow_html=True)
    if not rem_cards:
        st.success("🎉 手牌已清空！請點「提交答案」。", icon="✅")
    else:
        st.caption("點卡片選取（可多選）→ 點右方 📥 放入")
        COLS = 3
        for rs in range(0, len(rem_cards), COLS):
            row = rem_cards[rs:rs + COLS]
            cols = st.columns(COLS, gap="small")
            for ci, name in enumerate(row):
                with cols[ci]:
                    info   = CARDS[name]
                    is_sel = name in st.session_state.selected
                    sc     = "sel" if is_sel else ""
                    spc    = "sp" if info["special"] else ""
                    nc     = "sp-name" if info["special"] else ""
                    chk    = '<div class="badge-sel">✓</div>' if is_sel else ""
                    star   = '<div class="badge-star">★特殊</div>' if info["special"] else ""

                    st.markdown(f'<div class="card-outer">{chk}{star}<div class="card-inner {sc} {spc}">', unsafe_allow_html=True)
                    st.image(get_image_url(name), width="stretch")
                    st.markdown(f'<div class="card-name {nc}">{name}</div></div></div>', unsafe_allow_html=True)
                    st.button(
                        "✅ 已選" if is_sel else "選取",
                        key=f"hand_{name}",
                        on_click=toggle_select, args=(name,),
                        use_container_width=True,
                        type="primary" if is_sel else "secondary",
                    )

# ─── 右：分類區 ───
with col_board:
    st.markdown('<div class="panel-title">🧺 分類區</div>', unsafe_allow_html=True)

    for row_cats in [CATEGORIES[:2], CATEGORIES[2:]]:
        pair_cols = st.columns(2, gap="medium")
        for ci, cat in enumerate(row_cats):
            with pair_cols[ci]:
                s      = CAT_STYLE[cat]
                placed = st.session_state.placed[cat]
                cnt    = len(placed)

                st.markdown(f"""
                <div class="cat-zone" style="border-color:{s['border']};">
                  <div class="cat-hdr" style="background:{s['hdr']};">
                    <span>{cat}</span>
                    <span class="cat-cnt">{cnt} 張</span>
                  </div>
                  <div class="cat-body" style="background:{s['bg']};">
                """, unsafe_allow_html=True)

                # 放入按鈕
                st.button(
                    f"📥 放入此類別",
                    key=f"put_{cat}",
                    on_click=place_selected, args=(cat,),
                    use_container_width=True,
                )

                # 已放置卡片
                if not placed:
                    st.markdown('<div class="cat-empty">尚無卡片</div>', unsafe_allow_html=True)
                else:
                    IMG_COLS = 4
                    for rs2 in range(0, len(placed), IMG_COLS):
                        row = placed[rs2:rs2 + IMG_COLS]
                        icols = st.columns(IMG_COLS, gap="small")
                        for ci2, pname in enumerate(row):
                            with icols[ci2]:
                                key       = f"{pname}|{cat}"
                                is_locked = key in st.session_state.scored_keys
                                res       = st.session_state.result.get(key)

                                if is_locked or res == "correct":
                                    pw, ov, lbl = "pc", "c", "✓"
                                    lc = "lc"
                                elif res == "wrong":
                                    pw, ov, lbl = "pw", "w", "✗"
                                    lc = "lw"
                                else:
                                    pw, ov, lbl, lc = "", "", "", ""

                                ov_html = f'<div class="pcard-ov {ov}">{lbl}</div>' if ov else ""
                                short   = pname.lstrip("★")

                                st.markdown(f'<div class="pcard {pw}">{ov_html}', unsafe_allow_html=True)
                                st.image(get_image_url(pname), width="stretch")
                                st.markdown(f'<div class="pcard-lbl {lc}">{short}</div></div>', unsafe_allow_html=True)

                                # 個別退回（未鎖定、非錯誤、未鎖整場）
                                if not is_locked and not st.session_state.locked and res != "wrong":
                                    st.button(
                                        "↩",
                                        key=f"rm_{pname}_{cat}",
                                        on_click=remove_card, args=(pname, cat),
                                        help=f"退回「{short}」",
                                    )

                st.markdown("</div></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# 底部控制
# ══════════════════════════════════════════════
st.divider()
b1, b2, b3 = st.columns([2.5, 1, 1])
with b1:
    st.button(
        "✅ 提交答案",
        type="primary",
        disabled=st.session_state.locked,
        on_click=submit_answers,
        use_container_width=True,
    )
with b2:
    if st.button("🔄 重新開始", use_container_width=True):
        restart_game()
        st.rerun()
with b3:
    with st.expander("★ 特殊卡說明"):
        for name, info in CARDS.items():
            if info["special"]:
                cats = " ＋ ".join(info["valid"])
                st.caption(f"**{name}**\n→ {cats}")
