# Orte und Kameras

Alle Orte sind wiederverwendbar. Zu jeder Kamera gibt es zwei Bilder: einen **Blender-Screenshot** (`*_CAM_xx….png`) und eine **leere Flow-Raumszene** (`FLOW_*_CAM_xx….jpg`). Die Raumszene dient in Flow als Ortsreferenz.
Pläne: `../01_Hausplan_und_Zimmer_Bilder/` (Nachbarschaftsplan, Grundrisse von EG und OG mit Kameraplan). Übersichts-PDF: `../02_Komitee_Kameraplan_Blender_zu_Flow_Raumszenen.pdf` (neu bauen mit `../build_flow_raumszenen_pdf.py`).

## 1. Maxis Haus, Ahornweg 4 (mit Garten, Garage und Straße)
- **Blockout:** `../03_Blender_3D_Haus_Blockout/Maxis_Haus_Komplett_Blockout.blend` (Bauskript `build_house_blockout.py`, Nachbarhäuser `neighbor_anna_ahornweg2.py` / `neighbor_ben_ahornweg6.py`, Straße und Natur `street_and_nature.py`). Sicherungen: `…_vor_Treppenfix_2026-11-05.blend` und `…_vor_Oberschrankfix_2026-11-05.blend`.
- **Ordner** (alle in `../04_Komitee_Kameraplan_und_Flow_Raumszenen/`): Blender-Screenshots in `03_Blender_Kamera_Screenshots/`, Flow-Raumszenen in `04_Flow_Gemalte_Raumszenen/`, Raumreferenzen `REF_xx` in `01_Master_Referenzbilder_Raeume/`.

### Raumreferenzen (REF)
| REF | Raum |
|---|---|
| REF_01 | Straße Ahornweg und Nachbarhäuser |
| REF_02 | Hausgarten: Terrasse, Apfelbaum, Schuppen |
| REF_03 | EG Wohnzimmer |
| REF_04 | EG Küche |
| REF_05 | EG Spielzimmer |
| REF_06 | EG Gästeklo |
| REF_07 | Flur und Treppenhaus (erneuert 2026-11-05) |
| REF_08 | OG Kinderzimmer |
| REF_09 | OG Elternzimmer |
| REF_10 | OG Badezimmer mit Badewanne |
| REF_11 | DG Dachboden |
| REF_12 | Einfahrt und Garage mit Werkbank |

### Standardkameras (KOM_CAM)
Die Kürzel stehen für die Räume: WZ Wohnzimmer, KU Küche, SZ Spielzimmer, GK Gästeklo, KZ Kinderzimmer, EZ Elternzimmer, BD Bad, DB Dachboden, GAR Garage.

| Kamera | Motiv |
|---|---|
| KOM_CAM_01 | Straße, Totale mit drei Häusern |
| KOM_CAM_02 | Bürgersteig, Straßenverlauf und Zebrastreifen |
| KOM_CAM_03 | Vorgarten, Gartentor und Veranda |
| KOM_CAM_04 | Garten-Totale: Wiese, Sandkasten, Schaukel/Schuppen |
| KOM_CAM_05 | Holzterrasse und Apfelbaum mit Schaukel |
| KOM_CAM_06 | Opas Gartenschuppen, Werkbank, Sandkasten |
| KOM_CAM_07 | WZ: Sofa, Sessel, Teppich, Blick in die Küche |
| KOM_CAM_08 | WZ-Gegenschuss: TV-Board und Flurdurchgang |
| KOM_CAM_09 | KU: Küchenzeile, Tritthocker, 6er-Esstisch |
| KOM_CAM_10 | KU-Gegenschuss: Esstisch, durch die Terrassentür in den Garten |
| KOM_CAM_11 | SZ-Totale: Indoor-Rutsche, Maltisch, Kuschelecke |
| KOM_CAM_12 | SZ-Gegenschuss: Würfelregal, Spielteppich |
| KOM_CAM_13 | GK: Waschbecken, Spiegel, Tritthocker, WC |
| KOM_CAM_14 | GK-Gegenschuss: WC und Waschplatz |
| (KOM_CAM_15/16) | alte Flur-Kameras, **ersetzt durch FLUR_CAM_01–05** |
| KOM_CAM_17 | KZ: Kinderbett mit Hasi, Kissenburg, Eisenbahn |
| KOM_CAM_18 | KZ-Gegenschuss: Eisenbahnteppich, Kleiderschrank, Bücherregal |
| KOM_CAM_19 | EZ: Doppelbett, Nachttische, Gartenfenster |
| KOM_CAM_20 | EZ-Gegenschuss: Lesesessel, Kleiderschrank, Kommode |
| KOM_CAM_21 | BD: Doppelwaschtisch, Tritthocker, freistehende Badewanne |
| KOM_CAM_22 | BD: Badewanne nah, Walk-in-Dusche |
| KOM_CAM_23 | DB: Dachbalken, Schatztruhe, Fernrohr, Giebelfenster |
| KOM_CAM_24 | DB: Geheimversteck der Kinder, Laterne, Kisten |
| KOM_CAM_25 | GAR: Einfahrt, offenes Garagentor von außen |
| KOM_CAM_26 | GAR innen: Werkbank, Schraubstock, Werkzeugwand |
| KOM_CAM_27 | GAR-Gegenschuss: Werkbank, durch das Tor zur Einfahrt |
| KOM_CAM_28 | Annas Nachbarhaus (Ahornweg 2): Vorgarten, Wintergarten |
| KOM_CAM_29 | Bens Nachbarhaus (Ahornweg 6): Hof, Skaterampe, Basketballkorb |
| KOM_CAM_30 | WZ frontal: geblümtes Familiensofa, Vorlesesessel |
| KOM_CAM_31 | KU nah: Maxis Tritthocker, Spüle, Küchenzeile |
| KOM_CAM_32 | KZ auf Kinderaugenhöhe: Bett, Hasi, Eisenbahn, Kissenburg |
| KOM_CAM_33 | Garten: Zauntor zu Anna, Hochbeet, Apfelbaum |
| KOM_CAM_34 | WZ: Teppichkante, Blick über das Parkett zum Küchendurchgang (aus F01K) |
| KOM_CAM_35 | Vom WZ zur KU: Kissenbrücke, Durchgang, Korridor (aus F01K) |
| KOM_CAM_36 | KU: Terrassentür-Schwelle nah, Gartenblick (aus F01K) |
| KOM_CAM_37 | Garten: Picknickmatte nah, Apfelbaum und Haus (aus F01K) |
| KOM_CAM_38 | Vorgarten: Gartentor und Briefkasten nah, Kinderaugenhöhe (aus F01P) |

### Flur (neu seit 2026-11-05, Treppe repariert)
Die Bilder liegen in `../11_Flur_Neu_Treppe_Blender_und_Flow/`, den Vermerk dazu findest du dort.
| Kamera | Motiv |
|---|---|
| FLUR_CAM_01 | Haustür und Garderobe, Blick nach Süden |
| FLUR_CAM_02 | Vom Eingang zur Treppe, Blick nach Norden |
| FLUR_CAM_03 | Haustür und Garderobe auf Kinderaugenhöhe |
| FLUR_CAM_04 | Treppenfuß nah, Blick nach oben |
| FLUR_CAM_05 | OG-Galerie und Dachbodentreppe |

### Kameras einzelner Folgen im Haus
Diese Kameras stehen nur im Skript `../09_Folge_02_Pilze_im_Herbstwald/02_Szenen_Blender_Mockups/build_folge02_szenen_AB.py`:
- `CAM_010`, `CAM_011`, `CAM_020`, `CAM_030`, `CAM_040`, `CAM_050`, `CAM_051` (Sprecher-Einstellungen, Runde 6)
- `CAM_190S` (vom WZ-Durchgang in die Ecke mit Herd und Spüle)
- Einfahrt mit Auto, Auto-Innenraum
- `INTRO` und `INTRO2_*` (vor dem Haus)
Wenn eine dieser Kameras öfter gebraucht wird, macht man daraus eine Standardkamera.

### Architektur-Blöcke (gehören in jeden Prompt für diesen Ort)
- **Küche:** Die Küchenzeile ist L-förmig und steht nur an der West- und der Nordwand: salbeigrün, mit Holz-Arbeitsplatte und weißer Bauernspüle unter einem Sprossenfenster. Es gibt **keine Insel und keine Hängelampen**. Über der Spüle und an der Terrassen-Rückwand hängen **keine Oberschränke**. Gearbeitet wird nur an echten Möbeln; zum Schneiden steht Mama am Esstisch.
- **Esstisch/Rückwand:** links die Spülenzeile, hinter Mama und Papa die gläserne Schiebetür zur Terrasse, rechts eine schlichte Wand. Raumreferenzen: FLOW_CAM_09, FLOW_CAM_10 oder SH200A.
- **Sitzordnung am Esstisch:** Alle sitzen an einer Längsseite, links Maxi, in der Mitte Mama, rechts Papa.
- **Flur:** Die Treppe steht auf dem Boden. Im Durchgang von der Küche zum Flur ist die Flurtreppe zu sehen.

## 2. Herbstwald mit Tunnel am Waldrand
- **Blockout:** `../09_Folge_02_Pilze_im_Herbstwald/01_Neue_Orte_Blender_und_Flow/Herbstwald_Blockout.blend` (Bauskript `build_herbstwald_blockout.py`, Sicherung `…_vor_Strassenfix_2026-11-05.blend`). Screenshots und Flow-Raumszenen liegen im selben Ordner.
- Was zum Ort gehört: Landstraße, Waldparkplatz mit Holzschild, Waldweg, Wurzelbaum (Fundort des Steinpilzes), Pilzlichtung mit Baumstumpf und Pfifferlingen, Giftpilz-Stelle östlich des Wegs (Mooshügel unter einer Birke), Tunnel (Collection `04_Tunnel_am_Waldrand`).
- **Auf der Fahrbahn stehen keine Bäume** (wurde am 05.11. korrigiert).

| Kamera | Motiv |
|---|---|
| WALD_CAM_01 | Landstraße zum Waldrand |
| WALD_CAM_02 | Waldparkplatz mit Holzschild |
| WALD_CAM_03 | Waldweg, Totale |
| WALD_CAM_04 | Waldweg nah, Baumwurzel, Kinderaugenhöhe |
| WALD_CAM_05 | Pilzlichtung mit Baumstumpf (ohne weißen Pilz) |
| WALD_CAM_06 | Giftpilz-Stelle nah, Kinderaugenhöhe |
| WALD_CAM_07 | Giftpilz-Stelle, Totale vom Waldweg |
| TUNNEL_CAM_01 | Tunneleingang, Kinderaugenhöhe |
| TUNNEL_CAM_02 | Im Tunnel, Blick zum Ausgang |
| TUNNEL_CAM_03 | Tunnelausgang, Gegenschuss von der Wiese |
| TUNNEL_CAM_04 | Totale vom Parkplatz auf den Damm |

Tunnel (Bibel 5.2): ein Fußweg-Durchlass aus Beton unter dem Feldwegdamm, 1,30 m hoch und 12 m lang, 20 Schritte vom Parkplatz entfernt. Den Ausgang sieht man immer als hellen Kreis. Kein Wasser, keine völlige Dunkelheit.
Kameras einzelner Folgen im Wald: `CAM_150S` (exakt seitlich, Auto parallel zum Bildrand).

## 3. Familienszene Wohnzimmer
`../08_Familienszene_Wohnzimmer_Blender_und_Flow/` ist eine Musterszene auf KOM_CAM_30 mit Maxi, Mama und Papa auf dem Sofa (Blend, Mockup und Flow-Bild).

## Noch nicht gebaut (laut Staffelbogen nötig)
- Bens Garage, halbdunkel, mit Lichtschalter (F09)
- Karls Haus am Ende des Ahornwegs mit Haustür und Garten (F02-Schlussbild, F06)
- Ahornweg 8 mit Zaun
- Skaterpark
- Omas Küche in Lindenallee 12 (Bilder dazu gibt es schon in `02_Charaktere…/05b`, `06b`)
