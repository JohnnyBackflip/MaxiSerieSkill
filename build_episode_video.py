#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Baut aus einem Szenen-Manifest (JSON) ein stummes Storyboard-Video:
Jedes Szenenbild wird nacheinander exakt für seine geplante Dauer angezeigt,
darunter steht der in diesem Moment gesprochene Text (Sprecher + Satz).

Aufruf:
    python3 build_episode_video.py <manifest.json> <ausgabe.mp4> [--workdir DIR]

Manifest-Format (alle Pfade absolut oder relativ zum Manifest):
{
  "title": "Maxi Cartoons – Folge 01",
  "subtitle": "Der verschwundene Hasi",
  "width": 1920, "height": 1080, "fps": 24,
  "title_card_seconds": 3.0,
  "end_card_seconds": 2.0,
  "end_card_text": "ENDE",
  "scenes": [
    {"id": "SH010", "title": "Start im Wohnzimmer",
     "frames": [
        {"image": "Sequenzen/SH010_1.jpg", "seconds": 2.0,
         "speaker": "MAXI", "text": "Ahoi, ihr Landratten!"},
        ...
     ]}
  ]
}
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageFont

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
FONT_REGULAR = os.path.join(FONT_DIR, "DejaVuSans.ttf")
FONT_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")

SPEAKER_COLORS = {
    "MAXI": (255, 214, 102),
    "ANNA": (255, 160, 122),
    "BEN": (135, 206, 250),
    "MAMA": (255, 236, 139),
    "MAMA KATRIN": (255, 236, 139),
    "PAPA": (152, 251, 152),
    "PAPA THOMAS": (152, 251, 152),
    "OMA ROSI": (221, 160, 221),
    "OPA HEINRICH": (210, 180, 140),
    "BELLO": (255, 182, 193),
    "KARL": (255, 140, 60),
    "ERZÄHLER": (220, 220, 220),
}


def load_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def wrap_text(draw, text, font, max_width):
    words = text.split()
    lines, line = [], ""
    for w in words:
        test = (line + " " + w).strip()
        if draw.textlength(test, font=font) <= max_width:
            line = test
        else:
            if line:
                lines.append(line)
            line = w
    if line:
        lines.append(line)
    return lines or [""]


def fit_image(img, w, h):
    """Bild proportional in w×h einpassen (Letterbox, dunkler Rand)."""
    canvas = Image.new("RGB", (w, h), (18, 16, 14))
    scale = min(w / img.width, h / img.height)
    nw, nh = max(1, round(img.width * scale)), max(1, round(img.height * scale))
    resized = img.convert("RGB").resize((nw, nh), Image.LANCZOS)
    canvas.paste(resized, ((w - nw) // 2, (h - nh) // 2))
    return canvas


def render_frame(image_path, w, h, speaker, text, scene_label, time_label, image_no=None):
    # Festes Untertitel-Band UNTER dem Bild (kein Überdecken des Szenenbilds):
    # Bild wird in den oberen Bereich eingepasst, das Band belegt die unteren ~18 %.
    band_h = int(h * 0.18)
    image_h = h - band_h
    base = Image.new("RGB", (w, h), (18, 16, 14))
    base.paste(fit_image(Image.open(image_path), w, image_h), (0, 0))
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    font_text = load_font(FONT_REGULAR, max(22, h // 26))
    font_speaker = load_font(FONT_BOLD, max(22, h // 30))
    font_small = load_font(FONT_REGULAR, max(16, h // 48))

    margin = w // 32
    max_text_w = w - 2 * margin
    lines = wrap_text(draw, text, font_text, max_text_w) if text else []
    line_h = int(font_text.size * 1.3)
    speaker_h = int(font_speaker.size * 1.3) if speaker else 0

    band_top = image_h
    draw.rectangle([0, band_top, w, h], fill=(0, 0, 0, 255))
    if speaker or lines:
        content_h = speaker_h + line_h * len(lines)
        y = band_top + max(8, (band_h - content_h) // 2)
        if speaker:
            col = SPEAKER_COLORS.get(speaker.upper(), (255, 255, 255))
            draw.text((margin, y), speaker, font=font_speaker, fill=col + (255,))
            y += speaker_h
        for ln in lines:
            draw.text((margin, y), ln, font=font_text, fill=(255, 255, 255, 255))
            y += line_h

    # kleines Szenen-Label oben links
    label = f"{scene_label}   {time_label}".strip()
    if label:
        pad = 8
        tw = draw.textlength(label, font=font_small)
        draw.rectangle([margin // 2, margin // 2, margin // 2 + tw + 2 * pad,
                        margin // 2 + font_small.size + 2 * pad], fill=(0, 0, 0, 120))
        draw.text((margin // 2 + pad, margin // 2 + pad), label, font=font_small,
                  fill=(255, 255, 255, 230))

    # Bildnummer groß oben rechts (zum Kritisieren: "Bild 07 ...")
    if image_no is not None:
        font_no = load_font(FONT_BOLD, max(28, h // 18))
        txt = f"Bild {image_no:02d}"
        pad = 12
        tw = draw.textlength(txt, font=font_no)
        x2 = w - margin // 2
        x1 = x2 - tw - 2 * pad
        y1 = margin // 2
        y2 = y1 + font_no.size + 2 * pad
        draw.rounded_rectangle([x1, y1, x2, y2], radius=10, fill=(255, 214, 60, 235))
        draw.text((x1 + pad, y1 + pad - font_no.size * 0.08), txt, font=font_no, fill=(20, 16, 10, 255))

    return Image.alpha_composite(base.convert("RGBA"), overlay).convert("RGB")


def render_card(w, h, title, subtitle):
    img = Image.new("RGB", (w, h), (24, 20, 18))
    draw = ImageDraw.Draw(img)
    f1 = load_font(FONT_BOLD, h // 12)
    f2 = load_font(FONT_REGULAR, h // 22)
    tw = draw.textlength(title, font=f1)
    draw.text(((w - tw) / 2, h * 0.38), title, font=f1, fill=(255, 220, 120))
    if subtitle:
        sw = draw.textlength(subtitle, font=f2)
        draw.text(((w - sw) / 2, h * 0.38 + f1.size * 1.4), subtitle, font=f2,
                  fill=(240, 240, 240))
    return img


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("manifest")
    ap.add_argument("output")
    ap.add_argument("--workdir", default=None)
    args = ap.parse_args()

    with open(args.manifest, encoding="utf-8") as fh:
        m = json.load(fh)
    base_dir = os.path.dirname(os.path.abspath(args.manifest))
    w, h, fps = int(m.get("width", 1920)), int(m.get("height", 1080)), int(m.get("fps", 24))

    workdir = args.workdir or tempfile.mkdtemp(prefix="episode_video_")
    os.makedirs(workdir, exist_ok=True)
    frames_dir = os.path.join(workdir, "frames")
    if os.path.isdir(frames_dir):
        shutil.rmtree(frames_dir)
    os.makedirs(frames_dir)

    entries = []  # (png path, seconds)
    idx = 0

    tc = float(m.get("title_card_seconds", 0) or 0)
    if tc > 0:
        p = os.path.join(frames_dir, f"f{idx:04d}.png")
        render_card(w, h, m.get("title", ""), m.get("subtitle", "")).save(p)
        entries.append((p, tc))
        idx += 1

    total = 0.0
    missing = []
    t_cursor = tc
    number_images = bool(m.get("number_images", True))
    image_numbers = {}   # Bildpfad -> laufende Nummer (gleiches Bild = gleiche Nummer)
    bildliste = []       # (Nr, Startzeit, Szene, Datei)
    for scene in m["scenes"]:
        sid = scene.get("id", "")
        for fr in scene["frames"]:
            img_path = fr["image"]
            if not os.path.isabs(img_path):
                img_path = os.path.join(base_dir, img_path)
            if not os.path.isfile(img_path):
                missing.append(img_path)
                continue
            secs = float(fr["seconds"])
            time_label = f"{t_cursor:05.1f}s"
            if img_path not in image_numbers:
                image_numbers[img_path] = len(image_numbers) + 1
                bildliste.append((image_numbers[img_path], t_cursor, sid, os.path.basename(img_path)))
            p = os.path.join(frames_dir, f"f{idx:04d}.png")
            render_frame(img_path, w, h, fr.get("speaker", ""), fr.get("text", ""),
                         sid, time_label, image_numbers[img_path] if number_images else None).save(p)
            entries.append((p, secs))
            idx += 1
            total += secs
            t_cursor += secs

    ec = float(m.get("end_card_seconds", 0) or 0)
    if ec > 0:
        p = os.path.join(frames_dir, f"f{idx:04d}.png")
        render_card(w, h, m.get("end_card_text", "ENDE"), m.get("title", "")).save(p)
        entries.append((p, ec))
        idx += 1

    if missing:
        print("FEHLENDE BILDER:", file=sys.stderr)
        for mp in missing:
            print("  " + mp, file=sys.stderr)
    if not entries:
        sys.exit("Keine Frames erzeugt.")

    list_path = os.path.join(workdir, "concat.txt")
    with open(list_path, "w", encoding="utf-8") as fh:
        for p, secs in entries:
            fh.write(f"file '{p}'\nduration {secs:.3f}\n")
        fh.write(f"file '{entries[-1][0]}'\n")  # letzter Frame muss wiederholt werden

    os.makedirs(os.path.dirname(os.path.abspath(args.output)) or ".", exist_ok=True)
    cmd = [
        "ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", list_path,
        "-vf", f"fps={fps},format=yuv420p", "-c:v", "libx264", "-preset", "medium",
        "-crf", "18", "-movflags", "+faststart", "-an", args.output,
    ]
    subprocess.run(cmd, check=True)
    intro_off = 0.0
    intro = m.get("intro")
    if intro:  # Serien-Intro (mit Ton) vor das stumme Storyboard setzen
        ip = intro if os.path.isabs(intro) else os.path.join(base_dir, intro)
        intro_off = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", ip]))
        tmp = os.path.splitext(args.output)[0] + "_ohne_intro_tmp.mp4"
        os.replace(args.output, tmp)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", ip, "-i", tmp, "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
                        "-filter_complex", f"[0:v]scale={w}:{h}:force_original_aspect_ratio=decrease,pad={w}:{h}:(ow-iw)/2:(oh-ih)/2,setsar=1,fps={fps},format=yuv420p[v0];"
                        f"[0:a]aresample=48000,aformat=channel_layouts=stereo[a0];[1:v]setsar=1,fps={fps},format=yuv420p[v1];[2:a]atrim=duration={total + tc + ec}[a1];"
                        "[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]", "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "18", "-c:a", "aac",
                        "-movflags", "+faststart", args.output], check=True)
        os.remove(tmp)
        print(f"Intro vorangestellt: {ip} ({intro_off:.1f}s)")
    print(f"Video geschrieben: {args.output}")
    if number_images and bildliste:
        lp = os.path.splitext(args.output)[0] + "_Bildliste.md"
        with open(lp, "w", encoding="utf-8") as fh:
            fh.write(f"# Bildliste – {m.get('title', '')}\n\n")
            fh.write("Die Nummer steht im Video oben rechts (gelb). Kritik bitte als „Bild NN: …“.\n\n")
            fh.write("| Bild | ab Sekunde | Szene | Datei |\n|---|---|---|---|\n")
            for no, t0, sid, fn in bildliste:
                t0 += intro_off
                fh.write(f"| {no:02d} | {int(t0)//60}:{t0%60:04.1f} | {sid} | `{fn}` |\n")
        print(f"Bildliste geschrieben: {lp}")
    print(f"Szenenbilder: {idx - (1 if tc > 0 else 0) - (1 if ec > 0 else 0)} | "
          f"Szenen-Spielzeit: {total:.1f}s | Gesamt inkl. Karten: {total + tc + ec:.1f}s")
    if missing:
        print(f"ACHTUNG: {len(missing)} Bilder fehlten und wurden übersprungen.")
        sys.exit(2)


if __name__ == "__main__":
    main()
