from PIL import Image, ImageDraw, ImageFont
import random, os

W, H = 1080, 1080

os.makedirs("output", exist_ok=True)

quotes = [
"People reveal priorities through repeated actions.",
"Silence often exposes more than conversation.",
"Habits decide futures quietly.",
"Discipline removes emotional negotiation.",
"Attention is your real currency.",
"Consistency builds invisible authority.",
"Comfort delays potential.",
"Self-control is private power.",
"Patterns predict behavior.",
"Environment shapes decisions."
]

def make_slide(text, i):
    img = Image.new("RGB",(W,H),(0,0,0))
    d = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf",60)
    except:
        font = ImageFont.load_default()

    lines = []
    words = text.split()
    line=""

    for w in words:
        if len(line+w) < 18:
            line+=w+" "
        else:
            lines.append(line)
            line=w+" "
    lines.append(line)

    y=H//2 - len(lines)*35

    for l in lines:
        w,h = d.textsize(l,font=font)
        d.text(((W-w)//2,y),l,font=font,fill=(255,215,0))
        y+=80

    img.save(f"output/post_{i}.png")

for i in range(5):
    make_slide(random.choice(quotes),i)

print("Done")
