from PIL import Image, ImageDraw, ImageFont
import textwrap
import os
import json
import random
from datetime import datetime, timezone

# ========= SETTINGS =========

WIDTH = 1080
HEIGHT = 1350
BG_COLOR = (0, 0, 0)

TITLE_COLOR = (255, 190, 0)
TEXT_COLOR = (240, 240, 240)
CTA_COLOR = (255, 190, 0)
WATERMARK_COLOR = (90, 90, 90)

FONT_PATH = "src/Montserrat-Bold.ttf"

TITLE_SIZE = 64
TEXT_SIZE = 36
CTA_SIZE = 38
WATERMARK_SIZE = 24

OUTPUT_FOLDER = "output"

# IMPORTANT:
# GitHub Actions runners are fresh each run.
# We persist this state file via workflow artifacts.
STATE_FILE = os.path.join(OUTPUT_FOLDER, "state.json")

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ========= SMART WRAP =========

def smart_wrap(line: str) -> str:
    line = line.strip()

    if len(line) <= 55:
        return line
    if 56 <= len(line) <= 95:
        return textwrap.fill(line, width=42)
    if len(line) > 95:
        return textwrap.fill(line, width=36)
    return line

# ========= CONTENT BANK =========
# NOTE: For true 365-day no-repeat, make sure len(content_bank) >= 365
# You can paste your big bank here anytime.

content_bank = [
    {
        import random

# ========= DARK ELITE POOLS =========

title_part1 = [
"DARK TRUTHS",
"BRUTAL REALITIES",
"HARSH TRUTHS",
"UNCOMFORTABLE TRUTHS",
"PSYCHOLOGICAL TRUTHS",
"REALITIES",
"TRUTHS",
"SIGNS"
]

title_part2 = [
"ABOUT HUMAN NATURE",
"ABOUT PEOPLE",
"ABOUT RESPECT",
"ABOUT POWER",
"ABOUT STATUS",
"ABOUT SOCIAL LIFE",
"ABOUT HUMAN BEHAVIOR",
"ABOUT ATTENTION",
"ABOUT CONTROL",
"ABOUT SILENCE",
"ABOUT EGO",
"ABOUT DISCIPLINE"
]

line_pool = [
"People respect what they fear losing.",
"Attention is the real currency.",
"Silence reveals more than words.",
"Most loyalty is conditional.",
"Comfort kills ambition.",
"People test limits quietly.",
"Status changes treatment.",
"People believe actions, not words.",
"Absence increases value.",
"Familiarity reduces respect.",
"People protect self-interest first.",
"Calm people look powerful.",
"Desperation lowers value.",
"Boundaries reveal self-worth.",
"Consistency builds authority.",
"People admire restraint.",
"Emotional control signals strength.",
"Over-explaining reduces credibility.",
"Not everyone deserves access.",
"Privacy increases mystery.",
"Validation seeking weakens presence.",
"Scarcity creates attraction.",
"People notice discipline.",
"Respect follows standards.",
"Energy speaks before words.",
"People test your limits silently.",
"Calmness intimidates chaos.",
"Control earns admiration.",
"Detachment shows power.",
"People value what’s rare.",
"Reaction reveals insecurity.",
"Stillness shows confidence.",
"Presence beats noise.",
"Power is often quiet.",
"Observation beats talking.",
"People read behavior.",
"Predictability lowers intrigue.",
"Self-control earns respect.",
"Patience shows authority.",
"Silence filters people.",
"Not everyone clapping supports you.",
"Some loyalty is temporary.",
"People respect firmness.",
"Boundaries attract respect.",
"Too available lowers value.",
"People study your reactions.",
"Discipline separates you.",
"People trust consistency.",
"Calm minds look powerful.",
"Composure earns status."
]

cta_pool = [
"If you don’t follow now, you’ll probably never see us again.",
"Follow now or miss future truths.",
"Follow for deeper human truths.",
"Follow for dark psychology insights.",
"Follow if you value awareness.",
"Follow for real human behavior.",
"Follow for quiet psychological truths.",
"Follow for deeper perception.",
"Follow for mental sharpness.",
"Follow for human nature truths."
]

# ========= BUILD 365 POSTS =========

random.seed(42)  # stable rotation

content_bank = []

for _ in range(365):
    t1 = random.choice(title_part1)
    t2 = random.choice(title_part2)

    title = f"7 {t1}\n{t2}"

    lines = random.sample(line_pool, 7)
    lines.append(random.choice(cta_pool))

    content_bank.append({
        "title": title,
        "lines": lines
    })

]

# ========= YEAR ENGINE (NO REPEAT) =========

def today_str_utc() -> str:
    # Stable date regardless of runner timezone issues
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")

def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def save_state(state: dict):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def build_year_order(n: int, year: int, seed_salt: str = "THE_HUMAN_CODE_V9"):
    # Deterministic yearly shuffle: same year -> same order
    rng = random.Random(f"{seed_salt}:{year}:{n}")
    order = list(range(n))
    rng.shuffle(order)
    return order

def pick_next_post_id(n: int):
    state = load_state()
    year = int(datetime.now(timezone.utc).strftime("%Y"))

    # Reset if new year OR content length changed
    if (
        state.get("year") != year
        or state.get("n") != n
        or "order" not in state
        or "idx" not in state
    ):
        state["year"] = year
        state["n"] = n
        state["order"] = build_year_order(n, year)
        state["idx"] = 0

    # Safety if idx out of bounds
    if state["idx"] >= len(state["order"]):
        state["idx"] = 0

    post_id = state["order"][state["idx"]]
    state["idx"] += 1
    save_state(state)

    return post_id, state

# ========= PICK TODAY =========

POST_ID, STATE = pick_next_post_id(len(content_bank))
data = content_bank[POST_ID]

title = data["title"]
lines = data["lines"]

# ========= CREATE OUTPUT FOLDER FOR TODAY =========

DATE_TAG = today_str_utc()
DAY_DIR = os.path.join(OUTPUT_FOLDER, DATE_TAG)
os.makedirs(DAY_DIR, exist_ok=True)

# ========= CREATE IMAGE =========

img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
draw = ImageDraw.Draw(img)

title_font = ImageFont.truetype(FONT_PATH, TITLE_SIZE)
text_font = ImageFont.truetype(FONT_PATH, TEXT_SIZE)
cta_font = ImageFont.truetype(FONT_PATH, CTA_SIZE)
watermark_font = ImageFont.truetype(FONT_PATH, WATERMARK_SIZE)

# ========= DRAW TITLE =========

y = 120
for tline in title.split("\n"):
    w = draw.textlength(tline, font=title_font)
    draw.text(((WIDTH - w) / 2, y), tline, font=title_font, fill=TITLE_COLOR)
    y += 70
y += 40

# ========= DRAW LIST =========

number = 1
for line in lines:
    wrapped = smart_wrap(line)

    font = text_font
    color = TEXT_COLOR
    if number == len(lines):
        font = cta_font
        color = CTA_COLOR

    wrapped_lines = wrapped.split("\n")

    for wline in wrapped_lines:
        text = f"{number}. {wline}" if wline == wrapped_lines[0] else wline
        w = draw.textlength(text, font=font)
        draw.text(((WIDTH - w) / 2, y), text, font=font, fill=color)
        y += 50

    y += 25
    number += 1

# ========= WATERMARK =========

watermark = "THE HUMAN CODE"
w = draw.textlength(watermark, font=watermark_font)
draw.text(((WIDTH - w) / 2, HEIGHT - 60), watermark, font=watermark_font, fill=WATERMARK_COLOR)

# ========= SAVE IMAGE + CAPTION =========

img_path = os.path.join(DAY_DIR, f"post_{DATE_TAG}_id{POST_ID}.png")
img.save(img_path)

caption = title.replace("\n", " ") + "\n\n"
for i, l in enumerate(lines, 1):
    caption += f"{i}. {l}\n"

caption_path = os.path.join(DAY_DIR, f"caption_{DATE_TAG}_id{POST_ID}.txt")
with open(caption_path, "w", encoding="utf-8") as f:
    f.write(caption)

print("DONE")
print("DATE:", DATE_TAG)
print("POST_ID:", POST_ID)
print("STATE:", {"year": STATE.get("year"), "idx": STATE.get("idx"), "n": STATE.get("n")})
print("Image:", img_path)
print("Caption:", caption_path)
print("State file:", STATE_FILE)
