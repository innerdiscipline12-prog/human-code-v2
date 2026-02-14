import os
import random
import textwrap
from typing import List, Tuple

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageClip

# ================== SETTINGS ==================
OUT = "output"
os.makedirs(OUT, exist_ok=True)

# Output counts
BATCH = 5

# Image sizes
SQUARE = (1080, 1080)      # IG post
REEL = (1080, 1920)        # IG/FB reel
REEL_DUR = 6               # seconds
REEL_FPS = 24

# Theme
BG = (10, 10, 10)
TITLE = (255, 180, 0)      # premium gold
TEXT = (235, 235, 235)
WM = (130, 130, 130)

FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# ================== CONTENT ==================
CTAS = [
    "If you scroll past now, this may never find you again.",
    "Most will scroll. Few will understand.",
    "If this reached you, it was meant for you.",
    "You noticed this for a reason.",
    "Only a few pay attention to this."
]

HOOKS = [
    "Few notice this.",
    "Quiet truth.",
    "Human pattern.",
    "Observe closely.",
    "This changes perception."
]

HASHTAGS = [
    "#psychology", "#humanbehavior", "#selfawareness", "#mindset", "#discipline",
    "#personalgrowth", "#emotionalintelligence", "#habits", "#mentalstrength",
    "#awareness", "#socialdynamics", "#selfcontrol", "#behavioralpsychology"
]

# (title1, title2, bullet_lines)
POSTS: List[Tuple[str, str, List[str]]] = [
    ("7 SIGNS YOU MIGHT BE", "TOO AVAILABLE", [
        "You reply instantly to everyone.",
        "You cancel plans for others.",
        "You say yes when you want no.",
        "You over-explain yourself.",
        "You chase closure.",
        "You accept last-minute invites.",
        "You fear disappointing people."
    ]),
    ("THE WALK AWAY RULE", "", [
        "If respect is missing, leave.",
        "If effort is one-sided, leave.",
        "If trust feels forced, leave.",
        "If peace disappears, leave.",
        "If honesty is rare, leave.",
        "If boundaries are ignored, leave.",
        "If you feel smaller, leave."
    ]),
    ("REAL POWER", "", [
        "Silence shows confidence.",
        "Boundaries show self-worth.",
        "Habits show priorities.",
        "Discipline shows identity.",
        "Patience shows control.",
        "Consistency shows strength.",
        "Calm shows authority."
    ]),
    ("THE PEOPLE TEST", "", [
        "Watch who listens when you speak softly.",
        "Watch who stays when you stop entertaining.",
        "Watch who respects no without punishment.",
        "Watch who keeps promises unobserved.",
        "Watch who benefits from your confusion.",
        "Watch who disappears when you improve.",
        "Patterns never lie."
    ]),
    ("EMOTIONAL CONTROL", "", [
        "Pause before reacting.",
        "Name the feeling without obeying it.",
        "Choose the standard, not the impulse.",
        "Silence is a decision.",
        "Delay is power.",
        "Clarity comes after the wave.",
        "Composure builds authority."
    ]),
]

# ================== HELPERS ==================
def load_font(size: int) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except Exception:
        return ImageFont.load_default()

def center_text(draw: ImageDraw.ImageDraw, text: str, font, y: int, color, w: int):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    x = int((w - tw) / 2)
    draw.text((x, y), text, font=font, fill=color)

def multiline_center(draw: ImageDraw.ImageDraw, text: str, font, y: int, color, w: int, wrap: int, spacing: int):
    lines = textwrap.wrap(text, width=wrap)
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        th = bbox[3] - bbox[1]
        center_text(draw, line, font, y, color, w)
        y += th + spacing
    return y

def render_slide(size: Tuple[int, int], title1: str, title2: str, bullets: List[str], cta: str, watermark: str) -> Image.Image:
    w, h = size
    img = Image.new("RGB", (w, h), BG)
    draw = ImageDraw.Draw(img)

    title_font = load_font(64)
    body_font = load_font(38)
    cta_font = load_font(36)
    wm_font = load_font(28)

    y = 70

    # Titles
    center_text(draw, title1, title_font, y, TITLE, w)
    y += 90
    if title2:
        center_text(draw, title2, title_font, y, TITLE, w)
        y += 90
    y += 25

    # Bullets
    for i, line in enumerate(bullets, 1):
        y = multiline_center(draw, f"{i}. {line}", body_font, y, TEXT, w, wrap=34, spacing=8)
        y += 8

    # CTA (always last)
    y += 18
    y = multiline_center(draw, cta, cta_font, y, TEXT, w, wrap=34, spacing=8)

    # Watermark bottom
    center_text(draw, watermark, wm_font, h - 60, WM, w)

    return img

def write_caption_file(idx: int, title1: str, title2: str, bullets: List[str], cta: str):
    # Titles
    ig_title = f"{title1} {title2}".strip()[:70]
    fb_title = f"Psychology: {title1}".strip()[:70]

    # Caption A/B
    hook = random.choice(HOOKS)
    tags = " ".join(random.sample(HASHTAGS, 10))

    bullets_text = "\n".join([f"- {b}" for b in bullets[:5]])

    caption_a = f"""{hook}

{bullets_text}

{cta}

Follow for daily human psychology.
{tags}"""

    caption_b = f"""{cta}

{bullets_text}

{hook}

Follow for daily human psychology.
{tags}"""

    path = os.path.join(OUT, f"post_{idx}_caption.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"INSTAGRAM TITLE:\n{ig_title}\n\n")
        f.write(f"FACEBOOK TITLE:\n{fb_title}\n\n")
        f.write("CAPTION VERSION A:\n" + caption_a + "\n\n")
        f.write("CAPTION VERSION B:\n" + caption_b + "\n")

def make_reel_from_image(img_path: str, out_path: str):
    clip = ImageClip(img_path).set_duration(REEL_DUR)
    clip = clip.resize(newsize=REEL)
    clip.write_videofile(out_path, fps=REEL_FPS, codec="libx264", audio=False, verbose=False, logger=None)

# ================== MAIN ==================
def main():
    for i in range(1, BATCH + 1):
        title1, title2, bullets = random.choice(POSTS)
        cta = random.choice(CTAS)

        # 1) Square post image
        square = render_slide(SQUARE, title1, title2, bullets, cta, "THE HUMAN CODE")
        square_path = os.path.join(OUT, f"post_{i}.png")
        square.save(square_path)

        # 2) Reel image (vertical) + reel video
        vertical = render_slide(REEL, title1, title2, bullets, cta, "THE HUMAN CODE")
        vertical_path = os.path.join(OUT, f"reel_{i}_frame.png")
        vertical.save(vertical_path)

        reel_path = os.path.join(OUT, f"reel_{i}.mp4")
        make_reel_from_image(vertical_path, reel_path)

        # 3) Captions/titles/hashtags A/B
        write_caption_file(i, title1, title2, bullets, cta)

    # Combined index file
    with open(os.path.join(OUT, "README_OUTPUT.txt"), "w", encoding="utf-8") as f:
        f.write("Generated:\n")
        f.write("- 5 square posts: post_1.png ... post_5.png\n")
        f.write("- 5 reel frames: reel_1_frame.png ... reel_5_frame.png\n")
        f.write("- 5 reels: reel_1.mp4 ... reel_5.mp4\n")
        f.write("- 5 caption files: post_1_caption.txt ... post_5_caption.txt\n")

    print("DONE ✅ V4 content generated in /output")

if __name__ == "__main__":
    main()
