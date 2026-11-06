#!/usr/bin/env python3
"""Soundeffekte mit ElevenLabs (Sound-Generation-API) aus einem Katalog erzeugen.
NUR Soundeffekte – Musik kommt aus Gemini Lyria (Chrome-Plugin), nicht von hier (User-Vorgabe 2026-11-06).
Key: ~/.elevenlabs_key (eine Zeile, NIE ins Repo) oder $ELEVENLABS_KEY_FILE.

  python3 sfx_elevenlabs.py <katalog.json> <ausgabeordner> [--nur id1,id2] [--force]
katalog.json: {"auto_parkt": {"prompt": "...", "dauer": 5, "einfluss": 0.5}, ...}  -> <ausgabeordner>/<id>.mp3
"""
import argparse, json, os, subprocess, urllib.request, urllib.error

KEYFILE = os.environ.get("ELEVENLABS_KEY_FILE", os.path.expanduser("~/.elevenlabs_key"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("katalog"); ap.add_argument("out")
    ap.add_argument("--nur", default=""); ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    key = open(KEYFILE).read().strip()
    kat = json.load(open(a.katalog)); nur = set(x for x in a.nur.split(",") if x)
    os.makedirs(a.out, exist_ok=True)
    for sid, c in kat.items():
        if nur and sid not in nur:
            continue
        dst = os.path.join(a.out, sid + ".mp3")
        if os.path.exists(dst) and not a.force:
            continue
        body = json.dumps({"text": c["prompt"], "duration_seconds": c.get("dauer", 3),
                           "prompt_influence": c.get("einfluss", 0.5)}).encode()
        req = urllib.request.Request("https://api.elevenlabs.io/v1/sound-generation?output_format=mp3_44100_128", data=body,
                                     headers={"xi-api-key": key, "Content-Type": "application/json"})
        try:
            data = urllib.request.urlopen(req, timeout=120).read()
        except urllib.error.HTTPError as e:
            print(f"{sid}: HTTP {e.code} {e.read()[:120]!r}"); continue
        raw = dst + ".roh.mp3"; open(raw, "wb").write(data)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-af", "loudnorm=I=-20:TP=-2", dst], check=True)
        os.remove(raw)
        dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", dst]))
        open(os.path.join(a.out, sid + ".prompt.txt"), "w").write(c["prompt"] + "\n")
        print(f"{sid}: {dur:.1f} s", flush=True)


if __name__ == "__main__":
    main()
