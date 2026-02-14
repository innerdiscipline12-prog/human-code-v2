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

content_bank = {
"title":"7 DARK TRUTHS\nABOUT HUMAN NATURE",
"lines":[
"People respect what they fear losing.",
"Attention is the real currency.",
"Silence reveals more than words.",
"Most loyalty is conditional.",
"Comfort kills ambition.",
"People test limits quietly.",
"Status changes treatment.",
"If you don’t follow now, you’ll probably never see us again."
]
},

{
"title":"7 SIGNS YOU’RE\nEASY TO REPLACE",
"lines":[
"You always agree.",
"You fear being disliked.",
"You over-explain yourself.",
"You tolerate disrespect.",
"You chase validation.",
"You avoid conflict.",
"You accept bare minimum.",
"If you don’t follow now, you’ll probably never see us again."
]
},

{
"title":"7 REALITIES\nABOUT STATUS",
"lines":[
"Status changes tone.",
"People respect power.",
"Visibility creates value.",
"Success attracts loyalty.",
"Money amplifies voice.",
"Results silence doubt.",
"Perception shapes treatment.",
"If you don’t follow now, you’ll probably never see us again."
]
},

{
"title":"7 BRUTAL\nSOCIAL TRUTHS",
"lines":[
"Nice is often ignored.",
"Confidence beats kindness.",
"Attention favors boldness.",
"People follow strength.",
"Softness gets tested.",
"Fear drives respect.",
"Silence intimidates.",
"If you don’t follow now, you’ll probably never see us again."
]
},

{
"title":"7 SIGNS YOU\nSEEK APPROVAL",
"lines":[
"You hate saying no.",
"You explain your choices.",
"You fear rejection.",
"You copy others.",
"You doubt decisions.",
"You need praise.",
"You avoid judgment.",
"If you don’t follow now, you’ll probably never see us again."
]
},

{
"title":"7 HARSH\nLIFE REALITIES",
"lines":[
"Effort isn’t always rewarded.",
"People forget favors.",
"Fairness is rare.",
"Comfort traps growth.",
"Trust is fragile.",
"Respect must be earned.",
"Silence speaks power.",
"If you don’t follow now, you’ll probably never see us again."
]
},

{
"title":"7 DARK TRUTHS\nABOUT FRIENDS",
"lines":[
"Some compete quietly.",
"Some celebrate your fall.",
"Some envy your growth.",
"Some stay for benefit.",
"Some copy your moves.",
"Some hide resentment.",
"Few are genuine.",
"If you don’t follow now, you’ll probably never see us again."
]
},

{
"title":"7 SIGNS YOU\nOVERCARE",
"lines":[
"You reply instantly.",
"You prioritize others.",
"You forgive too fast.",
"You ignore red flags.",
"You chase closure.",
"You fear distance.",
"You accept crumbs.",
"If you don’t follow now, you’ll probably never see us again."
]
},

{
"title":"7 POWER\nREALITIES",
"lines":[
"Control earns respect.",
"Calm signals power.",
"Silence dominates.",
"Boundaries command value.",
"Presence speaks first.",
"Restraint intimidates.",
"Focus builds authority.",
"If you don’t follow now, you’ll probably never see us again."
]
},

{
"title":"7 DARK TRUTHS\nABOUT PEOPLE",
"lines":[
"People test limits.",
"People copy winners.",
"People follow status.",
"People respect scarcity.",
"People chase value.",
"People fear loss.",
"People admire power.",
"If you don’t follow now, you’ll probably never see us again."
]
},

{
"title":"7 SIGNS YOU’RE\nTOO AVAILABLE",
"lines":[
"You answer anytime.",
"You cancel plans.",
"You wait on others.",
"You accept last-minute.",
"You chase attention.",
"You tolerate delays.",
"You fear missing out.",
"If you don’t follow now, you’ll probably never see us again."
]
},

{
"title":"7 TRUTHS\nABOUT RESPECT",
"lines":[
"Respect silence.",
"Respect boundaries.",
"Respect control.",
"Respect standards.",
"Respect discipline.",
"Respect presence.",
"Respect restraint.",
"If you don’t follow now, you’ll probably never see us again."
]
},

{
"title":"7 REALITIES\nABOUT VALUE",
"lines":[
"Scarcity increases value.",
"Silence builds mystery.",
"Control shows strength.",
"Distance creates respect.",
"Focus earns status.",
"Standards filter people.",
"Presence commands attention.",
"If you don’t follow now, you’ll probably never see us again."
]
},

{
"title":"7 DARK\nPSYCHOLOGY TRUTHS",
"lines":[
"People mirror confidence.",
"People test weakness.",
"People chase status.",
"People value scarcity.",
"People respect control.",
"People admire calm.",
"People follow power.",
"If you don’t follow now, you’ll probably never see us again."
]
},

{
"title":"7 SIGNS YOU\nLACK BOUNDARIES",
"lines":[
"You say yes fast.",
"You fear conflict.",
"You accept disrespect.",
"You avoid saying no.",
"You over-give.",
"You tolerate misuse.",
"You explain limits.",
"If you don’t follow now, you’ll probably never see us again."
]
},

{
"title":"7 HARSH\nRELATIONSHIP TRUTHS",
"lines":[
"Effort reveals interest.",
"Consistency shows care.",
"Silence shows distance.",
"Respect shows love.",
"Time shows priority.",
"Actions show truth.",
"Excuses show intent.",
"If you don’t follow now, you’ll probably never see us again."
]
},

{
"title":"7 TRUTHS\nABOUT DISCIPLINE",
"lines":[
"Discipline beats mood.",
"Standards beat feelings.",
"Structure beats chaos.",
"Habits beat motivation.",
"Consistency beats hype.",
"Control beats impulse.",
"Focus beats distraction.",
"If you don’t follow now, you’ll probably never see us again."
]
},

{
"title":"7 SIGNS\nYOU’RE TOO NICE",
"lines":[
"You avoid saying no.",
"You forgive easily.",
"You tolerate disrespect.",
"You seek approval.",
"You fear tension.",
"You over-help.",
"You accept less.",
"If you don’t follow now, you’ll probably never see us again."
]
},

{
"title":"7 REALITIES\nABOUT POWER",
"lines":[
"Power is quiet.",
"Power is calm.",
"Power is controlled.",
"Power is patient.",
"Power is focused.",
"Power is reserved.",
"Power is disciplined.",
"If you don’t follow now, you’ll probably never see us again."
]
},

{
"title":"7 DARK\nSUCCESS TRUTHS",
"lines":[
"Success isolates.",
"Success attracts envy.",
"Success reveals loyalty.",
"Success changes circles.",
"Success demands sacrifice.",
"Success tests character.",
"Success exposes people.",
"If you don’t follow now, you’ll probably never see us again."
]
},

{
"title":"7 SIGNS YOU\nOVER-TRUST",
"lines":[
"You share quickly.",
"You believe words.",
"You ignore signs.",
"You defend liars.",
"You trust easily.",
"You forgive patterns.",
"You expect honesty.",
"If you don’t follow now, you’ll probably never see us again."
]
},

{
"title":"7 TRUTHS\nABOUT SILENCE",
"lines":[
"Silence intimidates.",
"Silence controls rooms.",
"Silence reveals people.",
"Silence protects power.",
"Silence builds mystery.",
"Silence signals strength.",
"Silence speaks volumes.",
"If you don’t follow now, you’ll probably never see us again."
]
},

{
"title":"7 DARK\nLOYALTY TRUTHS",
"lines":[
"Loyalty is tested.",
"Loyalty is rare.",
"Loyalty is quiet.",
"Loyalty needs respect.",
"Loyalty needs value.",
"Loyalty needs honesty.",
"Loyalty needs boundaries.",
"If you don’t follow now, you’ll probably never see us again."
]
},

{
"title":"7 SIGNS YOU\nCHASE PEOPLE",
"lines":[
"You text first.",
"You double text.",
"You wait replies.",
"You excuse behavior.",
"You over-invest.",
"You seek attention.",
"You fear distance.",
"If you don’t follow now, you’ll probably never see us again."
]
},

{
"title":"7 HARSH\nEGO TRUTHS",
"lines":[
"Ego blocks growth.",
"Ego fears truth.",
"Ego hates silence.",
"Ego seeks praise.",
"Ego avoids blame.",
"Ego rejects limits.",
"Ego resists change.",
"If you don’t follow now, you’ll probably never see us again."
]
},

{
"title":"7 DARK TRUTHS\nABOUT ATTENTION",
"lines":[
"Attention is borrowed.",
"Attention follows value.",
"Attention fades fast.",
"Attention is selective.",
"Attention rewards rarity.",
"Attention respects presence.",
"Attention follows power.",
"If you don’t follow now, you’ll probably never see us again."
]
},

{
"title":"7 SIGNS YOU’RE\nEMOTIONALLY READABLE",
"lines":[
"Your face reveals stress.",
"Your tone shows doubt.",
"Your silence shows hurt.",
"Your reactions expose you.",
"Your eyes show fear.",
"Your words leak feelings.",
"Your mood is visible.",
"If you don’t follow now, you’ll probably never see us again."
]
},

{
"title":"7 HARSH\nREALITY CHECKS",
"lines":[
"No one owes support.",
"Effort isn’t guaranteed reward.",
"People choose convenience.",
"Feelings don’t equal truth.",
"Trust can expire.",
"Time exposes lies.",
"Results silence talk.",
"If you don’t follow now, you’ll probably never see us again."
]
},

{
"title":"7 DARK TRUTHS\nABOUT SUCCESS",
"lines":[
"Success changes friendships.",
"Success attracts fakes.",
"Success reveals envy.",
"Success creates distance.",
"Success isolates quietly.",
"Success raises standards.",
"Success exposes motives.",
"If you don’t follow now, you’ll probably never see us again."
]
},

{
"title":"7 SIGNS YOU\nFEAR REJECTION",
"lines":[
"You over-please.",
"You apologize often.",
"You avoid honesty.",
"You hide opinions.",
"You fear silence.",
"You seek approval.",
"You avoid risk.",
"If you don’t follow now, you’ll probably never see us again."
]
},

{
"title":"7 TRUTHS\nABOUT CONTROL",
"lines":[
"Control beats chaos.",
"Control beats emotion.",
"Control beats impulse.",
"Control shows power.",
"Control earns respect.",
"Control builds presence.",
"Control protects value.",
"If you don’t follow now, you’ll probably never see us again."
]
},

{
"title":"7 DARK\nPEOPLE TRUTHS",
"lines":[
"People protect self-interest.",
"People follow advantage.",
"People admire winners.",
"People copy confidence.",
"People test weakness.",
"People value scarcity.",
"People respect power.",
"If you don’t follow now, you’ll probably never see us again."
]
},

{
"title":"7 SIGNS YOU’RE\nTOO TRUSTING",
"lines":[
"You believe promises.",
"You ignore patterns.",
"You forgive lies.",
"You defend betrayers.",
"You share secrets.",
"You expect honesty.",
"You trust words.",
"If you don’t follow now, you’ll probably never see us again."
]
},

{
"title":"7 REALITIES\nABOUT FRIENDSHIPS",
"lines":[
"Some compete quietly.",
"Some compare silently.",
"Some stay for gain.",
"Some hide jealousy.",
"Some copy success.",
"Few stay loyal.",
"Time reveals truth.",
"If you don’t follow now, you’ll probably never see us again."
]
},

{
"title":"7 DARK TRUTHS\nABOUT VALUE",
"lines":[
"Value attracts respect.",
"Value creates demand.",
"Value needs scarcity.",
"Value needs standards.",
"Value needs discipline.",
"Value filters people.",
"Value builds power.",
"If you don’t follow now, you’ll probably never see us again."
]
},

{
"title":"7 SIGNS YOU’RE\nOVER-AVAILABLE",
"lines":[
"You reply instantly.",
"You wait on others.",
"You cancel plans.",
"You say yes always.",
"You accept delays.",
"You chase replies.",
"You fear missing out.",
"If you don’t follow now, you’ll probably never see us again."
]
},

{
"title":"7 HARSH\nTRUTH BOMBS",
"lines":[
"Not all support you.",
"Not all clap for you.",
"Not all mean well.",
"Not all stay loyal.",
"Not all want growth.",
"Not all wish success.",
"Not all are real.",
"If you don’t follow now, you’ll probably never see us again."
]
},

{
"title":"7 TRUTHS\nABOUT SILENCE",
"lines":[
"Silence controls rooms.",
"Silence shows strength.",
"Silence hides strategy.",
"Silence builds mystery.",
"Silence filters noise.",
"Silence protects power.",
"Silence speaks loud.",
"If you don’t follow now, you’ll probably never see us again."
]
},

{
"title":"7 DARK\nLOYALTY REALITIES",
"lines":[
"Loyalty gets tested.",
"Loyalty needs value.",
"Loyalty needs respect.",
"Loyalty needs honesty.",
"Loyalty is rare.",
"Loyalty is proven.",
"Loyalty is quiet.",
"If you don’t follow now, you’ll probably never see us again."
]
},

{
"title":"7 SIGNS YOU\nSEEK VALIDATION",
"lines":[
"You post for praise.",
"You check reactions.",
"You need approval.",
"You fear criticism.",
"You copy trends.",
"You chase likes.",
"You doubt yourself.",
"If you don’t follow now, you’ll probably never see us again."
]
},

{
"title":"7 REALITIES\nABOUT STATUS",
"lines":[
"Status changes tone.",
"Status attracts attention.",
"Status gains respect.",
"Status shifts behavior.",
"Status raises value.",
"Status filters circles.",
"Status influences treatment.",
"If you don’t follow now, you’ll probably never see us again."
]
},

{
"title":"7 DARK TRUTHS\nABOUT EGO",
"lines":[
"Ego fears truth.",
"Ego blocks growth.",
"Ego hates silence.",
"Ego avoids blame.",
"Ego resists change.",
"Ego seeks praise.",
"Ego hides weakness.",
"If you don’t follow now, you’ll probably never see us again."
]
},

{
"title":"7 SIGNS YOU’RE\nTOO PASSIVE",
"lines":[
"You avoid conflict.",
"You stay silent.",
"You tolerate disrespect.",
"You accept less.",
"You fear speaking.",
"You suppress needs.",
"You avoid tension.",
"If you don’t follow now, you’ll probably never see us again."
]
},

{
"title":"7 POWER\nPRINCIPLES",
"lines":[
"Calm wins respect.",
"Control shows strength.",
"Focus builds authority.",
"Standards build value.",
"Discipline builds power.",
"Presence commands rooms.",
"Restraint intimidates.",
"If you don’t follow now, you’ll probably never see us again."
]
},

{
"title":"7 DARK\nSOCIAL REALITIES",
"lines":[
"People judge quickly.",
"People follow status.",
"People copy success.",
"People fear power.",
"People admire control.",
"People test limits.",
"People respect strength.",
"If you don’t follow now, you’ll probably never see us again."
]
},

{
"title":"7 SIGNS YOU\nOVERSHARE",
"lines":[
"You reveal plans.",
"You share emotions.",
"You talk too much.",
"You explain goals.",
"You expose moves.",
"You vent publicly.",
"You leak feelings.",
"If you don’t follow now, you’ll probably never see us again."
]
},

{
"title":"7 TRUTHS\nABOUT DISCIPLINE",
"lines":[
"Discipline beats mood.",
"Habits beat hype.",
"Structure beats chaos.",
"Standards beat feelings.",
"Focus beats distraction.",
"Consistency builds identity.",
"Control builds power.",
"If you don’t follow now, you’ll probably never see us again."
]
},

{
"title":"7 DARK\nRESPECT TRUTHS",
"lines":[
"Respect calm minds.",
"Respect boundaries.",
"Respect discipline.",
"Respect presence.",
"Respect standards.",
"Respect control.",
"Respect silence.",
"If you don’t follow now, you’ll probably never see us again."
]
},

{
"title":"7 SIGNS YOU\nPEOPLE-PLEASE",
"lines":[
"You fear saying no.",
"You over-give.",
"You avoid tension.",
"You accept crumbs.",
"You seek praise.",
"You tolerate misuse.",
"You hide needs.",
"If you don’t follow now, you’ll probably never see us again."
]
},

{
"title":"7 HARSH\nGROWTH TRUTHS",
"lines":[
"Growth feels lonely.",
"Growth needs sacrifice.",
"Growth demands discipline.",
"Growth requires focus.",
"Growth filters people.",
"Growth tests patience.",
"Growth changes circles.",
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
