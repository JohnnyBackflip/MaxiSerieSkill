#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Wrapper für die Bildgenerierung mit der Antigravity-CLI `agy` (nicht-interaktiv).

agy ruft intern den Subagenten `image-generator` (Werkzeug `generate_image`) auf und
übernimmt die angegebenen Referenzbilder als Bildeingabe (`ImagePaths`). Verifiziert am
2026-11-03 (Host-Test): Ausgabe 1376×768 JPG, Referenzen wurden übergeben.

Einzelbild:
    python3 agy_generate_image.py one --out <datei.jpg> --prompt "<Motiv ...>" \
        --ref <CHAR_01.jpg> --ref <REF_03.jpg> [--ref ...] [--no-style-preamble]

Batch (mehrere Jobs, optional parallel):
    python3 agy_generate_image.py batch <jobs.json> [--parallel 2] [--force]

jobs.json:
{
  "default_refs": ["<pfad>", ...],            # optional, wird jedem Job vorangestellt
  "jobs": [
    {"id": "OBJ_01", "out": "<abs. pfad.jpg>", "prompt": "<Motiv>", "refs": ["<pfad>", ...],
     "style": "scene" | "object" | "none"}
  ]
}

Zu jedem Bild wird <out>.prompt.txt mit dem vollständigen Prompt und den Referenzen
geschrieben (Nachvollziehbarkeit für das Storyboard-PDF).
"""

import argparse
import json
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

KORREKTURMAPPE = os.environ.get("MAXI_ROOT", os.path.dirname(os.path.abspath(__file__)))

STYLE_SCENE = (
    "STIL (verbindlich): Hochwertiger 3D-Pixar-CGI-Look wie ein gerenderter Animationsfilm, "
    "weiche globale Beleuchtung, warme Farben, saubere runde Formen, KEINE schwarzen Outlines, "
    "keine 2D-Comic-Umrandungen, keine Texte/Schriften/Logos im Bild, Querformat 16:9 (1376×768). "
    "Figuren, Hautfarbe, Haarfarbe, Augenfarbe, Proportionen und Kleidung EXAKT wie auf den "
    "Charakter-Referenzbildern; Raum, Wandfarben, Boden und Möbel EXAKT wie auf den Raum-Referenzbildern; "
    "Objekte in Farbe/Form EXAKT wie auf den Objekt-Referenzbildern. "
)

STYLE_OBJECT = (
    "STIL (verbindlich): Freigestelltes 3D-Studio-Modelsheet eines einzelnen Objekts im Pixar-CGI-Look "
    "auf neutralem, hellem Studio-Hintergrund (warmes Hellgrau/Creme), weiches Studiolicht, "
    "zwei Ansichten nebeneinander (Dreiviertel-Ansicht links, zweite Ansicht rechts), keine Personen, "
    "keine schwarzen Outlines, keine Texte/Schriften im Bild, Querformat 16:9 (1376×768). "
)

STYLES = {"scene": STYLE_SCENE, "object": STYLE_OBJECT, "none": ""}


def build_prompt(motif, refs, style):
    parts = []
    if STYLES.get(style):
        parts.append(STYLES[style])
    if refs:
        parts.append("REFERENZBILDER (als Bildeingabe übergeben, exakt einhalten):")
        for r in refs:
            parts.append(f"- {r}")
    parts.append("MOTIV: " + motif.strip())
    return "\n".join(parts)


def run_agy(out_path, full_prompt, refs, timeout_s):
    out_dir = os.path.dirname(os.path.abspath(out_path))
    os.makedirs(out_dir, exist_ok=True)
    add_dirs = {out_dir, KORREKTURMAPPE}
    for r in refs:
        add_dirs.add(os.path.dirname(os.path.abspath(r)))
    instruction = (
        full_prompt
        + f"\n\nAUFGABE: Erzeuge genau EIN Bild mit deinem Bildgenerierungs-Werkzeug und übergib "
        f"dabei ALLE oben gelisteten Referenzbilder als Bildeingabe. Speichere das fertige Bild als JPG "
        f"unter exakt diesem Pfad: {os.path.abspath(out_path)} . "
        f"Antworte am Ende nur mit dem absoluten Pfad der gespeicherten Datei."
    )
    cmd = ["agy"]
    for d in sorted(add_dirs):
        cmd += ["--add-dir", d]
    cmd += ["--print-timeout", f"{timeout_s}s", f"--print={instruction}"]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout_s + 60,
                             cwd=out_dir)
        return res.returncode, (res.stdout or "") + (res.stderr or "")
    except subprocess.TimeoutExpired:
        return 124, "TIMEOUT"


def valid_image(path, min_w=800):
    try:
        from PIL import Image
        with Image.open(path) as im:
            im.verify()
        with Image.open(path) as im:
            return max(im.width, im.height) >= min_w
    except Exception:
        return False


def generate(out_path, motif, refs, style="scene", timeout_s=600, retries=2, force=False,
             log=print):
    refs = [os.path.abspath(r) for r in refs]
    missing = [r for r in refs if not os.path.isfile(r)]
    if missing:
        raise FileNotFoundError("Referenzbild fehlt: " + ", ".join(missing))
    out_path = os.path.abspath(out_path)
    full_prompt = build_prompt(motif, refs, style)
    with open(out_path + ".prompt.txt", "w", encoding="utf-8") as fh:
        fh.write(full_prompt + "\n")
    if os.path.isfile(out_path) and valid_image(out_path) and not force:
        log(f"[skip] existiert bereits: {out_path}")
        return True
    if force and os.path.isfile(out_path):
        # Altes Bild vor der Regeneration entfernen, sonst wuerde ein liegengebliebenes
        # Bild nach einem fehlgeschlagenen agy-Aufruf faelschlich als [ok] gemeldet.
        # (Abgelehnte Fassungen gehoeren vorher nach rejected/, siehe schedule.md 5.3.)
        os.remove(out_path)
        log(f"[force] altes Bild entfernt: {out_path}")
    for attempt in range(1, retries + 2):
        t0 = time.time()
        rc, out = run_agy(out_path, full_prompt, refs, timeout_s)
        dt = time.time() - t0
        if os.path.isfile(out_path) and valid_image(out_path):
            log(f"[ok] {os.path.basename(out_path)} ({dt:.0f}s, Versuch {attempt})")
            return True
        log(f"[fail] {os.path.basename(out_path)} Versuch {attempt} rc={rc} ({dt:.0f}s): "
            + out.strip()[-300:].replace("\n", " | "))
    return False


def cmd_one(a):
    motif = a.prompt
    if a.prompt_file:
        with open(a.prompt_file, encoding="utf-8") as fh:
            motif = fh.read()
    if not motif:
        sys.exit("Prompt fehlt (--prompt oder --prompt-file).")
    ok = generate(a.out, motif, a.ref or [], style=("none" if a.no_style_preamble else a.style),
                  timeout_s=a.timeout, retries=a.retries, force=a.force)
    sys.exit(0 if ok else 1)


def cmd_batch(a):
    with open(a.jobs, encoding="utf-8") as fh:
        spec = json.load(fh)
    default_refs = spec.get("default_refs", [])
    jobs = spec["jobs"]
    results = {}

    def work(job):
        refs = list(default_refs) + list(job.get("refs", []))
        try:
            ok = generate(job["out"], job["prompt"], refs, style=job.get("style", "scene"),
                          timeout_s=a.timeout, retries=a.retries, force=a.force,
                          log=lambda s: print(f"{job.get('id','?')}: {s}", flush=True))
        except Exception as e:  # noqa: BLE001
            print(f"{job.get('id','?')}: [error] {e}", flush=True)
            ok = False
        return job.get("id", job["out"]), ok

    with ThreadPoolExecutor(max_workers=max(1, a.parallel)) as ex:
        futs = [ex.submit(work, j) for j in jobs]
        for f in as_completed(futs):
            jid, ok = f.result()
            results[jid] = ok
    failed = [k for k, v in results.items() if not v]
    print(f"\nFertig: {len(results) - len(failed)}/{len(results)} ok.")
    if failed:
        print("FEHLGESCHLAGEN: " + ", ".join(sorted(failed)))
        sys.exit(1)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p1 = sub.add_parser("one")
    p1.add_argument("--out", required=True)
    p1.add_argument("--prompt")
    p1.add_argument("--prompt-file")
    p1.add_argument("--ref", action="append")
    p1.add_argument("--style", choices=list(STYLES), default="scene")
    p1.add_argument("--no-style-preamble", action="store_true")
    p1.add_argument("--timeout", type=int, default=600)
    p1.add_argument("--retries", type=int, default=2)
    p1.add_argument("--force", action="store_true")
    p1.set_defaults(func=cmd_one)
    p2 = sub.add_parser("batch")
    p2.add_argument("jobs")
    p2.add_argument("--parallel", type=int, default=2)
    p2.add_argument("--timeout", type=int, default=600)
    p2.add_argument("--retries", type=int, default=2)
    p2.add_argument("--force", action="store_true")
    p2.set_defaults(func=cmd_batch)
    a = ap.parse_args()
    a.func(a)


if __name__ == "__main__":
    main()
