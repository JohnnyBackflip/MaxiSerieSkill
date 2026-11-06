#!/usr/bin/env python3
"""Master-Kette (Kompressor + Limiter + loudnorm) auf den Ton eines beliebigen Videos. Bild wird nur kopiert.
  python3 video_pegeln.py <video.mp4> [<aus.mp4>]   (ohne 2. Argument: <video>_gepegelt.mp4)"""
import os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from audio_kette import MASTER
src = sys.argv[1]; dst = sys.argv[2] if len(sys.argv) > 2 else os.path.splitext(src)[0] + "_gepegelt.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-c:v", "copy", "-af", MASTER, "-c:a", "aac", "-b:a", "192k", dst], check=True)
print("gepegelt:", dst)
