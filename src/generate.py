import os
from PIL import Image, ImageDraw, ImageFont
import textwrap
import random

# ===== SETTINGS =====
W, H = 1080, 1350
BG_COLOR = (10,10,10)
GOLD = (212,175,55)
WHITE = (240,240,240)
GRAY = (130,130,130)

TITLE_FONT_SIZE = 72
BODY_FONT_SIZE = 44
CTA_FONT_SIZE = 38

OUTPUT_DIR = "output/photos"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ===== FONTS (GitHub safe default) =====
title_font = ImageFont.load_default()
body_font = ImageFont.load_default()
cta_font = ImageFont.load_default()

# ===== CONTENT =====
posts = [
    {
        "title": "SELF-RESPECT CHECK",
        "lines":[
            "You ignore red flags",
            "You seek constant approval",
            "You excuse disrespect",
            "You stay where you're drained",
            "You accept less than you give",
        ],
        "cta":"If you don’t follow now, you’ll probably never see us again."
    },
    {
        "title":"QUIET POWER RULES",
        "lines":[
            "Move in silence",
            "Protect your energy",
            "Consistency beats mood",
            "Discipline over feelings",
            "Standards over comfort",
        ],
        "cta":"If you don’t follow now, you’ll probably never see us again."
    },
    {
        "title":"BOUNDARY REMINDERS",
        "lines":[
            "No is a full sentence",
            "Distance is protection",
            "Not everyone deserves access",
            "Peace over people-pleasing",
            "Respect your limits",
        ],
        "cta":"If you don’t follow now, you’ll probably never see us again."
    },
]

# ===== DRAW FUNCTION =====
def create_post(data, idx):
    img = Image.new("RGB",(W,H),BG_COLOR)
    draw = ImageDraw.Draw(img)

    y = 80

    # Title
    title = data["title"]
    tw = draw.textlength(title,font=title_font)
    draw.text(((W-tw)/2,y),title,fill=GOLD,font=title_font)
    y += 120

    # Lines
    for i,line in enumerate(data["lines"],1):
        text = f"{i}. {line}"
        wrapped = textwrap.fill(text,28)

        for part in wrapped.split("\n"):
            w = draw.textlength(part,font=body_font)
            draw.text(((W-w)/2,y),part,fill=WHITE,font=body_font)
            y+=55

        y+=15

    # CTA (numbered last)
    y+=40
    cta = f"{len(data['lines'])+1}. {data['cta']}"
    wrapped = textwrap.fill(cta,34)

    for part in wrapped.split("\n"):
        w = draw.textlength(part,font=cta_font)
        draw.text(((W-w)/2,y),part,fill=GRAY,font=cta_font)
        y+=45

    # Watermark
    wm="THE HUMAN CODE"
    w = draw.textlength(wm,font=body_font)
    draw.text(((W-w)/2,H-60),wm,fill=(80,80,80),font=body_font)

    img.save(f"{OUTPUT_DIR}/post_{idx}.jpg",quality=95)

# ===== RUN =====
for i,data in enumerate(posts,1):
    create_post(data,i)

print("DONE — Photos generated.")
