from PIL import Image, ImageDraw, ImageFont
import textwrap
import os
import json
import random

# ========= SETTINGS =========

WIDTH = 1080
HEIGHT = 1350
BG_COLOR = (0, 0, 0)

TITLE_COLOR = (255, 190, 0)
TEXT_COLOR = (240, 240, 240)
CTA_COLOR = (255, 190, 0)
WATERMARK_COLOR = (90, 90, 90)
QUOTE_COLOR = (200, 200, 200)
ACCENT_COLOR = (255, 190, 0)

FONT_PATH = "src/Montserrat-Bold.ttf"

TITLE_SIZE = 64
TEXT_SIZE = 36
CTA_SIZE = 38
WATERMARK_SIZE = 24
QUOTE_SIZE = 44
QUOTE_LABEL_SIZE = 26
COVER_TITLE_SIZE = 62

OUTPUT_FOLDER = "output"
STATE_FILE = "state.json"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ========= WRAP =========

def smart_wrap(line):
    if len(line) <= 55:
        return line
    if len(line) <= 95:
        return textwrap.fill(line, width=42)
    return textwrap.fill(line, width=36)

def wrap_quote(line, width=30):
    return textwrap.fill(line, width=width)

# ========= TITLE POOLS =========

title_part1 = [
    "DARK TRUTHS",
    "HARSH REALITIES",
    "BRUTAL TRUTHS",
    "PSYCHOLOGICAL TRUTHS",
    "UNCOMFORTABLE TRUTHS",
    "SOCIAL TRUTHS",
    "COLD FACTS",
    "HIDDEN LAWS",
    "SILENT RULES",
    "UNSPOKEN TRUTHS",
]

title_part2 = [
    "ABOUT PEOPLE",
    "ABOUT POWER",
    "ABOUT RESPECT",
    "ABOUT HUMAN NATURE",
    "ABOUT STATUS",
    "ABOUT EGO",
    "ABOUT CONTROL",
    "ABOUT LOYALTY",
    "ABOUT INFLUENCE",
    "ABOUT MINDSET",
    "ABOUT SUCCESS",
    "ABOUT WEAKNESS",
]

# ========= LINE POOL =========

line_pool = [
    # Power & Control
    "Power is maintained through mystery.",
    "People obey confidence, not credentials.",
    "Those who need approval lose control.",
    "Influence is built in private.",
    "The one who cares less holds more power.",
    "Control your reactions, control the room.",
    "People exploit predictability.",
    "Authority is felt before it is spoken.",
    "The quietest person often runs the room.",
    "Dependence is the oldest form of control.",

    # Human Nature
    "Everyone acts in their own interest first.",
    "People reveal themselves under pressure.",
    "Flattery is a weapon in disguise.",
    "Most generosity comes with a hidden price.",
    "People fear being ordinary more than failure.",
    "Humans justify what they already want.",
    "Nobody remembers your intentions, only outcomes.",
    "Most people need an enemy to feel purpose.",
    "People respect those who need them least.",
    "Belonging matters more to most than truth.",

    # Respect & Status
    "Respect withdrawn is a message.",
    "Status is assigned by how you enter a room.",
    "People treat you how you train them to.",
    "Lowering your standards signals desperation.",
    "Tolerance for disrespect invites more of it.",
    "How you react teaches others your limits.",
    "Dignity is non-negotiable or it is nothing.",
    "Titles impress the weak. Results impress everyone.",
    "Those who beg for loyalty never receive it.",
    "Never chase what should be drawn to you.",

    # Mindset & Discipline
    "Clarity is a competitive advantage.",
    "Most people quit the moment it gets real.",
    "Routine is the foundation all greatness hides behind.",
    "Boredom is where discipline is actually built.",
    "The mind you ignore will eventually run you.",
    "Focus is a form of violence toward distraction.",
    "Self-deception costs more than any enemy could.",
    "Soft habits produce hard consequences.",
    "Every compromise on discipline compounds.",
    "Pain avoided today becomes debt tomorrow.",

    # Emotion & Ego
    "Ego is loudest when identity feels threatened.",
    "Defensiveness broadcasts the wound.",
    "Anger signals where you are still controlled.",
    "Pride is the most expensive luxury most people keep.",
    "People project what they cannot admit.",
    "Blame is the language of the powerless.",
    "Emotional neediness destroys what it clings to.",
    "Insecurity dressed up still shows through.",
    "Unhealed wounds become weapons aimed at others.",
    "The ego wants to win. Wisdom wants to grow.",

    # Trust & Loyalty
    "Loyalty that has a price was never loyalty.",
    "People show you who they are in small moments.",
    "Trust is verified through inconvenience.",
    "Silence during your struggle reveals your circle.",
    "Those who gossip to you gossip about you.",
    "Fair weather allies disappear before the storm ends.",
    "Betrayal rarely comes from strangers.",
    "Oversharing creates ammunition.",
    "People remember how useful you were, not who you were.",
    "Watch what people do when they no longer need you.",

    # Success & Reality
    "Success is deeply uncomfortable before it is rewarding.",
    "Talent without timing is wasted.",
    "Most overnight success is a decade in hiding.",
    "Opportunity looks like work to the unprepared.",
    "The gap between who you are and who you want to be is daily habits.",
    "Winners are just losers who kept iterating.",
    "Comfort zones shrink without you noticing.",
    "Everyone wants the result. Few respect the process.",
    "Luck favors those who removed luck from the equation.",
    "The market does not care about your effort.",

    # Social Dynamics
    "People align with winners before victory is confirmed.",
    "Scarcity is the root of most desire.",
    "Perception is managed or it manages you.",
    "Most conversations are negotiations in disguise.",
    "The one who speaks first in silence often loses.",
    "Charisma is attention made to feel like warmth.",
    "Social hierarchies form whether you acknowledge them or not.",
    "People read confidence faster than they read words.",
    "Your reputation enters rooms you have never been in.",
    "Most rejection is redirection wearing a cruel mask.",
]

# ========= QUOTE OF THE DAY POOL =========

quote_pool = [
    ("The less you react, the more powerful you become.", "Unknown"),
    ("Silence is the best response to a fool.", "Unknown"),
    ("Discipline is choosing what you want most over what you want now.", "Abraham Lincoln"),
    ("The wolf does not concern himself with the opinion of sheep.", "Unknown"),
    ("Do not argue with fools. They drag you to their level.", "Mark Twain"),
    ("Some people aren't loyal to you. They are loyal to their need of you.", "Unknown"),
    ("Work in silence. Let success make the noise.", "Unknown"),
    ("Fear kills more dreams than failure ever will.", "Suzy Kassem"),
    ("When you react, you give away your power.", "Unknown"),
    ("Be careful who you trust. Salt and sugar look the same.", "Unknown"),
    ("Not everyone deserves access to you.", "Unknown"),
    ("You are the average of the five people you spend the most time with.", "Jim Rohn"),
    ("Energy is everything. Protect yours.", "Unknown"),
    ("The quieter you become, the more you can hear.", "Ram Dass"),
    ("Master your mind or your mind will master you.", "Unknown"),
    ("Stop explaining yourself. You don't owe anyone your story.", "Unknown"),
    ("The man who does not read has no advantage over the man who cannot.", "Mark Twain"),
    ("Obsessed is a word the lazy use to describe the dedicated.", "Unknown"),
    ("Closed mouths don't get fed. Open ones don't stay hungry.", "Unknown"),
    ("Your vibe attracts your tribe.", "Unknown"),
]

# ========= CTA POOL =========

cta_pool = [
    "Follow for more dark psychology.",
    "Follow for deeper truths.",
    "Follow for real human behavior.",
    "Follow for unfiltered human nature.",
    "Follow. Most people scroll past wisdom.",
    "Follow for truths they won't teach you.",
    "Follow if you want to see more of this.",
    "Follow for cold truths about human nature.",
]

# ========= BUILD 365 BANK =========

random.seed(42)

all_combos = [(t1, t2) for t1 in title_part1 for t2 in title_part2]
random.shuffle(all_combos)

quote_cycle = quote_pool * (365 // len(quote_pool) + 1)
random.shuffle(quote_cycle)

cta_cycle = cta_pool * (365 // len(cta_pool) + 1)
random.shuffle(cta_cycle)

line_blocks = []
shuffled_lines = line_pool[:]
for i in range(365):
    if len(shuffled_lines) < 7:
        shuffled_lines = line_pool[:]
        random.shuffle(shuffled_lines)
    block = shuffled_lines[:7]
    shuffled_lines = shuffled_lines[7:]
    line_blocks.append(block)

content_bank = []

for i in range(365):
    t1, t2 = all_combos[i % len(all_combos)]
    title = f"7 {t1}\n{t2}"

    lines = line_blocks[i][:]
    lines.append(cta_cycle[i])

    quote, author = quote_cycle[i]

    content_bank.append({
        "title": title,
        "lines": lines,
        "quote": quote,
        "author": author,
    })

# ========= STATE ENGINE =========

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {"index": 0}

def save_state(s):
    with open(STATE_FILE, "w") as f:
        json.dump(s, f)

state = load_state()
idx = state["index"] % len(content_bank)
data = content_bank[idx]
state["index"] += 1
save_state(state)

# ========= HELPERS =========

def draw_watermark(draw, font, width, height):
    wm = "THE HUMAN CODE"
    w = draw.textlength(wm, font=font)
    draw.text(((width - w) / 2, height - 60), wm, font=font, fill=WATERMARK_COLOR)

def measure_content_height(data):
    total = 2 * 70 + 40
    for line in data["lines"]:
        wrapped = smart_wrap(line)
        total += len(wrapped.split("\n")) * 50 + 25
    return total

# ========= FONTS =========

title_font     = ImageFont.truetype(FONT_PATH, TITLE_SIZE)
text_font      = ImageFont.truetype(FONT_PATH, TEXT_SIZE)
cta_font       = ImageFont.truetype(FONT_PATH, CTA_SIZE)
watermark_font = ImageFont.truetype(FONT_PATH, WATERMARK_SIZE)
quote_font     = ImageFont.truetype(FONT_PATH, QUOTE_SIZE)
qlabel_font    = ImageFont.truetype(FONT_PATH, QUOTE_LABEL_SIZE)
cover_font     = ImageFont.truetype(FONT_PATH, COVER_TITLE_SIZE)

# =========================================
# SLIDE 1 â€” COVER (Title + Quote of the Day)
# =========================================

cover = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
cd = ImageDraw.Draw(cover)

quote_lines      = wrap_quote(data["quote"], width=30).split("\n")
title_lines      = data["title"].split("\n")
title_block_h    = len(title_lines) * 90
gap_after_title  = 50
divider_h        = 4 + 50
label_h          = 60
quote_block_h    = len(quote_lines) * 60
author_h         = 35 + 30
total_cover_h    = title_block_h + gap_after_title + divider_h + label_h + quote_block_h + author_h

WATERMARK_ZONE   = 120
usable           = HEIGHT - WATERMARK_ZONE
cy               = max(120, (usable - total_cover_h) // 2)

cd.rectangle([(80, 60), (WIDTH - 80, 66)], fill=ACCENT_COLOR)

brand = "THE HUMAN CODE"
bw = cd.textlength(brand, font=qlabel_font)
cd.text(((WIDTH - bw) / 2, 82), brand, font=qlabel_font, fill=WATERMARK_COLOR)

MARGIN = 80
for line in title_lines:
    font_size = COVER_TITLE_SIZE
    f = cover_font
    while cd.textlength(line, font=f) > (WIDTH - MARGIN * 2) and font_size > 40:
        font_size -= 2
        f = ImageFont.truetype(FONT_PATH, font_size)
    lw = cd.textlength(line, font=f)
    cd.text(((WIDTH - lw) / 2, cy), line, font=f, fill=TITLE_COLOR)
    cy += 90

cy += gap_after_title

cd.rectangle([(160, cy), (WIDTH - 160, cy + 4)], fill=ACCENT_COLOR)
cy += 30

label = "QUOTE OF THE DAY"
lw = cd.textlength(label, font=qlabel_font)
cd.text(((WIDTH - lw) / 2, cy), label, font=qlabel_font, fill=ACCENT_COLOR)
cy += label_h

cd.text((80, cy - 10), "\u201C", font=quote_font, fill=ACCENT_COLOR)

for qline in quote_lines:
    qw = cd.textlength(qline, font=quote_font)
    cd.text(((WIDTH - qw) / 2, cy), qline, font=quote_font, fill=QUOTE_COLOR)
    cy += 60

cd.text((WIDTH - 110, cy - 20), "\u201D", font=quote_font, fill=ACCENT_COLOR)
cy += 20

author_text = "\u2014 @humancode.psychology"
aw = cd.textlength(author_text, font=qlabel_font)
cd.text(((WIDTH - aw) / 2, cy), author_text, font=qlabel_font, fill=TEXT_COLOR)

cd.rectangle([(80, HEIGHT - 100), (WIDTH - 80, HEIGHT - 94)], fill=ACCENT_COLOR)

draw_watermark(cd, watermark_font, WIDTH, HEIGHT)

cover.save(f"{OUTPUT_FOLDER}/slide_1.png")
print("SLIDE 1 (cover) saved.")

# =========================================
# SLIDE 2 â€” LIST POST
# =========================================

img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
draw = ImageDraw.Draw(img)

content_height = measure_content_height(data)
usable_height = HEIGHT - 80
y = max(60, (usable_height - content_height) // 2)

for line in data["title"].split("\n"):
    w = draw.textlength(line, font=title_font)
    draw.text(((WIDTH - w) / 2, y), line, font=title_font, fill=TITLE_COLOR)
    y += 70

y += 40

num = 1
for line in data["lines"]:
    is_cta = (num == 8)
    wrapped = smart_wrap(line)
    font = cta_font if is_cta else text_font
    color = CTA_COLOR if is_cta else TEXT_COLOR

    sub_lines = wrapped.split("\n")
    for i, wl in enumerate(sub_lines):
        if is_cta:
            text = wl
        else:
            text = f"{num}. {wl}" if i == 0 else f"    {wl}"
        w = draw.textlength(text, font=font)
        draw.text(((WIDTH - w) / 2, y), text, font=font, fill=color)
        y += 50

    y += 25
    num += 1

draw_watermark(draw, watermark_font, WIDTH, HEIGHT)

img.save(f"{OUTPUT_FOLDER}/slide_2.png")
print("SLIDE 2 (post) saved.")
print("DONE")

# =========================================
# CAPTION + HASHTAGS
# =========================================

hashtag_pool = [
    "#darkpsychology", "#humanpsychology", "#psychologyfacts", "#mindset",
    "#mentalstrength", "#selfawareness", "#emotionalintelligence", "#personalgrowth",
    "#powermoves", "#respectyourself", "#boundaries", "#discipline",
    "#stoicism", "#socialskills", "#behaviouralhacks", "#mindpower",
    "#psychologytips", "#innerstrength", "#focusedmind", "#levelup",
    "#truthbombs", "#realtalk", "#uncuttruth", "#wakeupcall",
    "#humancode", "#darktruth", "#harshreality", "#brutaltruth",
    "#egocheck", "#socialdynamics", "#powerofsilence", "#controlfreak",
    "#statusmindset", "#influencefacts", "#loyaltyfacts", "#egofacts",
    "#coldtruth", "#psychologyhacks", "#mindbending", "#selfdiscipline",
    "#successmindset", "#confidenceboost", "#alphamindset", "#growthfacts",
    "#motivationdaily", "#truthhurts", "#psychologicalfacts", "#humannaturedaily",
    "#darkhumor", "#powerthinking",
]

hashtag_blocks = []
shuffled_tags = hashtag_pool[:]
random.shuffle(shuffled_tags)
for i in range(365):
    if len(shuffled_tags) < 10:
        shuffled_tags = hashtag_pool[:]
        random.shuffle(shuffled_tags)
    block = shuffled_tags[:10]
    shuffled_tags = shuffled_tags[10:]
    hashtag_blocks.append(block)

caption_title = data["title"].replace("\n", " ")
caption_tags  = " ".join(hashtag_blocks[idx])
caption       = f"{caption_title}\n\n{caption_tags}"

with open(f"{OUTPUT_FOLDER}/caption.txt", "w", encoding="utf-8") as f:
    f.write(caption)

print("CAPTION saved.")
print(caption)
