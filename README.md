# Maxi Cartoons – Skill und Serien-Baukasten

Claude-Code-Skill **`maxi-folge-erstellen`** für die Kinderserie „Maxi Cartoons“ (Maxis Welt) plus alle Werkzeuge und Serien-Bestände, um auf einem beliebigen Rechner neue Folgen zu bauen: Geschichte (auch frei nach Buch-Vorlage) → Szenenplan → Figurenstimmen (Gemini-TTS) und Hör-Storyboard → Blender-Mockups → Flow-Bilder → Storyboard-Video → Veo-Szenenvideos → Sprachprüfung und Schnitt → Intro und Lyria-Musik → Thumbnail und TikTok/YouTube-Texte.

## Schnellstart
```
git clone https://github.com/JohnnyBackflip/MaxiSerieSkill.git ~/Maxis_Welt
mkdir -p ~/.claude/skills && ln -s ~/Maxis_Welt/skill/maxi-folge-erstellen ~/.claude/skills/
echo 'export MAXI_ROOT=~/Maxis_Welt' >> ~/.bashrc
cd ~/Maxis_Welt && claude      # z. B. „Mach eine neue Maxi-Folge über …“
```
Google-API-Keys für die Stimmen gehören nach `~/.config/maxi/google_api_keys.txt` (nie ins Repo).
Benötigte Programme (Python/Pillow, ffmpeg, Blender, Antigravity-CLI `agy`, faster-whisper, Claude in Chrome für Flow/Gemini): **[skill/maxi-folge-erstellen/references/einrichtung.md](skill/maxi-folge-erstellen/references/einrichtung.md)**.

## Aufbau
| Pfad | Inhalt |
|---|---|
| `skill/maxi-folge-erstellen/` | Der Skill (`SKILL.md`) + Referenzen: Werkzeuge/Befehle, Veo/Flow-Dialog-Regeln, Einrichtung |
| `*.py` (Root) | Werkzeuge: `agy_generate_image.py` (Flow-Bilder), `build_episode_video.py` (Storyboard-Video), `stimmen_tts.py` + `stimmen_pruefen.py` (Figurenstimmen mit Gemini-TTS, Prüfung), `hoerstoryboard_bauen.py` (Storyboard mit Stimmen), `sprache_abschreiben.py` + `flow_clips_schneiden.py` (Sprachprüfung/Schnitt), `musik_unterlegen.py`, `intro_bauen_v2.py`, `thumbnail_bauen.py`, `maxi_blender_lib.py` (Blender-Figuren/Props) |
| `00_WIKI/` | Inhaltsverzeichnis der Serie: Figuren, Orte/Kameras, Objekte, Folgen/Szenen, Musik/Intro |
| `10_Charakterbibel_v2_Mehr_Wuerze/` | Charakterbibel v2.1 (Standard für neue Geschichten) |
| `02_Charaktere_Steckbriefe_und_Bilder/` | Modelsheets aller Figuren |
| `03_Blender_3D_Haus_Blockout/` | Haus-Blockout mit allen Kameras (`KOM_CAM_xx`, `FLUR_CAM_xx`) |
| `04_Komitee_Kameraplan_und_Flow_Raumszenen/` | Raumreferenzen `REF_xx` + leere Flow-Raumszenen `FLOW_CAM_xx` |
| `11_Flur_Neu_Treppe_Blender_und_Flow/` | Neuer Flur (Raumszenen + Job-Skript) |
| `00_Intro_Maxi_Cartoons/` | Logo, Intro quer (1280×720) und hochkant (1080×1920) |
| `00_Musik_Serie/` | Hintergrundmusik aus Gemini Lyria |
| `12_Folge_Tante_Frieda/` | Folge frei nach Ludwig Thoma (gemeinfrei): Drehbuch mit Tabelle Original → heute, `szenenplan_r1.json`, Stimmen + Besetzung, Modelsheets Frieda/Lorchen, OBJ-Sheets, Job-Skripte |
| `09_Folge_02_Pilze_im_Herbstwald/` | Musterfolge: Drehbuch, Vermerk, Objekt-Sheets, Herbstwald-Blockout + Raumszenen, Job-/Mockup-Skripte, Flow-Prompts, Untertitel, Thumbnails, `social_media.md` |

Nicht enthalten: fertige Folgenvideos, Szenenbilder/Clips, verworfene Fassungen, Blender-Screenshots (aus den `.blend` neu renderbar) und der Intro-Song (Herkunft ungeklärt).

Alle Pfade im Skill sind relativ zum Repo-Ordner. Die Skripte finden ihn über `MAXI_ROOT` oder ihren eigenen Speicherort.
