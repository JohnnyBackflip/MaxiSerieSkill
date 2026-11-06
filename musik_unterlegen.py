#!/usr/bin/env python3
"""Hintergrundmusik unter ein fertiges Video legen – das Original bleibt UNVERÄNDERT, es entsteht eine neue Datei.

  python3 musik_unterlegen.py <video.mp4> <ausgabe.mp4> --cue <musik.mp3>@<von_s>-<bis_s>[:ab=<s>][:laut=<dB>] [--cue …]
        [--ducking] [--fade 1.0]

Beispiel: --cue wald.mp3@35-80:ab=0:laut=-16  -> Musik ab Sekunde 0 der Datei, im Video von 35 s bis 80 s, Pegel -16 dB.
--ducking: Musik wird automatisch leiser, sobald jemand spricht (Sidechain auf die Originaltonspur), damit Dialoge verständlich bleiben.
Jeder Cue bekommt weiche Ein-/Ausblendungen (--fade). Video wird nur kopiert (kein Neukodieren).
"""
import argparse, re, subprocess

def parse_cue(c):
    m = re.match(r"(.+)@([\d.]+)-([\d.]+)((?::\w+=[-\d.]+)*)$", c)
    if not m:
        raise SystemExit(f"Cue nicht verstanden: {c}")
    opts = dict(o.split("=") for o in m.group(4).strip(":").split(":") if o)
    return {"datei": m.group(1), "von": float(m.group(2)), "bis": float(m.group(3)),
            "ab": float(opts.get("ab", 0)), "laut": float(opts.get("laut", -16))}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video"); ap.add_argument("ausgabe")
    ap.add_argument("--cue", action="append", required=True); ap.add_argument("--ducking", action="store_true"); ap.add_argument("--fade", type=float, default=1.0)
    a = ap.parse_args()
    cues = [parse_cue(c) for c in a.cue]
    vdur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", a.video]))
    inp = ["-i", a.video]
    fl = []
    for i, c in enumerate(cues, start=1):
        d = c["bis"] - c["von"]; f = min(a.fade, d / 3)
        inp += ["-i", c["datei"]]
        fl.append(f"[{i}:a]atrim=start={c['ab']}:duration={d},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,"
                  f"volume={c['laut']}dB,afade=t=in:st=0:d={f},afade=t=out:st={d-f}:d={f},adelay={int(c['von']*1000)}|{int(c['von']*1000)}[m{i}]")
    mus = "".join(f"[m{i}]" for i in range(1, len(cues) + 1))
    fl.append(f"{mus}amix=inputs={len(cues)}:normalize=0:duration=longest,apad=whole_dur={vdur}[musik]")
    key_idx = len(cues) + 1
    inp += ["-i", a.video]   # Originalton ein zweites Mal als unabhängige Ducking-Quelle (asplit blockierte am Ende)
    fl.append(f"[0:a]aresample=48000,aformat=channel_layouts=stereo,apad=whole_dur={vdur}[dialog]")
    fl.append(f"[{key_idx}:a]aresample=48000,aformat=channel_layouts=stereo,apad=whole_dur={vdur}[key]")
    if a.ducking:
        fl.append("[musik][key]sidechaincompress=threshold=0.05:ratio=4:attack=30:release=500:makeup=1[musikd]")
    else:
        fl.append("[key]anullsink"); fl.append("[musik]anull[musikd]")
    fl.append(f"[dialog][musikd]amix=inputs=2:normalize=0:duration=longest,alimiter=limit=0.95,atrim=duration={vdur}[out]")
    # Schritt 1: Ton allein mischen (beim direkten Muxen mit Untertitelspur riss der Ton am letzten Untertitel ab)
    import os, tempfile
    ton = os.path.join(tempfile.mkdtemp(), "ton.m4a")
    subprocess.run(["ffmpeg", "-v", "error", "-y", *inp, "-filter_complex", ";".join(fl), "-map", "[out]", "-c:a", "aac", "-b:a", "192k", ton], check=True)
    # Schritt 2: Video + neuer Ton + Untertitel des Originals zusammenpacken (Video/Untertitel nur kopiert)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a.video, "-i", ton, "-map", "0:v", "-map", "1:a", "-map", "0:s?",
                    "-c:v", "copy", "-c:a", "copy", "-c:s", "copy", "-max_interleave_delta", "0", a.ausgabe], check=True)
    # Kontrolle: Tonspur muss so lang sein wie das Video
    adur = float(subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=duration", "-of", "csv=p=0", a.ausgabe]))
    if adur < vdur - 0.2:
        raise SystemExit(f"FEHLER: Tonspur {adur:.2f}s kürzer als Video {vdur:.2f}s")
    print("geschrieben:", a.ausgabe, "| Cues:", [(c["datei"].split("/")[-1], c["von"], c["bis"], c["laut"]) for c in cues])

if __name__ == "__main__":
    main()
