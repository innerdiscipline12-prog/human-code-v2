from PIL import Image, ImageDraw, ImageFont
import textwrap
import os
import json
import random
from datetime import datetime, timezone

# ========= SETTINGS =========

WIDTH = 1080
HEIGHT = 1350
BG_COLOR = (0,0,0)

TITLE_COLOR = (255,190,0)
TEXT_COLOR = (240,240,240)
CTA_COLOR = (255,190,0)
WATERMARK_COLOR = (90,90,90)

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
        return textwrap.fill(line,width=42)
    return textwrap.fill(line,width=36)

# ========= TITLE POOLS =========

title_part1 = [
"DARK TRUTHS",
"HARSH REALITIES",
"BRUTAL TRUTHS",
"PSYCHOLOGICAL TRUTHS",
"UNCOMFORTABLE TRUTHS",
"SOCIAL TRUTHS"
]

title_part2 = [
"ABOUT PEOPLE",
"ABOUT POWER",
"ABOUT RESPECT",
"ABOUT HUMAN NATURE",
"ABOUT STATUS",
"ABOUT EGO",
"ABOUT CONTROL"
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
