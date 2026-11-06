#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Folge „Tante Frieda und Lorchen“ – ein Blender-Mockup (Farbpuppen) je Einstellung; daraus entstehen die Flow-Bilder.
Puppenfarben: blau Maxi, gelb Mama, grün Papa, türkis Anna, braun Opa, violett Frieda; Hasi hellgrau, Lorchen grün.
Aufruf: blender -b <Haus-Blockout.blend> --python build_frieda_szenen.py -- [SH010 SH020 ...]   (ohne ID: alle)
"""
import os, sys, math
import bpy
from mathutils import Vector

K = os.environ.get("MAXI_ROOT", os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")))
sys.path.insert(0, K)
import maxi_blender_lib as L  # noqa: E402

OUT_DIR = os.path.join(K, "12_Folge_Tante_Frieda", "02_Szenen_Blender_Mockups")
BLEND_DIR = os.path.join(OUT_DIR, "blend")
SCENE_COL = "SZENE_Figuren_und_Props"
SCENES = {}
Z_OG = 2.82  # Boden Obergeschoss (Kinderzimmer)


def scene(sid, cam):
    def deco(fn):
        SCENES[sid] = dict(cam=cam, build=fn)
        return fn
    return deco


def V(*a):
    return Vector(a)


def ball(col, loc, name="Ball"):
    return L.sphere(name, loc, 0.11, L.mat("MAT_Ball_Rot", (0.90, 0.15, 0.12, 1)), col)


def hide_blockout_hasi():
    for o in bpy.data.objects:
        if o.name.startswith("KZ_Hasi"):
            o.hide_render = True


def hasi(r, col, hand="hand_R", facing=0, dz=-0.10):
    return L.prop_hasi("Hasi", r[hand] + V(0, 0, dz), col, facing)


# ------------------------------------------------------------ Orte (Weltkoordinaten aus dem Haus-Blockout)
CAR = ((14.3, -10.6, 0), -90)           # Auto in der Einfahrt, Front zur Straße
NT = (-7.85, -2.10, 3.40)               # Kinderzimmer: Nachttisch-Oberfläche (Käfig)
CTR = (-6.20, 5.65, 0.94)               # Küche: Arbeitsplatte neben der Spüle (Käfig)
TAB_Y_N, TAB_Y_C = 4.18, 3.0            # Esstisch: Nordseite (Sitzreihe Maxi/Mama/Papa), Mitte
X_MAXI, X_MAMA, X_PAPA = -4.15, -3.45, -2.75
X_FRIEDA, X_OPA = -5.05, -1.85          # Stirnseiten


def tafel(col, frieda=True, opa=True, maxi=True, mama=True, papa=True, cake=True, cage=True, frieda_pose="sit", frieda_arms="hold_front",
          head_turn_frieda=0, maxi_arms="hold_front"):
    """Kaffeetafel in der Küche: Nordseite Maxi, Mama, Papa (Blick nach Süden), Stirnseiten Frieda (W) und Opa (O)."""
    out = {}
    if frieda:
        L.prop_chair("Stuhl_Frieda", (X_FRIEDA, TAB_Y_C, 0), 0, col)
        out["Frieda"] = L.build_figure("Tante_Frieda", (X_FRIEDA, TAB_Y_C), 0, frieda_pose, col, seat_z=0.46, arms=frieda_arms, head_turn_deg=head_turn_frieda)
    if opa:
        L.prop_chair("Stuhl_Opa", (X_OPA, TAB_Y_C, 0), 180, col)
        out["Opa"] = L.build_figure("Opa_Heinrich", (X_OPA, TAB_Y_C), 180, "sit", col, seat_z=0.46, arms="hold_front")
    if maxi:
        out["Maxi"] = L.build_figure("Maxi", (X_MAXI, TAB_Y_N), 270, "sit", col, seat_z=0.46, arms=maxi_arms)
    if mama:
        out["Mama"] = L.build_figure("Mama_Katrin", (X_MAMA, TAB_Y_N), 270, "sit", col, seat_z=0.46, arms="hold_front")
    if papa:
        out["Papa"] = L.build_figure("Papa_Thomas", (X_PAPA, TAB_Y_N), 270, "sit", col, seat_z=0.46, arms="hold_front")
    if cake:
        L.prop_cake("Kuchen", (-3.45, 3.0, 0.80), col)
        for i, x in enumerate((-4.2, -3.4, -2.6)):
            L.prop_cup(f"Tasse_{i}", (x, 3.55, 0.80), col)
    if cage:
        L.prop_cage("Kaefig", CTR, col, facing_deg=-41)
    return out


# ================================================================== BLOCK A  Ankunft (Einfahrt, Veranda, Flur, Kinderzimmer)
@scene("SH001", ((10.0, -9.2, 1.45), (13.6, -10.9, 1.20), 24.0))
def _(col):
    L.prop_car("Auto", *CAR, col, door_open="FR")                                       # Beifahrertür offen
    L.build_figure("Tante_Frieda", (12.4, -11.3), 300, "wave", col)                      # steht neben der offenen Tür
    L.build_figure("Mama_Katrin", (10.6, -8.0), 300, "wave", col)
    L.prop_dog("Bello", (9.9, -8.3, 0), 300, col)


@scene("SH002", ((12.0, -13.9, 1.55), (12.3, -9.0, 1.30), 30.0))
def _(col):
    L.prop_car("Auto", *CAR, col, door_open="FR")
    L.build_figure("Tante_Frieda", (13.0, -11.6), 100, "hold_front", col)                # Rücken zur Kamera
    L.build_figure("Mama_Katrin", (12.3, -9.0), 285, "wave", col)                        # frontal, begrüßt


@scene("SH003", ((11.6, -9.0, 1.55), (13.8, -8.0, 1.30), 26.0))
def _(col):
    L.prop_car("Auto", *CAR, col, door_open="FR")
    lid = L.box("Kofferraumklappe", (14.3, -8.3, 1.35), (1.5, 0.05, 0.9), L.mat("MAT_Auto_Blau", (0.16, 0.40, 0.72, 1)), col)
    lid.rotation_euler = (math.radians(-72), 0, 0)
    L.build_figure("Tante_Frieda", (13.3, -7.7), 235, "wave", col, head_turn_deg=-20)   # öffnet den Kofferraum, lacht zur Kamera
    L.build_figure("Mama_Katrin", (11.4, -9.8), 20, "stand", col)


@scene("SH010", ((14.2, -17.4, 1.50), (12.6, -11.6, 1.40), 28.0))
def _(col):
    L.prop_car("Auto", *CAR, col)
    r = L.build_figure("Tante_Frieda", (13.0, -13.9), 275, "hold_front", col)           # hält den Käfig im Arm
    L.prop_cage("Kaefig", ((r["hand_L"] + r["hand_R"]).x / 2, (r["hand_L"] + r["hand_R"]).y / 2, r["hand_L"].z - 0.62), col, facing_deg=90)
    L.build_figure("Mama_Katrin", (11.4, -11.6), 280, "stand", col)


@scene("SH020", ((-4.7, -8.8, 3.45), (-4.7, -6.3, 3.95), 48.0))
def _(col):
    hide_blockout_hasi()
    for o in bpy.data.objects:
        if o.name == "DET_Glas_OG_Aussenwand_Sued_window_1":
            o.hide_render = True                                                        # Fenster offen
    r = L.build_figure("Maxi", (-4.7, -5.8), 270, "hold_front", col, floor_z=Z_OG)       # lauscht am Fenster, frontal von der Straße
    hasi(r, col, "hand_R", 270, dz=0.0)


@scene("SH030", ((11.4, -9.9, 1.50), (12.6, -14.0, 1.10), 28.0))
def _(col):
    L.prop_car("Auto", *CAR, col)
    L.build_figure("Papa_Thomas", (12.9, -11.4), 235, "hold_front", col)             # Vordergrund links, zerrt am Koffer
    L.prop_suitcase("Koffer", (12.2, -12.4, 0), 200, col)
    L.build_figure("Tante_Frieda", (12.0, -13.5), 90, "point", col)                   # frontal zur Kamera, zeigt auf den Koffer


@scene("SH032", ((12.7, -14.6, 1.35), (12.9, -11.4, 1.25), 38.0))
def _(col):
    L.prop_car("Auto", *CAR, col)
    r = L.build_figure("Papa_Thomas", (12.9, -11.4), 268, "hold_front", col)          # hebt ächzend den Koffer, frontal
    L.prop_suitcase("Koffer", (r["hand_L"].x, r["hand_L"].y - 0.1, 0), 268, col)
    L.build_figure("Tante_Frieda", (11.7, -13.3), 60, "point", col)


@scene("SH040", ((0.3, -0.2, 1.35), (0.3, -3.0, 1.20), 30.0))
def _(col):
    L.build_figure("Tante_Frieda", (0.3, -3.0), 90, "hold_front", col)
    L.build_figure("Mama_Katrin", (0.55, -4.6), 90, "stand", col)


@scene("SH042", ((0.8, -0.9, 1.30), (0.3, -3.0, 1.25), 40.0))
def _(col):
    L.build_figure("Tante_Frieda", (0.3, -3.0), 90, "hold_front", col)
    L.build_figure("Mama_Katrin", (0.55, -4.6), 90, "stand", col)


@scene("SH041", ((-0.5, -1.6, 1.30), (0.55, -4.6, 1.25), 36.0))
def _(col):
    L.build_figure("Tante_Frieda", (0.3, -3.0), 90, "hold_front", col)
    L.build_figure("Mama_Katrin", (0.55, -4.6), 90, "hold_front", col)


@scene("SH047", ((-6.4, -1.6, 3.95), (-2.4, -1.4, 3.80), 24.0))
def _(col):
    r = L.build_figure("Tante_Frieda", (-3.1, -1.3), 180, "walk", col, floor_z=Z_OG)  # tritt mit dem Käfig ein
    L.prop_cage("Kaefig", (r["hand_R"].x, r["hand_R"].y, r["hand_R"].z - 0.62), col, facing_deg=180)


@scene("SH048", ((-5.4, -2.3, 4.15), (-7.55, -3.6, 3.60), 38.0))
def _(col):
    pass   # Hasi liegt auf dem Kissen (aus dem Blockout)


@scene("SH050", ((-7.4, -3.6, 3.70), (-5.0, -3.4, 3.72), 26.0))
def _(col):
    hide_blockout_hasi()
    r = L.build_figure("Tante_Frieda", (-5.0, -3.4), 180, "hold_front", col, floor_z=Z_OG)   # steht vorm Bett, Hasi auf Hüfthöhe
    L.prop_hasi("Hasi", (-5.28, -3.42, Z_OG + 0.74), col, 180)
    L.prop_cage("Kaefig", (-4.4, -2.5, Z_OG), col, facing_deg=180)
    L.prop_suitcase("Koffer", (-3.4, -0.3, Z_OG), 90, col, open_lid=True)


@scene("SH051", ((-7.4, -3.6, 3.70), (-3.2, -2.0, 3.80), 28.0))
def _(col):
    hide_blockout_hasi()
    r = L.build_figure("Tante_Frieda", (-5.0, -3.4), 180, "hold_front", col, floor_z=Z_OG)   # steht vorm Bett, Hasi auf Hüfthöhe
    L.prop_hasi("Hasi", (-5.28, -3.42, Z_OG + 0.74), col, 180)
    L.prop_cage("Kaefig", (-4.4, -2.5, Z_OG), col, facing_deg=180)
    L.build_figure("Maxi", (-3.4, -1.5), 195, "hold_front", col, floor_z=Z_OG)               # steht frontal in der Tür


@scene("SH052", ((-4.8, -5.3, 3.85), (-4.9, -3.0, 3.70), 32.0))
def _(col):
    hide_blockout_hasi()
    r = L.build_figure("Tante_Frieda", (-5.0, -3.4), 180, "hold_front", col, floor_z=Z_OG)
    L.prop_hasi("Hasi", (-5.28, -3.42, Z_OG + 0.74), col, 180)
    L.build_figure("Maxi", (-4.55, -2.6), 270, "point", col, floor_z=Z_OG)               # greift eingeschnappt nach Hasi, frontal
    L.prop_cage("Kaefig", (-3.9, -2.3, Z_OG), col, facing_deg=180)


@scene("SH058", ((-5.5, -2.7, 3.80), (-7.9, -1.8, 3.80), 32.0))
def _(col):
    hide_blockout_hasi()
    r = L.build_figure("Tante_Frieda", (-7.5, -1.2), 250, "hold_front", col, floor_z=Z_OG)
    L.prop_cage("Kaefig", (-7.85, -1.95, 3.45), col, facing_deg=0)                          # wird gerade auf den Nachttisch gestellt


@scene("SH060", ((-4.6, -0.2, 4.05), (-7.5, -2.1, 3.80), 30.0))
def _(col):
    hide_blockout_hasi()
    L.prop_cage("Kaefig", NT, col, facing_deg=0)
    L.build_figure("Tante_Frieda", (-7.7, -0.9), 255, "stand", col, floor_z=Z_OG)


# ================================================================== BLOCK B  Der Auftrag (Garten)
GATE = (-18.9, 1.8)


@scene("SH065", ((-11.6, 0.4, 1.05), (-14.5, 1.3, 0.55), 34.0))
def _(col):
    L.build_figure("Maxi", (-13.6, 1.1), 20, "walk", col, head_turn_deg=-20)
    ball(col, (-13.0, 0.9, 0.11))


@scene("SH070", ((-13.2, 1.7, 1.25), (-18.3, 1.8, 1.00), 30.0))
def _(col):
    L.build_figure("Anna", (GATE[0], GATE[1]), 0, "sit", col, seat_z=1.02, arms="point")   # weit hinten auf dem Tor, ruft
    L.build_figure("Maxi", (-14.6, 1.2), 180, "stand", col)                                  # Rücken zur Kamera
    ball(col, (-14.9, 0.8, 0.11))


@scene("SH075", ((-14.2, -0.8, 1.10), (-16.8, 1.6, 0.80), 30.0))
def _(col):
    L.build_figure("Anna", (GATE[0], GATE[1]), 0, "sit", col, seat_z=1.02, arms="wave")
    r = L.build_figure("Maxi", (-15.4, 1.2), 190, "walk", col)
    ball(col, (r["hand_L"].x, r["hand_L"].y, r["hand_L"].z - 0.05))


@scene("SH071", ((-14.0, 1.7, 1.20), (-17.6, 1.8, 0.95), 34.0))
def _(col):
    r = L.build_figure("Anna", (GATE[0], GATE[1]), 0, "sit", col, seat_z=1.02, arms="lift")   # Aufstellung wie SH070
    L.prop_glitterstone("Glitzerstein", r["hand_R"] + V(0, 0, 0.05), col)
    L.build_figure("Maxi", (-17.0, 1.4), 180, "stand", col)


@scene("SH072", ((-21.0, 3.8, 1.90), (-17.0, 1.4, 0.95), 30.0))
def _(col):
    L.build_figure("Anna", (GATE[0], GATE[1]), 0, "sit", col, seat_z=1.02, arms="point")     # Rücken zur Kamera
    L.build_figure("Maxi", (-17.0, 1.4), 180, "point", col)                                  # spricht frontal zur Kamera


# ================================================================== BLOCK C  Versuch 1: die Dusche (Kinderzimmer)
@scene("SH080", ((-3.3, -1.1, 3.50), (-7.0, -2.0, 3.55), 28.0))
def _(col):
    hide_blockout_hasi()
    L.prop_cage("Kaefig", NT, col, facing_deg=0)
    r = L.build_figure("Maxi", (-5.4, -1.3), 190, "walk", col, floor_z=Z_OG)
    L.prop_sprayer("Spruehflasche", r["hand_R"] + V(0, 0, 0.02), col)


@scene("SH081", ((-4.9, -0.1, 3.75), (-7.6, -1.9, 3.70), 28.0))
def _(col):
    hide_blockout_hasi()
    L.prop_cage("Kaefig", NT, col, facing_deg=-25, wet=True, wings_open=True)
    r = L.build_figure("Maxi", (-6.7, -1.0), 215, "point", col, floor_z=Z_OG)
    L.prop_sprayer("Spruehflasche", r["hand_R"] + V(0.05, -0.05, 0.0), col)


@scene("SH089", ((-4.8, -1.3, 3.90), (-2.2, -1.3, 3.80), 28.0))
def _(col):
    hide_blockout_hasi()
    L.prop_cage("Kaefig", NT, col, facing_deg=0, wet=True)
    L.build_figure("Tante_Frieda", (-2.5, -1.3), 180, "stand", col, floor_z=Z_OG)    # öffnet die Tür, groß im Bild


@scene("SH090", ((-7.1, -2.8, 3.95), (-7.85, -1.2, 3.70), 28.0))
def _(col):
    hide_blockout_hasi()
    L.prop_cage("Kaefig", NT, col, facing_deg=0, wet=True)
    L.build_figure("Tante_Frieda", (-7.85, -1.15), 270, "crouch", col, floor_z=Z_OG)
    r = L.build_figure("Maxi", (-6.5, -3.5), 0, "sit", col, seat_z=3.46, arms="hold_front")
    L.prop_book("Bilderbuch", r["hand_R"] + V(0, 0, 0.0), col, 90)


@scene("SH091", ((-3.0, -1.2, 4.25), (-6.8, -2.8, 3.75), 24.0))
def _(col):
    hide_blockout_hasi()
    L.prop_cage("Kaefig", NT, col, facing_deg=0, wet=True)
    L.build_figure("Tante_Frieda", (-7.85, -1.15), 270, "crouch", col, floor_z=Z_OG)
    r = L.build_figure("Maxi", (-6.5, -3.5), 0, "sit", col, seat_z=3.46, arms="hold_front")
    L.prop_book("Bilderbuch", r["hand_R"] + V(0, 0, 0.0), col, 90)


@scene("SH092", ((-4.9, -1.0, 3.30), (-2.4, -1.0, 3.05), 35.0))
def _(col):
    hide_blockout_hasi()
    L.prop_dog("Bello", (-3.0, -1.0, Z_OG), 180, col)


@scene("SH093", ((-6.5, -1.6, 3.85), (-7.85, -2.1, 3.75), 38.0))
def _(col):
    hide_blockout_hasi()
    L.prop_cage("Kaefig", NT, col, facing_deg=0, wet=True)
    L.build_figure("Tante_Frieda", (-7.85, -1.15), 270, "crouch", col, floor_z=Z_OG)
    r = L.build_figure("Maxi", (-6.5, -3.5), 0, "sit", col, seat_z=3.46, arms="hold_front")
    L.prop_book("Bilderbuch", r["hand_R"] + V(0, 0, 0.0), col, 90)


@scene("SH094", ((-3.0, -1.7, 4.20), (-6.4, -1.3, 3.90), 30.0))
def _(col):
    hide_blockout_hasi()
    r = L.build_figure("Tante_Frieda", (-7.2, -1.3), 0, "hold_front", col, floor_z=Z_OG)
    L.prop_cage("Kaefig", ((r["hand_L"] + r["hand_R"]).x / 2, (r["hand_L"] + r["hand_R"]).y / 2, r["hand_L"].z - 0.62), col, facing_deg=180, wet=True)
    r2 = L.build_figure("Maxi", (-6.5, -3.5), 0, "sit", col, seat_z=3.46, arms="hold_front")
    L.prop_book("Bilderbuch", r2["hand_R"] + V(0, 0, 0.0), col, 90)


# ================================================================== BLOCK D  Versuch 2: Kaffeetafel (Küche)
@scene("SH100", ((-3.0, 1.2, 1.50), (-5.0, 4.5, 1.15), 26.0))
def _(col):
    tafel(col, opa=False, maxi=False, mama=False, papa=False, cake=False, frieda_arms="hold_front")
    r = L.build_figure("Mama_Katrin", (-3.4, 4.5), 270, "hold_front", col)
    L.prop_cake("KuchenHand", (r["hand_L"] + r["hand_R"]).__mul__(0.5) + V(0, 0, -0.08), col)


@scene("SH101", ((-3.3, 2.5, 1.25), (-5.0, 3.0, 1.10), 30.0))
def _(col):
    tafel(col, opa=False, maxi=False, mama=False, papa=False, frieda_arms="wave")


@scene("SH110", ((-0.3, -1.6, 1.35), (0.3, -5.3, 1.30), 30.0))
def _(col):
    L.build_figure("Opa_Heinrich", (0.3, -5.3), 90, "lift", col)
    L.build_figure("Tante_Frieda", (0.3, -3.3), 270, "hold_front", col)
    L.prop_cap("Muetze", (0.45, -5.0, 1.55), col)


@scene("SH111", ((1.0, -5.7, 1.30), (0.3, -3.3, 1.30), 30.0))
def _(col):
    L.build_figure("Opa_Heinrich", (0.3, -5.3), 90, "stand", col)
    L.build_figure("Tante_Frieda", (0.3, -3.3), 270, "point", col)


@scene("SH112", ((-0.3, -1.6, 1.35), (0.3, -5.3, 1.30), 28.0))
def _(col):
    L.build_figure("Opa_Heinrich", (0.3, -5.3), 90, "hold_front", col)
    L.build_figure("Tante_Frieda", (0.3, -3.3), 270, "stand", col)


@scene("SH120", ((-3.45, 0.9, 1.45), (-3.45, 3.5, 0.85), 20.0))
def _(col):
    tafel(col, head_turn_frieda=-90)


@scene("SH122", ((-3.3, 2.5, 1.25), (-5.0, 3.0, 1.10), 30.0))
def _(col):
    tafel(col, opa=False, maxi=False, mama=False, frieda_arms="hold_front")


@scene("SH123", ((-2.85, 2.2, 1.30), (-2.8, 4.2, 1.10), 30.0))
def _(col):
    tafel(col, frieda=False, opa=False, maxi=False)


@scene("SH124", ((-4.15, 2.3, 1.15), (-4.15, 4.2, 1.00), 32.0))
def _(col):
    r = tafel(col, frieda=False, opa=False, mama=False, papa=False)
    hasi(r["Maxi"], col, "hand_R", 270, dz=0.02)


@scene("SH130", ((-3.2, 3.2, 1.50), (-6.2, 5.5, 1.10), 28.0))
def _(col):
    L.prop_cage("Kaefig", CTR, col, facing_deg=-41)
    r = L.build_figure("Maxi", (-6.0, 4.9), 70, "hold_front", col, floor_z=0.44)     # steht auf dem Tritthocker
    hasi(r, col, "hand_L", 70, dz=0.0)
    L.build_figure("Anna", (-6.9, 6.8), 270, "wave", col, floor_z=0.18)               # draußen vor dem Sprossenfenster über der Spüle


@scene("SH140", ((-3.3, 2.5, 1.25), (-5.0, 3.0, 1.10), 30.0))
def _(col):
    tafel(col, opa=False, maxi=False, mama=False, papa=False, frieda_arms="lift")


@scene("SH141", ((-5.0, 4.6, 1.35), (-6.2, 5.7, 1.15), 40.0))
def _(col):
    L.prop_cage("Kaefig", CTR, col, facing_deg=-41)


@scene("SH143", ((-4.6, 2.0, 1.25), (-1.9, 3.0, 1.10), 30.0))
def _(col):
    tafel(col, frieda=False, maxi=False, mama=False, papa=False)


@scene("SH144", ((-5.0, 4.6, 1.35), (-6.2, 5.7, 1.15), 40.0))
def _(col):
    L.prop_cage("Kaefig", CTR, col, facing_deg=-41)


@scene("SH150", ((-3.3, 2.5, 1.30), (-5.0, 3.0, 1.15), 30.0))
def _(col):
    L.prop_chair("Stuhl_Frieda", (X_FRIEDA - 0.25, TAB_Y_C, 0), 0, col)
    L.build_figure("Tante_Frieda", (-5.0, 3.0), 0, "stand", col, arms="hands_hip")
    L.prop_cake("Kuchen", (-3.45, 3.0, 0.80), col)


@scene("SH151", ((-4.15, 2.3, 1.15), (-4.15, 4.2, 1.00), 32.0))
def _(col):
    r = tafel(col, frieda=False, opa=False, mama=False, papa=False)
    hasi(r["Maxi"], col, "hand_R", 270, dz=0.10)


@scene("SH152", ((-4.15, 2.3, 1.20), (-4.15, 4.4, 1.05), 32.0))
def _(col):
    for o in bpy.data.objects:
        if o.name.startswith("KU_Stuhl_N1"):
            o.hide_render = True                                                       # Stuhl zurückgeschoben
    r = L.build_figure("Maxi", (X_MAXI, 4.55), 270, "hold_front", col)
    hasi(r, col, "hand_R", 270, dz=-0.10)


@scene("SH160", ((-3.4, 2.8, 1.40), (-5.3, 4.9, 1.20), 28.0))
def _(col):
    L.prop_chair("Stuhl_Frieda", (X_FRIEDA, TAB_Y_C, 0), 0, col)
    r = L.build_figure("Tante_Frieda", (-5.4, 4.9), 320, "hold_front", col)
    L.prop_cage("Kaefig", (r["hand_L"] + r["hand_R"]).__mul__(0.5) - V(0, 0, 0.28), col, facing_deg=150)


# ================================================================== BLOCK G/H  Tiefpunkt und Reparatur (Flur, Dämmerung)
@scene("SH170", ((0.2, -1.4, 1.30), (1.2, 2.0, 0.75), 18.0))
def _(col):
    L.build_figure("Maxi", (1.4, 1.95), 270, "sit", col, seat_z=0.17)
    L.prop_hasi("Hasi", (1.4, 1.5, 0.30), col, 270)
    r2 = L.build_figure("Papa_Thomas", (-0.1, -0.2), 255, "walk", col)
    L.prop_suitcase("Koffer", (r2["hand_R"].x, r2["hand_R"].y - 0.2, 0), 255, col)
    L.build_figure("Tante_Frieda", (-0.7, -1.0), 250, "stand", col)


@scene("SH171", ((1.3, -0.6, 0.90), (1.4, 1.95, 0.70), 30.0))
def _(col):
    L.build_figure("Maxi", (1.4, 1.95), 270, "sit", col, seat_z=0.17, arms="hold_front")
    L.prop_hasi("Hasi", (1.4, 1.55, 0.28), col, 270)


@scene("SH173", ((0.3, -1.4, 1.30), (0.3, -4.0, 1.25), 32.0))
def _(col):
    L.build_figure("Tante_Frieda", (0.3, -3.9), 90, "hold_front", col)


@scene("SH180", ((-0.9, -1.4, 1.25), (1.0, -3.4, 1.00), 28.0))
def _(col):
    L.build_figure("Maxi", (1.0, -3.4), 180, "hold_front", col)
    r = L.build_figure("Tante_Frieda", (-0.3, -3.4), 0, "hold_front", col)
    L.build_figure("Mama_Katrin", (0.4, -1.6), 270, "stand", col)
    L.prop_cakebox("Kuchendose", (0.85, -3.35, 0.78), col)


@scene("SH181", ((1.6, -3.0, 1.20), (-0.3, -3.4, 1.20), 28.0))
def _(col):
    L.build_figure("Maxi", (1.0, -3.4), 180, "hold_front", col)
    r = L.build_figure("Tante_Frieda", (-0.3, -3.4), 0, "hold_front", col)
    L.build_figure("Mama_Katrin", (0.4, -1.6), 270, "stand", col)
    L.prop_cakebox("Kuchendose", (-0.2, -3.35, 0.95), col)


@scene("SH182", ((0.4, -5.9, 1.30), (0.4, -1.6, 1.25), 34.0))
def _(col):
    L.build_figure("Maxi", (1.0, -3.4), 180, "hold_front", col)
    r = L.build_figure("Tante_Frieda", (-0.3, -3.4), 0, "hold_front", col)
    L.build_figure("Mama_Katrin", (0.4, -1.6), 270, "wave", col)
    L.prop_cakebox("Kuchendose", (-0.2, -3.35, 0.95), col)


@scene("SH183", ((-0.9, -1.4, 1.25), (1.0, -3.4, 1.00), 28.0))
def _(col):
    L.build_figure("Maxi", (1.0, -3.4), 180, "hold_front", col)
    r = L.build_figure("Tante_Frieda", (-0.3, -3.4), 0, "hold_front", col)
    L.build_figure("Mama_Katrin", (0.4, -1.6), 270, "stand", col)
    L.prop_cakebox("Kuchendose", (-0.2, -3.35, 0.95), col)


@scene("SH184", ((0.3, -2.5, 1.25), (0.3, -4.7, 1.15), 35.0))
def _(col):
    L.prop_suitcase("Koffer", (0.3, -4.7, 0), 90, col)
    L.prop_cage("Kaefig", (0.3, -4.7, 0.90), col, facing_deg=-90, wings_open=True)


@scene("SH190", ((8.4, -10.4, 1.40), (14.0, -10.5, 1.25), 26.0))
def _(col):
    e, seats = L.prop_car("Auto", *CAR, col, door_open=None)
    L.build_figure("Tante_Frieda", (seats["VR"].x, seats["VR"].y), -90, "sit", col, seat_z=seats["VR"].z, floor_z=0.62, arms="wave")
    L.prop_cage("Kaefig", (seats["VR"].x, seats["VR"].y, seats["VR"].z + 0.25), col, facing_deg=-90)
    L.build_figure("Mama_Katrin", (11.4, -8.8), 10, "wave", col)
    L.build_figure("Opa_Heinrich", (10.6, -9.5), 10, "wave", col)
    L.build_figure("Maxi", (11.9, -9.8), 10, "wave", col)


@scene("SH195", ((-15.0, 2.0, 1.10), (-18.6, 1.9, 0.95), 32.0))
def _(col):
    L.build_figure("Maxi", (-17.6, 2.0), 25, "stand", col, head_turn_deg=-35)
    L.build_figure("Anna", (-19.6, 1.8), 0, "point", col)
    L.prop_glitterstone("Glitzerstein", (-18.7, 1.9, 0.60), col)


# ================================================================== BLOCK I  Hochgefühl (Kinderzimmer, Abend)
@scene("SH200", ((-3.8, -3.0, 4.20), (-6.4, -3.3, 3.85), 26.0))
def _(col):
    hide_blockout_hasi()
    r = L.build_figure("Maxi", (-6.6, -3.5), 0, "lift", col, floor_z=3.46)
    L.prop_hasi("Hasi", r["hand_R"] + V(0, 0, 0.05), col, 0)
    L.build_figure("Papa_Thomas", (-4.6, -1.5), 200, "stand", col, floor_z=Z_OG, arms="lift")


@scene("SH201", ((-2.6, -3.0, 4.05), (-5.3, -3.2, 3.75), 24.0))
def _(col):
    hide_blockout_hasi()
    r = L.build_figure("Opa_Heinrich", (-5.2, -3.5), 0, "sit", col, seat_z=3.30, floor_z=Z_OG, arms="hold_front")
    L.prop_tin("MutDose", (r["hand_L"] + r["hand_R"]).__mul__(0.5) - V(0, 0, 0.05), col)
    L.build_figure("Maxi", (-4.4, -2.9), 150, "hold_front", col, floor_z=Z_OG)


@scene("SH210", ((-1.9, -1.1, 4.30), (-6.5, -2.8, 3.85), 20.0))
def _(col):
    hide_blockout_hasi()
    r = L.build_figure("Maxi", (-6.9, -3.4), 0, "lift", col, floor_z=3.46)
    L.prop_hasi("Hasi", r["hand_R"] + V(0, 0, 0.05), col, 0)
    L.build_figure("Mama_Katrin", (-5.0, -2.0), 0, "lift", col, floor_z=Z_OG)
    L.build_figure("Papa_Thomas", (-4.2, -3.2), 0, "lift", col, floor_z=Z_OG)
    L.build_figure("Opa_Heinrich", (-4.9, -0.4), 0, "lift", col, floor_z=Z_OG)
    L.prop_dog("Bello", (-3.4, -1.8, Z_OG), 0, col)


# ------------------------------------------------------------------ Ablauf
def clear_scene_col():
    col = bpy.data.collections.get(SCENE_COL)
    if col:
        for o in list(col.objects):
            bpy.data.objects.remove(o, do_unlink=True)
        bpy.data.collections.remove(col)
    for o in bpy.data.objects:
        if o.name.startswith(("KU_Stuhl", "KZ_Hasi", "DET_Glas")):
            o.hide_render = False
    for o in list(bpy.data.objects):
        if o.name.startswith("SZENE_CAM_"):
            bpy.data.objects.remove(o, do_unlink=True)


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    wanted = argv or list(SCENES)
    os.makedirs(BLEND_DIR, exist_ok=True)
    L.configure_render(1600, 900)
    for c in bpy.data.collections:
        c.hide_render = False
    cam_col = L.get_collection("99_Kameras")
    for sid in wanted:
        spec = SCENES[sid]
        clear_scene_col()
        col = L.get_collection(SCENE_COL)
        spec["build"](col)
        loc, tgt, lens = spec["cam"]
        cam = L.add_camera(f"SZENE_CAM_{sid}", loc, tgt, lens, cam_col)
        L.render_camera(cam, os.path.join(OUT_DIR, f"{sid}_blender.png"))
        print("Szene fertig:", sid)
    clear_scene_col()


if __name__ == "__main__":
    main()
