#!/usr/bin/env python3
"""Flow-Szenenbilder (2026-11-06): je Einstellung ein STARTBILD (SHxxxA.jpg) und ein ENDBILD (SHxxxB.jpg).
Referenz 1 = Blender-Mockup (nur Layout, Farbpuppen werden durch die Figuren ersetzt), dann CHAR-/OBJ-Sheets (höchstens 5 Referenzen insgesamt).
Endbild: Referenz 1 = Mockup (bei Zoom/Sprung das B-Mockup), Referenz 2 = fertiges Startbild, danach Sheets.
  python3 make_jobs_flow.py [A|B] [SH010 SH020 ...]    -> jobs_flow_A.json / jobs_flow_B.json
Ein Bild entspricht der halben Szenenzeit im Video (Startbild erste Hälfte, Endbild zweite Hälfte)."""
import json, os, re, sys
E = os.path.dirname(os.path.abspath(__file__))
CH, OB, MOCK, OUT = (f"{E}/00_Charakter_Referenzbilder_Modelsheets", f"{E}/00_Objekt_Referenzbilder_Props",
                     f"{E}/02_Szenen_Blender_Mockups", f"{E}/03_Szenen_Flow_Bilder")
SHEET = {"Frieda": "CHAR_13_Tante_Frieda_Modelsheet", "Lorchen": "CHAR_14_Lorchen_Papagei_Modelsheet", "Maxi": "CHAR_01_Maxi_Turnaround_Modelsheet",
         "Mama": "CHAR_03_Mama_Katrin_Modelsheet", "Papa": "CHAR_04_Papa_Thomas_Modelsheet", "Opa": "CHAR_05_Opa_Heinrich_Modelsheet",
         "Anna": "CHAR_07_Anna_Freundin_Modelsheet", "Bello": "CHAR_09_Bello_Beagle_Modelsheet", "Hasi": "CHAR_02_Hasi_Kuschelhase_Modelsheet"}
OBJ = {"Kaefig": "OBJ_TF01_Lorchens_Messing_Kaefig", "Koffer": "OBJ_TF02_Friedas_Riesen_Rollkoffer", "Auto": "OBJ_05_Blaues_Familienauto_Kombi"}
SUCH = {"Frieda": r"frieda|tante", "Lorchen": r"lorchen|papagei|vogel", "Maxi": r"maxi", "Mama": r"mama|katrin", "Papa": r"papa|thomas",
        "Opa": r"opa|heinrich", "Anna": r"anna|mädchen", "Bello": r"bello|hund", "Hasi": r"hasi"}
OSUCH = {"Kaefig": r"käfig|lorchen|papagei", "Koffer": r"koffer", "Auto": r"auto|kofferraum|beifahrer"}
PUPPEN = ("blau = Maxi, gelb = Mama Katrin, grün = Papa Thomas, türkis = Anna, braun = Opa Heinrich, violett = Tante Frieda, "
          "kleines hellgraues Stofftier = Hasi, grüner Klecks im Messingkäfig = der Papagei Lorchen, braun-weißer Klotz = Hund Bello")
LICHT = (" LICHT: warmes, tiefes goldenes Nachmittagssonnenlicht von außen (Novembersonne) fällt durch die Fenster, weiche Schatten, "
         "Lampen sind aus, in der Ferne leichter Dunst.")
GESICHT = " GESICHTER: klar, sauber, symmetrisch, unverzerrt, exakt nach den Modelsheets; keine verzogenen Münder, keine schiefen Augen."
NOTE = (" Figuren und Kleidung exakt wie auf den Modelsheets; Ort, Möbel, Böden, Türen und Wandfarben exakt wie im Blender-Mockup (Texturen sind schon im Mockup). "
        "VERBOTE: keine weiteren Personen oder Tiere als genannt, kein Text, keine Untertitel, keine Sprechblasen, keine schwarzen Outlines, "
        "keine Gliederpuppen-Optik; reiner 3D-Pixar-CGI-Look, Querformat 16:9.")
B_MOCK = {"SH041": "SH041_B", "SH082": "SH082_B"}      # Endbild mit anderem Kamerawinkel/Pose
ENDE = {
 "SH001": "Frieda hat die Beifahrertür weiter geöffnet und steigt aus; das Auto steht still, Mama winkt weiter.",
 "SH002": "Mama und Frieda stehen sich gegenüber, Mama lächelt mit weit offenen Armen, Frieda schaut kühl zurück.",
 "SH003": "Frieda hat den Käfig mit Lorchen aus dem Kofferraum geholt und hält ihn am Griff, ihr Blick geht weiter zum Auto.",
 "SH010": "Frieda hebt den Käfig leicht und spricht weiter, Mama im Hintergrund schaut verdutzt.",
 "SH020": "Maxi hat die Hand vor dem Mund, große entsetzte Augen, lehnt sich ins Zimmer zurück.",
 "SH030": "Frieda zeigt noch auf den Koffer, Papa hebt ihn schon an und stöhnt.",
 "SH032": "Papa hat den Koffer hochgehoben, das Gesicht verzogen, und schleppt ihn los.",
 "SH040": "Frieda beugt sich leicht vor und mustert den Läufer; Mama hinten lächelt verkrampft.",
 "SH042": "Frieda rümpft die Nase, Kopf leicht zurück; Mama hinten schaut betreten zu Boden.",
 "SH041": "ZOOM: Die Kamera ist ganz nah an Mamas Gesicht herangefahren, Mama lacht verlegen und errötet, Frieda nur noch unscharf als Schulter vorn.",
 "SH047": "Frieda hat die Tür hinter sich zugezogen und schaut sich im Zimmer um, Kopf zur Seite gedreht.",
 "SH048": "Die Kamera ist näher an Hasi herangefahren, Hasi liegt weiter auf dem Kissen; Frieda ist nur unscharf am Bildrand zu ahnen.",
 "SH050": "Frieda hält Hasi am ausgestreckten Arm vor sich und mustert ihn naserümpfend.",
 "SH051": "Maxi starrt mit zusammengezogenen Brauen, der Mund öffnet sich zum Sprechen.",
 "SH052": "Maxi hat Hasi an sich gerissen und drückt ihn an die Brust, Frieda hat die leeren Hände.",
 "SH058": "Frieda hat den Käfig auf den Nachttisch gestellt und streichelt über das Gitter.",
 "SH060": "Frieda spitzt den Mund, Lorchen gibt ihr ein Schnabel-Küsschen.",
 "SH065": "Maxi hat den Ball weggekickt, der Ball fliegt durch die Luft, Maxi schaut ihm missmutig nach.",
 "SH070": "Anna beugt sich weiter vom Tor vor und winkt Maxi herbei.",
 "SH075": "Maxi schaut traurig zu Boden, der Ball unter dem Arm.",
 "SH071": "Anna zwinkert und grinst breit.",
 "SH073": "Maxi blickt auf, die Augen werden groß: Ihm kommt eine Idee.",
 "SH074": "Anna reckt triumphierend die Faust.",
 "SH072": "Maxi streckt Anna die Hand hin und beide grinsen verschwörerisch.",
 "SH080": "Maxi schleicht gebückt Richtung Schrank, den Käfig am Griff.",
 "SH081": "Der Käfig steht im Schrank, Maxi schließt die Schranktüren.",
 "SH082": "Maxi springt mit ausgebreiteten Armen aufs Bett (Endbild: in der Luft über dem Bett).",
 "SH089": "Frieda steckt den Kopf noch weiter ins Zimmer, neugierig, die Augen suchend.",
 "SH083": "Maxi liegt auf dem Bett und liest, grinst heimlich hinter dem Buch.",
 "SH084": "Der leere Nachttisch, die Kamera ist etwas näher gefahren.",
 "SH085": "Frieda hat die Augen weit aufgerissen und den Mund offen, die Hände heben sich.",
 "SH086": "Frieda hat beide Hände vor dem Gesicht (halbtotal), Maxi liest auf dem Bett.",
 "SH087": "Die Schranktür wackelt leicht; Frieda dreht sich verwundert zum Schrank.",
 "SH090": "Frieda zieht strahlend den Käfig aus dem Schrank, die Kamera steht im Schrank.",
 "SH091": "Frieda hebt eine Augenbraue, der Blick fest auf Maxi.",
 "SH093": "Lorchen öffnet den Schnabel weit, Frieda schaut den Käfig an.",
 "SH095": "Maxi ist schon halb zur Tür hinaus und streckt die Zunge heraus.",
 "SH094": "Frieda drückt den Käfig an sich und schaut streng, aber liebevoll.",
 "SH100": "Mama hat den Kuchen abgestellt und lächelt gezwungen.",
 "SH101": "Frieda trinkt aus der Tasse und schaut spöttisch über den Rand.",
 "SH109": "Opa hat geklingelt und tritt einen Schritt zurück, wartet.",
 "SH110": "Opa strahlt, die Mütze in der Hand.",
 "SH111": "Frieda zeigt entsetzt nach oben auf Opas Kopf.",
 "SH112": "Opa lacht und streicht über die Glatze.",
 "SH120": "Frieda hält die Kuchengabel angewidert in der Luft, alle anderen schauen betreten.",
 "SH122": "Frieda zeigt mit der Kuchengabel auf Papa.",
 "SH123": "Papa lächelt gezwungen, die Tasse wieder unten.",
 "SH124": "Maxi flüstert Hasi etwas ins Ohr, der Blick böse und entschlossen.",
 "SH130": "Maxi flüstert weiter durchs Gitter, Lorchen neigt den Kopf.",
 "SH140": "Frieda stellt die Tasse klirrend ab und verzieht den Mund.",
 "SH141": "Lorchen plustert sich auf, der Schnabel weit offen.",
 "SH143": "Opa wischt sich Lachtränen, der Kopf zurückgeworfen.",
 "SH145": "Maxi presst beide Hände vor den Mund, die Schultern zucken, die Augen zugekniffen.",
 "SH144": "Lorchen legt den Kopf schief, der Schnabel offen.",
 "SH150": "Frieda steht empört da, die Nasenspitze weiß.",
 "SH151": "Maxi hält Hasi vors Gesicht und schaut treuherzig darüber.",
 "SH160": "Frieda hält den Käfig fest im Arm und wendet sich zum Gehen.",
 "SH165": "Mama hebt die Hände zu einer bittenden Geste.",
 "SH166": "Frieda schaut beleidigt zur Seite, das Kinn hoch.",
 "SH167": "Papa nimmt den Koffer am Griff.",
 "SH170": "Papa geht mit dem Koffer weiter auf die Kamera zu, Frieda knöpft ihren Mantel zu.",
 "SH171": "Maxi drückt Hasi an sich, der Kopf gesenkt.",
 "SH173": "Frieda wirft Maxi einen letzten Blick, die Augen glänzen.",
 "SH174": "Papa legt Maxi den Arm um die Schultern.",
 "SH175": "Maxi schaut auf, ein kleines Lächeln.",
 "SH177": "Maxi sieht Frieda ehrlich an, die Hände nervös gefaltet.",
 "SH178": "Maxi schaut zu Boden und scharrt mit dem Fuß.",
 "SH179": "Frieda lächelt mild und legt Maxi die Hand auf die Schulter.",
 "SH184": "Lorchen hüpft vergnügt auf der Stange, die Flügel halb offen.",
 "SH186": "Alle lachen herzlich, Frieda wischt sich Lachtränen, Maxi kugelt sich vor Lachen, Bello springt.",
}


def figuren(x):
    t = (x["ort"] + " " + x["bild"] + " " + x["sprecher"]).lower()
    f = [k for k, rx in SUCH.items() if re.search(rx, t)]
    if x["sprecher"] in SHEET and x["sprecher"] in f:
        f.remove(x["sprecher"]); f.insert(0, x["sprecher"])
    o = [k for k, rx in OSUCH.items() if re.search(rx, t)]
    return f, o


def refs_fuer(x):
    f, o = figuren(x)
    refs = []
    if "Lorchen" in f and "Kaefig" not in o: o.append("Kaefig")
    for k in o[:2]:
        refs.append(f"{OB}/{OBJ[k]}.jpg")
    for k in f:
        if len(refs) >= 4: break
        refs.append(f"{CH}/{SHEET[k]}.jpg")
    return refs[:4], f, o


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] in ("A", "B") else "A"
    nur = set(a for a in sys.argv[1:] if a.startswith("SH"))
    plan = json.load(open(f"{E}/szenenplan_r5.json"))
    jobs = []
    for x in plan:
        sid = x["id"]
        if nur and sid not in nur:
            continue
        sheets, f, o = refs_fuer(x)
        mockA = f"{MOCK}/{sid}_blender.png"
        sp = ""
        if x["sprecher"] not in ("–", "-"):
            sp = (f" SPRECHER-EINSTELLUNG: {x['sprecher']} ist der EINZIGE Sprecher – groß im Bild, Gesicht zur Kamera, Mund gut sichtbar und leicht geöffnet. "
                  "Alle anderen Figuren schweigen mit geschlossenem Mund.")
        else:
            sp = " STUMME EINSTELLUNG: niemand spricht, alle Münder geschlossen."
        layout = (f"Aufbau, Kamera und Position/Haltung jeder Figur EXAKT wie auf dem Blender-Mockup (Referenz 1 – nur Layout; Klötzchen-/Gliederpuppen-Look NICHT übernehmen, "
                  f"Puppenfarben: {PUPPEN}; die Puppen durch die echten Figuren ersetzen). ")
        if mode == "A":
            refs = [mockA] + sheets
            names = "; ".join(f"Referenz {i+1} = {os.path.basename(r).rsplit('.',1)[0]}" for i, r in enumerate(refs))
            prompt = (f"EINSTELLUNG {sid}, STARTBILD der Folge „Tante Frieda und Lorchen“ (Samstag, 14. November). {layout}({names}). MOTIV: {x['bild']}{LICHT}{sp}{GESICHT}{NOTE}")
            jobs.append({"id": sid + "A", "style": "scene", "out": f"{OUT}/{sid}A.jpg", "refs": refs, "prompt": prompt})
        else:
            mockB = f"{MOCK}/{B_MOCK[sid]}_blender.png" if sid in B_MOCK else mockA
            refs = [mockB, f"{OUT}/{sid}A.jpg"] + sheets
            names = "; ".join(f"Referenz {i+1} = {os.path.basename(r).rsplit('.',1)[0]}" for i, r in enumerate(refs))
            sek = max(2.0, x["sek"] / 2)
            ende = ENDE.get(sid, "Der Sprecher hat den Satz beendet, Mund geschlossen, leichte Änderung von Haltung und Blick; alle anderen unverändert.")
            prompt = (f"EINSTELLUNG {sid}, ENDBILD derselben Einstellung ca. {sek:.0f} Sekunden später. {layout}Referenz 2 ist das STARTBILD: Hintergrund, Möbel, Licht, Farben, "
                      f"Kleidung und Gesichter 1:1 übernehmen – dieselbe Kamera (außer es steht ausdrücklich Zoom/Sprung da), nur die Posen ändern sich wie beschrieben ({names}). "
                      f"ENDE-MOTIV: {ende}{LICHT}{sp}{GESICHT}{NOTE}")
            jobs.append({"id": sid + "B", "style": "scene", "out": f"{OUT}/{sid}B.jpg", "refs": refs, "prompt": prompt})
    fn = f"{E}/jobs_flow_{mode}{'_' + '_'.join(sorted(nur)) if nur and len(nur) < 6 else ''}.json"
    json.dump({"jobs": jobs}, open(fn, "w"), ensure_ascii=False, indent=1)
    miss = sorted({r for j in jobs for r in j["refs"] if not os.path.isfile(r) and not r.endswith(("A.jpg",))})
    print(mode, len(jobs), "Jobs ->", os.path.basename(fn), "| fehlende Referenzen:", [os.path.basename(m) for m in miss][:8])


if __name__ == "__main__":
    main()
