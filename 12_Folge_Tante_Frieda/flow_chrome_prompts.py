#!/usr/bin/env python3
"""Kompakte Flow-Prompts + Referenz-Suchbegriffe für das Malen im Chrome-Flow (Claude in Chrome).
Die Referenzen liegen in Flow unter kurzen Namen (Upload per Screenshot-Drop, siehe Skill): CHAR_01_Maxi.jpg, ...,
Mockups als SHxxx_mockup.jpg, Startbilder als SHxxxA.jpg.
  python3 flow_chrome_prompts.py A SH060      -> druckt Suchbegriffe + Prompt
  python3 flow_chrome_prompts.py B SH060
"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_jobs_flow as M

FLOWNAME = {"Frieda": ("CHAR_13", "Modelsheet Tante Frieda"), "Lorchen": ("CHAR_14_Lorchen", "Modelsheet Papagei Lorchen"),
            "Maxi": ("CHAR_01_Maxi.jpg", "Modelsheet Maxi"), "Mama": ("CHAR_03_Mama", "Modelsheet Mama Katrin"),
            "Papa": ("CHAR_04_Papa", "Modelsheet Papa Thomas"), "Opa": ("CHAR_05_Opa", "Modelsheet Opa Heinrich"),
            "Anna": ("CHAR_07_Anna", "Modelsheet Anna"), "Bello": ("CHAR_09_Bello", "Modelsheet Hund Bello"),
            "Hasi": ("CHAR_02_Hasi", "Modelsheet Kuschelhase Hasi"),
            "Kaefig": ("OBJ_TF01_Kaefig", "Objektblatt Messingkäfig"), "Koffer": ("OBJ_TF02_Koffer", "Objektblatt Rollkoffer"),
            "Auto": ("OBJ_05_Auto", "Objektblatt blaues Familienauto"),
            "Kuchen": ("OBJ_TF04_Kuchen", "Objektblatt Apfelkuchen/Kuchendose"), "Muetze": ("OBJ_TF06_Muetze", "Objektblatt Opas Schiebermütze"),
            "Sprueher": ("OBJ_TF03_Sprueher", "Objektblatt grüner Blumensprüher"), "Stein": ("OBJ_TF05_Glitzerstein", "Objektblatt Annas Glitzerstein"),
            "MutDose": ("OBJ_TF07_MutDose", "Objektblatt Mut-Dose und Hasen-Stein")}
EXTRA_O = {"Kuchen": r"kuchen", "Muetze": r"mütze", "Sprueher": r"sprüh", "Stein": r"glitzerstein", "MutDose": r"mut-dose|hasen-stein"}

OVERRIDE = {"SH075": ["Maxi", "Anna"], "SH071": ["Anna", "Maxi"], "SH073": ["Maxi", "Anna"]}   # Regex-Treffer falsch (\"Tante\" im Text, Frieda nicht im Bild)


def build(mode, sid):
    plan = {x["id"]: x for x in json.load(open(f"{M.E}/szenenplan_r5.json"))}
    x = plan[sid]
    f, o = M.figuren(x)
    t = (x["bild"] + " " + x["zeile"]).lower()
    o = [k for k in o] + [k for k, rx in EXTRA_O.items() if re.search(rx, t) and not re.search(r"kein[e]? " + rx, t)]
    if "Lorchen" in f and "Kaefig" not in o: o.append("Kaefig")
    keys = o[:2] + f
    keys = OVERRIDE.get(sid, keys)
    keys = keys[:4]
    if mode == "A":
        refs = [(f"{sid}_mockup", f"Blender-Mockup {sid}")]
    else:
        mb = M.B_MOCK.get(sid, sid)
        refs = [(f"{mb}_mockup", f"Blender-Mockup {mb}"), (f"{sid}A.jpg", f"Startbild {sid}A")]
    refs += [FLOWNAME[k] for k in keys][: 5 - len(refs)]
    names = "; ".join(f"Referenz {i+1} = {d}" for i, (_, d) in enumerate(refs))
    sp = (f" SPRECHER: {x['sprecher']} ist der EINZIGE Sprecher – groß im Bild, Gesicht zur Kamera, Mund leicht geöffnet; alle anderen Münder geschlossen."
          if x["sprecher"] not in ("–", "-") else " STUMME EINSTELLUNG: alle Münder geschlossen.")
    layout = ("Aufbau, Kamera und Position/Haltung jeder Figur EXAKT wie auf dem Blender-Mockup (Referenz 1 – nur Layout; Gliederpuppen-Look NICHT übernehmen; "
              f"Puppenfarben: {M.PUPPEN}; die Puppen durch die echten Figuren ersetzen). ")
    if mode == "A":
        p = f"EINSTELLUNG {sid}, STARTBILD der Folge „Tante Frieda und Lorchen“. {layout}({names}). MOTIV: {x['bild']}"
    else:
        ende = M.ENDE.get(sid, "Der Sprecher hat den Satz beendet, Mund geschlossen, leichte Änderung von Haltung und Blick; alle anderen unverändert.")
        p = (f"EINSTELLUNG {sid}, ENDBILD derselben Einstellung ca. {max(2, x['sek']/2):.0f} Sekunden später. {layout}Referenz 2 ist das STARTBILD: Hintergrund, Möbel, Licht, "
             f"Farben, Kleidung und Gesichter 1:1 übernehmen, dieselbe Kamera, nur die Posen ändern sich ({names}). ENDE-MOTIV: {ende}")
    licht = M.LICHT
    if re.search(r"garten|einfahrt|außen", x["ort"].lower()):
        licht = " LICHT: draußen, warmes tiefes goldenes Nachmittagssonnenlicht (Novembersonne), lange weiche Schatten, blauer Himmel mit leichtem Dunst in der Ferne."
    p += licht + sp + M.GESICHT + M.NOTE.replace("keine Gliederpuppen-Optik;", "keine Gliederpuppen-Optik, kein schwarzer Rand;")
    return [r for r, _ in refs], p


if __name__ == "__main__":
    refs, p = build(sys.argv[1], sys.argv[2])
    print("REFS:", " | ".join(refs)); print(p)
