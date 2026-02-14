import os
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import *

# ========= SETTINGS =========
W, H = 1080, 1920
BG = (0,0,0)
YELLOW = (255,190,0)
WHITE = (240,240,240)

TITLE = "SELF-RESPECT CHECK"

LINES = [
"1. You ignore red flags",
"2. You seek constant approval",
"3. You chase those ignoring you",
"4. You accept less than you give",
"5. You avoid hard conversations",
"6. If you scroll past now, this may never find you again."
]

WATERMARK = "THE HUMAN CODE"

os.makedirs("output", exist_ok=True)

# ========= FONT =========
# Default bold system font
title_font = ImageFont.truetype("DejaVuSans-Bold.ttf", 90)
text_font = ImageFont.truetype("DejaVuSans-Bold.ttf", 56)
wm_font = ImageFont.truetype("DejaVuSans-Bold.ttf", 36)

# ========= IMAGE FUNCTION =========
def make_image(lines, filename):
    img = Image.new("RGB",(W,H),BG)
    d = ImageDraw.Draw(img)

    # Title
    d.text((80,120), TITLE, font=title_font, fill=YELLOW)

    y = 380
    for line in lines:
        d.text((120,y), line, font=text_font, fill=WHITE)
        y += 120

    # Watermark bottom center
    d.text((W//2-170,H-120), WATERMARK, font=wm_font, fill=(120,120,120))

    img.save(f"output/{filename}")

# ========= MAIN IMAGE =========
make_image(LINES, "image.png")

# ========= CAROUSEL =========
chunks = [
LINES[0:2],
LINES[2:4],
LINES[4:6],
]

for i,c in enumerate(chunks):
    make_image(c, f"carousel_{i+1}.png")

# ========= REEL =========
clips = []
for line in LINES:
    txt = TextClip(
        line,
        fontsize=80,
        font="DejaVu-Sans-Bold",
        color="white",
        size=(900,None),
        method="caption"
    ).set_position("center").set_duration(1.4)

    bg = ColorClip((W,H), color=(0,0,0), duration=1.4)
    clips.append(CompositeVideoClip([bg,txt]))

final = concatenate_videoclips(clips, method="compose")
final.write_videofile("output/reel.mp4", fps=24)

print("DONE.")
