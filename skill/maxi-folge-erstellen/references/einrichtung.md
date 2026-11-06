# Einrichtung auf einem neuen Rechner

Repo: https://github.com/JohnnyBackflip/MaxiSerieSkill (öffentlich). Getestet unter Ubuntu 22.04.

## 1. Repo holen und Skill einhängen
```
git clone https://github.com/JohnnyBackflip/MaxiSerieSkill.git ~/Maxis_Welt
mkdir -p ~/.claude/skills
ln -s ~/Maxis_Welt/skill/maxi-folge-erstellen ~/.claude/skills/maxi-folge-erstellen
export MAXI_ROOT=~/Maxis_Welt        # in ~/.bashrc eintragen
```
Der Repo-Ordner IST der Projektordner (Root). Claude Code dort starten (`cd ~/Maxis_Welt && claude`).

## 2. Programme (Versionen, mit denen es lief)
| Programm | Version | Wofür | Installation |
|---|---|---|---|
| Python 3 + Pillow | 3.10 / Pillow 10 | alle Skripte | `sudo apt install python3-pil` oder `pip install pillow` |
| ffmpeg | 4.4 | Video, Ton, Musik, Intro | `sudo apt install ffmpeg` |
| Blender | 5.2 LTS | Blockouts, Mockups (`maxi_blender_lib.py`) | blender.org, `blender` muss im PATH liegen |
| Antigravity-CLI `agy` | 1.5 | Bildgenerierung (`agy_generate_image.py`, Google-Bildmodell, Referenzbilder) | Google Antigravity installieren, einmal anmelden, `agy` im PATH |
| faster-whisper | 1.2.1 (Modell large-v3-turbo) | Sprachprüfung und Schnitt | siehe 3 |
| Schriften | DejaVu Sans, Cantarell ExtraBold | Storyboard-Video, Thumbnail | `sudo apt install fonts-dejavu fonts-cantarell` |
| Claude in Chrome | – | Flow (Veo-Videos), Gemini (Lyria-Musik) im Browser | Chrome-Erweiterung, bei flow.google.com und gemini.google.com angemeldet |

## 3. Sprachwerkzeug (venv im Root)
```
cd $MAXI_ROOT
python3 -m venv .venv_sprache
.venv_sprache/bin/pip install faster-whisper==1.2.1 numpy
```
Das Whisper-Modell (~1,6 GB) lädt beim ersten Aufruf von `sprache_abschreiben.py`.

## 4. Prüfbefehl
```
cd $MAXI_ROOT
python3 thumbnail_bauen.py 09_Folge_02_Pilze_im_Herbstwald/05_Thumbnail/Thumbnail_Hintergrund_16x9.jpg /tmp/test.jpg --zeile "TEST" --folge "FOLGE 0"
ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 00_Intro_Maxi_Cartoons/Maxi_Cartoons_Intro.mp4   # 1280,720
agy --version && blender --version | head -1
```

## 5. Was im Repo ist – und was nicht
- Drin: Skill, Werkzeuge, Wiki, Charakterbibel v2.1, Modelsheets, Objekt-Sheets, Raumreferenzen `REF_xx`, leere Flow-Raumszenen `FLOW_CAM_xx`, Blender-Blockouts (Haus, Herbstwald + Tunnel), Logo, Intro (quer + hochkant), Lyria-Musik, Folge 02 als Musterbeispiel (Drehbuch, Vermerk, Job-/Mockup-Skripte, Flow-Prompts, Thumbnails, `social_media.md`).
- Nicht drin: fertige Folgenvideos, Szenenbilder und Flow-Clips, `rejected/`, `*.bak`, Blender-Kamera-Screenshots (aus den `.blend` neu rendern), der Intro-Song `Saturday_Morning_Adventure.mp3` (Herkunft ungeklärt; das fertige Intro reicht für neue Folgen). Wer das Intro neu bauen will, braucht den Song separat.
- Große Ergebnisse neuer Folgen (mp4, Flow-Bilder) nicht ins Repo committen – `.gitignore` schließt sie aus.

## Google-API-Keys für Stimmen (Gemini-TTS)
`mkdir -p ~/.config/maxi && nano ~/.config/maxi/google_api_keys.txt && chmod 600 ~/.config/maxi/google_api_keys.txt` – eine Key-Zeile (`AIza…`) je Zeile; Free-Tier-Keys reichen (werden reihum genutzt). Die Datei liegt bewusst außerhalb des Repos. Test: `python3 stimmen_tts.py` mit `--nur` auf eine Zeile.
