# Haus texturiert (2026-11-06)

Auftrag (User): ganzes Haus mit Google-Flow-Texturen, UV-Maps, individueller Boden je Raum, Türen als Textur, Treppe seitlich verkleidet, Küchenschränke und Fensterrahmen texturiert, außen alles, Rasen auf die Wiese, mehr Detail; neue Blender-Grafiken dauerhaft speichern.

## Dateien
| Datei | Zweck |
|---|---|
| `Maxis_Haus_Komplett_Blockout.blend` | Original (unverändert) |
| `Maxis_Haus_Komplett_Texturiert.blend` | **neues Haus** mit Texturen, UV-Maps, Details (Texturen relativ `//Texturen/`) |
| `texturen_katalog.py` | 43 Texturen: Flow-Beschreibung, Meter je Bild, Modus (kachel/fit) |
| `texturen_nachbearbeiten.py` | Rohbild → nahtlos (Versatz-Überblendung), quadratisch 1024 px; Türen zugeschnitten |
| `texturiere_haus.py` | Materialien ersetzen, UV-Maps (Weltmaß-Box-Projektion), Details einbauen, speichern |
| `Texturen/roh/*.jpg` | Flow-Rohbilder (1376×768) mit `.prompt.txt` |
| `Texturen/*.jpg` | fertige Kacheln (1024²), Türen 512×1024 |

## Ablauf (wiederholbar)
```
python3 texturen_katalog.py                                   # jobs_texturen.json
python3 ../agy_generate_image.py batch jobs_texturen.json --parallel 3   # Flow, ca. 45–95 s je Bild
python3 texturen_nachbearbeiten.py [id …]                     # Kacheln
blender -b Maxis_Haus_Komplett_Blockout.blend --python texturiere_haus.py
```
Ohne `-I` starten (die Skripte importieren ihre Nachbarn).

## Texturen
- **Böden je Raum einzeln:** EG Flur (Terrakotta-Creme-Fliesen), Wohnzimmer (Fischgrät-Eiche), Küche (Salbei-Creme-Schachbrett), Spielzimmer (blaugrauer Spielboden mit Konfetti), Gästeklo (weiße Sechseck-Fliesen); OG Bad (türkise Mosaikfliesen), Flur (dunkles Nussbaumholz), Kinderzimmer (helle Birke), Eltern (graubraune Eiche), Dachboden (alte Dielen), Garage (Beton).
- **Wände/Fassade:** Innenputz (Raufaser), Außenputz creme-gelb, Dachziegel, Ziegel (Ben), Schiefer (Anna-Dach), Minzputz (Anna), Garagentor, Schuppenholz, Bitumendach.
- **Türen/Rahmen:** Innentür (weiß, 6 Füllungen, ein Bild je Türfläche), Haustür (petrolblau mit Briefschlitz), Fenster- und Türrahmen weiß lackiert.
- **Küche:** Salbei-Lack-Fronten (als Geometrie), Arbeitsplatte Eiche-Block.
- **Treppe:** Holz für Tritt, Wange, Handlauf; Setzstufen weiß gestrichen.
- **Möbel:** Nuss, Eiche, Kiefer; Sofa geblümt (Retro-Gold), Teppiche (blau Rauten, Terrakotta, Spielteppich mit Straßen).
- **Außen:** Rasen, Wiese mit Klee, Hecken/Laub, Rinde, Pflaster (Pfad, Blöcke), Asphalt, Granit-Bordstein, Zaun, Terrassendielen.

## Neue Details (Geometrie, Sammlung `07_Details_Texturiert`)
- **67 Fußleisten** innen und **37 Sockel** (Stein, 35 cm) außen an allen vollen Wandsegmenten.
- **Treppenverkleidung:** geschlossene Holzseite für die EG-Treppe samt Wangenleiste und für die Dachbodentreppe.
- **Küchenschränke:** Fronten im 60-cm-Raster mit Messinggriffen (Unter- und Oberschränke).
- **18 Fensterscheiben** (Glas, durchsichtig) im Haus.
- **Decken weiß:** Unterseiten der Böden von OG und DG und die Innenseiten der Außenwände bekommen Innenputz (vorher Boden- bzw. Fassadentextur).

## Bekanntes / offen
- Texturen sind als Albedo gemalt (kein Normal-/Roughness-Map); Blockout-Formen bleiben kantig, Möbel sind weiter Primitive.
- Nahtlose Überblendung kann bei regelmäßigen Mustern (Fliesen) leicht verwaschene Linien zeigen.
- Kein Schnee/Herbstlaub, Beleuchtung wie im Blockout.
