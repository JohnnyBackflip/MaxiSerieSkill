#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Folge 02 – Start-/Endbild je Szene (A = Startbild, B = Endbild): 44 grobe Blender-Mockups mit Standardfiguren.
Aufruf:  blender -b <Haus-Blockout.blend> --python build_folge02_szenen_AB.py -- haus [SH010A ...]
         blender -b <Herbstwald_Blockout.blend> --python build_folge02_szenen_AB.py -- wald [SH060A ...]
"""
import os, sys, math
import bpy
from mathutils import Vector

K = os.environ.get("MAXI_ROOT", os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")))
sys.path.insert(0, K)
import maxi_blender_lib as L  # noqa: E402

EP = os.path.join(K, "09_Folge_02_Pilze_im_Herbstwald")
OUT_DIR = os.path.join(EP, "02_Szenen_Blender_Mockups")
BLEND_DIR = os.path.join(OUT_DIR, "blend")
SCENE_COL = "SZENE_Figuren_und_Props"
SCENES = {}


def scene(sid, base, cam):
    def deco(fn):
        SCENES[sid] = dict(base=base, cam=cam, build=fn)
        return fn
    return deco


def basket_in_hands(r, facing, col, full=False, name="Korb"):
    L.prop_basket(name, ((r["hand_L"] + r["hand_R"]) / 2 - Vector((0, 0, 0.12))), facing, col, full=full)


# ------------------------------------------------------------------ HAUS
CAR_DRIVEWAY = ((14.3, -10.6, 0), -90)
CAR_STREET = ((6.0, -18.6, 0), 180)
CAR_STREET_FAR = ((9.5, -18.6, 0), 180)
CAM_39 = ((16.7, -6.6, 1.9), (13.6, -14.8, 0.8), 18.0)
CAM_40 = ((16.9, -6.3, 2.0), (12.6, -15.0, 0.7), 17.0)
CAM_50 = ((17.2, -15.4, 1.15), (16.0, -11.9, 0.85), 28.0)
CAM_160 = ((12.5, -13.6, 1.7), (3.5, -18.0, 0.9), 22.0)
CAM_180 = ((-1.2, -14.4, 1.3), (4.2, -15.4, 1.0), 32.0)
CAM_20 = ((0.3, 0.3, 1.35), (0.3, -4.9, 0.95), 26.0)
CAM_210 = ((-3.45, 1.75, 1.25), (-3.45, 4.4, 0.95), 24.0)   # Runde 4: frontal, nah
CAM_220 = ((-3.45, 1.20, 1.45), (-3.45, 4.4, 0.95), 22.0)   # Runde 4: frontal, halbnah
CAM_160N = ((-1.6, -16.4, 1.25), (4.5, -17.4, 1.15), 24.0)   # Runde 4: nah am Auto
CAM_190N = ((-4.5, 2.2, 1.50), (-6.4, 4.7, 1.15), 22.0)     # Runde 4: nah an Herd/Spüle (verworfen)
CAM_190S = ((-5.6, 1.0, 1.50), (-6.3, 5.2, 1.10), 20.0)     # Runde 5: vom WZ-Durchgang in die Ecke Herd/Spüle, Esstisch rechts vorn
KU09 = "KOM_CAM_09_KU_Kuechenzeile_Tritthocker_und_6er_Esstisch"
KU10 = "KOM_CAM_10_KU_Gegenschuss_Esstisch_durch_Terrassentuer_in_Garten"
KU31 = "KOM_CAM_31_KU_Nah_Maxis_Tritthocker_Spuele_und_Kuechenzeile"
TABLE_Z = 0.80


# --- Runde 6 (2026-11-05): Veo-Guide-Regeln STRIKT – eine Einstellung = EIN Sprecher, Sprecher groß/halbnah/frontal
CAM_010 = ((-3.55, 2.60, 1.55), (-3.55, 4.65, 1.25), 30.0)    # Mama hinter dem Esstisch, frontal
CAM_011 = ((-4.15, 2.30, 1.00), (-4.15, 4.30, 0.95), 35.0)  # Maxi am Tisch, Kinderaugenhöhe
CAM_020 = ((0.4, -3.00, 1.45), (0.4, -6.30, 1.25), 28.0)    # Flur Richtung Haustür, Papa frontal
CAM_030 = ((13.6, -15.2, 1.30), (12.8, -10.8, 1.15), 30.0)  # Einfahrt, Mama frontal neben dem Auto
CAM_040 = ((12.9, -13.3, 1.15), (12.9, -15.4, 1.00), 30.0)  # aus der Einfahrt auf den Bürgersteig, Karl frontal
CAM_050 = ((12.7, -14.9, 1.00), (12.8, -12.9, 0.85), 35.0)  # Maxi nah, Kinderaugenhöhe
CAM_051 = ((12.4, -14.9, 1.00), (12.5, -12.9, 0.75), 32.0)  # Mama hockt bei Maxi

@scene("SH010A", "haus", CAM_010)
def _(col):
    r = L.build_figure("Mama_Katrin", (-3.2, 4.65), 270, "hold_front", col)          # hält den leeren Korb vor sich
    L.prop_basket("Korb", ((r["hand_L"] + r["hand_R"]) / 2 - Vector((0, 0, 0.1))), 270, col)
    L.build_figure("Maxi", (-4.15, 4.18), 270, "sit", col, seat_z=0.46, head_turn_deg=60, arms="hold_front")  # hört zu (still)

@scene("SH010B", "haus", CAM_010)
def _(col):
    r = L.build_figure("Mama_Katrin", (-3.2, 4.65), 270, "lift", col)                # hebt den Korb hoch
    L.prop_basket("Korb", ((r["hand_L"] + r["hand_R"]) / 2 + Vector((0, 0, 0.05))), 270, col)
    L.build_figure("Maxi", (-4.15, 4.18), 270, "sit", col, seat_z=0.46, head_turn_deg=60, arms="hold_front")

@scene("SH011A", "haus", CAM_011)
def _(col):
    L.build_figure("Maxi", (-4.15, 4.18), 270, "sit", col, seat_z=0.46, arms="hold_front")   # sitzt, große Augen

@scene("SH011B", "haus", CAM_011)
def _(col):
    L.build_figure("Maxi", (-4.15, 4.18), 270, "sit", col, seat_z=0.46, arms="lift")   # jubelt, Arme hoch

@scene("SH020A", "haus", CAM_020)
def _(col):
    L.build_figure("Papa_Thomas", (0.85, -5.0), 90, "wave", col)                       # Schlüssel hoch, frontal
    r = L.build_figure("Maxi", (-0.15, -4.75), 90, "hold_front", col)                  # still, mit Korb
    basket_in_hands(r, 90, col)

@scene("SH020B", "haus", CAM_020)
def _(col):
    L.build_figure("Papa_Thomas", (0.85, -5.0), 90, "point", col)                      # winkt „los geht's“
    r = L.build_figure("Maxi", (-0.1, -5.3), 270, "walk", col, arms="hold_front")      # hüpft zur Tür
    basket_in_hands(r, 270, col)

@scene("SH030A", "haus", CAM_030)
def _(col):
    L.prop_car("Auto", *CAR_DRIVEWAY, col)
    L.build_figure("Mama_Katrin", (12.75, -12.6), 280, "walk", col)                      # kommt auf die Kamera zu
    r = L.build_figure("Maxi", (14.0, -13.6), 120, "walk", col, arms="hold_front")     # Vordergrund rechts, 3/4 von hinten, still
    L.prop_basket("Korb", (r["hand_R"].x, r["hand_R"].y, r["hand_R"].z - 0.35), 120, col)  # Korb baumelt tief

@scene("SH030B", "haus", CAM_030)
def _(col):
    L.prop_car("Auto", *CAR_DRIVEWAY, col)
    L.build_figure("Mama_Katrin", (12.75, -12.9), 290, "wave", col)                      # Daumen hoch
    r = L.build_figure("Maxi", (14.0, -13.6), 120, "lift", col)                        # hält den Korb hoch
    L.prop_basket("Korb", ((r["hand_L"] + r["hand_R"]) / 2 + Vector((0, 0, 0.05))), 120, col)

@scene("SH040A", "haus", CAM_040)
def _(col):
    _, seat, bar = L.prop_bike("Rad", (13.9, -15.3, 0), 180, col)                       # rollt heran
    L.build_figure("Karl", (seat.x, seat.y), 180, "bike", col, seat_z=seat.z, head_turn_deg=-60)

@scene("SH040B", "haus", CAM_040)
def _(col):
    _, seat, bar = L.prop_bike("Rad", (12.9, -15.3, 0), 180, col)                       # hält am Gartentor
    L.build_figure("Karl", (seat.x, seat.y), 180, "bike", col, seat_z=seat.z, head_turn_deg=-90, arms="hands_hip")

@scene("SH050A", "haus", CAM_050)
def _(col):
    L.prop_car("Auto", *CAR_DRIVEWAY, col)
    r = L.build_figure("Maxi", (12.8, -12.9), 270, "hold_front", col, head_turn_deg=45)  # schaut Karl hinterher
    basket_in_hands(r, 270, col)

@scene("SH050B", "haus", CAM_050)
def _(col):
    L.prop_car("Auto", *CAR_DRIVEWAY, col)
    r = L.build_figure("Maxi", (12.8, -12.9), 270, "hold_front", col)                    # frontal, schmollt
    basket_in_hands(r, 270, col)

@scene("SH051A", "haus", CAM_051)
def _(col):
    L.prop_car("Auto", *CAR_DRIVEWAY, col)
    L.build_figure("Mama_Katrin", (12.15, -12.75), 290, "crouch", col)                   # hockt sich hin, frontal
    r = L.build_figure("Maxi", (12.95, -12.95), 210, "hold_front", col)                  # schaut zu Mama (still)
    basket_in_hands(r, 210, col)

@scene("SH051B", "haus", CAM_051)
def _(col):
    L.prop_car("Auto", *CAR_DRIVEWAY, col)
    L.build_figure("Mama_Katrin", (12.15, -12.75), 290, "crouch", col, arms="wave")      # Hand auf Maxis Schulter, lächelt
    r = L.build_figure("Maxi", (12.95, -12.95), 230, "hold_front", col)
    basket_in_hands(r, 230, col)

def _car_family(col, carpos, facing, maxi_turn=0, maxi_arms=None):
    e, seats = L.prop_car("Auto", carpos, facing, col)
    L.build_figure("Papa_Thomas", (seats["VL"].x, seats["VL"].y), facing, "sit", col, seat_z=seats["VL"].z, floor_z=0.62, arms="bike")
    L.build_figure("Mama_Katrin", (seats["VR"].x, seats["VR"].y), facing, "sit", col, seat_z=seats["VR"].z, floor_z=0.62)
    r = L.build_figure("Maxi", (seats["HR"].x, seats["HR"].y), facing, "sit", col, seat_z=seats["HR"].z, floor_z=0.62, head_turn_deg=maxi_turn, arms=maxi_arms)
    return e, seats, r

@scene("SH160A", "haus", CAM_160N)
def _(col):
    _car_family(col, (5.6, -18.6, 0), 180)                                              # Auto kommt (nah)
    _, seat, bar = L.prop_bike("Rad", (1.8, -15.3, 0), 180, col)
    L.build_figure("Karl", (seat.x, seat.y), 180, "bike", col, seat_z=seat.z)

@scene("SH160B", "haus", CAM_160N)
def _(col):
    _car_family(col, (3.6, -18.6, 0), 180, maxi_turn=-90, maxi_arms="point")             # Maxi zeigt nach vorn
    _, seat, bar = L.prop_bike("Rad", (0.6, -15.3, 0), 180, col)
    L.build_figure("Karl", (seat.x, seat.y), 180, "bike", col, seat_z=seat.z)

def _cam_auto_innen(e):
    return (tuple(L.world_of(e, (-0.45, 0.9, 1.28))), tuple(L.world_of(e, (-1.1, -2.6, 1.1))), 18.0)

@scene("SH170A", "haus", "AUTO_INNEN")
def _(col):
    e, seats, r = _car_family(col, (6.0, -18.6, 0), 180, maxi_turn=-90, maxi_arms="hold_front")   # Korb noch auf dem Schoß
    L.prop_basket("Korb", ((r["hand_L"] + r["hand_R"]) / 2 - Vector((0, 0, 0.1))), 90, col, full=True)
    _, seat, bar = L.prop_bike("Rad", (7.3, -15.3, 0), 180, col)
    L.build_figure("Karl", (seat.x, seat.y), 180, "bike", col, seat_z=seat.z, head_turn_deg=90)
    return _cam_auto_innen(e)

@scene("SH170B", "haus", "AUTO_INNEN")
def _(col):
    e, seats, r = _car_family(col, (6.0, -18.6, 0), 180, maxi_turn=-90, maxi_arms="lift")        # Korb hoch ans Fenster
    L.prop_basket("Korb", ((r["hand_L"] + r["hand_R"]) / 2 + Vector((0, 0, 0.05))), 90, col, full=True)
    _, seat, bar = L.prop_bike("Rad", (7.3, -15.3, 0), 180, col)
    L.build_figure("Karl", (seat.x, seat.y), 180, "bike", col, seat_z=seat.z, head_turn_deg=90)
    return _cam_auto_innen(e)

@scene("SH180A", "haus", CAM_180)
def _(col):
    _, seats, r = _car_family(col, (7.5, -18.6, 0), 180, maxi_turn=-90, maxi_arms="lift")
    L.prop_basket("Korb", ((r["hand_L"] + r["hand_R"]) / 2 + Vector((0, 0, 0.05))), 90, col, full=True)
    _, seat, bar = L.prop_bike("Rad", (4.0, -15.3, 0), 180, col)
    L.build_figure("Karl", (seat.x, seat.y), 180, "bike", col, seat_z=seat.z, head_turn_deg=60)   # schaut rüber

@scene("SH180B", "haus", CAM_180)
def _(col):
    _, seats, r = _car_family(col, (4.0, -18.6, 0), 180, maxi_turn=-90, maxi_arms="lift")      # Auto fährt vorbei
    L.prop_basket("Korb", ((r["hand_L"] + r["hand_R"]) / 2 + Vector((0, 0, 0.05))), 90, col, full=True)
    _, seat, bar = L.prop_bike("Rad", (4.0, -15.3, 0), 180, col)
    L.build_figure("Karl", (seat.x, seat.y), 180, "bike", col, seat_z=seat.z, head_turn_deg=100, arms="hands_hip")  # angehalten, verdutzt

@scene("SH190A", "haus", CAM_190S)
def _(col):
    L.prop_pan("Pfanne", (-7.8, 3.5, 0.97), col)
    L.build_figure("Papa_Thomas", (-7.05, 3.4), 270, "hold_front", col, head_turn_deg=40)  # am Herd, Gesicht zur Kamera
    L.build_figure("Maxi", (-6.15, 5.05), 30, "hold_front", col, floor_z=0.44, head_turn_deg=-70)  # Tritthocker an der Spüle
    L.prop_basket("Korb", (-5.2, 5.75, 0.94), 0, col, full=True)                       # auf der Arbeitsplatte neben der Spüle
    L.build_figure("Mama_Katrin", (-4.9, 3.1), 0, "hold_front", col, head_turn_deg=-70)  # steht am Esstisch-Ende, schneidet
    L.prop_mushroom("Pilz_Brett_1", (-4.45, 2.95, 0.80), col, kind="steinpilz", h=0.14)
    L.prop_mushroom("Pilz_Brett_2", (-4.40, 3.15, 0.80), col, kind="steinpilz", h=0.1)

@scene("SH190B", "haus", CAM_190S)
def _(col):
    L.prop_pan("Pfanne", (-7.8, 3.5, 0.97), col)
    L.build_figure("Papa_Thomas", (-7.05, 3.4), 270, "stir", col, head_turn_deg=40)       # rührt, Dampf
    L.build_figure("Mama_Katrin", (-5.0, 3.3), 160, "hold_front", col, head_turn_deg=100)  # bringt das Brett zur Pfanne
    L.build_figure("Maxi", (-6.15, 5.05), 250, "stand", col, floor_z=0.44, head_turn_deg=30)  # schaut zur Pfanne
    L.prop_basket("Korb", (-5.2, 5.75, 0.94), 0, col)

@scene("SH200A", "haus", KU10)
def _(col):
    L.build_figure("Maxi", (-4.15, 4.18), 270, "sit", col, seat_z=0.46, arms="hold_front")
    L.build_figure("Papa_Thomas", (-2.75, 4.18), 270, "sit", col, seat_z=0.46, arms="hold_front")
    L.build_figure("Mama_Katrin", (-3.45, 4.75), 270, "stand", col, arms="hold_front")   # steht, verteilt Nudeln
    L.prop_pan("Pfanne", (-3.45, 3.45, TABLE_Z + 0.25), col)
    L.prop_plate("Teller_Maxi", (-4.15, 3.5, TABLE_Z), col)
    L.prop_plate("Teller_Papa", (-2.75, 3.5, TABLE_Z), col)

@scene("SH200B", "haus", KU10)
def _(col):
    for key, x in (("Maxi", -4.15), ("Mama_Katrin", -3.45), ("Papa_Thomas", -2.75)):
        L.build_figure(key, (x, 4.18), 270, "sit", col, seat_z=0.46, arms="hold_front")
        L.prop_plate(f"Teller_{key}", (x, 3.5, TABLE_Z), col)
    L.prop_pan("Pfanne", (-3.45, 2.6, TABLE_Z), col)

@scene("SH210A", "haus", CAM_210)
def _(col):
    for key, x, arms in (("Maxi", -4.15, "hold_front"), ("Mama_Katrin", -3.45, "hold_front"), ("Papa_Thomas", -2.75, "hold_front")):
        L.build_figure(key, (x, 4.18), 270, "sit", col, seat_z=0.46, arms=arms)          # Maxi wickelt Nudeln auf
        L.prop_plate(f"Teller_{key}", (x, 3.5, TABLE_Z), col)
    L.prop_pan("Pfanne", (-3.45, 2.6, TABLE_Z), col)

@scene("SH210B", "haus", CAM_210)
def _(col):
    for key, x, arms in (("Maxi", -4.15, "wave"), ("Mama_Katrin", -3.45, "hold_front"), ("Papa_Thomas", -2.75, "lift")):
        L.build_figure(key, (x, 4.18), 270, "sit", col, seat_z=0.46, arms=arms)
        L.prop_plate(f"Teller_{key}", (x, 3.5, TABLE_Z), col)
    L.prop_pan("Pfanne", (-3.45, 2.6, TABLE_Z), col)

@scene("SH220A", "haus", CAM_220)
def _(col):
    for key, x in (("Maxi", -4.15), ("Mama_Katrin", -3.45), ("Papa_Thomas", -2.75)):
        L.build_figure(key, (x, 4.18), 270, "sit", col, seat_z=0.46, arms="wave")       # Gabeln hoch
        L.prop_plate(f"Teller_{key}", (x, 3.5, TABLE_Z), col)
    L.prop_pan("Pfanne", (-3.45, 2.6, TABLE_Z), col)

@scene("SH220B", "haus", CAM_220)
def _(col):
    for key, x in (("Maxi", -4.15), ("Mama_Katrin", -3.45), ("Papa_Thomas", -2.75)):
        L.build_figure(key, (x, 4.18), 270, "sit", col, seat_z=0.46, arms="stir")       # essen
        L.prop_plate(f"Teller_{key}", (x, 3.5, TABLE_Z), col)
    L.prop_pan("Pfanne", (-3.45, 2.6, TABLE_Z), col)

# ------------------------------------------------------------------ WALD
W1 = "WALD_CAM_01_Landstrasse_zum_Waldrand"; W2 = "WALD_CAM_02_Waldparkplatz_mit_Holzschild"
W3 = "WALD_CAM_03_Waldweg_Totale"; W4 = "WALD_CAM_04_Waldweg_Nah_Baumwurzel_Kinderaugenhoehe"
W5 = "WALD_CAM_05_Pilzlichtung_Baumstumpf"; W6 = "WALD_CAM_06_Giftpilz_Stelle_Nah_Kinderaugenhoehe"
W7 = "WALD_CAM_07_Giftpilz_Stelle_Totale_vom_Waldweg"
CAM_80 = ((12.2, 21.0, 1.35), (12.2, 12.0, 1.05), 32.0)     # Runde 4: Figuren näher/größer
CAM_70 = ((5.4, 1.0, 1.40), (6.6, 6.4, 1.0), 26.0)          # Runde 4: nah am geparkten Auto
CAM_140 = ((12.2, 12.5, 1.35), (12.2, 24.0, 1.05), 32.0)    # Runde 4
CAM_150 = ((7.8, 1.2, 1.35), (6.3, 6.4, 1.0), 26.0)         # Runde 4 (verworfen: Auto wirkte schräg)
CAM_150S = ((6.6, 1.6, 1.30), (6.6, 7.2, 1.00), 24.0)       # Runde 5: exakt seitlich, Auto parallel zum Bildrand
CAR_PARK = ((6.5, 7.2, 0), 0)

@scene("SH060A", "wald", W1)
def _(col):
    _car_family(col, (-12.0, -1.5, 0), 0)                                                # Auto noch weit hinten
@scene("SH060B", "wald", W1)
def _(col):
    _car_family(col, (1.5, -1.5, 0), 0)                                                  # kurz vor der Parkbucht

@scene("SH070A", "wald", CAM_70)
def _(col):
    _car_family(col, CAR_PARK[0], 0)                                                     # geparkt, alle noch drin
@scene("SH070B", "wald", CAM_70)
def _(col):
    L.prop_car("Auto", *CAR_PARK, col, door_open="RR")
    L.build_figure("Papa_Thomas", (8.6, 5.5), 200, "point", col)
    L.build_figure("Mama_Katrin", (5.6, 5.3), 300, "stand", col)
    r = L.build_figure("Maxi", (4.6, 5.1), 320, "hold_front", col)
    basket_in_hands(r, 320, col)

@scene("SH080A", "wald", CAM_80)
def _(col):
    r = L.build_figure("Maxi", (12.4, 15.8), 90, "walk", col, arms="hold_front")          # kommt näher
    basket_in_hands(r, 90, col)
    L.build_figure("Mama_Katrin", (11.5, 14.8), 90, "walk", col)
    L.build_figure("Papa_Thomas", (13.1, 14.5), 90, "walk", col)
@scene("SH080B", "wald", CAM_80)
def _(col):
    r = L.build_figure("Maxi", (12.4, 18.2), 90, "walk", col, arms="hold_front")
    basket_in_hands(r, 90, col)
    L.build_figure("Mama_Katrin", (11.5, 17.3), 90, "walk", col, arms="point_down")      # zeigt unter die Bäume
    L.build_figure("Papa_Thomas", (13.1, 17.0), 90, "walk", col)

@scene("SH090A", "wald", W4)
def _(col):
    r = L.build_figure("Maxi", (13.4, 27.6), 60, "crouch", col, arms="hold_front")        # entdeckt den Pilz, beugt sich vor
    L.prop_basket("Korb", (14.9, 27.4, 0.03), 50, col)
    L.build_figure("Mama_Katrin", (12.0, 35.0), 270, "walk", col)
    L.build_figure("Papa_Thomas", (13.2, 36.0), 270, "walk", col)
@scene("SH090B", "wald", W4)
def _(col):
    L.build_figure("Maxi", (14.2, 28.2), 125, "kneel", col, arms="wave")
    L.prop_basket("Korb", (14.9, 27.4, 0.03), 50, col)
    L.build_figure("Mama_Katrin", (12.0, 33.0), 270, "walk", col)
    L.build_figure("Papa_Thomas", (13.2, 34.0), 270, "walk", col)

@scene("SH100A", "wald", W4)
def _(col):
    r = L.build_figure("Papa_Thomas", (12.7, 29.5), 250, "crouch", col, arms="point")     # betrachtet den Pilz in der Hand
    L.prop_mushroom("Pilz_in_Hand", (r["hand_R"].x, r["hand_R"].y, r["hand_R"].z - 0.05), col, kind="steinpilz", h=0.17)
    m = L.build_figure("Maxi", (14.3, 28.3), 135, "kneel", col, arms="hold_front")
    basket_in_hands(m, 135, col)
    L.build_figure("Mama_Katrin", (12.0, 31.5), 300, "stand", col)
@scene("SH100B", "wald", W4)
def _(col):
    r = L.build_figure("Papa_Thomas", (13.1, 29.2), 250, "crouch", col, arms="point_down")  # legt ihn in Maxis Korb
    m = L.build_figure("Maxi", (14.0, 28.2), 135, "kneel", col, arms="hold_front")
    basket_in_hands(m, 135, col, full=True)
    L.build_figure("Mama_Katrin", (12.0, 31.5), 300, "stand", col)

@scene("SH110A", "wald", W5)
def _(col):
    L.build_figure("Mama_Katrin", (10.7, 47.05), 50, "kneel", col, arms="point_down")
    r = L.build_figure("Maxi", (12.6, 48.6), 215, "hold_front", col)
    basket_in_hands(r, 215, col)
    L.build_figure("Papa_Thomas", (8.6, 45.6), 60, "stand", col)
@scene("SH110B", "wald", W5)
def _(col):
    L.build_figure("Mama_Katrin", (10.7, 47.05), 50, "kneel", col, arms="hold_front")    # pflückt die Pfifferlinge
    r = L.build_figure("Maxi", (12.0, 47.9), 215, "crouch", col, arms="hold_front")      # hält den Korb hin
    basket_in_hands(r, 215, col, full=True)
    L.build_figure("Papa_Thomas", (8.6, 45.6), 60, "stand", col)

@scene("SH120A", "wald", W7)
def _(col):
    L.build_figure("Maxi", (14.6, 40.9), 320, "walk", col, arms="hold_front")            # kommt zum Mooshügel
    L.prop_basket("Korb", (14.0, 41.2, 0.03), 0, col, full=True)
    L.build_figure("Mama_Katrin", (12.9, 41.5), 20, "walk", col)
    L.build_figure("Papa_Thomas", (13.6, 36.8), 60, "walk", col)
@scene("SH120B", "wald", W7)
def _(col):
    L.build_figure("Maxi", (16.0, 40.5), 305, "point", col)
    L.prop_basket("Korb", (15.2, 40.8, 0.03), 0, col, full=True)
    L.build_figure("Mama_Katrin", (13.5, 40.1), 20, "walk", col)
    L.build_figure("Papa_Thomas", (14.9, 37.3), 60, "walk", col)

@scene("SH130A", "wald", W6)
def _(col):
    L.build_figure("Maxi", (16.2, 40.5), 300, "point", col)
    L.build_figure("Mama_Katrin", (17.6, 40.1), 195, "crouch", col, arms="point")
    L.prop_basket("Korb", (15.5, 41.1, 0.03), 0, col, full=True)
@scene("SH130B", "wald", W6)
def _(col):
    L.build_figure("Maxi", (16.4, 40.8), 300, "stand", col)                              # nickt, Hände unten
    L.build_figure("Mama_Katrin", (17.5, 40.6), 200, "crouch", col, arms="point_down")   # Hand auf seiner Schulter
    L.prop_basket("Korb", (15.5, 41.1, 0.03), 0, col, full=True)

@scene("SH140A", "wald", CAM_140)
def _(col):
    r = L.build_figure("Maxi", (12.3, 18.0), 270, "walk", col, arms="hold_front")
    basket_in_hands(r, 270, col, full=True)
    L.build_figure("Mama_Katrin", (11.5, 19.0), 270, "walk", col)
    L.build_figure("Papa_Thomas", (13.1, 19.3), 270, "walk", col)
@scene("SH140B", "wald", CAM_140)
def _(col):
    r = L.build_figure("Maxi", (12.3, 15.6), 270, "walk", col, arms="hold_front")
    basket_in_hands(r, 270, col, full=True)
    L.build_figure("Mama_Katrin", (11.5, 16.6), 270, "walk", col)
    L.build_figure("Papa_Thomas", (13.1, 16.9), 270, "walk", col, arms="wave")

@scene("SH150A", "wald", CAM_150S)
def _(col):
    L.prop_car("Auto", *CAR_PARK, col, door_open="RR")                                  # parallel, Front rechts
    r = L.build_figure("Maxi", (5.95, 5.7), 250, "hold_front", col)                     # vor der offenen hinteren Tür
    basket_in_hands(r, 250, col, full=True)
    L.build_figure("Papa_Thomas", (4.75, 5.0), 0, "hold_front", col, head_turn_deg=-70) # hält die Tür
    L.build_figure("Mama_Katrin", (8.6, 5.4), 200, "walk", col)                          # kommt von vorn

@scene("SH150B", "wald", CAM_150S)
def _(col):
    e, seats = L.prop_car("Auto", *CAR_PARK, col)                                        # alle Türen zu
    r = L.build_figure("Maxi", (seats["HR"].x, seats["HR"].y), 270, "sit", col, seat_z=seats["HR"].z, floor_z=0.62, arms="hold_front")
    L.prop_basket("Korb", ((r["hand_L"] + r["hand_R"]) / 2 - Vector((0, 0, 0.1))), 270, col, full=True)
    L.build_figure("Mama_Katrin", (7.0, 5.75), 270, "stand", col)                         # an der Beifahrertür vorn
    L.build_figure("Papa_Thomas", (9.25, 6.1), 45, "walk", col, head_turn_deg=-90)        # geht vorn ums Auto zur Fahrerseite


# --- Runde 7 (2026-11-05): Sprecher-Einstellungen „S“ für die Flow-Videos (EIN Sprecher, groß, frontal)
@scene("SH090S", "wald", ((12.0, 27.3, 0.80), (13.1, 28.95, 0.50), 28.0))
def _(col):
    L.build_figure("Maxi", (12.85, 28.9), 242, "kneel", col, arms="wave")                # ruft frontal, Steinpilz rechts hinter ihm
    L.prop_basket("Korb", (12.45, 29.15, 0.03), 50, col)

@scene("SH120S", "wald", ((15.0, 37.9, 0.95), (15.95, 39.55, 0.65), 30.0))
def _(col):
    L.build_figure("Maxi", (15.85, 39.6), 243, "hold_front", col, floor_z=0.08)           # frontal, weißer Pilz rechts neben ihm

@scene("SH130S", "wald", ((16.5, 37.6, 0.85), (16.65, 39.45, 0.60), 30.0))
def _(col):
    L.build_figure("Mama_Katrin", (17.05, 39.3), 254, "crouch", col, arms="point_down")   # frontal, ernst, hält Maxis Hand zurück
    L.build_figure("Maxi", (16.1, 39.5), 0, "hold_front", col, floor_z=0.08)               # still, schaut zu Mama
    L.prop_basket("Korb", (15.5, 40.0, 0.03), 0, col, full=True)

@scene("SH190S", "haus", ((-4.28, 1.41, 1.50), (-4.80, 3.05, 1.30), 30.0))
def _(col):
    L.build_figure("Mama_Katrin", (-4.95, 3.0), 0, "hold_front", col, head_turn_deg=-70)  # schneidet am Esstisch, frontal
    L.prop_mushroom("Pilz_Brett_1", (-4.45, 2.95, 0.80), col, kind="steinpilz", h=0.14)
    L.prop_mushroom("Pilz_Brett_2", (-4.40, 3.15, 0.80), col, kind="steinpilz", h=0.1)

@scene("SH191S", "haus", ((-5.83, 1.94, 1.60), (-7.00, 3.45, 1.40), 30.0))
def _(col):
    L.prop_pan("Pfanne", (-7.8, 3.5, 0.97), col)
    L.build_figure("Papa_Thomas", (-7.05, 3.4), 270, "stir", col, head_turn_deg=40)       # rührt, Gesicht zur Kamera

@scene("SH200S", "haus", CAM_011)
def _(col):
    L.build_figure("Maxi", (-4.15, 4.18), 270, "sit", col, seat_z=0.46, arms="hold_front")  # nah am Tisch, Teller vor sich
    L.prop_plate("Teller_Maxi", (-4.15, 3.5, TABLE_Z), col)
    L.prop_pan("Pfanne", (-3.6, 3.2, TABLE_Z), col)


# --- Serien-Intro „Maxi Cartoons“ (2026-11-05): Familie winkt vor dem Haus in die Kamera, oben Platz fürs Logo
@scene("INTRO", "haus", ((0.5, -12.6, 1.05), (0.5, -6.3, 1.75), 30.0))
def _(col):
    L.build_figure("Mama_Katrin", (-0.45, -9.3), 270, "wave", col)
    L.build_figure("Maxi", (0.5, -9.0), 270, "lift", col)
    L.build_figure("Papa_Thomas", (1.45, -9.3), 270, "wave", col)


# --- Intro v2 (2026-11-05, User-Kritik): Nahaufnahmen Maxi/Mama/Papa, dann alle ENG zusammen winkend, oben Platz fürs Logo
def _intro_familie(col, maxi_pose="wave"):
    L.build_figure("Mama_Katrin", (0.05, -9.25), 270, "wave", col)
    L.build_figure("Maxi", (0.5, -8.65), 270, maxi_pose, col)
    L.build_figure("Papa_Thomas", (0.97, -9.25), 270, "wave", col)

@scene("INTRO2_MAXI", "haus", ((0.5, -10.0, 0.95), (0.5, -8.65, 0.9), 40.0))
def _(col):
    _intro_familie(col)

@scene("INTRO2_MAMA", "haus", ((0.0, -10.9, 1.5), (0.05, -9.25, 1.42), 38.0))
def _(col):
    _intro_familie(col)

@scene("INTRO2_PAPA", "haus", ((1.02, -10.9, 1.6), (0.97, -9.25, 1.52), 38.0))
def _(col):
    _intro_familie(col)

@scene("INTRO2_ALLE", "haus", ((0.5, -11.9, 1.3), (0.5, -9.0, 1.5), 28.0))
def _(col):
    _intro_familie(col, maxi_pose="lift")


# ------------------------------------------------------------------ Ablauf
def clear_scene_col():
    col = bpy.data.collections.get(SCENE_COL)
    if col:
        for o in list(col.objects):
            bpy.data.objects.remove(o, do_unlink=True)
        bpy.data.collections.remove(col)
    for o in list(bpy.data.objects):
        if o.name.startswith("SZENE_CAM_"):
            bpy.data.objects.remove(o, do_unlink=True)


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    base = argv[0]
    wanted = argv[1:] or [k for k, v in SCENES.items() if v["base"] == base]
    os.makedirs(BLEND_DIR, exist_ok=True)
    L.configure_render()
    for c in bpy.data.collections:
        c.hide_render = False
    cam_col = L.get_collection("99_Kameras")
    for sid in wanted:
        spec = SCENES[sid]
        if spec["base"] != base:
            continue
        clear_scene_col()
        col = L.get_collection(SCENE_COL)
        cam_spec = spec["build"](col) or spec["cam"]
        if isinstance(cam_spec, str) and cam_spec != "AUTO_INNEN":
            cam = bpy.data.objects[cam_spec]
        else:
            loc, tgt, lens = cam_spec
            cam = L.add_camera(f"SZENE_CAM_{sid}", loc, tgt, lens, cam_col)
        L.render_camera(cam, os.path.join(OUT_DIR, f"{sid}_blender.png"))
        bpy.ops.wm.save_as_mainfile(filepath=os.path.join(BLEND_DIR, f"{sid}.blend"), copy=True)
        print("Szene gesichert:", sid)
    clear_scene_col()


if __name__ == "__main__":
    main()
