from PIL import Image, ImageDraw, ImageFont
import textwrap
import os
import json
import random

# ========= SETTINGS =========

WIDTH = 1080
HEIGHT = 1350
BG_COLOR = (0, 0, 0)

TITLE_COLOR = (255, 190, 0)
TEXT_COLOR = (240, 240, 240)
CTA_COLOR = (255, 190, 0)
WATERMARK_COLOR = (90, 90, 90)
QUOTE_COLOR = (200, 200, 200)
ACCENT_COLOR = (255, 190, 0)

FONT_PATH = "src/Montserrat-Bold.ttf"

TITLE_SIZE = 64
TEXT_SIZE = 36
CTA_SIZE = 38
WATERMARK_SIZE = 24
QUOTE_SIZE = 44
QUOTE_LABEL_SIZE = 26
COVER_TITLE_SIZE = 62

OUTPUT_FOLDER = "output"
STATE_FILE = "state.json"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ========= WRAP =========

def smart_wrap(line):
    if len(line) <= 55:
        return line
    if len(line) <= 95:
        return textwrap.fill(line, width=42)
    return textwrap.fill(line, width=36)

def wrap_quote(line, width=30):
    return textwrap.fill(line, width=width)

# ========= TITLE POOLS =========

title_part1 = [
    "DARK TRUTHS",
    "HARSH REALITIES",
    "BRUTAL TRUTHS",
    "PSYCHOLOGICAL TRUTHS",
    "UNCOMFORTABLE TRUTHS",
    "SOCIAL TRUTHS",
    "COLD FACTS",
    "HIDDEN LAWS",
    "SILENT RULES",
    "UNSPOKEN TRUTHS",
]

title_part2 = [
    "ABOUT PEOPLE",
    "ABOUT POWER",
    "ABOUT RESPECT",
    "ABOUT HUMAN NATURE",
    "ABOUT STATUS",
    "ABOUT EGO",
    "ABOUT CONTROL",
    "ABOUT LOYALTY",
    "ABOUT INFLUENCE",
    "ABOUT MINDSET",
    "ABOUT SUCCESS",
    "ABOUT WEAKNESS",
]

# ========= LINE POOL =========

line_pool = [
    "People respect what they fear losing.",
    "Silence exposes truth.",
    "Comfort weakens discipline.",
    "Attention equals value.",
    "Status changes treatment.",
    "Consistency builds authority.",
    "Boundaries earn respect.",
    "Presence speaks loudly.",
    "Control attracts respect.",
    "People test limits quietly.",
    "Energy reveals confidence.",
    "Calm signals power.",
    "Results silence doubt.",
    "Most loyalty is conditional.",
    "People value scarcity.",
    "Focus creates advantage.",
    "Detachment reveals worth.",
    "Discipline shapes identity.",
    "Restraint shows strength.",
    "Patience builds leverage.",
    "Desperation repels opportunity.",
    "Ambition without action is fantasy.",
    "Weakness invites disrespect.",
    "Most advice protects the giver.",
    "Envy hides behind criticism.",
    "Neediness destroys attraction.",
    "Power is taken, not given.",
    "Kindness without limits gets exploited.",
    "People follow confidence, not logic.",
    "Your network defines your ceiling.",
    "Emotions cloud judgment at the worst times.",
    "Obsession beats talent consistently.",
    "Those who talk most know least.",
    "Money reveals true character.",
    "Reputation travels faster than truth.",
    "Urgency is often manufactured.",
    "Pain teaches what comfort never could.",
    "Most people fear standing alone.",
    "Accountability is rare and powerful.",
    "Perception shapes reality more than facts.",
]

# ========= QUOTE OF THE DAY POOL =========

quote_pool = [
    ("The less you react, the more powerful you become.", "Unknown"),
    ("Silence is the best response to a fool.", "Unknown"),
    ("Discipline is choosing what you want most over what you want now.", "Abraham Lincoln"),
    ("The wolf does not concern himself with the opinion of sheep.", "Unknown"),
    ("Do not argue with fools. They drag you to their level.", "Mark Twain"),
    ("Some people aren't loyal to you. They are loyal to their need of you.", "Unknown"),
    ("Work in silence. Let success make the noise.", "Unknown"),
    ("Fear kills more dreams than failure ever will.", "Suzy Kassem"),
    ("When you react, you give away your power.", "Unknown"),
    ("Be careful who you trust. Salt and sugar look the same.", "Unknown"),
    ("Not everyone deserves access to you.", "Unknown"),
    ("You are the average of the five people you spend the most time with.", "Jim Rohn"),
    ("Energy is everything. Protect yours.", "Unknown"),
    ("The quieter you become, the more you can hear.", "Ram Dass"),
    ("Master your mind or your mind will master you.", "Unknown"),
    ("Stop explaining yourself. You don't owe anyone your story.", "Unknown"),
    ("The man who does not read has no advantage over the man who cannot.", "Mark Twain"),
    ("Obsessed is a word the lazy use to describe the dedicated.", "Unknown"),
    ("Closed mouths don't get fed. Open ones don't stay hungry.", "Unknown"),
    ("Your vibe attracts your tribe.", "Unknown"),
]

# ========= CTA POOL =========

cta_pool = [
    "Follow for more dark psychology.",
    "Follow for deeper truths.",
    "Follow for real human behavior.",
    "Follow for unfiltered human nature.",
    "Follow. Most people scroll past wisdom.",
    "Follow for truths they won't teach you.",
    "Follow if you want to see more of this.",
    "Follow for cold truths about human nature.",
]

# ========= BUILD 365 BANK =========

# All unique title combos shuffled — 120 unique combinations
all_combos = [(t1, t2) for t1 in title_part1 for t2 in title_part2]
random.shuffle(all_combos)

# Non-repeating quote and CTA cycles
quote_cycle = quote_pool * (365 // len(quote_pool) + 1)
random.shuffle(quote_cycle)

cta_cycle = cta_pool * (365 // len(cta_pool) + 1)
random.shuffle(cta_cycle)

# Non-repeating 7-line blocks from line pool
line_blocks = []
shuffled_lines = line_pool[:]
random.shuffle(shuffled_lines)
for i in range(365):
    if len(shuffled_lines) < 7:
        shuffled_lines = line_pool[:]
        random.shuffle(shuffled_lines)
    block = shuffled_lines[:7]
    shuffled_lines = shuffled_lines[7:]
    line_blocks.append(block)

content_bank = []

for i in range(365):
    t1, t2 = all_combos[i % len(all_combos)]
    title = f"7 {t1}\n{t2}"
    lines = line_blocks[i][:]
    lines.append(cta_cycle[i])
    quote, author = quote_cycle[i]
    content_bank.append({
        "title": title,
        "lines": lines,
        "quote": quote,
        "author": author,
    })

# ========= STATE ENGINE =========

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {"index": 0}

def save_state(s):
    with open(STATE_FILE, "w") as f:
        json.dump(s, f)

state = load_state()
idx = state["index"] % len(content_bank)
data = content_bank[idx]
state["index"] += 1
save_state(state)

# ========= HELPERS =========

def draw_watermark(draw, font, width, height):
    wm = "THE HUMAN CODE"
    w = draw.textlength(wm, font=font)
    draw.text(((width - w) / 2, height - 60), wm, font=font, fill=WATERMARK_COLOR)

def measure_content_height(data):
    total = 2 * 70 + 40
    for line in data["lines"]:
        wrapped = smart_wrap(line)
        total += len(wrapped.split("\n")) * 50 + 25
    return total

# ========= FONTS =========

title_font     = ImageFont.truetype(FONT_PATH, TITLE_SIZE)
text_font      = ImageFont.truetype(FONT_PATH, TEXT_SIZE)
cta_font       = ImageFont.truetype(FONT_PATH, CTA_SIZE)
watermark_font = ImageFont.truetype(FONT_PATH, WATERMARK_SIZE)
quote_font     = ImageFont.truetype(FONT_PATH, QUOTE_SIZE)
qlabel_font    = ImageFont.truetype(FONT_PATH, QUOTE_LABEL_SIZE)
cover_font     = ImageFont.truetype(FONT_PATH, COVER_TITLE_SIZE)

# =========================================
# SLIDE 1 — COVER (Title + Quote of the Day)
# =========================================

cover = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
cd = ImageDraw.Draw(cover)

quote_lines     = wrap_quote(data["quote"], width=30).split("\n")
title_lines     = data["title"].split("\n")
title_block_h   = len(title_lines) * 90
gap_after_title = 50
divider_h       = 4 + 50
label_h         = 60
quote_block_h   = len(quote_lines) * 60
author_h        = 65
total_cover_h   = title_block_h + gap_after_title + divider_h + label_h + quote_block_h + author_h

WATERMARK_ZONE  = 120
usable          = HEIGHT - WATERMARK_ZONE
cy              = max(120, (usable - total_cover_h) // 2)

# Top accent line
cd.rectangle([(80, 60), (WIDTH - 80, 66)], fill=ACCENT_COLOR)

# Brand label
brand = "THE HUMAN CODE"
bw = cd.textlength(brand, font=qlabel_font)
cd.text(((WIDTH - bw) / 2, 82), brand, font=qlabel_font, fill=WATERMARK_COLOR)

# Cover title with dynamic font shrink
MARGIN = 80
for line in title_lines:
    font_size = COVER_TITLE_SIZE
    f = cover_font
    while cd.textlength(line, font=f) > (WIDTH - MARGIN * 2) and font_size > 40:
        font_size -= 2
        f = ImageFont.truetype(FONT_PATH, font_size)
    lw = cd.textlength(line, font=f)
    cd.text(((WIDTH - lw) / 2, cy), line, font=f, fill=TITLE_COLOR)
    cy += 90

cy += gap_after_title

# Divider
cd.rectangle([(160, cy), (WIDTH - 160, cy + 4)], fill=ACCENT_COLOR)
cy += 30

# QUOTE OF THE DAY label
label = "QUOTE OF THE DAY"
lw = cd.textlength(label, font=qlabel_font)
cd.text(((WIDTH - lw) / 2, cy), label, font=qlabel_font, fill=ACCENT_COLOR)
cy += label_h

# Opening quote mark
cd.text((80, cy - 10), "\u201C", font=quote_font, fill=ACCENT_COLOR)

# Quote text
for qline in quote_lines:
    qw = cd.textlength(qline, font=quote_font)
    cd.text(((WIDTH - qw) / 2, cy), qline, font=quote_font, fill=QUOTE_COLOR)
    cy += 60

# Closing quote mark
cd.text((WIDTH - 110, cy - 20), "\u201D", font=quote_font, fill=ACCENT_COLOR)
cy += 20

# Author / handle
author_text = "\u2014 @humancode.psychology"
aw = cd.textlength(author_text, font=qlabel_font)
cd.text(((WIDTH - aw) / 2, cy), author_text, font=qlabel_font, fill=TEXT_COLOR)

# Bottom accent line
cd.rectangle([(80, HEIGHT - 100), (WIDTH - 80, HEIGHT - 94)], fill=ACCENT_COLOR)

# Watermark
draw_watermark(cd, watermark_font, WIDTH, HEIGHT)

cover.save(f"{OUTPUT_FOLDER}/slide_1.png")
print("SLIDE 1 (cover) saved.")

# =========================================
# SLIDE 2 — LIST POST
# =========================================

img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
draw = ImageDraw.Draw(img)

content_height = measure_content_height(data)
usable_height = HEIGHT - 80
y = max(60, (usable_height - content_height) // 2)

# Title
for line in data["title"].split("\n"):
    w = draw.textlength(line, font=title_font)
    draw.text(((WIDTH - w) / 2, y), line, font=title_font, fill=TITLE_COLOR)
    y += 70

y += 40

# Lines
num = 1
for line in data["lines"]:
    is_cta = (num == 8)
    wrapped = smart_wrap(line)
    font = cta_font if is_cta else text_font
    color = CTA_COLOR if is_cta else TEXT_COLOR

    sub_lines = wrapped.split("\n")
    for i, wl in enumerate(sub_lines):
        if is_cta:
            text = wl
        else:
            text = f"{num}. {wl}" if i == 0 else f"    {wl}"
        w = draw.textlength(text, font=font)
        draw.text(((WIDTH - w) / 2, y), text, font=font, fill=color)
        y += 50

    y += 25
    num += 1

# Watermark
draw_watermark(draw, watermark_font, WIDTH, HEIGHT)

img.save(f"{OUTPUT_FOLDER}/slide_2.png")
print("SLIDE 2 (post) saved.")
print("DONE")
