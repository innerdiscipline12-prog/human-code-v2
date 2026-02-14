from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

# ---------- SETTINGS ----------
WIDTH = 1080
HEIGHT = 1350  # 4:5 ratio (viral format)

BG_COLOR = (0, 0, 0)
YELLOW = (255, 185, 0)
WHITE = (235, 235, 235)
GRAY = (90, 90, 90)

FONT_PATH = "src/Montserrat-Bold.ttf"


TITLE_SIZE = 82  # ~8% smaller
BODY_SIZE = 44
CTA_SIZE = 48
WATERMARK_SIZE = 28

LEFT_MARGIN = 90
RIGHT_MARGIN = 90

# ---------- TEXT ----------
title = "7 SIGNS YOU MIGHT BE\nTOXIC TO YOURSELF"

points = [
"You say sorry for things that were never your fault.",
"You tolerate people who shrink your confidence.",
"You keep checking your phone, waiting for texts that don’t come.",
"You treat every piece of feedback like it’s an attack on your worth.",
"You measure your life against everyone else’s highlight reel.",
"You sleep more to escape, not to rest.",
"You agree with everything because you’re afraid your real opinion won’t be accepted."
]

cta = "If you don’t follow now, you’ll probably never see us again."

# ---------- IMAGE ----------
img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
draw = ImageDraw.Draw(img)

title_font = ImageFont.truetype(FONT_PATH, TITLE_SIZE)
body_font = ImageFont.truetype(FONT_PATH, BODY_SIZE)
cta_font = ImageFont.truetype(FONT_PATH, CTA_SIZE)
watermark_font = ImageFont.truetype(FONT_PATH, WATERMARK_SIZE)

# ---------- TITLE ----------
title_y = 80

for line in title.split("\n"):
    w = draw.textlength(line, font=title_font)
    draw.text(((WIDTH-w)/2, title_y), line, font=title_font, fill=YELLOW)
    title_y += TITLE_SIZE + 10

# ---------- BODY ----------
y = title_y + 40

for i, p in enumerate(points, 1):
    text = f"{i}. {p}"
    wrapped = textwrap.fill(text, width=42)

    for line in wrapped.split("\n"):
        draw.text((LEFT_MARGIN, y), line, font=body_font, fill=WHITE)
        y += BODY_SIZE + 8
    
    y += 12  # spacing between points

# ---------- CTA ----------
y += 10
wrapped_cta = textwrap.fill(f"{len(points)+1}. {cta}", width=42)

for line in wrapped_cta.split("\n"):
    draw.text((LEFT_MARGIN, y), line, font=cta_font, fill=YELLOW)
    y += CTA_SIZE + 6

# ---------- WATERMARK ----------
wm = "THE HUMAN CODE"
w = draw.textlength(wm, font=watermark_font)
draw.text(((WIDTH-w)/2, HEIGHT-70), wm, font=watermark_font, fill=GRAY)

# ---------- SAVE ----------
os.makedirs("output", exist_ok=True)
img.save("output/post.png")

print("DONE ✅ Image saved in /output/post.png")
