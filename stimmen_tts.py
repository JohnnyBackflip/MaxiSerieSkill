#!/usr/bin/env python3
"""Stimmen fuer die Figuren mit Gemini-TTS erzeugen (Hoer-Storyboard).

Liest einen Szenenplan (JSON-Liste mit id, sprecher, zeile) und eine Besetzung
(JSON: Sprecher -> voice, stil, halbtoene, tempo) und schreibt je Zeile
<out>/<SH>_<Sprecher>.wav (24 kHz mono). Keys: eine Zeile je Key in
~/.config/maxi/google_api_keys.txt (NIE ins Projekt/Repo legen) oder $GOOGLE_API_KEYS_FILE.
Die Keys werden reihum benutzt; bei 429/Fehler kommt der naechste Key.

  python3 stimmen_tts.py <szenenplan.json> <besetzung.json> <ausgabeordner> [--nur SH010,SH020] [--force]
"""
import argparse, base64, json, os, subprocess, sys, time, urllib.request, urllib.error, wave

MODEL = os.environ.get("TTS_MODEL", "gemini-2.5-flash-preview-tts")
KEYFILE = os.environ.get("GOOGLE_API_KEYS_FILE", os.path.expanduser("~/.config/maxi/google_api_keys.txt"))


def load_keys():
    return [k.strip() for k in open(KEYFILE) if k.strip()]


def tts(text, voice, keys, state):
    body = json.dumps({
        "contents": [{"parts": [{"text": text}]}],
        "generationConfig": {"responseModalities": ["AUDIO"],
                             "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}}},
    }).encode()
    last = None
    for attempt in range(len(keys) * 2):
        k = keys[state["i"] % len(keys)]
        state["i"] += 1
        req = urllib.request.Request(
            f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={k}",
            data=body, headers={"Content-Type": "application/json"})
        try:
            r = json.load(urllib.request.urlopen(req, timeout=120))
            return base64.b64decode(r["candidates"][0]["content"]["parts"][0]["inlineData"]["data"])
        except urllib.error.HTTPError as e:
            last = f"HTTP {e.code}"
            if e.code == 429:
                time.sleep(2)
        except Exception as e:  # leere Antwort o. ae.
            last = type(e).__name__
        time.sleep(1)
    raise RuntimeError(f"TTS fehlgeschlagen ({last})")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("plan"); ap.add_argument("besetzung"); ap.add_argument("out")
    ap.add_argument("--nur", default=""); ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    plan = json.load(open(a.plan)); cast = json.load(open(a.besetzung))
    nur = set(x for x in a.nur.split(",") if x)
    os.makedirs(a.out, exist_ok=True)
    keys = load_keys(); state = {"i": 0}
    for s in plan:
        if s["sprecher"] in ("–", "-", "") or (nur and s["id"] not in nur):
            continue
        rolle = s.get("stimme") or s["sprecher"]
        c = cast[rolle]
        name = f"{s['id']}_{s['sprecher']}"
        wav = os.path.join(a.out, name + ".wav")
        if os.path.exists(wav) and not a.force:
            continue
        stil = s.get("stil_zusatz", "")
        prompt = f"{c['stil']}{(' ' + stil) if stil else ''}: {s['zeile']}"
        pcm = tts(prompt, c["voice"], keys, state)
        roh = os.path.join(a.out, name + "_roh.wav")
        with wave.open(roh, "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(pcm)
        st = float(c.get("halbtoene", 0)); tempo = float(c.get("tempo", 1.0))
        f = 2 ** (st / 12)
        flt = f"asetrate={int(24000*f)},aresample=24000,atempo={tempo/f:.5f},silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,loudnorm=I=-18:TP=-2"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", roh, "-af", flt, "-ar", "24000", "-ac", "1", wav], check=True)
        os.remove(roh)
        dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", wav]))
        print(f"{name}: {dur:.2f} s  ({c['voice']})", flush=True)
        with open(os.path.join(a.out, name + ".prompt.txt"), "w") as fh:
            fh.write(f"voice={c['voice']} halbtoene={st} tempo={tempo}\n{prompt}\n")


if __name__ == "__main__":
    main()
