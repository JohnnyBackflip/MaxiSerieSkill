# Vermerk – Flur komplett neu (2026-11-05)

**Anlass:** Der User hat gesagt: „rendere nochmal den flur neu … generell neu auch die referenzbilder.“

**Ursache des alten Fehlers:**
- Im Haus-Blockout schwebten die Treppenstufen frei in der Luft.
- Die Komitee-Kamera KOM_CAM_15 stand unter der Treppe und sah die Stufen von unten.
- Flow hat daraus eine „hängende Treppe“ gemalt. Das betraf FLOW_CAM_15 und FLOW_CAM_16 und alle SH020-Bilder.

**Neu gebaut** mit `03_Blender_3D_Haus_Blockout/fix_flur_treppe_und_kameras.py`:
- **EG-Treppe** (X 0,88–1,90 / Y 1,8–5,4): massive Stufenkörper, die auf dem Boden stehen, mit Holz-Trittflächen, dunkler Wange, weißen Stäben, Antrittspfosten und Handlauf.
- **Dachbodentreppe** im OG: gleich aufgebaut.
- **Galerie-Brüstung im OG:** Handlauf mit Stäben statt massiver Platte.
- **Sicherung** des alten Stands: `Maxis_Haus_Komplett_Blockout_vor_Treppenfix_2026-11-05.blend`.

**Kameras** (Collection `99_Flur_Neu_Kameras` im Haus-Blend; für jede gibt es ein Blender-PNG und ein FLOW_*.jpg):

| Kamera | Blick |
|---|---|
| FLUR_CAM_01 | Haustür und Garderobe, Blick nach Süden (Achse von SH020) |
| FLUR_CAM_02 | Vom Eingang zur Treppe, Blick nach Norden |
| FLUR_CAM_03 | Kinderaugenhöhe, Haustür offen, Garderobe |
| FLUR_CAM_04 | Treppenfuß nah, Blick nach oben |
| FLUR_CAM_05 | OG-Galerie und Dachbodentreppe |

**Ersetzt:**
- **Folgen-Referenz:** `09_…/00_Raum_Referenzbilder/FLOW_CAM_15…` liegt jetzt in `rejected/`. Neu sind FLOW_FLUR_CAM_01 und 03.
- **Komitee-Raumszenen:** `04_…/04_Flow_Gemalte_Raumszenen/FLOW_CAM_15 und 16` liegen jetzt in `rejected/`. Neu sind FLOW_FLUR_CAM_01 bis 05.
- **SH020, SH020A und SH020B:** neu gemalt ohne alte Flurbilder; die alten liegen in `03_Szenen_Flow_Bilder/rejected/`.

## 2026-11-05 nachmittags: Raumszenen-PDF aktualisiert
- `build_flow_raumszenen_pdf.py`: Kameras 15/16 (hängende Treppe) durch FLUR_CAM_01–05 ersetzt (Blender-PNGs nach `04_…/03_Blender_Kamera_Screenshots/`, alte KOM_CAM_15/16 nach `rejected/`); Zähler dynamisch (jetzt 40 Kameras, 46 Seiten).
- Master-Referenz `REF_07_Flur_und_Treppenhaus.jpg` (ebenfalls hängende Treppe) → `rejected/…_v001_haengende_Treppe.jpg`, ersetzt durch FLOW_FLUR_CAM_02.
- PDFs neu: `04_…/00_Komitee_Kameraplan_Blender_zu_Flow_Raumszenen.pdf`, `02_Komitee_Kameraplan…pdf`, `00_Hausplan_und_Standard_Kameraeinstellungen.pdf` (Backup Skript: `build_flow_raumszenen_pdf_vor_Flurfix.py.bak`).
