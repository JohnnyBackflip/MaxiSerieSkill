#!/usr/bin/env python3
"""Neueste Flow-Datei aus ~/Downloads (jünger als N s) als 03_Szenen_Flow_Bilder/<ID>.jpg ablegen, schwarze Ränder abschneiden.
  python3 flow_holen.py SH058A [--max-alter 120]"""
import glob, os, shutil, subprocess, sys, time
E = os.path.dirname(os.path.abspath(__file__)); OUT = f"{E}/03_Szenen_Flow_Bilder"
sid = sys.argv[1]; alter = float(sys.argv[sys.argv.index("--max-alter") + 1]) if "--max-alter" in sys.argv else 180
LOG0 = f"{OUT}/.flow_downloads.log"
for _ in range(40):
    f = sorted(glob.glob(os.path.expanduser("~/Downloads/*.jpg")) + glob.glob(os.path.expanduser("~/Downloads/*.png")), key=os.path.getmtime)
    if f and os.path.exists(LOG0) and os.path.basename(f[-1]) not in open(LOG0).read().split("\n"): break
    time.sleep(0.5)
f = sorted(glob.glob(os.path.expanduser("~/Downloads/*.jpg")) + glob.glob(os.path.expanduser("~/Downloads/*.png")), key=os.path.getmtime)
if not f or time.time() - os.path.getmtime(f[-1]) > alter: sys.exit("keine frische Datei in ~/Downloads")
LOG = f"{OUT}/.flow_downloads.log"
benutzt = set(open(LOG).read().split("\n")) if os.path.exists(LOG) else set()
if os.path.basename(f[-1]) in benutzt: sys.exit("neueste Datei schon verwendet: " + os.path.basename(f[-1]))
ziel = f"{OUT}/{sid}.jpg"
if os.path.exists(ziel):
    os.makedirs(f"{OUT}/rejected", exist_ok=True); shutil.move(ziel, f"{OUT}/rejected/{sid}_{int(time.time())}.jpg")
subprocess.run(["convert", f[-1], "-bordercolor", "black", "-border", "1", "-fuzz", "6%", "-trim", "+repage", "-resize", "1376x768!", "-quality", "93", ziel], check=True)
pr = subprocess.run([sys.executable, f"{E}/flow_chrome_prompts.py", sid[-1], sid[:-1]], capture_output=True, text=True).stdout
open(ziel + ".prompt.txt", "w").write(f"Flow (Chrome) aus {os.path.basename(f[-1])}\n{pr}")
open(LOG, "a").write(os.path.basename(f[-1]) + "\n")
print(sid, "<-", os.path.basename(f[-1]))
