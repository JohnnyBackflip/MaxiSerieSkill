# Musik und Intro

## Serien-Intro „Maxi Cartoons“
Ordner `../00_Intro_Maxi_Cartoons/`, Vermerk `00_VERMERK_Intro.md`.

| Datei | Format | Länge | Verwendung |
|---|---|---|---|
| `Maxi_Cartoons_Intro.mp4` | quer 1280×720 | 4,54 s | **aktuell** für alle Folgen im Querformat (Bild v3, Ton v2, Schwarzblende am Ende) |
| `Maxi_Cartoons_Intro_Hochkant.mp4` | hochkant 1080×1920 | 4,54 s | **aktuell** für alle Folgen im Hochkantformat (TikTok); Schlussbild eigenes 9:16-Flow-Video `v2/hochkant/` |
| `v2/hochkant/Maxi_Cartoons_Intro_Hochkant_v1_box.mp4` | hochkant | 4,54 s | verworfen: Schlussbild als Querformat auf unscharfem Hintergrund |
| `v2/Maxi_Cartoons_Intro_v3.mp4` | quer | 4,54 s | Bild-Quelle (Ton neu auf den Schlag gelegt, verworfen) |
| `v2/Maxi_Cartoons_Intro_v2.mp4`, `…_v2_7s.mp4` | quer | 7,2 s | alte, langsame Fassung, Ton-Quelle |
| `alt_v1/` | quer | 6 s | erste Fassung |

- **Ablauf:** Maxi 0,8 s → Mama 0,8 s → Papa 0,8 s → alle eng zusammen winkend (2,12 s). Das Logo ploppt im Schlussbild auf. Das Intro endet in Maxis Sprung.
- **Schluss:** Bild und Ton blenden in den letzten 0,3 s auf Schwarz/Stille aus (`--schwarz-aus 0.3 --musik-aus 0.3`).
- **Hochkant:** Nahaufnahmen als 9:16-Ausschnitt der Quer-Clips; Schlussbild `v2/hochkant/INTRO3_ALLE_HOCH.jpg` (Flow, Nano Banana 2.1, 9:16) → Video `v2/hochkant/flow_videos/INTRO3_ALLE_HOCH_flow.mp4` (Veo 3.1 Fast, 4 s, 1080p), Clip-Modus `voll`. Nie ein Querbild ins Hochformat quetschen oder auf Unschärfe-Hintergrund setzen.
- **Logo:** `Maxi_Cartoons_Logo.png` (3D-Bonbonschrift aus Flow, freigestellt).
- **Song:** `../Saturday_Morning_Adventure.mp3`, ab 1:00.
- **Regel:** Das Intro hat **immer das Format der Folge**. Danach kommt in der Flow-Fassung keine Titelkarte; die erste Einstellung wird 1 s aus Schwarz eingeblendet. Eine Titelkarte gibt es nur im Storyboard-Video.

## Hintergrundmusik (Gemini Lyria im Browser)
Die Tracks entstehen auf gemini.google.com → Plus → „Musik erstellen“ (Lyria), instrumental, Länge Standard (ca. 3 min). Download über „Nur Audio (MP3-Track)“. Ordner `../00_Musik_Serie/`, Vermerk `00_VERMERK_Musik.md`.

| Datei | Länge | Stimmung / Zweck | Besonderheit | Verwendet in |
|---|---|---|---|---|
| `Musik_01_Herbstwald_Leaves_and_Tiny_Treasures.mp3` | 179 s | fröhlich, Wald, Spaziergang, Pilzsuche (Glockenspiel, Ukulele, Pizzicato, Flöte, Holzblock) | ca. 1,2 s Stille am Anfang → `ab=1.0` | F02 v005/v006: Folgenanfang (4,54–13,5 s, `ab=1.0`) + SH060–SH150 (32,4–78,1 s) |
| `Musik_02_Kueche_Abend_Shared_Plates_and_Smiles.mp3` | ca. 3 min | gemütlich, Abend, Kochen, Essen (Akustikgitarre, Klavier, Glockenspiel, Streicher) | – | F02 v005/v006: SH190–SH220 (89,9–108,1 s) |
| `Musik_03_Heimlich_Before_the_Floorboards_Creak.mp3` | 172,8 s | heimlich/schleichend, Pizzicato, Holzbläser-Staccato, leiser Bass, spitzbübisch (2026-11-06, Gemini Lyria) | beginnt ohne Stille, `ab=0` | FTF Mockup-Vorschau v002: SH080–SH081 (ab 0 s) und SH124–SH130 (ab 40 s), −11 dB |
| `../Saturday_Morning_Adventure.mp3` | – | Intro-Song | – | Intro |

Unterlegen mit `../musik_unterlegen.py`: je Szenenblock ein Cue, ca. −9 dB, `--ducking`, `--fade 1.5`.
Neue Tracks bitte hier und im Musik-Vermerk eintragen, jeweils mit Prompt.


## Soundeffekte (ElevenLabs, nur Effekte)
Katalog `../12_Folge_Tante_Frieda/04_Video/01_Ton/sfx_katalog.json`, Dateien in `…/01_Ton/sfx/`, Cues in `ton_r2.json`. Erzeugt mit `../sfx_elevenlabs.py` (Key `~/.elevenlabs_key`, nicht im Repo). Musik gehört **nicht** zu ElevenLabs, sondern zu Gemini Lyria.
