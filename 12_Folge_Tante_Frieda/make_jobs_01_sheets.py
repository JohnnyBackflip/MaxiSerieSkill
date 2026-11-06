#!/usr/bin/env python3
"""Welle 1 (2026-11-06): neue Modelsheets (CHAR_13 Frieda, CHAR_14 Lorchen) + OBJ_TF-Sheets.
Eigene Entwürfe (keine Vorlage aus dem Buch). Aufruf: python3 make_jobs_01_sheets.py -> jobs_01_sheets.json"""
import json, os
E = os.path.dirname(os.path.abspath(__file__))
CH, OB = f"{E}/00_Charakter_Referenzbilder_Modelsheets", f"{E}/00_Objekt_Referenzbilder_Props"
MAXI, OPA, MAMA = f"{CH}/CHAR_01_Maxi_Turnaround_Modelsheet.jpg", f"{CH}/CHAR_05_Opa_Heinrich_Modelsheet.jpg", f"{CH}/CHAR_03_Mama_Katrin_Modelsheet.jpg"
SHEET = ("CHARACTER MODEL SHEET im exakt gleichen 3D-Pixar-CGI-Stil, Proportionen und Studio-Look wie die Referenz-Modelsheets: "
         "Drei Ansichten nebeneinander auf neutralem grauem Studiohintergrund – links Ganzkörper Frontansicht, Mitte Ganzkörper "
         "Dreiviertel-Ansicht, rechts großes Gesichts-Close-up. ")
ENDE = " Keine Texte, keine Schrift, keine Logos im Bild, keine schwarzen Outlines, Querformat 16:9 (1376×768)."
jobs = [
 {"id": "CHAR_13", "style": "none", "out": f"{CH}/CHAR_13_Tante_Frieda_Modelsheet.jpg", "refs": [OPA, MAMA],
  "prompt": SHEET + "(Referenz 1 = Großvater Heinrich, ihr jüngerer Bruder – gleiche Familienähnlichkeit, gleiche Größe der Erwachsenen; "
  "Referenz 2 = Erwachsene für Stil und Proportionen.) NEUE FIGUR: TANTE FRIEDA, ca. 72 Jahre, Großtante, etwa 1,60 m, aufrechte, "
  "steife Haltung. Silbergraue, feste, runde Dauerwellen-Frisur; große ovale Brille mit dünnem Goldrand an einer Perlenkette; "
  "schmale spitze Nase, schmale Lippen, hochgezogene Augenbrauen, leicht missbilligender, aber nicht böser Blick (komische Figur). "
  "Kleidung: pflaumenfarbene (dunkles Violett-Rot) Strickjacke mit runder goldener Brosche, darunter weiße Bluse mit kleinem Kragen, "
  "grau karierter Rock bis unter das Knie, hautfarbene Strumpfhose, schwarze Halbschuhe; schwarze Henkelhandtasche am Unterarm." + ENDE},
 {"id": "CHAR_14", "style": "none", "out": f"{CH}/CHAR_14_Lorchen_Papagei_Modelsheet.jpg", "refs": [MAXI],
  "prompt": SHEET.replace("Ganzkörper ", "") + "(Referenz 1 = Kind Maxi, nur für Stil und Größenvergleich.) NEUE FIGUR: LORCHEN, ein Papagei "
  "(Amazone), etwa 35 cm groß. Gefieder kräftig grasgrün, gelbe Stirn und gelbe Wangen, roter Fleck an den Flügeln (Flügelspiegel), "
  "Schwanzspitzen gelbgrün, heller hornfarbener gebogener Schnabel, große runde orangefarbene Augen mit weißem Ring, graue Füße. "
  "Ausdrucksstark und frech, wie eine Cartoonfigur. Links frontal auf einer Holzstange sitzend, Mitte im Profil mit leicht geöffneten "
  "Flügeln, rechts Kopf-Close-up mit schief gelegtem Kopf. Keine Menschen auf dem Sheet." + ENDE},
]
O = [
 ("OBJ_TF01", "Lorchens_Messing_Kaefig", "Ein runder Vogelkäfig aus glänzendem Messing mit Kuppeldach und Tragering oben, etwa 55 cm hoch und 35 cm Durchmesser, "
  "senkrechte Gitterstäbe, kleine Tür vorn, eine waagrechte Holz-Sitzstange, ein weißer Porzellan-Futternapf, Boden mit Schublade. "
  "LINKS: Käfig mit einem grünen Papagei (gelbe Stirn, roter Flügelfleck) trocken und ordentlich auf der Stange. "
  "RECHTS: derselbe Käfig, der Papagei ist tropfnass, die Federn gesträubt und plustrig, glücklich mit ausgebreiteten Flügeln, ein paar Wassertropfen. "
  "Größenbezug: ein 5-jähriges Kind (1,06 m) muss ihn mit beiden Armen tragen."),
 ("OBJ_TF02", "Friedas_Riesen_Rollkoffer", "Ein riesiger Hartschalen-Rollkoffer in Pflaumenfarbe (dunkles Violett-Rot), etwa 85 cm hoch (reicht einem 5-jährigen "
  "Kind bis zur Brust), vier Rollen, ausziehbarer Griff, goldene Zahlenschloss-Schnallen, ein altmodischer brauner Lederanhänger. "
  "LINKS: Dreiviertel-Ansicht stehend. RECHTS: Seitenansicht mit ausgezogenem Griff."),
 ("OBJ_TF03", "Mamas_gruener_Blumensprueher", "Ein grüner Kunststoff-Blumensprüher (Pumpsprüher) für Zimmerpflanzen, etwa 25 cm hoch, "
  "halbtransparente grüne Flasche mit Wasser, weißer Sprühkopf mit Abzugsgriff. LINKS: Dreiviertel-Ansicht. RECHTS: Seitenansicht, ein feiner Sprühnebel tritt aus."),
 ("OBJ_TF04", "Apfelkuchen_und_Kuchendose", "LINKS: ein runder gedeckter Apfelkuchen mit goldbraunem Streuselgitter auf einer weißen Tortenplatte, ein Stück "
  "herausgeschnitten, Apfelfüllung sichtbar, daneben ein Tortenheber. RECHTS: eine runde himmelblaue Kuchendose aus Kunststoff mit "
  "durchsichtigem Deckel, darin drei Stück Apfelkuchen. Größenbezug: Ein 5-jähriges Kind kann die Dose mit beiden Händen halten."),
 ("OBJ_TF05", "Annas_Glitzerstein", "Ein daumengroßer violetter Kristall (Amethyst-Druse) mit funkelnden Spitzen, etwa 4 cm, liegt in einer offenen Kinderhand "
  "(nur Hand sichtbar). LINKS: Kristall allein in Dreiviertel-Ansicht, glitzernd. RECHTS: Kristall in einer kleinen Kinderhand."),
 ("OBJ_TF06", "Opas_graue_Schiebermuetze", "Eine graue Schiebermütze (Flatcap) aus Tweed mit feinem Fischgrätmuster und kurzem Schirm. "
  "LINKS: Dreiviertel-Ansicht von vorn. RECHTS: Seitenansicht."),
 ("OBJ_TF07", "Mut_Dose_und_Hasen_Stein", "LINKS: eine alte runde Blechdose (Keksdose) mit Deckel, etwa 15 cm Durchmesser, verblasstes Dunkelrot mit Goldrand, "
  "leicht zerkratzt, Deckel offen, innen einige glatte Kieselsteine. RECHTS: ein flacher grauer Kieselstein, etwa 5 cm, mit einem "
  "einfachen, kindlich aufgemalten weißen Hasengesicht mit langen Ohren (ohne Schrift)."),
]
for oid, name, txt in O:
    jobs.append({"id": oid, "style": "object", "out": f"{OB}/{oid}_{name}.jpg", "refs": [], "prompt": "OBJEKT: " + txt})
json.dump({"jobs": jobs}, open(f"{E}/jobs_01_sheets.json", "w"), ensure_ascii=False, indent=1)
print(len(jobs), "Jobs")
