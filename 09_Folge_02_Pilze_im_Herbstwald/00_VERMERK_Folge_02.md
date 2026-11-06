# Vermerk: Folge 02 „Pilze im Herbstwald“ – Korrekturvorlage

**Erstellt:** 2026-11-04, eigenständig ohne Komitee. Alles in diesem Ordner ist Vorlage zur Korrektur.

## Reihenfolge, in der gearbeitet wurde
1. **Geschichte & Szenenplan** → `00_Drehbuch_und_Szenenplan_Folge_02.md` (22 Szenen à 4/6/8 s, 120 s + Titel/Ende).
2. **Objekte zuerst in Flow** → `00_Objekt_Referenzbilder_Props/OBJ_01…OBJ_08` (Pilzkorb, Steinpilz, Pfifferlinge, Knollenblätterpilz, blaues Familienauto, Karls BMX, Pfanne mit Pilzsauce, Nudelteller). Neue Figur **Karl** → `00_Charakter_Referenzbilder_Modelsheets/CHAR_10_Karl_Nachbarsjunge_Modelsheet.jpg` (erster Prompt wurde vom Google-Filter abgelehnt, neutral umformuliert).
3. **Neue Orte in Blender** (wiederverwendbar) → `01_Neue_Orte_Blender_und_Flow/`:
   - `Herbstwald_Blockout.blend` + `build_herbstwald_blockout.py`: Landstraße, Waldparkplatz mit Holzschild, Waldweg, Wurzelbaum mit Steinpilz-Fundort, Pilzlichtung mit Baumstumpf, Pfifferlingen und Knollenblätterpilz. Sechs Standardkameras `WALD_CAM_01…06`, je als Blender-Screenshot (`.png`) und leere Flow-Raumszene (`FLOW_WALD_CAM_xx.jpg`).
   - Familienauto und BMX sind als Blender-Props in `maxi_blender_lib.py` (Korrekturmappen-Root) hinterlegt und können in jede Szene gesetzt werden.
4. **Szenen-Mockups in Blender** → `02_Szenen_Blender_Mockups/SHxxx_blender.png` (+ `blend/SHxxx.blend` je Szene, Skript `build_folge02_szenen.py`). Standardfiguren aus Primitiven: blau = Maxi, gelb = Mama, grün = Papa, orange = Karl. Haus-Szenen auf Basis des Haus-Blockouts (neue Kameras: Einfahrt mit Auto, Auto-Innenraum), Wald-Szenen auf Basis des Herbstwald-Blockouts.
5. **Flow-Bilder je Szene** → `03_Szenen_Flow_Bilder/SHxxx.jpg` (+ `.prompt.txt` mit allen Referenzen). Referenzen je Bild: Blender-Mockup (Layout), Modelsheets der vorkommenden Figuren, Objekt-Sheets, passende Raumszene.
6. **Video** → `04_Video/Folge_02_Pilze_im_Herbstwald_Storyboard_Video-v001.mp4` aus dem Manifest `Folge_02_Pilze_im_Herbstwald_manifest.json` (Skript `build_episode_video.py` im Root). Jede Szene wird exakt so lange gezeigt wie geplant; oben links Szenen-ID und Zeitstempel, unten Sprecher und gesprochener Text.

## Nachvollziehbarkeit
- `jobs_01_objekte_und_karl.json`, `jobs_02_neue_orte_flow.json`, `jobs_03_szenen_flow.json` + zugehörige `.log`: alle Flow-Prompts und Laufzeiten.
- Pro Szene liegt die Blender-Datei bei; Positionen/Posen in `build_folge02_szenen.py` ändern und einzelne Szenen neu rendern: `blender -b <Basis.blend> --python build_folge02_szenen.py -- haus|wald SH010 …`

## Bekannte Schwächen (für die Korrektur)
- Kleidung bleibt laut Regel die Standard-Kleidung; im November-Wald wären Jacken realistischer.
- Flow interpretiert Mimik/Gesten frei; Zungenrausstrecken (SH170/SH180) und Gesichtsausdrücke bitte prüfen.
- Das Blender-Auto ist ein offenes Klötzchen-Modell (ohne Scheiben), damit Innenraum-Kameras funktionieren.

## Korrekturrunde 1 (2026-11-04, User-Rückmeldung)
1. **SH020 Flur:** Treppe war verformt, Figuren winzig → neue, nähere Kamera im Flur (Mockup `SH020_blender.png` neu), Flow-Bild neu.
2. **Knollenblätterpilz an eigene Stelle:** Der Giftpilz steht nicht mehr an der Pfifferling-Lichtung, sondern an einer eigenen Stelle östlich des Waldwegs (Mooshügel unter einer Birke, Stein, Ast). Neue wiederverwendbare Kameras `WALD_CAM_06_Giftpilz_Stelle_Nah` und `WALD_CAM_07_Giftpilz_Stelle_Totale`; `FLOW_WALD_CAM_05` ohne weißen Pilz neu erzeugt. SH120/SH130 dort neu gebaut.
3. **SH110:** Mama zeigt jetzt mit dem Finger direkt auf die Pfifferlinge (neue Pose `point_down` in der Bibliothek).
4. **Tageszeit ab 1:40 (SH190–SH220):** Abend, draußen Nacht – alle Küchenbilder neu mit dunklen Fenstern und warmem Lampenlicht. Tageszeit-Abschnitt im Szenenplan ergänzt.
5. Abgelehnte Fassungen liegen in `03_Szenen_Flow_Bilder/rejected/` (`*_v001.jpg`). Video neu als `-v002.mp4`.
Jobs: `jobs_04a_orte_korrektur.json`, `jobs_04b1_szenen_haus.json`, `jobs_04b2_szenen_wald.json` (+ Logs).

## Runde 2 (2026-11-04): Start- und Endbild je Szene
- Jede der 22 Szenen hat jetzt ein **Startbild (A)** und ein **Endbild (B)**: `02_Szenen_Blender_Mockups/SHxxxA_blender.png` / `SHxxxB_blender.png` (+ `blend/`), Skript `build_folge02_szenen_AB.py`; Flow-Bilder `03_Szenen_Flow_Bilder/SHxxxA.jpg` / `SHxxxB.jpg` (Jobs `jobs_05_start_ende.json`, Generator `make_jobs_05_start_ende.py`).
- Referenzen je A/B-Bild: das A/B-Mockup (Layout) **plus das freigegebene Einzelbild der Szene** (Look, Licht, Tageszeit), dazu Modelsheets, Objekt-Sheets, Raumszene.
- Video `04_Video/…-v003.mp4` aus `Folge_02_Pilze_im_Herbstwald_manifest_v003.json` (`make_manifest_v003.py`): erste Szenenhälfte Startbild, zweite Hälfte Endbild; Dialogfenster unverändert.
- Die Einzelbilder `SHxxx.jpg` (v002) bleiben als Referenz liegen.

## Neue Assets für Staffel 1 nach Charakterbibel v2.1 (2026-11-05)
- **Tunnel am Waldrand** im `Herbstwald_Blockout.blend` (Collection `04_Tunnel_am_Waldrand`, Durchlass unter dem Feldwegdamm westlich des Parkplatzes, 1,30 m hoch, 12 m lang). Kameras `TUNNEL_CAM_01` Eingang Kinderaugenhöhe, `_02` innen zum Ausgang, `_03` Ausgang von der Wiese, `_04` Totale vom Parkplatz – je als Blender-Screenshot und leere Flow-Raumszene `FLOW_TUNNEL_CAM_0x.jpg`. Nur Tunnel-Kameras neu gerendert (`RENDER_ONLY=TUNNEL_CAM`); WALD_CAM-Bilder unverändert.
- **Modelsheets Lea (11) und Timo (12)** in `02_Charaktere_Steckbriefe_und_Bilder/`, Karl dort als `10_` ergänzt. Erster Prompt vom Google-Filter abgelehnt (vermutlich Körper-/Kleidungsbegriffe bei Kindern, z. B. „Leggings", „schlaksig", „rundlich und weich"); neutral umformuliert → `jobs_06b_lea_timo_retry.json`.

## Runde 3 (2026-11-05): Flur neu + Bildnummern
- Der Flur ist komplett neu: die Treppe im Haus-Blockout ist repariert, und es gibt 5 neue Flur-Kameras und Referenzbilder in `11_Flur_Neu_Treppe_Blender_und_Flow/`.
- SH020, SH020A und SH020B sind neu gemalt; die alten Fassungen liegen in `03_Szenen_Flow_Bilder/rejected/`.
- Video **v004** hat oben rechts eine gelbe Nummer „Bild NN“ auf jedem Bild. Die Zuordnung steht in `04_Video/…-v004_Bildliste.md`.

## Runde 4 (2026-11-05): Kritik zu v004 (Bilder 13, 15, 19–22, 27, 30–32, 37, 38, 41)
- **Verzerrte Gesichter:** Ursache waren zu kleine Figuren. Die Mockup-Kameras für SH070, SH080, SH140, SH150, SH160, SH190, SH210 und SH220 sind jetzt nah, die Gesichter zeigen zur Kamera, und jeder Prompt hat einen Gesichts-Satz.
- **A/B-Paare:** Die Endbilder sind mit dem fertigen Startbild als Referenz 2 neu gemalt. Das betrifft SH100B und SH110B (Papa neu) und alle neu gemachten Paare.
- **Esstisch:** Die Sitzordnung ist fest: eine Längsseite, links Maxi, Mitte Mama, rechts Papa. Bei SH200 und SH220 ist die Flurtreppe im Durchgang jetzt korrekt.
- **SH160:** Maxi sitzt hinten am Fenster und ist erkennbar. Das Auto ist der Kombi OBJ_05; die Käfer-Fassung mit Gesicht liegt in `rejected/`.
- **Offen:** SH160B wurde wegen Speichermangel abgebrochen. In v005 steht SH160A für die ganze Szene; dadurch rutschen die Bildnummern ab Bild 32 um eins nach vorn.
- **Generator:** `make_jobs_08_runde4.py`. Die alten Bilder liegen in `03_Szenen_Flow_Bilder/rejected/`, die alten Mockups in `02_…/rejected/`.

## Runde 5 – 2026-11-05 (Kritik zu Video v005)

| Bild | Kritik | Ursache | Änderung |
|---|---|---|---|
| 30 (SH150B) | Mama steigt in den Kofferraum, Auto steht schräg | Mockup-Kamera sah das Auto schräg; Flow malte Straßenkante + Heck-Tür | Neue Kamera `CAM_150S` exakt seitlich, Auto parallel zum Bildrand, Front rechts; B: alle Türen zu, Mama an der **vorderen Beifahrertür**, Papa geht vorn herum; Prompt-Block `AUTO` (gerade, Schotter, kein Bordstein, niemand am Heck). A (Bild 29) mit neu, weil B daraus entsteht. Auto jetzt wieder exakt OBJ_05 (der alte Passat-artige Wagen war modellfremd). |
| 36/37 (SH190A/B) | Küchen-Architektur stimmt nicht | Mama schnitt an einer erfundenen Arbeitsplatte; im Blockout hing `KU_Oberschrank_1` vor dem Westfenster | Blockout repariert (Oberschrank auf y 1,52–1,98 gekürzt, Backup `…_vor_Oberschrankfix_2026-11-05.blend`); neue Kamera `CAM_190S` vom WZ-Durchgang; Mama steht am **echten Esstisch**; Prompt-Block `KUECHE` (L-Zeile nur an West- und Nordwand, keine Insel, keine Hängelampen) + FLOW_CAM_09 als zusätzliche Raumreferenz. |
| 43 (SH220B) | Küchen-Architektur stimmt nicht | Flow malte Oberschränke/Hängelampen an die Terrassen-Rückwand | Prompt-Block `ESS` (Rückwand: Spülenzeile links, Schiebetür hinter Mama/Papa, rechts schlichte Wand, keine Oberschränke) + SH200A als Raumreferenz; A (Bild 42) mit neu. |

Dateien: `make_jobs_09_runde5.py`, `jobs_09_runde5_welle1/2.json`, Logs `jobs_09_welle1/2.log`; alte Fassungen `03_Szenen_Flow_Bilder/rejected/*_r4.jpg`, alte Mockups `02_…/rejected/*_blender_r4.png`, Skript-Backup `build_folge02_szenen_AB_vor_Runde5.py.bak`.
Video: `04_Video/Folge_02_Pilze_im_Herbstwald_Storyboard_Video-v006.mp4` (+ `_Bildliste.md`), Bildnummern unverändert gegenüber v005. SH160B weiterhin offen.

## Runde 6 – 2026-11-05 (Veo/Flow-Dialog-Regeln STRIKT, Kritik „falsche Person spricht, Timing falsch“)
- Regeln gespeichert: Gedächtnis `veo-flow-dialog-regeln`, Skill-Entwurf Abschnitt 1 + neuer Abschnitt 6b.
- Szenenplan SH010–SH050 → 7 Einstellungen mit je EINEM Sprecher (SH010 Mama, SH011 Maxi, SH020 Papa, SH030 Mama, SH040 Karl, SH050 Maxi, SH051 Mama), Sprecher groß/halbnah/frontal, kurze Zeilen mit Zeitfenster (Drehbuch „Runde 6“).
- Blender: neue Kameras `CAM_010…CAM_051` in `build_folge02_szenen_AB.py` (Backup `…_vor_Runde6.py.bak`), 14 Mockups; alte nach `02_…/rejected/*_blender_r5.png`.
- Flow: `make_jobs_10_runde6.py` → `jobs_10_runde6_welle1/2.json` (A, dann B mit A als Referenz 2); SH030B einmal neu (Korb war voller Pilze → `rejected/SH030B_r6_voller_Korb.jpg`, `jobs_10b_sh030b.json`). Alte Bilder `03_…/rejected/*_r5.jpg`.
- Videos: `04_Video/Folge_02_Anfang_SH010-SH051_Untertitel-r6.mp4` (39 s) und `04_Video/Folge_02_Pilze_im_Herbstwald_Storyboard_Video-v007.mp4` (131 s, 57 Bilder; Untertitel nur im Sprechfenster, davor stumm). Manifeste `…_manifest_r6.json`, `…_manifest_v007.json`.
- Nebenbei: Flur im Raumszenen-PDF + REF_07 erneuert (siehe `11_Flur_Neu_Treppe_Blender_und_Flow/00_VERMERK_Flur_neu.md`); Charakterbibel v2.1 als Standard gemerkt.

## Runde 7 – 2026-11-05: komplette Flow-Fassung
- Spracherkennung installiert (`.venv_sprache`, faster-whisper large-v3-turbo) + Skripte `sprache_abschreiben.py`, `flow_clips_schneiden.py` (Korrekturmappe-Root).
- Restliche Folge SH060–SH220 als Flow-Videos (Ein-Sprecher-Regel, neue Sprecher-Startbilder SH090S/120S/130S/190S/191S/200S), Details `04_Video/07_Flow_Szenenvideos_Rest_r7/00_VERMERK_Flow_Szenenvideos_r7.md`.
- Zusammenschnitt `04_Video/08_Flow_Folge_komplett/Folge_02_Pilze_im_Herbstwald_Flow_v001.mp4` (109 s).

## Thumbnail + Social Media – 2026-11-06
- Texte für TikTok/YouTube (Titel, Beschreibung, je 10 Hashtags, Hinweise „Für Kinder“ und KI-Kennzeichnung): `04_Video/08_Flow_Folge_komplett/social_media.md`.
- Thumbnail-Hintergründe in Flow ohne Schrift (`05_Thumbnail/jobs_13_thumbnail.json`, Log `jobs_13.log`): Maxi mit Riesen-Steinpilz und vollem Korb, Karl verdutzt hinterm Baum. 16:9 (`Thumbnail_Hintergrund_16x9.jpg`) und 9:16 (`Thumbnail_Hintergrund_9x16.jpg`). Das 9:16-Bild ist im Log als „fail“ markiert, weil das Bildwerkzeug höchstens 3 Referenzen nimmt (Maxi, Karl, Waldweg). Korb und Pilze kamen nur aus dem Text; geprüft, stimmen mit OBJ_01–03 überein → verwendet.
- Logo, Titel „PILZE IM / HERBSTWALD!“ und Plakette „FOLGE 2“ mit neuem Root-Skript `thumbnail_bauen.py` (`--format quer|hochkant`) → `05_Thumbnail/Folge_02_Pilze_im_Herbstwald_Thumbnail_YouTube_1280x720.jpg` und `…_Cover_TikTok_1080x1920.jpg`.
- Bildprüfung: Maxi (gestreiftes Shirt, Jeans) und Karl (oranger Hoodie, schwarze Stachelhaare) wie Modelsheets, Gesichter sauber, Titel überdeckt keine Gesichter.
