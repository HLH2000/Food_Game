"""
食物卡片分類遊戲（圖片版）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【計分規則】
  每次提交只有「新答對」的牌才能得分
  舊有已答對的牌不重複計分

  第1次提交答對：每題 50 分（全分）
  第2次提交新答對：每題 25 分（×0.5）
  第3次提交新答對：每題 12 分（×0.25）
  全對後鎖定，不再計分

【加入圖片 — 看這裡！】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  第 1 步：在本程式（.py 檔案）同一個資料夾下
           建立一個叫做 images 的子資料夾

  第 2 步：把圖片放進去，檔名必須和卡片名稱完全一致
           支援格式：.jpg  .jpeg  .png  .webp

  對應表（卡片名稱 → 圖片檔名）：
    牛排         → images/牛排.jpg
    雞腿         → images/雞腿.jpg
    培根         → images/培根.jpg
    蝦子         → images/蝦子.jpg
    青花椰       → images/青花椰.jpg
    紅蘿蔔       → images/紅蘿蔔.jpg
    玉米         → images/玉米.jpg
    番茄         → images/番茄.jpg
    蘋果         → images/蘋果.jpg
    香蕉         → images/香蕉.jpg
    草莓         → images/草莓.jpg
    西瓜         → images/西瓜.jpg
    蛋糕         → images/蛋糕.jpg
    冰淇淋       → images/冰淇淋.jpg
    餅乾         → images/餅乾.jpg
    ★草莓蛋糕   → images/★草莓蛋糕.jpg
    ★玉米濃湯   → images/★玉米濃湯.jpg
    ★水果冰淇淋 → images/★水果冰淇淋.jpg
    ★番茄炒蛋   → images/★番茄炒蛋.jpg

  第 3 步：執行程式，圖片會自動載入
           沒有圖片的卡片會顯示彩色色塊

需要：pip install pillow
"""

import tkinter as tk
from tkinter import font as tkfont, messagebox
import random, os

# Windows DPI 感知（解決字模糊）
try:
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass

try:
    from PIL import Image, ImageTk, ImageDraw, ImageFont
    PIL_OK = True
except ImportError:
    PIL_OK = False

# ─────────────── 路徑 ───────────────
IMG_DIR   = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")
os.makedirs(IMG_DIR, exist_ok=True)

HAND_SIZE = (90, 90)
CAT_SIZE  = (70, 70)

# ─────────────── 遊戲資料 ───────────────
CATEGORIES = ["🥩 肉類", "🥦 蔬菜", "🍎 水果", "🧁 甜點"]

# ══════════════════════════════════════════════
# 卡片資料
# 若要修改卡片名稱，images/ 資料夾內的圖片檔名也需同步修改
# ══════════════════════════════════════════════
CARDS = [
    # ── 肉類（圖片：images/牛排.jpg 等）──
    {"name": "牛排",         "color": "#FECACA", "valid": ["🥩 肉類"],            "special": False},
    {"name": "雞腿",         "color": "#FED7AA", "valid": ["🥩 肉類"],            "special": False},
    {"name": "培根",         "color": "#FCA5A5", "valid": ["🥩 肉類"],            "special": False},
    {"name": "蝦子",         "color": "#FDBA74", "valid": ["🥩 肉類"],            "special": False},
    # ── 蔬菜（圖片：images/青花椰.jpg 等）──
    {"name": "青花椰",       "color": "#86EFAC", "valid": ["🥦 蔬菜"],            "special": False},
    {"name": "紅蘿蔔",       "color": "#FCA5A5", "valid": ["🥦 蔬菜"],            "special": False},
    {"name": "玉米",         "color": "#FDE68A", "valid": ["🥦 蔬菜"],            "special": False},
    {"name": "番茄",         "color": "#FCA5A5", "valid": ["🥦 蔬菜"],            "special": False},
    # ── 水果（圖片：images/蘋果.jpg 等）──
    {"name": "蘋果",         "color": "#FCA5A5", "valid": ["🍎 水果"],            "special": False},
    {"name": "香蕉",         "color": "#FDE68A", "valid": ["🍎 水果"],            "special": False},
    {"name": "草莓",         "color": "#FECDD3", "valid": ["🍎 水果"],            "special": False},
    {"name": "西瓜",         "color": "#BBF7D0", "valid": ["🍎 水果"],            "special": False},
    # ── 甜點（圖片：images/蛋糕.jpg 等）──
    {"name": "蛋糕",         "color": "#E9D5FF", "valid": ["🧁 甜點"],            "special": False},
    {"name": "冰淇淋",       "color": "#BFDBFE", "valid": ["🧁 甜點"],            "special": False},
    {"name": "餅乾",         "color": "#FDE68A", "valid": ["🧁 甜點"],            "special": False},
    # ── 特殊卡（跨類別，圖片：images/★草莓蛋糕.jpg 等）──
    {"name": "★草莓蛋糕",   "color": "#F5D0FE", "valid": ["🍎 水果", "🧁 甜點"], "special": True},
    {"name": "★玉米濃湯",   "color": "#D1FAE5", "valid": ["🥦 蔬菜", "🥩 肉類"], "special": True},
    {"name": "★水果冰淇淋", "color": "#BAE6FD", "valid": ["🍎 水果", "🧁 甜點"], "special": True},
    {"name": "★番茄炒蛋",   "color": "#FED7AA", "valid": ["🥦 蔬菜", "🥩 肉類"], "special": True},
]

BASE_SCORE = 50   # 第1次提交每題得分，之後每次減半

C = {
    "bg":         "#F7F7F5",
    "surface":    "#FFFFFF",
    "border":     "#E5E5E3",
    "primary":    "#18181B",
    "sub":        "#71717A",
    "accent":     "#2563EB",
    "success":    "#16A34A",
    "danger":     "#DC2626",
    "warn":       "#D97706",
    "multi":      "#EDE9FE",
    "multi_bdr":  "#7C3AED",
    "correct":    "#DCFCE7",
    "correct_bd": "#16A34A",
    "wrong":      "#FEE2E2",
    "wrong_bd":   "#DC2626",
    "submit":     "#2563EB",
    "submit_hv":  "#1D4ED8",
    "locked":     "#6B7280",
}

CAT_COLORS = {
    "🥩 肉類": ("#FEE2E2", "#DC2626"),
    "🥦 蔬菜": ("#DCFCE7", "#16A34A"),
    "🍎 水果": ("#FEF9C3", "#D97706"),
    "🧁 甜點": ("#FAE8FF", "#7C3AED"),
}

# ─────────────── 圖片工具 ───────────────
def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def make_placeholder(name, color_hex, size):
    rgb  = hex_to_rgb(color_hex)
    img  = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([0, 0, size[0]-1, size[1]-1],
                            radius=12, fill=rgb+(255,),
                            outline=(255, 255, 255, 180), width=2)
    label = name.replace("★", "").strip()
    if len(label) > 4:
        label = label[:3] + "\n" + label[3:]
    fnt = ImageFont.load_default()
    for fp in ["/System/Library/Fonts/PingFang.ttc",
               "/System/Library/Fonts/STHeiti Medium.ttc",
               "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
               "C:/Windows/Fonts/msjh.ttc",
               "C:/Windows/Fonts/msyh.ttc"]:
        try:
            fnt = ImageFont.truetype(fp, max(10, size[0]//7)); break
        except Exception:
            pass
    draw.text((size[0]//2, size[1]//2), label,
              fill=(30, 30, 30, 220), font=fnt, anchor="mm", align="center")
    bg = Image.new("RGB", size, (247, 247, 245))
    bg.paste(img, mask=img.split()[3])
    return bg

def load_image(card, size):
    if not PIL_OK:
        return None
    for ext in (".jpg", ".jpeg", ".png", ".webp"):
        path = os.path.join(IMG_DIR, card["name"] + ext)
        if os.path.exists(path):
            try:
                img = Image.open(path).convert("RGB")
                return ImageTk.PhotoImage(img.resize(size, Image.LANCZOS))
            except Exception:
                pass
    return ImageTk.PhotoImage(make_placeholder(card["name"], card["color"], size))


# ─────────────── WrapFrame ───────────────
class WrapFrame(tk.Frame):
    def __init__(self, master, wrap_width, h_gap=6, v_gap=6, **kw):
        super().__init__(master, **kw)
        self._wrap_w = wrap_width
        self._hgap   = h_gap
        self._vgap   = v_gap

    def clear_children(self):
        for w in self.winfo_children():
            w.destroy()
        self.config(height=10)

    def reflow(self):
        children = self.winfo_children()
        x, y, row_h = self._hgap, self._vgap, 0
        for w in children:
            self.update_idletasks()
            ww = w.winfo_reqwidth()
            wh = w.winfo_reqheight()
            if x + ww > self._wrap_w - self._hgap and x > self._hgap:
                x     = self._hgap
                y    += row_h + self._vgap
                row_h = 0
            w.place(x=x, y=y)
            x    += ww + self._hgap
            row_h = max(row_h, wh)
        total_h = y + row_h + self._vgap if children else 10
        self.config(height=max(total_h, 10))


# ─────────────── 主遊戲 ───────────────
class FoodSortGame:
    def __init__(self, root, fullscreen=False):
        self.root = root
        self.root.title("食物分類遊戲")
        self.root.configure(bg=C["bg"])

        if fullscreen:
            self.root.state("zoomed")
            self.root.update_idletasks()
        else:
            self.root.geometry("1400x900")
            self.root.resizable(True, True)

        self.root.update_idletasks()
        self._W = max(self.root.winfo_width(), 1400)
        self._H = max(self.root.winfo_height(), 900)
        self._scale = max(0.85, min(1.6, self._W / 1400))

        # ── 分數狀態 ──
        self.score        = 0
        self.submit_count = 0          # 已提交次數
        self.locked       = False      # 全對後鎖死

        # 追蹤每次已答對的 key set，避免重複計分
        # key 格式："{card_name}|{cat}"
        self.scored_keys  = set()      # 累計已得過分的 key

        self.placed    = {}
        self.cat_slots = {}
        self.result    = {}            # key -> "correct"/"wrong"（最新批改）
        self.selected  = set()
        self._imgs     = {}

        self._fonts()
        self._build_ui()
        self._deal()

        if not PIL_OK:
            messagebox.showwarning("缺少套件",
                "未安裝 Pillow，將使用彩色色塊。\n安裝：pip install pillow")

    def _fs(self, base): return max(8, round(base * self._scale))

    def _fonts(self):
        fam = "Microsoft JhengHei UI"
        self.f_title = tkfont.Font(family=fam, size=self._fs(18), weight="bold")
        self.f_label = tkfont.Font(family=fam, size=self._fs(11), weight="bold")
        self.f_name  = tkfont.Font(family=fam, size=self._fs(9),  weight="bold")
        self.f_small = tkfont.Font(family=fam, size=self._fs(8))
        self.f_btn   = tkfont.Font(family=fam, size=self._fs(10), weight="bold")
        self.f_stat  = tkfont.Font(family=fam, size=self._fs(10))
        self.f_result= tkfont.Font(family=fam, size=self._fs(13), weight="bold")
        self.f_badge = tkfont.Font(family=fam, size=self._fs(8),  weight="bold")

    # ── 計分輔助 ──
    def _multiplier(self):
        """本次提交倍率：第1次=1.0，第2次=0.5 …（submit_count 尚未+1時呼叫）"""
        return 1.0 / (2 ** self.submit_count)

    def _pts_for_new_correct(self):
        """每題新答對的得分"""
        return max(1, round(BASE_SCORE * self._multiplier()))

    # ════════════════ UI ════════════════
    def _build_ui(self):
        s  = self._scale
        px = round(28 * s)

        # 頂部
        top = tk.Frame(self.root, bg=C["bg"])
        top.pack(fill="x", padx=px, pady=(round(16*s), round(5*s)))
        tk.Label(top, text="食物分類遊戲", bg=C["bg"], fg=C["primary"],
                 font=self.f_title).pack(side="left")

        st = tk.Frame(top, bg=C["bg"])
        st.pack(side="right")
        self.submit_lbl = tk.Label(st, text="提交 0 次",
                                    bg=C["bg"], fg=C["sub"], font=self.f_label)
        self.submit_lbl.pack(side="right", padx=(12, 0))
        self.mult_lbl = tk.Label(st, text="本次每題得 50 分",
                                  bg=C["bg"], fg=C["success"], font=self.f_label)
        self.mult_lbl.pack(side="right", padx=(12, 0))
        self.score_lbl = tk.Label(st, text="分數  0",
                                   bg=C["bg"], fg=C["accent"], font=self.f_label)
        self.score_lbl.pack(side="right", padx=(12, 0))

        tk.Frame(self.root, bg=C["border"], height=1).pack(fill="x", padx=px)

        # 結果橫幅
        rb = tk.Frame(self.root, bg=C["bg"], height=round(36*s))
        rb.pack(fill="x", padx=px)
        rb.pack_propagate(False)
        self.result_lbl = tk.Label(rb, text="", bg=C["bg"],
                                    fg=C["success"], font=self.f_result)
        self.result_lbl.pack(side="left", pady=4)
        self.pts_lbl = tk.Label(rb, text="", bg=C["bg"],
                                 fg=C["sub"], font=self.f_stat)
        self.pts_lbl.pack(side="right", pady=4)

        # 說明
        tk.Label(self.root,
            text="點選手牌多選 → 點類別批次放入 ｜ 只有新答對的牌才得分 ｜ 全對後鎖定得分",
            bg=C["bg"], fg=C["sub"], font=self.f_small).pack(pady=(2, 4))

        # 主體
        body = tk.Frame(self.root, bg=C["bg"])
        body.pack(fill="both", expand=True, padx=px, pady=2)
        self._build_hand_panel(body)
        self._build_cat_area(body)

        # 底部
        bot = tk.Frame(self.root, bg=C["bg"])
        bot.pack(fill="x", padx=px, pady=(4, round(14*s)))

        self.submit_btn = tk.Label(
            bot, text="✅  提交答案", bg=C["submit"], fg="white",
            font=self.f_btn, cursor="hand2",
            padx=round(20*s), pady=round(9*s))
        self.submit_btn.pack(side="left", padx=(0, 12))
        self.submit_btn.bind("<Button-1>", lambda e: self._submit())
        self.submit_btn.bind("<Enter>",
            lambda e: self.submit_btn.config(bg=C["submit_hv"]))
        self.submit_btn.bind("<Leave>",
            lambda e: self.submit_btn.config(bg=C["submit"]))

        def gbtn(text, cmd):
            b = tk.Label(bot, text=text, bg=C["surface"], fg=C["primary"],
                         font=self.f_btn, cursor="hand2",
                         padx=round(14*s), pady=round(7*s),
                         highlightthickness=1, highlightbackground=C["border"])
            b.pack(side="left", padx=(0, 8))
            b.bind("<Button-1>", lambda e: cmd())
            b.bind("<Enter>", lambda e: b.config(
                bg=C["primary"], fg="white", highlightbackground=C["primary"]))
            b.bind("<Leave>", lambda e: b.config(
                bg=C["surface"], fg=C["primary"], highlightbackground=C["border"]))

        gbtn("清除選擇", self._clear_sel)
        gbtn("重新開始", self._restart)
        gbtn("💡 提示 −10", self._hint)

        self.status_lbl = tk.Label(
            bot, text="點選手牌選擇卡片，再點類別放入",
            bg=C["bg"], fg=C["sub"], font=self.f_stat)
        self.status_lbl.pack(side="right")

    # ── 手牌面板 ──
    def _build_hand_panel(self, parent):
        s = self._scale
        PANEL_W = round(230 * s)
        panel = tk.Frame(parent, bg=C["surface"],
                          highlightthickness=1,
                          highlightbackground=C["border"],
                          width=PANEL_W)
        panel.pack(side="left", fill="y", padx=(0, round(16*s)))
        panel.pack_propagate(False)

        hdr = tk.Frame(panel, bg=C["surface"])
        hdr.pack(fill="x", padx=12, pady=(12, 6))
        tk.Label(hdr, text="手牌", bg=C["surface"], fg=C["sub"],
                 font=self.f_label).pack(side="left")
        self.sel_badge = tk.Label(hdr, text="", bg=C["multi_bdr"],
                                   fg="white", font=self.f_badge, padx=6, pady=1)
        self.hand_count_lbl = tk.Label(hdr, text="", bg=C["surface"],
                                        fg=C["sub"], font=self.f_small)
        self.hand_count_lbl.pack(side="right", padx=(0, 4))

        tk.Frame(panel, bg=C["border"], height=1).pack(fill="x", padx=12)

        self._hand_canvas = tk.Canvas(panel, bg=C["surface"], bd=0,
                                       highlightthickness=0)
        _sb = tk.Scrollbar(panel, orient="vertical",
                            command=self._hand_canvas.yview)
        self._hand_canvas.configure(yscrollcommand=_sb.set)
        _sb.pack(side="right", fill="y")
        self._hand_canvas.pack(fill="both", expand=True)

        WRAP_W = PANEL_W - 16
        self.hand_wf = WrapFrame(self._hand_canvas, wrap_width=WRAP_W,
                                  h_gap=5, v_gap=5, bg=C["surface"])
        self._hand_canvas.create_window(
            (0, 0), window=self.hand_wf, anchor="nw", width=WRAP_W)
        self.hand_wf.bind("<Configure>", lambda e:
            self._hand_canvas.configure(
                scrollregion=self._hand_canvas.bbox("all")))

    # ── 類別區 ──
    def _build_cat_area(self, parent):
        s = self._scale
        right = tk.Frame(parent, bg=C["bg"])
        right.pack(side="left", fill="both", expand=True)
        right.columnconfigure(0, weight=1)
        right.columnconfigure(1, weight=1)
        right.rowconfigure(0, weight=1)
        right.rowconfigure(1, weight=1)

        self.cat_wf      = {}
        self.cat_cnt_lbl = {}
        cat_w = max(400, round((self._W - round(230*s) - round(80*s)) / 2))

        for i, cat in enumerate(CATEGORIES):
            bg_tag, accent = CAT_COLORS[cat]
            outer = tk.Frame(right, bg=C["border"])
            outer.grid(row=i//2, column=i%2, padx=5, pady=5, sticky="nsew")

            iw = tk.Frame(outer, bg=C["surface"])
            iw.pack(fill="both", expand=True, padx=1, pady=1)

            hdr = tk.Frame(iw, bg=bg_tag)
            hdr.pack(fill="x")
            tk.Label(hdr, text=cat, bg=bg_tag, fg=accent,
                     font=self.f_label,
                     padx=round(12*s), pady=round(8*s)).pack(side="left")
            cnt = tk.Label(hdr, text="0 張", bg=bg_tag, fg=accent,
                            font=self.f_small)
            cnt.pack(side="right", padx=10)
            self.cat_cnt_lbl[cat] = cnt

            cv = tk.Canvas(iw, bg=C["surface"], bd=0,
                            highlightthickness=0, height=round(240*s))
            cv.pack(fill="both", expand=True, padx=4, pady=4)

            wf = WrapFrame(cv, wrap_width=cat_w, h_gap=5, v_gap=5,
                            bg=C["surface"])
            cv.create_window((0, 0), window=wf, anchor="nw", width=cat_w)
            wf.bind("<Configure>", lambda e, c=cv:
                c.configure(scrollregion=c.bbox("all")))
            self.cat_wf[cat] = wf

            for w in [outer, iw, hdr, cv]:
                w.bind("<Button-1>", lambda e, c=cat: self._place(c))
            wf.bind("<Button-1>", lambda e, c=cat: self._place(c))

    # ════════════════ 資料 ════════════════
    def _deal(self):
        self.placed      = {c["name"]: [] for c in CARDS}
        self.cat_slots   = {cat: [] for cat in CATEGORIES}
        self.result      = {}
        self.selected    = set()
        self._imgs       = {}
        self.deck        = random.sample(CARDS, len(CARDS))
        self._refresh_hand()
        self._refresh_cats()
        self._upd_hand_count()
        self._upd_sel_badge()

    def _remaining(self):
        out = []
        for c in self.deck:
            if not c["special"] and not self.placed[c["name"]]:
                out.append(c)
            elif c["special"] and len(self.placed[c["name"]]) < len(c["valid"]):
                out.append(c)
        return out

    def _upd_hand_count(self):
        n = len(self._remaining())
        self.hand_count_lbl.config(text=f"剩 {n} 張")

    def _upd_sel_badge(self):
        n = len(self.selected)
        if n:
            self.sel_badge.config(text=f"已選 {n}")
            self.sel_badge.pack(side="right", padx=(0, 4),
                                 before=self.hand_count_lbl)
        else:
            self.sel_badge.pack_forget()

    def _upd_stats(self):
        self.score_lbl.config(text=f"分數  {self.score}")
        self.submit_lbl.config(text=f"提交 {self.submit_count} 次")

        if self.locked:
            self.mult_lbl.config(text="🔒 得分已鎖定", fg=C["locked"])
            # 鎖住提交按鈕
            self.submit_btn.config(bg=C["locked"], cursor="arrow")
            self.submit_btn.unbind("<Button-1>")
            self.submit_btn.unbind("<Enter>")
            self.submit_btn.unbind("<Leave>")
        else:
            pts = self._pts_for_new_correct()
            mult = self._multiplier()
            if mult >= 1.0:
                color = C["success"]
            elif mult >= 0.25:
                color = C["warn"]
            else:
                color = C["danger"]
            pct = round(mult * 100)
            label = f"本次新答對每題得 {pts} 分（{pct}%）" if mult < 1.0 \
                    else f"本次新答對每題得 {pts} 分（全分）"
            self.mult_lbl.config(text=label, fg=color)

    # ── 手牌刷新 ──
    def _refresh_hand(self):
        self.hand_wf.clear_children()
        for card in self._remaining():
            self._make_hand_card(card)
        self.hand_wf.reflow()
        self.root.update_idletasks()

    def _make_hand_card(self, card):
        s      = self._scale
        is_sel = card["name"] in self.selected
        border = C["multi_bdr"] if is_sel else C["border"]
        bg     = C["multi"]     if is_sel else C["surface"]
        hs     = (round(HAND_SIZE[0]*s), round(HAND_SIZE[1]*s))
        W      = hs[0] + round(18*s)
        H      = hs[1] + round(40*s)

        outer = tk.Frame(self.hand_wf, bg=border,
                          cursor="hand2", width=W, height=H)
        outer.pack_propagate(False)
        inner = tk.Frame(outer, bg=bg,
                          padx=round(4*s), pady=round(4*s))
        inner.place(x=1, y=1, width=W-2, height=H-2)

        if PIL_OK:
            photo = load_image(card, hs)
            self._imgs[f"h_{card['name']}"] = photo
            img_w = tk.Label(inner, image=photo, bg=bg)
        else:
            img_w = tk.Frame(inner, bg=card["color"], width=hs[0], height=hs[1])
        img_w.pack()

        tk.Label(inner, text=card["name"], bg=bg, fg=C["primary"],
                 font=self.f_name, wraplength=W-10,
                 justify="center").pack(pady=(2, 0))

        if is_sel:
            ck = tk.Label(outer, text="✓", bg=C["multi_bdr"], fg="white",
                           font=self.f_badge, padx=3, pady=0)
            ck.place(relx=1.0, y=2, anchor="ne", x=-2)

        def click(e, c=card):
            self._toggle_select(c)
            return "break"
        for w in [outer, inner, img_w]:
            w.bind("<Button-1>", click)

    # ── 類別欄刷新 ──
    def _refresh_cats(self):
        for cat in CATEGORIES:
            wf = self.cat_wf[cat]
            wf.clear_children()
            slots = self.cat_slots[cat]
            self.cat_cnt_lbl[cat].config(text=f"{len(slots)} 張")
            if not slots:
                ph = tk.Label(wf, text="點此放入卡片",
                               bg=C["surface"], fg="#D4D4D4", font=self.f_small)
                ph.bind("<Button-1>", lambda e, c=cat: self._place(c))
                wf.reflow()
                continue
            for cname in slots:
                card = next(c for c in CARDS if c["name"] == cname)
                self._make_cat_card(wf, card, cat)
            wf.reflow()

    def _make_cat_card(self, parent_wf, card, cat):
        s   = self._scale
        key = f"{card['name']}|{cat}"
        res = self.result.get(key)

        # 已得過分的牌顯示淡綠（鎖定狀態），剛批對顯示亮綠
        if key in self.scored_keys:
            border, bg = C["correct_bd"], C["correct"]
        elif res == "wrong":
            border, bg = C["wrong_bd"], C["wrong"]
        else:
            border, bg = C["border"], C["surface"]

        cs = (round(CAT_SIZE[0]*s), round(CAT_SIZE[1]*s))
        W  = cs[0] + round(16*s)
        H  = cs[1] + round(38*s)

        outer = tk.Frame(parent_wf, bg=border,
                          cursor="hand2", width=W, height=H)
        outer.pack_propagate(False)
        inner = tk.Frame(outer, bg=bg,
                          padx=round(3*s), pady=round(3*s))
        inner.place(x=1, y=1, width=W-2, height=H-2)

        if PIL_OK:
            photo = load_image(card, cs)
            self._imgs[f"c_{card['name']}_{cat}"] = photo
            img_w = tk.Label(inner, image=photo, bg=bg)
        else:
            img_w = tk.Frame(inner, bg=card["color"], width=cs[0], height=cs[1])
        img_w.pack()

        # 名稱標示
        if key in self.scored_keys:
            name_txt, name_fg = card["name"] + " ✓", C["success"]
        elif res == "wrong":
            name_txt, name_fg = card["name"] + " ✗", C["danger"]
        else:
            name_txt, name_fg = card["name"], C["primary"]

        tk.Label(inner, text=name_txt, bg=bg, fg=name_fg,
                 font=self.f_small, wraplength=W-6,
                 justify="center").pack(pady=(2, 0))

        # 已得分的牌不顯示退回（避免誤操作）
        if key not in self.scored_keys:
            rm = tk.Label(inner, text="× 退回", bg=bg, fg="#A1A1AA",
                          font=self.f_small, cursor="hand2")
            rm.pack()

            def on_remove(e, c=card, ct=cat):
                self._remove(c, ct)
                return "break"
            for w in [outer, inner, img_w, rm]:
                w.bind("<Button-1>", on_remove)
        else:
            # 已得分牌：點擊不做任何事（鎖定）
            def noop(e): return "break"
            for w in [outer, inner, img_w]:
                w.bind("<Button-1>", noop)

    # ════════════════ 互動 ════════════════
    def _toggle_select(self, card):
        name = card["name"]
        if name in self.selected:
            self.selected.discard(name)
        else:
            self.selected.add(name)
        self._refresh_hand()
        self._upd_sel_badge()
        n = len(self.selected)
        if n == 0:
            self.status_lbl.config(
                text="點選手牌選擇卡片，再點類別放入", fg=C["sub"])
        elif n == 1:
            self.status_lbl.config(
                text=f"已選「{name}」→ 點類別放入", fg=C["accent"])
        else:
            preview = "、".join(list(self.selected)[:2])
            if n > 2: preview += f" …共{n}張"
            self.status_lbl.config(
                text=f"已選 {n} 張（{preview}）→ 點類別批次放入",
                fg=C["multi_bdr"])

    def _clear_sel(self):
        self.selected.clear()
        self._refresh_hand()
        self._upd_sel_badge()
        self.status_lbl.config(text="已清除選擇", fg=C["sub"])

    def _place(self, cat):
        if self.locked: return
        if not self.selected:
            self.status_lbl.config(text="請先點選左側手牌", fg=C["warn"])
            self.root.after(1800, lambda: self.status_lbl.config(
                text="點選手牌選擇卡片，再點類別放入", fg=C["sub"]))
            return

        placed_n = skipped_n = 0
        for name in list(self.selected):
            card = next((c for c in CARDS if c["name"] == name), None)
            if not card: continue
            if cat in self.placed[card["name"]]:
                skipped_n += 1; continue
            if not card["special"] and self.placed[card["name"]]:
                old = self.placed[card["name"]][0]
                # 若舊位置已得過分則不允許移動
                old_key = f"{card['name']}|{old}"
                if old_key in self.scored_keys:
                    skipped_n += 1; continue
                self.cat_slots[old].remove(card["name"])
                self.placed[card["name"]].clear()
                self.result.pop(old_key, None)
            self.placed[card["name"]].append(cat)
            self.cat_slots[cat].append(card["name"])
            self.result.pop(f"{card['name']}|{cat}", None)
            self.selected.discard(name)
            placed_n += 1

        self._refresh_hand()
        self._refresh_cats()
        self._upd_hand_count()
        self._upd_sel_badge()

        if placed_n and not skipped_n:
            self.status_lbl.config(
                text=f"✓  {placed_n} 張 → {cat}", fg=C["success"])
        elif placed_n:
            self.status_lbl.config(
                text=f"✓ {placed_n} 張放入，{skipped_n} 張跳過",
                fg=C["warn"])
        else:
            self.status_lbl.config(
                text="所選卡片已在此類別或已鎖定", fg=C["warn"])
            self.root.after(1800, lambda: self.status_lbl.config(
                text="點選手牌選擇卡片，再點類別放入", fg=C["sub"]))

    def _remove(self, card, cat):
        if self.locked: return
        key = f"{card['name']}|{cat}"
        if key in self.scored_keys: return  # 已得分不可退回
        if card["name"] in self.cat_slots[cat]:
            self.cat_slots[cat].remove(card["name"])
        if cat in self.placed[card["name"]]:
            self.placed[card["name"]].remove(cat)
        self.result.pop(key, None)
        self.selected.discard(card["name"])
        self._refresh_hand()
        self._refresh_cats()
        self._upd_hand_count()
        self._upd_sel_badge()
        self.status_lbl.config(
            text=f"↩  {card['name']} 退回手牌", fg=C["sub"])

    # ════════════════ 提交 ════════════════
    def _submit(self):
        if self.locked:
            messagebox.showinfo("已鎖定",
                "已全對！得分已鎖定，請按「重新開始」。")
            return

        rem = self._remaining()
        if rem:
            names = "、".join(c["name"] for c in rem[:3])
            if len(rem) > 3: names += f" 等{len(rem)}張"
            messagebox.showwarning("尚未完成",
                f"還有 {len(rem)} 張在手牌：{names}\n請全部放入後再提交！")
            return

        # ── 批改 ──
        new_result   = {}
        new_correct  = 0    # 本次「新增答對」數量
        wrong        = 0
        new_pts      = 0    # 本次新增得分
        pts_per      = self._pts_for_new_correct()   # 計分前取倍率

        for card in self.deck:
            for cat in self.placed[card["name"]]:
                key = f"{card['name']}|{cat}"
                if cat in card["valid"]:
                    new_result[key] = "correct"
                    if key not in self.scored_keys:
                        # 新答對 → 得分並記錄
                        self.scored_keys.add(key)
                        new_pts    += pts_per
                        new_correct += 1
                else:
                    new_result[key] = "wrong"
                    wrong += 1

        self.result        = new_result
        self.submit_count += 1
        self.score        += new_pts

        # 全對判斷：所有 key 都在 scored_keys 且無 wrong
        total_needed = sum(len(c["valid"]) for c in CARDS)
        if wrong == 0 and len(self.scored_keys) >= total_needed:
            self.locked = True

        self._upd_stats()
        self._refresh_cats()

        # ── 顯示結果 ──
        mult    = 1.0 / (2 ** (self.submit_count - 1))
        pct_str = "全分" if mult >= 1.0 else f"{round(mult*100)}%"

        already_correct = len(self.scored_keys) - new_correct  # 本次前已答對數

        if self.locked:
            self.result_lbl.config(
                text=f"🎉 全對！本次新答對 {new_correct} 題",
                fg=C["success"])
            self.pts_lbl.config(
                text=f"+{new_pts} 分（每題{pts_per}分，{pct_str}）  🔒 得分已鎖定",
                fg=C["success"])
            self.status_lbl.config(
                text="完美！得分已鎖定，可按重新開始", fg=C["success"])
        elif wrong == 0 and new_correct == 0:
            # 全放對但全都是舊答對，沒有新得分
            self.result_lbl.config(
                text=f"所有答對均已計過分，本次 +0",
                fg=C["sub"])
            self.pts_lbl.config(text="", fg=C["sub"])
            self.status_lbl.config(
                text="沒有新答對，請調整錯誤的卡片", fg=C["warn"])
        else:
            next_pts = max(1, round(BASE_SCORE * self._multiplier()))
            self.result_lbl.config(
                text=(f"新答對 {new_correct} 題  ｜  "
                      f"答錯 {wrong} 題  ｜  "
                      f"舊有答對 {already_correct} 題（不計分）"),
                fg=C["warn"] if wrong else C["accent"])
            self.pts_lbl.config(
                text=(f"+{new_pts} 分（每題{pts_per}分，{pct_str}）"
                      f"  ▸ 下次新答對每題得 {next_pts} 分"),
                fg=C["sub"])
            self.status_lbl.config(
                text="紅色為錯誤，退回修改後可再提交（新答對才得分）",
                fg=C["danger"] if wrong else C["sub"])

    def _hint(self):
        if self.locked: return
        for card in self.deck:
            missing = [c for c in card["valid"]
                       if c not in self.placed.get(card["name"], [])]
            if (not card["special"] and not self.placed[card["name"]]) \
               or (card["special"] and missing):
                target = missing[0] if missing else card["valid"][0]
                self.score = max(0, self.score - 10)
                self._upd_stats()
                self.result_lbl.config(text="💡 提示使用", fg=C["sub"])
                self.pts_lbl.config(text="−10 分", fg=C["sub"])
                messagebox.showinfo("💡 提示",
                    f"「{card['name']}」應放到「{target}」")
                return
        messagebox.showinfo("提示", "所有卡片已放完，按提交答案！")

    def _restart(self):
        self.score        = 0
        self.submit_count = 0
        self.locked       = False
        self.scored_keys  = set()
        # 恢復提交按鈕
        self.submit_btn.config(bg=C["submit"], cursor="hand2")
        self.submit_btn.bind("<Button-1>", lambda e: self._submit())
        self.submit_btn.bind("<Enter>",
            lambda e: self.submit_btn.config(bg=C["submit_hv"]))
        self.submit_btn.bind("<Leave>",
            lambda e: self.submit_btn.config(bg=C["submit"]))
        self._upd_stats()
        self.result_lbl.config(text="")
        self.pts_lbl.config(text="")
        self.status_lbl.config(
            text="點選手牌選擇卡片，再點類別放入", fg=C["sub"])
        self._deal()


# ════════════════ 啟動視窗 ════════════════
def ask_fullscreen():
    dlg = tk.Tk()
    dlg.title("食物分類遊戲")
    dlg.resizable(False, False)
    dlg.configure(bg="#F7F7F5")
    dlg.update_idletasks()
    W, H = 380, 200
    sw, sh = dlg.winfo_screenwidth(), dlg.winfo_screenheight()
    dlg.geometry(f"{W}x{H}+{(sw-W)//2}+{(sh-H)//2}")

    choice = {"full": False}
    fnt_t = tkfont.Font(family="Microsoft JhengHei UI", size=14, weight="bold")
    fnt_s = tkfont.Font(family="Microsoft JhengHei UI", size=10)
    fnt_b = tkfont.Font(family="Microsoft JhengHei UI", size=11, weight="bold")

    tk.Label(dlg, text="食物分類遊戲", bg="#F7F7F5", fg="#18181B",
             font=fnt_t).pack(pady=(28, 6))
    tk.Label(dlg, text="請選擇視窗模式：", bg="#F7F7F5", fg="#71717A",
             font=fnt_s).pack()

    btn_row = tk.Frame(dlg, bg="#F7F7F5")
    btn_row.pack(pady=18)

    def start(full):
        choice["full"] = full
        dlg.destroy()

    b1 = tk.Label(btn_row, text="🖥  全螢幕", bg="#2563EB", fg="white",
                   font=fnt_b, cursor="hand2", padx=20, pady=9)
    b1.pack(side="left", padx=10)
    b1.bind("<Button-1>", lambda e: start(True))
    b1.bind("<Enter>", lambda e: b1.config(bg="#1D4ED8"))
    b1.bind("<Leave>", lambda e: b1.config(bg="#2563EB"))

    b2 = tk.Label(btn_row, text="🪟  視窗模式", bg="#FFFFFF", fg="#18181B",
                   font=fnt_b, cursor="hand2", padx=20, pady=9,
                   highlightthickness=1, highlightbackground="#E5E5E3")
    b2.pack(side="left", padx=10)
    b2.bind("<Button-1>", lambda e: start(False))
    b2.bind("<Enter>", lambda e: b2.config(bg="#F3F4F6"))
    b2.bind("<Leave>", lambda e: b2.config(bg="#FFFFFF"))

    dlg.mainloop()
    return choice["full"]


if __name__ == "__main__":
    fullscreen = ask_fullscreen()
    root = tk.Tk()
    FoodSortGame(root, fullscreen=fullscreen)
    root.mainloop()
