#!/usr/bin/env python3
"""Hoer-Storyboard: Szenenplan + TTS-Stimmen -> Video, bevor es Bilder gibt.

Je Einstellung eine Bildkarte (SH-ID, Ort/Kamera, Bildbeschreibung, Tageszeit). Gibt es schon ein
Bild (03_Szenen_Flow_Bilder/<SH>*.jpg o. ae. ueber --bilder), wird es statt der Karte genommen.
Die Stimmen (<stimmen>/<SH>_<Sprecher>.wav) liegen am Anfang des geplanten Sprechfensters.
Video selbst baut build_episode_video.py (Intro, Titelkarte, Untertitel nur im Sprechfenster).

  python3 hoerstoryboard_bauen.py <szenenplan.json> <stimmen_ordner> <ausgabe.mp4> \
      --titel "Tante Frieda und Lorchen" [--intro 00_Intro_Maxi_Cartoons/Maxi_Cartoons_Intro.mp4] [--bilder DIR]
"""
import argparse, glob, json, os, re, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
W, H = 1920, 1080


def farbe(tageszeit):
    t = tageszeit.lower()
    if "abend" in t and "19" in t: return (22, 28, 52)
    if "dämmerung" in t: return (38, 44, 78)
    if "15:" in t or "kaffee" in t: return (92, 74, 52)
    return (70, 82, 92)


def wrap(d, text, font, maxw):
    out, line = [], ""
    for wort in text.split():
        t = (line + " " + wort).strip()
        if d.textlength(t, font=font) <= maxw: line = t
        else: out.append(line); line = wort
    if line: out.append(line)
    return out


def karte(s, path):
    img = Image.new("RGB", (W, H), farbe(s["tageszeit"]))
    d = ImageDraw.Draw(img)
    f1, f2, f3 = ImageFont.truetype(FB, 64), ImageFont.truetype(FR, 46), ImageFont.truetype(FR, 34)
    y = 150
    d.text((120, y), s["ort"], font=f1, fill=(255, 230, 160)); y += 110
    for z in wrap(d, s["bild"], f2, W - 240)[:7]:
        d.text((120, y), z, font=f2, fill=(245, 245, 245)); y += 62
    d.text((120, H - 300), s["tageszeit"], font=f3, fill=(190, 200, 210))
    img.save(path)


def fenster_start(f):
    m = re.match(r"\s*([\d,\.]+)", f or "")
    return float(m.group(1).replace(",", ".")) if m else 0.0


def dauer(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("plan"); ap.add_argument("stimmen"); ap.add_argument("out")
    ap.add_argument("--titel", default=""); ap.add_argument("--untertitel", default="Hör-Storyboard (Stimmen: Gemini-TTS)")
    ap.add_argument("--intro", default=os.path.join(ROOT, "00_Intro_Maxi_Cartoons/Maxi_Cartoons_Intro.mp4"))
    ap.add_argument("--ton", default="", help="ton.json mit sfx[] und musik[] (Soundeffekte/Musik je SH)"); ap.add_argument("--bilder", default=""); ap.add_argument("--titel_sek", type=float, default=3.0)
    a = ap.parse_args()
    plan = json.load(open(a.plan))
    work = os.path.splitext(os.path.abspath(a.out))[0] + "_arbeit"
    os.makedirs(work + "/karten", exist_ok=True)
    scenes, voices, t = [], [], 0.0
    starts = {}
    for s in plan:
        img = None
        if a.bilder:
            c = sorted(glob.glob(os.path.join(os.path.abspath(a.bilder), s["id"] + "*.jpg")) + glob.glob(os.path.join(os.path.abspath(a.bilder), s["id"] + "*.png")))
            img = c[0] if c else None
        if not img:
            img = os.path.join(work, "karten", s["id"] + ".png"); karte(s, img)
        starts[s["id"]] = (t, float(s["sek"]))
        sek = float(s["sek"]); frames = []
        wav = os.path.join(a.stimmen, f"{s['id']}_{s['sprecher']}.wav")
        if s["sprecher"] not in ("–", "-", "") and os.path.exists(wav):
            st = fenster_start(s["fenster"]); d = min(dauer(wav), sek - st)
            if st > 0: frames.append({"image": img, "seconds": st})
            frames.append({"image": img, "seconds": round(d + 0.3, 2) if st + d + 0.3 <= sek else round(sek - st, 2),
                           "speaker": s["sprecher"].upper(), "text": s["zeile"]})
            rest = sek - sum(f["seconds"] for f in frames)
            if rest > 0.01: frames.append({"image": img, "seconds": round(rest, 2)})
            voices.append((t + st, wav))
        else:
            frames.append({"image": img, "seconds": sek})
        scenes.append({"id": s["id"], "frames": frames}); t += sek
    man = {"title": "Maxi Cartoons – " + a.titel, "subtitle": a.untertitel, "width": W, "height": H, "fps": 24,
           "title_card_seconds": a.titel_sek, "end_card_seconds": 2.0, "end_card_text": "ENDE",
           "intro": os.path.abspath(a.intro), "scenes": scenes}
    mpath = os.path.splitext(os.path.abspath(a.out))[0] + "_manifest.json"
    json.dump(man, open(mpath, "w"), ensure_ascii=False, indent=1)
    stumm = os.path.join(work, "bild.mp4")
    subprocess.run([sys.executable, os.path.join(ROOT, "build_episode_video.py"), mpath, stumm, "--workdir", work + "/bev"], check=True)
    off = dauer(os.path.abspath(a.intro)) + a.titel_sek
    total = dauer(stumm)
    inputs, fl, labels = ["-i", stumm], [], []
    for i, (ts, wav) in enumerate(voices, start=1):
        inputs += ["-i", wav]
        ms = int((off + ts) * 1000)
        fl.append(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo,adelay={ms}|{ms}[v{i}]"); labels.append(f"[v{i}]")
    n = len(labels)
    if a.ton:  # Soundeffekte und Musik (Pfade relativ zur ton.json)
        ton = json.load(open(a.ton)); base = os.path.dirname(os.path.abspath(a.ton))
        pf = lambda p: p if os.path.isabs(p) else os.path.join(base, p)
        for c in ton.get("sfx", []):
            n += 1; inputs += ["-i", pf(c["datei"])]
            ms = int((off + starts[c["sh"]][0] + float(c.get("off", 0))) * 1000)
            fl.append(f"[{n}:a]aresample=48000,aformat=channel_layouts=stereo,volume={c.get('db', -6)}dB,adelay={ms}|{ms}[v{n}]"); labels.append(f"[v{n}]")
        for c in ton.get("musik", []):
            n += 1; inputs += ["-i", pf(c["datei"])]
            o = float(c.get("off", 0))                       # Einsatz innerhalb der ersten Szene (s)
            t0 = off + starts[c["von"]][0] + o; t1 = off + starts[c["bis"]][0] + starts[c["bis"]][1]
            ln = float(c["dauer"]) if "dauer" in c else t1 - t0
            ms = int(t0 * 1000); ab = float(c.get("ab", 0))
            fi, fo = float(c.get("fade_in", 0.8)), float(c.get("fade_out", 1.2))
            fl.append(f"[{n}:a]atrim=start={ab}:duration={ln:.2f},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,"
                      f"volume={c.get('db', -14)}dB,afade=t=in:d={max(fi,0.005)},afade=t=out:st={max(ln-fo,0):.2f}:d={max(fo,0.005)},adelay={ms}|{ms}[v{n}]"); labels.append(f"[v{n}]")
    fl.append(f"[0:a]aresample=48000[a0]")
    fl.append("[a0]" + "".join(labels) + f"amix=inputs={len(labels)+1}:normalize=0:duration=first[a]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(fl), "-map", "0:v", "-map", "[a]",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", f"{total}", os.path.abspath(a.out)], check=True)
    print(f"fertig: {a.out} ({total:.1f} s, {len(voices)} Stimmen)")


if __name__ == "__main__":
    main()
