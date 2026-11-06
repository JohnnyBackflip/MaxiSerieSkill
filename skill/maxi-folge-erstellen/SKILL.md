---
name: maxi-folge-erstellen
description: Eine Folge der Serie „Maxi Cartoons“ (Maxis Welt) von der Geschichte bis zum fertigen Video bauen – Szenenplan, Objekt-Sheets, Blender-Blockouts und Mockups, Flow-Bilder, Storyboard-Video mit Bildprüfung, Veo-Szenenvideos mit Dialog, Sprachprüfung und Schnitt, Intro, Einblenden, Lyria-Musik, Thumbnail und Social-Media-Texte (TikTok/YouTube) – und das Projekt-Wiki pflegen. Verwenden, wenn der User eine neue Folge, Szene, Figur, einen Ort oder eine Korrekturrunde für Maxi Cartoons / Maxis Welt / die Korrekturmappe will, oder von Storyboard-Video, Flow-Szenenvideo, Veo-Dialog, Intro, Hintergrundmusik, Thumbnail, TikTok/YouTube-Texten oder Wiki der Serie spricht.
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
- Ablage: `00_Drehbuch_und_Szenenplan_Folge_NN.md`.

### 2. Objekte zuerst
Jeder Gegenstand, der gehalten wird oder eine Rolle spielt → `OBJ_xx`-Modelsheet in Flow (Stil `object`: zwei Ansichten, Studio-Hintergrund, Farben/Maße, Größenbezug zu Maxi). Zwei Zustände (Korb leer/voll) auf ein Blatt.

### 3. Neue Orte in Blender (wiederverwendbar)
- Eigene `.blend` je Ort, Standardkameras definieren, Screenshots rendern → leere Flow-Raumszene (Referenzen: Screenshot als Layout + bestehende Flow-Szene für den Stil + Objekt-Sheets).
- Jeder Story-Beat bekommt eigenen Ort/eigene Kamera.
- **Blockout baulich prüfen, bevor Flow läuft:** Treppen stehen auf dem Boden, keine Kamera in/unter Bauteilen, keine Bäume/Objekte auf Fahrbahnen, keine Schränke vor Fenstern – Flow malt Blockout-Fehler mit.
- Wiederkehrende Props (Auto, Fahrrad) in `maxi_blender_lib.py`.

### 4. Szenen-Mockups in Blender
- Farbpuppen: blau Maxi, gelb Mama, grün Papa, orange Karl; Props; Kamera; PNG + `.blend` je Szene (`02_Szenen_Blender_Mockups/`, Skript `build_folgeNN_szenen*.py`).
- Prüfen: Figuren groß genug (Erwachsene ≈ halbe Bildhöhe – kleine Figuren → verzerrte Gesichter), Gesichter zur Kamera, kein Rücken, Gesten treffen ihr Ziel (`point_down`), Fahrzeuge exakt seitlich/frontal.
- Für Dialog-Einstellungen eigene Sprecher-Startbilder (Sprecher halbnah frontal), z. B. `SH090S`.

### 5. Szenenbilder in Flow
- Prompt = Stil-Präambel (`scene`) + LAYOUT-Satz (Mockup nur als Layout, Puppen durch Figuren ersetzen) + Motiv + Tageszeit/Licht + **Architektur-Block des Ortes** (was steht wo, was es NICHT gibt) + Gesichts-Satz + Verbote.
- Referenzen in fester Reihenfolge: **1 Mockup, 2 (bei B-Bildern) fertiges A-Bild / freigegebenes Szenenbild, dann CHAR-Modelsheets, OBJ-Sheets, Raumszene des Ortes** (+ Raumszene des sichtbaren Nachbarraums, + Szene mit korrekter Architektur).
- A/B nacheinander: erst alle Startbilder, dann Endbilder mit Startbild als Referenz 2.
- Batch `--parallel 2–3`, nicht parallel zu zwei Blender-Instanzen (Speicher). Flow braucht 1,5–7 min/Bild.

### 6. Storyboard-Video mit Bildprüfung (PFLICHT)
- Manifest → `build_episode_video.py`: jede Szene exakt so lange wie geplant; oben links SH-ID + Zeit, **oben rechts „Bild NN“**, unten Sprecher + Text (nur im Sprechfenster); `_Bildliste.md` entsteht automatisch.
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
