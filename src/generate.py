import os, random, textwrap
from PIL import Image, ImageDraw, ImageFont

OUT="output"
os.makedirs(OUT,exist_ok=True)

W,H=1080,1080

FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def font(s):
    try: return ImageFont.truetype(FONT,s)
    except: return ImageFont.load_default()

TITLE=font(72)
BODY=font(40)
BIG=font(110)
WM=font(26)

DARK_BG=(10,10,10)
LIGHT_BG=(245,245,245)

WHITE=(240,240,240)
BLACK=(20,20,20)
GOLD=(255,185,0)
GREY=(120,120,120)

CTAS=[
"If you scroll past now, this may never find you again.",
"Most will scroll. Few will understand.",
"You noticed this for a reason.",
]

POSTS=[
("7","SIGNS YOU MIGHT BE TOO AVAILABLE",[
"You reply instantly to everyone.",
"You cancel plans for others.",
"You say yes when you want no.",
"You over-explain yourself.",
"You chase closure.",
"You fear disappointing people."
]),
("THE WALK AWAY","RULE",[
"If respect is missing, leave.",
"If effort is one-sided, leave.",
"If trust is forced, leave.",
"If peace disappears, leave.",
"If honesty is rare, leave.",
"If you feel smaller, leave."
])
]

def center(draw,t,f,y,c):
    b=draw.textbbox((0,0),t,font=f)
    w=b[2]-b[0]
    draw.text(((W-w)/2,y),t,font=f,fill=c)

def wrap(draw,t,f,y,c,width=30):
    for line in textwrap.wrap(t,width):
        b=draw.textbbox((0,0),line,font=f)
        h=b[3]-b[1]
        center(draw,line,f,y,c)
        y+=h+8
    return y

def slide(bg, text_color):
    return Image.new("RGB",(W,H),bg), text_color

def watermark(draw):
    center(draw,"THE HUMAN CODE",WM,H-50,GREY)

def make_carousel(topic,index):
    big, title, bullets = topic
    cta=random.choice(CTAS)

    # pattern break (20% light slides)
    if random.random()<0.2:
        BG=LIGHT_BG; TC=BLACK
    else:
        BG=DARK_BG; TC=WHITE

    # Slide 1 — Hook
    img,_=slide(BG,TC)
    d=ImageDraw.Draw(img)
    center(d,big,BIG,160,GOLD)
    wrap(d,title,TITLE,360,TC)
    watermark(d)
    img.save(f"{OUT}/post_{index}_1.png")

    # Slides 2-4 — bullets
    chunks=[bullets[i:i+2] for i in range(0,len(bullets),2)]
    s=2
    for ch in chunks[:3]:
        img,_=slide(BG,TC)
        d=ImageDraw.Draw(img)
        y=220
        for line in ch:
            y=wrap(d,line,BODY,y,TC)
            y+=20
        watermark(d)
        img.save(f"{OUT}/post_{index}_{s}.png")
        s+=1

    # Last slide — CTA
    img,_=slide(BG,TC)
    d=ImageDraw.Draw(img)
    wrap(d,cta,BODY,420,TC)
    watermark(d)
    img.save(f"{OUT}/post_{index}_{s}.png")

for i in range(3):
    make_carousel(random.choice(POSTS),i+1)

print("DONE ✅ V4.1 Carousel Generated")
