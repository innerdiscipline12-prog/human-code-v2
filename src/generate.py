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

content_bank = titles = [

"7 DARK TRUTHS ABOUT HUMAN NATURE",
"7 SIGNS PEOPLE READ YOU EASILY",
"7 UNCOMFORTABLE REALITIES",
"7 SIGNS YOU’RE EASY TO REPLACE",
"7 DARK TRUTHS ABOUT ATTENTION",
"7 SIGNS PEOPLE TEST YOUR LIMITS",
"7 REALITIES ABOUT RESPECT",
"7 SIGNS YOU’RE TOO PREDICTABLE",
"7 DARK TRUTHS ABOUT SOCIAL LIFE",
"7 SIGNS PEOPLE DON’T FEAR LOSING YOU",
"7 REALITIES ABOUT STATUS",
"7 SIGNS YOU’RE TOO NICE",
"7 DARK TRUTHS ABOUT FRIENDSHIPS",
"7 SIGNS YOU OVERVALUE PEOPLE",
"7 REALITIES ABOUT POWER",
"7 SIGNS YOU’RE EMOTIONALLY READABLE",
"7 DARK TRUTHS ABOUT LOYALTY",
"7 SIGNS YOU’RE TAKEN FOR GRANTED",
"7 REALITIES ABOUT HUMAN EGO",
"7 SIGNS YOU SEEK Approval",
"7 DARK TRUTHS ABOUT CLOSENESS",
"7 SIGNS PEOPLE USE YOU QUIETLY",
"7 REALITIES ABOUT TRUST",
"7 SIGNS YOU’RE TOO AVAILABLE",
"7 DARK TRUTHS ABOUT KINDNESS",
"7 SIGNS YOU LOOK EASY TO HANDLE",
"7 REALITIES ABOUT PERCEPTION",
"7 SIGNS PEOPLE DON’T TAKE YOU SERIOUSLY",
"7 DARK TRUTHS ABOUT VALUE",
"7 SIGNS YOU’RE TOO OPEN",
"7 REALITIES ABOUT HUMAN INTEREST",
"7 SIGNS YOU’RE EASY TO READ",
"7 DARK TRUTHS ABOUT PEOPLE",
"7 SIGNS YOU SHOW YOUR HAND",
"7 REALITIES ABOUT PRIORITY",
"7 SIGNS YOU’RE AN OPTION",
"7 DARK TRUTHS ABOUT ATTACHMENT",
"7 SIGNS YOU’RE TOO FORGIVING",
"7 REALITIES ABOUT REPLACEMENT",
"7 SIGNS YOU’RE TOO ACCESSIBLE",
"7 DARK TRUTHS ABOUT EFFORT",
"7 SIGNS YOU LOOK LOW-RISK",
"7 REALITIES ABOUT SOCIAL VALUE",
"7 SIGNS YOU’RE TOO TRUSTING",
"7 DARK TRUTHS ABOUT RELATIONSHIPS",
"7 SIGNS YOU’RE EASY TO LOSE",
"7 REALITIES ABOUT HUMAN FOCUS",
"7 SIGNS YOU’RE NOT A PRIORITY",
"7 DARK TRUTHS ABOUT TIME",
"7 SIGNS YOU’RE QUIETLY DISRESPECTED"
]

line_pool = [

"People value what feels scarce.",
"Familiarity reduces perceived value.",
"Attention follows status.",
"People test limits silently.",
"Kindness without boundaries invites use.",
"Availability lowers urgency.",
"Predictability reduces intrigue.",
"Silence makes people curious.",
"Too much access removes mystery.",
"People respect what they can lose.",
"Emotional reactions reveal leverage.",
"Over-explaining signals insecurity.",
"Quick replies lower perceived demand.",
"People mirror your standards.",
"Low boundaries attract pressure.",
"Forgiveness without change invites repeats.",
"People protect advantage first.",
"Interest follows perceived value.",
"Consistency without respect breeds comfort.",
"People invest where reward exists.",
"Attention is a social currency.",
"People notice withdrawal more than presence.",
"Too much honesty removes leverage.",
"People read patterns quickly.",
"Soft limits get crossed.",
"People remember how you react.",
"Desperation is sensed, not heard.",
"People test tolerance quietly.",
"Low friction lowers value.",
"People respect resistance.",
"Emotional control raises presence.",
"People chase what feels distant.",
"Familiar access lowers excitement.",
"People protect their interests first.",
"Too much availability invites delay.",
"People reward perceived status.",
"Respect grows with boundaries.",
"People value what feels selective.",
"Calm detachment shifts power.",
"People track your reactions.",
"Over-giving creates imbalance.",
"People notice who adjusts.",
"Unclear standards invite trials.",
"People invest where effort matters.",
"Too much openness removes edge.",
"People value self-control.",
"Withdrawal reveals true interest.",
"People respond to limits.",
"Uncertainty creates attention.",
"People protect leverage.",
"Control attracts respect.",
"People read emotional cues fast.",
"Distance increases perceived value.",
"People test quiet personalities.",
"Reactions teach others how to treat you.",
"People notice restraint.",
"Value rises with selectiveness.",
"People respect self-containment.",
"Over-availability looks replaceable.",
"People track social worth.",
"Attention moves to rarity.",
"People respect firmness.",
"Softness invites testing.",
"People adjust to your tolerance.",
"Control shapes perception.",
"People read your pace.",
"Silence builds weight.",
"People value calm presence.",
"Quick access lowers curiosity.",
"People invest selectively.",
"Boundaries define value.",
"People measure reactions.",
"Too much clarity removes tension.",
"People protect their image.",
"Status influences attention.",
"People respect emotional discipline.",
"Scarcity shapes interest.",
"People track social signals.",
"Calm detachment signals strength.",
"People mirror your standards.",
"Firm limits deter misuse.",
"People value composure.",
"Predictability reduces impact.",
"People notice who stays steady.",
"Emotional restraint builds gravity.",
"People respect self-control.",
"Too much warmth invites assumption.",
"People value selective energy.",
"Consistency builds quiet power.",
"People notice emotional shifts.",
"Distance sharpens interest.",
"People value restraint.",
"Control creates presence.",
"People read subtle cues.",
"Selective access raises value.",
"People respect calm authority.",
"Too much effort lowers mystery.",
"People value perceived demand.",
"Composure builds influence.",
"People notice detachment.",
"Scarcity increases attention.",
"People value emotional control.",
"Measured responses build weight.",
"People read behavior deeply.",
"Boundaries create respect.",
"People track reactions.",
"Silence adds presence.",
"People value limits.",
"Composure signals strength.",
"People read consistency.",
"Emotional control attracts respect.",
"Distance creates curiosity.",
"People value firmness.",
"Control shapes reputation.",
"People notice selectiveness.",
"Restraint builds power.",
"People respect boundaries.",
"Calm presence influences perception.",
"People value quiet confidence.",
"Too much exposure lowers intrigue.",
"People value mystery.",
"Controlled energy attracts respect.",
"People notice who withdraws.",
"Scarcity drives attention.",
"People respect discipline.",
"Presence grows with control.",
"People value calm strength.",
"Detachment changes dynamics.",
"People respect limits.",
"Composure holds power.",
"People value subtlety.",
"Measured distance builds value.",
"People notice self-control.",
"Restraint earns respect.",
"People value steadiness.",
"Quiet discipline builds presence.",
"People track emotional stability.",
"Control attracts attention.",
"People respect calm minds.",
"Selective energy signals value.",
"People value distance.",
"Composure influences perception.",
"Calm control builds gravity.",
"People value inner restraint.",
"Stability commands respect.",
"People respect controlled presence.",
"Detachment reveals value.",
"Control defines power.",
"People respect calm discipline."
]

cta_pool = [

"Follow for deeper human truths.",
"Follow for dark psychology insights.",
"Follow if you observe people closely.",
"Follow for real human behavior.",
"Follow for quiet psychological truths.",
"Follow for deeper awareness.",
"Follow if you value perception.",
"Follow for mental sharpness.",
"Follow for psychological insight.",
"Follow for human nature truths."
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
