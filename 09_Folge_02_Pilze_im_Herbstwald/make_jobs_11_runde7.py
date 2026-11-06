#!/usr/bin/env python3
"""Runde 7 (2026-11-05): Sprecher-Startbilder „S“ für die Flow-Videos der restlichen Folge (EIN Sprecher, groß, frontal).
Aufruf: python3 make_jobs_11_runde7.py -> jobs_11_runde7.json"""
import json, os
E = os.path.dirname(os.path.abspath(__file__))
CH, OB, RA = f"{E}/00_Charakter_Referenzbilder_Modelsheets", f"{E}/00_Objekt_Referenzbilder_Props", f"{E}/00_Raum_Referenzbilder"
MOCK, OUT, ORT = f"{E}/02_Szenen_Blender_Mockups", f"{E}/03_Szenen_Flow_Bilder", f"{E}/01_Neue_Orte_Blender_und_Flow"
C = {"Maxi": f"{CH}/CHAR_01_Maxi_Turnaround_Modelsheet.jpg", "Mama": f"{CH}/CHAR_03_Mama_Katrin_Modelsheet.jpg", "Papa": f"{CH}/CHAR_04_Papa_Thomas_Modelsheet.jpg"}
O = {k: f"{OB}/{v}" for k, v in {"Korb": "OBJ_01_Brauner_Weiden_Pilzkorb.jpg", "Steinpilz": "OBJ_02_Steinpilz.jpg", "Gift": "OBJ_04_Gruener_Knollenblaetterpilz_Giftpilz.jpg",
                                  "Pfanne": "OBJ_07_Pfanne_mit_Pilz_Sahnesauce.jpg", "Teller": "OBJ_08_Teller_Bandnudeln_mit_Pilzsauce.jpg"}.items()}
LAYOUT = ("Aufbau, Kamera und Position/Haltung EXAKT wie auf dem Blender-Mockup (Referenz 1 – nur Layout; Gliederpuppen NICHT übernehmen: "
          "blaue kleine Puppe = Maxi, gelbe = Mama Katrin, grüne = Papa Thomas). Referenz 2 ist ein fertiges Bild DESSELBEN Ortes aus der Folge: "
          "Ort, Licht, Farben, Kleidung und Look daraus übernehmen. ")
SPRECH = (" SPRECHER-EINSTELLUNG: {who} ist der EINZIGE Sprecher – groß im Bild, halbnah, Gesicht frontal zur Kamera, Mund gut sichtbar. {silent}")
GESICHT = " GESICHTER: klar, sauber, symmetrisch, unverzerrt, exakt nach den Modelsheets."
NOTE = (" VERBOTE: keine weiteren Personen, keine Tiere, kein Text, keine Untertitel, keine schwarzen Outlines, keine Gliederpuppen; "
        "reiner 3D-Pixar-CGI-Look, Querformat 16:9.")
NACHT = " TAGESZEIT: Abend, draußen NACHT – Fenster/Terrassentür dunkelblau-schwarz, nur warmes Lampenlicht."
WALD = " LICHT: Nachmittag im Herbstwald, warme tiefe Sonne, buntes Laub."
KU = (" KÜCHE (fest): salbeigrüne Küchenzeile mit Holz-Arbeitsplatte nur an zwei Wänden (links Kochfeld unter Sprossenfenster, Rückwand Bauernspüle "
      "unter Sprossenfenster und Glas-Schiebetür zur Terrasse), langer Holz-Esstisch; keine Kücheninsel, keine Hängelampen.")
S = [
 ("SH090S", f"{OUT}/SH090A.jpg", ["Maxi"], ["Korb", "Steinpilz"], "Maxi (blau-weiß gestreiftes Shirt, Mitte)", "Keine weiteren Figuren im Bild.",
  "Waldweg an der großen Baumwurzel: Maxi kniet/steht vorn halbnah frontal, winkt aufgeregt mit einem Arm und ruft begeistert; rechts hinter ihm "
  "zwischen den Wurzeln ein großer brauner Steinpilz (OBJ_02); links neben ihm der LEERE Weidenkorb (OBJ_01)." + WALD),
 ("SH120S", f"{OUT}/SH120A.jpg", ["Maxi"], ["Gift"], "Maxi (blau-weiß gestreiftes Shirt, Mitte)", "Keine weiteren Figuren im Bild.",
  "Mooshügel unter einer Birke abseits des Wegs: Maxi steht halbnah frontal auf dem Moos, staunt fasziniert und will etwas zeigen; direkt neben "
  "seinen Füßen wächst ein weißer Knollenblätterpilz (OBJ_04) mit Ring und Knolle; ein Ast und ein Stein auf dem Moos." + WALD),
 ("SH130S", f"{OUT}/SH130A.jpg", ["Mama", "Maxi"], ["Gift", "Korb"], "Mama Katrin (gelber Pullover, rechts, in der Hocke)", "Maxi links schweigt mit geschlossenem Mund.",
  "Mooshügel unter der Birke: Mama Katrin hockt rechts halbnah frontal zur Kamera, ernstes, aber liebevolles Gesicht, hebt warnend die Hand; "
  "links steht Maxi im Profil und schaut sie an (still); zwischen ihnen der weiße Knollenblätterpilz (OBJ_04); links hinten der volle Korb." + WALD),
 ("SH190S", f"{OUT}/SH190A.jpg", ["Mama"], ["Steinpilz"], "Mama Katrin (gelber Pullover, Mitte)", "Keine weiteren Figuren im Bild.",
  "Küche am Abend: Mama Katrin steht halbnah frontal am Ende des Holz-Esstischs und schneidet Steinpilze (OBJ_02) auf einem Holzbrett, schaut lächelnd "
  "zur Kamera; hinter ihr die Küchenzeile mit Tritthocker." + KU + NACHT),
 ("SH191S", f"{OUT}/SH190B.jpg", ["Papa"], ["Pfanne"], "Papa Thomas (olivgrünes T-Shirt, Mitte)", "Keine weiteren Figuren im Bild.",
  "Küche am Abend: Papa Thomas steht halbnah am Kochfeld unter dem Fenster, rührt mit dem Holzlöffel in der Pfanne mit cremiger Pilz-Sahnesauce (OBJ_07), "
  "Dampf steigt auf, er dreht das Gesicht frontal lächelnd zur Kamera; links neben ihm ein grüner Oberschrank." + KU + NACHT),
 ("SH200S", f"{OUT}/SH200A.jpg", ["Maxi"], ["Teller", "Pfanne"], "Maxi (blau-weiß gestreiftes Shirt, Mitte)", "Keine weiteren Figuren im Bild.",
  "Esstisch am Abend, Nahaufnahme in Kinderaugenhöhe: Maxi sitzt frontal am Holztisch, vor ihm ein Teller Bandnudeln mit Pilzsauce (OBJ_08), rechts die Pfanne; "
  "er schnuppert mit leuchtenden Augen. Hinter ihm Küchenzeile und dunkle Glas-Schiebetür." + KU + NACHT),
]
jobs = []
for sid, look, figs, objs, who, silent, mot in S:
    refs = [f"{MOCK}/{sid}_blender.png", look] + [C[f] for f in figs] + [O[o] for o in objs]
    names = [f"Referenz {i+1} = {os.path.basename(r).rsplit('.',1)[0]}" for i, r in enumerate(refs)]
    prompt = (f"EINSTELLUNG {sid} der Folge „Pilze im Herbstwald“ (4. November). " + LAYOUT + "(" + "; ".join(names) + "). MOTIV: " + mot
              + SPRECH.format(who=who, silent=silent) + GESICHT + NOTE)
    jobs.append({"id": sid, "style": "scene", "out": f"{OUT}/{sid}.jpg", "refs": refs, "prompt": prompt})
json.dump({"jobs": jobs}, open(f"{E}/jobs_11_runde7.json", "w"), ensure_ascii=False, indent=1)
print(len(jobs), "Jobs; fehlend:", [r for j in jobs for r in j["refs"] if not os.path.isfile(r)])
