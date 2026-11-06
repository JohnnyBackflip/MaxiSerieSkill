# Werkzeuge und Befehle (Root = Projektordner bzw. Repo-Klon, siehe `einrichtung.md`)

## Bestand, der wiederverwendet wird
- Haus-Blockout: `03_Blender_3D_Haus_Blockout/Maxis_Haus_Komplett_Blockout.blend`, Kameras `KOM_CAM_01…38`, Flur `FLUR_CAM_01–05` (`11_Flur_Neu_Treppe_Blender_und_Flow/`).
- Raumreferenzen `REF_01…12`, Blender-Screenshots und leere Flow-Raumszenen `FLOW_CAM_xx.jpg`: `04_Komitee_Kameraplan_und_Flow_Raumszenen/` (01_Master_Referenzbilder_Raeume, 03_Blender_Kamera_Screenshots, 04_Flow_Gemalte_Raumszenen). Übersichts-PDF neu bauen: `python3 build_flow_raumszenen_pdf.py`.
- Herbstwald + Tunnel: `09_Folge_02_Pilze_im_Herbstwald/01_Neue_Orte_Blender_und_Flow/Herbstwald_Blockout.blend` (`WALD_CAM_01…07`, `TUNNEL_CAM_01…04`).
- Modelsheets: `02_Charaktere_Steckbriefe_und_Bilder/` (CHAR 01–12), Charakterbibel `10_Charakterbibel_v2_Mehr_Wuerze/`.
- Blender-Bibliothek: `maxi_blender_lib.py` (Figuren mit Posen, Auto, BMX, Welt/Sonne, Eevee+Freestyle, Kameras).

## Bilder in Flow – `agy_generate_image.py`
```
python3 agy_generate_image.py one --out <bild.jpg> --prompt "<Motiv>" --ref <mockup.png> --ref <CHAR.jpg> ...
python3 agy_generate_image.py batch <jobs.json> [--parallel 2] [--force]
```
jobs.json: `{"default_refs": [...], "jobs": [{"id", "out", "prompt", "refs": [...], "style": "scene"|"object"|"none"}]}`; schreibt `<bild>.prompt.txt`. Jobs mit `make_jobs_NN_*.py` erzeugen, Log mitschreiben. Warteschleifen auf laufende Jobs ohne Selbst-Treffer bei `pgrep`.

## Blender
```
blender -b <Basis.blend> --python <build_folgeNN_szenen_AB.py> -- haus|wald SH010 SH020 ...
```
Nur betroffene Kameras rendern (z. B. `RENDER_ONLY=TUNNEL_CAM`). Vor Flow-Lauf: nicht zwei Blender-Instanzen gleichzeitig mit Flow-Batch (Speicher).

## Storyboard-Video – `build_episode_video.py`
```
python3 build_episode_video.py <manifest.json> <ausgabe.mp4>
```
Manifest: `title`, `subtitle` (Titelkarte – nur hier!), `width`/`height`, `intro` (Pfad zum Intro im passenden Format), `scenes[].frames[]` mit `image`, `seconds`, `speaker`, `text`. Erzeugt `<ausgabe>_Bildliste.md` (Bild NN → Startzeit → Szene → Datei).

## Stimmen (Gemini-TTS) und Hör-Storyboard
Keys: `~/.config/maxi/google_api_keys.txt` (eine je Zeile, chmod 600, nie ins Repo). Modell `gemini-2.5-flash-preview-tts` (änderbar per `TTS_MODEL`).
```
python3 stimmen_tts.py <NN_Folge>/szenenplan_rN.json <NN_Folge>/04_Video/00_Stimmen_TTS/besetzung.json <NN_Folge>/04_Video/00_Stimmen_TTS [--nur SH010,SH020] [--force]
.venv_sprache/bin/python stimmen_pruefen.py <szenenplan.json> <stimmen_ordner> [--nur …] [--grenze 0.8]
python3 hoerstoryboard_bauen.py <szenenplan.json> <stimmen_ordner> <ausgabe.mp4> --titel "<Titel>" [--bilder <03_Szenen_Flow_Bilder>] [--intro <intro.mp4>]
```
besetzung.json: `{"Maxi": {"voice": "Puck", "halbtoene": 4, "tempo": 1.0, "stil": "Sprich auf Deutsch wie ein aufgeweckter fünfjähriger Junge…"}, …}`; Sonderstimmen je Zeile über `"stimme": "Lorchen_Kind"` im Szenenplan, Zusatz über `"stil_zusatz": "flüsternd"`.
Gemini-Stimmen (Auswahl): weiblich Aoede, Leda, Kore, Zephyr, Gacrux (reif), Sulafat (warm), Laomedeia; männlich Puck, Charon, Algenib (rau), Iapetus, Orus, Achird.
Sync prüfen: `ffmpeg -ss <t> -t 30 -i v.mp4 -vn -af silencedetect=n=-40dB:d=0.4 -f null -` → Sprech-Einsätze = Intro + Titel + Szenenstart + Fensterstart.

## Soundeffekte (ElevenLabs – nur Effekte, keine Musik)
```
python3 sfx_elevenlabs.py <NN_Folge>/04_Video/01_Ton/sfx_katalog.json <NN_Folge>/04_Video/01_Ton/sfx [--nur id1,id2] [--force]
```
Katalog: `{"auto_parkt": {"prompt": "small family car slowly driving into a driveway …", "dauer": 5}}` (englische Prompts, 0,5–22 s). Key in `~/.elevenlabs_key`. Musik erzeugt man mit Gemini Lyria im Browser (siehe „Musik – Gemini Lyria“), nicht hier.
Ton in das Vorschau-Video mischen: `python3 hoerstoryboard_bauen.py … --ton <NN_Folge>/04_Video/01_Ton/ton_rN.json`.

## Sprachwerkzeug (venv `.venv_sprache`, faster-whisper large-v3-turbo + VAD)
Prüfen:
```
.venv_sprache/bin/python sprache_abschreiben.py <clip.mp4|ordner> --soll flow_video_prompts_rN.json [--bericht bericht.md]
```
Schneiden + Zusammensetzen (stille Enden weg, .srt, Schnittliste):
```
.venv_sprache/bin/python flow_clips_schneiden.py <ausgabe.mp4> --clips <ordner1> [<ordner2>] --soll <p1.json> [<p2.json>] \
   --reihenfolge SH010,SH011,... --intro 00_Intro_Maxi_Cartoons/Maxi_Cartoons_Intro.mp4 --einblenden 1.0 \
   [--start SH040=0.6] [--pause 0.5]
```
Kein `--titel` in der Flow-Fassung. Untertitelspur zuschaltbar: `ffmpeg -i v.mp4 -i v.srt -map 0 -map 1 -c copy -c:s mov_text -metadata:s:s:0 language=ger v_mit_Untertitelspur.mp4`.

## Intro
- Quer (aktuell): `00_Intro_Maxi_Cartoons/Maxi_Cartoons_Intro.mp4` (4,54 s, Bild v3 + Ton v2). Vermerk: `00_Intro_Maxi_Cartoons/00_VERMERK_Intro.md`.
- Hochkant (vorhanden): `00_Intro_Maxi_Cartoons/Maxi_Cartoons_Intro_Hochkant.mp4` (1080×1920, 4,54 s). Neu bauen: `python3 intro_bauen_v2.py <aus.mp4> --format hochkant --logo ... --song ... --clip DATEI:START:DAUER:AUSSCHNITT ...` (Ausschnitt 0..1 = Bildmitte des 9:16-Ausschnitts oder `box`). Gleiche Clips/Zeiten wie die Querfassung (siehe Vermerk), Ton wie die Querfassung.
- Format prüfen: `ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 <datei>`.

## Musik – Gemini Lyria
- Erzeugen: Gemini „Musik erstellen“ (Lyria), Instrumental, Dauer Standard (~3 min); Download „Nur Audio (MP3-Track)“ → `00_Musik_Serie/`. Prompt: Stimmung, Instrumente, Tempo, „dezent unter Dialog“.
- Vorhanden: `Musik_01_Herbstwald_Leaves_and_Tiny_Treasures.mp3` (Wald, ~1,2 s Stille am Anfang → `ab=1.0`), `Musik_02_Kueche_Abend_Shared_Plates_and_Smiles.mp3` (Abend/Essen).
- Unterlegen:
```
python3 musik_unterlegen.py <video.mp4> <ausgabe.mp4> --cue <musik.mp3>@<von>-<bis>[:ab=<s>][:laut=<dB>] [--cue ...] --ducking --fade 1.5
```
Folgenanfang: `--cue 00_Musik_Serie/Musik_01_...mp3@4.54-13.5:ab=1.0:laut=-9`.

## Flow im Browser (Claude in Chrome)
- Download: Chrome blockiert nach 2 Dateien → Blob-Download per JS abfangen und an einen Empfänger auf 127.0.0.1 posten (Details: `09_…/04_Video/05_Flow_Szenenvideos/` Vermerk). Flow löst den Anker-Klick erst nach einigen Sekunden aus → Dateinamen erst nach Eingang der vorigen Datei umstellen (~10 s je Clip).
- Bild-Upload: `HTMLInputElement.click` für type=file abfangen, dann `file_upload` auf das Feld (kein Datei-Dialog).
- Google-Filter: Prompt neutral umformulieren und neu senden.

### Szenenbilder in Flow ohne Skript (bewährt 2026-11-06, Folge Tante Frieda, 30 Bilder in ~1,5 h)
Flow-Seite (Nano Banana 2.1) hat **keinen Datei-Input**, der Upload-Knopf öffnet einen nativen Dialog; Strg+V mit Bild friert den Tab ein. Stattdessen:
1. Folgenordner lokal ausliefern: `cd NN_Folge && python3 -m http.server 8765 --bind 127.0.0.1`; dort `_flow_view.html` (zeigt `?i=<pfad>` randlos, `object-fit: cover`). `file://` darf das Plugin nicht öffnen; Chromes eigene Bildansicht hat schwarzen Rand → Flow malt den Rand mit.
2. Zweiter Tab: `_flow_view.html?i=02_Szenen_Blender_Mockups/SHxxx_blender.jpg` öffnen, **Screenshot in voller Größe** (mit `scale` kommen nur ~20 KB an), dann `upload_image(imageId, coordinate=[700,400])` auf den Flow-Tab = Drag & Drop. Dateiname `SHxxx_mockup.jpg`. Modelsheets/OBJ-Sheets einmal genauso hochladen (Kurznamen `CHAR_01_Maxi.jpg` …).
3. Referenzen: Knopf „Bildelemente zum Prompt-Feld hinzufügen“ (per `find`-ref klicken, nicht per Koordinate) → Picker mit Suchfeld → Name tippen → „Zum Prompt hinzufügen“. Reihenfolge = Referenz 1, 2 … (Mockup zuerst). Fertige Flow-Bilder als Raum-Referenz über ihren Flow-Titel suchen (z. B. „Boy places cage“).
4. Prompt tippen (`flow_chrome_prompts.py A|B SHxxx` liefert Suchbegriffe + Prompt), senden. Während Flow malt, nächste Szene vorbereiten.
5. Download: Kachel-Menü ⋮ → Herunterladen → 1K; `python3 flow_holen.py SHxxxA` holt die neueste Datei aus ~/Downloads (wartet bis 20 s, schneidet Ränder, legt Prompt daneben, verhindert Doppelverwendung).
Fallen: Ein Fehlklick auf eine Kachel öffnet die Bearbeiten-Ansicht („Was möchten Sie ändern?“) – dort NIE senden, Prompt löschen und zurück. Tippen ohne offenes Feld löst Tastenkürzel aus (Agentenmodus an, Ansicht wechselt) – Agentenmodus wieder ausschalten, Modell muss „Nano Banana 2.1“ zeigen. Fenstergröße kann sich ändern → Koordinaten neu messen. „Fehlgeschlagen – verstößt möglicherweise gegen Richtlinien“ kam bei allen Opa-Szenen an der Haustür (auch neutral, auch ohne Opa-Sheet) – zurückstellen. **„Ungewöhnliche Aktivitäten festgestellt“ = sofort aufhören und dem User melden** (nach ~35 Bildern am Stück).

## Thumbnail / Cover – `thumbnail_bauen.py`
1. Hintergrund in Flow ohne Schrift (Maxi groß, frontal, mit dem Haupt-Objekt; Gegenspieler klein hinten; eine Bildseite bzw. das obere Drittel ruhig für den Titel). **Bildwerkzeug nimmt höchstens 3 Referenzen** (Maxi, Gegenspieler, Ort) – Objekte über den Text beschreiben und danach prüfen. (Seit 2026-11-06 prüft `valid_image` die längere Bildseite; vorher wurden Hochkantbilder 768×1376 fälschlich als „fail“ gemeldet.) Für 9:16 `style: none` + eigene Stil-Präambel mit „HOCHFORMAT 9:16“.
2. Text drauf:
```
python3 thumbnail_bauen.py <hintergrund.jpg> <aus.jpg> --format quer|hochkant --zeile "PILZE IM" --zeile "HERBSTWALD!" --folge "FOLGE 2" [--titel-seite links|rechts]
```
quer = 1280×720 (YouTube), hochkant = 1080×1920 (TikTok-Cover). Ablage `NN_Folge_…/05_Thumbnail/`. Prüfen, dass Titel/Plakette kein Gesicht verdecken.
