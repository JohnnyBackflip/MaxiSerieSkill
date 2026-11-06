#!/usr/bin/env python3
"""TTS-Stimmen gegen den Szenenplan pruefen (Whisper, venv .venv_sprache).

  .venv_sprache/bin/python stimmen_pruefen.py <szenenplan.json> <stimmen_ordner> [--nur SH010,SH020] [--grenze 0.8]

Gibt je <SH>_<Sprecher>.wav die Text-Aehnlichkeit aus ("OK" ab --grenze, sonst "!!").
Ob die richtige STIMME spricht, kann Whisper nicht pruefen -> anhoeren.
"""
import argparse, difflib, glob, json, os, re
from faster_whisper import WhisperModel


def norm(t):
    return re.sub(r"[^a-zäöüß ]", "", t.lower().replace("-", " ")).split()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("plan"); ap.add_argument("ordner")
    ap.add_argument("--nur", default=""); ap.add_argument("--grenze", type=float, default=0.8)
    a = ap.parse_args()
    plan = {x["id"]: x for x in json.load(open(a.plan))}
    nur = set(x for x in a.nur.split(",") if x)
    m = WhisperModel("large-v3-turbo", device="cpu", compute_type="int8")
    schlecht = 0
    for f in sorted(glob.glob(os.path.join(a.ordner, "SH*.wav"))):
        sh = os.path.basename(f).split("_")[0]
        if sh not in plan or (nur and sh not in nur):
            continue
        segs, _ = m.transcribe(f, language="de", beam_size=5)
        t = " ".join(s.text.strip() for s in segs)
        r = difflib.SequenceMatcher(None, norm(plan[sh]["zeile"]), norm(t)).ratio()
        ok = r >= a.grenze
        schlecht += not ok
        print(f"{'OK ' if ok else '!! '}{r:.2f} {sh}: {t}  || soll: {plan[sh]['zeile']}", flush=True)
    print(f"{schlecht} Zeile(n) unter {a.grenze}")


if __name__ == "__main__":
    main()
