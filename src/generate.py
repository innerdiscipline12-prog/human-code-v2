from PIL import Image, ImageDraw, ImageFont
import textwrap
import os
from datetime import datetime

# ========= SETTINGS =========

WIDTH = 1080
HEIGHT = 1350
BG_COLOR = (0,0,0)

TITLE_COLOR = (255,190,0)
TEXT_COLOR = (240,240,240)
CTA_COLOR = (255,190,0)
WATERMARK_COLOR = (90,90,90)

FONT_PATH = "src/Montserrat-Bold.ttf"

TITLE_SIZE = 64
TEXT_SIZE = 36
CTA_SIZE = 38
WATERMARK_SIZE = 24

OUTPUT_FOLDER = "output"
ARCHIVE_FOLDER = "archive"
MEMORY_FILE = "post_memory.txt"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(ARCHIVE_FOLDER, exist_ok=True)

# ========= SMART WRAP =========

def smart_wrap(line):
    line=line.strip()
    if len(line)<=55: return line
    if 56<=len(line)<=95: return textwrap.fill(line,width=42)
    if len(line)>95: return textwrap.fill(line,width=36)
    return line

# ========= AUTO MEMORY =========

def get_next_post_id(max_posts):
    if not os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE,"w") as f: f.write("0")

    with open(MEMORY_FILE,"r") as f:
        last=int(f.read().strip())

    nxt=last+1
    if nxt>=max_posts: nxt=0

    with open(MEMORY_FILE,"w") as f:
        f.write(str(nxt))

    return nxt

# ========= CONTENT BANK =========

content_bank = [

{
"title":"7 SIGNS YOU MIGHT BE\nTOO AVAILABLE",
"lines":[
"You reply instantly to everyone.",
"You cancel plans for people who wouldn’t do the same.",
"You over-explain your boundaries.",
"You say yes when you want to say no.",
"You chase closure from people who moved on.",
"You prioritize others over your own goals.",
"You tolerate low effort.",
"If you don’t follow now, you’ll probably never see us again."
]
},

{
"title":"7 DISCIPLINE\nTRUTHS",
"lines":[
"Motivation fades.",
"Standards stay.",
"Feelings fluctuate.",
"Structure wins.",
"Habits shape identity.",
"Comfort kills growth.",
"Consistency builds power.",
"If you don’t follow now, you’ll probably never see us again."
]
},

]

# ========= PICK TODAY =========

POST_ID = get_next_post_id(len(content_bank))
data = content_bank[POST_ID]

title = data["title"]
lines = data["lines"]

# ========= CREATE IMAGE =========

img = Image.new("RGB",(WIDTH,HEIGHT),BG_COLOR)
draw = ImageDraw.Draw(img)

title_font = ImageFont.truetype(FONT_PATH,TITLE_SIZE)
text_font = ImageFont.truetype(FONT_PATH,TEXT_SIZE)
cta_font = ImageFont.truetype(FONT_PATH,CTA_SIZE)
watermark_font = ImageFont.truetype(FONT_PATH,WATERMARK_SIZE)

y=120

# TITLE
for tline in title.split("\n"):
    w=draw.textlength(tline,font=title_font)
    draw.text(((WIDTH-w)/2,y),tline,font=title_font,fill=TITLE_COLOR)
    y+=70

y+=40

# BODY
number=1
caption_lines=[]

for line in lines:
    caption_lines.append(f"{number}. {line}")

    wrapped=smart_wrap(line)

    font=text_font
    color=TEXT_COLOR

    if number==len(lines):
        font=cta_font
        color=CTA_COLOR

    for wline in wrapped.split("\n"):
        text=f"{number}. {wline}" if wline==wrapped.split("\n")[0] else wline
        w=draw.textlength(text,font=font)
        draw.text(((WIDTH-w)/2,y),text,font=font,fill=color)
        y+=50

    y+=25
    number+=1

# WATERMARK
watermark="THE HUMAN CODE"
w=draw.textlength(watermark,font=watermark_font)
draw.text(((WIDTH-w)/2,HEIGHT-60),watermark,font=watermark_font,fill=WATERMARK_COLOR)

# SAVE IMAGE
today=datetime.now().strftime("%Y-%m-%d")

img.save(f"{OUTPUT_FOLDER}/post.png")
img.save(f"{ARCHIVE_FOLDER}/{today}.png")

# ========= AUTO CAPTIONS EXPORT =========

hashtags = "\n\n#discipline #selfcontrol #mindset #personalgrowth #psychology #focus #success"

caption_text = title.replace("\n"," ") + "\n\n" + "\n".join(caption_lines) + hashtags

with open(f"{OUTPUT_FOLDER}/captions.txt","w",encoding="utf-8") as f:
    f.write(caption_text)

with open(f"{ARCHIVE_FOLDER}/{today}.txt","w",encoding="utf-8") as f:
    f.write(caption_text)

print("DONE — Image + captions exported.")
