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
    ap.add_argument("--paare", action="store_true", help="je Szene Startbild <SH>A und Endbild <SH>B, jedes die halbe Szenenzeit")
    ap.add_argument("--kuerzen", action="store_true", help="lange Pausen ohne Ton kürzen (Szenenlänge = Sprache/Effekt + kurzer Auslauf)")
    ap.add_argument("--format", choices=["quer", "hochkant"], default="quer")
    ap.add_argument("--fallback", default="", help="Ordner mit Ersatzbildern (z. B. Mockups), wenn ein Flow-Bild fehlt")
    a = ap.parse_args()
    global W, H
    if a.format == "hochkant":
        W, H = 1080, 1920
        if a.intro.endswith("Maxi_Cartoons_Intro.mp4"):
            a.intro = a.intro.replace("Maxi_Cartoons_Intro.mp4", "Maxi_Cartoons_Intro_Hochkant.mp4")
    plan = json.load(open(a.plan))
    ton = json.load(open(a.ton)) if a.ton else {"sfx": [], "musik": []}
    ids = [p["id"] for p in plan]
    musik_szenen = set()
    for c in ton.get("musik", []):
        musik_szenen.update(ids[ids.index(c["von"]): ids.index(c["bis"]) + 1])
    tbase = os.path.dirname(os.path.abspath(a.ton)) if a.ton else ""
    _dc = {}
    def sfx_laenge(c):
        p = c["datei"] if os.path.isabs(c["datei"]) else os.path.join(tbase, c["datei"])
        if p not in _dc: _dc[p] = dauer(p)
        return _dc[p]
    work = os.path.splitext(os.path.abspath(a.out))[0] + "_arbeit"
    os.makedirs(work + "/karten", exist_ok=True)
    scenes, voices, t = [], [], 0.0
    starts = {}

    def bild(sid, suffix):
        if not a.bilder: return None
        d = os.path.abspath(a.bilder)
        for pat in ([f"{sid}{suffix}.jpg", f"{sid}{suffix}.png", f"{sid}{suffix}_blender.jpg", f"{sid}{suffix}_blender.png"] if suffix
                    else [f"{sid}_blender.jpg", f"{sid}_blender.png", f"{sid}.jpg", f"{sid}.png"]):
            p = os.path.join(d, pat)
            if os.path.exists(p): return p
        return None

    for s in plan:
        sid = s["id"]; sek = float(s["sek"])
        wav = os.path.join(a.stimmen, f"{sid}_{s['sprecher']}.wav")
        sprache = s["sprecher"] not in ("–", "-", "") and os.path.exists(wav)
        st = fenster_start(s["fenster"]) if sprache else 0.0
        d = dauer(wav) if sprache else 0.0
        cues = [c for c in ton.get("sfx", []) if c["sh"] == sid]
        if a.kuerzen:
            lead = min(st, 0.35) if sprache else 0.0
            if sprache:
                sek = lead + d + 0.55
            else:
                ende = max([float(c.get("off", 0)) + min(sfx_laenge(c), 1.8) + 0.3 for c in cues] + [0.0])
                sek = max(2.5, min(ende if cues else (3.5 if sid in musik_szenen else 2.5), sek))
            for c in cues:                                  # Effekte, die später einsetzen, müssen noch in die Szene passen
                sek = max(sek, float(c.get("off", 0)) + min(sfx_laenge(c), 1.2))
            st = lead
        starts[sid] = (t, sek)
        # Zeitleiste: (Dauer, Sprecher, Text)
        if sprache:
            seg = ([(st, "", "")] if st > 0.01 else []) + [(round(d + 0.3, 2), s["sprecher"].upper(), s["zeile"])]
            rest = sek - sum(x[0] for x in seg)
            if rest > 0.01: seg.append((round(rest, 2), "", ""))
            voices.append((t + st, wav))
        else:
            seg = [(sek, "", "")]
        total_s = sum(x[0] for x in seg)
        imgA = bild(sid, "A" if a.paare else ""); imgB = bild(sid, "B") if a.paare else None
        if a.fallback and not imgA:
            fb = os.path.join(os.path.abspath(a.fallback), f"{sid}_blender.jpg")
            fb = fb if os.path.exists(fb) else os.path.join(os.path.abspath(a.fallback), f"{sid}_blender.png")
            imgA = fb if os.path.exists(fb) else None
        if a.fallback and imgA and a.paare and not imgB and not imgA.endswith(("_blender.jpg", "_blender.png")):
            imgB = None                                   # nur Startbild vorhanden: Szene bleibt mit einem Bild
        if not imgA:
            imgA = os.path.join(work, "karten", sid + ".png"); karte(s, imgA)
        frames, cur = [], 0.0
        half = total_s / 2
        for dur, sp, tx in seg:
            parts = [(dur, imgA)]
            if imgB:
                if cur >= half: parts = [(dur, imgB)]
                elif cur + dur > half: parts = [(half - cur, imgA), (cur + dur - half, imgB)]
            for dd, im in parts:
                if dd > 0.01: frames.append({"image": im, "seconds": round(dd, 3), "speaker": sp, "text": tx})
            cur += dur
        scenes.append({"id": sid, "frames": frames}); t += total_s
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
        base = os.path.dirname(os.path.abspath(a.ton))
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
