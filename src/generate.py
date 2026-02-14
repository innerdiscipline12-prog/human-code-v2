import os
import random
from PIL import Image, ImageDraw, ImageFont

# ========== SETTINGS ==========
WIDTH = 1080
HEIGHT = 1350

YELLOW = (255, 193, 7)
WHITE = (255, 255, 255)
GREY = (170, 170, 170)

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ========== DATA ==========
HEADLINES = [
    "SIGNS YOU LACK BOUNDARIES",
    "RULES OF HUMAN NATURE",
    "TRUTHS ABOUT SELF-RESPECT",
    "SIGNS YOU NEED DISCIPLINE",
    "HARD TRUTHS ABOUT LIFE"
]

LINES = [
    "You excuse disrespect",
    "You ignore red flags",
    "You fear being disliked",
    "You over-explain yourself",
    "You accept less than you give",
    "You avoid hard conversations",
    "You seek constant approval",
    "You tolerate repeated lies",
    "You chase those ignoring you",
    "You stay where you're drained",
]

CTAS = [
    "If you scroll past now,\nthis may never find you again.",
    "Few apply this.\nMany ignore it.",
    "Most won't remember this.\nDisciplined ones will."
]

# ========== FONTS ==========
try:
    FONT_HEAD = ImageFont.truetype("DejaVuSans-Bold.ttf", 64)
    FONT_BODY = ImageFont.truetype("DejaVuSans.ttf", 40)
    FONT_CTA = ImageFont.truetype("DejaVuSans.ttf", 30)
except:
    FONT_HEAD = FONT_BODY = FONT_CTA = ImageFont.load_default()

# ========== HELPERS ==========
def gradient_bg():
    img = Image.new("RGB", (WIDTH, HEIGHT), (10,10,10))
    draw = ImageDraw.Draw(img)

    for y in range(HEIGHT):
        shade = 10 + int((y/HEIGHT)*20)
        draw.line((0,y,WIDTH,y), fill=(shade,shade,shade))

    return img

def center_text(draw, text, y, font, color):
    bbox = draw.textbbox((0,0), text, font=font)
    w = bbox[2] - bbox[0]
    x = (WIDTH - w)//2
    draw.text((x,y), text, font=font, fill=color)

# ========== GENERATOR ==========
def make_post(i):
    img = gradient_bg()
    draw = ImageDraw.Draw(img)

    headline = random.choice(HEADLINES)
    lines = random.sample(LINES, 5)
    cta = random.choice(CTAS)

    # Headline
    center_text(draw, headline, 120, FONT_HEAD, YELLOW)

    # Body
    y = 300
    for line in lines:
        txt = f"• {line}"
        center_text(draw, txt, y, FONT_BODY, WHITE)
        y += 80

    # CTA
    for part in cta.split("\n"):
        center_text(draw, part, HEIGHT-180, FONT_CTA, GREY)
        HEIGHT_OFFSET = 40
        center_text(draw, part, HEIGHT-180, FONT_CTA, GREY)

    img.save(f"{OUTPUT_DIR}/post_{i+1}.png")

# ========== RUN ==========
for i in range(5):
    make_post(i)

print("V5 images generated.")
