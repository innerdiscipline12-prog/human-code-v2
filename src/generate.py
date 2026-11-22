from PIL import Image, ImageDraw, ImageFont
import json
import os
import re
import sys
from itertools import combinations

WIDTH, HEIGHT = 1080, 1350
BG_COLOR = (0, 0, 0)
TITLE_COLOR = (255, 190, 0)
TEXT_COLOR = (240, 240, 240)
CTA_COLOR = (255, 190, 0)
WATERMARK_COLOR = (90, 90, 90)
QUOTE_COLOR = (200, 200, 200)
ACCENT_COLOR = (255, 190, 0)

FONT_PATH = "src/Montserrat-Bold.ttf"
TITLE_SIZE, TEXT_SIZE, CTA_SIZE = 64, 36, 38
WATERMARK_SIZE, QUOTE_SIZE, QUOTE_LABEL_SIZE = 24, 44, 26
COVER_TITLE_SIZE = 62
OUTPUT_FOLDER = "output"
STATE_FILE = "state.json"
HISTORY_LIMIT = 96
ORIGINALITY_THRESHOLD = 0.72

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Human Code V3: curated psychological narratives.
# Each arc is intentionally built as:
# HOOK -> CURIOSITY -> TENSION -> ESCALATION -> REFRAME -> CONSEQUENCE -> PAYOFF.
# The black/gold visual system remains unchanged.

ARCS = [
    ("RESPECT", "BOUNDARIES", "COLD FACTS", [
        "People notice what you tolerate before they notice what you demand.",
        "Every exception teaches someone what your boundary really means.",
        "If disrespect has no consequence, it becomes a safe experiment.",
        "Repeated tolerance slowly turns bad behavior into expectation.",
        "Then you start defending standards you never enforced.",
        "The problem is no longer what they did; it is what you trained them to expect.",
        "Respect begins where your actions make your limits believable.",
    ]),
    ("RESPECT", "APPROVAL", "PSYCHOLOGICAL TRUTHS", [
        "The harder you need approval, the easier you are to control.",
        "People can feel when your confidence depends on their reaction.",
        "That need makes you explain decisions that never required permission.",
        "Over-explaining turns a choice into a negotiation.",
        "Eventually, you start editing yourself before anyone asks.",
        "The approval you chased becomes the authority you surrendered.",
        "Real respect starts when acceptance stops being your price.",
    ]),
    ("RESPECT", "INCONSISTENCY", "HIDDEN LAWS", [
        "People trust patterns more than promises.",
        "One strong boundary means little if you abandon it tomorrow.",
        "Inconsistency teaches others to wait until your resistance disappears.",
        "That is why repeated exceptions become more powerful than your rules.",
        "Soon, your words describe standards your behavior cannot prove.",
        "People respond to the pattern, not the speech.",
        "If you want respect, make your actions predictable.",
    ]),

    ("STATUS", "PERCEPTION", "UNSPOKEN RULES", [
        "Status is often decided before the first serious conversation.",
        "People watch how you enter, speak, listen, and react.",
        "Small signals become a fast judgment about confidence and value.",
        "Then that judgment changes how much attention you receive.",
        "The strange part is that perception can become reality through repetition.",
        "People treat the role they believe you occupy.",
        "Your reputation starts working before you arrive.",
    ]),
    ("STATUS", "SCARCITY", "COLD FACTS", [
        "Availability can increase access while quietly reducing perceived value.",
        "When attention is unlimited, people stop feeling its weight.",
        "Constant replies can make your presence feel ordinary.",
        "Ordinary becomes expected, and expected becomes invisible.",
        "That does not mean playing games; it means having a life beyond approval.",
        "People value what feels intentional, not what feels desperate.",
        "Your attention becomes valuable when it has standards.",
    ]),
    ("STATUS", "COMPETENCE", "BRUTAL TRUTHS", [
        "Confidence without competence eventually gets exposed.",
        "People may believe a strong image for a while.",
        "Pressure is where borrowed confidence starts losing its cover.",
        "Results become harder to fake when consequences arrive.",
        "That is why quiet competence often outlasts loud charisma.",
        "The person who can actually deliver needs less convincing.",
        "Real status is easier to maintain than to pretend.",
    ]),

    ("POWER", "REACTION", "SILENT RULES", [
        "The fastest way to lose leverage is to reveal what controls you.",
        "Anger can expose the exact button someone needs to press.",
        "Once the button is known, your reactions become predictable.",
        "Predictability makes manipulation cheaper.",
        "The strongest response is often the one you choose after the emotion passes.",
        "Control does not mean feeling nothing; it means delaying the decision.",
        "Whoever controls your reaction can influence your direction.",
    ]),
    ("POWER", "INFORMATION", "HIDDEN LAWS", [
        "Not every thought becomes more valuable when you reveal it.",
        "People use information differently once they know what matters to you.",
        "Oversharing can turn private fears into public leverage.",
        "The more predictable your motives become, the easier you are to steer.",
        "Privacy creates room to think without performing.",
        "Silence is not weakness when it protects your position.",
        "Power often grows where unnecessary information stops.",
    ]),
    ("POWER", "DEPENDENCE", "HARSH REALITIES", [
        "The person who cannot walk away often has less leverage.",
        "Dependence changes what you are willing to tolerate.",
        "Then tolerance changes your behavior before anyone says a word.",
        "Others notice when your need is stronger than your standards.",
        "That imbalance quietly shifts the relationship.",
        "Leverage returns when you build options instead of begging for one.",
        "The strongest position is having a choice.",
    ]),

    ("EGO", "DEFENSIVENESS", "PSYCHOLOGICAL TRUTHS", [
        "Defensiveness often reveals what the argument touched.",
        "A harmless question should not feel like an attack.",
        "But an exposed insecurity can turn curiosity into conflict.",
        "Then protecting the image becomes more important than learning.",
        "That is how ego turns correction into disrespect.",
        "The person who must always be right eventually stops improving.",
        "Growth begins when protecting your image matters less than finding the truth.",
    ]),
    ("EGO", "IDENTITY", "DARK TRUTHS", [
        "People defend identities long after the evidence changes.",
        "Once an opinion becomes part of who you are, changing it feels like losing.",
        "That emotional cost can make obvious facts uncomfortable.",
        "So the mind searches for reasons to protect the old story.",
        "The longer you defend it, the harder it becomes to question.",
        "Pride can keep a person loyal to a version of themselves that no longer works.",
        "Wisdom begins when identity can survive correction.",
    ]),
    ("EGO", "WINNING", "UNCOMFORTABLE TRUTHS", [
        "Some people would rather win an argument than improve their life.",
        "Winning gives the ego an immediate reward.",
        "Learning usually requires admitting something was missing.",
        "That admission feels like weakness to a fragile identity.",
        "So the argument gets defended while the problem stays untouched.",
        "A victory that changes nothing is still a loss.",
        "The strongest mind can leave an argument with something learned.",
    ]),

    ("PEOPLE", "MOTIVES", "COLD FACTS", [
        "People can give you a reason without giving you the real motive.",
        "The stated reason is often the socially acceptable version.",
        "The real motive usually appears in what benefits them.",
        "Watch what changes when the reward disappears.",
        "That is where intention becomes behavior.",
        "Behavior repeated under different conditions is harder to fake.",
        "If you want to understand people, study incentives and patterns.",
    ]),
    ("PEOPLE", "PRESSURE", "HIDDEN LAWS", [
        "Pressure does not create every behavior; it removes the mask from some of them.",
        "Comfort lets people manage appearances.",
        "Stress makes priorities harder to hide.",
        "Fear reveals what someone protects first.",
        "Power reveals what someone thinks they can get away with.",
        "Pressure is therefore information, not just a problem.",
        "Watch behavior when the cost of honesty rises.",
    ]),
    ("PEOPLE", "PROJECTION", "PSYCHOLOGICAL TRUTHS", [
        "People often criticize in others what they struggle to face in themselves.",
        "The accusation can reveal an uncomfortable internal conflict.",
        "That does not make every criticism projection.",
        "But repeated obsession with the same flaw is worth examining.",
        "Especially when the critic shows the same pattern privately.",
        "The mirror is sometimes disguised as judgment.",
        "Pay attention to what people cannot stop talking about.",
    ]),

    ("LOYALTY", "CONVENIENCE", "BRUTAL TRUTHS", [
        "Not everyone who stays is loyal; some people simply have no reason to leave.",
        "Convenience can look like commitment while everything is easy.",
        "The difference appears when loyalty becomes expensive.",
        "Distance, disagreement, or inconvenience tests what the relationship can survive.",
        "That is why difficult seasons reveal more than comfortable years.",
        "Real loyalty costs something and still chooses to remain.",
        "Watch who stays when staying stops being useful.",
    ]),
    ("LOYALTY", "GOSSIP", "SILENT RULES", [
        "The person who constantly brings you other people's secrets is giving you a warning.",
        "They are showing you how they handle private information.",
        "What feels like intimacy today can become ammunition tomorrow.",
        "Trust weakens when every conversation becomes a story about someone absent.",
        "You do not need to expose others to feel close.",
        "Privacy is often a stronger test of character than friendliness.",
        "Watch what people protect when nobody is watching.",
    ]),
    ("LOYALTY", "NEED", "HARSH REALITIES", [
        "Need can imitate loyalty until the need disappears.",
        "Some relationships feel strong because both sides benefit.",
        "Remove the benefit and the emotional truth becomes clearer.",
        "Sudden distance can reveal what the relationship was actually built on.",
        "That realization hurts because history can make convenience look like love.",
        "Loyalty survives when the transaction ends.",
        "Pay attention to who still values you without needing something.",
    ]),

    ("CONFIDENCE", "PERFORMANCE", "COLD FACTS", [
        "Confidence becomes weaker when it needs to be constantly displayed.",
        "People who trust themselves rarely need every room to notice.",
        "Performance seeks witnesses; competence seeks results.",
        "That difference becomes obvious when attention disappears.",
        "Without an audience, insecure confidence often loses its energy.",
        "Real confidence survives being unseen.",
        "You know you are becoming stronger when you stop needing to prove it.",
    ]),
    ("CONFIDENCE", "REJECTION", "PSYCHOLOGICAL TRUTHS", [
        "Rejection hurts more when you treat it as a verdict on your identity.",
        "One person's decision can become a story you repeat about yourself.",
        "Then you start avoiding opportunities that might produce the same pain.",
        "Avoidance feels safe while quietly shrinking your world.",
        "The rejection was one event; the meaning you attached to it became a pattern.",
        "Confidence returns when outcomes stop defining your worth.",
        "A closed door is information, not a complete identity.",
    ]),
    ("CONFIDENCE", "SILENCE", "UNSPOKEN TRUTHS", [
        "You learn a lot about confidence by watching who needs the last word.",
        "Some people speak to communicate; others speak to control the room.",
        "The difference becomes obvious when nobody agrees with them.",
        "A fragile ego treats silence as surrender.",
        "A secure mind can let a moment remain unresolved.",
        "Not every disagreement needs your performance.",
        "Sometimes confidence is simply being comfortable without the final word.",
    ]),

    ("BOUNDARIES", "GUILT", "HARSH REALITIES", [
        "Guilt can make a healthy boundary feel like cruelty.",
        "If people benefited from your lack of limits, they may resist the change.",
        "Their discomfort can make you question your decision.",
        "Then you soften the boundary just to restore peace.",
        "Peace bought with self-betrayal is not peace.",
        "A boundary is not an attack because someone dislikes it.",
        "You are allowed to disappoint people without abandoning yourself.",
    ]),
    ("BOUNDARIES", "ACCESS", "HIDDEN LAWS", [
        "Access to you should match the level of trust someone has earned.",
        "Giving everyone the same access removes the meaning of trust.",
        "Some people learn your weaknesses simply because you never protected them.",
        "Then private information becomes public leverage.",
        "Healthy distance is not hatred; it is information management.",
        "Closeness should be earned through consistency.",
        "Not everyone deserves the same version of you.",
    ]),
    ("BOUNDARIES", "CONSEQUENCES", "UNCOMFORTABLE TRUTHS", [
        "A boundary without a consequence is often just a request.",
        "People learn the real rule from what happens after they cross it.",
        "If nothing changes, the crossing becomes cheaper each time.",
        "Eventually the boundary exists only in your words.",
        "That is when frustration replaces authority.",
        "Consequences do not need anger; they need consistency.",
        "The clearest boundary is the one your behavior enforces.",
    ]),
]

TITLE_FALLBACKS = [
    "COLD FACTS", "HIDDEN LAWS", "PSYCHOLOGICAL TRUTHS", "UNSPOKEN RULES",
    "BRUTAL TRUTHS", "SILENT RULES", "HARSH REALITIES", "UNCOMFORTABLE TRUTHS",
]

QUOTE_POOL = [
    ("When you react, you give away your power.", "Unknown"),
    ("The less you react, the more powerful you become.", "Unknown"),
    ("Not everyone deserves access to you.", "Unknown"),
    ("Silence is often the clearest answer.", "Unknown"),
    ("The strongest position is having a choice.", "Unknown"),
    ("What you tolerate teaches people how to treat you.", "Unknown"),
    ("People reveal themselves through patterns, not promises.", "Unknown"),
    ("Self-awareness begins where excuses end.", "Unknown"),
]

CTA_POOL = [
    "Follow for deeper human psychology.",
    "Follow for real human behavior.",
    "Follow for truths people learn late.",
    "Follow The Human Code.",
]

HASHTAGS = [
    "#humancode", "#humanpsychology", "#psychologyfacts", "#psychology",
    "#humannature", "#socialdynamics", "#selfawareness", "#mindset",
    "#behavior", "#psychologicaltruths", "#personalgrowth", "#darkpsychology",
]

def normalize(text):
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]+", " ", text.lower())).strip()

def tokens(text):
    return set(normalize(text).split())

def similarity(a, b):
    ta, tb = tokens(a), tokens(b)
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)

def narrative_signature(arc):
    return normalize(arc["title"] + " " + " ".join(arc["lines"]))

def impact_score(arc):
    lines = arc["lines"]
    first = normalize(lines[0])
    middle = normalize(" ".join(lines[1:6]))
    final = normalize(lines[-1])
    # Base structural credit: every curated arc already has seven distinct,
    # deliberately ordered points. Content keywords then refine the score.
    score = 1.0

    curiosity = ["before", "why", "what", "people notice", "the difference", "the person", "not everyone", "the fastest", "the harder"]
    tension = ["control", "exposed", "consequence", "cost", "pressure", "desperate", "insecurity", "risk", "trust", "need", "fear", "disrespect"]
    payoff = ["respect", "control", "choice", "pattern", "standard", "truth", "growth", "identity", "behavior", "boundaries", "confidence"]

    score += sum(1.0 for x in curiosity if x in first)
    score += min(2.0, sum(0.35 for x in tension if x in middle))
    score += min(2.0, sum(0.45 for x in payoff if x in final))
    if 7 <= len(first.split()) <= 15:
        score += 1.0
    if 7 <= len(final.split()) <= 15:
        score += 1.0
    if len(set(normalize(x) for x in lines)) == 7:
        score += 1.0

    # Penalize generic motivational endings and flat repetition.
    if final in {"keep going", "stay strong", "never quit", "believe in yourself"}:
        score -= 3.0
    if similarity(lines[0], " ".join(lines[1:])) > 0.45:
        score -= 1.5
    return round(score, 3)

def build_candidates(index):
    candidates = []
    for i, (topic, angle, frame, lines) in enumerate(ARCS):
        title_frame = frame if i % 3 else TITLE_FALLBACKS[index % len(TITLE_FALLBACKS)]
        title = f"7 {title_frame}\nABOUT {topic}"
        candidates.append({
            "topic": topic,
            "angle": angle,
            "frame": frame,
            "title": title,
            "lines": list(lines),
            "impact_score": impact_score({"title": title, "lines": lines}),
            "arc_id": f"{topic.lower()}-{angle.lower()}",
        })
    return candidates

def choose_candidate(index, history):
    candidates = build_candidates(index)
    recent = history[-HISTORY_LIMIT:]
    recent_text = [h.get("signature", "") for h in recent]
    recent_topics = [h.get("topic") for h in recent[-6:]]

    scored = []
    for c in candidates:
        sig = narrative_signature(c)
        max_sim = max((similarity(sig, old) for old in recent_text), default=0.0)
        if max_sim >= ORIGINALITY_THRESHOLD:
            continue
        score = c["impact_score"]
        if c["topic"] in recent_topics:
            score -= 0.75
        score += ((index + len(c["arc_id"])) % 7) * 0.01
        scored.append((score, c))

    if not scored:
        # Fail safe: choose the least similar candidate rather than stopping production.
        scored = []
        for c in candidates:
            sig = narrative_signature(c)
            max_sim = max((similarity(sig, old) for old in recent_text), default=0.0)
            scored.append((c["impact_score"] - max_sim * 2.0, c))

    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[0][1]

def load_state():
    if not os.path.exists(STATE_FILE):
        return {"index": 0, "history": []}
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            state = json.load(f)
    except Exception:
        return {"index": 0, "history": []}
    if not isinstance(state, dict):
        return {"index": int(state) if isinstance(state, int) else 0, "history": []}
    state.setdefault("index", 0)
    state.setdefault("history", [])
    return state

def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)

def smart_wrap(line):
    if len(line) <= 55:
        return line
    if len(line) <= 95:
        import textwrap
        return textwrap.fill(line, width=42)
    import textwrap
    return textwrap.fill(line, width=36)

def wrap_quote(line, width=30):
    import textwrap
    return textwrap.fill(line, width=width)

def draw_watermark(draw, font):
    wm = "THE HUMAN CODE"
    w = draw.textlength(wm, font=font)
    draw.text(((WIDTH - w) / 2, HEIGHT - 60), wm, font=font, fill=WATERMARK_COLOR)

def render(arc, quote, author, tags):
    title_font = ImageFont.truetype(FONT_PATH, TITLE_SIZE)
    text_font = ImageFont.truetype(FONT_PATH, TEXT_SIZE)
    cta_font = ImageFont.truetype(FONT_PATH, CTA_SIZE)
    watermark_font = ImageFont.truetype(FONT_PATH, WATERMARK_SIZE)
    quote_font = ImageFont.truetype(FONT_PATH, QUOTE_SIZE)
    qlabel_font = ImageFont.truetype(FONT_PATH, QUOTE_LABEL_SIZE)
    cover_font = ImageFont.truetype(FONT_PATH, COVER_TITLE_SIZE)

    # Slide 1: preserve the existing black/gold cover identity.
    cover = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    cd = ImageDraw.Draw(cover)
    quote_lines = wrap_quote(quote, 30).split("\n")
    title_lines = arc["title"].split("\n")
    total = len(title_lines) * 90 + 50 + 4 + 50 + 60 + len(quote_lines) * 60 + 65
    cy = max(120, (HEIGHT - 120 - total) // 2)
    cd.rectangle([(80, 60), (WIDTH - 80, 66)], fill=ACCENT_COLOR)
    brand = "THE HUMAN CODE"
    bw = cd.textlength(brand, font=qlabel_font)
    cd.text(((WIDTH - bw) / 2, 82), brand, font=qlabel_font, fill=WATERMARK_COLOR)

    for line in title_lines:
        f = cover_font
        size = COVER_TITLE_SIZE
        while cd.textlength(line, font=f) > WIDTH - 160 and size > 40:
            size -= 2
            f = ImageFont.truetype(FONT_PATH, size)
        lw = cd.textlength(line, font=f)
        cd.text(((WIDTH - lw) / 2, cy), line, font=f, fill=TITLE_COLOR)
        cy += 90

    cy += 50
    cd.rectangle([(160, cy), (WIDTH - 160, cy + 4)], fill=ACCENT_COLOR)
    cy += 30
    label = "QUOTE OF THE DAY"
    lw = cd.textlength(label, font=qlabel_font)
    cd.text(((WIDTH - lw) / 2, cy), label, font=qlabel_font, fill=ACCENT_COLOR)
    cy += 60
    cd.text((80, cy - 10), "“", font=quote_font, fill=ACCENT_COLOR)
    for qline in quote_lines:
        qw = cd.textlength(qline, font=quote_font)
        cd.text(((WIDTH - qw) / 2, cy), qline, font=quote_font, fill=QUOTE_COLOR)
        cy += 60
    author_text = f"— {author}"
    aw = cd.textlength(author_text, font=qlabel_font)
    cd.text(((WIDTH - aw) / 2, cy + 10), author_text, font=qlabel_font, fill=TEXT_COLOR)
    cd.rectangle([(80, HEIGHT - 100), (WIDTH - 80, HEIGHT - 94)], fill=ACCENT_COLOR)
    draw_watermark(cd, watermark_font)
    cover.save(f"{OUTPUT_FOLDER}/slide_1.png")

    # Slide 2: seven escalating points + CTA.
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    title_h = len(title_lines) * 70 + 40
    line_heights = sum(max(1, len(smart_wrap(x).split("\n"))) * 50 + 25 for x in arc["lines"])
    total_h = title_h + line_heights + 80
    y = max(60, (HEIGHT - total_h) // 2)

    for line in title_lines:
        w = draw.textlength(line, font=title_font)
        draw.text(((WIDTH - w) / 2, y), line, font=title_font, fill=TITLE_COLOR)
        y += 70
    y += 40

    for n, line in enumerate(arc["lines"], 1):
        wrapped = smart_wrap(line)
        for j, wl in enumerate(wrapped.split("\n")):
            text = f"{n}. {wl}" if j == 0 else f"    {wl}"
            w = draw.textlength(text, font=text_font)
            draw.text(((WIDTH - w) / 2, y), text, font=text_font, fill=TEXT_COLOR)
            y += 50
        y += 25

    cta = CTA_POOL[(sum(ord(c) for c in arc["topic"] + arc["angle"]) % len(CTA_POOL))]
    cw = draw.textlength(cta, font=cta_font)
    draw.text(((WIDTH - cw) / 2, y), cta, font=cta_font, fill=CTA_COLOR)
    draw_watermark(draw, watermark_font)
    img.save(f"{OUTPUT_FOLDER}/slide_2.png")

    caption = arc["title"].replace("\n", " ") + "\n\n" + " ".join(tags)
    with open(f"{OUTPUT_FOLDER}/caption.txt", "w", encoding="utf-8") as f:
        f.write(caption)

    with open(f"{OUTPUT_FOLDER}/manifest.json", "w", encoding="utf-8") as f:
        json.dump({
            "engine": "Human Code V3",
            "topic": arc["topic"],
            "angle": arc["angle"],
            "frame": arc["frame"],
            "impact_score": arc["impact_score"],
            "title": arc["title"],
            "lines": arc["lines"],
        }, f, indent=2)

def stress_test(count=20):
    history = []
    seen = []
    failures = []
    for i in range(count):
        arc = choose_candidate(i, history)
        sig = narrative_signature(arc)
        if any(similarity(sig, old) >= ORIGINALITY_THRESHOLD for old in seen):
            failures.append({"run": i + 1, "reason": "semantic duplicate"})
        if len(arc["lines"]) != 7:
            failures.append({"run": i + 1, "reason": "not seven points"})
        if len(set(arc["lines"])) != 7:
            failures.append({"run": i + 1, "reason": "duplicate points"})
        if arc["impact_score"] < 4.0:
            failures.append({"run": i + 1, "reason": f"low impact score {arc['impact_score']}"})
        history.append({
            "topic": arc["topic"],
            "angle": arc["angle"],
            "signature": sig,
        })
        seen.append(sig)

    report = {
        "engine": "Human Code V3",
        "requested": count,
        "passed": not failures,
        "failures": failures,
        "unique_runs": len(seen) == len(set(seen)),
    }
    os.makedirs(f"{OUTPUT_FOLDER}/stress_test", exist_ok=True)
    with open(f"{OUTPUT_FOLDER}/stress_test/report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    for i, item in enumerate(history, 1):
        with open(f"{OUTPUT_FOLDER}/stress_test/run_{i:02d}.json", "w", encoding="utf-8") as f:
            json.dump(item, f, indent=2)
    print(json.dumps(report, indent=2))
    if failures:
        raise SystemExit(1)

def main():
    if "--stress-test" in sys.argv:
        pos = sys.argv.index("--stress-test")
        count = int(sys.argv[pos + 1]) if pos + 1 < len(sys.argv) else 20
        stress_test(count)
        return

    state = load_state()
    idx = int(state.get("index", 0))
    arc = choose_candidate(idx, state.get("history", []))

    quote, author = QUOTE_POOL[idx % len(QUOTE_POOL)]
    tags = HASHTAGS[idx % len(HASHTAGS):] + HASHTAGS[:idx % len(HASHTAGS)]
    tags = tags[:10]

    render(arc, quote, author, tags)

    state["index"] = idx + 1
    state["history"] = (state.get("history", []) + [{
        "index": idx,
        "topic": arc["topic"],
        "angle": arc["angle"],
        "frame": arc["frame"],
        "title": arc["title"],
        "signature": narrative_signature(arc),
        "impact_score": arc["impact_score"],
    }])[-HISTORY_LIMIT:]
    save_state(state)

    print(f"Human Code V3 generated: {arc['title'].replace(chr(10), ' ')}")
    print(f"Topic: {arc['topic']} | Angle: {arc['angle']} | Impact: {arc['impact_score']}")

if __name__ == "__main__":
    main()
