from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

# ========= SETTINGS =========

WIDTH = 1080
HEIGHT = 1350
BG_COLOR = (0,0,0)

TITLE_COLOR = (255,190,0)
TEXT_COLOR = (240,240,240)
CTA_COLOR = (255,190,0)
WATERMARK_COLOR = (90,90,90)

FONT_PATH = "Montserrat-Bold.ttf"

TITLE_SIZE = 64
TEXT_SIZE = 36
CTA_SIZE = 38
WATERMARK_SIZE = 24

OUTPUT_FOLDER = "output"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ========= SMART WRAP (V4 ELITE) =========

def smart_wrap(line):
    line=line.strip()

    if len(line)<=55:
        return line

    if 56<=len(line)<=95:
        return textwrap.fill(line,width=42)

    if len(line)>95:
        return textwrap.fill(line,width=36)

    return line

# ========= CONTENT =========

title = "7 SIGNS YOU MIGHT BE\nTOXIC TO YOURSELF"

lines = [
"You say sorry for things that were never your fault.",
"You tolerate people who shrink your confidence.",
"You keep checking your phone, waiting for texts that don’t come.",
"You treat every piece of feedback like it’s an attack on your worth.",
"You measure your life against everyone else’s highlight reel.",
"You sleep more to escape, not to rest.",
"You agree with everything because you’re afraid your real opinion won’t be accepted.",
"If you don’t follow now, you’ll probably never see us again."
]

# ========= CREATE IMAGE =========

img = Image.new("RGB",(WIDTH,HEIGHT),BG_COLOR)
draw = ImageDraw.Draw(img)

title_font = ImageFont.truetype(FONT_PATH,TITLE_SIZE)
text_font = ImageFont.truetype(FONT_PATH,TEXT_SIZE)
cta_font = ImageFont.truetype(FONT_PATH,CTA_SIZE)
watermark_font = ImageFont.truetype(FONT_PATH,WATERMARK_SIZE)

# ========= DRAW TITLE =========

y = 120

for tline in title.split("\n"):
    w = draw.textlength(tline,font=title_font)
    draw.text(((WIDTH-w)/2,y),tline,font=title_font,fill=TITLE_COLOR)
    y+=70

y+=40

# ========= DRAW LIST =========

number=1

for line in lines:

    wrapped = smart_wrap(line)

    font = text_font
    color = TEXT_COLOR

    if number==len(lines):
        font = cta_font
        color = CTA_COLOR

    wrapped_lines = wrapped.split("\n")

    for wline in wrapped_lines:
        text = f"{number}. {wline}" if wline==wrapped_lines[0] else wline

        w = draw.textlength(text,font=font)
        draw.text(((WIDTH-w)/2,y),text,font=font,fill=color)

        y+=50

    y+=25
    number+=1

# ========= WATERMARK =========

watermark="THE HUMAN CODE"
w = draw.textlength(watermark,font=watermark_font)
draw.text(((WIDTH-w)/2,HEIGHT-60),watermark,font=watermark_font,fill=WATERMARK_COLOR)

# ========= SAVE =========

img.save(f"{OUTPUT_FOLDER}/post.png")

print("DONE — Saved to output/post.png")
