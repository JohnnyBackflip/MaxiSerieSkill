#!/usr/bin/env python3
"""
Rendert alle 24 vom 5-köpfigen Produktionskomitee (@regie, @story-layout,
@rigging-animation, @lighting-rendering, @audio-tonmeister) beschlossenen
Standard-Kameraperspektiven aus Maxis_Haus_Komplett_Blockout.blend.
"""

import os
import bpy
from mathutils import Vector

BLEND_PATH = "/home/felix/projects/dump/Maxis_Welt_Korrekturmappe/03_Blender_3D_Haus_Blockout/Maxis_Haus_Komplett_Blockout.blend"
OUT_DIR = "/home/felix/projects/dump/Maxis_Welt_Korrekturmappe/04_Komitee_Kameraplan_und_Flow_Raumszenen/03_Blender_Kamera_Screenshots"

COMMITTEE_CAMERAS = [
    # Bereich 1: Straße, Bürgersteig & Nachbarhäuser (3 Kameras)
    ("KOM_CAM_01_Strasse_Totale_Drei_Haeuser", (0.00, -52.00, 18.50), (0.00, 0.00, 2.50), 22.0),
    ("KOM_CAM_02_Buergersteig_Strassenverlauf_und_Zebrastreifen", (-26.50, -17.80, 2.15), (8.00, -15.50, 1.80), 19.0),
    ("KOM_CAM_03_Vorgarten_Gartentor_und_Veranda", (2.40, -21.50, 2.65), (0.60, -6.50, 2.10), 21.0),
    # Bereich 2: Großer Hausgarten hinterm Haus (3 Kameras)
    ("KOM_CAM_04_Garten_Totale_Wiese_Sandkasten_und_Schaukel", (2.50, 25.50, 5.40), (-0.50, 8.50, 2.30), 20.0),
    ("KOM_CAM_05_Holzterrasse_und_Apfelbaum_Schaukel", (5.80, 8.80, 2.05), (-10.50, 11.20, 1.95), 20.0),
    ("KOM_CAM_06_Opas_Gartenschuppen_Werkbank_und_Sandkasten", (-1.50, 8.20, 2.05), (10.20, 14.20, 1.65), 20.0),
    # Bereich 3: Wohnzimmer im EG (2 Kameras - inkl. 1 runder Deckenleuchte & Stehlampe in der Süd-West-Ecke!)
    ("KOM_CAM_07_WZ_Sofa_Sessel_Teppich_und_Kuechendurchblick", (-1.60, -5.45, 1.55), (-6.60, -2.15, 1.22), 17.5),
    ("KOM_CAM_08_WZ_Gegenschuss_TV_Board_und_Flurdurchgang", (-7.15, -0.45, 1.55), (-3.85, -4.65, 1.22), 16.5),
    # Bereich 4: Familienküche im EG (2 Kameras - inkl. 1 runder Deckenleuchte!)
    ("KOM_CAM_09_KU_Kuechenzeile_Tritthocker_und_6er_Esstisch", (-1.65, 1.15, 1.55), (-6.40, 4.30, 1.22), 17.5),
    ("KOM_CAM_10_KU_Gegenschuss_Esstisch_durch_Terrassentuer_in_Garten", (-6.85, 1.15, 1.55), (-2.85, 6.20, 1.25), 17.5),
    # Bereich 5: Großes Spielzimmer im EG (2 Kameras - inkl. 1 runder Deckenleuchte!)
    ("KOM_CAM_11_SZ_Totale_Indoor_Rutsche_Maltisch_und_Kuschelecke", (2.55, -1.65, 1.58), (5.55, 3.35, 1.20), 17.5),
    ("KOM_CAM_12_SZ_Gegenschuss_Wuerfelregal_und_Spielteppich", (7.65, 5.45, 1.58), (4.35, -1.05, 1.20), 17.5),
    # Bereich 6: Gästeklo im EG (2 Kameras - inkl. 1 runder Deckenleuchte!)
    ("KOM_CAM_13_GK_Waschbecken_Spiegel_Tritthocker_und_WC", (2.55, -5.75, 1.48), (6.20, -3.25, 1.26), 17.0),
    ("KOM_CAM_14_GK_Gegenschuss_WC_und_Waschplatz", (7.80, -5.75, 1.48), (4.40, -3.15, 1.26), 17.0),
    # Bereich 7: Flur & Treppenhaus EG/OG (2 Kameras - inkl. 2 runden Flur-Deckenleuchten!)
    ("KOM_CAM_15_FL_Erdgeschoss_Haustuer_Garderobe_und_Treppe", (0.25, 5.35, 1.55), (0.35, -4.80, 1.25), 18.0),
    ("KOM_CAM_16_FL_Obergeschoss_Galerie_und_Dachbodentreppe", (1.35, 5.30, 4.30), (-0.10, -3.50, 4.05), 17.5),
    # Bereich 8: Maxis Kinderzimmer im 1. OG (2 Kameras - inkl. 1 runder Deckenleuchte!)
    ("KOM_CAM_17_KZ_Kinderbett_mit_Hasi_Kissenburg_und_Eisenbahn", (-1.65, -4.35, 4.30), (-6.15, 1.35, 3.88), 17.5),
    ("KOM_CAM_18_KZ_Gegenschuss_Eisenbahnteppich_Kleiderschrank_und_Buecherregal", (-5.45, 5.35, 4.30), (-3.20, -3.60, 3.88), 17.5),
    # Bereich 9: Elternzimmer im 1. OG (2 Kameras - inkl. 1 runder Deckenleuchte!)
    ("KOM_CAM_19_EZ_Doppelbett_Nachttische_und_Gartenfenster", (7.65, 1.05, 4.30), (3.75, 4.10, 3.94), 17.5),
    ("KOM_CAM_20_EZ_Gegenschuss_Lesesessel_Kleiderschrank_und_Kommode", (2.60, 5.50, 4.30), (6.35, 1.85, 3.95), 17.5),
    # Bereich 10: Familien-Badezimmer mit Badewanne im 1. OG (2 Kameras - inkl. 1 runder Deckenleuchte!)
    ("KOM_CAM_21_BD_Doppelwaschtisch_Tritthocker_und_Freistehende_Badewanne", (2.45, -5.55, 4.32), (5.35, -1.85, 3.90), 17.0),
    ("KOM_CAM_22_BD_Freistehende_Badewanne_Nah_und_WalkIn_Dusche", (2.55, -0.55, 4.28), (6.35, -2.75, 3.92), 17.0),
    # Bereich 11: Großer Dachboden im DG (2 Kameras - inkl. 2 runden Deckenleuchten an den Kehlbalken!)
    ("KOM_CAM_23_DB_Dachbalken_Schatztruhe_Fernrohr_und_Giebelfenster", (-7.20, -1.20, 6.70), (4.50, 0.40, 6.40), 18.0),
    ("KOM_CAM_24_DB_Kinder_Geheimversteck_Laterne_und_Kisten", (6.80, -1.00, 6.70), (-4.80, 1.80, 6.40), 18.0),
    # Bereich 12: Einfahrt & Familien-Garage mit großer Werkbank (3 Kameras - inkl. 1 runder Garagen-Deckenleuchte!)
    ("KOM_CAM_25_GAR_Einfahrt_und_Offenes_Garagentor_Aussen", (13.80, -20.50, 2.35), (14.10, -3.50, 1.55), 20.0),
    ("KOM_CAM_26_GAR_Innen_Werkbank_Schraubstock_und_Werkzeugwand", (13.20, -5.20, 1.62), (14.40, 1.60, 1.25), 17.5),
    ("KOM_CAM_27_GAR_Gegenschuss_Werkbank_durch_Tor_zur_Einfahrt", (15.60, 1.20, 1.65), (13.40, -8.50, 1.28), 17.5),
    # Bereich 13 (NEU – Komitee-Zusatzperspektiven für Nachbarhäuser & Schlüsselszenen):
    ("KOM_CAM_28_Anna_Nachbarhaus_Ahornweg2_Vorgarten_und_Wintergarten", (-28.50, -21.80, 2.75), (-33.20, -4.50, 2.50), 20.0),
    ("KOM_CAM_29_Ben_Nachbarhaus_Ahornweg6_Hof_Skaterampe_und_Basketballkorb", (29.20, -21.50, 2.80), (34.80, -3.50, 2.50), 19.5),
    ("KOM_CAM_30_WZ_Frontal_Gebluemtes_Familiensofa_und_Vorlesesessel", (-2.15, -3.15, 1.38), (-7.20, -2.95, 1.15), 17.5),
    ("KOM_CAM_31_KU_Nah_Maxis_Tritthocker_Spuele_und_Kuechenzeile", (-3.65, 1.25, 1.50), (-7.25, 4.75, 1.35), 17.0),
    ("KOM_CAM_32_KZ_Kinderaugenhoehe_Bett_Hasi_Eisenbahn_und_Kissenburg", (-1.95, -1.10, 3.65), (-6.85, -1.35, 3.55), 16.0),
    ("KOM_CAM_33_Garten_Zauntor_zu_Anna_Hochbeet_und_Apfelbaum", (-9.20, -1.80, 1.95), (-15.50, 7.50, 1.75), 18.5),
    # Bereich 14 (NEU – Wiederverwendbare Szenen-Kameras für Folge 1 "Die große Kissen-Expedition" & Folgegeschichten):
    ("KOM_CAM_34_WZ_Teppichkante_Blick_auf_Parkett_und_Kuechendurchgang", (-5.20, -3.60, 1.15), (-3.80, 2.20, 1.10), 17.5),
    ("KOM_CAM_35_WZ_zu_KU_Kissenbruecke_Durchgang_Korridor", (-3.10, -2.40, 1.25), (-3.00, 5.80, 1.15), 17.5),
    ("KOM_CAM_36_KU_Terrassentuer_Schwelle_Nah_Gartenblick", (-4.45, 4.15, 1.12), (-2.50, 8.80, 1.05), 17.5),
    ("KOM_CAM_37_Garten_Picknickmatte_Nah_Apfelbaum_und_Haus", (1.80, 16.80, 1.25), (-4.80, 11.80, 1.35), 18.5),
]


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    bpy.ops.wm.open_mainfile(filepath=BLEND_PATH)
    scene = bpy.context.scene
    scene.render.resolution_x = 1600
    scene.render.resolution_y = 1000
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'

    # Alle Sammlungen & Objekte sichtbar schalten
    for col in bpy.data.collections:
        col.hide_render = False
    for obj in bpy.data.objects:
        obj.hide_render = False

    col_name = "99_Komitee_Standard_Kameras"
    col_cam = bpy.data.collections.get(col_name)
    if col_cam is None:
        col_cam = bpy.data.collections.new(col_name)
        scene.collection.children.link(col_cam)

    for name, loc, target, lens in COMMITTEE_CAMERAS:
        old = bpy.data.objects.get(name)
        if old:
            bpy.data.objects.remove(old, do_unlink=True)
        cdata = bpy.data.cameras.new(name=name)
        cdata.lens = lens
        cdata.clip_start = 0.08
        cdata.clip_end = 250.0
        cobj = bpy.data.objects.new(name=name, object_data=cdata)
        cobj.location = Vector(loc)
        direction = Vector(target) - Vector(loc)
        cobj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
        col_cam.objects.link(cobj)

        scene.camera = cobj
        out_file = os.path.join(OUT_DIR, f"{name}.png")
        if os.environ.get("ONLY_NEW") == "1" and os.path.exists(out_file):
            continue
        scene.render.filepath = out_file
        bpy.ops.render.render(write_still=True)
        print(f"Gerendert: {out_file}")

    bpy.ops.wm.save_as_mainfile(filepath=BLEND_PATH)
    print("Alle 24 Komitee-Kameras gerendert und in .blend gespeichert!")


if __name__ == "__main__":
    main()
