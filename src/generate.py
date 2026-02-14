from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

# -------- SETTINGS --------
WIDTH = 1080
HEIGHT = 1350

BG_COLOR = (0, 0, 0)
YELLOW = (255, 185, 0)
WHITE = (235, 235, 235)
GRAY = (90, 90, 90)

FONT_PATH = "src/Montserrat-Bold.ttf"

TITLE_SIZE = 82
BODY_SIZE = 44
CTA_SIZE = 48
WATERMARK_SIZE = 28

LEFT_MARGIN = 90
RIGHT_MARGIN = 90

# -------- TEXT --------
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

cta = "8. If you don’t follow now, you’ll probably never see us again."
watermark = "THE HUMAN CODE"

# -------- FONTS --------
title_font = ImageFont.truetype(FONT_PATH, TITLE_SIZE)
body_font = ImageFont.truetype(FONT_PATH, BODY_SIZE)
cta_font = ImageFont.truetype(FONT_PATH, CTA_SIZE)
watermark_font = ImageFont.truetype(FONT_PATH, WATERMARK_SIZE)

# -------- CANVAS --------
img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
draw = ImageDraw.Draw(img)

# -------- TITLE --------
y = 80

for line in title.split("\n"):
    w, h = draw.textbbox((0,0), line, font=title_font)[2:]
    x = (WIDTH - w) // 2
    draw.text((x, y), line, fill=YELLOW, font=title_font)
    y += h + 10

y += 40

# -------- AUTO SPACING ENGINE --------
wrap_width = 32
line_gap = 8

for i, point in enumerate(points, start=1):

    wrapped = textwrap.fill(f"{i}. {point}", width=wrap_width)
    lines = wrapped.split("\n")

    for line in lines:
        draw.text((LEFT_MARGIN, y), line, fill=WHITE, font=body_font)
        line_h = draw.textbbox((0,0), line, font=body_font)[3]
        y += line_h + line_gap

    # dynamic spacing after each point
    y += 28

# -------- CTA --------
y += 10
wrapped_cta = textwrap.fill(cta, width=32)
for line in wrapped_cta.split("\n"):
    draw.text((LEFT_MARGIN, y), line, fill=YELLOW, font=cta_font)
    line_h = draw.textbbox((0,0), line, font=cta_font)[3]
    y += line_h + 6

# -------- WATERMARK --------
w, h = draw.textbbox((0,0), watermark, font=watermark_font)[2:]
draw.text(((WIDTH-w)//2, HEIGHT-80), watermark, fill=GRAY, font=watermark_font)

# -------- SAVE --------
os.makedirs("output", exist_ok=True)
img.save("output/post.png")

print("Done. Saved to output/post.png")
