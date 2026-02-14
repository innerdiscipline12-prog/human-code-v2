from PIL import Image, ImageDraw, ImageFont
import os
import textwrap

# -------- SETTINGS --------
W, H = 1080, 1350
BG_COLOR = (0,0,0)

YELLOW = (255,185,0)
WHITE = (245,245,245)
GRAY = (90,90,90)

TITLE_SIZE = 72
BODY_SIZE = 42
CTA_SIZE = 42
WM_SIZE = 28

LEFT_MARGIN = 90
RIGHT_MARGIN = 90

# -------- LOAD FONTS --------
def load_font(size):
    try:
        return ImageFont.truetype("Montserrat-Bold.ttf", size)
    except:
        return ImageFont.load_default()

title_font = load_font(TITLE_SIZE)
body_font = load_font(BODY_SIZE)
cta_font = load_font(CTA_SIZE)
wm_font = load_font(WM_SIZE)

# -------- CONTENT --------
title = "7 SIGNS YOU MIGHT BE TOXIC TO YOURSELF"

points = [
"You say sorry for things that were never your fault.",
"You tolerate people who shrink your confidence.",
"You keep checking your phone, waiting for texts that don’t come.",
"You treat every piece of feedback like it’s an attack on your worth.",
"You measure your life against everyone else’s highlight reel.",
"You sleep more to escape, not to rest.",
"You agree with everything because you're afraid your real opinion won’t be accepted."
]

cta = "If you don’t follow now, you’ll probably never see us again."
watermark = "THE HUMAN CODE"

# -------- CREATE IMAGE --------
img = Image.new("RGB",(W,H),BG_COLOR)
draw = ImageDraw.Draw(img)

y = 70

# -------- TITLE --------
title_lines = textwrap.wrap(title.upper(), width=20)

for line in title_lines:
    w = draw.textlength(line, font=title_font)
    draw.text(((W-w)/2, y), line, font=title_font, fill=YELLOW)
    y += 80

y += 30

# -------- BODY --------
for i, p in enumerate(points):
    text = f"{i+1}. {p}"
    wrapped = textwrap.wrap(text, width=40)

    for line in wrapped:
        draw.text((LEFT_MARGIN, y), line, font=body_font, fill=WHITE)
        y += 55

    y += 10

# -------- CTA (YELLOW) --------
y += 10
cta_lines = textwrap.wrap(f"{len(points)+1}. {cta}", width=40)

for line in cta_lines:
    draw.text((LEFT_MARGIN, y), line, font=cta_font, fill=YELLOW)
    y += 55

# -------- WATERMARK --------
w = draw.textlength(watermark, font=wm_font)
draw.text(((W-w)/2, H-70), watermark, font=wm_font, fill=GRAY)

# -------- SAVE --------
os.makedirs("output", exist_ok=True)
img.save("output/viral_post.png")

print("✅ Viral post generated -> output/viral_post.png")
