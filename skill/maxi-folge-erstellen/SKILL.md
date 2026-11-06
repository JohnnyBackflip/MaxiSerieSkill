---
name: maxi-folge-erstellen
description: Eine Folge der Serie „Maxi Cartoons“ (Maxis Welt) von der Geschichte bis zum fertigen Video bauen – Szenenplan, Objekt-Sheets, Blender-Blockouts und Mockups, Flow-Bilder, Figurenstimmen mit Gemini-TTS, Soundeffekte mit ElevenLabs, Musik mit Gemini Lyria, Hör-Storyboard, Storyboard-Video mit Bildprüfung und Stimmen, Veo-Szenenvideos mit Dialog, Sprachprüfung und Schnitt, Intro, Einblenden, Lyria-Musik, Thumbnail und Social-Media-Texte (TikTok/YouTube) – und das Projekt-Wiki pflegen. Verwenden, wenn der User eine neue Folge (auch frei nach einer Buch-Vorlage), Szene, Figur, einen Ort oder eine Korrekturrunde für Maxi Cartoons / Maxis Welt / die Korrekturmappe will, oder von Storyboard-Video, Stimmen/TTS/Hör-Storyboard, Flow-Szenenvideo, Veo-Dialog, Intro, Hintergrundmusik, Thumbnail, TikTok/YouTube-Texten oder Wiki der Serie spricht.
---

# Maxi-Folge erstellen

Projektordner (Root) = Ordner, in dem `agy_generate_image.py` & Co. liegen: lokal `/home/felix/projects/dump/Maxis_Welt_Korrekturmappe`, auf anderen Rechnern der Klon von github.com/JohnnyBackflip/MaxiSerieSkill (Umgebungsvariable `MAXI_ROOT` setzen, falls Skripte von woanders laufen). Alle Pfade unten relativ dazu.
Neuer Rechner? Zuerst `references/einrichtung.md` (Programme, venv, Flow/Chrome, Prüfbefehl).
Gelernt an Folge 02 „Pilze im Herbstwald“ (2026-11-04 bis 11-06). Musterordner: `09_Folge_02_Pilze_im_Herbstwald/`.

**Grundregeln**
- **Kein Komitee.** Direkt in die Korrekturmappe arbeiten; alles ist Vorlage zur Korrektur durch den User.
- `00_VERBINDLICHER_STORYBOARD_UND_FLOW_WORKFLOW.md` (Komitee, 2-s-Takt, Storyboard-PDF) ist **überholt** – dieser Skill gilt.
- Nichts überschreiben: alte Fassungen nach `rejected/` (mit Rundensuffix `_r4`, `_v001` …), Skripte vor Änderungen als `*_vor_<Grund>.py.bak` sichern, Videos als neue Version (`-v00N`).
- Jede Folge hat einen `00_VERMERK_*.md`, der nach jeder Runde fortgeschrieben wird (was, warum, welche Dateien/Jobs).
- **Das Wiki (`00_WIKI/`) wird bei jeder Änderung mitgepflegt** (siehe Abschnitt „Wiki“).

Befehle, Prompt-Bausteine und Werkzeug-Details: `references/werkzeuge_und_befehle.md`.
Einrichtung auf einem neuen Rechner: `references/einrichtung.md`.
Veo/Flow-Dialog-Regeln (STRIKT): `references/veo_flow_dialog_regeln.md` – vor jedem Szenenplan und jedem Flow-Video lesen.

## Wiki (übergeordnet, Pflicht)

`00_WIKI/` im Root ist das Inhaltsverzeichnis der ganzen Serie: Was gibt es, wo liegt es, in welcher Folge kommt es vor.
- `00_START.md` – Übersicht + Links auf die Seiten unten, Stand-Datum.
- `Figuren.md` – je Figur: ID (`CHAR_xx`), Name, Rolle, Standardkleidung, Blender-Farbcode, Modelsheet-Pfad, Steckbrief, Folgen, in denen sie vorkommt.
- `Orte_und_Kameras.md` – je Ort: Blend-Datei, Kameras (`KOM_CAM_xx`, `FLUR_CAM_xx`, `WALD_CAM_xx`, `TUNNEL_CAM_xx` …), Blender-Screenshot, leere Flow-Raumszene, `REF_xx`, Architektur-Block (was es dort gibt / NICHT gibt), Sitzordnungen.
- `Objekte.md` – je `OBJ_xx`: Beschreibung, Zustände, Sheet-Pfad, Folge.
- `Folgen_und_Szenen.md` – je Folge: Titel, Ordner, Status, aktuelle Video-Versionen; Szenentabelle (SH-ID, Länge, Ort/Kamera, Sprecher, Zeile, Startbild, Flow-Clip, Status).
- `Musik_und_Intro.md` – Intro-Fassungen und -Formate, Musiktracks (Datei, Länge, Stimmung, wo verwendet).
Regel: Neue Figur, neuer Ort, neue Kamera, neues Objekt, neue Szene, neue Version → im selben Arbeitsschritt ins Wiki. Vor jeder neuen Folge zuerst im Wiki nachsehen, was wiederverwendet werden kann.

## Ablauf je Folge

### 1. Geschichte und Szenenplan
- Standard: **Charakterbibel v2.1** (`10_Charakterbibel_v2_Mehr_Wuerze/Charakterbibel_v2.1_Maxis_Welt.md`) – Missions-Regel, Beat-Sheet, Figuren, Staffelziel.
- Datum/Jahreszeit festlegen; wenige Figuren; neue Figur → Modelsheet in Flow (neutral formulieren, sonst Google-Filter: keine Körper-/Kleidungsbegriffe bei Kindern wie „Leggings“, „schlaksig“, „rundlich“).
- Szenenplan-Tabelle: ID (SH010, SH011 …), Dauer **4/6/8 s**, Ort/Kamera, Bild, Sprecher, Zeile, Sprechzeitfenster.
- **Eine Einstellung = EIN Sprecher**, Zeilen ≤ ~8 Wörter / ≤ 3 s, Sprecher groß, halbnah, frontal (Details: Dialog-Regeln).
- Tageszeit je Szenenblock festschreiben (ab Abend sind alle Fenster/Außenbilder dunkel). Standardkleidung. Feste Sitz-/Platzordnung je Ort.
- Ablage: `00_Drehbuch_und_Szenenplan_Folge_NN.md` **und** `szenenplan_rN.json` (je Einstellung `id, sek, ort, bild, sprecher, zeile, fenster, block, tageszeit`, optional `stimme`, `stil_zusatz`) – die JSON speist Stimmen und Hör-Storyboard.
- **Buch-/Fremdvorlage** (z. B. Ludwig Thoma, „Tante Frieda“ → Folge FTF): Nur gemeinfreie Texte oder Vorlagen mit Erlaubnis übernehmen und auch dann nur die Handlung – Dialoge neu schreiben, Illustrationen nicht verwenden, Figuren neu entwerfen. Im Drehbuch eine Tabelle „Original → heute“ (Figur/Ereignis | heute | warum) anlegen; Unzeitgemäßes (Titel, Stände, Geld) ersetzen, und alles, was gegen die Nachahmungsregel verstößt (Feuer, Pulver, Tierquälerei), zu einem harmlosen Gag umbauen. Danach die Bibel-Bausteine nachweisen (Mission, Uhr, Mutprobe, Reparatur, Hochgefühl).

### 1b. Figurenstimmen (Gemini-TTS) und Hör-Storyboard
Damit sich der User die Geschichte vor den Bildern vorstellen kann – und später als Tonspur des Storyboard-Videos.
- Keys: eine Zeile je Google-API-Key in `~/.config/maxi/google_api_keys.txt` (chmod 600). **Niemals ins Projekt/Repo** (öffentlich!). Vor dem Push `git grep -n "AIza"` → muss leer sein.
- Besetzung je Folge in `04_Video/00_Stimmen_TTS/besetzung.json` (Sprecher → `voice`, `stil`, `halbtoene`, `tempo`). Bewährt (FTF): Maxi Puck +4, Anna Leda +4, Mama Aoede, Papa Charon, Opa Algenib −1, Frieda Gacrux +1, Papagei Gacrux +4 (mehr als +4 wird unverständlich). Kinder = erwachsene Stimme + 4 Halbtöne + „wie ein fünfjähriger Junge/Mädchen“ im Stil.
- Erzeugen: `python3 stimmen_tts.py <szenenplan.json> <besetzung.json> <ordner> [--nur SH010,…] [--force]` → `<SH>_<Sprecher>.wav` (+ `.prompt.txt`), Stille an den Rändern weg, Lautheit normalisiert, Keys reihum.
- Prüfen: `.venv_sprache/bin/python stimmen_pruefen.py <szenenplan.json> <ordner>` (Whisper, OK ab 0,8). Fehlerhafte Zeile nach `rejected/<name>_v00N.wav`, mit `--nur` neu erzeugen. Stimme/Figur selbst anhören lassen – Whisper erkennt keine Sprecher.
- Hör-Storyboard: `python3 hoerstoryboard_bauen.py <szenenplan.json> <stimmen_ordner> <04_Video/…_Hoerstoryboard-v00N.mp4> --titel "<Titel>" [--bilder 03_Szenen_Flow_Bilder]`. Ohne Bilder: Karte je Einstellung (Ort, Bild, Tageszeit); mit `--bilder` nimmt es `SHxxx*.jpg`. Intro + Titelkarte davor, jede Stimme beginnt am Anfang ihres Sprechfensters. Ton-Sync mit `silencedetect` an einer Stelle nachmessen.

### 2. Objekte zuerst
Jeder Gegenstand, der gehalten wird oder eine Rolle spielt → `OBJ_xx`-Modelsheet in Flow (Stil `object`: zwei Ansichten, Studio-Hintergrund, Farben/Maße, Größenbezug zu Maxi). Zwei Zustände (Korb leer/voll) auf ein Blatt.

### 3a. Haus texturieren (Flow-Texturen, UV-Maps, Details) – vor den Mockups
- Texturkatalog `03_Blender_3D_Haus_Blockout/texturen_katalog.py` (id → Flow-Beschreibung, Meter je Bild, Modus kachel/fit). Jeder Raum bekommt einen **individuellen Boden**, dazu Wände, Dach, Türen, Fensterrahmen, Küchenschränke, Treppe, Möbelhölzer, Stoffe, Rasen, Pflaster, Asphalt, Hecken, Nachbarhäuser.
- Ablauf: `python3 texturen_katalog.py` → `jobs_texturen.json` → `agy_generate_image.py batch … --parallel 3` (Rohbilder `Texturen/roh/`) → `python3 texturen_nachbearbeiten.py` (nahtlos per Versatz-Überblendung, quadratisch 1024 px) → `blender -b Maxis_Haus_Komplett_Blockout.blend --python texturiere_haus.py` → `Maxis_Haus_Komplett_Texturiert.blend`.
- `texturiere_haus.py` ersetzt Materialien nach Namen, baut **UV-Maps im Weltmaß** (Box-Projektion, Meter je Textur; Türen: ein Bild je Fläche) und ergänzt Details: Fußleisten, Sockel außen, Treppenverkleidung (EG-Treppe, Dachbodentreppe), Küchenfronten mit Griffen, Fensterscheiben.
- Texturregeln: mattes Albedo, keine Schatten/Glanzlichter/Perspektive, nahtlos, keine Schrift. Mockups ab jetzt mit der **texturierten** Blend rendern (`blender -b Maxis_Haus_Komplett_Texturiert.blend --python build_…`). Texturen, Blend und Mockup-PNGs dauerhaft ins Repo (nicht `.gitignore`n).

### 3b. Licht (Cycles): warme Sonne durch die Fenster, Schatten, Dunst
- `03_Blender_3D_Haus_Blockout/licht_haus.py` entfernt alle Lampen und die Pseudo-Aufhellung (Emission 0,14 in den Blockout-Materialien), setzt eine warme tiefe Sonne (Azimut je Raum so, dass sie durch dessen Fenster fällt), Himmel (Multiple-Scattering-Sky) und ein **begrenztes Dunst-Volumen** (Box um das Viertel; ein Welt-Volumen ist unendlich und löscht auch die Sonne → schwarzes Bild!). Konturlinien aus, AgX, GPU (CUDA).
- `blender -b Maxis_Haus_Komplett_Texturiert.blend --python licht_haus.py -- [--raeume EG_Kueche,… | --aussen] [--samples 64] [--save]` → Raumbilder in `Raumbilder_Licht/`. 64 Samples + OIDN ≈ 1,5 min je Bild (GTX 1080). Dunkle Räume (Flur OG, Dachboden) brauchen mehr Belichtung/anderen Azimut (Tabelle `ROOMS`).
- Mockups können mit dem Licht gerendert werden, indem `build_…_szenen.py` mit `Maxis_Haus_Komplett_Texturiert_Licht.blend` gestartet wird (Cycles statt Eevee, deutlich langsamer).

### 3. Neue Orte in Blender (wiederverwendbar)
- Eigene `.blend` je Ort, Standardkameras definieren, Screenshots rendern → leere Flow-Raumszene (Referenzen: Screenshot als Layout + bestehende Flow-Szene für den Stil + Objekt-Sheets).
- Jeder Story-Beat bekommt eigenen Ort/eigene Kamera.
- **Blockout baulich prüfen, bevor Flow läuft:** Treppen stehen auf dem Boden, keine Kamera in/unter Bauteilen, keine Bäume/Objekte auf Fahrbahnen, keine Schränke vor Fenstern – Flow malt Blockout-Fehler mit.
- Wiederkehrende Props (Auto, Fahrrad) in `maxi_blender_lib.py`.

### 4. Szenen-Mockups in Blender (PFLICHT vor jedem Flow-Szenenbild)
- **DIALOGE (User 2026-11-06, Skill `dialog-szenen-inszenieren`):** Szene EINMAL aufbauen (feste Positionen/Blickrichtungen im Skript als gemeinsamer Block), dann je Sprecher nur die **Kamera** wechseln (frontal, Over-the-Shoulder, Übersicht). Nie die Figuren pro Einstellung an dieselbe Stelle setzen und austauschen. Mindestens 3 Einstellungen pro Aufstellung aus verschiedenen Perspektiven.
- Mimik der Puppen: Posen `open`, `sip`, `face`, `lie`, `mood=angry|startled|suspicious|sad` (Augenbrauen), `prop_wardrobe` (öffnender Schrank), großer Käfig `prop_cage`. Farbpuppen: blau Maxi, gelb Mama, grün Papa, orange Karl, türkis Anna, braun Opa, violett Frieda (weitere Farben im Wiki `Figuren.md` festlegen); Props; Kamera; PNG + `.blend` je Szene (`02_Szenen_Blender_Mockups/`, Skript `build_folgeNN_szenen*.py`).
- Prüfen: Figuren groß genug (Erwachsene ≈ halbe Bildhöhe – kleine Figuren → verzerrte Gesichter), Gesichter zur Kamera, kein Rücken, Gesten treffen ihr Ziel (`point_down`), Fahrzeuge exakt seitlich/frontal.
- Für Dialog-Einstellungen eigene Sprecher-Startbilder (Sprecher halbnah frontal), z. B. `SH090S`.

### Audio-Regel (User 2026-11-06, gilt für ALLE Ton- und Sprachteile in ALLEN Videos)
Jede Spur läuft durch **Kompressor + Limiter** und wird auf gleiche Lautstärke gebracht – Stimmen, Effekte, Musik und zuletzt das fertige Video (Master).
- Ketten: `audio_kette.py` (Stimme: Kompressor Ratio 3 → Mittel −20 dB → Limiter −1,5 dBFS; Effekt/Musik eigene Kompressoren; Master: Kompressor + Limiter + `loudnorm` −16 LUFS, Spitze −1,5 dB).
- `stimmen_tts.py` ruft `stimmen_normalisieren.py` selbst auf (Originale in `…/vor_Normalisierung/`); `hoerstoryboard_bauen.py` wendet Effekt-, Musik- und Master-Kette an.
- **Alles andere** (Veo-Clips, `flow_clips_schneiden.py`-/`musik_unterlegen.py`-Ausgaben, Intro-Zusammenschnitt): am Ende `python3 video_pegeln.py <video.mp4>` (Bild bleibt unverändert).
- Prüfen: `ffmpeg -i v.mp4 -af ebur128 -f null -` (≈ −16 LUFS), Spitze < −1,5 dB, alle sprechenden Szenen ähnlich laut (TTS liefert teils −40 dB und leiser: sonst hört man nichts).

### 4b. Mockup-Vorschau-Video (Freigabe vor Flow)
- **Ton-Quellen (User-Vorgabe 2026-11-06, strikt getrennt):** Stimmen = Gemini-TTS (1b). **Soundeffekte NUR mit ElevenLabs** (`sfx_elevenlabs.py`, Katalog `04_Video/01_Ton/sfx_katalog.json`, Key `~/.elevenlabs_key`, nie ins Repo). **Musik NUR mit Gemini Lyria über das Chrome-Plugin** (gemini.google.com → Plus → „Musik erstellen“, Gesang „Instrumental“, Download „Nur Audio (MP3-Track)“ → `00_Musik_Serie/Musik_NN_…`; die ElevenLabs-Music-API nicht benutzen). Stimmung je Szene passend wählen, z. B. heimliche Szenen = Schleichmusik (Pizzicato, Holzbläser-Staccato).
- Effekte/Musik an die passenden Szenen legen: `ton_rN.json` mit `sfx:[{datei,sh,off,db}]` und `musik:[{datei,von,bis,ab,db}]` (Musik ca. −11 dB, Fade ein/aus automatisch), Video mit `--ton ton_rN.json` bauen. Effekt-Ideen: Auto parkt/fährt weg, Tür/Schritte, Ball, Sprühen, Tier-Geräusche, Koffer, Bett, Dose klackt. Danach Pegel (`volumedetect`, Spitze < −0,5 dB) und eine Stelle mit Musik prüfen.
- Aus den **unstilisierten** Blender-Mockup-PNGs (`SHxxx_blender.png`) + den TTS-Stimmen (1b) das Video bauen: `python3 hoerstoryboard_bauen.py <szenenplan.json> <stimmen> <04_Video/…_Mockup-Vorschau-v00N.mp4> --titel "<Titel>" --bilder 02_Szenen_Blender_Mockups` (nimmt `SHxxx_blender.png`) (Bilder werden nummeriert: „Bild NN“ oben rechts, siehe Schritt 6).
- Dem User zeigen, Kritik als „Bild NN: …“ einarbeiten (Mockups/Szenenplan/Zeilen ändern, Stimmen neu), neue Version `-v00N`. **Erst nach ausdrücklicher Freigabe weiter zu Schritt 5.**

### 5. Szenenbilder in Flow (nur nach Freigabe von 4b)
- Prompt = Stil-Präambel (`scene`) + LAYOUT-Satz (Mockup nur als Layout, Puppen durch Figuren ersetzen) + Motiv + Tageszeit/Licht + **Architektur-Block des Ortes** (was steht wo, was es NICHT gibt) + Gesichts-Satz + Verbote.
- Referenzen in fester Reihenfolge: **1 Mockup, 2 (bei B-Bildern) fertiges A-Bild / freigegebenes Szenenbild, dann CHAR-Modelsheets, OBJ-Sheets, Raumszene des Ortes** (+ Raumszene des sichtbaren Nachbarraums, + Szene mit korrekter Architektur).
- **A/B je Einstellung (User-Vorgabe 2026-11-06):** Jede Szene bekommt ein **Startbild A** (`SHxxxA.jpg`) und ein **Endbild B** (`SHxxxB.jpg`). Im Video zeigt A die **erste Hälfte** und B die **zweite Hälfte** der Szenenzeit (beide Bilder werden nummeriert). A zuerst, dann B mit dem fertigen A als Referenz 2 (Mockup bleibt Referenz 1; bei Zoom/Sprung/anderem Winkel ein eigenes B-Mockup `SHxxx_B_blender.png`). B-Text = was sich in der zweiten Hälfte ändert (Haltung, Blick, Zoom), Kamera/Ort/Licht bleiben.
- **Skripte:** `make_jobs_flow.py A|B [SHxxx …]` je Folge (Datenblock `ENDE` mit dem Endmotiv je Szene, Figuren-/Objekt-Referenzen automatisch aus dem Szenentext, höchstens 5 Referenzen) und `flow_treiber.py` (Hintergrundlauf: nimmt fertige Mockups, malt A, dann B; `MOCK_START=<Epoche>` setzt, ab wann Mockups als neu gelten – sonst werden alte Mockups gemalt!).
- **Kontingent der Bildgenerierung (agy) ist begrenzt:** Nach ca. 18 Bildern (2026-11-06) kam `RESOURCE_EXHAUSTED (429) – Individual quota reached, Resets in ~150 h`. Dann **sofort alle Läufe stoppen** (kein Wiederholen, der Treiber bricht ab), dem User Stand und Reset-Zeit nennen und fragen (Upgrade, anderes Konto, Wartezeit, Browser-Flow). Vorher Bilder sparsam planen: nur Szenen, die in der Fassung wirklich vorkommen, und Startbilder zuerst; Einzelbild-Tests vor Großläufen.
- **Mockup-Render:** Cycles mit Licht kostet ~100 s je Bild (auch mit Persistent Data) – für ~70 Szenen nur als Referenz zu teuer; für Flow-Referenzen reicht **Eevee** (`MOCKUP_LICHT=1 MOCK_EEVEE=1 blender -b …_Licht.blend --python build_…_szenen.py -- …`, ~30 s je Bild, Belichtung −1,7 gegenüber Cycles).
- **Flow im Browser (Claude in Chrome):** Referenzbilder per **Strg+V aus der Zwischenablage hängen den Flow-Tab auf** (2× am 2026-11-06, auch mit 768-px-PNG; danach Screenshots/Tasten timeouten, der User musste Chrome neu öffnen). Der Datei-Dialog (`Medien hochladen`) ist für das Plugin nicht bedienbar, und die Regel „keine Skripte in der Flow-Seite“ verbietet das Abfangen des Datei-Inputs. **Erst mit dem User klären, wie Referenzen eingebracht werden sollen** (z. B. Bilder vorab in Flows Bibliothek/Charakter ablegen), nicht erneut Strg+V versuchen.
- Die Bildprüfung (Schritt 6) gilt für beide Bilder; schlechte Bilder nach `rejected/` und mit `make_jobs_flow.py A|B SHxxx` neu.
- Batch `--parallel 2–3`, nicht parallel zu zwei Blender-Instanzen (Speicher). Flow braucht 1,5–7 min/Bild.
- Jobs immer per Skript `make_jobs_NN_*.py` (Datenblock je SH: Raum, Figuren, Objekte, Licht, Motiv, Sprecher → Prompt-Bausteine), Log `jobs_NN_*.log`. Höchstens 5 Referenzen je Bild.
- **IMMER erst Blender-Mockups mit Farbpuppen (Schritt 4), dann daraus die Flow-Bilder.** Kein Bild nur mit Raumszene als Layout; Referenz 1 ist immer das Mockup.
- **FREIGABE-SCHRANKE (User 2026-11-06): Flow-Szenenbilder erst malen, wenn der User das Mockup-Vorschau-Video (Schritt 4b) freigegeben hat.** Vorher keine Flow-Welle starten – auch nicht „zur Beschleunigung“.
- Neue Figuren/Objekte als **Welle 1** (`make_jobs_01_sheets.py`), Szenen als **Welle 2** erst danach starten (Szenen brauchen die Sheets als Referenz).

### 6. Storyboard-Video mit Bildprüfung (PFLICHT)
- Manifest → `build_episode_video.py`: jede Szene exakt so lange wie geplant; oben links SH-ID + Zeit, **oben rechts „Bild NN“**, unten Sprecher + Text (nur im Sprechfenster); `_Bildliste.md` entsteht automatisch.
- **Bilder im Vorschau-/Storyboard-Video IMMER nummerieren** (User-Vorgabe 2026-11-06): oben rechts „Bild NN“, laufend in Spielreihenfolge, dasselbe Bild = dieselbe Nummer (`number_images` im Manifest, Standard an – nie abschalten). Auch im Hör-Storyboard und in jeder Korrekturfassung; `_Bildliste.md` ordnet Nr. → SH-ID → Datei. Der User kritisiert per „Bild NN: …“. **Wichtig:** Fügt man Einstellungen ein, verschieben sich die Nummern – im Vermerk und in der Antwort an den User eine Tabelle „Bild (alt) → Änderung“ führen und die neuen Nummern aus `_Bildliste.md` nennen.
- **Flow-Video aus A/B-Paaren:** `python3 hoerstoryboard_bauen.py <szenenplan.json> <stimmen> <04_Video/…_Flow-Vorschau-v00N.mp4> --titel "…" --bilder 03_Szenen_Flow_Bilder --paare --kuerzen --ton <ton_rN.json>`. `--paare` = A erste Hälfte, B zweite Hälfte; `--kuerzen` = **lange Pausen ohne Ton abschneiden** (Szenenlänge = Sprache + 0,55 s bzw. Effekt + Auslauf, stumme Szenen ≥ 2,5 s; Standard für jede Fassung). `--format hochkant` baut 1080×1920 mit dem Hochkant-Intro.
- **Mit Stimmen:** Liegen TTS-Stimmen vor (1b), das Storyboard mit `hoerstoryboard_bauen.py … --bilder 03_Szenen_Flow_Bilder` bauen (die Mockup-Fassung davor ist Schritt 4b) – gleiche Manifest-Logik, Bilder statt Karten, Stimmen im Sprechfenster.
- **Titelkarte gibt es NUR im Storyboard-Video** (`title`/`subtitle` im Manifest), nach dem Intro (`"intro"` im Manifest).
- **Jedes Bild selbst prüfen, bevor das Video an den User geht** – Bild für Bild ansehen und gegen Szenenplan, Modelsheets, OBJ-Sheets und Raumszene abgleichen:
  - Figuren: richtige Person, Kleidung/Haare/Farben wie Modelsheet, keine verzerrten Gesichter, richtige Anzahl Figuren, Sprecher groß/frontal.
  - Objekte: Form/Farbe wie OBJ-Sheet, richtiger Zustand (Korb leer/voll), wer hält was.
  - Ort: Architektur wie Blockout (nichts erfunden, nichts fehlt), Sitzordnung, Hintergrundraum korrekt.
  - Kontinuität: Tageszeit/Licht, A→B gleicher Hintergrund, nichts springt zwischen Bildern.
  - Logik: Gesten treffen Ziel, Autos gerade und Einstieg an Seitentüren, niemand am Heck.
- Unstimmigkeit gefunden → Ursache bestimmen (Mockup? Blockout? Prompt? Referenz?), dort korrigieren, Bild neu malen, altes nach `rejected/`. Erst wenn alle Bilder stimmen, Video bauen und dem User mit Liste der eigenen Korrekturen zeigen.

### 7. Korrekturrunden (User-Kritik als „Bild NN: …“)
Kritik → Ursachen-Tabelle (Bild | Kritik | Ursache | Änderung) im Vermerk → nur Betroffenes neu (Blockout/Mockup/Prompt/Bild) → Bildprüfung wie in 6 → Video als neue Version → Vermerk + Wiki fortschreiben.

### 8. Szenenvideos in Flow (Veo)
- flow.google.com → Video → **Frames, nur Startbild**, Veo 3.1 Fast, 720p, Länge 4/6/8 s = Szenenlänge. Prompts in `flow_video_prompts_rN.json` (+ `SHxxx_prompt.txt`).
- **Alle Regeln aus `references/veo_flow_dialog_regeln.md` einhalten.**
- Clips nach `04_Video/0N_Flow_Szenenvideos_*/SHxxx_*.mp4`; Download/Upload-Tricks siehe Werkzeuge.

### 9. Sprachprüfung und Schnitt (Sprachwerkzeug)
- **Sprachfehler testen:** `sprache_abschreiben.py` gegen die Prompt-JSON – Text-Ähnlichkeit, fehlende/falsche Wörter, liegt die Sprache im Soll-Fenster? Stimme (Kind/Frau/Mann = richtiger Sprecher) zusätzlich anhören – Whisper erkennt Sprecher nicht. Fehlerhafter Clip → in Flow neu erzeugen (alten nach `rejected/`).
- **Leere Stellen rausschneiden:** `flow_clips_schneiden.py` schneidet stille Enden weg (Ende = Sprachabschnitt mit letztem Wort + 0,5 s, Mindestlänge 2,5 s). Stillen Anfang/Musikvorspann mit `--start SHxxx=<s>` entfernen (Spektrogramm der ersten Sekunde prüfen). Stille ohne Funktion = weg; Stille mit Funktion (Aktion, Reaktion, Pointe, Blick) bleibt – im Zweifel behalten und in der Schnittliste vermerken.
- Nach dem Schnitt alle Teile erneut abschreiben und mit dem Original vergleichen: kein Wort darf abgeschnitten sein.

### 10. Intro, Folgenanfang, Format
- **Vor JEDES Video das Serien-Intro** `00_Intro_Maxi_Cartoons/Maxi_Cartoons_Intro.mp4` (Flow-Fassung: `--intro`, Storyboard: Manifest `"intro"`).
- **Das Intro muss immer das Format des Videos haben** – Querformat-Folge → Quer-Intro (1280×720), Hochkant-Folge → Hochkant-Intro (1080×1920). Hochkant-Intro bauen mit `intro_bauen_v2.py --format hochkant` (gleiche Clips, Ausschnitt je Clip wählen). Nie ein Intro strecken/stauchen; Format vor dem Zusammenschnitt mit `ffprobe` prüfen.
- **Nach dem Intro: keine Titelkarte** (in der Flow-Fassung). Die erste Einstellung wird **aus Schwarz eingeblendet** (`--einblenden 1.0`), darunter leise Serienmusik (Cue ab Intro-Ende, ca. 9 s, −9 dB, `--ducking`, Stille am Liedanfang mit `ab=` überspringen).

### 11. Hintergrundmusik mit Gemini Lyria (nutzen!)
- Für Szenenblöcke eigene Hintergrundmusik mit **Gemini Lyria** erzeugen (Instrumental, Stimmung/Instrumente passend zum Ort und zur Tageszeit, dezent unter Dialog). Ablage `00_Musik_Serie/Musik_NN_<Ort>_<Titel>.mp3`, Eintrag in `00_Musik_Serie/00_VERMERK_Musik.md` + Wiki (Prompt, Länge, Zweck).
- Vorhandene Tracks zuerst wiederverwenden (Wiki), neue nur für neue Stimmungen.
- Unterlegen mit `musik_unterlegen.py` (Original bleibt unverändert, neue Datei): je Szenenblock ein Cue, ca. −9 dB für Gemini-Tracks, `--ducking`, `--fade 1.5`.

### 12. Abschluss jeder Fassung
Video + `_mit_Untertitelspur.mp4` + `.srt` + Schnittliste; Vermerk (`04_Video/08_Flow_Folge_komplett/00_VERMERK_Flow_Folge.md`) und Wiki aktualisieren; dem User nennen, was geprüft wurde und was offen ist.

### 13. Veröffentlichen: Thumbnail und Social-Media-Texte
- **Texte:** `04_Video/08_Flow_Folge_komplett/social_media.md` – je TikTok und YouTube: Titel, Beschreibung, genau 10 Hashtags (#MaxiCartoons zuerst). YouTube-Beschreibung erzählt die Folge nach und enthält einen Sicherheits-/Lernhinweis, wenn die Folge einen hat. Am Ende Hinweise: YouTube „Ja, für Kinder“, KI-Kennzeichnung (TikTok-Schalter „KI-generierter Inhalt“, YouTube „Veränderte oder synthetische Inhalte“), welches Format/Intro für TikTok vorliegt.
- **Thumbnail:** Hintergrund in Flow **ohne Schrift** (Maxi groß, frontal, strahlend mit dem Haupt-Objekt der Folge; Gegenspieler klein im Hintergrund; eine Bildseite bzw. das obere Drittel ruhig für den Titel), 16:9 für YouTube und 9:16 als TikTok-Cover. Dann `thumbnail_bauen.py` (Logo, Titel in 2 Zeilen, Plakette „FOLGE N“). Ablage `05_Thumbnail/`.
- Bildprüfung wie in 6 (Figuren wie Modelsheet, Objekte wie OBJ-Sheet) + Titel/Plakette verdecken kein Gesicht.
- Auf Wunsch Paket für den Upload zusammenstellen (Video, .srt, Thumbnails, `social_media.md`).

## Ablage je Folge (`NN_Folge_NN_Titel/`)
`00_Drehbuch_und_Szenenplan_Folge_NN.md`, `00_VERMERK_Folge_NN.md`, `00_Charakter_Referenzbilder_Modelsheets/`, `00_Objekt_Referenzbilder_Props/`, `00_Raum_Referenzbilder/`, `01_Neue_Orte_Blender_und_Flow/`, `02_Szenen_Blender_Mockups/` (+ `blend/`, `rejected/`), `03_Szenen_Flow_Bilder/` (+ `rejected/`), `04_Video/` (Storyboard-Videos + Manifeste, `0N_Flow_Szenenvideos_rN/`, `08_Flow_Folge_komplett/` inkl. `social_media.md`), `05_Thumbnail/`, `jobs_NN_*.json` + `.log`, `make_jobs_NN_*.py`.
