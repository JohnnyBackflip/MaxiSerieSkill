#!/usr/bin/env python3
"""Treiber: erzeugt Flow-Start- (A) und Endbilder (B) für alle Einstellungen, sobald ihre Mockups fertig sind.
Läuft, bis alles da ist (oder das Mockup-Rendern beendet ist und nichts mehr fehlt). Aufruf (im Hintergrund): python3 flow_treiber.py"""
import json, os, subprocess, sys, time
E = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(E)
plan = [x["id"] for x in json.load(open(f"{E}/szenenplan_r5.json"))]
OUT, MOCK = f"{E}/03_Szenen_Flow_Bilder", f"{E}/02_Szenen_Blender_Mockups"
os.makedirs(OUT, exist_ok=True)
B_MOCK = {"SH041": "SH041_B", "SH082": "SH082_B"}
START = float(os.environ.get("MOCK_START", "0"))   # Epoche: nur Mockups, die nach dem Render-Start entstanden sind
def fertig(p): return os.path.exists(p) and os.path.getmtime(p) > START and time.time() - os.path.getmtime(p) > 25
def ok(p): return os.path.exists(p) and os.path.getsize(p) > 20000
def render_laeuft():
    return subprocess.run("ps -eo args | grep -q '[b]uild_frieda_szenen.py'", shell=True).returncode == 0
def kontingent_leer():
    """Bei erschöpftem Kontingent (HTTP 429 RESOURCE_EXHAUSTED) sofort abbrechen, nicht weiter anfragen."""
    try:
        t = open(f"{E}/jobs_flow.log").read()[-6000:]
    except OSError:
        return False
    return t.count("RESOURCE_EXHAUSTED") >= 3


def lauf(mode, ids):
    subprocess.run([sys.executable, f"{E}/make_jobs_flow.py", mode] + ids, check=True)
    fn = f"{E}/jobs_flow_{mode}.json" if len(ids) >= 6 else f"{E}/jobs_flow_{mode}_{'_'.join(sorted(ids))}.json"
    with open(f"{E}/jobs_flow.log", "a") as lg:
        subprocess.run([sys.executable, f"{ROOT}/agy_generate_image.py", "batch", fn, "--parallel", "3"], stdout=lg, stderr=lg)
while True:
    if kontingent_leer():
        print("ABBRUCH: Kontingent der Bildgenerierung erschöpft (429 RESOURCE_EXHAUSTED) – siehe jobs_flow.log"); break
    a = [i for i in plan if fertig(f"{MOCK}/{i}_blender.png") and not ok(f"{OUT}/{i}A.jpg")]
    if a:
        lauf("A", a[:9]); continue
    b = [i for i in plan if ok(f"{OUT}/{i}A.jpg") and not ok(f"{OUT}/{i}B.jpg") and fertig(f"{MOCK}/{B_MOCK.get(i, i)}_blender.png")]
    if b:
        lauf("B", b[:9]); continue
    offen = [i for i in plan if not (ok(f"{OUT}/{i}A.jpg") and ok(f"{OUT}/{i}B.jpg"))]
    if not offen: print("ALLES FERTIG"); break
    if not render_laeuft():
        print("Render beendet, offen:", offen); break
    time.sleep(30)
