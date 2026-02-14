import os
import random
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1080
RW, RH = 1080, 1920
DURATION = 7

os.makedirs("output/images", exist_ok=True)
os.makedirs("output/reels", exist_ok=True)

quotes = [
    "You become what you tolerate.",
    "Discipline reveals priorities.",
    "Silence exposes truth.",
    "Habits decide futures.",
    "Attention shapes reality.",
    "Consistency builds identity.",
    "Control your inputs.",
]

CTA = "If you scroll past now, this may never find you again."

def font(size):
    try:
        return ImageFont.truetype("DejaVuSans-Bold.ttf", size)
    except:
        return ImageFont.load_default()

def make_image(text, size=(1080,1080)):
    img = Image.new("RGB", size, (10,10,10))
    draw = ImageDraw.Draw(img)
    f = font(60)

    words = text.split()
    lines, line = [], ""
    for w in words:
        if len(line+w) < 16:
            line += w+" "
        else:
            lines.append(line)
            line = w+" "
    lines.append(line)

    y = size[1]//2 - 100
    for l in lines:
        bbox = draw.textbbox((0,0), l, font=f)
        w = bbox[2]-bbox[0]
        draw.text(((size[0]-w)//2,y), l, fill="white", font=f)
        y+=80

    return img

# ---------- GENERATE ----------
for i in range(5):

    quote = random.choice(quotes)

    # IMAGE POST
    img = make_image(quote,(W,H))
    img_path = f"output/images/post_{i+1}.png"
    img.save(img_path)

    # REEL
    reel_img = make_image(quote,(RW,RH))
    cta_img = make_image(CTA,(RW,RH))

    reel_img.save("temp1.png")
    cta_img.save("temp2.png")

    clip1 = ImageClip("temp1.png").set_duration(DURATION-2)
    clip2 = ImageClip("temp2.png").set_duration(2)

    final = concatenate_videoclips([clip1,clip2])
    final.write_videofile(
        f"output/reels/reel_{i+1}.mp4",
        fps=24,
        codec="libx264",
        audio=False
    )

print("DONE ✅ 5 images + 5 reels created")
