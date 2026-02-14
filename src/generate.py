import os
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageSequenceClip

W,H = 1080,1920
BG=(0,0,0)
YELLOW=(255,190,0)
WHITE=(240,240,240)

TITLE="SELF-RESPECT CHECK"

LINES=[
"1. You ignore red flags",
"2. You seek constant approval",
"3. You chase those ignoring you",
"4. You accept less than you give",
"5. You avoid hard conversations",
"6. If you scroll past now, this may never find you again."
]

os.makedirs("output",exist_ok=True)

title_font=ImageFont.truetype("DejaVuSans-Bold.ttf",90)
text_font=ImageFont.truetype("DejaVuSans-Bold.ttf",60)
wm_font=ImageFont.truetype("DejaVuSans-Bold.ttf",36)

# ===== IMAGE =====
def make_img(lines,name):
    img=Image.new("RGB",(W,H),BG)
    d=ImageDraw.Draw(img)

    d.text((80,120),TITLE,font=title_font,fill=YELLOW)

    y=380
    for l in lines:
        d.text((120,y),l,font=text_font,fill=WHITE)
        y+=120

    d.text((W//2-160,H-120),"THE HUMAN CODE",font=wm_font,fill=(120,120,120))
    img.save(f"output/{name}")

make_img(LINES,"image.png")

# ===== CAROUSEL =====
chunks=[LINES[0:2],LINES[2:4],LINES[4:6]]
for i,c in enumerate(chunks):
    make_img(c,f"carousel_{i+1}.png")

# ===== REEL =====
frames=[]
for line in LINES:
    img=Image.new("RGB",(W,H),BG)
    d=ImageDraw.Draw(img)

    d.text((80,120),TITLE,font=title_font,fill=YELLOW)
    d.text((120,900),line,font=text_font,fill=WHITE)

    frame_path=f"output/frame_{len(frames)}.png"
    img.save(frame_path)
    frames.append(frame_path)

clip=ImageSequenceClip(frames,fps=1)
clip.write_videofile("output/reel.mp4",fps=24)

print("DONE")
