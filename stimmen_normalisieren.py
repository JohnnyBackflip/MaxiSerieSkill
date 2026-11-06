#!/usr/bin/env python3
"""Stimmen auf gleichen Pegel bringen (Gemini-TTS liefert teils sehr leise Clips, loudnorm greift bei kurzen Clips nicht).
Ziel: mittlerer Pegel -20 dB, Spitze höchstens -1,5 dB (Limiter). Originale: <ordner>/vor_Normalisierung/.
  python3 stimmen_normalisieren.py <stimmen_ordner> [--ziel -20]"""
import os, re, shutil, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from audio_kette import KOMP_STIMME, LIMIT
ordner = sys.argv[1]; ziel = float(sys.argv[sys.argv.index("--ziel") + 1]) if "--ziel" in sys.argv else -20.0
bak = os.path.join(ordner, "vor_Normalisierung"); os.makedirs(bak, exist_ok=True)
for f in sorted(os.listdir(ordner)):
    if not (f.startswith("SH") and f.endswith(".wav")): continue
    p = os.path.join(ordner, f)
    if not os.path.exists(os.path.join(bak, f)): shutil.copy(p, os.path.join(bak, f))
    q = os.path.join(bak, f)                                   # immer vom Original ausgehen (idempotent)
    o = subprocess.run(["ffmpeg", "-v", "info", "-i", q, "-af", "volumedetect", "-f", "null", "-"], capture_output=True, text=True).stderr
    mean = float(re.search(r"mean_volume: (-?[\d.]+)", o).group(1))
    # 1. Kompressor, 2. Pegel auf das Ziel (aus dem komprimierten Mittel), 3. Limiter
    gain = max(-6.0, min(32.0, ziel - (mean + 1.5)))
    tmp = p + ".tmp.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", q, "-af", f"{KOMP_STIMME},volume={gain:.1f}dB,{LIMIT}", "-ar", "24000", "-ac", "1", tmp], check=True)
    o2 = subprocess.run(["ffmpeg", "-v", "info", "-i", tmp, "-af", "volumedetect", "-f", "null", "-"], capture_output=True, text=True).stderr
    m2 = float(re.search(r"mean_volume: (-?[\d.]+)", o2).group(1))
    fine = max(-6.0, min(8.0, ziel - m2))                      # Feinabgleich auf das Ziel, danach nochmals Limiter
    if abs(fine) > 0.8:
        tmp2 = p + ".tmp2.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-af", f"volume={fine:.1f}dB,{LIMIT}", "-ar", "24000", "-ac", "1", tmp2], check=True)
        os.replace(tmp2, tmp)
    os.replace(tmp, p); print(f"{f}: {mean:.1f} dB -> {ziel:.0f} dB (Kompressor + Limiter)")
