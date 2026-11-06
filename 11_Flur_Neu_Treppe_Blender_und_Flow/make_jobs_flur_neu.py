import json, os
import os
K = os.environ.get("MAXI_ROOT", os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")))
D = f"{K}/11_Flur_Neu_Treppe_Blender_und_Flow"
R = f"{K}/04_Komitee_Kameraplan_und_Flow_Raumszenen/04_Flow_Gemalte_Raumszenen"
STYLE = [f"{R}/FLOW_CAM_07_WZ_Sofa_Sessel_Teppich_und_Kuechendurchblick.jpg",
         f"{R}/FLOW_CAM_09_KU_Kuechenzeile_Tritthocker_und_6er_Esstisch.jpg"]
FLUR = ("Der Flur von Maxis Familienhaus: langer, gerader Flur (3,2 m breit, 12,6 m lang), Wände warmes Cremeweiß, "
        "Boden helles Eichenparkett, Decke hell mit runden flachen Deckenleuchten, Türen und Zargen aus mittelbraunem Holz. "
        "Haustür an der Stirnseite im Süden (Holztür mit kleinem Fenster), daneben Schuhbank aus Holz und Garderobe mit Hakenleiste, "
        "daran eine rote und eine blaue Jacke. Breiter offener Durchgang zum Wohnzimmer. "
        "TREPPE (wichtig, muss baulich korrekt sein): eine normale, gerade, einläufige Holztreppe, die FEST AUF DEM BODEN STEHT und "
        "an der Wand entlang nach oben ins Obergeschoss führt; geschlossene Stufen mit hellen Setzstufen und Holz-Trittflächen, "
        "dunkle Holzwange, weiße Geländerstäbe und dunkler Holzhandlauf auf der offenen Seite. Keine schwebenden, hängenden "
        "oder auf dem Kopf stehenden Stufen, keine Treppe an der Decke, keine Wendeltreppe.")
LAYOUT = ("Aufbau und Perspektive EXAKT wie auf dem Blender-Kamerabild (Referenz 1 – nur als Layout, dessen Klötzchen-Look, "
          "Linien und Flächenfarben NICHT übernehmen). Pixar-Innenraum-Stil, Materialien, Farben und Licht wie die bestehenden "
          "Raumszenen Wohnzimmer (Referenz 2) und Küche (Referenz 3) desselben Hauses.")
END = (" LICHT: heller Vormittag, warmes Tageslicht durch Fenster und Türglas, Deckenleuchten aus. "
       "VERBOTE: keine Personen, keine Tiere, kein Text, keine Schrift, keine schwarzen Outlines; reiner 3D-Pixar-CGI-Look, Querformat 16:9.")
CAMS = {
 "FLUR_CAM_01_Haustuer_Garderobe_Blick_Sued":
   "MOTIV: Blick den Flur entlang auf die geschlossene Haustür am Ende; rechts die Schuhbank und die Garderobe mit Jacken, "
   "rechts vorn der breite offene Durchgang ins Wohnzimmer (Sofa angeschnitten sichtbar), links eine Holztür. Die Treppe liegt hinter der Kamera und ist NICHT im Bild.",
 "FLUR_CAM_02_Eingang_Blick_zur_Treppe_Nord":
   "MOTIV: Gegenschuss von der Haustür-Seite den Flur hinunter: rechts steht die gerade Holztreppe, beginnt unten auf dem Parkett und steigt an der rechten Wand nach hinten ins Obergeschoss, "
   "mit weißen Stäben und Handlauf auf der zum Flur offenen Seite; rechts vorn eine offene Tür, links Türen und der Durchgang in die Küche, am Ende ein Fenster mit Garten.",
 "FLUR_CAM_03_Kinderaugenhoehe_Haustuer_und_Garderobe":
   "MOTIV: Kinderaugenhöhe (0,95 m), nah an der Haustür: die Haustür steht halb offen, draußen der sonnige Vorgarten mit Gartenzaun; rechts die Schuhbank mit Gummistiefeln und darüber die Garderobe mit roter und blauer Jacke.",
 "FLUR_CAM_04_Treppenfuss_Nah_Blick_nach_oben":
   "MOTIV: am Treppenfuß, Blick schräg die gerade Holztreppe hinauf ins helle Obergeschoss; deutlich der Antrittspfosten, die weißen Geländerstäbe auf jeder Stufe, der dunkle Handlauf und die geschlossene Wange bis zum Boden; links ein Türrahmen und ein Fenster mit Garten.",
 "FLUR_CAM_05_OG_Galerie_und_Dachbodentreppe":
   "MOTIV: oberer Flur / Galerie im Obergeschoss: links vorn das Galeriegeländer (weiße Stäbe, dunkler Handlauf) über dem Treppenloch, der Flur läuft gerade nach hinten, Türen zu Kinderzimmer, Bad und Elternzimmer, "
   "am Ende eine schmale gerade Holztreppe, die ebenfalls fest auf dem Boden steht und zum Dachboden hinaufführt.",
}
jobs = []
for name, motiv in CAMS.items():
    jobs.append(dict(id=name[:12], style="scene", out=f"{D}/FLOW_{name}.jpg",
                     refs=[f"{D}/{name}.png"] + STYLE,
                     prompt=f"LEERE Flow-Raumszene (Referenzbild) für die Kamera {name}. {LAYOUT} {FLUR} {motiv}{END}"))
json.dump({"jobs": jobs}, open(f"{D}/jobs_flur_neu.json", "w"), ensure_ascii=False, indent=1)
print(len(jobs))
