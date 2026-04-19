import tkinter as tk
from tkinter import Canvas, Frame, Label, Button, Entry
import random
import json
import os
import threading
import calendar
import datetime
try:
    import requests
    REQUESTS_OK = True
except ImportError:
    REQUESTS_OK = False

# ============ DESIGN TOKENS ============
BG_DARK        = "#0a0a0f"
BG_CARD        = "#12121a"
BG_CARD2       = "#1a1a28"
ACCENT_CYAN    = "#00e5ff"
ACCENT_PINK    = "#ff2d78"
ACCENT_GREEN   = "#39ff14"
ACCENT_PURPLE  = "#9b59ff"
ACCENT_ORANGE  = "#ff8c00"
ACCENT_YELLOW  = "#ffe600"
ACCENT_TEAL    = "#00ffc8"
TEXT_PRIMARY   = "#f0f0ff"
TEXT_DIM       = "#6b6b8a"
FONT_TITLE     = ("Courier New", 52, "bold")
FONT_SUBTITLE  = ("Courier New", 16)
FONT_BODY      = ("Courier New", 13)
FONT_SCORE     = ("Courier New", 20, "bold")
FONT_BTN       = ("Courier New", 14, "bold")
FONT_BTN_LG    = ("Courier New", 18, "bold")

SCORES_FILE    = os.path.join(os.path.dirname(os.path.abspath(__file__)), "game_hub_scores.json")
SETTINGS_FILE  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hub_settings.json")
DAILY_CACHE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "daily_cache.json")

# ============ SNAKE CONSTANTS ============
GAME_WIDTH   = 600
GAME_HEIGHT  = 600
SPEED        = 100
SPACE_SIZE   = 30
BODY_PARTS   = 3

# ============ WORDLE WORD LIST ============
WORDLE_WORDS = [
    "ABOUT","ABOVE","ABUSE","ACTOR","ACUTE","ADMIT","ADOPT","ADULT","AFTER","AGAIN",
    "AGENT","AGREE","AHEAD","ALARM","ALBUM","ALERT","ALIVE","ALLEY","ALLOW","ALONE",
    "ALONG","ALTER","ANGEL","ANGER","ANGLE","ANGRY","ANKLE","APART","APPLE","APPLY",
    "ARGUE","ARISE","ARMOR","AROMA","AROSE","ARROW","ASIDE","ATLAS","ATTIC","AUDIO",
    "AVOID","AWAKE","AWARD","AWARE","AWFUL","BAKER","BASIC","BASIS","BATCH","BEACH",
    "BEGAN","BEGIN","BEING","BELOW","BENCH","BIRTH","BLACK","BLADE","BLAME","BLANK",
    "BLAST","BLAZE","BLEND","BLIND","BLOCK","BLOOD","BLOOM","BLOWN","BLUNT","BOARD",
    "BONUS","BOOST","BOUND","BRACE","BRAIN","BRAND","BRAVE","BREAK","BREED","BRICK",
    "BRIDE","BRIEF","BRING","BROAD","BROKE","BROWN","BRUSH","BUILD","BUILT","BUNCH",
    "BURST","BUYER","CABIN","CABLE","CANDY","CARRY","CATCH","CAUSE","CHAIR","CHAOS",
    "CHARM","CHART","CHASE","CHEAP","CHECK","CHESS","CHEST","CHIEF","CHILD","CHOIR",
    "CHOSE","CIVIL","CLAIM","CLASH","CLASS","CLEAN","CLEAR","CLIFF","CLIMB","CLOCK",
    "CLOSE","CLOUD","COACH","COAST","COUNT","COURT","COVER","CRACK","CRAFT","CRASH",
    "CRAZY","CREAM","CRIME","CRISP","CROSS","CROWD","CROWN","CRUEL","CRUSH","CYCLE",
    "DANCE","DEATH","DELAY","DENSE","DEPTH","DEVIL","DIRTY","DOUBT","DOUGH","DRAFT",
    "DRAMA","DRAWN","DREAM","DRESS","DRIFT","DRINK","DRIVE","DRONE","DROVE","DROWN",
    "DUSTY","EARLY","EARTH","EIGHT","ELITE","EMPTY","ENEMY","ENJOY","ENTER","EQUAL",
    "ERROR","EVENT","EXACT","EXIST","EXTRA","FABLE","FAIRY","FAITH","FALSE","FANCY",
    "FATAL","FEAST","FENCE","FEVER","FIELD","FIFTH","FIFTY","FIGHT","FINAL","FIRST",
    "FIXED","FLAME","FLASH","FLEET","FLESH","FLINT","FLOAT","FLOOD","FLOOR","FLOUR",
    "FLUID","FLUTE","FOCUS","FORCE","FORGE","FORTH","FORUM","FOUND","FRAME","FRANK",
    "FRAUD","FRESH","FRONT","FROZE","FRUIT","FULLY","FUNNY","GHOST","GIANT","GLASS",
    "GLOBE","GLORY","GLOVE","GRACE","GRADE","GRAIN","GRAND","GRANT","GRASP","GRASS",
    "GRAVE","GREAT","GREED","GREEN","GRIEF","GRILL","GRIND","GROAN","GROUP","GROVE",
    "GROWN","GUARD","GUESS","GUIDE","GUILD","GUILT","HAPPY","HARSH","HAVEN","HEART",
    "HEAVY","HINGE","HOBBY","HONEY","HONOR","HORSE","HOTEL","HOUSE","HUMAN","HUMOR",
    "HURRY","IDEAL","IMAGE","IMPLY","INNER","INPUT","ISSUE","JEWEL","JOKER","JOINT",
    "JUDGE","JUICE","JUMBO","LABEL","LANCE","LARGE","LASER","LATCH","LATER","LAUGH",
    "LAYER","LEARN","LEAST","LEGAL","LEMON","LEVEL","LIGHT","LIMIT","LOCAL","LOGIC",
    "LOOSE","LOVER","LOWER","LOYAL","LUCKY","MAGIC","MAJOR","MAKER","MARCH","MATCH",
    "MAYOR","MEDAL","MEDIA","MERCY","MERIT","METAL","MIGHT","MINOR","MIXED","MODEL",
    "MONEY","MONTH","MORAL","MOTOR","MOUNT","MOUTH","MOVIE","MUSIC","NAIVE","NERVE",
    "NEVER","NIGHT","NOBLE","NOISE","NORTH","NOVEL","NURSE","OCCUR","OCEAN","OFFER",
    "OFTEN","ORDER","OTHER","OUTER","OWNED","PAINT","PANEL","PAPER","PARTY","PASTA",
    "PATCH","PAUSE","PEACE","PEACH","PEARL","PENNY","PHASE","PHONE","PHOTO","PITCH",
    "PIXEL","PIZZA","PLACE","PLAIN","PLANE","PLANT","PLATE","POINT","POLAR","PORCH",
    "POWER","PRESS","PRICE","PRIDE","PRIME","PRINT","PRIZE","PROBE","PROOF","PROSE",
    "PROUD","PROVE","PULSE","QUEEN","QUERY","QUEST","QUICK","QUIET","QUOTA","QUOTE",
    "RADAR","RADIO","RAISE","RANGE","RAPID","REACH","REACT","READY","REALM","REBEL",
    "REFER","REIGN","RELAX","REPLY","RESET","RIDGE","RIGHT","RIVAL","RIVER","ROAST",
    "ROBOT","ROCKY","ROUND","ROUTE","ROYAL","RULER","SAINT","SALAD","SAUCE","SCALE",
    "SCARE","SCENE","SCOPE","SCORE","SCOUT","SEIZE","SENSE","SERVE","SEVEN","SHADE",
    "SHAKE","SHAME","SHAPE","SHARE","SHARK","SHARP","SHELF","SHELL","SHIFT","SHINE",
    "SHOCK","SHORE","SHORT","SHOUT","SIGHT","SINCE","SIXTH","SIXTY","SKILL","SKULL",
    "SLATE","SLEEP","SLICE","SLIDE","SLOPE","SMART","SMILE","SMOKE","SNEAK","SOLVE",
    "SORRY","SOUND","SOUTH","SPACE","SPARK","SPEAK","SPEED","SPEND","SPICE","SPIKE",
    "SPITE","SPLIT","SPORT","SPRAY","STACK","STAFF","STAGE","STAIN","STAKE","STAND",
    "STARE","START","STATE","STEAL","STEAM","STEEL","STICK","STILL","STOCK","STONE",
    "STORE","STORM","STORY","STRAP","STRAW","STRIP","STUCK","STUDY","STYLE","SUGAR",
    "SUITE","SUNNY","SUPER","SURGE","SWEAR","SWEET","SWIFT","TABLE","TASTE","TEACH",
    "TENSE","THANK","THEME","THICK","THING","THINK","THIRD","THORN","THREE","THREW",
    "THROW","TIGER","TIGHT","TIRED","TITLE","TODAY","TOKEN","TORCH","TOTAL","TOUCH",
    "TOUGH","TOWER","TOXIC","TRACK","TRADE","TRAIL","TRAIN","TRAIT","TREND","TRIAL",
    "TRIBE","TROOP","TRUCE","TRUCK","TRUNK","TRUST","TRUTH","TWICE","TWIST","ULTRA",
    "UNCLE","UNDER","UNION","UNITY","UNTIL","UPPER","UPSET","URBAN","VALID","VALUE",
    "VAPOR","VAULT","VENOM","VERSE","VIDEO","VIRAL","VISIT","VITAL","VIVID","VOCAL",
    "VOICE","WASTE","WATCH","WATER","WEAVE","WEIRD","WHALE","WHEAT","WHEEL","WHERE",
    "WHICH","WHILE","WHITE","WHOLE","WITCH","WOMAN","WORLD","WORRY","WORSE","WORST",
    "WORTH","WOULD","WOUND","WRATH","WRIST","WROTE","YIELD","YOUNG","YOUTH","ZEBRA",
]

# ============ HANGMAN WORDS ============
HANGMAN_WORDS = [
    "PYTHON","KEYBOARD","MONITOR","FUNCTION","VARIABLE","ALGORITHM","DATABASE",
    "NETWORK","BROWSER","INTERFACE","DEVELOPER","PROGRAMMING","COMPUTER","SOFTWARE",
    "HARDWARE","ELEPHANT","GIRAFFE","DOLPHIN","PENGUIN","CHEETAH","CROCODILE",
    "BUTTERFLY","OCTOPUS","KANGAROO","FLAMINGO","MOUNTAIN","VOLCANO","GLACIER",
    "WATERFALL","RAINFOREST","ADVENTURE","CHOCOLATE","SPAGHETTI","UMBRELLA",
    "BLANKET","CALENDAR","HOSPITAL","TREASURE","UNIVERSE","CHAMPION","BIRTHDAY",
    "FOOTBALL","BASKETBALL","SWIMMING","CLIMBING","PAINTING","MYSTERY","FANTASY",
    "JOURNEY","VICTORY","DIAMOND","CRYSTAL","TORNADO","THUNDER","RAINBOW",
]

# ─── UNIVERSITY CONSTANTS ─────────────────────────────────────────────
UNIVERSITY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "university_data.json")

TIMETABLE = {
    "Monday": [
        {"start": "12:00", "end": "14:00", "type": "Lec",
         "module": "Contemporary Marketing",
         "room": "Dorothy Fleming Lecture Theatre, Level 0, City"},
    ],
    "Wednesday": [
        {"start": "09:00", "end": "11:00", "type": "Sem",
         "module": "Understanding People And Cultures",
         "room": "Owen-1033, Level 10, City"},
        {"start": "11:00", "end": "13:00", "type": "Sem",
         "module": "Contemporary Marketing",
         "room": "Langsett-38 03 02, Level 3, City"},
    ],
    "Friday": [
        {"start": "14:00", "end": "15:00", "type": "Lec",
         "module": "Understanding People And Cultures",
         "room": "Howard-5225 Pennine, Level 2, City"},
        {"start": "15:00", "end": "17:00", "type": "Sem",
         "module": "Contemporary Marketing",
         "room": "Cantor-9234, Level 2, City"},
    ],
}

DEGREE_START = datetime.date(2025, 9, 1)
DEGREE_END   = datetime.date(2028, 6, 1)

MODULE_COLORS = {
    "Contemporary Marketing":            ACCENT_ORANGE,
    "Understanding People And Cultures": ACCENT_TEAL,
}


class GameHub:
    def __init__(self, root):
        self.root = root
        self.root.title("HARRY'S GAME HUB")
        self.root.state("zoomed")
        self.root.configure(bg=BG_DARK)
        self.snake_state = {}
        self.high_scores = self._load_scores()
        self._load_settings()
        self.show_login()

    # ─── UTILS ────────────────────────────────────────────────
    def clear(self):
        for w in self.root.winfo_children():
            w.destroy()
        # Unbind generic keys that games may have set
        self.root.unbind("<Key>")

    def glow_btn(self, parent, text, cmd, color=ACCENT_CYAN, width=22):
        f = Frame(parent, bg=color, padx=2, pady=2)
        b = Button(f, text=text, command=cmd,
                   bg=BG_CARD2, fg=color, font=FONT_BTN_LG,
                   relief="flat", bd=0, padx=24, pady=12,
                   activebackground=color, activeforeground=BG_DARK,
                   cursor="hand2", width=width)
        b.pack()
        b.bind("<Enter>", lambda e: b.config(bg=color, fg=BG_DARK))
        b.bind("<Leave>", lambda e: b.config(bg=BG_CARD2, fg=color))
        return f

    def small_btn(self, parent, text, cmd, color=ACCENT_CYAN):
        f = Frame(parent, bg=color, padx=1, pady=1)
        b = Button(f, text=text, command=cmd,
                   bg=BG_CARD2, fg=color, font=FONT_BTN,
                   relief="flat", bd=0, padx=18, pady=8,
                   activebackground=color, activeforeground=BG_DARK,
                   cursor="hand2")
        b.pack()
        b.bind("<Enter>", lambda e: b.config(bg=color, fg=BG_DARK))
        b.bind("<Leave>", lambda e: b.config(bg=BG_CARD2, fg=color))
        return f

    def divider(self, parent, color=ACCENT_CYAN):
        return Canvas(parent, height=2, bg=color, highlightthickness=0, bd=0)

    def game_header(self, title_text, color, restart_cmd):
        """Standard top bar: title + Restart + Home buttons."""
        header = Frame(self.root, bg=BG_DARK, pady=8)
        header.pack(fill="x", padx=40)
        Label(header, text=title_text, font=("Courier New", 26, "bold"),
              bg=BG_DARK, fg=color).pack(side="left")
        self.small_btn(header, "⌂  DASHBOARD", self.show_dashboard,
                       TEXT_DIM).pack(side="right", padx=(6, 0))
        self.small_btn(header, "🎮  GAMES", self.show_home,
                       TEXT_DIM).pack(side="right", padx=(6, 0))
        self.small_btn(header, "↺  RESTART", restart_cmd,
                       color).pack(side="right", padx=6)
        self.divider(self.root, color).pack(fill="x", padx=40)

    # ─── HIGH SCORES ──────────────────────────────────────────
    def _load_scores(self):
        try:
            with open(SCORES_FILE, "r") as f:
                data = json.load(f)
            # Migrate old format (list of ints) to list of dicts
            for game in data:
                data[game] = [
                    e if isinstance(e, dict) else {"score": e, "name": ""}
                    for e in data[game]
                ]
            return data
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _load_settings(self):
        global ACCENT_CYAN
        defaults = {
            "display_name": "HARRY",
            "password":     "0211",
            "snake_speed":  100,
            "accent_colour": "#00e5ff",
        }
        try:
            with open(SETTINGS_FILE, "r") as f:
                data = json.load(f)
            self.settings = {**defaults, **data}
        except (FileNotFoundError, json.JSONDecodeError):
            self.settings = defaults
        self.snake_speed = self.settings["snake_speed"]
        ACCENT_CYAN = self.settings["accent_colour"]

    def _save_settings(self):
        with open(SETTINGS_FILE, "w") as f:
            json.dump(self.settings, f)

    def _load_daily_cache(self):
        try:
            with open(DAILY_CACHE_FILE, "r") as f:
                data = json.load(f)
            if data.get("date") == str(datetime.date.today()):
                return data
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        return {}

    def _save_daily_cache(self, data):
        data["date"] = str(datetime.date.today())
        with open(DAILY_CACHE_FILE, "w") as f:
            json.dump(data, f)

    def _save_scores(self):
        with open(SCORES_FILE, "w") as f:
            json.dump(self.high_scores, f)

    def _check_rank(self, game, score):
        """Return what rank this score would achieve (1-based), or None if outside top 5."""
        entries = self.high_scores.get(game, [])
        rank = sum(1 for e in entries if e["score"] > score) + 1
        return rank if rank <= 5 else None

    def _add_score(self, game, score, name=""):
        """Save score with name. Returns rank (1-5) or None."""
        entries = self.high_scores.setdefault(game, [])
        entries.append({"score": score, "name": name})
        entries.sort(key=lambda e: e["score"], reverse=True)
        self.high_scores[game] = entries[:5]
        self._save_scores()
        try:
            return next(i + 1 for i, e in enumerate(self.high_scores[game])
                        if e["score"] == score and e["name"] == name)
        except StopIteration:
            return None

    def _check_rank_asc(self, game, score):
        """Like _check_rank but lower score is better (e.g. fewest attempts)."""
        entries = self.high_scores.get(game, [])
        rank = sum(1 for e in entries if e["score"] < score) + 1
        return rank if rank <= 5 else None

    def _add_score_asc(self, game, score, name=""):
        """Save score where lower is better. Returns rank (1-5) or None."""
        entries = self.high_scores.setdefault(game, [])
        entries.append({"score": score, "name": name})
        entries.sort(key=lambda e: e["score"])
        self.high_scores[game] = entries[:5]
        self._save_scores()
        try:
            return next(i + 1 for i, e in enumerate(self.high_scores[game])
                        if e["score"] == score and e["name"] == name)
        except StopIteration:
            return None

    def _prompt_name(self, score, rank, on_save):
        """Show a styled name-entry popup for a top-3 score."""
        win = tk.Toplevel(self.root)
        win.title("New High Score!")
        win.configure(bg=BG_DARK)
        win.resizable(False, False)
        win.grab_set()

        medal_map  = {1: "🥇", 2: "🥈", 3: "🥉"}
        color_map  = {1: ACCENT_YELLOW, 2: "#c8c8c8", 3: "#cd7f32"}
        medal = medal_map.get(rank, "🏆")
        color = color_map.get(rank, ACCENT_GREEN)

        Label(win, text=f"{medal}  TOP {rank} HIGH SCORE  {medal}",
              font=("Courier New", 20, "bold"),
              bg=BG_DARK, fg=color).pack(pady=(24, 4))
        Label(win, text=f"SCORE:  {score}",
              font=("Courier New", 16), bg=BG_DARK, fg=ACCENT_CYAN).pack(pady=(0, 14))
        Canvas(win, height=2, bg=color, highlightthickness=0,
               bd=0, width=320).pack(fill="x", padx=30)
        Label(win, text="ENTER YOUR NAME",
              font=FONT_BODY, bg=BG_DARK, fg=TEXT_DIM).pack(pady=(16, 6))

        ef = Frame(win, bg=color, padx=2, pady=2)
        ef.pack()
        entry = Entry(ef, font=("Courier New", 22, "bold"), width=10,
                      bg=BG_CARD2, fg=color, insertbackground=color,
                      relief="flat", bd=0, justify="center")
        entry.pack(ipady=8, ipadx=8)
        entry.focus()

        def save(*_):
            name = entry.get().strip()[:12] or "???"
            win.destroy()
            on_save(name)

        entry.bind("<Return>", save)
        self.small_btn(win, "✓  SAVE", save, color).pack(pady=(14, 22))
        win.protocol("WM_DELETE_WINDOW", save)  # treat close as save with current input

        win.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width()  - win.winfo_width())  // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - win.winfo_height()) // 2
        win.geometry(f"+{x}+{y}")

    def show_snake_scores(self):
        win = tk.Toplevel(self.root)
        win.title("Snake — High Scores")
        win.configure(bg=BG_DARK)
        win.resizable(False, False)
        win.grab_set()

        Label(win, text="🏆  SNAKE  HIGH SCORES",
              font=("Courier New", 20, "bold"),
              bg=BG_DARK, fg=ACCENT_GREEN).pack(pady=(24, 8))
        Canvas(win, height=2, bg=ACCENT_GREEN, highlightthickness=0,
               bd=0, width=340).pack(fill="x", padx=30)

        scores = self.high_scores.get("snake", [])
        medals      = ["🥇", "🥈", "🥉", " 4.", " 5."]
        name_colors = {0: ACCENT_YELLOW, 1: "#c8c8c8", 2: "#cd7f32"}

        inner = Frame(win, bg=BG_DARK)
        inner.pack(pady=12, padx=30, fill="x")

        if not scores:
            Label(inner, text="No scores yet!\nPlay Snake to set a record.",
                  font=FONT_BODY, bg=BG_DARK, fg=TEXT_DIM,
                  justify="center").pack(pady=20)
        else:
            for i, e in enumerate(scores):
                s    = e["score"] if isinstance(e, dict) else e
                name = e.get("name", "") if isinstance(e, dict) else ""
                nc   = name_colors.get(i, TEXT_DIM)
                row  = Frame(inner, bg=BG_CARD2,
                             highlightbackground=ACCENT_GREEN,
                             highlightthickness=1)
                row.pack(fill="x", pady=3, ipady=8)
                Label(row, text=medals[i] if i < len(medals) else f" {i+1}.",
                      font=("Courier New", 17, "bold"),
                      bg=BG_CARD2, fg=nc, width=4).pack(side="left", padx=10)
                if name:
                    Label(row, text=name,
                          font=("Courier New", 15, "bold"),
                          bg=BG_CARD2, fg=nc).pack(side="left", padx=4)
                Label(row, text=str(s),
                      font=("Courier New", 22, "bold"),
                      bg=BG_CARD2, fg=ACCENT_GREEN).pack(side="right", padx=16)
                Label(row, text="pts",
                      font=FONT_BODY, bg=BG_CARD2, fg=TEXT_DIM).pack(side="right")

        self.small_btn(win, "CLOSE", win.destroy,
                       ACCENT_CYAN).pack(pady=(8, 20))
        win.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width()  - win.winfo_width())  // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - win.winfo_height()) // 2
        win.geometry(f"+{x}+{y}")

    def show_number_scores(self):
        win = tk.Toplevel(self.root)
        win.title("Number Guess — High Scores")
        win.configure(bg=BG_DARK)
        win.resizable(False, False)
        win.grab_set()

        Label(win, text="🏆  NUMBER GUESS  HIGH SCORES",
              font=("Courier New", 20, "bold"),
              bg=BG_DARK, fg=ACCENT_PURPLE).pack(pady=(24, 4))
        Label(win, text="fewest attempts wins",
              font=FONT_BODY, bg=BG_DARK, fg=TEXT_DIM).pack(pady=(0, 8))
        Canvas(win, height=2, bg=ACCENT_PURPLE, highlightthickness=0,
               bd=0, width=340).pack(fill="x", padx=30)

        scores = self.high_scores.get("number_guess", [])
        medals      = ["🥇", "🥈", "🥉", " 4.", " 5."]
        name_colors = {0: ACCENT_YELLOW, 1: "#c8c8c8", 2: "#cd7f32"}

        inner = Frame(win, bg=BG_DARK)
        inner.pack(pady=12, padx=30, fill="x")

        if not scores:
            Label(inner, text="No scores yet!\nPlay Number Guess to set a record.",
                  font=FONT_BODY, bg=BG_DARK, fg=TEXT_DIM,
                  justify="center").pack(pady=20)
        else:
            for i, e in enumerate(scores):
                s    = e["score"] if isinstance(e, dict) else e
                name = e.get("name", "") if isinstance(e, dict) else ""
                nc   = name_colors.get(i, TEXT_DIM)
                row  = Frame(inner, bg=BG_CARD2,
                             highlightbackground=ACCENT_PURPLE,
                             highlightthickness=1)
                row.pack(fill="x", pady=3, ipady=8)
                Label(row, text=medals[i] if i < len(medals) else f" {i+1}.",
                      font=("Courier New", 17, "bold"),
                      bg=BG_CARD2, fg=nc, width=4).pack(side="left", padx=10)
                if name:
                    Label(row, text=name,
                          font=("Courier New", 15, "bold"),
                          bg=BG_CARD2, fg=nc).pack(side="left", padx=4)
                Label(row, text=str(s),
                      font=("Courier New", 22, "bold"),
                      bg=BG_CARD2, fg=ACCENT_PURPLE).pack(side="right", padx=16)
                Label(row, text="tries",
                      font=FONT_BODY, bg=BG_CARD2, fg=TEXT_DIM).pack(side="right")

        self.small_btn(win, "CLOSE", win.destroy,
                       ACCENT_CYAN).pack(pady=(8, 20))
        win.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width()  - win.winfo_width())  // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - win.winfo_height()) // 2
        win.geometry(f"+{x}+{y}")

    # ─── LOGIN SCREEN ─────────────────────────────────────────
    def show_login(self):
        self.clear()

        wrapper = Frame(self.root, bg=BG_DARK)
        wrapper.place(relx=0.5, rely=0.5, anchor="center")

        Label(wrapper, text=f"◈  {self.settings['display_name'].upper()}'S HUB  ◈",
              font=FONT_TITLE, bg=BG_DARK, fg=ACCENT_CYAN).pack(pady=(0, 6))
        self.divider(wrapper, ACCENT_CYAN).pack(fill="x", pady=4)
        Label(wrapper, text="L O G I N   T O   C O N T I N U E",
              font=FONT_SUBTITLE, bg=BG_DARK, fg=TEXT_DIM).pack(pady=(4, 30))

        form = Frame(wrapper, bg=BG_DARK)
        form.pack()

        # Username
        Label(form, text="USERNAME", font=FONT_BODY, bg=BG_DARK, fg=TEXT_DIM).grid(
              row=0, column=0, sticky="w", pady=(0, 4))
        uf = Frame(form, bg=ACCENT_CYAN, padx=2, pady=2)
        uf.grid(row=1, column=0, pady=(0, 18))
        user_entry = Entry(uf, font=("Courier New", 20, "bold"), width=18,
                           bg=BG_CARD2, fg=ACCENT_CYAN, insertbackground=ACCENT_CYAN,
                           relief="flat", bd=0, justify="center")
        user_entry.pack(ipady=8, ipadx=8)

        # Password
        Label(form, text="PASSWORD", font=FONT_BODY, bg=BG_DARK, fg=TEXT_DIM).grid(
              row=2, column=0, sticky="w", pady=(0, 4))
        pf = Frame(form, bg=ACCENT_CYAN, padx=2, pady=2)
        pf.grid(row=3, column=0, pady=(0, 8))
        pass_entry = Entry(pf, font=("Courier New", 20, "bold"), width=18,
                           bg=BG_CARD2, fg=ACCENT_CYAN, insertbackground=ACCENT_CYAN,
                           relief="flat", bd=0, justify="center", show="*")
        pass_entry.pack(ipady=8, ipadx=8)

        error_lbl = Label(wrapper, text="", font=FONT_BODY, bg=BG_DARK, fg=ACCENT_PINK)
        error_lbl.pack(pady=(0, 8))

        def attempt_login(*_):
            if (user_entry.get().strip().lower() == self.settings["display_name"].lower()
                    and pass_entry.get() == self.settings["password"]):
                self.show_dashboard()
            else:
                error_lbl.config(text="⚠  Invalid username or password.")
                pass_entry.delete(0, "end")
                pass_entry.focus()

        pass_entry.bind("<Return>", attempt_login)
        user_entry.bind("<Return>", lambda _: pass_entry.focus())
        self.glow_btn(wrapper, "LOGIN", attempt_login, color=ACCENT_CYAN, width=18).pack(pady=4)
        user_entry.focus()

    # ─── DASHBOARD ────────────────────────────────────────────
    _WMO = {
        0:"Clear Sky ☀️", 1:"Mainly Clear 🌤️", 2:"Partly Cloudy ⛅",
        3:"Overcast ☁️", 45:"Foggy 🌫️", 48:"Icy Fog 🌫️",
        51:"Light Drizzle 🌦️", 53:"Drizzle 🌦️", 55:"Heavy Drizzle 🌧️",
        61:"Light Rain 🌧️", 63:"Rain 🌧️", 65:"Heavy Rain 🌧️",
        71:"Light Snow ❄️", 73:"Snow ❄️", 75:"Heavy Snow ❄️",
        80:"Showers 🌦️", 81:"Showers 🌦️", 82:"Violent Showers 🌧️",
        95:"Thunderstorm ⛈️", 96:"Thunderstorm ⛈️", 99:"Thunderstorm ⛈️",
    }

    def show_dashboard(self):
        import urllib.request
        import xml.etree.ElementTree as ET

        self.clear()
        self._dash_after_ids = []

        bg_canvas = Canvas(self.root, bg=BG_DARK, highlightthickness=0)
        bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        self._draw_grid(bg_canvas)

        # ── top bar ──────────────────────────────────────────
        top = Frame(self.root, bg=BG_DARK)
        top.pack(fill="x", padx=40, pady=(14, 0))
        Label(top, text=f"◈  {self.settings['display_name'].upper()}'S HUB  ◈",
              font=("Courier New", 26, "bold"),
              bg=BG_DARK, fg=ACCENT_CYAN).pack(side="left")
        self.small_btn(top, "⚙  SETTINGS", self.show_settings,
                       TEXT_DIM).pack(side="right", padx=(6, 0))
        self.small_btn(top, "⏻  LOGOUT", self.show_login,
                       ACCENT_PINK).pack(side="right", padx=(6, 0))
        clock_lbl = Label(top, text="", font=("Courier New", 16, "bold"),
                          bg=BG_DARK, fg=TEXT_DIM)
        clock_lbl.pack(side="right", padx=(0, 12))
        self.divider(self.root, ACCENT_CYAN).pack(fill="x", padx=40, pady=(6, 0))

        def tick():
            now = datetime.datetime.now()
            clock_lbl.config(text=now.strftime("%A  %d %B %Y   %H:%M:%S"))
            aid = self.root.after(1000, tick)
            self._dash_after_ids.append(aid)
        tick()

        # ── top row: weather + system stats (col 0) + news (col 1) + quote/fact (col 2) ──
        top_row = Frame(self.root, bg=BG_DARK)
        top_row.pack(fill="x", padx=40, pady=(10, 0))
        top_row.columnconfigure(0, weight=1)
        top_row.columnconfigure(1, weight=2)
        top_row.columnconfigure(2, weight=2)
        top_row.rowconfigure(0, weight=1)
        top_row.rowconfigure(1, weight=1)

        # ── WEATHER CARD ─────────────────────────────────────
        w_card = Frame(top_row, bg=BG_CARD,
                       highlightbackground=ACCENT_CYAN, highlightthickness=2,
                       padx=24, pady=16)
        w_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        Label(w_card, text="🌍  WEATHER", font=("Courier New", 13, "bold"),
              bg=BG_CARD, fg=TEXT_DIM).pack(anchor="w")
        self.divider(w_card, ACCENT_CYAN).pack(fill="x", pady=(4, 10))
        city_lbl = Label(w_card, text="Detecting location…",
                         font=("Courier New", 13), bg=BG_CARD, fg=TEXT_DIM)
        city_lbl.pack(anchor="w")
        temp_lbl = Label(w_card, text="--°C",
                         font=("Courier New", 48, "bold"),
                         bg=BG_CARD, fg=ACCENT_CYAN)
        temp_lbl.pack(anchor="w", pady=(4, 0))
        cond_lbl = Label(w_card, text="", font=("Courier New", 14),
                         bg=BG_CARD, fg=TEXT_PRIMARY)
        cond_lbl.pack(anchor="w")
        detail_lbl = Label(w_card, text="", font=("Courier New", 12),
                           bg=BG_CARD, fg=TEXT_DIM)
        detail_lbl.pack(anchor="w", pady=(6, 0))
        updated_lbl = Label(w_card, text="", font=("Courier New", 10),
                            bg=BG_CARD, fg=TEXT_DIM)
        updated_lbl.pack(anchor="w", pady=(8, 0))

        def fetch_weather():
            if not REQUESTS_OK:
                self.root.after(0, lambda: city_lbl.config(
                    text="requests not installed", fg=ACCENT_PINK))
                return
            try:
                geo = requests.get("http://ip-api.com/json/", timeout=5).json()
                lat, lon = geo["lat"], geo["lon"]
                city = geo.get("city", "Unknown")
                url = (f"https://api.open-meteo.com/v1/forecast"
                       f"?latitude={lat}&longitude={lon}"
                       f"&current=temperature_2m,apparent_temperature,"
                       f"weather_code,wind_speed_10m,relative_humidity_2m"
                       f"&wind_speed_unit=mph&temperature_unit=celsius")
                w = requests.get(url, timeout=5).json()["current"]
                temp  = round(w["temperature_2m"])
                feels = round(w["apparent_temperature"])
                code  = w["weather_code"]
                wind  = round(w["wind_speed_10m"])
                hum   = w["relative_humidity_2m"]
                cond  = self._WMO.get(code, "Unknown")
                now   = datetime.datetime.now().strftime("%H:%M")
                def apply():
                    city_lbl.config(text=f"📍 {city}", fg=TEXT_PRIMARY)
                    temp_lbl.config(text=f"{temp}°C")
                    cond_lbl.config(text=cond)
                    detail_lbl.config(
                        text=f"Feels like {feels}°C   💨 {wind} mph   💧 {hum}%")
                    updated_lbl.config(text=f"Last updated {now}")
                self.root.after(0, apply)
            except Exception:
                self.root.after(0, lambda: city_lbl.config(
                    text="Weather unavailable", fg=ACCENT_PINK))

        def schedule_weather():
            threading.Thread(target=fetch_weather, daemon=True).start()
            aid = self.root.after(600_000, schedule_weather)
            self._dash_after_ids.append(aid)
        schedule_weather()

        # ── SYSTEM STATS CARD ────────────────────────────────
        sys_card = Frame(top_row, bg=BG_CARD,
                         highlightbackground=ACCENT_GREEN, highlightthickness=2,
                         padx=24, pady=12)
        sys_card.grid(row=1, column=0, sticky="nsew", padx=(0, 10), pady=(8, 0))

        Label(sys_card, text="🖥  SYSTEM", font=("Courier New", 13, "bold"),
              bg=BG_CARD, fg=TEXT_DIM).pack(anchor="w")
        self.divider(sys_card, ACCENT_GREEN).pack(fill="x", pady=(4, 10))

        stats_grid = Frame(sys_card, bg=BG_CARD)
        stats_grid.pack(fill="x")
        stats_grid.columnconfigure(0, weight=1)
        stats_grid.columnconfigure(1, weight=1)
        stats_grid.columnconfigure(2, weight=1)
        stats_grid.columnconfigure(3, weight=1)

        def _stat_col(parent, col, label, color):
            f = Frame(parent, bg=BG_CARD)
            f.grid(row=0, column=col, sticky="nsew", padx=4)
            Label(f, text=label, font=("Courier New", 9, "bold"),
                  bg=BG_CARD, fg=TEXT_DIM).pack()
            val = Label(f, text="--", font=("Courier New", 20, "bold"),
                        bg=BG_CARD, fg=color)
            val.pack()
            return val

        cpu_val  = _stat_col(stats_grid, 0, "CPU",   ACCENT_GREEN)
        freq_val = _stat_col(stats_grid, 1, "FREQ",  ACCENT_TEAL)
        ram_val  = _stat_col(stats_grid, 2, "RAM",   ACCENT_PURPLE)
        disk_val = _stat_col(stats_grid, 3, "DISK",  ACCENT_ORANGE)

        sys_updated = Label(sys_card, text="", font=("Courier New", 10),
                            bg=BG_CARD, fg=TEXT_DIM)
        sys_updated.pack(anchor="w", pady=(8, 0))

        def fetch_sys_stats():
            import psutil
            cpu_pct  = psutil.cpu_percent(interval=1)
            freq     = psutil.cpu_freq()
            ram      = psutil.virtual_memory()
            disk     = psutil.disk_usage("C:\\")
            now = datetime.datetime.now().strftime("%H:%M:%S")
            def apply():
                cpu_val.config(text=f"{cpu_pct:.0f}%")
                freq_val.config(text=f"{freq.current/1000:.1f}G" if freq else "--")
                ram_val.config(text=f"{ram.percent:.0f}%")
                disk_val.config(
                    text=f"{disk.percent:.0f}%",
                    fg=ACCENT_PINK if disk.percent >= 90 else ACCENT_ORANGE)
                sys_updated.config(text=f"C:\\  {disk.used/1024**3:.0f} / {disk.total/1024**3:.0f} GB  ·  Updated {now}")
            self.root.after(0, apply)

        def schedule_sys():
            threading.Thread(target=fetch_sys_stats, daemon=True).start()
            aid = self.root.after(3_000, schedule_sys)
            self._dash_after_ids.append(aid)
        schedule_sys()

        # ── NEWS CARD ────────────────────────────────────────
        news_card = Frame(top_row, bg=BG_CARD,
                          highlightbackground=ACCENT_ORANGE, highlightthickness=2,
                          padx=20, pady=16)
        news_card.grid(row=0, column=1, rowspan=2, sticky="nsew")

        Label(news_card, text="📰  UK NEWS", font=("Courier New", 13, "bold"),
              bg=BG_CARD, fg=TEXT_DIM).pack(anchor="w")
        self.divider(news_card, ACCENT_ORANGE).pack(fill="x", pady=(4, 10))
        news_inner = Frame(news_card, bg=BG_CARD)
        news_inner.pack(fill="both", expand=True)
        news_status = Label(news_inner, text="Loading headlines…",
                            font=FONT_BODY, bg=BG_CARD, fg=TEXT_DIM)
        news_status.pack(anchor="w")
        news_updated = Label(news_card, text="", font=("Courier New", 10),
                             bg=BG_CARD, fg=TEXT_DIM)
        news_updated.pack(anchor="w", pady=(6, 0))

        def fetch_news():
            try:
                req = urllib.request.Request(
                    "https://feeds.bbci.co.uk/news/england/rss.xml",
                    headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=6) as resp:
                    tree = ET.parse(resp)
                items = tree.getroot().findall("./channel/item")
                headlines = [item.findtext("title", "").strip()
                             for item in items[:6] if item.findtext("title", "").strip()]
                now = datetime.datetime.now().strftime("%H:%M")
                def apply():
                    for w in news_inner.winfo_children():
                        w.destroy()
                    for i, h in enumerate(headlines):
                        row = Frame(news_inner, bg=BG_CARD2,
                                    highlightbackground=ACCENT_ORANGE,
                                    highlightthickness=1)
                        row.pack(fill="x", pady=2)
                        Label(row, text=f"{i+1}.", font=("Courier New", 10, "bold"),
                              bg=BG_CARD2, fg=ACCENT_ORANGE,
                              width=3).pack(side="left", padx=(6, 2), pady=5)
                        Label(row, text=h, font=("Courier New", 10),
                              bg=BG_CARD2, fg=TEXT_PRIMARY,
                              wraplength=500, justify="left",
                              anchor="w").pack(side="left", padx=4, pady=5)
                    news_updated.config(text=f"BBC News · Updated {now}")
                self.root.after(0, apply)
            except Exception:
                self.root.after(0, lambda: news_status.config(
                    text="News unavailable", fg=ACCENT_PINK))

        def schedule_news():
            threading.Thread(target=fetch_news, daemon=True).start()
            aid = self.root.after(900_000, schedule_news)
            self._dash_after_ids.append(aid)
        schedule_news()

        # ── QUOTE card (col 2, row 0) ─────────────────────────
        q_card = Frame(top_row, bg=BG_CARD,
                       highlightbackground=ACCENT_TEAL, highlightthickness=2,
                       padx=20, pady=14)
        q_card.grid(row=0, column=2, sticky="nsew", padx=(8, 0))
        Label(q_card, text="💬  QUOTE OF THE DAY", font=("Courier New", 13, "bold"),
              bg=BG_CARD, fg=TEXT_DIM).pack(anchor="w")
        self.divider(q_card, ACCENT_TEAL).pack(fill="x", pady=(4, 10))
        quote_lbl = Label(q_card, text="Loading…", font=("Courier New", 13, "italic"),
                          bg=BG_CARD, fg=TEXT_PRIMARY, wraplength=380, justify="left")
        quote_lbl.pack(anchor="w", fill="x")
        author_lbl = Label(q_card, text="", font=("Courier New", 11, "bold"),
                           bg=BG_CARD, fg=ACCENT_TEAL)
        author_lbl.pack(anchor="e", pady=(8, 0))

        # ── FACT card (col 2, row 1) ──────────────────────────
        f_card = Frame(top_row, bg=BG_CARD,
                       highlightbackground=ACCENT_PURPLE, highlightthickness=2,
                       padx=20, pady=14)
        f_card.grid(row=1, column=2, sticky="nsew", padx=(8, 0), pady=(8, 0))
        Label(f_card, text="💡  FACT OF THE DAY", font=("Courier New", 13, "bold"),
              bg=BG_CARD, fg=TEXT_DIM).pack(anchor="w")
        self.divider(f_card, ACCENT_PURPLE).pack(fill="x", pady=(4, 10))
        fact_lbl = Label(f_card, text="Loading…", font=("Courier New", 13),
                         bg=BG_CARD, fg=TEXT_PRIMARY, wraplength=380, justify="left")
        fact_lbl.pack(anchor="w", fill="x")
        fact_src_lbl = Label(f_card, text="", font=("Courier New", 10),
                             bg=BG_CARD, fg=TEXT_DIM)
        fact_src_lbl.pack(anchor="e", pady=(8, 0))

        def fetch_quote_fact():
            if not REQUESTS_OK:
                self.root.after(0, lambda: quote_lbl.config(
                    text="Install 'requests' to enable this card.", fg=ACCENT_PINK))
                self.root.after(0, lambda: fact_lbl.config(
                    text="Install 'requests' to enable this card.", fg=ACCENT_PINK))
                return
            cache = self._load_daily_cache()

            if "quote" in cache:
                q_text   = cache["quote"]
                q_author = cache.get("author", "")
            else:
                try:
                    data     = requests.get(
                        "https://zenquotes.io/api/today", timeout=6).json()
                    q_text   = data[0]["q"]
                    q_author = data[0]["a"]
                    cache["quote"]  = q_text
                    cache["author"] = q_author
                    self._save_daily_cache(cache)
                except Exception:
                    q_text   = "Could not load quote."
                    q_author = ""

            if "fact" in cache:
                f_text = cache["fact"]
                f_src  = cache.get("fact_src", "")
            else:
                try:
                    data   = requests.get(
                        "https://uselessfacts.jsph.pl/api/v2/facts/today",
                        timeout=6).json()
                    f_text = data["text"]
                    f_src  = data.get("source", "")
                    cache["fact"]     = f_text
                    cache["fact_src"] = f_src
                    self._save_daily_cache(cache)
                except Exception:
                    f_text = "Could not load fact."
                    f_src  = ""

            def apply():
                quote_lbl.config(text=f'"{q_text}"')
                author_lbl.config(
                    text=f"— {q_author}" if q_author else "")
                fact_lbl.config(text=f_text)
                fact_src_lbl.config(text=f_src)
            self.root.after(0, apply)

        threading.Thread(target=fetch_quote_fact, daemon=True).start()

        # ── YEAR CALENDAR ────────────────────────────────────
        today = datetime.date.today()

        cal_outer = Frame(self.root, bg=BG_CARD,
                          highlightbackground=ACCENT_PURPLE, highlightthickness=2)
        cal_outer.pack(fill="both", expand=True, padx=40, pady=(10, 0))

        # header row with year navigator
        cal_header = Frame(cal_outer, bg=BG_CARD, pady=8)
        cal_header.pack(fill="x", padx=16)
        view_year = [today.year]
        year_lbl = Label(cal_header, text=str(today.year),
                         font=("Courier New", 15, "bold"),
                         bg=BG_CARD, fg=ACCENT_PURPLE)
        year_lbl.pack(side="left", expand=True)
        Label(cal_header, text="📅  CALENDAR", font=("Courier New", 13, "bold"),
              bg=BG_CARD, fg=TEXT_DIM).pack(side="left", expand=True)
        Button(cal_header, text="◀", font=("Courier New", 12, "bold"),
               bg=BG_CARD, fg=ACCENT_PURPLE, relief="flat", bd=0,
               activebackground=BG_CARD2, cursor="hand2",
               command=lambda: change_year(-1)).pack(side="right", padx=4)
        Button(cal_header, text="▶", font=("Courier New", 12, "bold"),
               bg=BG_CARD, fg=ACCENT_PURPLE, relief="flat", bd=0,
               activebackground=BG_CARD2, cursor="hand2",
               command=lambda: change_year(1)).pack(side="right", padx=4)
        self.divider(cal_outer, ACCENT_PURPLE).pack(fill="x", padx=16)

        months_frame = Frame(cal_outer, bg=BG_CARD)
        months_frame.pack(fill="both", expand=True, padx=10, pady=8)
        for c in range(4):
            months_frame.columnconfigure(c, weight=1)
        for r in range(3):
            months_frame.rowconfigure(r, weight=1)

        DAY_FONT  = ("Courier New", 9)
        DAY_FONTB = ("Courier New", 9, "bold")
        HDR_FONT  = ("Courier New", 10, "bold")

        # store all day label widgets: month_cells[m] = list of 42 labels
        month_cells = {}

        def build_months():
            for w in months_frame.winfo_children():
                w.destroy()
            month_cells.clear()
            y = view_year[0]
            year_lbl.config(text=str(y))
            for m in range(1, 13):
                row_idx = (m - 1) // 4
                col_idx = (m - 1) % 4
                mf = Frame(months_frame, bg=BG_CARD2,
                           highlightbackground=ACCENT_PURPLE,
                           highlightthickness=1, padx=6, pady=6)
                mf.grid(row=row_idx, column=col_idx, sticky="nsew",
                        padx=4, pady=4)

                mname = datetime.date(y, m, 1).strftime("%B").upper()
                is_cur = (m == today.month and y == today.year)
                Label(mf, text=mname, font=HDR_FONT, bg=BG_CARD2,
                      fg=ACCENT_CYAN if is_cur else ACCENT_PURPLE).pack()

                grid_f = Frame(mf, bg=BG_CARD2)
                grid_f.pack()

                for col, d in enumerate(["M","T","W","T","F","S","S"]):
                    Label(grid_f, text=d, font=("Courier New", 8, "bold"),
                          bg=BG_CARD2,
                          fg=ACCENT_PINK if col >= 5 else TEXT_DIM,
                          width=2).grid(row=0, column=col)

                mat = calendar.monthcalendar(y, m)
                while len(mat) < 6:
                    mat.append([0] * 7)

                cells = []
                for r2, week in enumerate(mat):
                    for c2, day in enumerate(week):
                        is_today = (day == today.day and
                                    m == today.month and y == today.year)
                        is_wknd  = c2 >= 5
                        txt  = str(day) if day else ""
                        fg   = BG_DARK if is_today else (
                               ACCENT_PINK if is_wknd else TEXT_PRIMARY)
                        bg   = ACCENT_CYAN if is_today else BG_CARD2
                        font = DAY_FONTB if is_today else DAY_FONT
                        lbl  = Label(grid_f, text=txt, font=font,
                                     bg=bg, fg=fg, width=2)
                        lbl.grid(row=r2 + 1, column=c2)
                        cells.append(lbl)
                month_cells[m] = cells

        def change_year(delta):
            view_year[0] += delta
            build_months()

        build_months()

        # ── NAV CARDS ────────────────────────────────────────
        nav_row = Frame(self.root, bg=BG_DARK)
        nav_row.pack(pady=(8, 10))

        nav_items = [
            ("🎮", "GAME HUB",   "Snake, Wordle & more",  ACCENT_GREEN,  self.show_home),
            ("📚", "UNIVERSITY", "Notes & assignments",    ACCENT_YELLOW, self.show_university),
            ("✅", "TO-DO LIST", "Tasks & reminders",      ACCENT_TEAL,   None),
        ]

        for icon, title, desc, color, cmd in nav_items:
            card = Frame(nav_row, bg=BG_CARD2, padx=18, pady=10,
                         highlightbackground=color, highlightthickness=2,
                         cursor="hand2" if cmd else "arrow")
            card.pack(side="left", padx=8)
            Label(card, text=icon, font=("Segoe UI Emoji", 20),
                  bg=BG_CARD2, fg=color).pack()
            Label(card, text=title, font=("Courier New", 11, "bold"),
                  bg=BG_CARD2, fg=color).pack(pady=(4, 2))
            Label(card, text=desc, font=("Courier New", 9),
                  bg=BG_CARD2, fg=TEXT_DIM).pack()
            if cmd:
                lbl2 = Label(card, text="▶  OPEN", font=("Courier New", 9, "bold"),
                             bg=BG_CARD2, fg=color, cursor="hand2")
                lbl2.pack(pady=(4, 0))
                for w in (card, lbl2):
                    w.bind("<Button-1>", lambda e, c=cmd: c())
            else:
                Label(card, text="COMING SOON", font=("Courier New", 9),
                      bg=BG_CARD2, fg=TEXT_DIM).pack(pady=(4, 0))

    # ─── HOME SCREEN ──────────────────────────────────────────
    def show_home(self):
        self.clear()

        bg_canvas = Canvas(self.root, bg=BG_DARK, highlightthickness=0)
        bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        self._draw_grid(bg_canvas)

        wrapper = Frame(self.root, bg=BG_DARK)
        wrapper.place(relx=0.5, rely=0.5, anchor="center")

        top_bar = Frame(wrapper, bg=BG_DARK)
        top_bar.pack(fill="x", pady=(0, 6))
        Label(top_bar, text=f"◈  {self.settings['display_name'].upper()}'S GAME HUB  ◈",
              font=FONT_TITLE, bg=BG_DARK, fg=ACCENT_CYAN).pack(side="left")
        self.small_btn(top_bar, "⌂  DASHBOARD", self.show_dashboard,
                       TEXT_DIM).pack(side="right", pady=10)
        self.divider(wrapper, ACCENT_CYAN).pack(fill="x", pady=4)
        Label(wrapper, text="S E L E C T   Y O U R   G A M E",
              font=FONT_SUBTITLE, bg=BG_DARK, fg=TEXT_DIM).pack(pady=(4, 20))

        games = [
            ("🐍", "SNAKE",         "Arrow keys / WASD",  ACCENT_GREEN,  self.show_snake_menu),
            ("✕○", "TIC TAC TOE",   "2-player strategy",  ACCENT_PINK,   self.start_tictactoe),
            ("🎯", "NUMBER GUESS",  "Guess 1 – 100",       ACCENT_PURPLE, self.start_number_game),
            ("✊", "ROCK PAPER",    "vs the computer",     ACCENT_ORANGE, self.start_rps),
            ("🪝", "HANGMAN",       "Guess the word",      ACCENT_TEAL,   self.start_hangman),
            ("🟩", "WORDLE",        "5 letters · 6 tries", ACCENT_YELLOW, self.start_wordle),
            ("🔴", "CONNECT FOUR",  "4 in a row wins",     ACCENT_CYAN,   self.start_connect4),
        ]

        row1 = Frame(wrapper, bg=BG_DARK)
        row1.pack()
        row2 = Frame(wrapper, bg=BG_DARK)
        row2.pack(pady=(14, 0))

        for i, (icon, title, desc, color, cmd) in enumerate(games):
            parent = row1 if i < 4 else row2
            self._game_card(parent, icon, title, desc, color, cmd).pack(
                side="left", padx=10)

    def _draw_grid(self, canvas):
        w = self.root.winfo_screenwidth()
        h = self.root.winfo_screenheight()
        for x in range(0, w, 60):
            canvas.create_line(x, 0, x, h, fill="#14141f", width=1)
        for y in range(0, h, 60):
            canvas.create_line(0, y, w, y, fill="#14141f", width=1)

    def _game_card(self, parent, icon, title, desc, color, cmd):
        card = Frame(parent, bg=BG_CARD, padx=20, pady=20,
                     highlightbackground=color, highlightthickness=2)
        Label(card, text=icon, font=("Segoe UI Emoji", 26),
              bg=BG_CARD, fg=color).pack()
        Label(card, text=title, font=("Courier New", 14, "bold"),
              bg=BG_CARD, fg=color).pack(pady=(6, 2))
        Label(card, text=desc, font=("Courier New", 11),
              bg=BG_CARD, fg=TEXT_DIM).pack(pady=(0, 12))
        self.glow_btn(card, "▶  PLAY", cmd, color=color, width=11).pack()

        def on_enter(e):
            card.config(bg=BG_CARD2)
            for c in card.winfo_children():
                try: c.config(bg=BG_CARD2)
                except: pass

        def on_leave(e):
            card.config(bg=BG_CARD)
            for c in card.winfo_children():
                try: c.config(bg=BG_CARD)
                except: pass

        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        for child in card.winfo_children():
            child.bind("<Enter>", on_enter)
            child.bind("<Leave>", on_leave)
        return card

    # ══════════════════════════════════════════════════════════
    # SNAKE
    # ══════════════════════════════════════════════════════════
    def show_snake_menu(self):
        self.clear()
        wrapper = Frame(self.root, bg=BG_DARK)
        wrapper.place(relx=0.5, rely=0.5, anchor="center")
        Label(wrapper, text="🐍  SNAKE", font=FONT_TITLE,
              bg=BG_DARK, fg=ACCENT_GREEN).pack(pady=(0, 8))
        self.divider(wrapper, ACCENT_GREEN).pack(fill="x", pady=4)
        Label(wrapper, text="Use ARROW KEYS or WASD to move",
              font=FONT_SUBTITLE, bg=BG_DARK, fg=TEXT_DIM).pack(pady=16)
        row = Frame(wrapper, bg=BG_DARK)
        row.pack(pady=20)
        self.glow_btn(row, "▶  START GAME", self.start_snake_game,
                      color=ACCENT_GREEN, width=18).pack(side="left", padx=12)
        self.glow_btn(row, "🏆  HIGH SCORES", self.show_snake_scores,
                      color=ACCENT_YELLOW, width=16).pack(side="left", padx=12)
        self.glow_btn(row, "🎮  GAMES", self.show_home,
                      color=TEXT_DIM, width=14).pack(side="left", padx=12)

    def start_snake_game(self):
        self.clear()
        ss = {'score': 0, 'direction': 'down', 'game_active': True}
        self.snake_state = ss

        self.game_header("🐍  SNAKE", ACCENT_GREEN, self.start_snake_game)

        score_row = Frame(self.root, bg=BG_DARK)
        score_row.pack()
        score_lbl = Label(score_row, text="SCORE  0", font=FONT_SCORE,
                          bg=BG_DARK, fg=ACCENT_CYAN)
        score_lbl.pack(side="left", padx=(0, 40))
        _top = self.high_scores.get("snake", [])
        best = (_top[0]["score"] if isinstance(_top[0], dict) else _top[0]) if _top else 0
        best_lbl = Label(score_row, text=f"BEST  {best}", font=FONT_SCORE,
                         bg=BG_DARK, fg=ACCENT_YELLOW)
        best_lbl.pack(side="left")

        canvas_wrap = Frame(self.root, bg=ACCENT_GREEN, padx=3, pady=3)
        canvas_wrap.pack(pady=8)
        game_canvas = Canvas(canvas_wrap, bg=BG_DARK,
                             height=GAME_HEIGHT, width=GAME_WIDTH,
                             highlightthickness=0)
        game_canvas.pack()

        def spawn_food():
            x = random.randint(0, GAME_WIDTH  // SPACE_SIZE - 1) * SPACE_SIZE
            y = random.randint(0, GAME_HEIGHT // SPACE_SIZE - 1) * SPACE_SIZE
            game_canvas.create_oval(x+2, y+2, x+SPACE_SIZE-2, y+SPACE_SIZE-2,
                                    fill=ACCENT_PINK, outline=ACCENT_PINK,
                                    width=2, tag="food")
            return [x, y]

        coords = [[0, 0]] * BODY_PARTS
        squares = []
        for x, y in coords:
            sq = game_canvas.create_rectangle(
                x+1, y+1, x+SPACE_SIZE-1, y+SPACE_SIZE-1,
                fill=ACCENT_GREEN, outline=BG_DARK, width=1)
            squares.append(sq)
        snake_coords = list(coords)
        snake_squares = squares

        ss['food_coords'] = spawn_food()

        def change_dir(nd):
            opposites = {'left':'right','right':'left','up':'down','down':'up'}
            if nd != opposites.get(ss['direction']):
                ss['direction'] = nd

        def next_turn():
            if not ss['game_active']:
                return
            x, y = snake_coords[0]
            d = ss['direction']
            if d == 'up':     y -= SPACE_SIZE
            elif d == 'down': y += SPACE_SIZE
            elif d == 'left': x -= SPACE_SIZE
            elif d == 'right':x += SPACE_SIZE

            snake_coords.insert(0, [x, y])
            sq = game_canvas.create_rectangle(
                x+1, y+1, x+SPACE_SIZE-1, y+SPACE_SIZE-1,
                fill=ACCENT_GREEN, outline=BG_DARK, width=1)
            snake_squares.insert(0, sq)

            if [x, y] == ss['food_coords']:
                ss['score'] += 1
                score_lbl.config(text=f"SCORE  {ss['score']}")
                game_canvas.delete("food")
                ss['food_coords'] = spawn_food()
            else:
                del snake_coords[-1]
                game_canvas.delete(snake_squares[-1])
                del snake_squares[-1]

            if (x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT or
                    [x, y] in snake_coords[1:]):
                ss['game_active'] = False
                final_score = ss['score']
                rank = self._check_rank("snake", final_score)

                game_canvas.delete("all")
                cx, cy = GAME_WIDTH // 2, GAME_HEIGHT // 2
                game_canvas.create_text(cx, cy - 50, text="GAME OVER",
                                        font=("Courier New", 50, "bold"),
                                        fill=ACCENT_PINK)
                game_canvas.create_text(cx, cy + 10,
                                        text=f"FINAL SCORE: {final_score}",
                                        font=("Courier New", 22),
                                        fill=ACCENT_CYAN)

                def finish(name=""):
                    saved_rank = self._add_score("snake", final_score, name)
                    top = self.high_scores["snake"]
                    new_best = top[0]["score"] if isinstance(top[0], dict) else top[0]
                    best_lbl.config(text=f"BEST  {new_best}")
                    rank_colors = {1: ACCENT_YELLOW, 2: "#c8c8c8", 3: "#cd7f32"}
                    if saved_rank == 1:
                        record_text  = "★  NEW RECORD!  ★"
                        record_color = ACCENT_YELLOW
                    elif saved_rank in (2, 3):
                        record_text  = f"#{saved_rank} ALL TIME"
                        record_color = rank_colors[saved_rank]
                    elif saved_rank is not None:
                        record_text  = f"#{saved_rank} ALL TIME"
                        record_color = ACCENT_GREEN
                    else:
                        record_text  = f"BEST: {new_best}"
                        record_color = TEXT_DIM
                    game_canvas.create_text(cx, cy + 50, text=record_text,
                                            font=("Courier New", 18, "bold"),
                                            fill=record_color)

                if rank is not None and rank <= 3:
                    self._prompt_name(final_score, rank, finish)
                else:
                    finish()
            else:
                self.root.after(self.snake_speed, next_turn)

        binds = {'<Left>':'left','<Right>':'right','<Up>':'up','<Down>':'down',
                 'a':'left','d':'right','w':'up','s':'down'}
        for key, nd in binds.items():
            self.root.bind(key, lambda e, d=nd: change_dir(d))

        next_turn()

    # ══════════════════════════════════════════════════════════
    # TIC TAC TOE
    # ══════════════════════════════════════════════════════════
    def start_tictactoe(self):
        self.clear()
        gs = {'player': random.choice(["X","O"]), 'over': False}
        grid = [[None]*3 for _ in range(3)]

        self.game_header("✕○  TIC TAC TOE", ACCENT_PINK, self.start_tictactoe)

        wrapper = Frame(self.root, bg=BG_DARK)
        wrapper.pack(expand=True)

        turn_color = lambda p: ACCENT_CYAN if p == "X" else ACCENT_PINK
        turn_lbl = Label(wrapper, text=f"PLAYER  {gs['player']}  TURN",
                         font=FONT_SCORE, bg=BG_DARK, fg=turn_color(gs['player']))
        turn_lbl.pack(pady=12)

        board_frame = Frame(wrapper, bg=ACCENT_PURPLE, padx=3, pady=3)
        board_frame.pack()

        def highlight_win(cells, color):
            for (r, c) in cells:
                grid[r][c].config(bg=color, fg=BG_DARK)

        def check_winner():
            lines = (
                [(0,0),(0,1),(0,2)],[(1,0),(1,1),(1,2)],[(2,0),(2,1),(2,2)],
                [(0,0),(1,0),(2,0)],[(0,1),(1,1),(2,1)],[(0,2),(1,2),(2,2)],
                [(0,0),(1,1),(2,2)],[(0,2),(1,1),(2,0)],
            )
            for line in lines:
                texts = [grid[r][c]['text'] for r, c in line]
                if texts[0] == texts[1] == texts[2] != "":
                    highlight_win(line, turn_color(texts[0]))
                    return True
            return False

        def click(r, c):
            if grid[r][c]['text'] != "" or gs['over']:
                return
            p = gs['player']
            col = ACCENT_CYAN if p == "X" else ACCENT_PINK
            grid[r][c].config(text=p, fg=col)
            if check_winner():
                turn_lbl.config(text=f"PLAYER  {p}  WINS! 🏆", fg=col)
                gs['over'] = True
            elif all(grid[r][c]['text'] != "" for r in range(3) for c in range(3)):
                turn_lbl.config(text="IT'S A DRAW!", fg=ACCENT_PURPLE)
                gs['over'] = True
            else:
                gs['player'] = "O" if p == "X" else "X"
                turn_lbl.config(text=f"PLAYER  {gs['player']}  TURN",
                                fg=turn_color(gs['player']))

        inner = Frame(board_frame, bg=BG_DARK)
        inner.pack()
        for r in range(3):
            for c in range(3):
                t = Label(inner, text="", font=("Courier New", 44, "bold"),
                          width=3, height=1, bg=BG_CARD2, fg=TEXT_PRIMARY,
                          relief="flat", highlightbackground=ACCENT_PURPLE,
                          highlightthickness=1, cursor="hand2")
                t.grid(row=r, column=c, padx=2, pady=2, ipadx=10, ipady=10)
                t.bind("<Button-1>", lambda e, row=r, col=c: click(row, col))
                grid[r][c] = t

    # ══════════════════════════════════════════════════════════
    # NUMBER GUESSING
    # ══════════════════════════════════════════════════════════
    def start_number_game(self):
        self.clear()
        gs = {'number': random.randint(1, 100), 'attempts': 0, 'over': False}

        self.game_header("🎯  NUMBER GUESS", ACCENT_PURPLE, self.start_number_game)

        wrapper = Frame(self.root, bg=BG_DARK)
        wrapper.pack(expand=True)

        Label(wrapper, text="I have a number between 1 and 100.",
              font=FONT_SUBTITLE, bg=BG_DARK, fg=TEXT_DIM).pack(pady=8)

        display_lbl = Label(wrapper, text="?", font=("Courier New", 80, "bold"),
                            bg=BG_DARK, fg=ACCENT_PURPLE)
        display_lbl.pack()

        msg_lbl = Label(wrapper, text="Enter your guess below",
                        font=FONT_SUBTITLE, bg=BG_DARK, fg=TEXT_DIM)
        msg_lbl.pack(pady=8)

        entry_frame = Frame(wrapper, bg=ACCENT_PURPLE, padx=2, pady=2)
        entry_frame.pack(pady=10)
        entry = Entry(entry_frame, font=("Courier New", 28, "bold"),
                      width=8, bg=BG_CARD2, fg=ACCENT_CYAN,
                      insertbackground=ACCENT_CYAN, relief="flat",
                      bd=0, justify="center")
        entry.pack(ipady=10, ipadx=10)
        entry.focus()

        attempts_lbl = Label(wrapper, text="ATTEMPTS: 0",
                             font=FONT_BODY, bg=BG_DARK, fg=TEXT_DIM)
        attempts_lbl.pack(pady=4)

        submit_f = [None]

        def submit(*_):
            if gs['over']: return
            try:
                guess = int(entry.get())
                entry.delete(0, "end")
            except ValueError:
                msg_lbl.config(text="⚠  Enter a valid number!", fg=ACCENT_PINK)
                return
            gs['attempts'] += 1
            attempts_lbl.config(text=f"ATTEMPTS: {gs['attempts']}")
            if guess < gs['number']:
                display_lbl.config(text="▲", fg=ACCENT_CYAN)
                msg_lbl.config(text=f"{guess}  →  Too LOW!", fg=ACCENT_CYAN)
            elif guess > gs['number']:
                display_lbl.config(text="▼", fg=ACCENT_PINK)
                msg_lbl.config(text=f"{guess}  →  Too HIGH!", fg=ACCENT_PINK)
            else:
                gs['over'] = True
                display_lbl.config(text=str(gs['number']), fg=ACCENT_GREEN)
                msg_lbl.config(
                    text=f"🎉  Correct in {gs['attempts']} attempt(s)!",
                    fg=ACCENT_GREEN)
                entry.config(state="disabled")
                if submit_f[0]:
                    submit_f[0].pack_forget()

                attempts = gs['attempts']
                btn_row = Frame(wrapper, bg=BG_DARK)
                btn_row.pack(pady=8)
                self.glow_btn(btn_row, "▶  PLAY AGAIN", self.start_number_game,
                              color=ACCENT_PURPLE, width=14).pack(side="left", padx=8)
                self.glow_btn(btn_row, "🏆  HIGH SCORES", self.show_number_scores,
                              color=ACCENT_YELLOW, width=14).pack(side="left", padx=8)

                rank = self._check_rank_asc("number_guess", attempts)
                if rank:
                    def save_score(name, a=attempts):
                        self._add_score_asc("number_guess", a, name)
                    self._prompt_name(attempts, rank, save_score)
                else:
                    self._add_score_asc("number_guess", attempts)

        entry.bind("<Return>", submit)
        submit_f[0] = self.glow_btn(wrapper, "GUESS", submit,
                                    color=ACCENT_PURPLE, width=14)
        submit_f[0].pack(pady=6)

    # ══════════════════════════════════════════════════════════
    # ROCK PAPER SCISSORS
    # ══════════════════════════════════════════════════════════
    def start_rps(self):
        self.clear()
        gs = {'player_score': 0, 'cpu_score': 0}

        self.game_header("✊  ROCK PAPER SCISSORS", ACCENT_ORANGE, self.start_rps)

        wrapper = Frame(self.root, bg=BG_DARK)
        wrapper.pack(expand=True)

        # Score board
        score_frame = Frame(wrapper, bg=BG_CARD2,
                            highlightbackground=ACCENT_ORANGE,
                            highlightthickness=2, padx=40, pady=16)
        score_frame.pack(pady=8)
        Label(score_frame, text="YOU", font=("Courier New", 14, "bold"),
              bg=BG_CARD2, fg=ACCENT_CYAN).grid(row=0, column=0, padx=30)
        Label(score_frame, text="VS", font=("Courier New", 14),
              bg=BG_CARD2, fg=TEXT_DIM).grid(row=0, column=1, padx=20)
        Label(score_frame, text="CPU", font=("Courier New", 14, "bold"),
              bg=BG_CARD2, fg=ACCENT_PINK).grid(row=0, column=2, padx=30)
        player_score_lbl = Label(score_frame, text="0",
                                  font=("Courier New", 40, "bold"),
                                  bg=BG_CARD2, fg=ACCENT_CYAN)
        player_score_lbl.grid(row=1, column=0)
        Label(score_frame, text="—", font=("Courier New", 40),
              bg=BG_CARD2, fg=TEXT_DIM).grid(row=1, column=1)
        cpu_score_lbl = Label(score_frame, text="0",
                               font=("Courier New", 40, "bold"),
                               bg=BG_CARD2, fg=ACCENT_PINK)
        cpu_score_lbl.grid(row=1, column=2)

        # Arena
        arena = Frame(wrapper, bg=BG_DARK)
        arena.pack(pady=16)
        player_icon = Label(arena, text="?", font=("Courier New", 64, "bold"),
                            bg=BG_DARK, fg=ACCENT_CYAN, width=4)
        player_icon.grid(row=0, column=0, padx=30)
        Label(arena, text="VS", font=("Courier New", 24),
              bg=BG_DARK, fg=TEXT_DIM).grid(row=0, column=1)
        cpu_icon = Label(arena, text="?", font=("Courier New", 64, "bold"),
                         bg=BG_DARK, fg=ACCENT_PINK, width=4)
        cpu_icon.grid(row=0, column=2, padx=30)

        result_lbl = Label(wrapper, text="Choose your move!",
                           font=("Courier New", 20, "bold"),
                           bg=BG_DARK, fg=TEXT_DIM)
        result_lbl.pack(pady=8)

        icons_map = {"ROCK": "✊", "PAPER": "✋", "SCISSORS": "✌"}
        beats     = {"ROCK": "SCISSORS", "PAPER": "ROCK", "SCISSORS": "PAPER"}

        def play(choice):
            cpu = random.choice(["ROCK", "PAPER", "SCISSORS"])
            player_icon.config(text=icons_map[choice])
            cpu_icon.config(text=icons_map[cpu])
            if choice == cpu:
                result_lbl.config(text="DRAW!", fg=ACCENT_YELLOW)
            elif beats[choice] == cpu:
                gs['player_score'] += 1
                player_score_lbl.config(text=str(gs['player_score']))
                result_lbl.config(
                    text=f"YOU WIN!  {choice} beats {cpu}", fg=ACCENT_GREEN)
            else:
                gs['cpu_score'] += 1
                cpu_score_lbl.config(text=str(gs['cpu_score']))
                result_lbl.config(
                    text=f"CPU WINS!  {cpu} beats {choice}", fg=ACCENT_PINK)

        btn_row = Frame(wrapper, bg=BG_DARK)
        btn_row.pack(pady=10)
        for emoji, name in [("✊","ROCK"),("✋","PAPER"),("✌","SCISSORS")]:
            f = Frame(btn_row, bg=ACCENT_ORANGE, padx=2, pady=2)
            f.pack(side="left", padx=12)
            b = Button(f, text=f"{emoji}\n{name}",
                       font=("Courier New", 16, "bold"),
                       bg=BG_CARD2, fg=ACCENT_ORANGE,
                       relief="flat", bd=0, padx=28, pady=18,
                       activebackground=ACCENT_ORANGE, activeforeground=BG_DARK,
                       cursor="hand2", command=lambda n=name: play(n))
            b.pack()
            b.bind("<Enter>", lambda e, btn=b: btn.config(bg=ACCENT_ORANGE, fg=BG_DARK))
            b.bind("<Leave>", lambda e, btn=b: btn.config(bg=BG_CARD2, fg=ACCENT_ORANGE))

    # ══════════════════════════════════════════════════════════
    # HANGMAN
    # ══════════════════════════════════════════════════════════
    def start_hangman(self):
        self.clear()
        word = random.choice(HANGMAN_WORDS)
        gs = {'word': word, 'guessed': set(), 'wrong': 0, 'max_wrong': 6, 'over': False}

        self.game_header("🪝  HANGMAN", ACCENT_TEAL, self.start_hangman)

        main = Frame(self.root, bg=BG_DARK)
        main.pack(expand=True, fill="both", padx=30, pady=6)

        # ── Left: gallows ──
        left = Frame(main, bg=BG_DARK)
        left.pack(side="left", padx=20)

        gallows = Canvas(left, width=260, height=280, bg=BG_CARD2,
                         highlightbackground=ACCENT_TEAL, highlightthickness=2)
        gallows.pack()

        def draw_gallows():
            gallows.delete("all")
            c  = ACCENT_TEAL
            dc = ACCENT_PINK
            gallows.create_line(20, 260, 240, 260, fill=c, width=4)
            gallows.create_line(60, 260, 60,  20,  fill=c, width=4)
            gallows.create_line(60, 20,  170, 20,  fill=c, width=4)
            gallows.create_line(170, 20, 170, 48,  fill=c, width=4)
            w = gs['wrong']
            if w >= 1: gallows.create_oval(148, 48, 192, 92, outline=dc, width=3)
            if w >= 2: gallows.create_line(170, 92,  170, 175, fill=dc, width=3)
            if w >= 3: gallows.create_line(170, 115, 130, 150, fill=dc, width=3)
            if w >= 4: gallows.create_line(170, 115, 210, 150, fill=dc, width=3)
            if w >= 5: gallows.create_line(170, 175, 130, 225, fill=dc, width=3)
            if w >= 6: gallows.create_line(170, 175, 210, 225, fill=dc, width=3)

        # ── Right: game area ──
        right = Frame(main, bg=BG_DARK)
        right.pack(side="left", padx=20, fill="both", expand=True)

        wrong_lbl = Label(right, text=f"WRONG: 0 / {gs['max_wrong']}",
                          font=FONT_SCORE, bg=BG_DARK, fg=ACCENT_PINK)
        wrong_lbl.pack(pady=(0, 10))

        # Word letter boxes
        word_frame = Frame(right, bg=BG_DARK)
        word_frame.pack(pady=8)
        letter_labels = []
        for ch in word:
            lf = Frame(word_frame, bg=ACCENT_TEAL, padx=1, pady=1)
            lf.pack(side="left", padx=2)
            lbl = Label(lf, text="_", font=("Courier New", 26, "bold"),
                        bg=BG_CARD2, fg=ACCENT_TEAL, width=2)
            lbl.pack(padx=5, pady=4)
            letter_labels.append(lbl)

        msg_lbl = Label(right, text="Guess a letter!",
                        font=FONT_SUBTITLE, bg=BG_DARK, fg=TEXT_DIM)
        msg_lbl.pack(pady=6)

        alpha_grid = Frame(right, bg=BG_DARK)
        alpha_grid.pack(pady=4)
        alpha_btns = {}

        def guess(letter):
            if gs['over'] or letter in gs['guessed']:
                return
            gs['guessed'].add(letter)
            btn = alpha_btns.get(letter)

            if letter in gs['word']:
                if btn:
                    btn.config(bg=ACCENT_GREEN, fg=BG_DARK, state="disabled",
                               activebackground=ACCENT_GREEN)
                for i, ch in enumerate(gs['word']):
                    if ch == letter:
                        letter_labels[i].config(text=ch, fg=ACCENT_GREEN)
                if all(ch in gs['guessed'] for ch in gs['word']):
                    gs['over'] = True
                    msg_lbl.config(text="🎉  YOU WIN!", fg=ACCENT_GREEN)
            else:
                gs['wrong'] += 1
                if btn:
                    btn.config(bg=ACCENT_PINK, fg=BG_DARK, state="disabled",
                               activebackground=ACCENT_PINK)
                wrong_lbl.config(text=f"WRONG: {gs['wrong']} / {gs['max_wrong']}")
                if gs['wrong'] >= gs['max_wrong']:
                    gs['over'] = True
                    for i, ch in enumerate(gs['word']):
                        letter_labels[i].config(text=ch, fg=ACCENT_PINK)
                    msg_lbl.config(
                        text=f"GAME OVER!  Word: {gs['word']}", fg=ACCENT_PINK)

            draw_gallows()

        for i, letter in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
            f = Frame(alpha_grid, bg=ACCENT_TEAL, padx=1, pady=1)
            f.grid(row=i//13, column=i%13, padx=2, pady=2)
            b = Button(f, text=letter, font=("Courier New", 12, "bold"),
                       bg=BG_CARD2, fg=ACCENT_TEAL,
                       relief="flat", bd=0, padx=6, pady=4,
                       activebackground=ACCENT_TEAL, activeforeground=BG_DARK,
                       cursor="hand2", width=2,
                       command=lambda l=letter: guess(l))
            b.pack()
            b.bind("<Enter>",
                   lambda e, btn=b: btn.config(bg=ACCENT_TEAL, fg=BG_DARK)
                   if str(btn['state']) != 'disabled' else None)
            b.bind("<Leave>",
                   lambda e, btn=b: btn.config(bg=BG_CARD2, fg=ACCENT_TEAL)
                   if str(btn['state']) != 'disabled' else None)
            alpha_btns[letter] = b

        def on_key(event):
            ch = event.char.upper()
            if ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                guess(ch)

        self.root.bind("<Key>", on_key)
        draw_gallows()

    # ══════════════════════════════════════════════════════════
    # WORDLE
    # ══════════════════════════════════════════════════════════
    def start_wordle(self):
        self.clear()
        word = random.choice([w for w in WORDLE_WORDS if len(w) == 5])
        gs = {'word': word, 'row': 0, 'col': 0, 'over': False, 'current': []}

        self.game_header("🟩  WORDLE", ACCENT_YELLOW, self.start_wordle)

        outer = Frame(self.root, bg=BG_DARK)
        outer.pack(expand=True)

        # 6×5 tile grid
        tiles = []
        grid_frame = Frame(outer, bg=BG_DARK)
        grid_frame.pack(pady=8)
        for r in range(6):
            row_tiles = []
            for c in range(5):
                f = Frame(grid_frame, bg=TEXT_DIM, padx=2, pady=2)
                f.grid(row=r, column=c, padx=3, pady=3)
                lbl = Label(f, text="", font=("Courier New", 22, "bold"),
                            width=2, height=1, bg=BG_CARD2, fg=TEXT_PRIMARY,
                            relief="flat")
                lbl.pack(ipady=8, ipadx=6)
                row_tiles.append(lbl)
            tiles.append(row_tiles)

        msg_lbl = Label(outer, text="Type a 5-letter word and press ENTER",
                        font=FONT_BODY, bg=BG_DARK, fg=TEXT_DIM)
        msg_lbl.pack(pady=4)

        # On-screen keyboard
        kb_frame = Frame(outer, bg=BG_DARK)
        kb_frame.pack(pady=4)
        kb_btns = {}

        def type_letter(letter):
            if gs['over'] or gs['col'] >= 5: return
            tiles[gs['row']][gs['col']].config(
                text=letter,
                highlightbackground=ACCENT_YELLOW,
                highlightthickness=1)
            gs['current'].append(letter)
            gs['col'] += 1

        def backspace():
            if gs['col'] > 0 and not gs['over']:
                gs['col'] -= 1
                gs['current'].pop()
                tiles[gs['row']][gs['col']].config(text="")

        def submit_word():
            if gs['col'] != 5 or gs['over']:
                if gs['col'] != 5:
                    msg_lbl.config(text="⚠  Need 5 letters!", fg=ACCENT_PINK)
                return
            guess_word = "".join(gs['current'])
            target = gs['word']

            result = ["absent"] * 5
            counts = {}
            for ch in target:
                counts[ch] = counts.get(ch, 0) + 1

            for i in range(5):
                if guess_word[i] == target[i]:
                    result[i] = "correct"
                    counts[guess_word[i]] -= 1

            for i in range(5):
                if result[i] == "absent" and guess_word[i] in counts and counts[guess_word[i]] > 0:
                    result[i] = "present"
                    counts[guess_word[i]] -= 1

            color_map    = {"correct": ACCENT_GREEN, "present": ACCENT_YELLOW, "absent": BG_CARD2}
            text_map     = {"correct": BG_DARK,      "present": BG_DARK,       "absent": TEXT_DIM}
            kb_color_map = {"correct": ACCENT_GREEN, "present": ACCENT_YELLOW, "absent": "#3a3a50"}
            kb_text_map  = {"correct": BG_DARK,      "present": BG_DARK,       "absent": TEXT_DIM}
            priority     = {"correct": 3, "present": 2, "absent": 1, "fresh": 0}

            for i, status in enumerate(result):
                tiles[gs['row']][i].config(bg=color_map[status], fg=text_map[status])
                letter = guess_word[i]
                if letter in kb_btns:
                    cur_bg = kb_btns[letter]['bg']
                    cur_status = "fresh"
                    if cur_bg == ACCENT_GREEN:    cur_status = "correct"
                    elif cur_bg == ACCENT_YELLOW: cur_status = "present"
                    elif cur_bg == "#3a3a50":     cur_status = "absent"
                    if priority[status] > priority[cur_status]:
                        kb_btns[letter].config(bg=kb_color_map[status],
                                               fg=kb_text_map[status])

            gs['row'] += 1
            gs['col'] = 0
            gs['current'] = []

            if guess_word == target:
                gs['over'] = True
                msg_lbl.config(text=f"🎉  BRILLIANT!  The word was {target}",
                               fg=ACCENT_GREEN)
            elif gs['row'] >= 6:
                gs['over'] = True
                msg_lbl.config(text=f"GAME OVER!  The word was:  {target}",
                               fg=ACCENT_PINK)
            else:
                msg_lbl.config(text=f"Guess {gs['row'] + 1} of 6", fg=TEXT_DIM)

        def on_key(event):
            if gs['over']: return
            key = event.keysym.upper()
            if key == "RETURN":
                submit_word()
            elif key == "BACKSPACE":
                backspace()
            elif len(event.char) == 1 and event.char.upper() in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                type_letter(event.char.upper())

        self.root.bind("<Key>", on_key)

        for row_str in ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]:
            row_f = Frame(kb_frame, bg=BG_DARK)
            row_f.pack(pady=2)
            for letter in row_str:
                f = Frame(row_f, bg=TEXT_DIM, padx=1, pady=1)
                f.pack(side="left", padx=2)
                b = Button(f, text=letter, font=("Courier New", 11, "bold"),
                           bg=BG_CARD2, fg=TEXT_PRIMARY,
                           relief="flat", bd=0, padx=6, pady=5,
                           cursor="hand2", width=2,
                           command=lambda l=letter: type_letter(l))
                b.pack()
                kb_btns[letter] = b

        ctrl_row = Frame(kb_frame, bg=BG_DARK)
        ctrl_row.pack(pady=4)
        self.small_btn(ctrl_row, "ENTER", submit_word,
                       ACCENT_YELLOW).pack(side="left", padx=4)
        self.small_btn(ctrl_row, "⌫  DEL", backspace,
                       ACCENT_PINK).pack(side="left", padx=4)

    # ══════════════════════════════════════════════════════════
    # CONNECT FOUR
    # ══════════════════════════════════════════════════════════
    def start_connect4(self):
        self.clear()
        ROWS, COLS = 6, 7
        board = [[None]*COLS for _ in range(ROWS)]
        gs = {'player': "R", 'over': False}

        self.game_header("🔴  CONNECT FOUR", ACCENT_CYAN, self.start_connect4)

        wrapper = Frame(self.root, bg=BG_DARK)
        wrapper.pack(expand=True)

        player_colors = {"R": ACCENT_PINK,   "Y": ACCENT_YELLOW}
        player_names  = {"R": "🔴 RED",       "Y": "🟡 YELLOW"}

        turn_lbl = Label(wrapper,
                         text=f"{player_names[gs['player']]}  TURN",
                         font=FONT_SCORE, bg=BG_DARK,
                         fg=player_colors[gs['player']])
        turn_lbl.pack(pady=8)

        CELL = 70
        PAD  = 6
        CW   = COLS * CELL + PAD * 2
        CH   = ROWS * CELL + PAD * 2

        board_wrap = Frame(wrapper, bg=ACCENT_CYAN, padx=3, pady=3)
        board_wrap.pack()
        canvas = Canvas(board_wrap, width=CW, height=CH,
                        bg="#0d1b3e", highlightthickness=0)
        canvas.pack()

        hover_col = [None]

        def draw_board():
            canvas.delete("all")
            for r in range(ROWS):
                for c in range(COLS):
                    x1 = PAD + c*CELL + 6
                    y1 = PAD + r*CELL + 6
                    x2 = x1 + CELL - 12
                    y2 = y1 + CELL - 12
                    val  = board[r][c]
                    fill = BG_CARD2 if val is None else player_colors[val]
                    outl = "#1a2a5e" if val is None else fill
                    canvas.create_oval(x1, y1, x2, y2, fill=fill,
                                       outline=outl, width=2)
            if hover_col[0] is not None and not gs['over']:
                hc = hover_col[0]
                canvas.create_rectangle(
                    PAD + hc*CELL, PAD,
                    PAD + hc*CELL + CELL, CH - PAD,
                    outline=player_colors[gs['player']],
                    width=3, dash=(6, 3))

        def check_win(val):
            for r in range(ROWS):
                for c in range(COLS - 3):
                    if all(board[r][c+i] == val for i in range(4)): return True
            for r in range(ROWS - 3):
                for c in range(COLS):
                    if all(board[r+i][c] == val for i in range(4)): return True
            for r in range(ROWS - 3):
                for c in range(COLS - 3):
                    if all(board[r+i][c+i] == val for i in range(4)): return True
            for r in range(ROWS - 3):
                for c in range(3, COLS):
                    if all(board[r+i][c-i] == val for i in range(4)): return True
            return False

        def drop(col):
            if gs['over']: return
            for r in range(ROWS - 1, -1, -1):
                if board[r][col] is None:
                    p = gs['player']
                    board[r][col] = p
                    draw_board()
                    if check_win(p):
                        gs['over'] = True
                        turn_lbl.config(
                            text=f"{player_names[p]}  WINS! 🏆",
                            fg=player_colors[p])
                    elif all(board[0][c] is not None for c in range(COLS)):
                        gs['over'] = True
                        turn_lbl.config(text="IT'S A DRAW!", fg=ACCENT_CYAN)
                    else:
                        gs['player'] = "Y" if p == "R" else "R"
                        turn_lbl.config(
                            text=f"{player_names[gs['player']]}  TURN",
                            fg=player_colors[gs['player']])
                    return

        canvas.bind("<Button-1>",
                    lambda e: drop((e.x - PAD) // CELL)
                    if 0 <= (e.x - PAD) // CELL < COLS else None)

        def on_hover(e):
            col = (e.x - PAD) // CELL
            hover_col[0] = col if 0 <= col < COLS else None
            draw_board()

        canvas.bind("<Motion>", on_hover)
        canvas.bind("<Leave>", lambda e: [hover_col.__setitem__(0, None), draw_board()])

        # Drop buttons under board
        btn_row = Frame(wrapper, bg=BG_DARK)
        btn_row.pack(pady=6)
        for c in range(COLS):
            b = Button(btn_row, text="▼",
                       font=("Courier New", 14, "bold"),
                       bg=BG_CARD2, fg=ACCENT_CYAN,
                       relief="flat", bd=0, padx=0, pady=4,
                       width=4, cursor="hand2",
                       activebackground=ACCENT_CYAN,
                       activeforeground=BG_DARK,
                       command=lambda col=c: drop(col))
            b.pack(side="left", padx=3)
            b.bind("<Enter>",
                   lambda e, btn=b: btn.config(bg=ACCENT_CYAN, fg=BG_DARK))
            b.bind("<Leave>",
                   lambda e, btn=b: btn.config(bg=BG_CARD2, fg=ACCENT_CYAN))

        draw_board()

    # ══════════════════════════════════════════════════════════
    # UNIVERSITY
    # ══════════════════════════════════════════════════════════
    def _load_deadlines(self):
        try:
            with open(UNIVERSITY_FILE, "r") as f:
                return json.load(f).get("deadlines", [])
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_deadlines(self, deadlines):
        try:
            with open(UNIVERSITY_FILE, "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}
        data["deadlines"] = deadlines
        with open(UNIVERSITY_FILE, "w") as f:
            json.dump(data, f)

    def _get_next_class(self):
        """Return (day_name, class_dict) for the next upcoming class, or None."""
        now = datetime.datetime.now()
        today_wd = now.weekday()  # 0=Mon
        day_names = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        for offset in range(7):
            day = day_names[(today_wd + offset) % 7]
            if day not in TIMETABLE:
                continue
            for cls in TIMETABLE[day]:
                if offset == 0:
                    end_h, end_m = map(int, cls["end"].split(":"))
                    cls_end = now.replace(hour=end_h, minute=end_m, second=0, microsecond=0)
                    if now < cls_end:
                        return (day, cls)
                else:
                    return (day, cls)
        return None

    def show_university(self):
        self.clear()

        bg_canvas = Canvas(self.root, bg=BG_DARK, highlightthickness=0)
        bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        self._draw_grid(bg_canvas)

        # ── Header ──
        header = Frame(self.root, bg=BG_DARK, pady=8)
        header.pack(fill="x", padx=40)
        Label(header, text="📚  UNIVERSITY",
              font=("Courier New", 26, "bold"),
              bg=BG_DARK, fg=ACCENT_YELLOW).pack(side="left")
        self.small_btn(header, "🎮  GAMES",    self.show_home,      TEXT_DIM).pack(side="right", padx=(6, 0))
        self.small_btn(header, "⌂  DASHBOARD", self.show_dashboard, TEXT_DIM).pack(side="right", padx=(6, 0))
        self.divider(self.root, ACCENT_YELLOW).pack(fill="x", padx=40, pady=(0, 8))

        # ── Graduation progress bar ──
        today        = datetime.date.today()
        total_days   = (DEGREE_END - DEGREE_START).days
        elapsed_days = (today - DEGREE_START).days
        grad_pct     = max(0.0, min(1.0, elapsed_days / total_days))
        days_to_grad = (DEGREE_END - today).days

        y2_start = datetime.date(2026, 9, 1)
        y3_start = datetime.date(2027, 9, 1)
        current_year = (3 if today >= y3_start else 2 if today >= y2_start else 1)

        grad_card = Frame(self.root, bg=BG_CARD,
                          highlightbackground=ACCENT_YELLOW, highlightthickness=2,
                          padx=20, pady=12)
        grad_card.pack(fill="x", padx=40, pady=(0, 8))

        gr_top = Frame(grad_card, bg=BG_CARD)
        gr_top.pack(fill="x")
        Label(gr_top, text="🎓  DEGREE PROGRESS — 3-Year BSc",
              font=("Courier New", 12, "bold"),
              bg=BG_CARD, fg=ACCENT_YELLOW).pack(side="left")
        Label(gr_top,
              text=f"Year {current_year} of 3  ·  {grad_pct*100:.1f}% complete  ·  {days_to_grad:,} days to graduation",
              font=FONT_BODY, bg=BG_CARD, fg=TEXT_DIM).pack(side="right")

        grad_bar = Canvas(grad_card, height=20, bg=BG_CARD2, highlightthickness=0)
        grad_bar.pack(fill="x", pady=(8, 4))

        def make_grad_draw(c, pct, total):
            y2_frac = (datetime.date(2026, 9, 1) - DEGREE_START).days / total
            y3_frac = (datetime.date(2027, 9, 1) - DEGREE_START).days / total
            def draw(event):
                w = event.width
                c.delete("all")
                c.create_rectangle(0, 0, w, 20, fill=BG_CARD2, outline="")
                c.create_rectangle(0, 0, int(w * pct), 20, fill=ACCENT_YELLOW, outline="")
                for frac, lbl in [(y2_frac, "Y2"), (y3_frac, "Y3")]:
                    x = int(w * frac)
                    c.create_line(x, 0, x, 20, fill=BG_DARK, width=2)
                    c.create_text(x + 14, 10, text=lbl,
                                  font=("Courier New", 8, "bold"), fill=BG_DARK)
            return draw

        grad_bar.bind("<Configure>", make_grad_draw(grad_bar, grad_pct, total_days))

        date_row = Frame(grad_card, bg=BG_CARD)
        date_row.pack(fill="x")
        Label(date_row, text="Sep 2025", font=("Courier New", 9),
              bg=BG_CARD, fg=TEXT_DIM).pack(side="left")
        Label(date_row, text="Jun 2028", font=("Courier New", 9),
              bg=BG_CARD, fg=TEXT_DIM).pack(side="right")

        # ── Main two-column layout ──
        main = Frame(self.root, bg=BG_DARK)
        main.pack(fill="both", expand=True, padx=40, pady=(0, 10))
        main.columnconfigure(0, weight=2)
        main.columnconfigure(1, weight=3)
        main.rowconfigure(0, weight=1)

        # ── LEFT: Timetable ──
        tt_outer = Frame(main, bg=BG_CARD,
                         highlightbackground=ACCENT_CYAN, highlightthickness=2,
                         padx=16, pady=12)
        tt_outer.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        Label(tt_outer, text="🗓  WEEKLY TIMETABLE",
              font=("Courier New", 12, "bold"),
              bg=BG_CARD, fg=ACCENT_CYAN).pack(anchor="w")
        self.divider(tt_outer, ACCENT_CYAN).pack(fill="x", pady=(4, 8))

        next_class = self._get_next_class()
        today_name = today.strftime("%A")

        for day in ["Monday", "Wednesday", "Friday"]:
            is_today  = (day == today_name)
            day_color = ACCENT_CYAN if is_today else TEXT_DIM
            Label(tt_outer, text=day.upper(),
                  font=("Courier New", 10, "bold"),
                  bg=BG_CARD, fg=day_color).pack(anchor="w", pady=(8, 2))

            for cls in TIMETABLE[day]:
                is_next      = (next_class is not None and
                                next_class[0] == day and
                                next_class[1]["start"] == cls["start"])
                mod_color    = MODULE_COLORS.get(cls["module"], ACCENT_CYAN)
                border_color = ACCENT_CYAN if is_next else "#2a2a3a"

                row = Frame(tt_outer, bg=BG_CARD2,
                            highlightbackground=border_color,
                            highlightthickness=2 if is_next else 1)
                row.pack(fill="x", pady=2)

                Frame(row, bg=mod_color, width=4).pack(side="left", fill="y")

                info = Frame(row, bg=BG_CARD2, padx=8, pady=6)
                info.pack(side="left", fill="both", expand=True)
                Label(info, text=f"{cls['start']} – {cls['end']}",
                      font=("Courier New", 10, "bold"),
                      bg=BG_CARD2, fg=mod_color).pack(anchor="w")
                Label(info, text=f"{cls['type']}  ·  {cls['module']}",
                      font=("Courier New", 10, "bold"),
                      bg=BG_CARD2, fg=TEXT_PRIMARY).pack(anchor="w")
                Label(info, text=cls["room"],
                      font=("Courier New", 9),
                      bg=BG_CARD2, fg=TEXT_DIM).pack(anchor="w")

                if is_next:
                    Label(row, text="▶  NEXT",
                          font=("Courier New", 9, "bold"),
                          bg=BG_CARD2, fg=ACCENT_CYAN).pack(side="right", padx=8)

        # ── RIGHT: Deadlines ──
        dl_outer = Frame(main, bg=BG_CARD,
                         highlightbackground=ACCENT_PINK, highlightthickness=2,
                         padx=16, pady=12)
        dl_outer.grid(row=0, column=1, sticky="nsew")

        dl_head = Frame(dl_outer, bg=BG_CARD)
        dl_head.pack(fill="x")
        Label(dl_head, text="📌  DEADLINES",
              font=("Courier New", 12, "bold"),
              bg=BG_CARD, fg=ACCENT_PINK).pack(side="left")

        deadlines = self._load_deadlines()

        self.divider(dl_outer, ACCENT_PINK).pack(fill="x", pady=(4, 6))

        # Scrollable deadlines list
        dl_scroll_wrap = Frame(dl_outer, bg=BG_CARD)
        dl_scroll_wrap.pack(fill="both", expand=True)

        dl_canvas_inner = Canvas(dl_scroll_wrap, bg=BG_CARD, highlightthickness=0)
        dl_scrollbar    = tk.Scrollbar(dl_scroll_wrap, orient="vertical",
                                       command=dl_canvas_inner.yview)
        dl_canvas_inner.configure(yscrollcommand=dl_scrollbar.set)
        dl_scrollbar.pack(side="right", fill="y")
        dl_canvas_inner.pack(side="left", fill="both", expand=True)

        dl_list = Frame(dl_canvas_inner, bg=BG_CARD)
        dl_win  = dl_canvas_inner.create_window((0, 0), window=dl_list, anchor="nw")

        dl_list.bind("<Configure>",
                     lambda e: dl_canvas_inner.configure(
                         scrollregion=dl_canvas_inner.bbox("all")))
        dl_canvas_inner.bind("<Configure>",
                             lambda e: dl_canvas_inner.itemconfig(dl_win, width=e.width))
        dl_canvas_inner.bind("<MouseWheel>",
                             lambda e: dl_canvas_inner.yview_scroll(
                                 int(-1 * (e.delta / 120)), "units"))

        # Add button — placed after dl_list is defined
        self.small_btn(dl_head, "+  ADD",
                       lambda: self._add_deadline_popup(deadlines, dl_list),
                       ACCENT_PINK).pack(side="right")

        self._render_deadlines(dl_list, deadlines)

    def _render_deadlines(self, parent, deadlines):
        for w in parent.winfo_children():
            w.destroy()

        if not deadlines:
            Label(parent,
                  text="No deadlines yet.\nClick  +  ADD  to create one.",
                  font=FONT_BODY, bg=BG_CARD, fg=TEXT_DIM,
                  justify="center").pack(pady=30)
            return

        today = datetime.date.today()

        for i, dl in enumerate(deadlines):
            deadline_date = datetime.date.fromisoformat(dl["date"])
            completed     = dl.get("completed", False)
            days_left     = (deadline_date - today).days

            if completed:
                border = TEXT_DIM
            elif days_left <= 3:
                border = ACCENT_PINK
            elif days_left <= 7:
                border = ACCENT_YELLOW
            else:
                border = ACCENT_GREEN

            card = Frame(parent, bg=BG_CARD2,
                         highlightbackground=border, highlightthickness=1)
            card.pack(fill="x", pady=3, padx=2)

            inner = Frame(card, bg=BG_CARD2, padx=10, pady=8)
            inner.pack(fill="x")

            # Title + action buttons
            title_row = Frame(inner, bg=BG_CARD2)
            title_row.pack(fill="x")

            name_fg    = TEXT_DIM if completed else TEXT_PRIMARY
            title_text = dl["module"] + ("  ✓" if completed else "")
            Label(title_row, text=title_text,
                  font=("Courier New", 11, "bold"),
                  bg=BG_CARD2, fg=name_fg).pack(side="left")

            btn_f = Frame(title_row, bg=BG_CARD2)
            btn_f.pack(side="right")

            def make_delete(idx):
                def delete():
                    deadlines.pop(idx)
                    self._save_deadlines(deadlines)
                    self._render_deadlines(parent, deadlines)
                return delete

            def make_complete(idx):
                def complete():
                    deadlines[idx]["completed"] = True
                    self._save_deadlines(deadlines)
                    self._render_deadlines(parent, deadlines)
                return complete

            self.small_btn(btn_f, "✕  DELETE", make_delete(i), TEXT_DIM).pack(side="right", padx=(4, 0))
            if not completed:
                self.small_btn(btn_f, "✓  DONE", make_complete(i), ACCENT_GREEN).pack(side="right", padx=(4, 0))

            # Date + status line
            date_str = deadline_date.strftime("%d %b %Y")
            if completed:
                status_text  = "Completed"
                status_color = TEXT_DIM
            elif days_left < 0:
                status_text  = f"Overdue by {-days_left} day{'s' if -days_left != 1 else ''}"
                status_color = ACCENT_PINK
            elif days_left == 0:
                status_text  = "Due TODAY"
                status_color = ACCENT_PINK
            elif days_left == 1:
                status_text  = "Due TOMORROW"
                status_color = ACCENT_YELLOW
            else:
                status_text  = f"{days_left} days remaining"
                status_color = (ACCENT_GREEN  if days_left > 14 else
                                ACCENT_YELLOW if days_left > 7  else
                                ACCENT_PINK)

            Label(inner, text=f"📅  {date_str}   ·   {status_text}",
                  font=("Courier New", 10),
                  bg=BG_CARD2, fg=status_color).pack(anchor="w", pady=(4, 0))

            # Deadline progress bar (incomplete only)
            if not completed:
                bar_start  = deadline_date - datetime.timedelta(days=21)
                elapsed    = (today - bar_start).days
                pct        = max(0.0, min(1.0, elapsed / 21))
                bar_color  = (ACCENT_PINK   if pct > 0.75 else
                              ACCENT_YELLOW if pct > 0.50 else
                              ACCENT_GREEN)

                bar_c = Canvas(inner, height=8, bg="#1e1e2e", highlightthickness=0)
                bar_c.pack(fill="x", pady=(6, 0))

                def make_bar_draw(c, p, col):
                    def draw(event):
                        c.delete("all")
                        c.create_rectangle(0, 0, event.width, 8, fill="#1e1e2e", outline="")
                        c.create_rectangle(0, 0, int(event.width * p), 8, fill=col, outline="")
                    return draw

                bar_c.bind("<Configure>", make_bar_draw(bar_c, pct, bar_color))

    def _add_deadline_popup(self, deadlines, render_parent):
        win = tk.Toplevel(self.root)
        win.title("Add Deadline")
        win.configure(bg=BG_DARK)
        win.resizable(False, False)
        win.grab_set()

        Label(win, text="📌  ADD DEADLINE",
              font=("Courier New", 18, "bold"),
              bg=BG_DARK, fg=ACCENT_PINK).pack(pady=(24, 8))
        Canvas(win, height=2, bg=ACCENT_PINK,
               highlightthickness=0, width=340).pack(fill="x", padx=30)

        Label(win, text="MODULE NAME",
              font=FONT_BODY, bg=BG_DARK, fg=TEXT_DIM).pack(pady=(18, 4))
        mf = Frame(win, bg=ACCENT_PINK, padx=2, pady=2)
        mf.pack()
        module_entry = Entry(mf, font=("Courier New", 16, "bold"), width=22,
                             bg=BG_CARD2, fg=ACCENT_PINK, insertbackground=ACCENT_PINK,
                             relief="flat", bd=0, justify="center")
        module_entry.pack(ipady=7, ipadx=7)
        module_entry.focus()

        Label(win, text="DEADLINE DATE  (DD/MM/YYYY)",
              font=FONT_BODY, bg=BG_DARK, fg=TEXT_DIM).pack(pady=(14, 4))
        df = Frame(win, bg=ACCENT_PINK, padx=2, pady=2)
        df.pack()
        date_entry = Entry(df, font=("Courier New", 16, "bold"), width=14,
                           bg=BG_CARD2, fg=ACCENT_PINK, insertbackground=ACCENT_PINK,
                           relief="flat", bd=0, justify="center")
        date_entry.pack(ipady=7, ipadx=7)

        err_lbl = Label(win, text="", font=FONT_BODY, bg=BG_DARK, fg=ACCENT_PINK)
        err_lbl.pack(pady=(10, 0))

        def save(*_):
            mod  = module_entry.get().strip()
            dstr = date_entry.get().strip()
            if not mod:
                err_lbl.config(text="⚠  Module name required.")
                return
            try:
                dt = datetime.datetime.strptime(dstr, "%d/%m/%Y").date()
            except ValueError:
                err_lbl.config(text="⚠  Use DD/MM/YYYY format.")
                return
            deadlines.append({"module": mod, "date": dt.isoformat(), "completed": False})
            deadlines.sort(key=lambda d: d["date"])
            self._save_deadlines(deadlines)
            self._render_deadlines(render_parent, deadlines)
            win.destroy()

        module_entry.bind("<Return>", lambda _: date_entry.focus())
        date_entry.bind("<Return>", save)
        self.small_btn(win, "✓  SAVE DEADLINE", save, ACCENT_PINK).pack(pady=(10, 26))
        win.protocol("WM_DELETE_WINDOW", win.destroy)

        win.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width()  - win.winfo_width())  // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - win.winfo_height()) // 2
        win.geometry(f"+{x}+{y}")


    # ══════════════════════════════════════════════════════════
    # SETTINGS
    # ══════════════════════════════════════════════════════════
    def show_settings(self):
        global ACCENT_CYAN
        self.clear()

        bg_canvas = Canvas(self.root, bg=BG_DARK, highlightthickness=0)
        bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        self._draw_grid(bg_canvas)

        # ── Header ──
        header = Frame(self.root, bg=BG_DARK, pady=8)
        header.pack(fill="x", padx=40)
        Label(header, text="⚙  SETTINGS",
              font=("Courier New", 26, "bold"),
              bg=BG_DARK, fg=ACCENT_CYAN).pack(side="left")
        self.small_btn(header, "🎮  GAMES",    self.show_home,      TEXT_DIM).pack(side="right", padx=(6, 0))
        self.small_btn(header, "⌂  DASHBOARD", self.show_dashboard, TEXT_DIM).pack(side="right", padx=(6, 0))
        self.divider(self.root, ACCENT_CYAN).pack(fill="x", padx=40, pady=(0, 16))

        # ── Two-column layout ──
        main = Frame(self.root, bg=BG_DARK)
        main.pack(fill="both", expand=True, padx=40, pady=(0, 20))
        main.columnconfigure(0, weight=1)
        main.columnconfigure(1, weight=1)
        main.rowconfigure(0, weight=1)

        # ════════════════════════════════════
        # LEFT COLUMN — Profile
        # ════════════════════════════════════
        left = Frame(main, bg=BG_DARK)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 12))

        # ── Display name card ──
        name_card = Frame(left, bg=BG_CARD,
                          highlightbackground=ACCENT_CYAN, highlightthickness=2,
                          padx=24, pady=18)
        name_card.pack(fill="x", pady=(0, 14))

        Label(name_card, text="👤  DISPLAY NAME",
              font=("Courier New", 13, "bold"),
              bg=BG_CARD, fg=TEXT_DIM).pack(anchor="w")
        self.divider(name_card, ACCENT_CYAN).pack(fill="x", pady=(4, 14))

        Label(name_card, text="USERNAME", font=FONT_BODY,
              bg=BG_CARD, fg=TEXT_DIM).pack(anchor="w", pady=(0, 4))
        nf = Frame(name_card, bg=ACCENT_CYAN, padx=2, pady=2)
        nf.pack(fill="x")
        name_entry = Entry(nf, font=("Courier New", 18, "bold"),
                           bg=BG_CARD2, fg=ACCENT_CYAN, insertbackground=ACCENT_CYAN,
                           relief="flat", bd=0, justify="center")
        name_entry.insert(0, self.settings["display_name"])
        name_entry.pack(fill="x", ipady=8, ipadx=8)

        name_msg = Label(name_card, text="", font=FONT_BODY,
                         bg=BG_CARD, fg=ACCENT_GREEN)
        name_msg.pack(anchor="w", pady=(8, 0))

        def save_name(*_):
            val = name_entry.get().strip()
            if not val:
                name_msg.config(text="⚠  Name cannot be empty.", fg=ACCENT_PINK)
                return
            self.settings["display_name"] = val
            self._save_settings()
            name_msg.config(text="✓  Saved!", fg=ACCENT_GREEN)

        self.small_btn(name_card, "✓  SAVE NAME", save_name,
                       ACCENT_CYAN).pack(anchor="w", pady=(10, 0))

        # ── Change password card ──
        pw_card = Frame(left, bg=BG_CARD,
                        highlightbackground=ACCENT_PINK, highlightthickness=2,
                        padx=24, pady=18)
        pw_card.pack(fill="x")

        Label(pw_card, text="🔒  CHANGE PASSWORD",
              font=("Courier New", 13, "bold"),
              bg=BG_CARD, fg=TEXT_DIM).pack(anchor="w")
        self.divider(pw_card, ACCENT_PINK).pack(fill="x", pady=(4, 14))

        for lbl_text, show_char in [("CURRENT PASSWORD", "*"), ("NEW PASSWORD", "*"), ("CONFIRM NEW", "*")]:
            Label(pw_card, text=lbl_text, font=FONT_BODY,
                  bg=BG_CARD, fg=TEXT_DIM).pack(anchor="w", pady=(0, 4))
            ef = Frame(pw_card, bg=ACCENT_PINK, padx=2, pady=2)
            ef.pack(fill="x", pady=(0, 10))
            e = Entry(ef, font=("Courier New", 16, "bold"), show=show_char,
                      bg=BG_CARD2, fg=ACCENT_PINK, insertbackground=ACCENT_PINK,
                      relief="flat", bd=0, justify="center")
            e.pack(fill="x", ipady=7, ipadx=8)
            if lbl_text == "CURRENT PASSWORD":
                cur_pw_entry = e
            elif lbl_text == "NEW PASSWORD":
                new_pw_entry = e
            else:
                conf_pw_entry = e

        pw_msg = Label(pw_card, text="", font=FONT_BODY, bg=BG_CARD, fg=ACCENT_GREEN)
        pw_msg.pack(anchor="w", pady=(0, 6))

        def save_password(*_):
            cur  = cur_pw_entry.get()
            new  = new_pw_entry.get()
            conf = conf_pw_entry.get()
            if cur != self.settings["password"]:
                pw_msg.config(text="⚠  Current password incorrect.", fg=ACCENT_PINK)
                return
            if len(new) < 2:
                pw_msg.config(text="⚠  Password too short.", fg=ACCENT_PINK)
                return
            if new != conf:
                pw_msg.config(text="⚠  Passwords do not match.", fg=ACCENT_PINK)
                return
            self.settings["password"] = new
            self._save_settings()
            cur_pw_entry.delete(0, "end")
            new_pw_entry.delete(0, "end")
            conf_pw_entry.delete(0, "end")
            pw_msg.config(text="✓  Password changed!", fg=ACCENT_GREEN)

        self.small_btn(pw_card, "✓  SAVE PASSWORD", save_password,
                       ACCENT_PINK).pack(anchor="w")

        # ════════════════════════════════════
        # RIGHT COLUMN — Preferences + Danger
        # ════════════════════════════════════
        right = Frame(main, bg=BG_DARK)
        right.grid(row=0, column=1, sticky="nsew", padx=(12, 0))

        # ── Snake speed card ──
        spd_card = Frame(right, bg=BG_CARD,
                         highlightbackground=ACCENT_GREEN, highlightthickness=2,
                         padx=24, pady=18)
        spd_card.pack(fill="x", pady=(0, 14))

        Label(spd_card, text="🐍  SNAKE SPEED",
              font=("Courier New", 13, "bold"),
              bg=BG_CARD, fg=TEXT_DIM).pack(anchor="w")
        self.divider(spd_card, ACCENT_GREEN).pack(fill="x", pady=(4, 14))

        spd_row = Frame(spd_card, bg=BG_CARD)
        spd_row.pack(fill="x")
        Label(spd_row, text="SLOW", font=FONT_BODY,
              bg=BG_CARD, fg=TEXT_DIM).pack(side="left")
        Label(spd_row, text="FAST", font=FONT_BODY,
              bg=BG_CARD, fg=TEXT_DIM).pack(side="right")

        # Speed stored as delay ms (higher = slower). Slider inverts: left=slow(200), right=fast(40)
        spd_var = tk.IntVar(value=self.settings["snake_speed"])
        spd_slider = tk.Scale(spd_card, from_=200, to=40, orient="horizontal",
                              variable=spd_var, showvalue=False,
                              bg=BG_CARD, fg=ACCENT_GREEN, troughcolor=BG_CARD2,
                              highlightthickness=0, bd=0, sliderrelief="flat",
                              activebackground=ACCENT_GREEN)
        spd_slider.pack(fill="x", pady=(2, 8))

        spd_labels = {200: "Very Slow", 160: "Slow", 120: "Medium",
                      80: "Fast", 40: "Very Fast"}

        def nearest_label(v):
            return spd_labels[min(spd_labels, key=lambda k: abs(k - v))]

        spd_lbl = Label(spd_card, text=nearest_label(self.settings["snake_speed"]),
                        font=("Courier New", 14, "bold"),
                        bg=BG_CARD, fg=ACCENT_GREEN)
        spd_lbl.pack(anchor="center")

        spd_msg = Label(spd_card, text="", font=FONT_BODY, bg=BG_CARD, fg=ACCENT_GREEN)
        spd_msg.pack(anchor="w", pady=(4, 0))

        def on_spd_change(*_):
            spd_lbl.config(text=nearest_label(spd_var.get()))
            spd_msg.config(text="")

        spd_var.trace_add("write", on_spd_change)

        def save_speed(*_):
            v = spd_var.get()
            self.settings["snake_speed"] = v
            self.snake_speed = v
            self._save_settings()
            spd_msg.config(text="✓  Saved!", fg=ACCENT_GREEN)

        self.small_btn(spd_card, "✓  SAVE SPEED", save_speed,
                       ACCENT_GREEN).pack(anchor="w", pady=(8, 0))

        # ── Accent colour card ──
        col_card = Frame(right, bg=BG_CARD,
                         highlightbackground=ACCENT_PURPLE, highlightthickness=2,
                         padx=24, pady=18)
        col_card.pack(fill="x", pady=(0, 14))

        Label(col_card, text="🎨  ACCENT COLOUR",
              font=("Courier New", 13, "bold"),
              bg=BG_CARD, fg=TEXT_DIM).pack(anchor="w")
        self.divider(col_card, ACCENT_PURPLE).pack(fill="x", pady=(4, 14))
        Label(col_card, text="Takes effect on next navigation.",
              font=("Courier New", 10), bg=BG_CARD, fg=TEXT_DIM).pack(anchor="w", pady=(0, 10))

        accent_options = [
            ("#00e5ff", "Cyan"),
            ("#ff2d78", "Pink"),
            ("#39ff14", "Green"),
            ("#9b59ff", "Purple"),
            ("#ff8c00", "Orange"),
            ("#ffe600", "Yellow"),
            ("#00ffc8", "Teal"),
        ]
        selected_colour = tk.StringVar(value=self.settings["accent_colour"])

        swatch_row = Frame(col_card, bg=BG_CARD)
        swatch_row.pack(anchor="w")

        col_msg = Label(col_card, text="", font=FONT_BODY, bg=BG_CARD, fg=ACCENT_GREEN)
        col_msg.pack(anchor="w", pady=(10, 0))

        def make_swatch(hex_val, name):
            is_sel = (hex_val == selected_colour.get())
            border = Frame(swatch_row, bg=TEXT_PRIMARY if is_sel else BG_CARD,
                           padx=2 if is_sel else 0, pady=2 if is_sel else 0)
            border.pack(side="left", padx=4)
            sw = Canvas(border, width=36, height=36, bg=hex_val,
                        highlightthickness=0, cursor="hand2")
            sw.pack()

            def click(e, h=hex_val):
                selected_colour.set(h)
                col_msg.config(text="")
                # Rebuild swatches to show new selection
                for w in swatch_row.winfo_children():
                    w.destroy()
                for hv, nm in accent_options:
                    make_swatch(hv, nm)

            sw.bind("<Button-1>", click)
            sw.bind("<Enter>", lambda e: sw.config(highlightthickness=2,
                                                    highlightbackground=TEXT_PRIMARY))
            sw.bind("<Leave>", lambda e: sw.config(highlightthickness=0))

        for hv, nm in accent_options:
            make_swatch(hv, nm)

        def save_colour(*_):
            global ACCENT_CYAN
            c = selected_colour.get()
            self.settings["accent_colour"] = c
            ACCENT_CYAN = c
            self.snake_speed = self.settings["snake_speed"]
            self._save_settings()
            col_msg.config(text="✓  Saved!", fg=ACCENT_GREEN)

        self.small_btn(col_card, "✓  SAVE COLOUR", save_colour,
                       ACCENT_PURPLE).pack(anchor="w", pady=(10, 0))

        # ── Clear scores card ──
        clr_card = Frame(right, bg=BG_CARD,
                         highlightbackground=ACCENT_PINK, highlightthickness=2,
                         padx=24, pady=18)
        clr_card.pack(fill="x")

        Label(clr_card, text="🗑  CLEAR HIGH SCORES",
              font=("Courier New", 13, "bold"),
              bg=BG_CARD, fg=TEXT_DIM).pack(anchor="w")
        self.divider(clr_card, ACCENT_PINK).pack(fill="x", pady=(4, 14))

        game_keys = {
            "snake":        ("Snake",        ACCENT_GREEN),
            "number_guess": ("Number Guess", ACCENT_PURPLE),
            "wordle":       ("Wordle",       ACCENT_YELLOW),
        }

        clr_msg = Label(clr_card, text="", font=FONT_BODY, bg=BG_CARD, fg=ACCENT_PINK)

        def clear_game(key, label):
            if key in self.high_scores:
                self.high_scores[key] = []
                self._save_scores()
            clr_msg.config(text=f"✓  {label} scores cleared.", fg=ACCENT_GREEN)

        def clear_all():
            self.high_scores.clear()
            self._save_scores()
            clr_msg.config(text="✓  All scores cleared.", fg=ACCENT_GREEN)

        btn_row = Frame(clr_card, bg=BG_CARD)
        btn_row.pack(anchor="w", pady=(0, 8))
        for key, (label, color) in game_keys.items():
            self.small_btn(btn_row, label, lambda k=key, l=label: clear_game(k, l),
                           color).pack(side="left", padx=(0, 8))

        self.small_btn(clr_card, "⚠  CLEAR ALL", clear_all,
                       ACCENT_PINK).pack(anchor="w", pady=(0, 4))
        clr_msg.pack(anchor="w")


# ─── LAUNCH ───────────────────────────────────────────────────
root = tk.Tk()
app = GameHub(root)
root.mainloop()