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
STATE_FILE = "state.json"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ========= WRAP =========

def smart_wrap(line):
    if len(line) <= 55:
        return line
    if len(line) <= 95:
        return textwrap.fill(line, width=42)
    return textwrap.fill(line, width=36)

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

# ========= MEASURE TOTAL HEIGHT =========

def measure_content_height(draw, data, title_font, text_font, cta_font):
    total = 0

    # Title lines
    for line in data["title"].split("\n"):
        total += 70
    total += 40  # gap after title

    # Body lines
    for i, line in enumerate(data["lines"]):
        num = i + 1
        wrapped = smart_wrap(line)
        font = cta_font if num == 8 else text_font
        sub_lines = wrapped.split("\n")
        total += len(sub_lines) * 50
        total += 25  # gap between items

    return total

# ========= DRAW =========

img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
draw = ImageDraw.Draw(img)

title_font = ImageFont.truetype(FONT_PATH, TITLE_SIZE)
text_font = ImageFont.truetype(FONT_PATH, TEXT_SIZE)
cta_font = ImageFont.truetype(FONT_PATH, CTA_SIZE)
watermark_font = ImageFont.truetype(FONT_PATH, WATERMARK_SIZE)

# Calculate vertical centering (leave 80px at bottom for watermark)
content_height = measure_content_height(draw, data, title_font, text_font, cta_font)
usable_height = HEIGHT - 80
y = max(80, (usable_height - content_height) // 2)

# Draw title
for line in data["title"].split("\n"):
    w = draw.textlength(line, font=title_font)
    draw.text(((WIDTH - w) / 2, y), line, font=title_font, fill=TITLE_COLOR)
    y += 70

y += 40

# Draw lines
num = 1
for line in data["lines"]:
    wrapped = smart_wrap(line)
    font = cta_font if num == 8 else text_font
    color = CTA_COLOR if num == 8 else TEXT_COLOR

    sub_lines = wrapped.split("\n")
    for i, wl in enumerate(sub_lines):
        if num == 8:
            # CTA: no number, just centered text
            text = wl
        else:
            text = f"{num}. {wl}" if i == 0 else f"    {wl}"

        w = draw.textlength(text, font=font)
        draw.text(((WIDTH - w) / 2, y), text, font=font, fill=color)
        y += 50

    y += 25
    num += 1

# Watermark
wm = "THE HUMAN CODE"
w = draw.textlength(wm, font=watermark_font)
draw.text(((WIDTH - w) / 2, HEIGHT - 60), wm, font=watermark_font, fill=WATERMARK_COLOR)

# Save
img.save(f"{OUTPUT_FOLDER}/post.png")
print("DONE")

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
"Patience builds leverage."
]

cta_pool = [
"If you don’t follow now, you’ll probably never see us again.",
"Follow for deeper truths.",
"Follow for dark psychology.",
"Follow for real human behavior."
]

# ========= BUILD 365 BANK =========

content_bank = []

for _ in range(365):
    t1 = random.choice(title_part1)
    t2 = random.choice(title_part2)
    title = f"7 {t1}\n{t2}"

    lines = random.sample(line_pool,7)
    lines.append(random.choice(cta_pool))

    content_bank.append({
        "title":title,
        "lines":lines
    })

# ========= STATE ENGINE =========

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE,"r") as f:
            return json.load(f)
    return {"index":0}

def save_state(s):
    with open(STATE_FILE,"w") as f:
        json.dump(s,f)

state = load_state()
idx = state["index"] % len(content_bank)

data = content_bank[idx]

state["index"] += 1
save_state(state)

# ========= DRAW =========

img = Image.new("RGB",(WIDTH,HEIGHT),BG_COLOR)
draw = ImageDraw.Draw(img)

title_font = ImageFont.truetype(FONT_PATH,TITLE_SIZE)
text_font = ImageFont.truetype(FONT_PATH,TEXT_SIZE)
cta_font = ImageFont.truetype(FONT_PATH,CTA_SIZE)
watermark_font = ImageFont.truetype(FONT_PATH,WATERMARK_SIZE)

y = 120

for line in data["title"].split("\n"):
    w = draw.textlength(line,font=title_font)
    draw.text(((WIDTH-w)/2,y),line,font=title_font,fill=TITLE_COLOR)
    y += 70

y += 40

num=1
for line in data["lines"]:
    wrapped = smart_wrap(line)

    font = cta_font if num==8 else text_font
    color = CTA_COLOR if num==8 else TEXT_COLOR

    for wl in wrapped.split("\n"):
        text = f"{num}. {wl}" if wl==wrapped.split("\n")[0] else wl
        w = draw.textlength(text,font=font)
        draw.text(((WIDTH-w)/2,y),text,font=font,fill=color)
        y+=50

    y+=25
    num+=1

# watermark
wm="THE HUMAN CODE"
w=draw.textlength(wm,font=watermark_font)
draw.text(((WIDTH-w)/2,HEIGHT-60),wm,font=watermark_font,fill=WATERMARK_COLOR)

# save
img.save(f"{OUTPUT_FOLDER}/post.png")

print("DONE")
