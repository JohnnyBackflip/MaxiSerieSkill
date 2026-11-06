#!/usr/bin/env python3
"""Flow/Veo-Clips anhand der Spracherkennung zuschneiden und zu einer Folge zusammensetzen.

  .venv_sprache/bin/python flow_clips_schneiden.py <ausgabe.mp4> --clips <ordner1> [<ordner2> ...] --soll <p1.json> [<p2.json> ...]
        [--reihenfolge SH010,SH011,...] [--titel "…"] [--pause 0.5] [--intro intro.mp4] [--einblenden 1.0]

Regeln: Anfang bleibt (Veo spricht meist ab 0 s); Ende = letztes erkanntes Wort + Pause (Standard 0,5 s).
Enthält der Soll-Text Laute, die Whisper nicht als Wort erkennt (Hehe, Bäääh, Hä), zählt das Ende der Sprachaktivität (VAD).
Ohne Sprache oder wenn der Schnitt < 2,5 s würde: Clip bleibt ungeschnitten. Schreibt <ausgabe>_Schnittliste.md und <ausgabe>.srt (Untertitel = erkannte Sätze).
"""
import argparse, glob, json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sprache_abschreiben import load_model, soll_aus_prompt, norm

def dur(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]).decode())

def srt_t(s):
    h, m = int(s // 3600), int(s % 3600 // 60); sec = s % 60
    return f"{h:02d}:{m:02d}:{int(sec):02d},{int(round((sec - int(sec)) * 1000)):03d}"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ausgabe"); ap.add_argument("--clips", nargs="+", required=True); ap.add_argument("--soll", nargs="+", default=[])
    ap.add_argument("--reihenfolge"); ap.add_argument("--titel"); ap.add_argument("--intro", help="Intro-Video, das vor allem läuft"); ap.add_argument("--start", action="append", default=[], help="SHxxx=Sekunden: Clip erst ab hier verwenden (z. B. Musik-Vorspann von Veo wegschneiden)"); ap.add_argument("--pause", type=float, default=0.5); ap.add_argument("--einblenden", type=float, default=0.0, help="erste Einstellung nach dem Intro aus Schwarz einblenden (Sekunden)"); ap.add_argument("--modell", default="large-v3-turbo")
    a = ap.parse_args()
    from faster_whisper.audio import decode_audio
    from faster_whisper.vad import get_speech_timestamps, VadOptions
    clips = {}
    for d in a.clips:
        for f in sorted(glob.glob(os.path.join(d, "SH*.mp4"))):
            clips[os.path.basename(f).split("_")[0]] = f
    soll, speaker = {}, {}
    for s in a.soll:
        for j in json.load(open(s)):
            soll[j["id"]] = soll_aus_prompt(j["prompt"]); speaker[j["id"]] = j.get("sprecher", "")
    order = a.reihenfolge.split(",") if a.reihenfolge else sorted(clips)
    model, dev = load_model(a.modell)
    work = os.path.splitext(a.ausgabe)[0] + "_teile"; os.makedirs(work, exist_ok=True)
    parts, rows, srt, t0 = [], [], [], 0.0
    starts = {k: float(v) for k, v in (x.split("=") for x in a.start)}
    if a.intro:
        ip = os.path.join(work, "000a_intro.mp4")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a.intro, "-vf", "scale=1280:720,setsar=1,fps=24,format=yuv420p", "-af", "aresample=48000,aformat=channel_layouts=stereo",
                        "-c:v", "libx264", "-crf", "18", "-c:a", "aac", ip], check=True)
        parts.append(ip); t0 += dur(ip)
    if a.titel:
        tp = os.path.join(work, "000b_titel.mp4")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "color=c=0x1f364d:s=1280x720:d=3:r=24", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
                        "-vf", f"drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:text='{a.titel}':fontsize=44:fontcolor=white:x=(w-tw)/2:y=(h-th)/2",
                        "-t", "3", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", tp], check=True)
        parts.append(tp); t0 += 3.0
    for i, sid in enumerate(order):
        f = clips.get(sid)
        if not f:
            rows.append(f"| {sid} | FEHLT | | | |"); continue
        st = starts.get(sid, 0.0)
        if st > 0:
            tmp = os.path.join(work, f"_src_{sid}.mp4")
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{st:.3f}", "-i", f, "-c:v", "libx264", "-crf", "16", "-c:a", "aac", tmp], check=True)
            f = tmp
        D = dur(f)
        audio = decode_audio(f, 16000)
        vad = [(v["start"] / 16000, v["end"] / 16000) for v in get_speech_timestamps(audio, VadOptions(min_silence_duration_ms=150, threshold=0.4))]
        segs, _ = model.transcribe(f, language="de", word_timestamps=True, vad_filter=False, beam_size=5, temperature=0)
        words = [(w.start, w.end, w.word.strip()) for s in segs for w in (s.words or [])]
        heard = " ".join(w for _, _, w in words)
        ref = " ".join(t for _, _, t in soll.get(sid, []))
        missing = [t for t in norm(ref) if t not in norm(heard)]
        laut = any(re.match(r"^(he|hä|bä|mm|ja)", t) for t in missing)
        if words:
            we = words[-1][1]
            # Ende des Sprachabschnitts (VAD), in dem das letzte Wort liegt – Whisper-Wortzeiten enden oft zu früh
            seg_end = max([b for (s0, b) in vad if s0 <= we + 0.2] or [we])
            end = max(we, seg_end if not laut else (vad[-1][1] if vad else we)) + a.pause
        else:
            end = D
        end = min(end, D)
        if end < 2.5:
            end = min(D, 2.5)
        cut = D - end > 0.15
        out = os.path.join(work, f"{i+1:03d}_{sid}.mp4")
        fade_in = f",fade=t=in:st=0:d={a.einblenden}" if (a.einblenden > 0 and i == 0) else ""
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f, "-t", f"{end:.3f}", "-vf", "scale=1280:720,setsar=1,fps=24,format=yuv420p" + fade_in,
                        "-af", f"aresample=48000,aformat=channel_layouts=stereo,afade=t=out:st={max(0, end-0.12):.3f}:d=0.12",
                        "-c:v", "libx264", "-crf", "18", "-c:a", "aac", out], check=True)
        parts.append(out)
        if words:
            srt.append((t0 + words[0][0], t0 + min(words[-1][1] + 0.3, end), f"{speaker.get(sid,'').upper()}: {heard}".strip(": ")))
        rows.append(f"| {sid} | {D:.2f} s{f' (ab {st:.2f} s)' if st else ''} | {end:.2f} s | {'geschnitten' if cut else 'voll'} ({'VAD-Ende, Laut' if laut else 'letztes Wort'} +{a.pause}s) | {heard} |")
        print(sid, f"{D:.2f} -> {end:.2f}", heard, flush=True)
        t0 += end
    lst = os.path.join(work, "liste.txt")
    open(lst, "w").write("".join(f"file '{os.path.abspath(p)}'\n" for p in parts))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c:v", "libx264", "-crf", "18", "-c:a", "aac", a.ausgabe], check=True)
    base = os.path.splitext(a.ausgabe)[0]
    open(base + ".srt", "w").write("".join(f"{n+1}\n{srt_t(s)} --> {srt_t(e)}\n{tx}\n\n" for n, (s, e, tx) in enumerate(srt)))
    open(base + "_Schnittliste.md", "w").write("# Schnittliste (" + a.modell + ", " + dev + ")\n\n| Einstellung | Clip | behalten | Schnitt | erkannt |\n|---|---|---|---|---|\n" + "\n".join(rows) + f"\n\nGesamtlänge: {t0:.1f} s\n")
    print("fertig", a.ausgabe, f"{t0:.1f}s")

if __name__ == "__main__":
    main()
