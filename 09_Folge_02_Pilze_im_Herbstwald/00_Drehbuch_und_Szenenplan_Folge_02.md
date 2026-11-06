# Maxi Cartoons – Folge 02: „Pilze im Herbstwald“

**Datum der Geschichte:** 4. November – ein goldener Herbsttag, bunte Blätter, Pilzzeit.
**Erstellt:** 2026-11-04, eigenständig ohne Komitee. Vorlage zur Korrektur.
**Figuren (nur 4):** Maxi (5), Mama Katrin, Papa Thomas, **Karl** (neu: „der fiese Karl“, 8 Jahre, Nachbarsjunge vom Ende des Ahornwegs, fährt ein schwarz-oranges BMX-Rad).
**Kleidung:** Alle Figuren tragen ihre Standard-Kleidung von den Modelsheets (Vorgabe: Kleidung ändert sich nie).
**Spielzeit:** 22 Szenen, 120 s reine Szenenzeit (+ Titel 3 s, Ende 2 s). Erlaubt wären bis 5 min.

## Kurzfassung
Mama, Papa und Maxi wollen im Wald Pilze sammeln. Auf dem Weg zum Auto radelt der fiese Karl vorbei: „Ihr findet eh nichts, hehe!“ Im Herbstwald finden sie aber Steinpilze und Pfifferlinge. Maxi entdeckt einen schönen weißen Pilz – Mama stoppt ihn: Das ist ein Knollenblätterpilz, giftig, den darf man nie essen! Auf der Heimfahrt sieht Maxi Karl aus dem Autofenster, hebt den vollen Korb hoch und streckt die Zunge raus. Zuhause kochen sie eine Pilz-Sahnesauce, essen Nudeln und sind glücklich.

## Objekte (vorab in Flow erzeugt, `00_Objekt_Referenzbilder_Props/`)
| ID | Objekt | Wer hält es / wo |
|---|---|---|
| OBJ_01 | Brauner Weiden-Pilzkorb mit Bügelgriff | Maxi (meist), Papa (SH020) |
| OBJ_02 | Steinpilz (brauner Hut, dicker heller Stiel) | Maxis Fund SH090/SH100, Korb |
| OBJ_03 | Pfifferlinge (gelbe Büschel im Moos) | Mamas Fund SH110 |
| OBJ_04 | Grüner Knollenblätterpilz (weiß-grünlich, Ring, Knolle) | bleibt im Wald stehen SH120/SH130 |
| OBJ_05 | Blaues Familienauto (Kombi) | SH030–SH070, SH150–SH180 |
| OBJ_06 | Karls schwarz-oranges BMX-Fahrrad | Karl SH040, SH160, SH180 |
| OBJ_07 | Pfanne mit Pilz-Sahnesauce + Holzlöffel | SH190 |
| OBJ_08 | Teller Bandnudeln mit Pilzsauce und Petersilie | SH200–SH220 |

## Neue Orte (in Blender modelliert, `01_Neue_Orte_Blender_und_Flow/`, wiederverwendbar)
| Kamera | Ort |
|---|---|
| WALD_CAM_01 | Landstraße zum Waldrand (Auto fährt) |
| WALD_CAM_02 | Waldparkplatz am Waldrand mit Holzschild |
| WALD_CAM_03 | Waldweg im Herbstwald, Totale |
| WALD_CAM_04 | Waldweg Nah: Baumwurzel mit Steinpilz (Kinderaugenhöhe) |
| WALD_CAM_05 | Pilzlichtung mit moosigem Baumstumpf (nur Pfifferlinge) |
| WALD_CAM_06 | Giftpilz-Stelle Nah: Mooshügel unter einer Birke abseits des Wegs (Knollenblätterpilz) |
| WALD_CAM_07 | Giftpilz-Stelle Totale vom Waldweg |
| KOM_CAM_39 | Einfahrt mit Familienauto, Blick zur Straße (Haus-Blockout, neue Kamera) |
| AUTO_CAM_01 | Auto-Innenraum, Rückbank, Blick aus dem Seitenfenster |

## Tageszeit (verbindlich für das Licht)
- SH010–SH050: Vormittag, helles Tageslicht.
- SH060–SH150: Nachmittag im Wald, ab SH120 späte Nachmittagssonne mit langen Schatten.
- SH160–SH180: Heimfahrt in der Abenddämmerung (goldenes, tiefes Licht).
- **SH190–SH220: Abend, draußen ist es NACHT** – alle Fenster dunkel, nur warmes Küchenlicht.

## Szenenplan (Dauer je 4 / 6 / 8 s, Dialog mit Zeitfenster)
| Szene | Dauer | Ort / Kamera | Bild | Dialog |
|---|---|---|---|---|
| SH010 | 6 s | Küche, KOM_CAM_09 | Morgens. Mama stellt den leeren Pilzkorb auf den Tisch, Maxi hüpft am Tisch, Papa in der Terrassentür. | 0–3 s MAMA: „Heute gehen wir Pilze sammeln im Wald!“ · 3–6 s MAXI: „Jaaa! Ich finde den allergrößten!“ |
| SH020 | 4 s | Flur, Kamera nah (KOM_CAM_15-Achse) | Maxi mit Korb an der Haustür, Papa mit Autoschlüssel, Mama kommt. | PAPA: „Alle einsteigen, der Wald wartet!“ |
| SH030 | 6 s | Einfahrt, KOM_CAM_39 | Die drei gehen zum blauen Auto, Papa öffnet die Tür. | 0–2 s – · 2–6 s MAMA: „Korb nicht vergessen, Maxi!“ |
| SH040 | 8 s | Einfahrt/Bürgersteig, KOM_CAM_39 | Karl radelt auf dem Bürgersteig vorbei, grinst frech. | 0–2 s – · 2–8 s KARL: „Pilze sammeln? Ihr findet eh nichts! Hehe!“ |
| SH050 | 4 s | Einfahrt Nah, KOM_CAM_39b | Maxi drückt den Korb an sich, Mama legt die Hand auf seine Schulter. | 0–2 s MAXI: „Der ist gemein!“ · 2–4 s MAMA: „Lass ihn reden. Wir zeigen’s ihm.“ |
| SH060 | 6 s | Landstraße, WALD_CAM_01 | Das blaue Auto fährt zwischen bunten Bäumen auf den Wald zu. | 0–3 s – · 3–6 s MAXI: „Sind wir bald da?“ |
| SH070 | 4 s | Waldparkplatz, WALD_CAM_02 | Auto geparkt, alle steigen aus, Maxi hält den Korb. | PAPA: „Da sind wir! Auf in den Wald!“ |
| SH080 | 6 s | Waldweg, WALD_CAM_03 | Die drei gehen den Waldweg entlang, Maxi vorneweg. | MAMA: „Schaut gut unter die Bäume, da verstecken sich die Pilze.“ |
| SH090 | 6 s | Baumwurzel, WALD_CAM_04 | Maxi kniet an einer Wurzel, vor ihm ein großer Steinpilz. | MAXI: „Mama! Papa! Ich hab einen! Ein Riesen-Pilz!“ |
| SH100 | 4 s | Baumwurzel, WALD_CAM_04 | Papa hockt neben Maxi, hält den Steinpilz, Maxi hält den Korb auf. | PAPA: „Ein Steinpilz! Der kommt in den Korb.“ |
| SH110 | 6 s | Pilzlichtung, WALD_CAM_05 | Mama kniet am Baumstumpf und zeigt mit dem Finger direkt auf die gelben Pfifferlinge, Maxi schaut zu. | MAMA: „Und hier: Pfifferlinge! Die sind lecker.“ |
| SH120 | 6 s | Giftpilz-Stelle, WALD_CAM_07 | Eigener Ort abseits des Wegs: Maxi steht auf dem Mooshügel und zeigt auf den weißen Pilz vor seinen Füßen; Eltern kommen vom Weg. | MAXI: „Guck mal, so ein schöner weißer!“ |
| SH130 | 8 s | Giftpilz-Stelle Nah, WALD_CAM_06 | Mama hält Maxis Hand zurück, ernstes Gesicht, der weiße Pilz bleibt stehen. | 0–5 s MAMA: „Stopp! Das ist ein Knollenblätterpilz. Der ist giftig, den darf man niemals essen!“ · 5–8 s MAXI: „Dann bleibt der hier stehen.“ |
| SH140 | 4 s | Waldweg, WALD_CAM_03 | Die drei gehen zurück, der Korb ist voll, alle fröhlich. | PAPA: „Der Korb ist voll. Zeit für Zuhause!“ |
| SH150 | 4 s | Waldparkplatz, WALD_CAM_02 | Maxi steigt mit dem vollen Korb ins Auto, Papa hält die Tür. | MAXI: „Ich halte den Korb fest!“ |
| SH160 | 6 s | Ahornweg, KOM_CAM_39 | Das Auto fährt in die Straße, auf dem Bürgersteig radelt Karl. | 0–3 s – · 3–6 s MAXI: „Da ist Karl!“ |
| SH170 | 6 s | Auto-Innenraum, AUTO_CAM_01 | Maxi auf der Rückbank hebt den vollen Pilzkorb ans Fenster und streckt die Zunge raus. | MAXI: „Bäääääh!“ |
| SH180 | 4 s | Bürgersteig, KOM_CAM_39c | Karl auf dem Rad, Mund offen, verdutzt; im Autofenster Maxi mit Korb. | KARL: „Hä?!“ |
| SH190 | 6 s | Küche, KOM_CAM_31 | Papa rührt die Pfanne am Herd, Mama schneidet Pilze, Maxi wäscht auf dem Tritthocker Pilze in der Spüle. | 0–3 s MAMA: „Die Pilze schneiden wir klein …“ · 3–6 s PAPA: „… und ab in die Sahnesauce!“ |
| SH200 | 6 s | Küche Esstisch, KOM_CAM_10 | Drei Teller Nudeln mit Pilzsauce, alle sitzen am Tisch. | MAXI: „Mmmh! Nudeln mit unseren Pilzen!“ |
| SH210 | 6 s | Esstisch Nah, KOM_CAM_09 | Maxi mit aufgewickelten Nudeln auf der Gabel, Eltern lachen. | PAPA: „Und Karl? Der hat nur Luft gefunden!“ |
| SH220 | 4 s | Esstisch, KOM_CAM_10 | Alle drei heben die Gabeln, Abendlicht durch die Terrassentür. | MAMA: „Guten Appetit, ihr Pilzsucher!“ |

**Gesamt:** 120 s Szenen + 5 s Karten = 125 s.

## Runde 6 (2026-11-05): SH010–SH050 nach den Veo/Flow-Dialog-Regeln neu (ersetzt die Zeilen SH010–SH050 oben)
Regeln: eine Einstellung = EIN Sprecher; Sprecher groß, halbnah, frontal; kurze Zeile mit Zeitfenster; alle anderen still.

| Einstellung | Dauer | Ort / Kamera | Bild (A → B) | Sprecher | Dialog (Zeitfenster) |
|---|---|---|---|---|---|
| SH010 | 4 s | Küche, `CAM_010` (Mama frontal hinter dem Esstisch) | Mama hält den leeren Korb → hebt ihn hoch; Maxi sitzt links (still) | MAMA | 0,5–3,5 s „Heute gehen wir Pilze sammeln im Wald!“ |
| SH011 | 4 s | Küche, `CAM_011` (Maxi nah, Kinderaugenhöhe) | Maxi sitzt mit großen Augen → springt auf, Arme hoch | MAXI | 0,5–3,5 s „Jaaa! Ich finde den allergrößten!“ |
| SH020 | 4 s | Flur, `CAM_020` (Blick zur Haustür) | Papa hält Schlüssel hoch → winkt „los“; Maxi mit Korb (still) | PAPA | 0,5–3,5 s „Alle einsteigen, der Wald wartet!“ |
| SH030 | 6 s | Einfahrt, `CAM_030` (Mama frontal am Auto) | Mama kommt auf die Kamera zu, Maxi vorn rechts mit baumelndem Korb → Daumen hoch / Korb hoch | MAMA | 2–4 s „Korb nicht vergessen, Maxi!“ |
| SH040 | 8 s | Bürgersteig, `CAM_040` (aus der Einfahrt) | Karl rollt auf dem Bürgersteig heran → hält am Torpfosten, Hände in den Hüften | KARL | 2–6 s „Pilze sammeln? Ihr findet eh nichts!“ · 6–8 s „Hehe!“ |
| SH050 | 4 s | Einfahrt, `CAM_050` (Maxi nah) | Maxi schaut Karl nach → schmollt frontal | MAXI | 1–3 s „Der ist gemein!“ |
| SH051 | 4 s | Einfahrt, `CAM_051` | Mama hockt sich zu Maxi → Hand auf seiner Schulter | MAMA | 0,5–3,5 s „Lass ihn reden. Wir zeigen's ihm.“ |
