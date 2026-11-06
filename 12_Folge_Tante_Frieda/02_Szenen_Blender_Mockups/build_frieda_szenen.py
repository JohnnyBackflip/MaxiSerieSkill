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


def schrank(col, open_deg=0.0, cage=False):
    """Eigener Kleiderschrank statt des Blockout-Kastens (der Käfig passt hinein)."""
    for o in bpy.data.objects:
        if o.name.startswith("KZ_Kleiderschrank"):
            o.hide_render = True
    return L.prop_wardrobe("Schrank", (-2.45, -5.68, Z_OG), col, open_deg=open_deg, cage=cage)


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
    L.build_figure("Mama_Katrin", (12.3, -9.0), 285, "open", col)                        # Arme weit auseinander, frontal


@scene("SH003", ((11.6, -9.0, 1.55), (13.8, -8.0, 1.30), 26.0))
def _(col):
    L.prop_car("Auto", *CAR, col, door_open="FR")
    lid = L.box("Kofferraumklappe", (14.3, -8.3, 1.35), (1.5, 0.05, 0.9), L.mat("MAT_Auto_Blau", (0.16, 0.40, 0.72, 1)), col)
    lid.rotation_euler = (math.radians(-72), 0, 0)
    L.build_figure("Tante_Frieda", (13.3, -7.7), 270, "point", col, head_turn_deg=55)       # blickt zum Kofferraum, holt etwas heraus
    L.prop_cage("Kaefig", (14.0, -7.0, 0), col, facing_deg=215)                              # der Käfig steht schon hinten am Auto
    L.build_figure("Mama_Katrin", (11.4, -9.8), 20, "stand", col)


@scene("SH010", ((11.6, -9.0, 1.55), (13.8, -8.0, 1.30), 26.0))
def _(col):
    L.prop_car("Auto", *CAR, col, door_open="FR")
    r = L.build_figure("Tante_Frieda", (13.3, -7.7), 250, "hold_front", col, head_turn_deg=20)   # Kofferraum zu, Käfig in der Hand
    L.prop_cage("Kaefig", ((r["hand_L"] + r["hand_R"]).x / 2, (r["hand_L"] + r["hand_R"]).y / 2, r["hand_L"].z - 0.62), col, facing_deg=215)
    L.build_figure("Mama_Katrin", (11.4, -9.8), 20, "stand", col)


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
    r = L.build_figure("Tante_Frieda", (0.3, -3.0), 90, "hold_front", col)
    L.prop_cage("Kaefig", ((r["hand_L"] + r["hand_R"]).x / 2, (r["hand_L"] + r["hand_R"]).y / 2 + 0.05, r["hand_L"].z - 0.62), col, facing_deg=90)
    L.build_figure("Mama_Katrin", (0.55, -4.6), 90, "stand", col)


@scene("SH042", ((0.8, -0.9, 1.30), (0.3, -3.0, 1.25), 40.0))
def _(col):
    r = L.build_figure("Tante_Frieda", (0.3, -3.0), 90, "hold_front", col)
    L.prop_cage("Kaefig", ((r["hand_L"] + r["hand_R"]).x / 2, (r["hand_L"] + r["hand_R"]).y / 2 + 0.05, r["hand_L"].z - 0.62), col, facing_deg=90)
    L.build_figure("Mama_Katrin", (0.55, -4.6), 90, "stand", col)


@scene("SH041", ((0.95, -3.6, 1.55), (0.55, -4.6, 1.58), 55.0))
def _(col):
    r = L.build_figure("Tante_Frieda", (0.3, -3.0), 90, "hold_front", col)
    L.prop_cage("Kaefig", ((r["hand_L"] + r["hand_R"]).x / 2, (r["hand_L"] + r["hand_R"]).y / 2 + 0.05, r["hand_L"].z - 0.62), col, facing_deg=90)
    L.build_figure("Mama_Katrin", (0.55, -4.6), 90, "hold_front", col)                                                                      # Fokus auf Mama, Frieda aus dem Bild


@scene("SH047", ((-4.4, 1.0, 4.15), (-1.3, 1.0, 3.95), 40.0))
def _(col):
    hide_blockout_hasi()
    r = L.build_figure("Tante_Frieda", (-1.9, 1.0), 180, "hands_hip", col, floor_z=Z_OG)     # schließt die Tür hinter sich, Tür und Rahmen im Bild
    L.prop_cage("Kaefig", (-2.0, 0.55, Z_OG + 0.3), col, facing_deg=0)


@scene("SH048", ((-5.6, -2.6, 3.95), (-7.5, -3.5, 3.62), 32.0))
def _(col):
    hide_blockout_hasi()
    L.prop_hasi("Hasi", (-7.4, -3.55, 3.46), col, 0, scale=2.2)                             # Hasi deutlich auf dem Bett


@scene("SH050", ((-7.4, -3.6, 3.70), (-5.0, -3.4, 3.72), 26.0))
def _(col):
    hide_blockout_hasi()
    r = L.build_figure("Tante_Frieda", (-5.0, -3.4), 180, "hold_front", col, floor_z=Z_OG)   # steht vorm Bett, Hasi auf Hüfthöhe
    L.prop_hasi("Hasi", (-5.28, -3.42, Z_OG + 0.74), col, 180)
    L.prop_cage("Kaefig", (-4.4, -2.5, Z_OG), col, facing_deg=180)
    L.prop_suitcase("Koffer", (-3.4, -0.3, Z_OG), 90, col, open_lid=True)


@scene("SH051", ((-3.7, 0.4, 3.85), (-1.7, 1.0, 3.80), 60.0))
def _(col):
    hide_blockout_hasi()
    L.build_figure("Maxi", (-1.8, 1.0), 185, "hold_front", col, floor_z=Z_OG, mood="angry")   # Closeup in der Tür, böser Blick


@scene("SH052", ((-4.8, -5.3, 3.85), (-4.9, -3.0, 3.70), 32.0))
def _(col):
    hide_blockout_hasi()
    r = L.build_figure("Tante_Frieda", (-5.0, -3.4), 180, "hold_front", col, floor_z=Z_OG)
    r2 = L.build_figure("Maxi", (-4.55, -2.6), 270, "point", col, floor_z=Z_OG, mood="angry")   # nimmt ihr Hasi ab
    L.prop_hasi("Hasi", r2["hand_R"] + V(0, 0, 0.0), col, 200)
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


@scene("SH075", ((-19.5, 4.4, 1.90), (-17.0, 1.4, 1.00), 40.0))
def _(col):
    L.build_figure("Anna", (GATE[0], GATE[1]), 0, "sit", col, seat_z=1.02, arms="point")     # Rücken zur Kamera
    L.build_figure("Maxi", (-17.0, 1.4), 180, "stand", col, mood="sad")                      # frontal, enttäuscht
    ball(col, (-16.8, 1.1, 0.11))


@scene("SH071", ((-14.0, 1.7, 1.20), (-17.6, 1.8, 0.95), 34.0))
def _(col):
    L.build_figure("Anna", (GATE[0], GATE[1]), 0, "sit", col, seat_z=1.02, arms="point")   # schlägt einen Streich vor
    L.build_figure("Maxi", (-17.0, 1.4), 180, "stand", col)


@scene("SH072", ((-19.4, 3.1, 1.30), (-17.0, 1.4, 0.95), 58.0))
def _(col):
    L.build_figure("Anna", (GATE[0], GATE[1]), 0, "sit", col, seat_z=1.02, arms="stand")     # Rücken zur Kamera
    L.build_figure("Maxi", (-17.0, 1.4), 180, "point", col)                                  # spricht frontal, Kamera näher am Gesicht


# ================================================================== BLOCK C  Versuch 1: die Dusche (Kinderzimmer)
@scene("SH080", ((-5.0, 0.2, 3.80), (-7.4, -1.6, 3.60), 30.0))
def _(col):
    hide_blockout_hasi(); schrank(col, 0)
    r = L.build_figure("Maxi", (-7.3, -1.3), 200, "stand", col, floor_z=Z_OG)                # trägt den Käfig am Griff neben sich
    L.prop_cage("Kaefig", (-7.2, -2.05, Z_OG), col, facing_deg=0)                            # Käfig steht links neben ihm, überlappt ihn nicht


@scene("SH081", ((-3.9, -2.3, 3.95), (-2.5, -5.2, 3.60), 30.0))
def _(col):
    hide_blockout_hasi(); schrank(col, 100, cage=True)
    L.build_figure("Maxi", (-2.7, -4.4), 270, "hold_front", col, floor_z=Z_OG)               # versteckt den Käfig im Schrank


@scene("SH089", ((-4.3, 1.0, 4.25), (-1.5, 1.0, 4.20), 40.0))
def _(col):
    hide_blockout_hasi(); schrank(col, 0)
    L.build_figure("Tante_Frieda", (-1.6, 1.0), 180, "stand", col, floor_z=Z_OG, head_turn_deg=15)   # neugieriges Gesicht im Türrahmen


@scene("SH090", ((-2.45, -5.85, 3.95), (-2.8, -2.0, 3.85), 22.0))
def _(col):
    hide_blockout_hasi(); schrank(col, 165, cage=True)                                          # Kamera steht im Schrank
    L.build_figure("Tante_Frieda", (-2.8, -4.4), 270, "crouch", col, floor_z=Z_OG)
    r = L.build_figure("Maxi", (-6.9, -3.5), 180, "lie", col, floor_z=3.46, arms="lift")
    L.prop_book("Bilderbuch", r["hand_R"] + V(0, 0, 0.05), col, 90)


@scene("SH091", ((-6.7, -3.3, 3.80), (-2.7, -4.4, 3.90), 30.0))
def _(col):
    hide_blockout_hasi(); schrank(col, 165, cage=True)                                          # aus Maxis Sicht vom Bett
    L.build_figure("Tante_Frieda", (-2.9, -4.3), 200, "stand", col, floor_z=Z_OG, mood="suspicious")


@scene("SH092", ((-4.9, -1.0, 3.30), (-2.4, -1.0, 3.05), 35.0))
def _(col):
    hide_blockout_hasi()
    L.prop_dog("Bello", (-3.0, -1.0, Z_OG), 180, col)


@scene("SH093", ((-4.9, -3.0, 4.00), (-3.3, -4.4, 3.80), 32.0))
def _(col):
    hide_blockout_hasi(); schrank(col, 165)
    r = L.build_figure("Tante_Frieda", (-3.0, -4.5), 220, "hold_front", col, floor_z=Z_OG)
    L.prop_cage("Kaefig", ((r["hand_L"] + r["hand_R"]).x / 2, (r["hand_L"] + r["hand_R"]).y / 2, r["hand_L"].z - 0.62), col, facing_deg=140)


@scene("SH094", ((-4.5, -1.5, 4.10), (-7.2, -1.3, 3.95), 40.0))
def _(col):
    hide_blockout_hasi(); schrank(col, 165)
    r = L.build_figure("Tante_Frieda", (-7.2, -1.3), 0, "hold_front", col, floor_z=Z_OG)
    L.prop_cage("Kaefig", ((r["hand_L"] + r["hand_R"]).x / 2, (r["hand_L"] + r["hand_R"]).y / 2, r["hand_L"].z - 0.62), col, facing_deg=180)


# ================================================================== BLOCK D  Versuch 2: Kaffeetafel (Küche)
@scene("SH100", ((-3.0, 1.2, 1.50), (-5.0, 4.5, 1.15), 26.0))
def _(col):
    tafel(col, opa=False, maxi=False, mama=False, papa=False, cake=False, frieda_arms="hold_front")
    r = L.build_figure("Mama_Katrin", (-3.4, 4.5), 270, "hold_front", col)
    L.prop_cake("KuchenHand", (r["hand_L"] + r["hand_R"]).__mul__(0.5) + V(0, 0, -0.08), col)


@scene("SH101", ((-3.3, 2.5, 1.25), (-5.0, 3.0, 1.10), 30.0))
def _(col):
    r = tafel(col, opa=False, maxi=False, mama=False, papa=False, frieda_arms="sip")          # Ellbogen auf dem Tisch, Kaffee trinken
    L.prop_cup("Tasse_Frieda", (r["Frieda"]["hand_R"].x, r["Frieda"]["hand_R"].y, r["Frieda"]["hand_R"].z - 0.05), col)


@scene("SH110", ((-0.3, -1.6, 1.35), (0.3, -5.3, 1.30), 30.0))
def _(col):
    L.build_figure("Opa_Heinrich", (0.3, -5.3), 90, "lift", col)
    L.build_figure("Tante_Frieda", (0.3, -3.3), 270, "hold_front", col)
    L.prop_cap("Muetze", (0.45, -5.0, 1.55), col)


@scene("SH111", ((1.0, -5.7, 1.30), (0.3, -3.3, 1.30), 30.0))
def _(col):
    L.build_figure("Opa_Heinrich", (0.3, -5.3), 90, "stand", col)
    L.build_figure("Tante_Frieda", (0.3, -3.3), 270, "hands_hip", col)


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


@scene("SH141", ((-4.6, 4.2, 1.35), (-6.2, 5.65, 1.20), 30.0))
def _(col):
    L.prop_cage("Kaefig", CTR, col, facing_deg=-41)


@scene("SH143", ((-4.6, 2.0, 1.25), (-1.9, 3.0, 1.10), 30.0))
def _(col):
    tafel(col, frieda=False, maxi=False, mama=False, papa=False)


@scene("SH144", ((-4.9, 4.6, 1.30), (-6.2, 5.65, 1.15), 36.0))
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
@scene("SH170", ((0.3, -4.6, 1.30), (0.2, -1.0, 1.20), 30.0))
def _(col):
    r = L.build_figure("Papa_Thomas", (0.0, -2.3), 270, "walk", col)                          # trägt den Koffer gut sichtbar zur Haustür
    L.prop_suitcase("Koffer", (r["hand_R"].x, r["hand_R"].y - 0.05, 0), 270, col)
    L.build_figure("Tante_Frieda", (1.3, -3.3), 120, "stand", col)
    L.build_figure("Maxi", (1.4, 1.95), 270, "sit", col, seat_z=0.17)


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


@scene("SH082", ((-4.2, -5.0, 4.20), (-5.2, -2.8, 3.80), 28.0))
def _(col):
    hide_blockout_hasi(); schrank(col, 0)
    L.build_figure("Maxi", (-4.4, -3.2), 170, "walk", col, floor_z=Z_OG)                     # rennt in Richtung Bett


@scene("SH083", ((-2.6, -1.3, 3.95), (-6.6, -3.4, 3.70), 30.0))
def _(col):
    hide_blockout_hasi(); schrank(col, 0)
    r = L.build_figure("Maxi", (-6.9, -3.5), 180, "lie", col, floor_z=3.46, arms="lift")    # liegt auf dem Bett und liest
    L.prop_book("Bilderbuch", r["hand_R"] + V(0, 0, 0.05), col, 90)


@scene("SH084", ((-6.4, -1.6, 3.75), (-7.85, -2.1, 3.45), 55.0))
def _(col):
    hide_blockout_hasi(); schrank(col, 0)                                                    # Nachttisch leer


@scene("SH085", ((-4.9, -1.5, 4.20), (-6.9, -1.5, 4.20), 60.0))
def _(col):
    hide_blockout_hasi(); schrank(col, 0)
    L.build_figure("Tante_Frieda", (-6.9, -1.5), 0, "stand", col, floor_z=Z_OG, mood="startled")   # Closeup, erschrickt


@scene("SH086", ((-3.4, -1.5, 4.20), (-6.9, -1.5, 3.90), 26.0))
def _(col):
    hide_blockout_hasi(); schrank(col, 0)
    L.build_figure("Tante_Frieda", (-6.9, -1.5), 0, "face", col, floor_z=Z_OG, mood="startled")   # Hände vors Gesicht
    r = L.build_figure("Maxi", (-6.9, -3.5), 180, "lie", col, floor_z=3.46, arms="lift")
    L.prop_book("Bilderbuch", r["hand_R"] + V(0, 0, 0.05), col, 90)


@scene("SH087", ((-4.8, -3.4, 3.90), (-2.5, -5.5, 3.90), 28.0))
def _(col):
    hide_blockout_hasi(); schrank(col, 0)
    L.build_figure("Tante_Frieda", (-4.4, -2.4), 300, "face", col, floor_z=Z_OG, mood="startled")


@scene("SH095", ((-4.5, 0.8, 3.95), (-1.8, 1.0, 3.80), 34.0))
def _(col):
    hide_blockout_hasi(); schrank(col, 165, cage=True)
    L.build_figure("Maxi", (-1.9, 1.0), 190, "walk", col, floor_z=Z_OG)                      # rennt zur Tür hinaus und ruft zurück


@scene("SH145", ((-4.15, 2.5, 1.15), (-4.15, 4.2, 1.00), 50.0))
def _(col):
    tafel(col, frieda=False, opa=False, mama=False, papa=False, maxi_arms="face")             # verkneift sich das Lachen


STAIR_PAPA = ('    L.build_figure("Maxi", (1.4, 1.95), 270, "sit", col, seat_z=0.17, mood="sad")\n'
              '    L.build_figure("Papa_Thomas", (1.4, 1.0), 90, "crouch", col)')


@scene("SH174", ((0.9, -1.0, 1.00), (1.45, 1.9, 0.80), 30.0))
def _(col):
    L.build_figure("Maxi", (1.2, 1.95), 270, "sit", col, seat_z=0.17, mood="sad")
    L.build_figure("Papa_Thomas", (1.65, 1.95), 270, "sit", col, seat_z=0.17)                # Papa sitzt neben Maxi auf der Treppe


@scene("SH175", ((0.8, 0.2, 0.95), (1.5, 1.9, 0.85), 40.0))
def _(col):
    L.build_figure("Maxi", (1.2, 1.95), 270, "sit", col, seat_z=0.17, mood="sad")
    L.build_figure("Papa_Thomas", (1.65, 1.95), 270, "sit", col, seat_z=0.17)


ABSCHIED = ('    L.build_figure("Maxi", (1.0, -3.4), 180, "hold_front", col)\n'
            '    L.build_figure("Tante_Frieda", (-0.3, -3.4), 0, "hold_front", col)')


@scene("SH177", ((-0.9, -1.4, 1.25), (1.0, -3.4, 1.00), 28.0))
def _(col):
    L.build_figure("Maxi", (1.0, -3.4), 180, "hold_front", col)
    L.build_figure("Tante_Frieda", (-0.3, -3.4), 0, "hold_front", col)


@scene("SH178", ((-0.9, -2.2, 1.10), (1.0, -3.4, 1.00), 40.0))
def _(col):
    L.build_figure("Maxi", (1.0, -3.4), 180, "hold_front", col, mood="sad")
    L.build_figure("Tante_Frieda", (-0.3, -3.4), 0, "hold_front", col)


@scene("SH179", ((1.6, -3.0, 1.20), (-0.3, -3.4, 1.20), 28.0))
def _(col):
    L.build_figure("Maxi", (1.0, -3.4), 180, "hold_front", col)
    L.build_figure("Tante_Frieda", (-0.3, -3.4), 0, "hold_front", col)


@scene("SH186", ((-2.6, -3.0, 1.25), (-7.1, -3.0, 0.85), 30.0))
def _(col):
    L.build_figure("Mama_Katrin", (-7.1, -2.2), 0, "sit", col, seat_z=0.445)
    L.build_figure("Papa_Thomas", (-7.1, -3.1), 0, "sit", col, seat_z=0.445)
    L.build_figure("Tante_Frieda", (-7.1, -4.0), 0, "sit", col, seat_z=0.445, arms="wave")
    L.build_figure("Maxi", (-5.9, -3.0), 0, "sit", col, seat_z=0.08, arms="lift")
    L.prop_dog("Bello", (-5.7, -2.0, 0), 0, col)


@scene("SH041_B", ((0.95, -3.6, 1.55), (0.55, -4.6, 1.58), 55.0))
def _(col):
    r = L.build_figure("Tante_Frieda", (0.3, -3.0), 90, "hold_front", col)
    L.prop_cage("Kaefig", ((r["hand_L"] + r["hand_R"]).x / 2, (r["hand_L"] + r["hand_R"]).y / 2 + 0.05, r["hand_L"].z - 0.62), col, facing_deg=90)
    L.build_figure("Mama_Katrin", (0.55, -4.6), 90, "hold_front", col, mood="startled" if False else None)                                                                      # Zoom auf Mamas Gesicht


@scene("SH082_B", ((-3.6, -3.9, 4.60), (-6.4, -3.4, 4.25), 24.0))
def _(col):
    hide_blockout_hasi(); schrank(col, 0)
    L.build_figure("Maxi", (-6.4, -3.5), 0, "lift", col, floor_z=3.95)                       # springt aufs Bett


@scene("SH073", ((-19.5, 4.4, 1.90), (-17.0, 1.4, 1.00), 40.0))
def _(col):
    L.build_figure("Anna", (GATE[0], GATE[1]), 0, "sit", col, seat_z=1.02, arms="point")     # Rücken zur Kamera
    L.build_figure("Maxi", (-17.0, 1.4), 180, "face", col, mood="suspicious")               # überlegt, Hand am Kinn


@scene("SH074", ((-15.6, 1.7, 1.55), (-18.9, 1.8, 1.50), 65.0))
def _(col):
    L.build_figure("Anna", (GATE[0], GATE[1]), 0, "sit", col, seat_z=1.02, arms="stand")     # Hände unten, Kamera nah am Gesicht
    L.build_figure("Maxi", (-17.0, 1.4), 180, "stand", col)


@scene("SH109", ((2.2, -9.6, 1.40), (0.8, -6.6, 1.40), 28.0))
def _(col):
    for o in bpy.data.objects:                                                              # offenes Türblatt weg, geschlossene Haustür davor
        if o.name.startswith("EG_Aussenwand_Sued_front_door_3_leaf"):
            o.hide_render = True
    L.box("Haustuer_zu", (0.62, -6.28, 1.10), (1.12, 0.07, 2.12), L.mat("MAT_Haustuer_Teal", (0.05, 0.30, 0.33, 1)), col)
    L.build_figure("Opa_Heinrich", (0.7, -7.3), 90, "point", col)                           # klingelt an der geschlossenen Haustür


@scene("SH165", ((0.0, -5.2, 1.30), (0.5, -2.2, 1.30), 30.0))
def _(col):
    r = L.build_figure("Tante_Frieda", (0.0, -3.8), 90, "stand", col)
    L.prop_suitcase("Koffer", (-0.6, -4.3, 0), 90, col)
    L.build_figure("Mama_Katrin", (0.5, -2.2), 270, "open", col)
    L.build_figure("Papa_Thomas", (1.2, -2.9), 250, "stand", col)


@scene("SH166", ((0.4, -0.6, 1.35), (0.0, -3.8, 1.25), 32.0))
def _(col):
    r = L.build_figure("Tante_Frieda", (0.0, -3.8), 90, "stand", col)
    L.prop_suitcase("Koffer", (-0.6, -4.3, 0), 90, col)
    L.build_figure("Mama_Katrin", (0.5, -2.2), 270, "stand", col)
    L.build_figure("Papa_Thomas", (1.2, -2.9), 250, "stand", col)


@scene("SH167", ((-0.5, -3.9, 1.40), (1.2, -2.9, 1.42), 50.0))
def _(col):
    L.build_figure("Tante_Frieda", (0.0, -3.8), 90, "stand", col)
    L.prop_suitcase("Koffer", (-0.6, -4.3, 0), 90, col)
    L.build_figure("Mama_Katrin", (0.5, -2.2), 270, "stand", col)
    L.build_figure("Papa_Thomas", (1.2, -2.9), 215, "hold_front", col)                       # Fokus auf Papa, schaut zu Frieda


@scene("SH173", ((0.2, -1.5, 1.30), (0.3, -4.5, 1.30), 32.0))
def _(col):
    L.build_figure("Tante_Frieda", (0.3, -4.5), 90, "stand", col, head_turn_deg=-10)         # verabschiedet sich von Maxi
    L.prop_suitcase("Koffer", (-0.5, -4.7, 0), 90, col)


# ------------------------------------------------------------------ Ablauf
def clear_scene_col():
    col = bpy.data.collections.get(SCENE_COL)
    if col:
        for o in list(col.objects):
            bpy.data.objects.remove(o, do_unlink=True)
        bpy.data.collections.remove(col)
    for o in bpy.data.objects:
        if o.name.startswith(("KU_Stuhl", "KZ_Hasi", "DET_Glas", "KZ_Kleiderschrank", "EG_Aussenwand_Sued_front_door_3_leaf")):
            o.hide_render = False
    for o in list(bpy.data.objects):
        if o.name.startswith("SZENE_CAM_"):
            bpy.data.objects.remove(o, do_unlink=True)


LICHT = bool(os.environ.get("MOCKUP_LICHT"))
_AUSSEN = {"SH001", "SH002", "SH003", "SH010", "SH030", "SH032", "SH109", "SH065", "SH070", "SH071", "SH072", "SH073", "SH074", "SH075"}
_FLUR = {"SH040", "SH041", "SH042", "SH110", "SH111", "SH112", "SH165", "SH166", "SH167", "SH170", "SH171", "SH173", "SH174", "SH175", "SH177", "SH178", "SH179", "SH184"}
_KUECHE = {"SH100", "SH101", "SH120", "SH122", "SH123", "SH124", "SH130", "SH140", "SH141", "SH143", "SH144", "SH145", "SH150", "SH151", "SH160"}


def light_for(sid):
    k = sid.split("_")[0]
    if k in _AUSSEN: return (222, 26, 0.0)
    if k == "SH020": return (215, 22, 0.5)
    if k in _FLUR: return (95, 32, 1.6)
    if k in _KUECHE: return (150, 28, 1.0)
    if k == "SH186": return (228, 26, 0.9)
    return (232, 27, 0.9)                                   # Kinderzimmer


def aim_light(az, el):
    from mathutils import Vector as Vec
    sun = bpy.data.objects.get("Sonne_Warm")
    a, e = math.radians(az), math.radians(el)
    to_sun = Vec((math.cos(e) * math.cos(a), math.cos(e) * math.sin(a), math.sin(e)))
    if sun:
        sun.rotation_euler = (-to_sun).to_track_quat("-Z", "Y").to_euler()
    w = bpy.context.scene.world
    for n in (w.node_tree.nodes if w and w.use_nodes else []):
        if n.bl_idname == "ShaderNodeTexSky":
            n.sun_elevation = math.radians(el); n.sun_rotation = math.radians(az - 90.0) % (2 * math.pi)


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    wanted = argv or list(SCENES)
    os.makedirs(BLEND_DIR, exist_ok=True)
    if LICHT:
        sc = bpy.context.scene
        if os.environ.get("MOCK_EEVEE"):                       # schnell: Eevee mit Sonne, Schatten und Raytracing
            sc.render.engine = "BLENDER_EEVEE"
            for k, v in (("use_raytracing", True), ("taa_render_samples", 24), ("use_shadows", True)):
                if hasattr(sc.eevee, k):
                    try: setattr(sc.eevee, k, v)
                    except Exception: pass
        else:
            sc.render.engine = "CYCLES"; sc.cycles.samples = int(os.environ.get("MOCK_SAMPLES", "48"))
        sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 1376, 768, 100
        sc.render.image_settings.file_format = "PNG"
        sc.render.use_persistent_data = True                  # Haus bleibt zwischen den Bildern im Speicher (viel schneller)
    else:
        L.configure_render(1600, 900)
    for c in bpy.data.collections:
        c.hide_render = False
    cam_col = L.get_collection("99_Kameras")
    for sid in wanted:
        spec = SCENES[sid]
        clear_scene_col()
        col = L.get_collection(SCENE_COL)
        spec["build"](col)
        if isinstance(spec["cam"], str):
            cam = next(o for o in bpy.data.objects if o.type == "CAMERA" and o.name.startswith(spec["cam"]))
        else:
            loc, tgt, lens = spec["cam"]
            cam = L.add_camera(f"SZENE_CAM_{sid}", loc, tgt, lens, cam_col)
        if LICHT:
            az, el, ev = light_for(sid); aim_light(az, el); bpy.context.scene.view_settings.exposure = ev - (1.7 if os.environ.get("MOCK_EEVEE") else 0.0)
            haze = bpy.data.objects.get("Dunst_Volumen")                      # Dunst nur draußen (Volumen ist teuer)
            if haze:
                haze.hide_render = sid.split("_")[0] not in (_AUSSEN | {"SH020"})
        L.render_camera(cam, os.path.join(OUT_DIR, f"{sid}_blender.png"))
        print("Szene fertig:", sid)
    clear_scene_col()


if __name__ == "__main__":
    main()
