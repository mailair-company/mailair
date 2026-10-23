"""
Regenerates the platform banners and share images in frontend/public/social
around the current positioning: "Email Marketing & Team Hub for Small
Businesses".

Each layout keeps its content inside that platform's safe-visible area
(profile-photo overlap, mobile side-crops, YouTube's TV/desktop/mobile
crop), not just the raw canvas size.

Run from the repo root:
    backend/venv/bin/python scripts/generate_brand_banners.py
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_PATH = os.path.join(ROOT, "backend", "assets", "fonts", "Fraunces.ttf")
ICON_PATH = os.path.join(ROOT, "backend", "assets", "images", "icon-transparent.png")
OUT_DIR = os.path.join(ROOT, "frontend", "public", "social")

TAGLINE = "Email Marketing & Team Hub for Small Businesses"
EYEBROW = "EMAIL MARKETING + TEAM HUB"
SUBLINE = "Campaigns · Shared inbox · Docs, chat & calls"
URL = "mailair.company"

CREAM = (250, 243, 236, 255)
INK = (34, 28, 22, 255)
MUTED = (99, 86, 70, 255)
LINE = (238, 232, 222, 255)
BORDER = (231, 224, 212, 255)
TERRACOTTA = (176, 71, 35, 255)
OLIVE = (92, 122, 74, 255)
AMBER = (179, 129, 44, 255)
SAGE = (117, 130, 79, 255)

WEIGHTS = {"Light": 300, "Regular": 400, "SemiBold": 600, "Bold": 700}


def font(size: int, weight: str = "SemiBold") -> ImageFont.FreeTypeFont:
    f = ImageFont.truetype(FONT_PATH, size)
    # Axes: optical size, weight, softness, wonky
    f.set_variation_by_axes([min(max(size, 9), 144), WEIGHTS[weight], 0, 0])
    return f


def wrap(draw, text, f, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if draw.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def canvas(w, h, glow_xy, glow_r):
    img = Image.new("RGBA", (w, h), CREAM)
    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    gx, gy = glow_xy
    ImageDraw.Draw(glow).ellipse((gx - glow_r, gy - glow_r, gx + glow_r, gy + glow_r), fill=(245, 197, 172, 120))
    img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(glow_r * 0.45)))
    return img


def wordmark(draw, x, y, size):
    f = font(size, "SemiBold")
    draw.text((x, y), "Mail", font=f, fill=INK)
    draw.text((x + draw.textlength("Mail", font=f), y), "air", font=f, fill=TERRACOTTA)


def text_block(img, x, y, max_w, scale, *, show_icon=True, show_sub=True, show_url=True, center=False):
    """Eyebrow, tagline headline, subline, URL. Returns the bottom y."""
    draw = ImageDraw.Draw(img)

    def place(line_w):
        return x + (max_w - line_w) / 2 if center else x

    if show_icon:
        icon_size = int(64 * scale)
        icon = Image.open(ICON_PATH).convert("RGBA").resize((icon_size, icon_size), Image.LANCZOS)
        wm_size = int(40 * scale)
        wm_w = draw.textlength("Mailair", font=font(wm_size))
        gap = int(14 * scale)
        row_w = icon_size + gap + wm_w
        rx = place(row_w)
        img.alpha_composite(icon, (int(rx), int(y)))
        wordmark(draw, rx + icon_size + gap, y + (icon_size - wm_size * 1.25) / 2, wm_size)
        y += icon_size + int(26 * scale)

    eb = font(int(17 * scale), "Bold")
    draw.text((place(draw.textlength(EYEBROW, font=eb)), y), EYEBROW, font=eb, fill=TERRACOTTA)
    y += int(36 * scale)

    hf = font(int(54 * scale), "SemiBold")
    lh = int(62 * scale)
    for line in wrap(draw, TAGLINE, hf, max_w):
        draw.text((place(draw.textlength(line, font=hf)), y), line, font=hf, fill=INK)
        y += lh

    if show_sub:
        y += int(14 * scale)
        sf = font(int(24 * scale), "Regular")
        draw.text((place(draw.textlength(SUBLINE, font=sf)), y), SUBLINE, font=sf, fill=MUTED)
        y += int(34 * scale)

    if show_url:
        y += int(10 * scale)
        uf = font(int(20 * scale), "SemiBold")
        draw.text((place(draw.textlength(URL, font=uf)), y), URL, font=uf, fill=TERRACOTTA)
        y += int(28 * scale)
    return y


HUB_ROWS = [
    ("Spring offer campaign", "Sent to 4,312 · 61% opened", "Campaign", OLIVE),
    ("Sarah Michaels", "Contract needs your signature", "Urgent", TERRACOTTA),
    ("Team chat", "Priya: proposal is up in Docs", "Team", SAGE),
    ("Call with Tech Corp", "Today, 3:00 PM · video", "Call", AMBER),
]


def hub_card(img, left, top, width, scale, rows=4):
    """A stylized 'Today in your hub' card — illustration, no real user data."""
    draw = ImageDraw.Draw(img)
    header_h = int(64 * scale)
    row_h = int(78 * scale)
    height = header_h + row_h * rows + int(8 * scale)
    radius = int(22 * scale)

    shadow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle(
        (left, top + 14 * scale, left + width, top + height + 14 * scale), radius=radius, fill=(94, 42, 26, 45))
    img.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(20 * scale)))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((left, top, left + width, top + height), radius=radius, fill=(255, 255, 255, 255), outline=BORDER, width=max(1, int(2 * scale)))

    pad = int(28 * scale)
    draw.text((left + pad, top + 20 * scale), "Today in your hub", font=font(int(24 * scale), "SemiBold"), fill=INK)
    cf = font(int(17 * scale), "Regular")
    count = f"{rows} updates"
    draw.text((left + width - pad - draw.textlength(count, font=cf), top + 25 * scale), count, font=cf, fill=MUTED)

    nf, sf, tf = font(int(21 * scale), "SemiBold"), font(int(18 * scale), "Light"), font(int(15 * scale), "SemiBold")
    y = top + header_h
    for title, detail, tag, color in HUB_ROWS[:rows]:
        draw.line((left + pad, y, left + width - pad, y), fill=LINE, width=max(1, int(2 * scale)))
        draw.text((left + pad, y + 14 * scale), title, font=nf, fill=INK)
        draw.text((left + pad, y + 44 * scale), detail, font=sf, fill=MUTED)
        tw = draw.textlength(tag, font=tf) + 26 * scale
        tx = left + width - pad - tw
        draw.rounded_rectangle((tx, y + 14 * scale, tx + tw, y + 42 * scale), radius=14 * scale, outline=color, width=max(1, int(2 * scale)))
        draw.text((tx + 13 * scale, y + 18 * scale), tag, font=tf, fill=color)
        y += row_h
    return top + height


def save(img, name):
    path = os.path.join(OUT_DIR, name)
    img.convert("RGB").save(path, optimize=True)
    print("wrote", os.path.relpath(path, ROOT))


def linkedin():
    # 1584x396. Profile photo covers roughly x<460 on the lower half (desktop)
    # and the left-center on mobile, so content starts at x=500.
    img = canvas(1584, 396, (1250, 200), 320)
    text_block(img, 500, 92, 560, 0.82, show_icon=False)
    hub_card(img, 1130, 84, 390, 0.72, rows=3)
    save(img, "mailair-banner-linkedin.png")


def twitter():
    # 1500x500. Avatar overlaps bottom-left; top/bottom ~60px can crop.
    img = canvas(1500, 500, (1150, 250), 360)
    text_block(img, 330, 78, 560, 0.9, show_icon=False)
    hub_card(img, 960, 78, 440, 0.8, rows=3)
    save(img, "mailair-banner-twitter.png")


def facebook():
    # 820x312 desktop; mobile shows the center 640 wide, so keep x in 90..730.
    img = canvas(820, 312, (410, 156), 260)
    text_block(img, 110, 34, 600, 0.68, center=True)
    save(img, "mailair-banner-facebook.png")


def youtube():
    # 2560x1440; the area visible on every device is the centered 1546x423
    # (x 507..2053, y 508..931).
    img = canvas(2560, 1440, (1700, 720), 600)
    text_block(img, 560, 540, 780, 1.0, show_icon=False, show_url=False)
    hub_card(img, 1520, 520, 500, 0.9, rows=3)
    save(img, "mailair-banner-youtube.png")


def og_image():
    # 1200x630 — the standard link-preview size (LinkedIn, X, WhatsApp, Slack).
    img = canvas(1200, 630, (900, 320), 380)
    text_block(img, 70, 110, 560, 1.0)
    hub_card(img, 690, 140, 450, 0.82)
    save(img, "mailair-og.png")


def product_hunt_cover():
    img = canvas(1600, 960, (1200, 470), 520)
    text_block(img, 90, 230, 680, 1.25)
    hub_card(img, 880, 220, 620, 1.1)
    save(img, "mailair-ph-gallery-1-cover.png")


if __name__ == "__main__":
    for fn in (linkedin, twitter, facebook, youtube, og_image, product_hunt_cover):
        fn()
