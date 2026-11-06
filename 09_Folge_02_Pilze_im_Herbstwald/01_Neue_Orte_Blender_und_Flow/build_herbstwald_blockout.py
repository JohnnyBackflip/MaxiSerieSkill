#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Neuer, wiederverwendbarer Ort für Maxis Welt: HERBSTWALD mit Landstraße, Waldparkplatz, Waldweg und Pilzlichtung.
Baut Herbstwald_Blockout.blend (ohne Figuren, ohne Auto) und rendert die leeren Standard-Kameras WALD_CAM_01..06.

Aufruf:  blender -b --factory-startup --python build_herbstwald_blockout.py
"""
import os, sys, math, random
import bpy
from mathutils import Vector

K = os.environ.get("MAXI_ROOT", os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")))
sys.path.insert(0, K)
import maxi_blender_lib as L  # noqa: E402

OUT_DIR = os.path.join(K, "09_Folge_02_Pilze_im_Herbstwald", "01_Neue_Orte_Blender_und_Flow")
OUT_BLEND = os.path.join(OUT_DIR, "Herbstwald_Blockout.blend")

# Koordinaten (Welt): Landstraße entlang X bei y=0; Wald nördlich (y>4) und östlich; Parkplatz x 2..12, y 4..10;
# Waldweg von (12, 10) nach Norden bis y=62 (Breite 2.2); Baumwurzel-Spot bei (14.5, 30); Lichtung um (10.5, 48).
CAMERAS = [
    ("WALD_CAM_01_Landstrasse_zum_Waldrand",            (-16.0, -7.5, 2.2),  (6.0, 1.0, 1.3),    22.0),
    ("WALD_CAM_02_Waldparkplatz_mit_Holzschild",        (0.5, 0.5, 1.7),     (9.0, 8.5, 1.1),    20.0),
    ("WALD_CAM_03_Waldweg_Totale",                      (12.0, 12.5, 1.45),  (12.2, 32.0, 1.0),  20.0),
    ("WALD_CAM_04_Waldweg_Nah_Baumwurzel_Kinderaugenhoehe", (11.3, 26.8, 0.95), (14.0, 29.6, 0.45), 24.0),
    ("WALD_CAM_05_Pilzlichtung_Baumstumpf",             (14.0, 44.6, 1.35),  (10.4, 48.4, 0.55), 22.0),
    ("WALD_CAM_06_Giftpilz_Stelle_Nah_Kinderaugenhoehe", (14.9, 38.2, 0.85), (16.6, 39.7, 0.35), 30.0),
    ("WALD_CAM_07_Giftpilz_Stelle_Totale_vom_Waldweg",   (12.8, 36.4, 1.4),  (16.4, 39.8, 0.6),  22.0),
    # Tunnel am Waldrand (Charakterbibel v2.1, Kap. 5.2): Durchlass unter dem Feldwegdamm westlich des Parkplatzes, Achse entlang X bei y=7.5
    ("TUNNEL_CAM_01_Eingang_Kinderaugenhoehe",           (3.2, 7.5, 0.95),   (-12.0, 7.5, 0.7),  24.0),
    ("TUNNEL_CAM_02_Innen_Blick_zum_Ausgang",            (-1.0, 7.5, 0.9),   (-14.0, 7.5, 0.75), 20.0),
    ("TUNNEL_CAM_03_Ausgang_Gegenschuss_Wiese",          (-16.5, 9.2, 1.1),  (-12.0, 7.5, 0.7),  24.0),
    ("TUNNEL_CAM_04_Totale_vom_Parkplatz_auf_Damm",      (6.0, 2.2, 1.7),    (-6.0, 9.0, 1.2),   20.0),
]


def clear_scene():
    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o, do_unlink=True)
    for c in list(bpy.data.collections):
        bpy.data.collections.remove(c)


def main():
    clear_scene()
    scene = bpy.context.scene
    col_ground = L.get_collection("00_Boden_Strasse_Parkplatz")
    col_forest = L.get_collection("01_Herbstwald_Baeume")
    col_path = L.get_collection("02_Waldweg_und_Lichtung")
    col_props = L.get_collection("03_Pilze_und_Details")
    col_light = L.get_collection("98_Beleuchtung")
    col_cam = L.get_collection("99_Kameras")

    m_grass = L.mat("MAT_Wiese", (0.42, 0.60, 0.25, 1))
    m_grass_dark = L.mat("MAT_Waldboden", (0.36, 0.30, 0.18, 1))
    m_road = L.mat("MAT_Asphalt", (0.36, 0.36, 0.38, 1))
    m_line = L.mat("MAT_Fahrbahnlinie", (0.95, 0.95, 0.90, 1))
    m_gravel = L.mat("MAT_Kies", (0.72, 0.68, 0.60, 1))
    m_path = L.mat("MAT_Waldweg_Erde", (0.55, 0.42, 0.26, 1))
    m_wood = L.mat("MAT_Holz_Schild", (0.60, 0.42, 0.22, 1))
    m_stone = L.mat("MAT_Stein_Grau", (0.60, 0.60, 0.58, 1))

    # ---- Boden
    L.box("Wiese_Sued", (-20, -30, -0.05), (160, 54, 0.1), m_grass, col_ground)
    L.box("Wiese_Nord", (-20, 30, -0.05), (160, 54, 0.1), m_grass, col_ground)
    L.box("Waldboden_Ost", (40, 35, -0.04), (80, 80, 0.1), m_grass_dark, col_ground)
    L.box("Landstrasse", (-20, 0, 0.0), (160, 6.0, 0.06), m_road, col_ground)
    for i in range(-80, 60, 4):
        L.box(f"Mittelstreifen_{i}", (i + 1, 0, 0.035), (2.0, 0.14, 0.01), m_line, col_ground)
    L.box("Parkplatz_Kies", (7, 7, 0.02), (10.0, 6.0, 0.06), m_gravel, col_ground)
    L.box("Parkplatz_Zufahrt", (7, 3.5, 0.02), (4.0, 1.2, 0.06), m_gravel, col_ground)
    for i, x in enumerate((2.3, 4.6, 6.9, 9.2, 11.5)):
        L.cyl(f"Parkplatz_Holzpoller_{i}", (x, 10.1, 0.3), 0.12, 0.6, m_wood, col_ground, verts=10)
    # Holzschild "Wald" (ohne Text)
    L.cyl("Schild_Pfosten", (12.4, 4.6, 0.9), 0.07, 1.8, m_wood, col_ground, verts=10)
    L.box("Schild_Brett", (12.4, 4.6, 1.65), (0.9, 0.06, 0.4), m_wood, col_ground)
    L.box("Schild_Pfeil", (12.75, 4.6, 1.65), (0.3, 0.07, 0.25), m_wood, col_ground, rot_z=0)

    # ---- Waldweg (Erde) + Lichtung
    L.box("Waldweg", (12.2, 36, 0.01), (2.2, 52, 0.04), m_path, col_path)
    L.box("Waldweg_Anschluss", (12.2, 10.3, 0.01), (2.2, 1.0, 0.04), m_path, col_path)
    L.box("Lichtung_Boden", (10.0, 48.5, 0.0), (8.0, 7.0, 0.05), m_grass_dark, col_path)
    L.prop_stump("Lichtung_Baumstumpf", (10.5, 48.2, 0.03), col_path, r=0.38, h=0.5)
    L.cyl("Lichtung_Liegender_Stamm", (7.5, 50.5, 0.3), 0.3, 3.5, L.mat("MAT_Baum_Stamm", (0.36, 0.25, 0.15, 1)), col_path, rot=(0, math.radians(90), 0), verts=12)
    for i, (x, y, r) in enumerate([(13.9, 29.6, 0.22), (15.2, 30.4, 0.18), (9.0, 47.0, 0.2), (13.0, 50.5, 0.25)]):
        L.sphere(f"Stein_{i}", (x, y, 0.0), r, m_stone, col_path, scale=(1.3, 1.0, 0.6))

    # Großer Wurzelbaum (Fundort Steinpilz) bei (14.5, 30)
    L.prop_tree("Wurzelbaum", (14.6, 30.4, 0), col_forest, h=9.0, kind="round", crown=(0.90, 0.60, 0.15, 1), trunk_r=0.45, seed=3)
    for i, ang in enumerate((200, 235, 265, 300)):
        a = math.radians(ang)
        L.cyl_between(f"Wurzelbaum_Wurzel_{i}", (14.6 + 0.3 * math.cos(a), 30.4 + 0.3 * math.sin(a), 0.25),
                      (14.6 + 1.3 * math.cos(a), 30.4 + 1.3 * math.sin(a), 0.03), 0.12, L.mat("MAT_Baum_Stamm", (0.36, 0.25, 0.15, 1)), col_forest)

    # ---- Bäume: Waldrand entlang der Straße (nördlich), dichter Wald rund um Weg und Lichtung
    rnd = random.Random(42)
    crowns = [(0.90, 0.55, 0.12, 1), (0.95, 0.75, 0.15, 1), (0.70, 0.28, 0.10, 1), (0.55, 0.60, 0.20, 1), (0.85, 0.42, 0.10, 1)]
    n = 0
    def tree_at(x, y, big=False):
        nonlocal n
        kind = "fir" if rnd.random() < 0.22 else "round"
        h = rnd.uniform(6.5, 10.5) if big else rnd.uniform(5.0, 8.5)
        L.prop_tree(f"Baum_{n:03d}", (x, y, 0), col_forest, h=h, kind=kind, crown=rnd.choice(crowns), trunk_r=rnd.uniform(0.2, 0.36), seed=n)
        n += 1
    # Waldrand nördlich der Straße (hinter Parkplatz), x von -70..40
    for x in range(-70, 42, 4):
        if 1 < x < 13:
            continue  # Parkplatz frei
        tree_at(x + rnd.uniform(-1, 1), rnd.uniform(11.5, 15.5), big=True)
        tree_at(x + rnd.uniform(-1, 1), rnd.uniform(17, 22))
    # Wald östlich der Straße (x > 16) und südlich vereinzelt
    for y in range(-30, 10, 5):
        tree_at(rnd.uniform(16, 20), y + rnd.uniform(-1, 1), big=True)
        tree_at(rnd.uniform(22, 30), y + rnd.uniform(-1, 1))
    for x in range(-70, 0, 7):
        tree_at(x + rnd.uniform(-2, 2), rnd.uniform(-14, -9))
    # Dichter Wald beidseits des Waldwegs (x<10.8 oder x>13.6), y 12..64, Lichtung (x 6..14, y 45..52) frei
    for _ in range(170):
        x = rnd.uniform(0, 28)
        y = rnd.uniform(12, 64)
        if 10.6 < x < 13.8:
            continue
        if 5.5 < x < 14.5 and 44.5 < y < 52.5:
            continue
        if (x - 14.6) ** 2 + (y - 30.4) ** 2 < 9:
            continue
        tree_at(x, y)
    # Lichtungsrand
    for ang in range(0, 360, 36):
        a = math.radians(ang)
        tree_at(10.0 + 5.2 * math.cos(a), 48.5 + 4.6 * math.sin(a), big=(ang % 72 == 0))

    # ---- Tunnel am Waldrand: Feldwegdamm (Gras) mit Beton-Durchlass, innen 1,6 m breit, 1,3 m hoch, 12 m lang
    col_tun = L.get_collection("04_Tunnel_am_Waldrand")
    m_damm = L.mat("MAT_Damm_Gras", (0.40, 0.55, 0.24, 1))
    m_beton = L.mat("MAT_Beton_Tunnel", (0.62, 0.61, 0.58, 1))
    m_feldweg = L.mat("MAT_Feldweg_Kies", (0.66, 0.58, 0.44, 1))
    X0, X1, YC, W, H, TOP = -12.0, 0.0, 7.5, 1.6, 1.3, 2.4
    yi0, yi1 = YC - W / 2, YC + W / 2
    # Bäume im Dammbereich entfernen
    near = [o.name[:-6] for o in col_forest.objects if o.name.startswith("Baum_") and o.name.endswith("_Stamm")
            and X0 - 1.5 < o.location.x < X1 + 1.5 and 3.0 < o.location.y < 26.0]
    for nm in [o.name for o in col_forest.objects if any(o.name.startswith(pre) for pre in near)]:
        bpy.data.objects.remove(bpy.data.objects[nm], do_unlink=True)
    L.box("Damm_Sued", ((X0 + X1) / 2, (3.6 + yi0 - 0.25) / 2, TOP / 2), (X1 - X0, (yi0 - 0.25) - 3.6, TOP), m_damm, col_tun)
    L.box("Damm_Nord", ((X0 + X1) / 2, (yi1 + 0.25 + 26.0) / 2, TOP / 2), (X1 - X0, 26.0 - (yi1 + 0.25), TOP), m_damm, col_tun)
    L.box("Damm_Ueber_Tunnel", ((X0 + X1) / 2, YC, (H + 0.25 + TOP) / 2), (X1 - X0, W + 0.5, TOP - H - 0.25), m_damm, col_tun)
    # Böschungen als schräge Platten – an den Portalen ausgespart (Öffnung frei)
    for nm, xo in (("Ost", X1 + 0.9), ("West", X0 - 0.9)):
        for part, (ya, yb) in (("S", (3.6, yi0 - 0.8)), ("N", (yi1 + 0.8, 26.0))):
            o = L.box(f"Damm_Boeschung_{nm}_{part}", (xo, (ya + yb) / 2, TOP / 2 - 0.15), (2.4, yb - ya, 0.3), m_damm, col_tun)
            o.rotation_euler = (0, math.radians(-55 if nm == "Ost" else 55), 0)
        xs = X1 + 0.6 if nm == "Ost" else X0 - 0.6   # Flügelmauern aus Beton neben dem Portal
        for part, yy in (("S", yi0 - 0.55), ("N", yi1 + 0.55)):
            L.box(f"Fluegelmauer_{nm}_{part}", (xs, yy, H / 2 + 0.2), (1.2, 0.25, H + 0.4), m_beton, col_tun)
    L.box("Feldweg_auf_Damm", ((X0 + X1) / 2, (3.6 + 26.0) / 2, TOP + 0.02), (2.6, 26.0 - 3.6, 0.04), m_feldweg, col_tun)
    # Durchlass innen
    L.box("Tunnel_Boden", ((X0 + X1) / 2, YC, 0.03), (X1 - X0, W, 0.06), m_beton, col_tun)
    L.box("Tunnel_Wand_S", ((X0 + X1) / 2, yi0 - 0.12, H / 2), (X1 - X0, 0.24, H + 0.1), m_beton, col_tun)
    L.box("Tunnel_Wand_N", ((X0 + X1) / 2, yi1 + 0.12, H / 2), (X1 - X0, 0.24, H + 0.1), m_beton, col_tun)
    L.box("Tunnel_Decke", ((X0 + X1) / 2, YC, H + 0.12), (X1 - X0, W + 0.48, 0.24), m_beton, col_tun)
    for nm, xp in (("Ost", X1), ("West", X0)):   # Portal-Rahmen (Stirnwände) aus Beton
        L.box(f"Portal_{nm}_Oben", (xp, YC, H + 0.45), (0.3, W + 1.6, 0.7), m_beton, col_tun)
        L.box(f"Portal_{nm}_S", (xp, yi0 - 0.45, H / 2), (0.3, 0.7, H + 0.2), m_beton, col_tun)
        L.box(f"Portal_{nm}_N", (xp, yi1 + 0.45, H / 2), (0.3, 0.7, H + 0.2), m_beton, col_tun)
    L.scatter_leaves("Laub_Tunnel", col_tun, (X0 + 0.3, X1 - 0.3), (yi0 + 0.15, yi1 - 0.15), n=70, seed=11, z=0.07)
    for i, (x, y) in enumerate([(X1 + 0.8, yi0 - 0.6), (X0 - 0.7, yi1 + 0.7), (X1 + 1.4, yi1 + 0.9)]):
        L.sphere(f"Tunnel_Moos_{i}", (x, y, 0.05), 0.45, L.mat("MAT_Moos", (0.30, 0.52, 0.22, 1)), col_tun, scale=(1.4, 1.0, 0.35))
    L.box("Pfad_Parkplatz_zum_Tunnel", ((X1 + 2.2) / 2 + 0.5, YC, 0.015), (3.2, 1.4, 0.03), m_path, col_tun)
    for i, (x, y) in enumerate([(-15.5, 4.0), (-17.0, 12.0), (-20.0, 6.5)]):
        L.prop_tree(f"Tunnel_Wiese_Baum_{i}", (x, y, 0), col_tun, h=7.5, kind="round", crown=(0.90, 0.55, 0.12, 1), trunk_r=0.3, seed=50 + i)
    # schwaches Streiflicht innen (nie völlige Schwärze)
    ld = bpy.data.lights.new("Licht_Tunnel_Innen", "AREA"); ld.energy = 25.0; ld.size = 1.2; ld.color = (1.0, 0.9, 0.75)
    lo = bpy.data.objects.new("Licht_Tunnel_Innen", ld); lo.location = ((X0 + X1) / 2, YC, H - 0.05); col_tun.objects.link(lo)

    # ---- Laub & Pilze
    L.scatter_leaves("Laub_Weg", col_props, (10.6, 13.8), (12, 62), n=260, seed=5)
    L.scatter_leaves("Laub_Lichtung", col_props, (6.5, 13.5), (45, 52), n=160, seed=6)
    L.scatter_leaves("Laub_Parkplatz", col_props, (2, 12), (4, 10), n=60, seed=7)
    # Pilze an den Standardplätzen (Teil des Ortes, wiederverwendbar)
    L.prop_mushroom("Pilz_Steinpilz_Wurzel", (13.6, 29.1, 0.03), col_props, kind="steinpilz", h=0.17)
    L.prop_mushroom("Pilz_Steinpilz_Wurzel_klein", (13.95, 28.8, 0.03), col_props, kind="steinpilz", h=0.11)
    L.prop_mushroom("Pilz_Pfifferlinge_Stumpf", (11.15, 47.7, 0.03), col_props, kind="pfifferlinge")
    # Giftpilz-Stelle: eigener Ort östlich des Waldwegs (NICHT an der Pilzlichtung), Mooshügel + Stein + Ast
    GIFT = (16.6, 39.6)
    near = [o.name[:-6] for o in col_forest.objects if o.name.startswith("Baum_") and o.name.endswith("_Stamm")
            and (Vector((o.location.x, o.location.y, 0)) - Vector((GIFT[0], GIFT[1], 0))).length < 2.3]
    victims = [o.name for o in col_forest.objects if any(o.name.startswith(pre) for pre in near)]
    for nm in victims:
        bpy.data.objects.remove(bpy.data.objects[nm], do_unlink=True)
    L.sphere("Giftpilz_Mooshuegel", (GIFT[0], GIFT[1], -0.02), 0.9, L.mat("MAT_Moos", (0.30, 0.52, 0.22, 1)), col_path, scale=(1.3, 1.0, 0.18))
    L.sphere("Giftpilz_Stein", (GIFT[0] + 0.7, GIFT[1] + 0.5, 0.0), 0.28, m_stone, col_path, scale=(1.2, 1.0, 0.7))
    L.cyl("Giftpilz_Ast", (GIFT[0] - 0.6, GIFT[1] + 0.8, 0.08), 0.06, 1.6, L.mat("MAT_Baum_Stamm", (0.36, 0.25, 0.15, 1)), col_path, rot=(0, math.radians(90), math.radians(25)), verts=8)
    L.prop_tree("Giftpilz_Birke", (GIFT[0] + 1.6, GIFT[1] + 1.4, 0), col_forest, h=8.5, kind="round", crown=(0.95, 0.80, 0.25, 1), trunk_r=0.22, seed=99)
    L.prop_mushroom("Pilz_Knollenblaetterpilz", (GIFT[0], GIFT[1], 0.03), col_props, kind="knollenblaetterpilz", h=0.17)

    # ---- Welt, Licht, Render, Kameras
    L.setup_world_and_sun(col_light, sky=(0.80, 0.86, 0.92, 1.0))
    L.configure_render()
    cams = [L.add_camera(nm, loc, tgt, lens, col_cam) for nm, loc, tgt, lens in CAMERAS]
    bpy.ops.wm.save_as_mainfile(filepath=OUT_BLEND)
    print("Gespeichert:", OUT_BLEND)
    if os.environ.get("NO_RENDER") != "1":
        only = os.environ.get("RENDER_ONLY", "")
        for cam in cams:
            if only and not cam.name.startswith(only):
                continue
            L.render_camera(cam, os.path.join(OUT_DIR, cam.name + ".png"))


if __name__ == "__main__":
    main()
