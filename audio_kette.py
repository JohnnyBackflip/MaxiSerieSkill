#!/usr/bin/env python3
"""Gemeinsame Audio-Ketten (User-Regel 2026-11-06): ALLE Sprach-, Effekt- und Musikspuren und jedes fertige Video
laufen durch Kompressor + Limiter, damit alles gleich laut ist. ffmpeg-Filterstrings.

  STIMME : Kompressor (Ratio 3, Schwelle -26 dB) -> Pegel auf Mittel -20 dB -> Limiter -1,5 dBFS
  EFFEKT : Kompressor (Ratio 2,5) -> Limiter
  MUSIK  : Kompressor (Ratio 2) -> Limiter (Pegel dann per volume=dB im Mix)
  MASTER : Kompressor (Ratio 2,2) -> Limiter -> loudnorm (-16 LUFS, Spitze -1,5 dB)
Nutzung: python3 video_pegeln.py <video.mp4> [<aus.mp4>]  (Master-Kette auf ein beliebiges Video, Bild bleibt unverändert)"""
KOMP_STIMME = "acompressor=threshold=-26dB:ratio=3:attack=4:release=90:makeup=2"
KOMP_EFFEKT = "acompressor=threshold=-24dB:ratio=2.5:attack=6:release=120:makeup=1"
KOMP_MUSIK = "acompressor=threshold=-26dB:ratio=2:attack=20:release=250:makeup=1"
LIMIT = "alimiter=limit=0.84:attack=3:release=60:level=false"
KOMP_MASTER = "acompressor=threshold=-20dB:ratio=2.2:attack=12:release=180:makeup=1"
LOUDNORM = "loudnorm=I=-16:TP=-1.5:LRA=9"
EFFEKT = f"{KOMP_EFFEKT},{LIMIT}"
MUSIK = f"{KOMP_MUSIK},{LIMIT}"
MASTER = f"{KOMP_MASTER},{LIMIT},{LOUDNORM}"
