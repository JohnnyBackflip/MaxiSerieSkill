#!/usr/bin/env python3
"""Runde 6 (2026-11-05): SH010–SH050 nach den Veo/Flow-Guide-Regeln neu (STRIKT):
eine Einstellung = EIN Sprecher (SH010/SH011, SH050/SH051 getrennt), Sprecher groß, halbnah, frontal, Mund gut sichtbar;
alle anderen still mit geschlossenem Mund. Startbild (A) zuerst, Endbild (B) danach mit A als Referenz 2.
Aufruf: python3 make_jobs_10_runde6.py   -> jobs_10_runde6_welle1.json (A) / _welle2.json (B)"""
import json, os
E = os.path.dirname(os.path.abspath(__file__))
K = os.path.dirname(E)
CH, OB, RA = f"{E}/00_Charakter_Referenzbilder_Modelsheets", f"{E}/00_Objekt_Referenzbilder_Props", f"{E}/00_Raum_Referenzbilder"
MOCK, OUT = f"{E}/02_Szenen_Blender_Mockups", f"{E}/03_Szenen_Flow_Bilder"
FL = f"{K}/04_Komitee_Kameraplan_und_Flow_Raumszenen/04_Flow_Gemalte_Raumszenen"
C = {"Maxi": f"{CH}/CHAR_01_Maxi_Turnaround_Modelsheet.jpg", "Mama": f"{CH}/CHAR_03_Mama_Katrin_Modelsheet.jpg",
     "Papa": f"{CH}/CHAR_04_Papa_Thomas_Modelsheet.jpg", "Karl": f"{CH}/CHAR_10_Karl_Nachbarsjunge_Modelsheet.jpg"}
O = {"Korb": f"{OB}/OBJ_01_Brauner_Weiden_Pilzkorb.jpg", "Auto": f"{OB}/OBJ_05_Blaues_Familienauto_Kombi.jpg",
     "BMX": f"{OB}/OBJ_06_Karls_Schwarz_Oranges_BMX_Fahrrad.jpg"}
KUECHE = f"{RA}/FLOW_CAM_10_KU_Gegenschuss_Esstisch_durch_Terrassentuer_in_Garten.jpg"
FLUR = f"{RA}/FLOW_FLUR_CAM_01_Haustuer_Garderobe_Blick_Sued.jpg"
EINF = f"{RA}/FLOW_CAM_25_GAR_Einfahrt_und_Offenes_Garagentor_Aussen.jpg"
STR = f"{RA}/FLOW_CAM_02_Buergersteig_Strassenverlauf_und_Zebrastreifen.jpg"

LAYOUT = ("Aufbau, Kamera und Position/Haltung jeder Person EXAKT wie auf dem Blender-Mockup (Referenz 1 – nur Layout; Klötzchen-Look und "
          "Gliederpuppen NICHT übernehmen: blaue kleine Puppe = Maxi, gelbe = Mama Katrin, grüne = Papa Thomas, orange = Karl). ")
LAYOUT_B = LAYOUT + ("Referenz 2 ist das STARTBILD derselben Einstellung: Hintergrund, Möbel, Licht, Farben, Kleidung und Gesichter 1:1 übernehmen – "
                     "dieselbe Kamera Sekunden später, nur Posen ändern sich wie beschrieben. ")
TAG = " LICHT: Vormittag, helles freundliches Herbst-Tageslicht."
SPRECH = (" SPRECHER-EINSTELLUNG (für das spätere Video): {who} ist der EINZIGE Sprecher dieser Einstellung – groß im Bild, halbnah, "
          "Gesicht frontal zur Kamera, Mund gut sichtbar und leicht geöffnet. {silent}")
STILL = "Alle anderen Figuren im Bild schweigen mit geschlossenem Mund."
GESICHT = (" GESICHTER: klar, sauber, symmetrisch, unverzerrt, exakt nach den Modelsheets; keine verzogenen Münder, keine schiefen Augen.")
NOTE = (" Figuren exakt wie auf den Modelsheets; Ort exakt wie auf der Raum-Referenz. VERBOTE: keine weiteren Personen, keine Tiere, "
        "kein Text, keine Untertitel, keine schwarzen Outlines, keine Gliederpuppen; reiner 3D-Pixar-CGI-Look, Querformat 16:9.")
KU_ARCH = (" KÜCHE (fest): hinter Mama die Rückwand mit der Glas-Schiebetür zur Terrasse (Garten im Morgenlicht), links davon die salbeigrüne "
           "Küchenzeile mit Holz-Arbeitsplatte und weißer Bauernspüle unter einem Sprossenfenster; vorn der lange Holz-Esstisch mit Holzstühlen. "
           "Keine Oberschränke an dieser Rückwand, keine Hängelampen, keine Kücheninsel.")
EIN_ARCH = (" EINFAHRT (fest): graue Pflaster-Einfahrt vor der Garage mit offenem Garagentor, das kleine runde blaue Familienauto (OBJ_05) "
            "steht GERADE in der Einfahrt mit der Front zur Straße, am Ende der Einfahrt zwei helle Torpfosten mit Kappen, dahinter Bürgersteig und Straße.")

S = [
 # id, wer, Figuren, Objekte, Raum, A-Motiv, B-Motiv
 ("SH010", "Mama Katrin (gelber Pullover, lange braune Haare, Mitte)", ["Mama", "Maxi"], ["Korb"], KUECHE,
  "Morgens in der Küche: Mama Katrin steht halbnah frontal hinter dem Esstisch und hält den LEEREN Weidenkorb (OBJ_01) vor sich, "
  "strahlt die Kamera an und beginnt zu sprechen. Links sitzt Maxi am Tisch und schaut neugierig zu ihr hoch (still)." + KU_ARCH,
  "Mama Katrin hebt den leeren Korb fröhlich hoch über den Kopf, lacht frontal in die Kamera; Maxi links am Tisch staunt (still)." + KU_ARCH),
 ("SH011", "Maxi (blau-weiß gestreiftes Shirt, Mitte)", ["Maxi"], [], KUECHE,
  "Nahaufnahme in Kinderaugenhöhe: Maxi sitzt am Esstisch, frontal zur Kamera, große begeisterte Augen, der Mund öffnet sich zum Jubeln. "
  "Hinter ihm die Glas-Schiebetür zum Garten im Morgenlicht." + KU_ARCH.replace("hinter Mama", "hinter Maxi"),
  "Maxi ist aufgesprungen und steht hinter seinem Stuhl, beide Arme jubelnd in die Luft, frontal zur Kamera, lacht mit offenem Mund." + KU_ARCH.replace("hinter Mama", "hinter Maxi")),
 ("SH020", "Papa Thomas (olivgrünes T-Shirt, rechts)", ["Papa", "Maxi"], ["Korb"], FLUR,
  "Flur am Morgen, Blick zur Haustür: Papa Thomas steht halbnah frontal vor der Haustür und hält den Autoschlüssel hoch in die Luft, "
  "beginnt fröhlich zu rufen. Links neben ihm Maxi mit dem leeren Korb (OBJ_01), still und erwartungsvoll. Garderobe an der Wand.",
  "Papa Thomas winkt frontal mit der Hand „los geht's“, lächelt in die Kamera; Maxi hüpft mit dem Korb zur Haustür (still)."),
 ("SH030", "Mama Katrin (gelber Pullover, links neben dem Auto)", ["Mama", "Maxi"], ["Korb", "Auto"], EINF,
  "Einfahrt am Vormittag: Mama Katrin kommt neben dem blauen Auto halbnah frontal auf die Kamera zu und ruft lächelnd. Rechts im Vordergrund "
  "Maxi in Dreiviertel-Rückenansicht, der leere Korb baumelt achtlos tief an seiner Hand (still)." + EIN_ARCH,
  "Mama Katrin zeigt lächelnd Daumen hoch frontal zur Kamera; Maxi rechts im Vordergrund hält den Korb stolz hoch (still)." + EIN_ARCH),
 ("SH040", "Karl (8 Jahre, orangefarbenes Shirt, schwarz-oranges BMX, Mitte)", ["Karl"], ["BMX"], STR,
  "Blick aus der Einfahrt auf den Bürgersteig: Karl rollt auf seinem schwarz-orangen BMX (OBJ_06) AUF DEM BÜRGERSTEIG heran, groß und halbnah, "
  "dreht den Kopf frech grinsend frontal zur Kamera. Rechts ein heller Torpfosten der Einfahrt, hinten Straße und Hecke. Karl bleibt auf dem Bürgersteig.",
  "Karl hält auf dem Bürgersteig am Torpfosten an, ein Fuß am Boden, Hände in den Hüften, grinst frech frontal in die Kamera und lacht."),
 ("SH050", "Maxi (blau-weiß gestreiftes Shirt, Mitte)", ["Maxi"], ["Korb", "Auto"], EINF,
  "Nahaufnahme in Kinderaugenhöhe in der Einfahrt: Maxi drückt den leeren Korb (OBJ_01) fest an die Brust und schaut gekränkt zur Seite "
  "Richtung Straße, Karl hinterher. Hinter ihm das blaue Auto und die Garage." + EIN_ARCH,
  "Maxi schaut jetzt frontal in die Kamera, schmollt mit vorgeschobener Unterlippe und gerunzelter Stirn, Korb fest an der Brust."),
 ("SH051", "Mama Katrin (gelber Pullover, links, in der Hocke)", ["Mama", "Maxi"], ["Korb", "Auto"], EINF,
  "Einfahrt: Mama Katrin geht links neben Maxi in die Hocke, halbnah frontal zur Kamera, warmes zuversichtliches Lächeln, beginnt zu sprechen; "
  "Maxi rechts schaut zu ihr (still), Korb im Arm." + EIN_ARCH,
  "Mama Katrin hat die Hand auf Maxis Schulter gelegt und lächelt frontal zuversichtlich; Maxi lächelt sie entschlossen an (still)." + EIN_ARCH),
]
jobs = {"1": [], "2": []}
for sid, who, figs, objs, raum, ma, mb in S:
    silent = STILL if len(figs) > 1 else "Keine weiteren Figuren im Bild."
    for ab, mot in (("A", ma), ("B", mb)):
        refs = [f"{MOCK}/{sid}{ab}_blender.png"]
        if ab == "B":
            refs.append(f"{OUT}/{sid}A.jpg")
        refs += [C[f] for f in figs] + [O[o] for o in objs] + [raum]
        names = [f"Referenz {i+1} = {os.path.basename(r).rsplit('.',1)[0]}" for i, r in enumerate(refs)]
        word = "STARTBILD" if ab == "A" else "ENDBILD"
        prompt = (f"EINSTELLUNG {sid}, {word} der Folge „Pilze im Herbstwald“ (4. November). " + (LAYOUT_B if ab == "B" else LAYOUT)
                  + "(" + "; ".join(names) + "). MOTIV: " + mot + TAG + SPRECH.format(who=who, silent=silent) + GESICHT + NOTE)
        jobs["1" if ab == "A" else "2"].append({"id": f"{sid}{ab}", "style": "scene", "out": f"{OUT}/{sid}{ab}.jpg", "refs": refs, "prompt": prompt})
for w, js in jobs.items():
    json.dump({"jobs": js}, open(f"{E}/jobs_10_runde6_welle{w}.json", "w"), ensure_ascii=False, indent=1)
    miss = [r for j in js for r in j["refs"] if not os.path.isfile(r) and not r.endswith(("A.jpg", "_blender.png"))]
    print("Welle", w, len(js), "Jobs; fehlende Referenzen:", miss)
