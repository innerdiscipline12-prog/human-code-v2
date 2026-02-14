import os
import random
from PIL import Image, ImageDraw, ImageFont
import imageio

# ========= SETTINGS =========

W, H = 1080, 1920
BG = (0,0,0)
YELLOW = (255,190,0)
WHITE = (240,240,240)
GREY = (150,150,150)

TITLE_FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
BODY_FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

os.makedirs("output", exist_ok=True)

quotes = [
"You tolerate repeated lies",
"You ignore red flags",
"You stay where you're drained",
"You chase those ignoring you",
"You accept less than you give",
"You seek constant approval",
"You avoid hard conversations",
"You excuse disrespect"
]

CTA = "If you scroll past now,\nthis may never find you again."

# ========= HELPERS =========

def wrap(draw, text, font, max_w):
    words = text.split()
    lines=[]
    cur=""
    for w in words:
        test = cur+" "+w if cur else w
        if draw.textlength(test,font=font) <= max_w:
            cur=test
        else:
            lines.append(cur)
            cur=w
    if cur: lines.append(cur)
    return lines

# ========= IMAGE =========

def make_image():
    img = Image.new("RGB",(W,H),BG)
    d = ImageDraw.Draw(img)

    title_f = ImageFont.truetype(TITLE_FONT,80)
    body_f = ImageFont.truetype(BODY_FONT,56)
    cta_f = ImageFont.truetype(BODY_FONT,42)

    # Title
    d.text((W//2,120),"TRUTHS ABOUT SELF-RESPECT",
           fill=YELLOW,font=title_f,anchor="mm")

    y=350
    chosen=random.sample(quotes,5)

    for i,q in enumerate(chosen,1):
        text=f"{i}. {q}"
        lines=wrap(d,text,body_f,900)
        for line in lines:
            d.text((W//2,y),line,fill=WHITE,font=body_f,anchor="mm")
            y+=70
        y+=25

    # CTA
    d.multiline_text((W//2,H-180),CTA,
                     fill=GREY,font=cta_f,
                     anchor="mm",align="center")

    img.save("output/image1.png")

# ========= CAROUSEL =========

def make_carousel():
    title_f = ImageFont.truetype(TITLE_FONT,72)
    body_f = ImageFont.truetype(BODY_FONT,56)

    selected=random.sample(quotes,6)

    for slide in range(3):
        img=Image.new("RGB",(W,H),BG)
        d=ImageDraw.Draw(img)

        d.text((W//2,140),"SELF-RESPECT CHECK",
               fill=YELLOW,font=title_f,anchor="mm")

        y=400
        for i in range(2):
            q=selected[slide*2+i]
            text=f"{slide*2+i+1}. {q}"
            d.text((W//2,y),text,
                   fill=WHITE,font=body_f,anchor="mm")
            y+=140

        img.save(f"output/carousel_{slide+1}.png")

# ========= REEL =========

def make_reel():
    frames=[]
    body_f = ImageFont.truetype(BODY_FONT,72)

    reel_lines=[
        "You become what",
        "you tolerate.",
        "",
        "Choose better."
    ]

    for line in reel_lines:
        img=Image.new("RGB",(W,H),BG)
        d=ImageDraw.Draw(img)

        d.text((W//2,H//2),line,
               fill=WHITE,font=body_f,anchor="mm")

        frames.append(img)

    # convert to video
    video_frames=[frame for frame in frames for _ in range(30)]
    imageio.mimsave("output/reel.mp4", video_frames, fps=10)

# ========= RUN =========

make_image()
make_carousel()
make_reel()

print("DONE ✅")
