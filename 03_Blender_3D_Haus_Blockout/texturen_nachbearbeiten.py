#!/usr/bin/env python3
"""Flow-Rohbilder (Texturen/roh/*.jpg, 1376x768) -> nahtlose, quadratische 1024er Kacheln (Texturen/<id>.jpg).
Nahtlos per Versatz-Überblendung (Bild ⟷ um die halbe Kantenlänge verschobenes Bild, weiche Maske).
'fit'-Texturen (Türen) werden nur zugeschnitten (Hochformat 0.45:1, Mitte), nicht kachelnd gemacht.
  python3 texturen_nachbearbeiten.py [id1 id2 ...]"""
import os, sys
import numpy as np
from PIL import Image
from texturen_katalog import T, E

FIT_CROP = {"door_front": (505, 70, 868, 706)}   # Türblatt von Hand (Flow malte Tür mit Seitenteilen)

def seamless(im, band=0.30):
    a = np.asarray(im.convert("RGB"), dtype=np.float32); h, w, _ = a.shape
    s = np.roll(np.roll(a, h // 2, axis=0), w // 2, axis=1)
    def ramp(n):
        x = np.minimum(np.arange(n), n - 1 - np.arange(n)) / (n * band)   # 0 am Rand -> 1 ab 'band'
        x = np.clip(x, 0, 1); return x * x * (3 - 2 * x)
    m = np.outer(ramp(h), ramp(w))[..., None]
    out = a * m + s * (1 - m)
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))

def main():
    ids = sys.argv[1:] or list(T)
    for k in ids:
        src = f"{E}/Texturen/roh/{k}.jpg"
        if not os.path.exists(src):
            print(k, "fehlt"); continue
        im = Image.open(src).convert("RGB"); w, h = im.size
        mode = T[k][2]
        if mode == "fit":   # Tür: Hochformat aus der Mitte
            if k in FIT_CROP:
                out = im.crop(FIT_CROP[k]).resize((512, 1024), Image.LANCZOS); out.save(f"{E}/Texturen/{k}.jpg", quality=92); print(k, out.size); continue
            arr = np.asarray(im, dtype=np.float32)
            bg = np.median(np.concatenate([arr[:, :20].reshape(-1, 3), arr[:, -20:].reshape(-1, 3)]), axis=0)
            diff = np.abs(arr - bg).sum(axis=2) > 36
            ys, xs = np.where(diff)
            if len(xs) > 1000:
                x0, x1, y0, y1 = xs.min() + 4, xs.max() - 4, ys.min() + 4, ys.max() - 4     # Rand ohne Hintergrund
            else:
                cw = int(h * 0.46); x0 = (w - cw) // 2; x1 = x0 + cw; y0, y1 = 0, h
            out = im.crop((x0, y0, x1, y1)).resize((512, 1024), Image.LANCZOS)
        else:
            c = im.crop(((w - h) // 2, 0, (w - h) // 2 + h, h))
            out = seamless(c).resize((1024, 1024), Image.LANCZOS)
        out.save(f"{E}/Texturen/{k}.jpg", quality=92)
        print(k, out.size)
if __name__ == "__main__":
    main()
