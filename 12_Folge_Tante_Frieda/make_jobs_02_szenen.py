#!/usr/bin/env python3
"""Welle 2 (2026-11-06): ein Startbild je Einstellung (SHxxx.jpg) fuer das Storyboard „Tante Frieda und Lorchen“.
Ohne Blender-Mockup (Runde 1): Referenz 1 = Raumszene/Ortsbild als Layout, dann CHAR-, dann OBJ-Sheets (max. 5 Referenzen).
Sprecher halbnah frontal, alle anderen mit geschlossenem Mund (Veo-Regeln). Aufruf: python3 make_jobs_02_szenen.py [SH010 ...]"""
import json, os, sys
E = os.path.dirname(os.path.abspath(__file__))
CH, OB, RA, OUT = (f"{E}/00_Charakter_Referenzbilder_Modelsheets", f"{E}/00_Objekt_Referenzbilder_Props",
                   f"{E}/00_Raum_Referenzbilder", f"{E}/03_Szenen_Flow_Bilder")
C = {"Maxi": "CHAR_01_Maxi_Turnaround_Modelsheet", "Hasi": "CHAR_02_Hasi_Kuschelhase_Modelsheet", "Mama": "CHAR_03_Mama_Katrin_Modelsheet",
     "Papa": "CHAR_04_Papa_Thomas_Modelsheet", "Opa": "CHAR_05_Opa_Heinrich_Modelsheet", "Anna": "CHAR_07_Anna_Freundin_Modelsheet",
     "Bello": "CHAR_09_Bello_Beagle_Modelsheet", "Frieda": "CHAR_13_Tante_Frieda_Modelsheet", "Lorchen": "CHAR_14_Lorchen_Papagei_Modelsheet"}
O = {"Kaefig": "OBJ_TF01_Lorchens_Messing_Kaefig", "Koffer": "OBJ_TF02_Friedas_Riesen_Rollkoffer", "Spruehr": "OBJ_TF03_Mamas_gruener_Blumensprueher",
     "Kuchen": "OBJ_TF04_Apfelkuchen_und_Kuchendose", "Stein": "OBJ_TF05_Annas_Glitzerstein", "Muetze": "OBJ_TF06_Opas_graue_Schiebermuetze",
     "Dose": "OBJ_TF07_Mut_Dose_und_Hasen_Stein", "Auto": "OBJ_05_Blaues_Familienauto_Kombi"}
R = {"EINF": "REF_Einfahrt_mit_Auto_aus_F02_SH030A", "VOR": "FLOW_CAM_03_Vorgarten_Gartentor_und_Veranda",
     "FLUR1": "FLOW_FLUR_CAM_01_Haustuer_Garderobe_Blick_Sued", "FLUR2": "FLOW_FLUR_CAM_02_Eingang_Blick_zur_Treppe_Nord",
     "KZ17": "FLOW_CAM_17_KZ_Kinderbett_mit_Hasi_Kissenburg_und_Eisenbahn", "KZ32": "FLOW_CAM_32_KZ_Kinderaugenhoehe_Bett_Hasi_Eisenbahn_und_Kissenburg",
     "ZAUN": "FLOW_CAM_33_Garten_Zauntor_zu_Anna_Hochbeet_und_Apfelbaum", "KU9": "FLOW_CAM_09_KU_Kuechenzeile_Tritthocker_und_6er_Esstisch",
     "KU10": "FLOW_CAM_10_KU_Gegenschuss_Esstisch_durch_Terrassentuer_in_Garten"}


def pfad(d, n):
    return f"{d}/{n}.jpg"


L_MITTAG = " LICHT: früher Nachmittag Mitte November, weiches graues Tageslicht, bedeckter Himmel, Bäume fast kahl, ein paar bunte Restblätter."
L_KAFFEE = " LICHT: Nachmittag Mitte November, warmes gemütliches Licht in der Küche, draußen hinter der Glastür bedeckter grauer Novemberhimmel."
L_DAEMM = " LICHT: Dämmerung, alle Fenster und Glastüren draußen dunkelblau, drinnen warmes gelbes Lampenlicht."
L_ABEND = " LICHT: später Abend, Fenster draußen schwarzblau (Nacht), warmes Licht einer Nachttischlampe."
KU_ARCH = (" KÜCHE (fest): salbeigrüne L-förmige Küchenzeile mit Holz-Arbeitsplatte nur an der linken Wand und der Fensterwand, weiße Bauernspüle "
           "unter einem Sprossenfenster; hinten die Glas-Schiebetür zur Terrasse; langer Holz-Esstisch mit Holzstühlen. Keine Kücheninsel, "
           "keine Hängelampen, keine Oberschränke über der Spüle.")
TAFEL = (" SITZORDNUNG KAFFEETAFEL (fest): an der Längsseite zur Kamera von links Maxi, Mama Katrin, Papa Thomas; an der linken Stirnseite "
         "Tante Frieda, an der rechten Stirnseite Opa Heinrich. Auf dem Tisch Apfelkuchen (OBJ_TF04), Kaffeetassen, eine Kaffeekanne.")
KAEFIG_KU = " Lorchens Messing-Käfig (OBJ_TF01) steht auf der Arbeitsplatte neben der Spüle."
KZ_ARCH = (" KINDERZIMMER (fest) wie Raum-Referenz: Maxis Kinderbett, Spielzeug-Eisenbahn, Kissenburg; Friedas pflaumenfarbener Riesenkoffer "
           "(OBJ_TF02) steht offen neben dem Bett, Lorchens Messing-Käfig (OBJ_TF01) steht auf dem Nachttisch.")
EIN_ARCH = (" EINFAHRT (fest) wie Referenz: graue Pflaster-Einfahrt vor der Garage, das kleine runde blaue Familienauto (OBJ_05) steht GERADE "
            "in der Einfahrt, Hauswand mit Sandkasten links.")
GESICHT = " GESICHTER: klar, sauber, symmetrisch, unverzerrt, exakt nach den Modelsheets; keine verzogenen Münder, keine schiefen Augen."
NOTE = (" Figuren und Kleidung exakt wie auf den Modelsheets, Ort exakt wie auf der Raum-Referenz. VERBOTE: keine weiteren Personen oder Tiere als genannt, "
        "kein Text, keine Untertitel, keine Sprechblasen, keine schwarzen Outlines; reiner 3D-Pixar-CGI-Look, Querformat 16:9.")

# id: (Raum, Figuren, Objekte, Licht, Motiv, Sprecher-Beschreibung oder None)
S = {
 "SH010": ("EINF", ["Frieda", "Maxi", "Mama"], ["Auto", "Kaefig"], L_MITTAG, "Das blaue Familienauto ist gerade angekommen. Tante Frieda ist hinten "
   "ausgestiegen, steht groß halbnah links vor dem Auto und reckt den Messing-Käfig mit dem grünen Papagei Lorchen wie eine Trophäe hoch, "
   "strahlt frontal in die Kamera und ruft. Rechts im Hintergrund an der Hauswand Mama Katrin und Maxi (Hasi im Arm), beide verdutzt." + EIN_ARCH,
   "Tante Frieda (pflaumenfarbene Strickjacke, links)"),
 "SH020": ("VOR", ["Maxi", "Hasi"], [], L_MITTAG, "Nah in Kinderaugenhöhe vor der Veranda: Maxi drückt Hasi fest an die Brust, die Augen werden zu "
   "entschlossenen Schlitzen, er spricht frontal in die Kamera.", "Maxi (blau-weiß gestreiftes Shirt, Mitte)"),
 "SH030": ("EINF", ["Frieda", "Papa"], ["Koffer", "Auto"], L_MITTAG, "Am offenen Kofferraum des blauen Autos: Papa Thomas zerrt mit beiden Händen "
   "an Friedas riesigem pflaumenfarbenem Rollkoffer (OBJ_TF02). Tante Frieda steht groß halbnah links frontal zur Kamera, zeigt mit ihrer "
   "Handtasche auf den Koffer und spricht befehlend." + EIN_ARCH, "Tante Frieda (links)"),
 "SH040": ("FLUR1", ["Frieda", "Mama"], [], L_MITTAG, "Flur: Tante Frieda steht groß halbnah frontal auf dem Flurläufer, schaut naserümpfend nach "
   "unten auf den Teppich und spricht abfällig. Hinten an der Haustür Mama Katrin mit erzwungenem Lächeln.", "Tante Frieda (Mitte)"),
 "SH041": ("FLUR1", ["Mama"], [], L_MITTAG, "Flur: Mama Katrin halbnah frontal, viel zu breites erzwungenes Lächeln, Hände vor der Brust "
   "gefaltet, flüstert sich selbst Ruhe zu.", "Mama Katrin (senfgelber Pullover)"),
 "SH050": ("KZ17", ["Frieda", "Hasi"], ["Kaefig", "Koffer"], L_MITTAG, "Kinderzimmer: Tante Frieda steht halbnah frontal neben Maxis Bett und "
   "hält Hasi mit spitzen zwei Fingern am Ohr weit von sich weg, angewidertes Gesicht, spricht." + KZ_ARCH, "Tante Frieda (Mitte)"),
 "SH051": ("KZ17", ["Maxi", "Hasi"], [], L_MITTAG, "Kinderzimmer, Kinderaugenhöhe: Maxi steht halbnah frontal und drückt Hasi beschützend an "
   "sich, empört, spricht energisch." + KZ_ARCH, "Maxi (Mitte)"),
 "SH060": ("KZ17", ["Frieda", "Lorchen", "Maxi"], ["Kaefig"], L_MITTAG, "Nah am Nachttisch: Tante Frieda beugt sich mit gespitztem Kussmund zum "
   "Gitter des Messing-Käfigs, der grüne Papagei Lorchen gibt ihr ein Schnabel-Küsschen. Frieda im Dreiviertelprofil zur Kamera, Gesicht gut "
   "sichtbar. Hinten unscharf Maxi, der angeekelt die Zunge herausstreckt (still).", "Tante Frieda (links)"),
 "SH070": ("ZAUN", ["Anna", "Maxi"], [], L_MITTAG, "Garten am gelben Zauntor zu Annas Haus: Anna sitzt rittlings oben auf dem niedrigen Gartentor "
   "(statt durchzugehen), halbnah frontal, zeigt mit dem Daumen über die Schulter Richtung Haus und fragt frech. Maxi steht rechts, Hasi im Arm (still).",
   "Anna (türkise Latzhose, auf dem Tor)"),
 "SH071": ("ZAUN", ["Anna", "Maxi"], ["Stein"], L_MITTAG, "Am Zauntor: Anna steht halbnah frontal und hält ihren funkelnden violetten "
   "Glitzerstein (OBJ_TF05) hoch, verschwörerisches Grinsen. Maxi rechts im Profil staunt (still).", "Anna (links)"),
 "SH072": ("ZAUN", ["Maxi", "Anna"], [], L_MITTAG, "Am Zauntor: Maxi halbnah frontal, entschlossen, schlägt mit Anna per Handschlag ein, Hasi "
   "unter den Arm geklemmt. Anna von hinten-seitlich angeschnitten links (still).", "Maxi (Mitte)"),
 "SH080": ("KZ32", ["Maxi", "Lorchen"], ["Spruehr", "Kaefig"], L_MITTAG, "Kinderzimmer, Kinderaugenhöhe: Maxi schleicht auf Zehenspitzen mit "
   "Mamas grünem Blumensprüher (OBJ_TF03) herein, frech-heimlicher Blick. Im Käfig auf dem Nachttisch drückt sich der Papagei Lorchen "
   "misstrauisch in die Ecke und hebt einen Fuß." + KZ_ARCH, None),
 "SH081": ("KZ32", ["Lorchen", "Maxi"], ["Kaefig", "Spruehr"], L_MITTAG, "Nah am Käfig: Maxi sprüht mit dem grünen Blumensprüher feinen "
   "Nebel in den Käfig. Lorchen ist begeistert, breitet nass die Flügel aus und dreht sich glücklich im Sprühnebel, Schnabel offen (wie rechte "
   "Hälfte von OBJ_TF01). Maxi am Bildrand völlig verdutzt.", "Lorchen, der grüne Papagei im Käfig (Mitte)"),
 "SH090": ("KZ17", ["Frieda", "Maxi", "Lorchen"], ["Kaefig"], L_MITTAG, "Kinderzimmer: Tante Frieda steht halbnah frontal in der Tür, Hände "
   "entsetzt an den Wangen, schaut auf den tropfnassen Papagei im Käfig. Maxi sitzt brav auf dem Bett mit einem Bilderbuch – verkehrt herum (still)." + KZ_ARCH,
   "Tante Frieda (in der Tür)"),
 "SH091": ("KZ32", ["Maxi", "Hasi"], [], L_MITTAG, "Maxi sitzt halbnah frontal auf seinem Bett, schaut mit unschuldigsten Kulleraugen über ein "
   "verkehrt herum gehaltenes Bilderbuch, Hasi neben sich, spricht.", "Maxi (Mitte)"),
 "SH093": ("KZ32", ["Lorchen"], ["Kaefig"], L_MITTAG, "Nah: der nasse Papagei Lorchen im Käfig auf dem Nachttisch schüttelt sich, Tropfen "
   "fliegen, starrt frech frontal und kreischt mit offenem Schnabel.", "Lorchen (Papagei, Mitte)"),
 "SH094": ("KZ17", ["Frieda", "Lorchen"], ["Kaefig"], L_MITTAG, "Tante Frieda halbnah frontal drückt den Messing-Käfig mit Lorchen beschützend "
   "an sich, hochmütig stolzer Blick, spricht." + KZ_ARCH, "Tante Frieda (Mitte)"),
 "SH100": ("KU9", ["Mama", "Frieda"], ["Kuchen", "Kaefig"], L_KAFFEE, "Küche: Mama Katrin stellt halbnah frontal den Apfelkuchen auf den Esstisch "
   "und spricht bittend in die Kamera. Links am Tisch sitzt Tante Frieda mit verschränkten Armen (still)." + KAEFIG_KU + KU_ARCH, "Mama Katrin (Mitte)"),
 "SH101": ("KU10", ["Frieda"], ["Kuchen"], L_KAFFEE, "Küche: Tante Frieda sitzt halbnah frontal am Esstisch, rückt ihre Brille an der Perlenkette "
   "zurecht, selbstgerecht, spricht." + KU_ARCH, "Tante Frieda (Mitte)"),
 "SH110": ("FLUR1", ["Opa"], ["Muetze"], L_KAFFEE, "Flur, Haustür offen: Opa Heinrich steht halbnah frontal in der Tür, nimmt fröhlich seine graue "
   "Schiebermütze (OBJ_TF06) ab, darunter glänzt seine Glatze, ruft herzlich.", "Opa Heinrich (Mitte)"),
 "SH111": ("FLUR1", ["Frieda"], [], L_KAFFEE, "Flur: Tante Frieda halbnah frontal, zeigt mit ausgestrecktem Finger nach oben auf Opas Kopf "
   "(außerhalb des Bildes), gespielt entsetzt, spricht.", "Tante Frieda (Mitte)"),
 "SH112": ("FLUR1", ["Opa"], ["Muetze"], L_KAFFEE, "Flur: Opa Heinrich halbnah frontal, grinst verschmitzt und streicht sich über die Glatze, "
   "Mütze in der Hand, spricht.", "Opa Heinrich (Mitte)"),
 "SH120": ("KU10", ["Frieda", "Maxi", "Mama", "Papa", "Opa"], ["Kuchen"], L_KAFFEE, "Kaffeetafel-Totale: alle sitzen am Tisch. Tante Frieda an der "
   "linken Stirnseite kaut und verzieht angewidert das Gesicht, ihr Gesicht zur Kamera gedreht, spricht." + TAFEL + KU_ARCH, "Tante Frieda (links)"),
 "SH122": ("KU10", ["Frieda", "Papa"], ["Kuchen"], L_KAFFEE, "Kaffeetafel: Tante Frieda halbnah frontal zeigt mit der Kuchengabel nach rechts "
   "auf Papa Thomas, spöttisch. Papa rechts angeschnitten (still)." + KU_ARCH, "Tante Frieda (links)"),
 "SH123": ("KU10", ["Papa"], [], L_KAFFEE, "Kaffeetafel: Papa Thomas halbnah frontal, die Kaffeetasse auf halbem Weg zum Mund erstarrt, "
   "trockene Miene, spricht.", "Papa Thomas (olivgrünes T-Shirt)"),
 "SH124": ("KU10", ["Maxi", "Hasi"], [], L_KAFFEE, "Kaffeetafel: Maxi halbnah frontal, rotes wütendes Gesicht, flüstert Hasi ins Ohr.",
   "Maxi (Mitte)"),
 "SH130": ("KU9", ["Maxi", "Lorchen", "Anna"], ["Kaefig"], L_KAFFEE, "Nah an der Arbeitsplatte neben der Spüle: Maxi flüstert halbnah im "
   "Dreiviertelprofil (Gesicht gut sichtbar) ans Gitter des Messing-Käfigs, Lorchen hört aufmerksam zu. Hinten an der Glas-Schiebetür drückt "
   "Anna draußen die Nase an die Scheibe und zeigt Daumen hoch (still)." + KU_ARCH, "Maxi (vorne)"),
 "SH140": ("KU10", ["Frieda"], ["Kuchen"], L_KAFFEE, "Kaffeetafel: Tante Frieda halbnah frontal hält die Kaffeetasse hoch und mäkelt.",
   "Tante Frieda (Mitte)"),
 "SH141": ("KU9", ["Lorchen"], ["Kaefig"], L_KAFFEE, "Nah: Lorchen im Messing-Käfig auf der Arbeitsplatte plustert sich auf, Schnabel weit "
   "offen, plappert frech frontal zur Kamera." + KU_ARCH, "Lorchen (Papagei)"),
 "SH143": ("KU10", ["Opa"], [], L_KAFFEE, "Kaffeetafel: Opa Heinrich halbnah frontal prustet vor Lachen los, haut mit der flachen Hand auf den "
   "Tisch, Lachtränen.", "Opa Heinrich (Mitte)"),
 "SH144": ("KU9", ["Lorchen"], ["Kaefig"], L_KAFFEE, "Nah: Lorchen im Käfig legt den Kopf schief, Schnabel offen, frech frontal.",
   "Lorchen (Papagei)"),
 "SH150": ("KU10", ["Frieda"], [], L_KAFFEE, "Kaffeetafel: Tante Frieda steht auf, halbnah frontal, die Nasenspitze ist weiß, sie reibt sie, "
   "empört und streng, spricht.", "Tante Frieda (Mitte)"),
 "SH151": ("KU10", ["Maxi", "Hasi"], [], L_KAFFEE, "Kaffeetafel: Maxi halbnah frontal hält Hasi vor sein halbes Gesicht wie ein Sprecher, "
   "kleinlaut, Mund sichtbar.", "Maxi (Mitte)"),
 "SH152": ("KU10", ["Maxi", "Hasi"], [], L_KAFFEE, "Kaffeetafel: Maxi ist aufgestanden, halbnah frontal, Hasi gesenkt, mutiger ehrlicher Blick, "
   "spricht laut.", "Maxi (Mitte)"),
 "SH160": ("KU9", ["Frieda", "Lorchen"], ["Kaefig"], L_KAFFEE, "Küche: Tante Frieda halbnah frontal nimmt den Messing-Käfig mit Lorchen "
   "entschlossen von der Arbeitsplatte, gekränkt und stur, spricht." + KU_ARCH, "Tante Frieda (Mitte)"),
 "SH170": ("FLUR2", ["Maxi", "Hasi", "Papa", "Frieda"], ["Koffer"], L_DAEMM, "Flur in der Dämmerung: Maxi sitzt traurig vorn auf der untersten "
   "Treppenstufe, Hasi mit dem Gesicht nach unten auf den Knien. Hinten trägt Papa Thomas den pflaumenfarbenen Riesenkoffer zur Haustür, "
   "Tante Frieda knöpft ihren Mantel zu.", None),
 "SH171": ("FLUR2", ["Maxi", "Hasi"], [], L_DAEMM, "Flur, Dämmerung: Maxi halbnah frontal auf der untersten Treppenstufe, traurig, Hasi im "
   "Schoß, spricht leise.", "Maxi (Mitte)"),
 "SH172": ("FLUR1", ["Lorchen"], ["Kaefig", "Koffer"], L_DAEMM, "Flur, Dämmerung: Lorchens Messing-Käfig steht auf dem pflaumenfarbenen "
   "Koffer an der Haustür; Lorchen sitzt still und traurig zusammengekauert auf der Stange, Schnabel leicht offen.", "Lorchen (Papagei)"),
 "SH173": ("FLUR1", ["Frieda"], [], L_DAEMM, "Flur, Dämmerung: Tante Frieda halbnah frontal im Mantel, erstarrt, die Augen glänzen feucht, "
   "sie reibt sich die Nase, zum ersten Mal verletzlich.", None),
 "SH180": ("FLUR1", ["Maxi", "Frieda"], ["Kuchen"], L_DAEMM, "Flur, Dämmerung: Maxi steht halbnah frontal und hält Tante Frieda mit beiden "
   "Händen die himmelblaue Kuchendose (OBJ_TF04) hin, schüchtern lächelnd. Frieda links angeschnitten (still).", "Maxi (Mitte)"),
 "SH181": ("FLUR1", ["Frieda"], ["Kuchen"], L_DAEMM, "Flur, Dämmerung: Tante Frieda halbnah frontal hält die himmelblaue Kuchendose, schaut "
   "zur Seite, ein kleines verlegenes Lächeln, spricht leise.", "Tante Frieda (Mitte)"),
 "SH182": ("FLUR1", ["Mama"], [], L_DAEMM, "Flur, Dämmerung: Mama Katrin halbnah frontal, platzt vor Freude, breitet die Arme weit aus, "
   "strahlt.", "Mama Katrin (Mitte)"),
 "SH183": ("FLUR1", ["Maxi", "Hasi"], [], L_DAEMM, "Flur, Dämmerung: Maxi halbnah frontal grinst schief, Hasi im Arm, spricht.", "Maxi (Mitte)"),
 "SH184": ("FLUR1", ["Lorchen"], ["Kaefig", "Koffer"], L_DAEMM, "Flur, Dämmerung: Lorchen hüpft im Messing-Käfig auf dem Koffer fröhlich "
   "auf der Stange, Flügel halb offen, Schnabel offen.", "Lorchen (Papagei)"),
 "SH190": ("EINF", ["Frieda", "Mama", "Opa", "Maxi"], ["Auto", "Kaefig"], L_DAEMM, "Einfahrt in der Dämmerung: das blaue Auto mit "
   "leuchtenden Scheinwerfern fährt los, Tante Frieda winkt aus dem Beifahrerfenster, Lorchens Käfig auf ihrem Schoß. Vorn winken Mama, Opa und "
   "Maxi (Rücken halb zur Kamera, Gesichter im Profil)." + EIN_ARCH, None),
 "SH195": ("ZAUN", ["Maxi", "Anna"], ["Stein"], L_DAEMM, "Garten am gelben Zauntor in der Dämmerung, Licht aus der Terrassentür: Anna hält Maxi "
   "über das Tor den violetten Glitzerstein hin; Maxi halbnah frontal schüttelt lächelnd den Kopf und schiebt ihre Hand sanft zurück.",
   "Maxi (rechts)"),
 "SH200": ("KZ32", ["Maxi", "Hasi", "Papa"], [], L_ABEND, "Kinderzimmer am Abend: Maxi hüpft im Schlafanzug-losen Standardoutfit glücklich mit "
   "Hasi in sein eigenes Bett, halbnah frontal, jubelt; Papa Thomas wirft lachend die Decke hinterher (still). Kein Käfig, kein Koffer mehr.",
   "Maxi (Mitte)"),
 "SH201": ("KZ32", ["Opa", "Maxi"], ["Dose"], L_ABEND, "Kinderzimmer am Abend: Opa Heinrich sitzt halbnah frontal auf der Bettkante und hält die "
   "alte rote Blechdose (OBJ_TF07) offen hin, stolz und warm, spricht; Maxi lässt seinen Kieselstein mit dem gemalten Hasen hineinfallen (still).",
   "Opa Heinrich (Mitte)"),
 "SH210": ("KZ17", ["Maxi", "Hasi", "Mama", "Papa", "Opa", "Bello"], [], L_ABEND, "Kinderzimmer-Totale am Abend: Maxi steht auf seinem Bett und "
   "reckt Hasi hoch, Mama, Papa und Opa davor heben jubelnd die Arme, Bello springt bellend; alle Gesichter zur Kamera. Kein Käfig, kein Koffer.",
   "Maxi (Mitte, auf dem Bett)"),
}

nur = set(sys.argv[1:])
jobs = []
for sid, (raum, figs, objs, licht, motiv, sprecher) in S.items():
    if nur and sid not in nur:
        continue
    refs = [pfad(RA, R[raum])] + [pfad(CH, C[f]) for f in figs] + [pfad(OB, O[o]) for o in objs]
    refs = refs[:5]  # Bildwerkzeug: hoechstens 5 Referenzen
    names = "; ".join(f"Referenz {i+1} = {os.path.basename(r)[:-4]}" for i, r in enumerate(refs))
    if sprecher:
        sp = (f" SPRECHER-EINSTELLUNG: {sprecher} ist der EINZIGE Sprecher – groß im Bild, Gesicht zur Kamera, Mund gut sichtbar und leicht "
              "geöffnet. " + ("Alle anderen Figuren schweigen mit geschlossenem Mund." if len(figs) > 1 else ""))
    else:
        sp = " STUMME EINSTELLUNG: niemand spricht, alle Münder geschlossen."
    prompt = (f"EINSTELLUNG {sid} der Folge „Tante Frieda und Lorchen“ (Samstag, 14. November). Referenz 1 ist die Raumszene des Ortes: "
              f"Raum, Möbel, Wandfarben exakt übernehmen, Kamera frei für die beschriebene Einstellung ({names}). MOTIV: {motiv}{licht}{sp}{GESICHT}{NOTE}")
    jobs.append({"id": sid, "style": "scene", "out": f"{OUT}/{sid}.jpg", "refs": refs, "prompt": prompt})
fn = f"{E}/jobs_02_szenen{'_' + '_'.join(sorted(nur)) if nur and len(nur) < 6 else ''}.json"
json.dump({"jobs": jobs}, open(fn, "w"), ensure_ascii=False, indent=1)
miss = sorted({r for j in jobs for r in j["refs"] if not os.path.isfile(r)})
print(len(jobs), "Jobs ->", os.path.basename(fn), "| fehlende Referenzen:", [os.path.basename(m) for m in miss])
