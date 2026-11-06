#!/usr/bin/env python3
"""Spracherkennung (lokal, faster-whisper) für Flow/Veo-Clips – prüft, WAS WANN gesagt wird.

Aufruf (mit der Projekt-venv):
  .venv_sprache/bin/python sprache_abschreiben.py <clip.mp4|ordner> [--soll prompts.json] [--modell medium] [--bericht bericht.md]

--soll: JSON-Liste [{"id": "SH010", "prompt": "... [00:01-00:04] ... says: Text ..."}] (z. B. flow_video_prompts_r6.json);
        dann wird je Clip (Dateiname beginnt mit der id) der Soll-Satz + Zeitfenster aus den Zeitblöcken gelesen und verglichen.
Ausgabe: je Clip die erkannten Wörter mit Zeitstempel, Ähnlichkeit zum Soll-Satz, ob die Sprache im Soll-Zeitfenster liegt.
Hinweis: Wer spricht, erkennt Whisper NICHT (keine Sprechererkennung) – Stimme (Kind/Frau/Mann) bitte anhören.
"""
import argparse, difflib, glob, json, os, re, sys

def load_model(name):
    from faster_whisper import WhisperModel
    try:  # GPU nur, wenn die CUDA-Bibliotheken (cuBLAS/cuDNN) wirklich laden
        import numpy as np
        m = WhisperModel(name, device="cuda", compute_type="float32")
        list(m.transcribe(np.zeros(16000, dtype="float32"), language="de")[0])
        return m, "cuda"
    except Exception:
        return WhisperModel(name, device="cpu", compute_type="int8"), "cpu"

def norm(t):
    return re.sub(r"[^a-zäöüß ]", "", t.lower().replace("ß", "ss")).split()

def soll_aus_prompt(prompt):
    """Liest Zeitblöcke '[00:01-00:04] ... says: Text' -> Liste (start, ende, text)."""
    out = []
    for m in re.finditer(r"\[00:(\d\d)-00:(\d\d)\]([^\[]*)", prompt):
        a, b, body = int(m.group(1)), int(m.group(2)), m.group(3)
        s = re.search(r"(?:says|shouts|calls|laughs|asks)[^:]*:\s*(.+?)(?:\s+Voice:|$)", body.strip())
        if s:
            out.append((a, b, s.group(1).strip()))
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pfad"); ap.add_argument("--soll"); ap.add_argument("--modell", default="large-v3-turbo"); ap.add_argument("--bericht")
    a = ap.parse_args()
    clips = sorted(glob.glob(os.path.join(a.pfad, "SH*.mp4"))) if os.path.isdir(a.pfad) else [a.pfad]
    soll = {j["id"]: soll_aus_prompt(j["prompt"]) for j in json.load(open(a.soll))} if a.soll else {}
    model, dev = load_model(a.modell)
    lines = [f"# Spracherkennung ({a.modell}, {dev})", "", "| Clip | erkannt (Sprache laut VAD) | Soll | Text-Treffer | im Zeitfenster |", "|---|---|---|---|---|"]
    for c in clips:
        from faster_whisper.audio import decode_audio
        from faster_whisper.vad import get_speech_timestamps, VadOptions
        audio = decode_audio(c, 16000)
        vad = [(v["start"] / 16000, v["end"] / 16000) for v in get_speech_timestamps(audio, VadOptions(min_silence_duration_ms=150, threshold=0.4))]
        segs, _ = model.transcribe(c, language="de", word_timestamps=True, vad_filter=False, beam_size=5, temperature=0)
        words = [(w.start, w.end, w.word.strip()) for s in segs for w in (s.words or [])]
        heard = " ".join(w for _, _, w in words)
        # Zeitfenster aus der Sprachaktivität (VAD) – Whisper legt das erste Wort sonst gern auf 0,0 s
        stamp = f"{vad[0][0]:.1f}–{vad[-1][1]:.1f} s" if vad else "—"
        cid = os.path.basename(c).split("_")[0]
        sl = soll.get(cid, [])
        if sl:
            ref = " ".join(t for _, _, t in sl)
            ratio = difflib.SequenceMatcher(None, norm(ref), norm(heard)).ratio()
            lo, hi = min(x[0] for x in sl), max(x[1] for x in sl)
            ok = bool(vad) and vad[0][0] >= lo - 0.4 and vad[-1][1] <= hi + 0.4
            lines.append(f"| {os.path.basename(c)} | {heard} ({stamp}) | {ref} ({lo}–{hi} s) | {ratio:.0%} | {'ja' if ok else 'NEIN'} |")
        else:
            lines.append(f"| {os.path.basename(c)} | {heard} ({stamp}) | – | – | – |")
        print(os.path.basename(c), "| Sprache (VAD):", ", ".join(f"{a:.2f}-{b:.2f}" for a, b in vad), "|", heard, flush=True)
        for s0, s1, w in words:
            print(f"    {s0:5.2f}-{s1:5.2f}  {w}")
    rep = "\n".join(lines) + "\n\nHinweis: Sprechererkennung (wer spricht) leistet Whisper nicht – Stimmlage bitte anhören.\n"
    if a.bericht:
        open(a.bericht, "w").write(rep)
    print(rep)

if __name__ == "__main__":
    main()
