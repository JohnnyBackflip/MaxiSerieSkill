#!/usr/bin/env python3
"""Serien-Intro „Maxi Cartoons“ v2: Nahaufnahmen (Maxi, Mama, Papa) + Schlussbild alle winken zusammen,
Logo „ploppt“ über den Figuren auf, darunter Song-Ausschnitt.

  python3 intro_bauen_v2.py <ausgabe.mp4> --logo <logo.png> --song <song.mp3> \
      --clip MAXI.mp4:0.0:1.4 --clip MAMA.mp4:0.1:1.4 --clip PAPA.mp4:0.2:1.4 --clip ALLE.mp4:0.0:3.0 \
      [--musik-ab 60] [--musik-aus 0.8] [--logo-ab-letzter 0.35] [--logo-breite 860] [--logo-y 92] [--xfade 0.15|0]
--clip Datei:Start:Dauer[:Ausschnitt] (Sekunden). Ausschnitt nur bei --format hochkant: Zahl 0..1 = horizontale
Bildmitte des 9:16-Ausschnitts (Standard 0.5), „box“ = ganzes 16:9-Bild mittig auf unscharfem Hintergrund, „voll“ = Clip ist schon 9:16 (bildfüllend skaliert).
--format hochkant = 1080×1920 (TikTok/Reels/Shorts). --schwarz-aus S = Bild und Ton in den letzten S Sekunden auf Schwarz/Stille. Das Logo erscheint im LETZTEN Clip (Schlussbild) nach --logo-ab-letzter Sekunden.
Der Originalton der Clips wird durch den Song ersetzt (weiche Ein-/Ausblendung).
"""
import argparse, os, subprocess, tempfile
from PIL import Image


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ausgabe")
    ap.add_argument("--logo", required=True); ap.add_argument("--song", required=True)
    ap.add_argument("--clip", action="append", required=True)
    ap.add_argument("--musik-ab", type=float, default=60.0)
    ap.add_argument("--logo-ab-letzter", type=float, default=0.35)
    ap.add_argument("--logo-breite", type=int, default=860)
    ap.add_argument("--logo-y", type=int, default=92, help="Mitte des Logos (px von oben, 720p)")
    ap.add_argument("--xfade", type=float, default=0.15, help="Überblendung in s; 0 = harter Schnitt")
    ap.add_argument("--musik-aus", type=float, default=0.8, help="Ausblenden der Musik am Ende (s); klein = Musik hört mit dem Bild auf")
    ap.add_argument("--format", choices=["quer", "hochkant"], default="quer")
    ap.add_argument("--schwarz-aus", type=float, default=0.0, help="Bild am Ende in S Sekunden auf Schwarz ausblenden")
    a = ap.parse_args()
    hoch = a.format == "hochkant"
    VW, VH = (1080, 1920) if hoch else (1280, 720)

    clips = []
    for c in a.clip:
        teile = c.split(":")
        aus = "0.5"
        if len(teile) == 4:
            aus = teile.pop()
        f, s, d = teile
        clips.append((f, float(s), float(d), aus))
    X = a.xfade
    D = sum(d for _, _, d, _ in clips) - X * (len(clips) - 1)

    lg = Image.open(a.logo).convert("RGBA"); lg = lg.crop(lg.getbbox())
    W = a.logo_breite; H = round(lg.height * W / lg.width)
    tmp = os.path.join(tempfile.mkdtemp(), "logo.png"); lg.resize((W, H), Image.LANCZOS).save(tmp)

    inputs, fc = [], []
    for i, (f, s, d, aus) in enumerate(clips):
        inputs += ["-i", f]
        anf = f"[{i}:v]trim=start={s}:duration={d},setpts=PTS-STARTPTS,scale=1280:720:flags=lanczos,setsar=1,fps=24"
        if hoch and aus == "voll":  # Clip ist schon 9:16 (eigenes Hochkant-Video) -> bildfüllend
            fc.append(f"[{i}:v]trim=start={s}:duration={d},setpts=PTS-STARTPTS,scale={VW}:{VH}:flags=lanczos,setsar=1,fps=24,format=yuv420p[c{i}]")
        elif not hoch:
            fc.append(f"{anf},format=yuv420p[c{i}]")
        elif aus == "box":  # ganzes Bild mittig, darüber/darunter dasselbe Bild vergrößert + unscharf
            fc.append(f"{anf},split[h{i}][v{i}];[h{i}]scale=-2:{VH},crop={VW}:{VH},boxblur=24:2,eq=brightness=-0.06[hb{i}];"
                      f"[v{i}]scale={VW}:-2:flags=lanczos[vb{i}];[hb{i}][vb{i}]overlay=0:(H-h)/2,setsar=1,format=yuv420p[c{i}]")
        else:  # 9:16-Ausschnitt um die angegebene Bildmitte
            cw = round(720 * 9 / 16)
            x = min(max(0, round(float(aus) * 1280 - cw / 2)), 1280 - cw)
            fc.append(f"{anf},crop={cw}:720:{x}:0,scale={VW}:{VH}:flags=lanczos,setsar=1,format=yuv420p[c{i}]")
    prev, off = "c0", 0.0
    if X > 0:
        for i in range(1, len(clips)):
            off += clips[i - 1][2] - X
            out = f"x{i}"
            fc.append(f"[{prev}][c{i}]xfade=transition=fade:duration={X}:offset={off:.3f}[{out}]")
            prev = out
    else:  # harte Schnitte
        off = sum(c[2] for c in clips[:-1])
        fc.append("".join(f"[c{i}]" for i in range(len(clips))) + f"concat=n={len(clips)}:v=1:a=0[xc]")
        prev = "xc"
    # letzte 2 Bilder ganz schwarz
    schwarz = f",fade=t=out:st={D-a.schwarz_aus:.3f}:d={a.schwarz_aus-2/24:.3f}" if a.schwarz_aus > 0 else ""
    t = off + a.logo_ab_letzter  # Start des letzten Clips + Verzögerung
    n = len(clips)
    s = (f"if(lt(t,{t}),0.01,if(lt(t,{t+0.25}),0.01+1.11*(t-{t})/0.25,if(lt(t,{t+0.40}),1.12-0.12*(t-{t+0.25})/0.15,1)))")
    fc.append(f"[{n}:v]format=rgba,scale=w='max(2,{W}*({s}))':h='max(2,{H}*({s}))':eval=frame[lg]")
    fc.append(f"[{prev}]format=yuva420p[bg];[bg][lg]overlay=x='(W-w)/2':y='max(6,{a.logo_y}-h/2)':eval=frame:enable='gte(t,{t})',format=yuv420p{schwarz}[v]")
    fc.append(f"[{n+1}:a]atrim=start={a.musik_ab}:duration={D},asetpts=PTS-STARTPTS,aresample=48000,"
              f"aformat=channel_layouts=stereo,afade=t=in:st=0:d=0.15,afade=t=out:st={D-a.musik_aus:.3f}:d={a.musik_aus}[a]")
    cmd = (["ffmpeg", "-v", "error", "-y"] + inputs +
           ["-loop", "1", "-framerate", "24", "-t", f"{D}", "-i", tmp, "-i", a.song,
            "-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[a]", "-t", f"{D}",
            "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", a.ausgabe])
    subprocess.run(cmd, check=True)
    print(f"Intro geschrieben: {a.ausgabe} ({D:.2f} s, Logo ab {t:.2f} s)")


if __name__ == "__main__":
    main()
