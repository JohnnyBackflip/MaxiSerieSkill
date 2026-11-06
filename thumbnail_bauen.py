#!/usr/bin/env python3
"""Thumbnail für eine Maxi-Cartoons-Folge bauen: Flow-Bild (ohne Text) + Logo + Titel + Folgen-Plakette.

python3 thumbnail_bauen.py <hintergrund.jpg> <ausgabe.jpg> --format quer|hochkant \
    --zeile "PILZE IM" --zeile "HERBSTWALD!" --folge "FOLGE 2" [--titel-seite links|rechts]

quer     -> 1280×720  (YouTube), Titel links oder rechts, Logo oben
hochkant -> 1080×1920 (TikTok-Cover), Logo + Titel im oberen Drittel
"""
import argparse
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

ROOT = os.environ.get("MAXI_ROOT", os.path.dirname(os.path.abspath(__file__)))
LOGO = f"{ROOT}/00_Intro_Maxi_Cartoons/Maxi_Cartoons_Logo.png"
FONT_KANDIDATEN = [
    "/usr/share/fonts/opentype/cantarell/Cantarell-ExtraBold.otf",   # Wunschschrift
    "/usr/share/fonts/truetype/open-sans/OpenSans-ExtraBold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",           # fast überall vorhanden
]
FONT = next((f for f in FONT_KANDIDATEN if os.path.isfile(f)), FONT_KANDIDATEN[-1])
NAVY = (13, 42, 92)          # Rand wie im Logo
GELB = (255, 214, 64)
WEISS = (255, 255, 255)
ORANGE = (255, 138, 30)


def fuellen(img, w, h, fokus_x=0.5, fokus_y=0.5):
    return ImageOps.fit(img.convert("RGB"), (w, h), Image.LANCZOS, centering=(fokus_x, fokus_y))


def text_block(canvas, zeilen, x, y, max_breite, ausrichtung="links", farben=(WEISS, GELB)):
    """Zeilen untereinander, jede so groß wie möglich (gemeinsame Größe), dicker Navy-Rand + Schatten."""
    groesse = 400
    while groesse > 20:
        f = ImageFont.truetype(FONT, groesse)
        if all(f.getbbox(z)[2] - f.getbbox(z)[0] <= max_breite for z in zeilen):
            break
        groesse -= 4
    f = ImageFont.truetype(FONT, groesse)
    rand = max(6, groesse // 9)
    schatten = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    schrift = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    ds, dt = ImageDraw.Draw(schatten), ImageDraw.Draw(schrift)
    zy = y
    for i, z in enumerate(zeilen):
        bb = f.getbbox(z)
        bw = bb[2] - bb[0]
        zx = x - bb[0] if ausrichtung == "links" else x + (max_breite - bw) // 2 - bb[0]
        off = rand // 2 + 4
        ds.text((zx + off, zy + off), z, font=f, fill=(0, 0, 0, 150), stroke_width=rand, stroke_fill=(0, 0, 0, 150))
        dt.text((zx, zy), z, font=f, fill=farben[i % len(farben)], stroke_width=rand, stroke_fill=NAVY)
        zy += int((bb[3] - bb[1]) * 1.12) + rand
    schatten = schatten.filter(ImageFilter.GaussianBlur(rand * 0.6))
    canvas.alpha_composite(schatten)
    canvas.alpha_composite(schrift)
    return zy


def plakette(canvas, text, cx, cy, hoehe, drehung=-6):
    f = ImageFont.truetype(FONT, int(hoehe * 0.62))
    bb = f.getbbox(text)
    bw, bh = bb[2] - bb[0], bb[3] - bb[1]
    pad = int(hoehe * 0.35)
    w, h = bw + 2 * pad, hoehe
    rand = max(4, hoehe // 12)
    tafel = Image.new("RGBA", (w + 4 * rand, h + 4 * rand), (0, 0, 0, 0))
    d = ImageDraw.Draw(tafel)
    d.rounded_rectangle([2 * rand, 2 * rand, w + 2 * rand, h + 2 * rand], radius=h // 2,
                        fill=ORANGE, outline=WEISS, width=rand)
    d.text((2 * rand + pad - bb[0], 2 * rand + (h - bh) // 2 - bb[1]), text, font=f, fill=WEISS,
           stroke_width=max(2, rand // 2), stroke_fill=NAVY)
    tafel = tafel.rotate(drehung, resample=Image.BICUBIC, expand=True)
    canvas.alpha_composite(tafel, (int(cx - tafel.width / 2), int(cy - tafel.height / 2)))


def logo(canvas, x, y, breite):
    lg = Image.open(LOGO).convert("RGBA")
    lg = lg.resize((breite, int(lg.height * breite / lg.width)), Image.LANCZOS)
    canvas.alpha_composite(lg, (x, y))
    return y + lg.height


def verlauf(canvas, seite, staerke=150):
    """Leichte Abdunklung hinter dem Titel, damit er auf jedem Bild lesbar ist."""
    w, h = canvas.size
    maske = Image.new("L", (w, h), 0)
    px = maske.load()
    for i in range(w if seite in ("links", "rechts") else h):
        if seite == "links":
            a = max(0.0, 1 - i / (w * 0.6))
        elif seite == "rechts":
            a = max(0.0, (i - w * 0.4) / (w * 0.6))
        else:  # oben
            a = max(0.0, 1 - i / (h * 0.5))
        v = int(staerke * a ** 1.4)
        if seite in ("links", "rechts"):
            for j in range(h):
                px[i, j] = v
        else:
            for j in range(w):
                px[j, i] = v
    dunkel = Image.new("RGBA", (w, h), (10, 20, 40, 255))
    dunkel.putalpha(maske)
    canvas.alpha_composite(dunkel)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("hintergrund")
    ap.add_argument("ausgabe")
    ap.add_argument("--format", choices=["quer", "hochkant"], default="quer")
    ap.add_argument("--zeile", action="append", required=True)
    ap.add_argument("--folge", default="")
    ap.add_argument("--titel-seite", choices=["links", "rechts"], default="links")
    ap.add_argument("--fokus-x", type=float, default=0.5)
    ap.add_argument("--fokus-y", type=float, default=0.5)
    a = ap.parse_args()

    if a.format == "quer":
        W, H = 1280, 720
        c = fuellen(Image.open(a.hintergrund), W, H, a.fokus_x, a.fokus_y).convert("RGBA")
        verlauf(c, a.titel_seite)
        rand = 40
        bx = rand if a.titel_seite == "links" else W // 2
        y = logo(c, bx, rand - 6, 460) + 14
        ende = text_block(c, a.zeile, bx, y, W // 2 - rand - 10)
        if a.folge:
            plakette(c, a.folge, bx + 120, min(ende + 62, H - 55), 74)
    else:
        W, H = 1080, 1920
        c = fuellen(Image.open(a.hintergrund), W, H, a.fokus_x, a.fokus_y).convert("RGBA")
        verlauf(c, "oben", 140)
        y = logo(c, 90, 150, W - 180) + 30
        ende = text_block(c, a.zeile, 70, y, W - 140, ausrichtung="mitte")
        if a.folge:
            plakette(c, a.folge, int(W * 0.19), ende + 150, 100, drehung=8)

    c.convert("RGB").save(a.ausgabe, quality=92)
    print("geschrieben:", a.ausgabe, c.size)


if __name__ == "__main__":
    main()
