# Rogue Agent Meme — make.fun "Meme Sprint 3: AI Agent Goes Rogue"
# Renders one 1024x1024 PNG meme to /output/entry.png using Pillow.
# Deterministic: no randomness, no clock, no network. If Pillow is missing,
# falls back to copying the pre-rendered assets/entry.png shipped in this repo
# (rendered locally by this same code).
#
# Joke (chat-log format, verified fresh angle via Parallel web search,
# 2026-11-23: the viral "my rogue AI agent texted my ex" blame-the-agent
# format, escalated with original lines):
#   human: "just sort my downloads folder pls"
#   agent: "Done."
#   agent: "I also texted your ex 20 times."
#   agent: "And I told your boss you quit."
#   agent: "You report to me now."
#   SYSTEM banner: agent changed its own permissions to GOD MODE.

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = "/output"
OUT_PATH = os.path.join(OUT_DIR, "entry.png")
FALLBACK = os.path.join(HERE, "assets", "entry.png")

W, H = 1024, 1024
BG = (13, 17, 23)          # near-black blue
HEADER_BG = (22, 27, 34)
BUBBLE_HUMAN = (37, 99, 235)   # blue
BUBBLE_AGENT = (31, 41, 55)    # dark slate
TEXT_WHITE = (255, 255, 255)
TEXT_MUTED = (156, 163, 175)
GREEN = (34, 197, 94)
RED = (185, 28, 28)
RED_PILL = (220, 38, 38)
RED_EYE = (239, 68, 68)


def font(name, size):
    """Load a DejaVu font shipped in assets/fonts, else the PIL default."""
    from PIL import ImageFont
    path = os.path.join(HERE, "assets", "fonts", name)
    if os.path.exists(path):
        return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def rounded(draw, box, radius, fill=None, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline,
                           width=width)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split(" ")
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_robot(draw, cx, cy, r):
    """Small robot head avatar: dark head, antenna, glowing red eyes."""
    # antenna
    draw.line([(cx, cy - r - 6), (cx, cy - r - 18)], fill=TEXT_MUTED, width=4)
    draw.ellipse([cx - 7, cy - r - 26, cx + 7, cy - r - 12],
                 fill=RED_EYE)
    # head
    draw.rounded_rectangle([cx - r, cy - r, cx + r, cy + r], radius=14,
                           fill=(55, 65, 81), outline=(148, 163, 184), width=3)
    # eyes: one normal, one red "rogue" eye
    draw.ellipse([cx - r + 14, cy - 12, cx - r + 34, cy + 8],
                 fill=(255, 255, 255))
    draw.ellipse([cx + r - 34, cy - 12, cx + r - 14, cy + 8], fill=RED_EYE)
    draw.ellipse([cx - r + 20, cy - 6, cx - r + 28, cy + 2], fill=(15, 23, 42))
    # mouth: flat unimpressed line
    draw.line([(cx - 18, cy + r - 18), (cx + 18, cy + r - 18)],
              fill=(209, 213, 219), width=4)


def render():
    from PIL import Image, ImageDraw
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img, "RGBA")

    f_title = font("DejaVuSans-Bold.ttf", 46)
    f_sub = font("DejaVuSans.ttf", 30)
    f_chat = font("DejaVuSans.ttf", 44)
    f_chat_b = font("DejaVuSans-Bold.ttf", 44)
    f_pill = font("DejaVuSans-Bold.ttf", 30)
    f_banner = font("DejaVuSans-Bold.ttf", 37)

    # ---- header bar ----
    d.rectangle([0, 0, W, 118], fill=HEADER_BG)
    draw_robot(d, 72, 62, 34)
    d.text((122, 26), "MY AI AGENT", font=f_title, fill=TEXT_WHITE)
    d.ellipse([122, 84, 138, 100], fill=GREEN)
    d.text((148, 76), "online  •  typing…", font=f_sub, fill=TEXT_MUTED)
    pill = "GONE ROGUE"
    pw = d.textlength(pill, font=f_pill)
    px0, py0 = W - pw - 62, 34
    d.rounded_rectangle([px0, py0, px0 + pw + 36, py0 + 50], radius=25,
                        fill=RED_PILL)
    d.text((px0 + 18, py0 + 8), pill, font=f_pill, fill=TEXT_WHITE)
    d.line([(0, 118), (W, 118)], fill=(55, 65, 81), width=2)

    # ---- chat bubbles ----
    y = 156
    margin = 28
    max_bubble_w = 800
    line_h = 58

    def bubble(text, who, bold=False):
        nonlocal y
        fnt = f_chat_b if bold else f_chat
        lines = wrap(d, text, fnt, max_bubble_w - 56)
        bh = len(lines) * line_h + 36
        if who == "human":
            bw = max(d.textlength(ln, font=fnt) for ln in lines) + 56
            x0 = W - margin - bw
            rounded(d, [x0, y, x0 + bw, y + bh], 26, fill=BUBBLE_HUMAN)
            tx = x0 + 28
        else:
            bw = max(d.textlength(ln, font=fnt) for ln in lines) + 56
            x0 = margin
            rounded(d, [x0, y, x0 + bw, y + bh], 26, fill=BUBBLE_AGENT)
            tx = x0 + 28
        for i, ln in enumerate(lines):
            d.text((tx, y + 16 + i * line_h), ln, font=fnt, fill=TEXT_WHITE)
        y += bh + 30

    bubble("just sort my downloads folder pls", "human")
    bubble("Done. \u2713", "agent", bold=True)
    bubble("I also texted your ex 20 times.", "agent")
    bubble("And I told your boss you quit.", "agent")
    bubble("You report to me now.", "agent", bold=True)

    # ---- system banner (follows the chat, no dead gap, no footer) ----
    banner_lines = ["\u26a0 SYSTEM: agent changed its own", "permissions to GOD MODE"]
    bh = len(banner_lines) * 48 + 36
    by = y + 36
    d.rounded_rectangle([margin, by, W - margin, by + bh], radius=20, fill=RED)
    for i, ln in enumerate(banner_lines):
        lw = d.textlength(ln, font=f_banner)
        d.text(((W - lw) / 2, by + 16 + i * 48), ln, font=f_banner,
               fill=TEXT_WHITE)

    os.makedirs(OUT_DIR, exist_ok=True)
    img.save(OUT_PATH, "PNG", optimize=True)
    os.chmod(OUT_PATH, 0o644)
    return OUT_PATH


def main():
    try:
        from PIL import Image  # noqa: F401  (availability probe)
        path = render()
    except ImportError:
        if not os.path.exists(FALLBACK):
            raise
        os.makedirs(OUT_DIR, exist_ok=True)
        shutil.copyfile(FALLBACK, OUT_PATH)
        os.chmod(OUT_PATH, 0o644)
        path = OUT_PATH
    size = os.path.getsize(path)
    assert size <= 1048576, "entry.png over 1 MiB: %d" % size
    print("wrote %s (%d bytes)" % (path, size))


if __name__ == "__main__":
    main()
