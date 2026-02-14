from PIL import Image, ImageDraw, ImageFont
import os

# ---------- SETTINGS ----------
WIDTH = 1080
HEIGHT = 1350
BG_COLOR = (0, 0, 0)
YELLOW = (255, 185, 0)
WHITE = (240, 240, 240)
GRAY = (120, 120, 120)

TITLE_SIZE = 64
TEXT_SIZE = 42
WATERMARK_SIZE = 28

FONT_BOLD = ImageFont.load_default()
FONT_REG = ImageFont.load_default()

# ---------- CONTENT ----------
title = "7 SIGNS YOU MIGHT BE\nTOXIC TO YOURSELF"

lines = [
"You say sorry for things that were never your fault.",
"You tolerate people who shrink your confidence.",
"You keep checking your phone, waiting for texts that don’t come.",
"You treat every piece of feedback like it’s an attack on your worth.",
"You measure your life against everyone else’s highlight reel.",
"You sleep more to escape, not to rest.",
"You agree with everything because you're afraid your real opinion won’t be accepted.",
"If you don’t follow now, you’ll probably never see us again."
]

watermark = "THE HUMAN CODE"

# ---------- CREATE IMAGE ----------
img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
draw = ImageDraw.Draw(img)

# ---------- TITLE ----------
y = 80
for tline in title.split("\n"):
    w = draw.textlength(tline, font=FONT_BOLD)
    draw.text(((WIDTH-w)/2, y), tline, fill=YELLOW, font=FONT_BOLD)
    y += 70

y += 40

# ---------- BODY ----------
num = 1
for i, line in enumerate(lines):
    text = f"{num}. {line}"

    color = YELLOW if i == len(lines)-1 else WHITE

    words = text.split()
    current = ""

    for word in words:
        test = current + word + " "
        w = draw.textlength(test, font=FONT_REG)

        if w > WIDTH - 160:
            draw.text((80, y), current, fill=color, font=FONT_REG)
            y += 55
            current = word + " "
        else:
            current = test

    draw.text((80, y), current, fill=color, font=FONT_REG)
    y += 55
    num += 1

# ---------- WATERMARK ----------
w = draw.textlength(watermark, font=FONT_REG)
draw.text(((WIDTH-w)/2, HEIGHT-60), watermark, fill=GRAY, font=FONT_REG)

# ---------- SAVE ----------
os.makedirs("output", exist_ok=True)
img.save("output/post.png")

print("✅ Image generated: output/post.png")
