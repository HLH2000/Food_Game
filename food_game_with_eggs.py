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

# ─────────────── GitHub 圖片（預先建好所有 URL，不重複計算）───────────────
GITHUB_BASE = "https://raw.githubusercontent.com/HLH2000/Food_Game/main/%E9%A3%9F%E7%89%A9%E5%9C%96/"

# 彩蛋圖片 URL（egg 資料夾，第2、3、4次提交）
EGG_BASE = "https://raw.githubusercontent.com/HLH2000/Food_Game/main/egg/"
EGG_URLS = {
    2: EGG_BASE + quote("彩蛋1", safe="") + ".jpg",
    3: EGG_BASE + quote("彩蛋3", safe="") + ".jpg",
    4: EGG_BASE + quote("彩蛋2", safe="") + ".jpg",
}

# 一次性建立全部 URL map，之後直接查表，不再呼叫函式
_IMG_URLS: dict[str, str] = {}

def _build_urls():
    for name in [
        "培根","牛排","炸雞","烤雞腿","熟蝦","鮭魚","鮪魚","龍蝦","螃蟹","扇貝","臘肉","雞排",
        "南瓜","大白菜","彩椒","玉米","白蘿蔔","紫甘藍","茄子","蘆筍","青花菜","杏鮑菇","蕈菇",
        "奇異果","木瓜","橘子","水蜜桃","西瓜","藍莓",
        "切片起司","巧克力","巧克力豆餅","甜甜圈","湯圓","糖果","糖葫蘆","鯛魚燒","優格","優酪乳","珍珠奶茶","爆米花",
        "藍莓起司蛋糕","披薩",
    ]:
        _IMG_URLS[name] = GITHUB_BASE + quote(name, safe="") + ".jpg"

_build_urls()

def img_url(card_name: str) -> str:
    """查表，O(1)"""
    base = card_name.lstrip("★").strip()
    return _IMG_URLS.get(base, GITHUB_BASE + quote(base, safe="") + ".jpg")

# ─────────────── 遊戲資料 ───────────────
CATEGORIES = ["🥩 肉類/海鮮", "🥦 蔬菜/五穀澱粉", "🍎 水果", "🧁 甜點/飲料"]

CAT_STYLE = {
    "🥩 肉類/海鮮": {"hdr": "#B91C1C", "border": "#B91C1C"},
    "🥦 蔬菜/五穀澱粉":      {"hdr": "#15803D", "border": "#15803D"},
    "🍎 水果":      {"hdr": "#C2410C", "border": "#C2410C"},
    "🧁 甜點/飲料": {"hdr": "#6D28D9", "border": "#6D28D9"},
}

CARDS: dict[str, dict] = {
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
    "南瓜":       {"valid": ["🥦 蔬菜/五穀澱粉"], "special": False},
    "大白菜":     {"valid": ["🥦 蔬菜/五穀澱粉"], "special": False},
    "彩椒":       {"valid": ["🥦 蔬菜/五穀澱粉"], "special": False},
    "玉米":       {"valid": ["🥦 蔬菜/五穀澱粉"], "special": False},
    "白蘿蔔":     {"valid": ["🥦 蔬菜/五穀澱粉"], "special": False},
    "紫甘藍":     {"valid": ["🥦 蔬菜/五穀澱粉"], "special": False},
    "茄子":       {"valid": ["🥦 蔬菜/五穀澱粉"], "special": False},
    "蘆筍":       {"valid": ["🥦 蔬菜/五穀澱粉"], "special": False},
    "青花菜":     {"valid": ["🥦 蔬菜/五穀澱粉"], "special": False},
    "杏鮑菇":     {"valid": ["🥦 蔬菜/五穀澱粉"], "special": False},
    "蕈菇":       {"valid": ["🥦 蔬菜/五穀澱粉"], "special": False},
    "奇異果":     {"valid": ["🍎 水果"], "special": False},
    "木瓜":       {"valid": ["🍎 水果"], "special": False},
    "橘子":       {"valid": ["🍎 水果"], "special": False},
    "水蜜桃":     {"valid": ["🍎 水果"], "special": False},
    "西瓜":       {"valid": ["🍎 水果"], "special": False},
    "藍莓":       {"valid": ["🍎 水果"], "special": False},
    "切片起司":     {"valid": ["🧁 甜點/飲料"], "special": False},
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
    "★披薩":         {"valid": ["🥦 蔬菜/五穀澱粉", "🧁 甜點/飲料"], "special": True},
}

BASE_SCORE = 50
TOTAL_NEEDED: int = sum(len(c["valid"]) for c in CARDS.values())  # 常數，只算一次

# ─────────────── 初始化 ───────────────
def init_game():
    st.session_state.update({
        "game_init":           True,
        "score":               0,
        "submit_count":        0,
        "locked":              False,
        "scored_keys":         set(),
        "selected":            set(),
        "result":              {},
        "placed":              {cat: [] for cat in CATEGORIES},
        "message":             "",
        "message_type":        "info",
        "return_wrong_avail":  None,  # None=未批改, True=可用, False=已用
        "show_egg":            False,  # 是否顯示彩蛋彈窗
        "egg_submit_count":    0,      # 觸發彩蛋時的提交次數
    })
    deck = list(CARDS.keys())
    random.shuffle(deck)
    st.session_state.deck = deck

if "game_init" not in st.session_state:
    init_game()

# ─────────────── 輔助（快取結果避免重複計算）───────────────
def get_remaining_cards() -> list[str]:
    placed = st.session_state.placed
    out = []
    for name in st.session_state.deck:
        info = CARDS[name]
        if info["special"]:
            cnt = sum(1 for cat in CATEGORIES if name in placed[cat])
            if cnt < len(info["valid"]):
                out.append(name)
        else:
            if not any(name in placed[cat] for cat in CATEGORIES):
                out.append(name)
    return out

def get_pts() -> int:
    return max(1, round(BASE_SCORE / (2 ** st.session_state.submit_count)))

def get_wrong_pairs() -> list[tuple[str, str]]:
    res = st.session_state.result
    return [
        (name, cat)
        for cat in CATEGORIES
        for name in st.session_state.placed[cat]
        if res.get(f"{name}|{cat}") == "wrong"
    ]

# ─────────────── Callbacks（純狀態操作，不觸碰 UI）───────────────
def toggle_select(name: str):
    if st.session_state.locked:
        return
    sel = st.session_state.selected
    sel.discard(name) if name in sel else sel.add(name)

def place_selected(target_cat: str):
    if st.session_state.locked:
        return
    sel = st.session_state.selected
    if not sel:
        st.session_state.message = "⚠️ 請先點選手牌卡片！"
        st.session_state.message_type = "warning"
        return
    placed = st.session_state.placed
    scored = st.session_state.scored_keys
    result = st.session_state.result
    placed_n = 0
    for name in list(sel):
        info = CARDS[name]
        if name in placed[target_cat]:
            continue
        if not info["special"]:
            old_cat = next((c for c in CATEGORIES if name in placed[c]), None)
            if old_cat:
                old_key = f"{name}|{old_cat}"
                if old_key in scored:
                    continue
                placed[old_cat].remove(name)
                result.pop(old_key, None)
        placed[target_cat].append(name)
        result.pop(f"{name}|{target_cat}", None)
        sel.discard(name)
        placed_n += 1
    if placed_n:
        st.session_state.message = f"✅ 成功放入 {placed_n} 張至【{target_cat}】"
        st.session_state.message_type = "success"
    else:
        st.session_state.message = "⚠️ 所選卡片已在此類別或已鎖定"
        st.session_state.message_type = "warning"

def remove_card(name: str, from_cat: str):
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
    placed  = st.session_state.placed
    scored  = st.session_state.scored_keys
    result  = st.session_state.result
    pts     = get_pts()
    new_correct = wrong = new_pts = 0
    for cat in CATEGORIES:
        for name in placed[cat]:
            key = f"{name}|{cat}"
            if cat in CARDS[name]["valid"]:
                result[key] = "correct"
                if key not in scored:
                    scored.add(key)
                    new_pts += pts
                    new_correct += 1
            else:
                result[key] = "wrong"
                wrong += 1
    st.session_state.submit_count += 1
    st.session_state.score += new_pts

    # ── 彩蛋觸發：第2、3、4次提交 ──
    if st.session_state.submit_count in EGG_URLS:
        st.session_state.show_egg = True
        st.session_state.egg_submit_count = st.session_state.submit_count

    if wrong == 0 and len(scored) >= TOTAL_NEEDED:
        st.session_state.locked = True
        st.session_state.message = f"🎉 完美全對！本次獲得 {new_pts} 分，總分 {st.session_state.score} 分！"
        st.session_state.message_type = "success"
        st.session_state.return_wrong_avail = None
    else:
        wp = get_wrong_pairs()
        wrong_names = "、".join(n for n, _ in wp[:6]) + ("…" if len(wp) > 6 else "")
        st.session_state.message = (
            f"批改完成：✅ 答對 {new_correct} 題　❌ 答錯 {wrong} 題　＋{new_pts} 分"
            + (f"\n錯誤：{wrong_names}" if wp else "")
        )
        st.session_state.message_type = "info" if wrong == 0 else "warning"
        st.session_state.return_wrong_avail = True if wrong > 0 else None

def return_all_wrong():
    pairs = get_wrong_pairs()
    result = st.session_state.result
    scored = st.session_state.scored_keys
    count = 0
    for name, cat in pairs:
        key = f"{name}|{cat}"
        if key not in scored:
            st.session_state.placed[cat].remove(name)
            result.pop(key, None)
            count += 1
    st.session_state.return_wrong_avail = False
    st.session_state.message = f"↩ 已退回 {count} 張錯誤卡牌至手牌，請重新放置後再提交！"
    st.session_state.message_type = "info"

def restart_game():
    for k in list(st.session_state.keys()):
        del st.session_state[k]

# ── 彩蛋 Dialog ──
@st.dialog("🎉 彩蛋出現！")
def show_egg_dialog(egg_url: str, submit_count: int):
    egg_labels = {2: "第一顆彩蛋", 3: "第二顆彩蛋", 4: "第三顆彩蛋"}
    label = egg_labels.get(submit_count, "彩蛋")
    st.markdown(
        f"""
        <div style="text-align:center;">
            <div style="font-size:1.1rem;font-weight:800;color:#7C3AED;margin-bottom:12px;">
                ✨ 恭喜發現{label}！✨
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.image(egg_url, use_container_width=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🙈 關閉彩蛋", use_container_width=True, type="primary"):
        st.session_state.show_egg = False
        st.rerun()

# ══════════════════════════════════════════════
# HTML 渲染輔助（批次生成 HTML，減少 st 呼叫次數）
# ══════════════════════════════════════════════

def render_hand_html(rem_cards: list[str], selected: set) -> str:
    """整個手牌區用一個 HTML 區塊渲染，按鈕仍用 st.button"""
    COLS = 3
    rows_html = []
    for rs in range(0, len(rem_cards), COLS):
        row = rem_cards[rs:rs + COLS]
        cells = []
        for name in row:
            info   = CARDS[name]
            is_sel = name in selected
            url    = img_url(name)
            sel_c  = "sel" if is_sel else ""
            sp_c   = "sp"  if info["special"] else ""
            nm_c   = "sp-name" if info["special"] else ""
            chk    = '<div class="badge-sel">✓</div>' if is_sel else ""
            star   = '<div class="badge-star">★特殊</div>' if info["special"] else ""
            cells.append(
                f'<div class="hcard-cell">'
                f'  <div class="card-outer">{chk}{star}'
                f'    <div class="card-inner {sel_c} {sp_c}">'
                f'      <img src="{url}" class="card-img" loading="lazy">'
                f'      <div class="card-name {nm_c}">{name}</div>'
                f'    </div>'
                f'  </div>'
                f'</div>'
            )
        # 補空格
        while len(cells) < COLS:
            cells.append('<div class="hcard-cell"></div>')
        rows_html.append(f'<div class="hcard-row">{"".join(cells)}</div>')
    return "".join(rows_html)

def render_placed_html(placed: list[str], cat: str, scored: set, result: dict, locked: bool) -> str:
    """分類區已放置卡片，整塊 HTML 一次輸出"""
    if not placed:
        return '<div class="cat-empty">尚無卡片</div>'
    COLS = 4
    rows = []
    for rs in range(0, len(placed), COLS):
        row = placed[rs:rs + COLS]
        cells = []
        for pname in row:
            key       = f"{pname}|{cat}"
            is_locked = key in scored
            res       = result.get(key)
            url       = img_url(pname)
            short     = pname.lstrip("★")
            if is_locked or res == "correct":
                pw, ov_c, ov_txt, lc = "pc", "c", "✓", "lc"
            elif res == "wrong":
                pw, ov_c, ov_txt, lc = "pw", "w", "✗", "lw"
            else:
                pw, ov_c, ov_txt, lc = "", "", "", ""
            ov_html = f'<div class="pcard-ov {ov_c}">{ov_txt}</div>' if ov_c else ""
            cells.append(
                f'<div class="pcard-cell">'
                f'  <div class="pcard {pw}">{ov_html}'
                f'    <img src="{url}" class="pcard-img" loading="lazy">'
                f'    <div class="pcard-lbl {lc}">{short}</div>'
                f'  </div>'
                f'</div>'
            )
        while len(cells) < COLS:
            cells.append('<div class="pcard-cell"></div>')
        rows.append(f'<div class="pcard-row">{"".join(cells)}</div>')
    return "".join(rows)

# ══════════════════════════════════════════════
# CSS
# ══════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;600;700;900&display=swap');
* { font-family: 'Noto Sans TC', sans-serif !important; }

[data-testid="stAppViewContainer"] {
    background: #F8F7FF;
    background-image:
        radial-gradient(ellipse at 0% 0%, rgba(185,28,28,0.07) 0%, transparent 50%),
        radial-gradient(ellipse at 100% 100%, rgba(109,40,217,0.07) 0%, transparent 50%);
}
[data-testid="stHeader"] { background: transparent !important; }
.block-container { padding-top: 0.5rem !important; padding-bottom: 2rem !important; }

/* ── Header ── */
.game-header {
    background: linear-gradient(120deg, #991B1B 0%, #B45309 50%, #5B21B6 100%);
    border-radius: 22px;
    padding: 18px 28px;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 8px 36px rgba(0,0,0,0.25);
    flex-wrap: wrap;
    gap: 10px;
}
.game-title { font-size: 1.8rem; font-weight: 900; color: #FFFFFF; letter-spacing: -0.5px; }
.stat-row { display: flex; gap: 8px; flex-wrap: wrap; }
.stat-pill {
    background: rgba(0,0,0,0.35);
    border: 1.5px solid rgba(255,255,255,0.3);
    border-radius: 50px;
    padding: 5px 14px;
    color: #FFFFFF;
    font-weight: 700;
    font-size: 0.82rem;
    white-space: nowrap;
}
.stat-pill b { font-size: 0.95rem; }

/* ── Progress ── */
.prog-wrap {
    background: #374151;
    border-radius: 50px;
    height: 12px;
    overflow: hidden;
    margin: 8px 0 2px;
}
.prog-fill {
    height: 100%;
    border-radius: 50px;
    background: #4ADE80;
    transition: width 0.5s cubic-bezier(.4,0,.2,1);
}
.prog-label { font-size: 0.78rem; color: #374151; font-weight: 600; text-align: right; margin-bottom: 8px; }

/* ── Section titles ── */
.panel-title {
    font-size: 1rem; font-weight: 800; color: #111827;
    padding-bottom: 10px;
    border-bottom: 2px solid #D1D5DB;
    margin-bottom: 10px;
}

/* ── Hand card wrapper ── */
.card-wrap {
    position: relative;
    width: 100%;
    margin-bottom: 0;
}

/* ── Hand cards ── */
.card-btn-inner,
.card-btn-inner,
.card-inner {
    border-radius: 12px;
    overflow: hidden;
    border: 3px solid #9CA3AF;
    background: white;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    transition: border-color 0.12s, box-shadow 0.12s;
    cursor: pointer;
    position: relative;
}
.card-btn-inner.sel,
.card-inner.sel {
    border-color: #B91C1C;
    box-shadow: 0 0 0 3px rgba(185,28,28,0.25), 0 6px 18px rgba(185,28,28,0.2);
}
.card-btn-inner.sp,
.card-inner.sp { border-color: #6D28D9; }
.card-btn-inner.sp.sel,
.card-inner.sp.sel { border-color: #B91C1C; }
.card-img {
    width: 100%;
    aspect-ratio: 1;
    object-fit: cover;
    display: block;
    image-rendering: auto;
}
.badge-sel {
    position: absolute; top: -8px; right: -8px; z-index: 10;
    background: #B91C1C; color: #FFFFFF;
    border-radius: 50%; width: 26px; height: 26px;
    display: flex; align-items: center; justify-content: center;
    font-size: 13px; font-weight: 900;
    box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    border: 2px solid white;
}
.badge-star {
    position: absolute; top: 6px; left: 6px; z-index: 10;
    background: #5B21B6; color: #FFFFFF;
    border-radius: 6px;
    padding: 2px 6px; font-size: 9px; font-weight: 900;
}
.card-name {
    text-align: center;
    padding: 5px 3px 6px;
    font-size: 0.75rem;
    font-weight: 700;
    color: #111827;
    background: white;
    border-top: 2px solid #E5E7EB;
}
.card-name.sp-name { color: #4C1D95; }

/* ── Category zones ── */
.cat-zone {
    border-radius: 18px;
    overflow: hidden;
    box-shadow: 0 4px 18px rgba(0,0,0,0.12);
    margin-bottom: 14px;
    border: 2px solid transparent;
}
.cat-hdr {
    padding: 12px 16px;
    font-weight: 800;
    font-size: 1rem;
    color: #FFFFFF;
    display: flex;
    align-items: center;
    justify-content: space-between;
    text-shadow: 0 1px 2px rgba(0,0,0,0.2);
}
.cat-cnt {
    background: rgba(0,0,0,0.28);
    border-radius: 50px;
    padding: 2px 10px;
    font-size: 0.78rem;
    font-weight: 700;
    color: #FFFFFF;
}
.cat-body { background: white; padding: 10px; min-height: 88px; }
.cat-empty { color: #6B7280; font-size: 0.82rem; font-weight: 600; padding: 18px 0 8px; text-align: center; }

/* ── Placed cards grid ── */
.pcard-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 6px;
    margin-bottom: 6px;
}
.pcard-cell { min-width: 0; }
.pcard {
    border-radius: 10px;
    overflow: hidden;
    border: 3px solid #9CA3AF;
    background: white;
    position: relative;
}
.pcard.pc { border-color: #15803D; }
.pcard.pw { border-color: #B91C1C; }
.pcard-img {
    width: 100%;
    aspect-ratio: 1;
    object-fit: cover;
    display: block;
}
.pcard-ov {
    position: absolute; top: 3px; right: 3px;
    width: 20px; height: 20px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 10px; font-weight: 900;
    border: 2px solid white;
}
.pcard-ov.c { background: #15803D; color: #FFFFFF; }
.pcard-ov.w { background: #B91C1C; color: #FFFFFF; }
.pcard-lbl {
    font-size: 0.68rem; font-weight: 700;
    text-align: center; padding: 3px 2px;
    color: #111827; background: white;
    border-top: 2px solid #E5E7EB;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.pcard-lbl.lc { color: #FFFFFF; background: #15803D; }
.pcard-lbl.lw { color: #FFFFFF; background: #B91C1C; }

/* ── Return banner ── */
.return-banner {
    background: #7F1D1D;
    border: 2px solid #991B1B;
    border-radius: 18px;
    padding: 16px 20px;
    margin: 4px 0 14px;
    display: flex; align-items: center; gap: 16px;
    box-shadow: 0 4px 20px rgba(127,29,29,0.35);
    animation: pulseShadow 2.2s ease-in-out infinite;
}
@keyframes pulseShadow {
    0%, 100% { box-shadow: 0 4px 20px rgba(127,29,29,0.3); }
    50%       { box-shadow: 0 4px 28px rgba(127,29,29,0.55); }
}
.return-icon { font-size: 2rem; line-height: 1; }
.return-info { flex: 1; }
.return-count { font-size: 1.15rem; font-weight: 900; color: #FEF2F2; }
.return-desc  { font-size: 0.8rem; color: #FECACA; margin-top: 3px; line-height: 1.5; font-weight: 500; }
.return-once  { font-size: 0.73rem; color: #FDE68A; font-weight: 700; margin-top: 3px; }

/* ── Buttons ── */
.stButton > button {
    border-radius: 12px !important;
    font-weight: 800 !important;
    font-size: 0.88rem !important;
    transition: transform 0.15s ease, box-shadow 0.15s ease !important;
}
.stButton > button:hover:not([disabled]) {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 20px rgba(0,0,0,0.15) !important;
}
.stButton > button[disabled] { opacity: 0.42 !important; }

/* 手牌按鈕緊貼卡片，去除多餘間距 */
.card-wrap + div[data-testid="stButton"] {
    margin-top: 0 !important;
}
hr { border-color: #D1D5DB !important; margin: 10px 0 !important; }

/* ── 彩蛋 Dialog 樣式 ── */
[data-testid="stDialog"] [data-testid="stImage"] img {
    border-radius: 16px;
    box-shadow: 0 8px 32px rgba(109,40,217,0.3);
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# 彩蛋 Dialog 觸發（必須在主體渲染前呼叫）
# ══════════════════════════════════════════════
if st.session_state.get("show_egg", False):
    egg_count = st.session_state.get("egg_submit_count", 0)
    if egg_count in EGG_URLS:
        show_egg_dialog(EGG_URLS[egg_count], egg_count)

# ══════════════════════════════════════════════
# 讀取狀態（一次性，不重複呼叫）
# ══════════════════════════════════════════════
rem_cards   = get_remaining_cards()
wrong_pairs = get_wrong_pairs()
scored      = st.session_state.scored_keys
scored_cnt  = len(scored)
prog_pct    = round(scored_cnt / TOTAL_NEEDED * 100)

# ══════════════════════════════════════════════
# Header
# ══════════════════════════════════════════════
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
<div class="prog-label">完成進度 {prog_pct}%　({scored_cnt}/{TOTAL_NEEDED} 題已鎖定)</div>
""", unsafe_allow_html=True)

# ── 訊息（深底淺字，高對比）──
if st.session_state.message:
    _styles = {
        "success": ("✅", "#14532D", "#FFFFFF", "#4ADE80"),
        "warning": ("⚠️", "#1F2937", "#F9FAFB", "#F59E0B"),
        "info":    ("📋", "#1F2937", "#F9FAFB", "#60A5FA"),
    }
    icon, bg, text, accent = _styles.get(st.session_state.message_type, _styles["info"])
    msg_html = st.session_state.message.replace("\n", "<br>")
    st.markdown(f"""
    <div style="background:{bg};border-left:5px solid {accent};border-radius:14px;
        padding:13px 18px;margin:6px 0 4px;font-size:0.88rem;font-weight:500;
        color:{text};line-height:1.7;display:flex;align-items:flex-start;gap:10px;">
      <span style="font-size:1.1rem;line-height:1.5;flex-shrink:0;">{icon}</span>
      <span>{msg_html}</span>
    </div>""", unsafe_allow_html=True)

if st.session_state.locked:
    st.balloons()

# ── 一鍵退回 Banner ──
if st.session_state.return_wrong_avail is True and wrong_pairs:
    n_wrong = len(wrong_pairs)
    col_info, col_btn = st.columns([3.5, 1])
    with col_info:
        st.markdown(f"""
        <div class="return-banner">
          <div class="return-icon">↩️</div>
          <div class="return-info">
            <div class="return-count">❌ 發現 {n_wrong} 張錯誤卡牌！</div>
            <div class="return-desc">可一鍵將所有錯誤卡牌退回手牌，重新放置後再提交。</div>
            <div class="return-once">⚠️ 每次批改後僅能使用一次，使用後不可復原</div>
          </div>
        </div>""", unsafe_allow_html=True)
    with col_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        st.button(f"↩ 一鍵退回 {n_wrong} 張", key="return_wrong_btn",
                  on_click=return_all_wrong, use_container_width=True, type="primary")

st.divider()

# ══════════════════════════════════════════════
# 主體
# ══════════════════════════════════════════════
col_hand, col_board = st.columns([1, 2.5], gap="large")

# ─── 左：手牌 ───────────────────────────────
with col_hand:
    n_rem = len(rem_cards)
    st.markdown(
        f'<div class="panel-title">🎴 手牌區　'
        f'<span style="color:#6B7280;font-weight:600;font-size:0.82rem;">剩 {n_rem} 張</span></div>',
        unsafe_allow_html=True,
    )

    if not rem_cards:
        st.markdown(
            '<div style="background:#14532D;color:#FFFFFF;border-radius:12px;'
            'padding:14px 16px;font-weight:700;font-size:0.9rem;text-align:center;">'
            '🎉 手牌已清空！請點「提交答案」</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<p style="color:#111827;font-weight:600;font-size:0.85rem;margin-bottom:8px;">'
            '點卡片選取（可多選）→ 點右方 📥 放入</p>',
            unsafe_allow_html=True,
        )

        selected = st.session_state.selected
        COLS = 3
        for rs in range(0, len(rem_cards), COLS):
            row = rem_cards[rs:rs + COLS]
            cols_ui = st.columns(COLS, gap="small")
            for ci, name in enumerate(row):
                with cols_ui[ci]:
                    info   = CARDS[name]
                    is_sel = name in selected
                    url    = img_url(name)
                    sel_c  = "sel" if is_sel else ""
                    sp_c   = "sp"  if info["special"] else ""
                    nm_c   = "sp-name" if info["special"] else ""
                    chk    = '<div class="badge-sel">✓</div>' if is_sel else ""
                    star   = '<div class="badge-star">★特殊</div>' if info["special"] else ""
                    st.markdown(
                        f'<div class="card-visual {sel_c} {sp_c}">' +
                        chk + star +
                        f'<img src="{url}" class="card-img" loading="lazy">' +
                        f'<div class="card-name {nm_c}">{name}</div>' +
                        '</div>',
                        unsafe_allow_html=True,
                    )
                    st.button(
                        "選取中" if is_sel else "選取",
                        key=f"hand_{name}",
                        on_click=toggle_select, args=(name,),
                        use_container_width=True,
                    )

# ─── 右：分類區 ─────────────────────────────
with col_board:
    st.markdown('<div class="panel-title">🧺 分類區</div>', unsafe_allow_html=True)

    result = st.session_state.result
    locked = st.session_state.locked

    for row_cats in [CATEGORIES[:2], CATEGORIES[2:]]:
        pair_cols = st.columns(2, gap="medium")
        for ci, cat in enumerate(row_cats):
            with pair_cols[ci]:
                s      = CAT_STYLE[cat]
                placed = st.session_state.placed[cat]
                cnt    = len(placed)

                st.markdown(
                    f'<div class="cat-zone" style="border-color:{s["border"]};">'
                    f'<div class="cat-hdr" style="background:{s["hdr"]};">'
                    f'<span>{cat}</span>'
                    f'<span class="cat-cnt">{cnt} 張</span>'
                    f'</div><div class="cat-body">',
                    unsafe_allow_html=True,
                )

                st.button(f"📥 放入此類別", key=f"put_{cat}",
                          on_click=place_selected, args=(cat,),
                          use_container_width=True)

                if not placed:
                    st.markdown('<div class="cat-empty">尚無卡片</div>', unsafe_allow_html=True)
                else:
                    IMG_COLS = 4
                    for rs2 in range(0, len(placed), IMG_COLS):
                        row_p = placed[rs2:rs2 + IMG_COLS]
                        p_cols = st.columns(IMG_COLS, gap="small")
                        for ci2, pname in enumerate(row_p):
                            with p_cols[ci2]:
                                key       = f"{pname}|{cat}"
                                is_locked = key in scored
                                res       = result.get(key)
                                url       = img_url(pname)
                                short     = pname.lstrip("★")

                                if is_locked or res == "correct":
                                    pw, ov_c, ov_txt, lc = "pc", "c", "✓", "lc"
                                elif res == "wrong":
                                    pw, ov_c, ov_txt, lc = "pw", "w", "✗", "lw"
                                else:
                                    pw, ov_c, ov_txt, lc = "", "", "", ""

                                ov_html = f'<div class="pcard-ov {ov_c}">{ov_txt}</div>' if ov_c else ""
                                st.markdown(
                                    f'<div class="pcard {pw}">{ov_html}' +
                                    f'<img src="{url}" class="pcard-img" loading="lazy">' +
                                    f'<div class="pcard-lbl {lc}">{short}</div></div>',
                                    unsafe_allow_html=True,
                                )

                                can_remove = (
                                    not is_locked
                                    and not locked
                                    and res not in ("correct", "wrong")
                                )
                                if can_remove:
                                    st.button(
                                        "↩ 退回",
                                        key=f"rm_{pname}_{cat}",
                                        on_click=remove_card, args=(pname, cat),
                                        use_container_width=True,
                                    )

                st.markdown("</div></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# 底部
# ══════════════════════════════════════════════
st.divider()
b1, b2 = st.columns([3, 1])
with b1:
    st.button("✅ 提交答案", type="primary",
              disabled=st.session_state.locked,
              on_click=submit_answers, use_container_width=True)
with b2:
    if st.button("🔄 重新開始", use_container_width=True):
        restart_game()
        st.rerun()
