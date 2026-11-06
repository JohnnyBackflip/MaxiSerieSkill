# Vermerk Folge „Tante Frieda und Lorchen“

## Runde 1 – 2026-11-06: Geschichte und Szenenplan
- Auftrag: Die erste Geschichte aus Ludwig Thoma, *Tante Frieda. Neue Lausbubengeschichten* (PDF in ~/Downloads), in die heutige Zeit übertragen und als Storyboard nach dem Skill entwerfen.
- Erledigt: Drehbuch und Szenenplan r1 (`00_Drehbuch_und_Szenenplan_Folge_Tante_Frieda.md`): 49 Einstellungen, 4:58 min, mit einer Tabelle vom Original zu heute. Ordnerstruktur angelegt.
- Wichtigste Änderungen am Original: kein Pulver und kein Knall; statt dessen plappert Lorchen nach. Dazu kommt Mutprobe Nr. 18 „Das war ich!“, außerdem Reparatur und Hochgefühl. Aus dem Amtsrichter wird Opa Heinrich, aus Annchen Anna.
- Wiki: Folge, neue Figuren (CHAR_13 Frieda, CHAR_14 Lorchen, beide noch ohne Modelsheet), neue Objekte (geplant) und Puppenfarben eingetragen.
- Offen: die Fragen in Abschnitt 8 des Drehbuchs. Danach folgen die Modelsheets für Frieda und Lorchen, die OBJ-Sheets, die Mockups, die Flow-Bilder und das Storyboard-Video.

## Runde 2 – 2026-11-06: Geschichte freigegeben, Stimmen (Gemini-TTS) und Hör-Storyboard
- Der User hat die Geschichte freigegeben. Die drei offenen Fragen aus Abschnitt 8 hat er nicht beantwortet; bis auf Weiteres gilt der Vorschlag (Sonderfolge, Frieda reist ab, Frieda ist Opas Schwester).
- Szenenplan als Daten: `szenenplan_r1.json` (49 Einstellungen; Felder `stimme` und `stil_zusatz` je Zeile).
- **Stimmen:** Das neue Werkzeug `../stimmen_tts.py` nutzt Gemini-TTS (`gemini-2.5-flash-preview-tts`). Die Keys liegen in `~/.config/maxi/google_api_keys.txt` und werden **nicht im Repo** abgelegt; sie stammen aus dem StrainOracle-Projekt, 9–11 davon funktionieren. Die Besetzung steht in `04_Video/00_Stimmen_TTS/besetzung.json`:
  Maxi Puck +4 Halbtöne, Anna Leda +4, Mama Aoede, Papa Charon, Opa Algenib −1, Frieda Gacrux +1, Lorchen Gacrux +4 (krächzend), Lorchen mit Kinderstimme Puck +8.
- 45 Zeilen wurden erzeugt und mit Whisper geprüft. Neu erzeugt wurden SH071, SH093, SH184 und SH195; die alten Fassungen liegen in `rejected/`. Lorchen war mit +6 Halbtönen unverständlich und hat jetzt +4.
- **Hör-Storyboard:** Das neue Werkzeug `../hoerstoryboard_bauen.py` zeigt je Einstellung eine Bildkarte oder, sobald vorhanden, das Flow-Bild. Die Stimme liegt am Anfang des Sprechfensters; davor stehen Intro und Titelkarte.
- SH184: Lorchen sagt in allen drei Versuchen „Ohne Mecken/Mähkern“. Die dritte Fassung ist als Papageien-Aussprache angenommen, die beiden ersten liegen in `rejected/`.
- Ergebnis: `04_Video/Folge_Tante_Frieda_Hoerstoryboard-v001.mp4` (1920×1080, 5:08 min = Intro 4,5 s + Titel 3 s + 298 s + Ende 2 s, 45 Stimmen) mit Manifest `…_manifest.json` und Bildliste `…_arbeit/bild_Bildliste.md`. Den Ton habe ich an SH141–SH150 mit silencedetect geprüft; die Stimmen setzen genau am Anfang ihres Sprechfensters ein.
- Weiter geht es mit den Modelsheets CHAR_13 Frieda und CHAR_14 Lorchen, den OBJ_TF-Sheets, den Mockups und den Flow-Bildern. Danach wird dasselbe Werkzeug mit `--bilder 03_Szenen_Flow_Bilder` gestartet, und es baut das echte Storyboard mit denselben Stimmen.

## Runde 3 – 2026-11-06: Blender-Mockups und Mockup-Vorschau-Video (ohne Flow-Szenenbilder)
- **User-Vorgaben:** (1) Flow-Bilder immer aus Blender-Mockups mit Farbpuppen. (2) Bilder im Vorschau-Video nummerieren. (3) **Erst das Vorschau-Video nur aus den unstilisierten Mockups mit dem Google-TTS-Ton, Flow-Szenenbilder erst nach Freigabe.** Alles steht im Skill (Schritt 4, 4b, 6).
- Die erste Flow-Welle (50 Szenenbilder ohne Mockup) wurde abgebrochen, bevor ein Bild fertig war. Das Job-Skript liegt als `rejected/make_jobs_02_szenen_ohne_Mockup_NICHT_BENUTZEN.py`; es muss später so umgebaut werden, dass Referenz 1 das Mockup `SHxxx_blender.png` ist.
- **Fertig:** Welle 1 (Sheets): CHAR_13 Tante Frieda, CHAR_14 Lorchen, OBJ_TF01–TF07 in Flow gemalt. Sie sind noch nicht freigegeben, aber unabhängig von den Szenen.
- **Mockups:** `02_Szenen_Blender_Mockups/build_frieda_szenen.py` baut mit `maxi_blender_lib.py` 49 Einstellungen (SH010–SH210) mit Farbpuppen auf dem Haus-Blockout. Ergebnis `SHxxx_blender.png`, Render-Log `render_r1.log`. Neue Puppen und Props in der Lib: Anna türkis, Opa braun, Frieda violett, Hasi, Bello, Lorchen, Käfig, Koffer, Sprüher, Kuchen, Kuchendose, Tasse, Glitzerstein, Mütze, Mut-Dose, Buch, Stuhl. Gesichter sind nur zwei Augenpunkte; Mimik gibt es erst in Flow.
- **Eigene Bildprüfung** (Kontaktbögen): Korrigiert wurden Figuren zu klein (SH010, SH020, SH030, SH070–SH072, SH092), verdeckt (SH152: Stuhl ausgeblendet, SH170: Frieda stand vor Maxi), Sprecher von hinten (SH060, SH090) und das Chaos in SH190 (jetzt von der Beifahrerseite, Frieda im Auto, Familie winkt von hinten). SH130: Anna steht draußen vor dem Sprossenfenster über der Spüle und nicht mehr vor der Glastür (Prompt später anpassen).
- **Video:** `04_Video/Folge_Tante_Frieda_Mockup-Vorschau-v001.mp4` (1920×1080, 5:08 min, 45 Stimmen, Bilder nummeriert, Bildliste in `…_arbeit/bild_Bildliste.md`). Hör-Storyboard `…Hoerstoryboard-v001.mp4` (Karten statt Bildern) bleibt als Vorgänger.
- **Offene Schwächen der Mockups:** In SH190 steht die Familie am Bildrand. Mimik und Gesten sind nur grob (z. B. „Hände an den Wangen“ fehlt), Lorchen ist ein kleiner grüner Klecks. Das wird in Flow über den Prompt erledigt.
- **Nächster Schritt:** Der User schaut das Mockup-Video an, Kritik als „Bild NN: …“, neue Version v002. **Erst nach Freigabe** werden die Flow-Szenenbilder gemalt.
