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

## Runde 4 – 2026-11-06: Überarbeitung nach Kritik am Mockup-Video v001 → v002
Ursachen-Tabelle (Bild-Nummern aus v001 → Änderung; **die Nummern in v002 haben sich verschoben**, siehe `…v002_arbeit/bild_Bildliste.md`):

| Bild (v001) | Kritik | Änderung |
|---|---|---|
| vor 1 | Ankunft fehlt: Auto parkt, Mama begrüßt, Frieda nimmt das Kinderzimmer | neu SH001 (Auto parkt, Frieda winkt im Beifahrersitz), SH002 (Mama: „Frieda! Wie schön, dass du da bist!“), danach SH010 (Frieda: „Ich nehm das Kinderzimmer!“) |
| 3 | Papa steht im Auto, muss links daneben stehen; Kamera Richtung Straße, Papa im Vordergrund | SH030 neue Kamera vom Haus Richtung Straße: Papa links im Vordergrund, Koffer, Frieda frontal dahinter |
| 4/5 | Dialog flach | SH040 Frieda „Oh, ihr habt einen neuen Teppich!“, neu SH042 „So etwas ist doch viel zu teuer.“, SH041 Mama verlegen: „Ähm, nein. Der war im Angebot. Hehe.“ (eine Lüge) |
| 6/7 | Ablauf anders: Frieda kommt rein, Hasi liegt auf dem Bett, Blick vom Bett, Maxi hinter ihr | neu SH047 (Frieda kommt rein), SH048 (Hasi auf dem Bett), SH050 (Blick vom Bett: „Und das Kuscheltier kommt raus.“), SH051 (Maxi hinter Friedas Rücken: „Das ist kein Kuscheltier. Das ist Hasi!“) |
| 8 | „Du kommst hier hin“ zum Papagei fehlt | neu SH058 (Frieda stellt den Käfig auf den Nachttisch) |
| vor 9/10 | Maxi spielt draußen mit Ball, Anna ruft von weitem, Maxi geht hin | neu SH065 (Ball), SH070 (Anna ruft, jetzt „von weitem“), neu SH075 (Maxi geht zum Tor), danach SH071 (Glitzerstein) |
| 12 | Schleichmusik, Sprüh-Effekt | Musik_03 (Gemini Lyria) in SH080–SH081 und SH124–SH130; Sprüh- und Papagei-Effekt (ElevenLabs) in SH081 |
| vor 14 | Frieda muss erst ins Zimmer kommen | neu SH089 (Tür, Schritte) |
| – | „Keiner ruft an“ weg | SH172 gestrichen (Mockup nach `rejected/`); SH173 bleibt als Blick auf den traurigen Maxi; SH183 „Und ich ruf an“ bleibt als freundliche Geste |

- **Stimmen:** neu erzeugt SH002, SH040, SH041, SH042, SH058, SH070 (Whisper OK, SH041 0,92); die alten Fassungen liegen in `04_Video/00_Stimmen_TTS/rejected/`.
- **Mockups:** 57 Einstellungen (`build_frieda_szenen.py`), Blockout-Hasi wird in Szenen ohne Hasi auf dem Bett ausgeblendet.
- **Ton (User-Vorgabe):** Soundeffekte **nur** mit ElevenLabs (`../sfx_elevenlabs.py`, Key `~/.elevenlabs_key`), Musik **nur** mit Gemini Lyria über das Chrome-Plugin. Die ElevenLabs-Music-API ist für Free-Konten gesperrt und war ohnehin nicht gewünscht. Effekte: Auto parkt (SH001), Koffer (SH030), Tür und Schritte (SH047, SH089), Ball (SH065), Sprüher und Papagei (SH081), Papagei (SH093), Auto fährt weg (SH190), Bett (SH200), Dose klackt (SH201).
- **Video:** `04_Video/Folge_Tante_Frieda_Mockup-Vorschau-v002.mp4` (5:41 min, 57 Einstellungen, 47 Stimmen, Bilder nummeriert). Tonprüfung: Musik liegt hörbar unter SH080–SH081, Spitzenpegel −0,3 dB.
- **Flow-Szenenbilder:** weiter **nicht** gemalt, sie warten auf die Freigabe von v002.

## Runde 5 – 2026-11-06: Kritik am Video v002 → Haus texturiert, Szenen überarbeitet, Video v003
Die Bild-Nummern der Kritik beziehen sich auf v002; in v003 haben sie sich erneut verschoben (`…v003_arbeit/bild_Bildliste.md`).

| Bild (v002) | Kritik | Änderung (v003-Nr.) |
|---|---|---|
| 1 | Frieda neben dem Auto mit offener Tür sichtbar, Papa raus | SH001 (Bild 1): Frieda steht an der offenen Beifahrertür, nur Mama und Bello warten, Papa nicht im Bild; Maxi ist jetzt oben im Haus |
| 3 | Frieda freut sich beim Kofferraum-Öffnen, hält den Papagei im Arm, nimmt das Kinderzimmer | neu SH003 (Bild 3): „Ich freue mich auch, hier zu sein!“ mit Kofferraum; SH010 (Bild 4): Käfig im Arm, „Und ich nehme das Kinderzimmer!“ |
| 4 | Maxi schaut aus dem Fenster und hat heimlich gehört | SH020 (Bild 5): Kamera von der Einfahrt hoch zum Kinderzimmerfenster, Maxi flüstert „Mein Zimmer?! Bis heute Abend ist die weg.“ |
| nach 5 | Papa stöhnt wegen des Koffers; Papa steht links im Vordergrund, Kamera Richtung Straße | SH030 (Bild 6): neue Kamera; neu SH032 (Bild 7): „Uff! Was ist da bloß drin? Steine?“ (Stöhnen) |
| 7 | Gesicht der Tante nicht richtig sichtbar, Aufstellung im Flur | SH040/SH042/SH041 (Bild 8–10): **feste Aufstellung** (Frieda vorn, Mama dahinter), nur die Kamera wechselt. Meine Lesart „in Richtung Flur“: Frieda steht tiefer im Flur und schaut in den Flur, die Kamera sieht ihr Gesicht frontal. |
| 11 | Kamera tiefer, Hasi auf Hüfthöhe | SH050 (Bild 13): Kamera vom Bett aus, Hasi auf Hüfthöhe |
| 4/13 | Maxi nimmt eingeschnappt den Hasen, dann „Und Lorchen kommt hier hin“, Nachttisch im Vordergrund | neu SH052 (Bild 15); SH058 (Bild 16): Nachttisch vorn, Frieda stellt den Käfig ab |
| 21/22 | Frieda und Kamera weg von der Eingangstür; Bild 22 groß auf die Tür; danach Käfig im Vordergrund, Tante gebeugt: „Oh nein, was ist denn mit dir passiert?“ | SH089 (Bild 25) groß auf die Tür; SH090 (Bild 26): Käfig im Vordergrund, Frieda gebeugt, neue Zeile; SH091 (Bild 27) Übersicht mit Frieda; SH089–SH094 teilen eine Aufstellung (Kamera wechselt). Für „Bild 21“ bin ich von SH089 ausgegangen. |
| – | Vogel nie richtig zu sehen, Käfig größer | Käfig und Papagei neu modelliert (0,95 m, 24 Stäbe, Kuppel, Ring, Napf; Papagei mit Augen, Hakenschnabel, Flügeln) |
| – | Dialoge einmal aufbauen, nur Kamera wechseln | Skill `dialog-szenen-inszenieren` und Hinweis in `maxi-folge-erstellen`; alle Dialoge (Flur, Zimmer, Garten, Opa/Frieda, Abschied) mit fester Aufstellung neu gebaut |
| – | Haus mit Flow-Texturen, UV, Details; alle Screenshots neu; dauerhaft speichern | siehe `../03_Blender_3D_Haus_Blockout/00_VERMERK_Texturierung.md`; alle 60 Mockups mit dem texturierten Haus neu gerendert |

- **Neuer Ton:** Soundeffekte Autotür, Kofferraum und Fenster (ElevenLabs), Cues in `04_Video/01_Ton/ton_r3.json`. Neue Stimmen: SH003, SH010, SH020 (flüsternd), SH032 (stöhnend), SH058, SH090; alte nach `00_Stimmen_TTS/rejected/`.
- **Szenenplan r3:** 60 Einstellungen, 5:48 min (`szenenplan_r3.json`).
- **Video:** `04_Video/Folge_Tante_Frieda_Mockup-Vorschau-v003.mp4` (5:58 min mit Intro/Titel, Spitzenpegel −0,3 dB).
- **Bekannte Schwächen:** SH020 (Maxi im Fenster) ist klein und sein Gesicht nur ein Punktpaar; SH001 zeigt die Autotür nur als Platte; Flur-Dialog „in Richtung Flur“ nach eigener Lesart; Papa-Stöhnen ist ein gesprochenes „Uff!“ (TTS), noch kein Stöhn-Effekt.
- **Flow-Szenenbilder:** weiter nicht gemalt, warten auf Freigabe von v003.

## Runde 6 – 2026-11-06: Kritik am Video v003 → neue Geschichte ab dem Streich, neues Ende, Video v004
Bild-Nummern der Kritik = v003. Szenenplan `szenenplan_r4.json` (65 Einstellungen, 6:06 min); v004 hat wieder neue Nummern (`…v004_arbeit/bild_Bildliste.md`).

| Bild (v003) | Kritik | Änderung |
|---|---|---|
| 2 | Mama breitet die Arme auseinander statt hoch | neue Pose `open` (SH002) |
| 3/4 | Frieda kühl, blickt zum Kofferraum und holt etwas heraus; Bild 4 = Bild 3 mit geschlossenem Kofferraum und Käfig in der Hand | SH003 (kühle Stimme, Blick zum Kofferraum, Käfig), SH010 gleiche Kamera, Kofferraum zu, Käfig in der Hand |
| 5 | Schock-Effekt, Geigen/gedämpfte Trompete | Gemini-Lyria-Track `Musik_04_Schock_The_Tiptoe_Retreat.mp3`, die ersten 4,2 s als Akzent bei SH020 (ob der Anfang wirklich wie ein Schock klingt, habe ich nicht gehört) |
| 8, 9, 10 | Frieda hält den Käfig auch im Flur | SH040/042/041 mit Käfig im Arm |
| 11/12 | Closeup, Tür hinter sich schließen; Hasi deutlich auf dem Bett, Schritte | SH047 Closeup (Tür-Effekt), SH048 großes Hasi auf dem Bett, Schritte-Effekt |
| 14 | Closeup Maxi, böser Blick | SH051 Closeup mit Augenbrauen `angry` (neu in der Lib) |
| 15/16 | Maxi: „Gib ihn mir!“; Frieda: „Naja, Lorchen kommt hier hin, sei bitte nett zu ihm.“ | SH052 (Maxi spricht, nimmt Hasi), SH058 neue Zeile |
| 18 | Vogelgeräusche | Effekt `vogel_garten` (ElevenLabs) unter SH065–SH072 |
| 20/21 | Maxi von vorn: „Das ist meine Tante …“; Anna schlägt einen Streich vor | SH075 (Maxi frontal, enttäuscht), SH071 („Dann spielen wir ihr einen Streich!“), SH072 („Gute Idee! Achtung Crew, Mission!“) |
| 23–29 | Streich: Maxi versteckt den Vogel im Schrank, springt aufs Bett; Frieda kommt neugierig herein, sieht den leeren Nachttisch, erschrickt, „Oje, wo ist Lorchen?“; Lorchen ruft aus dem Schrank; „Da ist er ja!“ (Kamera im Schrank); „Wer könnte das wohl gewesen sein?“; Lorchen: „Maxi hat mich versteckt!“; Maxi rennt raus; „Ich glaube, du bleibst jetzt lieber erstmal bei mir.“ | neu SH080–SH087, SH089–SH095, SH094; eigener Kleiderschrank `prop_wardrobe` zum Öffnen; Lorchens Ruf aus dem Schrank (Tiefpass, SH087: „Hilfe! Ich bin im Schrank!“, der Wortlaut ist von mir) |
| 31 | Frieda Ellbogen auf dem Tisch, Kaffee trinken | neue Pose `sip` (SH101) |
| 42/43 | Maxi verkneift sich das Lachen | neu SH145 (Closeup, Kichern-Effekt) |
| 46 | „Und ich hab auch den Vogel versteckt“ | SH152 neue Zeile |
| 48 | Papa mit Koffer besser sehen | SH170 neue Kamera |
| ab 50 | Neues Ende | SH174/175 Papa auf der Treppe neben Maxi, SH177/178 Entschuldigung, SH179 Frieda lenkt ein, SH184 Lorchen, SH186 alle lachen im Wohnzimmer (Lachen-Effekt, Musik_02) |

- **Neue Lib-Funktionen** (`maxi_blender_lib.py`): Posen `open`, `sip`, `face`, `lie`; `mood` (angry, startled, suspicious, sad) als Augenbrauen; `prop_wardrobe`.
- **Neuer Ton:** Effekte (ElevenLabs) Schritte, Tür zu, Vogelgezwitscher, Schrank auf/zu, Keuchen, Kichern, Lachen, Rennen; Schleichmusik (Musik_03) jetzt für SH080–SH087; Musik_02 im Finale; Cues `04_Video/01_Ton/ton_r4.json`.
- **Stimmen neu:** SH003 (kühl), SH052, SH058, SH071, SH072, SH075, SH086, SH087, SH090, SH091 (jetzt Frieda), SH093, SH095, SH094, SH152, SH174, SH175, SH177, SH178, SH179; Whisper-geprüft.
- **Video:** `04_Video/Folge_Tante_Frieda_Mockup-Vorschau-v004.mp4` (6:16 min mit Intro/Titel).
- **Licht (separat, auf Wunsch):** `03_Blender_3D_Haus_Blockout/licht_haus.py`, Raumbilder in `Raumbilder_Licht/`. Die Mockups von v004 sind noch mit dem alten (hellen, schattenlosen) Eevee-Look gerendert.
- **Offen/Schwach:** SH075 Maxi klein im Bild; Mockup-Gesichter bleiben Punkte; Stöhnen und Lachen sind Effekte aus ElevenLabs und TTS, kein Schauspiel; Flow-Szenenbilder weiter nicht gemalt.

## Runde 7 – 2026-11-06: Kritik am Video v004 → Plan r5, Mockups mit Licht, Flow-Bilder (unterbrochen durch Kontingent)
Bild-Nummern der Kritik = v004. Szenenplan `szenenplan_r5.json` (70 Einstellungen).

| Bild (v004) | Kritik | Änderung |
|---|---|---|
| 10 | Zoom auf Mama beim Sprechen | SH041: Startbild weit, **Endbild = Zoom** auf Mama (`SH041_B`-Mockup) |
| 11 | Türrahmen sichtbar | Die Kinderzimmertür liegt an der Ostwand (x −1,25, y 0,4–1,6); ich hatte Frieda im Raum statt an der Tür platziert. SH047 jetzt im Türrahmen, Closeup |
| 21 | „Dann spiel ihr doch einen Streich“ + 2 Bilder | SH071 neue Zeile, neu SH073 (Maxi), SH074 (Anna: „Versteck doch ihren Vogel!“) |
| 23 | Maxi steht im Käfig | SH080: Käfig neben Maxi auf dem Boden |
| 25 | Maxi rennt Richtung Bett; Tür, Rahmen, Texturen, Licht | SH082 rennt (Endbild springt aufs Bett); SH089 mit Tür und Rahmen; Mockups jetzt mit warmem Licht (Licht-Blend) |
| überall | lange Pausen ohne Ton abschneiden | `hoerstoryboard_bauen.py --kuerzen` (Szene = Sprache + 0,55 s bzw. Effekt; stumme Szenen ≥ 2,5 s): Szenenzeit 6:06 → ca. 4:08 min |
| vor 39 | Opa klingelt von draußen | neu SH109 + Klingel-Effekt |
| 48, 51 | Vogel nicht richtig im Bild | SH141/SH144 Kamera auf den ganzen Käfig. „Bild 51 auch nicht vom Vater“ habe ich nicht eindeutig verstanden: Ich habe SH170 (Papa mit Koffer) zusätzlich näher gerückt |
| 54 | komplett weg | SH152 gestrichen |
| 56/58 | Abschieddialog; Tante verabschiedet sich | neu SH165 (Mama), SH166 (Frieda), SH167 (Papa); SH173 Frieda: „Tschüss, Maxi. Sei schön brav.“ |
| – | Google-TTS-Spuren | neu: SH071, SH073, SH074, SH165, SH166, SH167, SH173 (Whisper-geprüft; SH074 klingt als „Versteckt“) |

- **Mockups:** 72 (70 + `SH041_B`, `SH082_B`). Die ersten 17 mit Cycles und Licht, der Rest mit Eevee (Cycles brauchte ~100 s je Bild).
- **Flow-Bilder:** `make_jobs_flow.py` (A = Startbild, B = Endbild, je halbe Szenenzeit) und `flow_treiber.py`. **Fertig: 18 Bilder** (Start+Ende für SH001, SH002, SH003, SH010, dazu Startbilder SH020, SH030, SH032, SH040, SH041, SH042, SH047, SH048, SH050, SH051). Danach **brach die Bildgenerierung mit „Individual quota reached“ (HTTP 429, Reset in ca. 151 h) ab.** Treiber und Läufe sind gestoppt, nichts läuft mehr.
- **Ton:** Klingel-Effekt neu, Cues müssen für r5 noch in `ton_r5.json` (Rest übernehmbar aus `ton_r4.json`).
- **Offen:** Flow-Bilder für die übrigen Szenen (Kontingent), Flow-Video, Hochkant-Version (wartet auf den Abschluss dieses Auftrags).
- **Videos (Stand Ende Runde 7):** `04_Video/Folge_Tante_Frieda_Mockup-Vorschau-v005.mp4` (alle 70 Szenen als Blender-Mockup mit Licht, gekürzte Pausen, 4:37 min) und `04_Video/Folge_Tante_Frieda_Flow-Vorschau-v001_teilweise.mp4` (A/B-Bildpaare je halbe Szenenzeit; nur SH001–SH010 mit Flow-Bildern, sonst Mockup als Ersatz; 184 nummerierte Bilder).
- **Mockup-Fehler gefunden und behoben:** SH041_B war leer, weil die Kamera in Friedas Körper stand (jetzt zwischen Frieda und Mama).
