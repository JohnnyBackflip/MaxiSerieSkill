#!/usr/bin/env python3
"""
Maxis Welt – Vollständiges 3D-Architektur- & Previs-Blockout-Modell (Blender 5.2 LTS)
Erzeugt:
  - Maxis_Haus_Komplett_Blockout.blend
  - 4 Cutaway-/Dollhouse-Übersichten (00..03)
  - 21 Innen- & Außen-Kameraperspektiven (Blockout_CAM_*.png)
Alle Wände besitzen echte 3D-Tür- und Fensteröffnungen; alle Möbel und Objekte
sind als farbcodierte, klar erkennbare Quader-Baugruppen (Box-Proxies) mit
Freestyle-Kantenlinien modelliert.
"""

import os
import math
import bpy
from mathutils import Vector, Euler

BASE_DIR = "/home/felix/projects/dump/Maxis_Welt_Korrekturmappe/03_Blender_3D_Haus_Blockout"
RENDER_DIR = os.path.join(BASE_DIR, "renders")
BLEND_PATH = os.path.join(BASE_DIR, "Maxis_Haus_Komplett_Blockout.blend")

os.makedirs(RENDER_DIR, exist_ok=True)


# ==============================================================================
# 1. SZENE ZURÜCKSETZEN & MATERIALIEN ANLEGEN
# ==============================================================================

def reset_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)


MATERIALS = {}


def make_mat(name, hex_color, roughness=0.75, metallic=0.0, alpha=1.0, emission_strength=0.14):
    if name in MATERIALS:
        return MATERIALS[name]
    mat = bpy.data.materials.new(name=name)
    if isinstance(hex_color, (tuple, list)):
        r, g, b = float(hex_color[0]), float(hex_color[1]), float(hex_color[2])
        if len(hex_color) >= 4:
            alpha = float(hex_color[3])
    else:
        r = int(hex_color[1:3], 16) / 255.0
        g = int(hex_color[3:5], 16) / 255.0
        b = int(hex_color[5:7], 16) / 255.0
    # sRGB -> Linear approximation
    rl = pow(r, 2.2)
    gl = pow(g, 2.2)
    bl = pow(b, 2.2)

    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (rl, gl, bl, 1.0)
        bsdf.inputs["Roughness"].default_value = roughness
        bsdf.inputs["Metallic"].default_value = metallic
        bsdf.inputs["Alpha"].default_value = alpha
        if "Emission Color" in bsdf.inputs:
            bsdf.inputs["Emission Color"].default_value = (rl, gl, bl, 1.0)
        if "Emission Strength" in bsdf.inputs:
            bsdf.inputs["Emission Strength"].default_value = emission_strength
    mat.diffuse_color = (rl, gl, bl, alpha)
    if alpha < 1.0:
        mat.surface_render_method = 'BLENDED'
    MATERIALS[name] = mat
    return mat


def init_palette():
    # Architektur & Natur
    make_mat("Grass_Lawn", "#8FBC6B", roughness=0.9)
    make_mat("Garden_Path", "#D9CCB4", roughness=0.85)
    make_mat("Fence_Wood", "#B88454", roughness=0.8)
    make_mat("Gate_Yellow", "#F2C94C", roughness=0.65)
    make_mat("Porch_Wood", "#C28B54", roughness=0.75)
    make_mat("Terrace_Wood", "#C9945E", roughness=0.75)
    make_mat("Sand_Yellow", "#ECD38C", roughness=0.9)
    make_mat("Tree_Trunk", "#6E4726", roughness=0.85)
    make_mat("Tree_Leaves", "#4E8C42", roughness=0.85)
    make_mat("Apple_Red", "#D63629", roughness=0.5)
    make_mat("Picnic_Green", "#5A9E56", roughness=0.8)
    make_mat("Picnic_RedWhite", "#E05A47", roughness=0.7)
    make_mat("Shed_Wood", "#A66E3E", roughness=0.8)
    make_mat("Shed_Roof", "#6E3B26", roughness=0.8)

    # Hauswände, Böden, Decken, Dach
    make_mat("Wall_Exterior", "#F2DFC4", roughness=0.8)
    make_mat("Wall_Interior", "#F7EFE2", roughness=0.8)
    make_mat("Wall_Bath", "#CFE8E6", roughness=0.6)
    make_mat("Floor_Oak", "#D6A874", roughness=0.65)
    make_mat("Floor_Kitchen", "#E8DEC8", roughness=0.6)
    make_mat("Floor_Bath", "#9AD0CE", roughness=0.45)
    make_mat("Floor_Attic", "#B88756", roughness=0.75)
    make_mat("Roof_Tiles", "#B84A32", roughness=0.75)
    make_mat("Beam_DarkWood", "#6B4222", roughness=0.75)
    make_mat("Frame_Window", "#FFFFFF", roughness=0.5)
    make_mat("Frame_Door", "#8C582B", roughness=0.65)
    make_mat("Door_Leaf", "#D9A875", roughness=0.65)
    make_mat("Door_Front", "#7A4219", roughness=0.6)

    # Möbel-Farbcodierung
    make_mat("Wood_Medium", "#A66A38", roughness=0.65)
    make_mat("Wood_Light", "#D49B63", roughness=0.65)
    make_mat("Wood_Dark", "#5E3819", roughness=0.65)
    make_mat("Sofa_Floral_Gold", "#F2A83B", roughness=0.75)
    make_mat("Sofa_Cushion_Coral", "#E06348", roughness=0.75)
    make_mat("Lamp_Warm", "#FFE27A", roughness=0.4, emission_strength=0.35)
    make_mat("Rug_Terra", "#C84B39", roughness=0.85)
    make_mat("Rug_Blue", "#345985", roughness=0.85)
    make_mat("Rug_Gold", "#EBC15A", roughness=0.85)
    make_mat("Rug_Sage", "#A2BA96", roughness=0.85)
    make_mat("Rug_Play", "#B4D6A4", roughness=0.85)
    make_mat("Rug_Bedroom", "#DECBB4", roughness=0.85)
    make_mat("TV_Black", "#26292E", roughness=0.35)
    make_mat("Kitchen_Sage", "#84A378", roughness=0.6)
    make_mat("Counter_Oak", "#C48A52", roughness=0.6)
    make_mat("Fridge_Cream", "#FAF7F0", roughness=0.4)
    make_mat("Metal_Silver", "#C4CBD0", roughness=0.3, metallic=0.5)
    make_mat("Sanitary_White", "#FFFFFF", roughness=0.3)
    make_mat("Mirror_Cyan", "#BCE6F2", roughness=0.2, metallic=0.3)
    make_mat("Water_Aqua", "#72C8D8", roughness=0.25)
    make_mat("Bed_Blue", "#4A7BB5", roughness=0.75)
    make_mat("Bed_Master_Teal", "#527D82", roughness=0.75)
    make_mat("Pillow_White", "#FAF8F5", roughness=0.75)
    make_mat("Hasi_Pink", "#F2B6C1", roughness=0.8)
    make_mat("Tent_Yellow", "#F7CE68", roughness=0.75)
    make_mat("Slide_Coral", "#E86F52", roughness=0.55)
    make_mat("Beanbag_Teal", "#48999E", roughness=0.8)
    make_mat("Beanbag_Mustard", "#E6B347", roughness=0.8)
    make_mat("Box_Cardboard", "#C99E67", roughness=0.8)
    make_mat("Box_Blue", "#5B89B8", roughness=0.7)
    make_mat("Box_Red", "#D45745", roughness=0.7)
    make_mat("Box_Green", "#6BA668", roughness=0.7)
    make_mat("Treasure_Chest", "#523015", roughness=0.65)
    make_mat("Brass_Gold", "#D9A738", roughness=0.35, metallic=0.6)
    make_mat("Hideout_Purple", "#8C659C", roughness=0.8)

    # Deckenleuchten-Materialien (ausgeschaltet / Tageslicht-Zustand)
    make_mat("Lamp_Shade_Cream", "#F5EBD6", roughness=0.6, emission_strength=0.10)
    make_mat("Lamp_Shade_Sage", "#8DAE82", roughness=0.5, emission_strength=0.10)
    make_mat("Lamp_Shade_Yellow", "#F7CE52", roughness=0.55, emission_strength=0.10)
    make_mat("Lamp_Shade_Sky", "#7EC4E8", roughness=0.55, emission_strength=0.10)
    make_mat("Lamp_Cord_Dark", "#3A322D", roughness=0.5, emission_strength=0.05)
    make_mat("Lamp_Glass_Off", "#EBF2F5", roughness=0.35, emission_strength=0.12)

    # Einfahrt & Garagen-Materialien
    make_mat("Driveway_Stone", "#B8B2A6", roughness=0.82)
    make_mat("Driveway_Border", "#8F897D", roughness=0.85)
    make_mat("Garage_Floor", "#C4C0B8", roughness=0.75)
    make_mat("Garage_Door_Panel", "#F2EDE2", roughness=0.6)
    make_mat("Pegboard_Wood", "#C99A64", roughness=0.75)
    make_mat("Vise_Blue", "#3B6E9C", roughness=0.45, metallic=0.3)
    make_mat("Tire_Rubber", "#2B2D2F", roughness=0.85)


# ==============================================================================
# 2. SAMMLUNGEN (COLLECTIONS) & GEOMETRIE-HELFER
# ==============================================================================

COLLECTIONS = {}


def get_collection(name, parent_name=None):
    if name in COLLECTIONS:
        return COLLECTIONS[name]
    col = bpy.data.collections.new(name)
    if parent_name and parent_name in COLLECTIONS:
        COLLECTIONS[parent_name].children.link(col)
    else:
        bpy.context.scene.collection.children.link(col)
    COLLECTIONS[name] = col
    return col


def link_to_col(obj, col):
    for c in list(obj.users_collection):
        c.objects.unlink(obj)
    col.objects.link(obj)


def add_box(name, x1, x2, y1, y2, z1, z2, mat_name, col, rot_z=0.0):
    """Erstellt einen achsenparallelen (oder um Z gedrehten) Quader von (x1,y1,z1) bis (x2,y2,z2) direkt per Mesh-API."""
    sx = abs(x2 - x1)
    sy = abs(y2 - y1)
    sz = abs(z2 - z1)
    if sx < 1e-4 or sy < 1e-4 or sz < 1e-4:
        return None
    cx = 0.5 * (x1 + x2)
    cy = 0.5 * (y1 + y2)
    cz = 0.5 * (z1 + z2)
    hx, hy, hz = 0.5 * sx, 0.5 * sy, 0.5 * sz

    verts = [
        (-hx, -hy, -hz), (hx, -hy, -hz), (hx, hy, -hz), (-hx, hy, -hz),
        (-hx, -hy, hz), (hx, -hy, hz), (hx, hy, hz), (-hx, hy, hz),
    ]
    faces = [
        (0, 3, 2, 1),
        (4, 5, 6, 7),
        (0, 1, 5, 4),
        (2, 3, 7, 6),
        (1, 2, 6, 5),
        (3, 0, 4, 7),
    ]
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    mesh.update()

    obj = bpy.data.objects.new(name, mesh)
    obj.location = (cx, cy, cz)
    if abs(rot_z) > 1e-5:
        obj.rotation_euler = (0.0, 0.0, math.radians(rot_z))

    mat = MATERIALS.get(mat_name) if isinstance(mat_name, str) else mat_name
    if mat:
        obj.data.materials.append(mat)
    link_to_col(obj, col)
    return obj


def add_pitched_prism(name, x1, x2, y1, y2, z_base, z_peak, mat_name, col, peak_axis='Y'):
    """Erstellt ein Dreiecksprisma (z.B. Giebelwand-Spitze, Zelt oder Rutsche)."""
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    if peak_axis == 'Y':
        ym = 0.5 * (y1 + y2)
        verts = [
            (x1, y1, z_base), (x2, y1, z_base),
            (x2, y2, z_base), (x1, y2, z_base),
            (x1, ym, z_peak), (x2, ym, z_peak),
        ]
        faces = [
            (0, 1, 2, 3),
            (0, 3, 4),
            (1, 5, 2),
            (0, 4, 5, 1),
            (3, 2, 5, 4),
        ]
    else:
        xm = 0.5 * (x1 + x2)
        verts = [
            (x1, y1, z_base), (x2, y1, z_base),
            (x2, y2, z_base), (x1, y2, z_base),
            (xm, y1, z_peak), (xm, y2, z_peak),
        ]
        faces = [
            (0, 1, 2, 3),
            (0, 1, 4),
            (3, 5, 2),
            (0, 4, 5, 3),
            (1, 2, 5, 4),
        ]
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    mat = MATERIALS.get(mat_name) if isinstance(mat_name, str) else mat_name
    if mat:
        obj.data.materials.append(mat)
    link_to_col(obj, col)
    return obj


def add_sloped_slab(name, x1, x2, y_low, z_low, y_high, z_high, thickness, mat_name, col):
    """Erstellt eine geneigte Platte (z.B. Dachfläche oder Rutschenbrett) entlang Y."""
    dy = y_high - y_low
    dz = z_high - z_low
    length = math.hypot(dy, dz)
    nx = 0.0
    ny = -dz / length * thickness
    nz = dy / length * thickness
    if nz < 0:
        ny, nz = -ny, -nz

    verts = [
        (x1, y_low, z_low),
        (x2, y_low, z_low),
        (x2, y_high, z_high),
        (x1, y_high, z_high),
        (x1, y_low + ny, z_low + nz),
        (x2, y_low + ny, z_low + nz),
        (x2, y_high + ny, z_high + nz),
        (x1, y_high + ny, z_high + nz),
    ]
    faces = [
        (0, 1, 2, 3),
        (4, 7, 6, 5),
        (0, 4, 5, 1),
        (1, 5, 6, 2),
        (2, 6, 7, 3),
        (3, 7, 4, 0),
    ]
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    mat = MATERIALS.get(mat_name) if isinstance(mat_name, str) else mat_name
    if mat:
        obj.data.materials.append(mat)
    link_to_col(obj, col)
    return obj


# ==============================================================================
# 3. WAND-GENERATOR MIT ECHTEN TÜR- & FENSTERÖFFNUNGEN
# ==============================================================================

def build_wall_x(name, x1, x2, y, thickness, z1, z2, mat_name, col, openings=None):
    """
    Baut eine Wand entlang X (von x1 bis x2 bei Y=y) mit echten Öffnungen.
    openings: Liste von Tupeln (s_start, s_end, oz1, oz2, kind)
              kind in {'window', 'door', 'arch', 'front_door', 'patio_door'}
    """
    openings = sorted(openings or [], key=lambda o: o[0])
    y_min = y - 0.5 * thickness
    y_max = y + 0.5 * thickness
    cursor = x1
    idx = 0

    for (ox1, ox2, oz1, oz2, kind) in openings:
        if ox1 > cursor + 0.005:
            add_box(f"{name}_seg_{idx}", cursor, ox1, y_min, y_max, z1, z2, mat_name, col)
            idx += 1
        # Brüstung unter Öffnung (z.B. Fensterbank)
        if oz1 > z1 + 0.005:
            add_box(f"{name}_sill_{idx}", ox1, ox2, y_min, y_max, z1, oz1, mat_name, col)
        # Sturz über Öffnung
        if oz2 < z2 - 0.005:
            add_box(f"{name}_lintel_{idx}", ox1, ox2, y_min, y_max, oz2, z2, mat_name, col)

        # Rahmen & Details für Fenster/Türen
        build_opening_details_x(f"{name}_{kind}_{idx}", ox1, ox2, y, thickness, oz1, oz2, kind, col)
        cursor = ox2
        idx += 1

    if cursor < x2 - 0.005:
        add_box(f"{name}_seg_{idx}", cursor, x2, y_min, y_max, z1, z2, mat_name, col)


def build_wall_y(name, x, y1, y2, thickness, z1, z2, mat_name, col, openings=None):
    """
    Baut eine Wand entlang Y (von y1 bis y2 bei X=x) mit echten Öffnungen.
    """
    openings = sorted(openings or [], key=lambda o: o[0])
    x_min = x - 0.5 * thickness
    x_max = x + 0.5 * thickness
    cursor = y1
    idx = 0

    for (oy1, oy2, oz1, oz2, kind) in openings:
        if oy1 > cursor + 0.005:
            add_box(f"{name}_seg_{idx}", x_min, x_max, cursor, oy1, z1, z2, mat_name, col)
            idx += 1
        if oz1 > z1 + 0.005:
            add_box(f"{name}_sill_{idx}", x_min, x_max, oy1, oy2, z1, oz1, mat_name, col)
        if oz2 < z2 - 0.005:
            add_box(f"{name}_lintel_{idx}", x_min, x_max, oy1, oy2, oz2, z2, mat_name, col)

        build_opening_details_y(f"{name}_{kind}_{idx}", x, oy1, oy2, thickness, oz1, oz2, kind, col)
        cursor = oy2
        idx += 1

    if cursor < y2 - 0.005:
        add_box(f"{name}_seg_{idx}", x_min, x_max, cursor, y2, z1, z2, mat_name, col)


def build_opening_details_x(name, x1, x2, y, thickness, z1, z2, kind, col):
    ft = 0.05
    ym1 = y - 0.5 * thickness - 0.015
    ym2 = y + 0.5 * thickness + 0.015

    if kind == "window":
        # Fensterrahmen + Fensterbank + Mittelpfosten (ohne verdeckendes Glas für freie Sicht!)
        add_box(f"{name}_sillboard", x1 - 0.04, x2 + 0.04, ym1 - 0.03, ym2 + 0.03, z1 - 0.02, z1 + 0.04, "Frame_Window", col)
        add_box(f"{name}_top", x1, x2, ym1, ym2, z2 - ft, z2, "Frame_Window", col)
        add_box(f"{name}_left", x1, x1 + ft, ym1, ym2, z1, z2, "Frame_Window", col)
        add_box(f"{name}_right", x2 - ft, x2, ym1, ym2, z1, z2, "Frame_Window", col)
        xm = 0.5 * (x1 + x2)
        add_box(f"{name}_mullion_v", xm - 0.02, xm + 0.02, y - 0.03, y + 0.03, z1, z2, "Frame_Window", col)
        zm = z1 + 0.55 * (z2 - z1)
        add_box(f"{name}_mullion_h", x1, x2, y - 0.025, y + 0.025, zm - 0.018, zm + 0.018, "Frame_Window", col)

    elif kind == "patio_door":
        add_box(f"{name}_top", x1, x2, ym1, ym2, z2 - ft, z2, "Frame_Window", col)
        add_box(f"{name}_left", x1, x1 + ft, ym1, ym2, z1, z2, "Frame_Window", col)
        add_box(f"{name}_right", x2 - ft, x2, ym1, ym2, z1, z2, "Frame_Window", col)
        xm = 0.5 * (x1 + x2)
        add_box(f"{name}_center", xm - 0.025, xm + 0.025, y - 0.03, y + 0.03, z1, z2, "Frame_Window", col)

    elif kind in ("door", "front_door"):
        fmat = "Door_Front" if kind == "front_door" else "Frame_Door"
        lmat = "Door_Front" if kind == "front_door" else "Door_Leaf"
        add_box(f"{name}_top", x1, x2, ym1, ym2, z2 - ft, z2, fmat, col)
        add_box(f"{name}_left", x1, x1 + ft, ym1, ym2, z1, z2, fmat, col)
        add_box(f"{name}_right", x2 - ft, x2, ym1, ym2, z1, z2, fmat, col)
        # Geöffnetes Türblatt (im 80°-Winkel offen, damit man frei hindurchschauen kann)
        dw = (x2 - x1) - 2 * ft
        add_box(f"{name}_leaf", x1 + ft, x1 + ft + 0.045, y, y + dw * 0.85, z1 + 0.02, z2 - ft, lmat, col)

    elif kind == "arch":
        add_box(f"{name}_top", x1, x2, ym1, ym2, z2 - 0.04, z2, "Frame_Door", col)
        add_box(f"{name}_left", x1, x1 + 0.04, ym1, ym2, z1, z2, "Frame_Door", col)
        add_box(f"{name}_right", x2 - 0.04, x2, ym1, ym2, z1, z2, "Frame_Door", col)


def build_opening_details_y(name, x, y1, y2, thickness, z1, z2, kind, col):
    ft = 0.05
    xm1 = x - 0.5 * thickness - 0.015
    xm2 = x + 0.5 * thickness + 0.015

    if kind == "window":
        add_box(f"{name}_sillboard", xm1 - 0.03, xm2 + 0.03, y1 - 0.04, y2 + 0.04, z1 - 0.02, z1 + 0.04, "Frame_Window", col)
        add_box(f"{name}_top", xm1, xm2, y1, y2, z2 - ft, z2, "Frame_Window", col)
        add_box(f"{name}_left", xm1, xm2, y1, y1 + ft, z1, z2, "Frame_Window", col)
        add_box(f"{name}_right", xm1, xm2, y2 - ft, y2, z1, z2, "Frame_Window", col)
        ym = 0.5 * (y1 + y2)
        add_box(f"{name}_mullion_v", x - 0.03, x + 0.03, ym - 0.02, ym + 0.02, z1, z2, "Frame_Window", col)
        zm = z1 + 0.55 * (z2 - z1)
        add_box(f"{name}_mullion_h", x - 0.025, x + 0.025, y1, y2, zm - 0.018, zm + 0.018, "Frame_Window", col)

    elif kind in ("door", "front_door"):
        fmat = "Frame_Door"
        lmat = "Door_Leaf"
        add_box(f"{name}_top", xm1, xm2, y1, y2, z2 - ft, z2, fmat, col)
        add_box(f"{name}_left", xm1, xm2, y1, y1 + ft, z1, z2, fmat, col)
        add_box(f"{name}_right", xm1, xm2, y2 - ft, y2, z1, z2, fmat, col)
        # Dezentes Türblatt flach an der Leibung/Wand, damit keine Innenkamera verdeckt wird
        dw = (y2 - y1) - 2 * ft
        direction = 1.0 if x >= 0 else -1.0
        if direction > 0:
            add_box(f"{name}_leaf", x + 0.02, x + 0.14, y1 + ft, y1 + ft + dw * 0.45, z1 + 0.02, z2 - ft, lmat, col)
        else:
            add_box(f"{name}_leaf", x - 0.14, x - 0.02, y1 + ft, y1 + ft + dw * 0.45, z1 + 0.02, z2 - ft, lmat, col)

    elif kind == "arch":
        add_box(f"{name}_top", xm1, xm2, y1, y2, z2 - 0.04, z2, "Frame_Door", col)
        add_box(f"{name}_left", xm1, xm2, y1, y1 + 0.04, z1, z2, "Frame_Door", col)
        add_box(f"{name}_right", xm1, xm2, y2 - 0.04, y2, z1, z2, "Frame_Door", col)


# ==============================================================================
# 4. BEREICH 00: GROSSER GARTEN & AUSSENANLAGEN (38.0 m x 36.0 m, Z = 0.0 m)
# ==============================================================================

def build_00_garten():
    col_garten = get_collection("00_Garten")

    # Großzügige Rasenfläche: 38.0 m breit (X = -19.0 .. +19.0) x 36.0 m tief (Y = -14.0 .. +22.0)
    # Haus steht bei X = -8.4 .. +8.4, Y = -6.3 .. +6.3 -> riesiger Hausgarten hinten bis Y = +22.0!
    add_box("Garten_Rasen", -19.2, 19.2, -14.2, 22.2, -0.12, 0.0, "Grass_Lawn", col_garten)

    # Gartenwege (langer Vorgartenweg zur Haustür + lange Seitenwege zu Annas & Bens Gartentor + Weg zum Schuppen)
    add_box("Weg_Haustuer", -0.3, 1.5, -14.0, -7.9, 0.0, 0.03, "Garden_Path", col_garten)
    add_box("Weg_Veranda_zu_Einfahrt", 2.5, 11.4, -8.3, -7.3, 0.0, 0.03, "Garden_Path", col_garten)
    add_box("Weg_Tor_Anna", -19.0, -8.4, 1.2, 2.4, 0.0, 0.03, "Garden_Path", col_garten)
    add_box("Weg_Tor_Ben", 8.4, 19.0, 3.6, 4.8, 0.0, 0.03, "Garden_Path", col_garten)
    add_box("Weg_Garage_Seitentuer", 9.6, 11.25, -0.5, 4.8, 0.0, 0.03, "Garden_Path", col_garten)
    add_box("Weg_Terrasse_Schuppen", 2.2, 11.2, 7.6, 8.8, 0.0, 0.025, "Garden_Path", col_garten)

    # Umlaufender Gartenzaun aus Quadern (X = ±19.0, Y = -14.0 .. +22.0)
    def fence_run_x(name, x_start, x_end, y_pos):
        add_box(f"{name}_rail_low", x_start, x_end, y_pos - 0.04, y_pos + 0.04, 0.25, 0.35, "Fence_Wood", col_garten)
        add_box(f"{name}_rail_high", x_start, x_end, y_pos - 0.04, y_pos + 0.04, 0.78, 0.88, "Fence_Wood", col_garten)
        steps = max(2, int(abs(x_end - x_start) / 1.2))
        for i in range(steps + 1):
            xp = x_start + (x_end - x_start) * (i / steps)
            add_box(f"{name}_post_{i}", xp - 0.07, xp + 0.07, y_pos - 0.07, y_pos + 0.07, 0.0, 1.05, "Fence_Wood", col_garten)

    def fence_run_y(name, x_pos, y_start, y_end):
        add_box(f"{name}_rail_low", x_pos - 0.04, x_pos + 0.04, y_start, y_end, 0.25, 0.35, "Fence_Wood", col_garten)
        add_box(f"{name}_rail_high", x_pos - 0.04, x_pos + 0.04, y_start, y_end, 0.78, 0.88, "Fence_Wood", col_garten)
        steps = max(2, int(abs(y_end - y_start) / 1.2))
        for i in range(steps + 1):
            yp = y_start + (y_end - y_start) * (i / steps)
            add_box(f"{name}_post_{i}", x_pos - 0.07, x_pos + 0.07, yp - 0.07, yp + 0.07, 0.0, 1.05, "Fence_Wood", col_garten)

    # Südzaun mit Gartentor vorne (X = -0.4 .. +1.6) UND breiter Garageneinfahrt (X = +11.2 .. +17.4)!
    fence_run_x("Zaun_Sued_L", -19.0, -0.4, -14.0)
    fence_run_x("Zaun_Sued_Mitte", 1.6, 11.2, -14.0)
    fence_run_x("Zaun_Sued_OstEcke", 17.4, 19.0, -14.0)
    add_box("Gartentor_Sued_Fluegel_L", -0.35, 0.55, -13.95, -13.85, 0.08, 0.98, "Gate_Yellow", col_garten, rot_z=25)
    add_box("Gartentor_Sued_Fluegel_R", 0.65, 1.55, -13.95, -13.85, 0.08, 0.98, "Gate_Yellow", col_garten, rot_z=-25)

    # Nordzaun durchgehend bei Y = +22.0
    fence_run_x("Zaun_Nord", -19.0, 19.0, 22.0)

    # Westzaun bei X = -19.0 mit Zauntor zu Annas Haus (Y = 1.0 .. 2.6)
    fence_run_y("Zaun_West_S", -19.0, -14.0, 1.0)
    fence_run_y("Zaun_West_N", -19.0, 2.6, 22.0)
    add_box("Zauntor_Anna_West", -19.05, -18.92, 1.05, 2.55, 0.08, 1.02, "Gate_Yellow", col_garten)

    # Ostzaun bei X = +19.0 mit Zauntor zu Bens Haus (Y = 3.4 .. 5.0, nördlich der Garage)
    fence_run_y("Zaun_Ost_S", 19.0, -14.0, 3.4)
    fence_run_y("Zaun_Ost_N", 19.0, 5.0, 22.0)
    add_box("Zauntor_Ben_Ost", 18.92, 19.05, 3.45, 4.95, 0.08, 1.02, "Gate_Yellow", col_garten)

    # Vorne (Süd): Holz-Veranda vor der Haustür (X = -1.4 .. +2.6, Y = -8.1 .. -6.3)
    add_box("Veranda_Deck", -1.4, 2.6, -8.1, -6.3, 0.0, 0.22, "Porch_Wood", col_garten)
    add_box("Veranda_Stufe", -0.3, 1.5, -8.45, -8.1, 0.0, 0.11, "Porch_Wood", col_garten)
    add_box("Veranda_Pfosten_L", -1.25, -1.10, -8.0, -7.85, 0.22, 2.45, "Beam_DarkWood", col_garten)
    add_box("Veranda_Pfosten_R", 2.30, 2.45, -8.0, -7.85, 0.22, 2.45, "Beam_DarkWood", col_garten)
    add_box("Veranda_Vordach", -1.5, 2.7, -8.15, -6.3, 2.45, 2.62, "Roof_Tiles", col_garten)
    add_box("Veranda_Gelaender_L", -1.30, -0.35, -8.02, -7.90, 0.22, 0.92, "Fence_Wood", col_garten)
    add_box("Veranda_Gelaender_R", 1.55, 2.50, -8.02, -7.90, 0.22, 0.92, "Fence_Wood", col_garten)

    # Roter Bollerwagen (Quader-Gruppe) vor der Veranda (X = 3.2 .. 4.7, Y = -8.4 .. -7.5)
    add_box("Bollerwagen_Wanne", 3.2, 4.7, -8.4, -7.5, 0.22, 0.64, "Apple_Red", col_garten)
    add_box("Bollerwagen_Rand", 3.16, 4.74, -8.44, -7.46, 0.56, 0.70, "Wood_Medium", col_garten)
    for wx in (3.38, 4.52):
        for wy in (-8.46, -7.44):
            add_box(f"Bollerwagen_Rad_{wx}_{wy}", wx - 0.15, wx + 0.15, wy - 0.05, wy + 0.05, 0.0, 0.28, "TV_Black", col_garten)
    add_box("Bollerwagen_Deichsel", 2.40, 3.20, -8.00, -7.90, 0.35, 0.43, "TV_Black", col_garten)

    # Vorgarten-Blumenbeete & Hecken-Quader links und rechts
    add_box("Vorgarten_Beet_West_Rahmen", -7.8, -3.2, -9.8, -8.2, 0.0, 0.24, "Wood_Medium", col_garten)
    add_box("Vorgarten_Beet_West_Gras", -7.6, -3.4, -9.6, -8.4, 0.24, 0.52, "Tree_Leaves", col_garten)
    add_box("Vorgarten_Beet_Ost_Rahmen", 4.8, 8.2, -9.8, -8.2, 0.0, 0.24, "Wood_Medium", col_garten)
    add_box("Vorgarten_Beet_Ost_Gras", 5.0, 8.0, -9.6, -8.4, 0.24, 0.52, "Tree_Leaves", col_garten)

    # Hinten (Nord): Große Holzterrasse am Haus (X = -7.8 .. +2.2, Y = +6.3 .. +10.2 -> 10.0m x 3.9m!)
    add_box("Holzterrasse_Deck", -7.8, 2.2, 6.3, 10.2, 0.0, 0.18, "Terrace_Wood", col_garten)
    add_box("Holzterrasse_Stufe", -4.2, -0.8, 10.2, 10.65, 0.0, 0.09, "Terrace_Wood", col_garten)
    # Großer Terrassentisch + 2 lange Gartenbänke auf der Holzterrasse
    add_box("Terrassentisch", -2.4, 0.6, 7.4, 8.8, 0.18, 0.86, "Wood_Medium", col_garten)
    add_box("Terrassenbank_N", -2.2, 0.4, 8.95, 9.45, 0.18, 0.58, "Wood_Light", col_garten)
    add_box("Terrassenbank_S", -2.2, 0.4, 6.75, 7.25, 0.18, 0.58, "Wood_Light", col_garten)

    # Großer Sandkasten (4.0m x 3.4m Quader mit Sitzrand) im Ost-Garten (X = 3.8 .. 7.8, Y = 9.2 .. 12.6)
    add_box("Sandkasten_Sand", 4.00, 7.60, 9.40, 12.40, 0.02, 0.22, "Sand_Yellow", col_garten)
    add_box("Sandkasten_Rand_S", 3.80, 7.80, 9.20, 9.42, 0.0, 0.30, "Wood_Medium", col_garten)
    add_box("Sandkasten_Rand_N", 3.80, 7.80, 12.38, 12.60, 0.0, 0.30, "Wood_Medium", col_garten)
    add_box("Sandkasten_Rand_W", 3.80, 4.02, 9.42, 12.38, 0.0, 0.30, "Wood_Medium", col_garten)
    add_box("Sandkasten_Rand_O", 7.58, 7.80, 9.42, 12.38, 0.0, 0.30, "Wood_Medium", col_garten)
    add_box("Sandkasten_Eimer", 5.10, 5.45, 10.60, 10.95, 0.22, 0.54, "Box_Red", col_garten)
    add_box("Sandkasten_Schaufel", 5.65, 6.15, 10.40, 10.60, 0.22, 0.32, "Box_Blue", col_garten)
    add_box("Sandkasten_Burg", 6.20, 6.85, 11.10, 11.75, 0.22, 0.62, "Sand_Yellow", col_garten)

    # Großer alter Apfelbaum (Stamm-Quader + Kronen-Quader + Holzschaukel) im Nord-West-Garten (X = -11.5, Y = 12.5)
    add_box("Apfelbaum_Stamm", -12.0, -11.0, 12.0, 13.0, 0.0, 3.8, "Tree_Trunk", col_garten)
    add_box("Apfelbaum_Schaukelast", -11.0, -8.2, 12.30, 12.70, 2.85, 3.20, "Tree_Trunk", col_garten)
    add_box("Apfelbaum_Krone_Haupt", -14.2, -9.0, 10.0, 15.0, 3.3, 6.2, "Tree_Leaves", col_garten)
    add_box("Apfelbaum_Krone_Top", -13.2, -10.0, 10.8, 14.2, 6.0, 7.5, "Tree_Leaves", col_garten)
    add_box("Apfelbaum_Krone_Ost", -9.5, -7.6, 11.0, 14.0, 3.2, 5.4, "Tree_Leaves", col_garten)
    # Rote Äpfel als Quader in der Krone
    for idx, (ax, ay, az) in enumerate([
        (-8.8, 11.2, 3.5), (-10.4, 10.1, 3.9), (-12.5, 10.1, 4.4),
        (-7.8, 12.5, 3.8), (-10.2, 14.8, 4.2), (-12.4, 14.8, 4.7),
        (-13.8, 12.4, 4.5), (-11.2, 11.5, 6.2)
    ]):
        add_box(f"Apfel_{idx}", ax - 0.16, ax + 0.16, ay - 0.16, ay + 0.16, az - 0.16, az + 0.16, "Apple_Red", col_garten)

    # Holzschaukel am Apfelbaum-Ast
    add_box("Holzschaukel_Seil_L", -9.85, -9.78, 12.46, 12.54, 0.68, 2.85, "Fence_Wood", col_garten)
    add_box("Holzschaukel_Seil_R", -9.05, -8.98, 12.46, 12.54, 0.68, 2.85, "Fence_Wood", col_garten)
    add_box("Holzschaukel_Sitzbrett", -9.98, -8.85, 12.25, 12.75, 0.60, 0.68, "Wood_Medium", col_garten)

    # Große Picknickmatte (flacher Quader) mitten auf der weiten Gartenwiese (X = -3.2 .. +1.2, Y = 13.0 .. 16.2)
    add_box("Picknickmatte_Basis", -3.2, 1.2, 13.0, 16.2, 0.01, 0.05, "Picnic_Green", col_garten)
    add_box("Picknickmatte_Decke", -2.8, 0.8, 13.3, 15.9, 0.05, 0.08, "Picnic_RedWhite", col_garten)
    add_box("Picknickkorb", -1.4, -0.5, 14.2, 14.9, 0.08, 0.48, "Wood_Medium", col_garten)

    # Hochbeet / Gemüsegarten im West-Garten (X = -16.5 .. -13.0, Y = 4.5 .. 8.0)
    add_box("Hochbeet_Rahmen", -16.5, -13.0, 4.5, 8.0, 0.0, 0.55, "Wood_Medium", col_garten)
    add_box("Hochbeet_Erde", -16.3, -13.2, 4.7, 7.8, 0.52, 0.60, "Tree_Trunk", col_garten)
    add_box("Hochbeet_Pflanzen_1", -16.0, -13.5, 5.0, 6.0, 0.60, 0.95, "Tree_Leaves", col_garten)
    add_box("Hochbeet_Pflanzen_2", -16.0, -13.5, 6.4, 7.4, 0.60, 0.95, "Picnic_Green", col_garten)

    # Opas Gartenschuppen + Werkbank im Nord-Ost-Garten (X = 10.5 .. 15.5, Y = 14.0 .. 19.0)
    add_box("Gartenschuppen_Boden", 10.5, 15.5, 14.0, 19.0, 0.0, 0.12, "Wood_Dark", col_garten)
    add_box("Gartenschuppen_Korpus", 10.7, 15.3, 14.4, 18.8, 0.12, 2.55, "Shed_Wood", col_garten)
    add_pitched_prism("Gartenschuppen_Dach", 10.4, 15.6, 14.2, 19.0, 2.55, 3.60, "Shed_Roof", col_garten, peak_axis='Y')
    add_box("Gartenschuppen_Tuer", 12.4, 13.5, 14.32, 14.44, 0.14, 2.15, "Door_Front", col_garten)
    # Opas Werkbank direkt vor dem Gartenschuppen
    add_box("Garten_Werkbank_Gestell", 10.7, 12.9, 13.2, 14.2, 0.0, 0.85, "Wood_Medium", col_garten)
    add_box("Garten_Werkbank_Platte", 10.6, 13.0, 13.1, 14.3, 0.85, 0.93, "Wood_Light", col_garten)
    add_box("Garten_Werkzeugkasten", 11.0, 11.7, 13.4, 13.9, 0.93, 1.22, "Apple_Red", col_garten)


# ==============================================================================
# 5. BEREICH 01: ERDGESCHOSS (16.8 m x 12.6 m, Z = 0.0 m bis Z = 2.80 m)
#    Vergrößerte Räume:
#    - EG_Wohnzimmer:  X = -8.4 .. -1.2, Y = -6.3 .. +0.3  (7.2 m x 6.6 m = 47.5 m²)
#    - EG_Kueche:      X = -8.4 .. -1.2, Y = +0.3 .. +6.3  (7.2 m x 6.0 m = 43.2 m²)
#    - EG_Flur:        X = -1.2 .. +2.0, Y = -6.3 .. +6.3  (3.2 m x 12.6 m)
#    - EG_Gaesteklo:   X = +2.0 .. +8.4, Y = -6.3 .. -2.5  (6.4 m x 3.8 m)
#    - EG_Spielzimmer: X = +2.0 .. +8.4, Y = -2.5 .. +6.3  (6.4 m x 8.8 m = 56.3 m²)
# ==============================================================================

def build_01_eg():
    col_eg = get_collection("01_EG")
    col_walls = get_collection("EG_Waende_und_Boeden", "01_EG")
    col_wz = get_collection("EG_Wohnzimmer", "01_EG")
    col_ku = get_collection("EG_Kueche", "01_EG")
    col_fl = get_collection("EG_Flur", "01_EG")
    col_gk = get_collection("EG_Gaesteklo", "01_EG")
    col_sz = get_collection("EG_Spielzimmer", "01_EG")

    z1, z2 = 0.0, 2.80
    tw_ext = 0.24
    tw_int = 0.16

    # --- BÖDEN ERDGESCHOSS ---
    add_box("EG_Boden_Wohnzimmer", -8.4, -1.2, -6.3, 0.3, -0.02, 0.02, "Floor_Oak", col_walls)
    add_box("EG_Boden_Kueche", -8.4, -1.2, 0.3, 6.3, -0.02, 0.02, "Floor_Kitchen", col_walls)
    add_box("EG_Boden_Flur", -1.2, 2.0, -6.3, 6.3, -0.02, 0.02, "Floor_Oak", col_walls)
    add_box("EG_Boden_Gaesteklo", 2.0, 8.4, -6.3, -2.5, -0.02, 0.02, "Floor_Bath", col_walls)
    add_box("EG_Boden_Spielzimmer", 2.0, 8.4, -2.5, 6.3, -0.02, 0.02, "Floor_Oak", col_walls)

    # --- AUSSENWÄNDE ERDGESCHOSS (mit echten Tür- und Fensteröffnungen!) ---
    # Südwand (Y = -6.3): großes WZ-Panoramafenster, Haustür im Flur, Gästeklo-Fenster
    build_wall_x(
        "EG_Aussenwand_Sued", -8.52, 8.52, -6.3, tw_ext, z1, z2, "Wall_Exterior", col_walls,
        openings=[
            (-6.8, -2.6, 0.72, 2.28, "window"),       # Wohnzimmer Südfenster (breit)
            (0.0, 1.2, 0.02, 2.22, "front_door"),     # Haustür im Flur
            (4.4, 5.8, 1.25, 2.15, "window"),         # Gästeklo Südfenster
        ]
    )
    # Nordwand (Y = +6.3): Küchenfenster, breite Terrassen-Doppeltür, Flurfenster, großes Spielzimmer-Gartenfenster
    build_wall_x(
        "EG_Aussenwand_Nord", -8.52, 8.52, 6.3, tw_ext, z1, z2, "Wall_Exterior", col_walls,
        openings=[
            (-7.2, -5.0, 1.02, 2.22, "window"),       # Küchenfenster über Spüle
            (-4.2, -1.6, 0.02, 2.28, "patio_door"),   # Breite Terrassen-Doppeltür zum Garten
            (-0.2, 0.9, 0.90, 2.22, "window"),        # Flur Nordfenster
            (3.4, 6.8, 0.72, 2.28, "window"),         # Großes Spielzimmer Nordfenster zum Garten
        ]
    )
    # Westwand (X = -8.4): Großes Wohnzimmer-Gartenfenster & Küchen-Westfenster
    build_wall_y(
        "EG_Aussenwand_West", -8.4, -6.3, 6.3, tw_ext, z1, z2, "Wall_Exterior", col_walls,
        openings=[
            (-4.8, -1.2, 0.72, 2.28, "window"),       # Wohnzimmer Westfenster
            (2.0, 4.2, 1.05, 2.22, "window"),         # Küchen Westfenster
        ]
    )
    # Ostwand (X = +8.4): Gästeklo-Fenster & 2 große Spielzimmer-Ostfenster
    build_wall_y(
        "EG_Aussenwand_Ost", 8.4, -6.3, 6.3, tw_ext, z1, z2, "Wall_Exterior", col_walls,
        openings=[
            (-4.9, -3.7, 1.25, 2.15, "window"),       # Gästeklo Ostfenster
            (-1.2, 1.6, 0.72, 2.28, "window"),        # Spielzimmer Ostfenster Süd
            (2.6, 5.2, 0.72, 2.28, "window"),         # Spielzimmer Ostfenster Nord
        ]
    )

    # --- INNENWÄNDE ERDGESCHOSS ---
    # Wand zwischen WZ/Küche (West) und Flur (Mitte) bei X = -1.2
    build_wall_y(
        "EG_Innenwand_WestFlur", -1.2, -6.3, 6.3, tw_int, z1, z2, "Wall_Interior", col_walls,
        openings=[
            (-3.8, -2.0, 0.02, 2.28, "arch"),         # Breiter offener Durchgang WZ <-> Flur
            (1.6, 3.2, 0.02, 2.25, "arch"),           # Breiter Durchgang Küche <-> Flur
        ]
    )
    # Wand zwischen Flur (Mitte) und Gästeklo/Spielzimmer (Ost) bei X = +2.0
    build_wall_y(
        "EG_Innenwand_OstFlur", 2.0, -6.3, 6.3, tw_int, z1, z2, "Wall_Interior", col_walls,
        openings=[
            (-4.8, -3.8, 0.02, 2.12, "door"),         # Tür zum Gästeklo
            (-0.6, 0.8, 0.02, 2.15, "door"),          # Breite Tür zum Spielzimmer
        ]
    )
    # Wand zwischen Wohnzimmer und Küche bei Y = +0.3 (X = -8.4 .. -1.2)
    build_wall_x(
        "EG_Innenwand_WZ_Kueche", -8.4, -1.2, 0.3, tw_int, z1, z2, "Wall_Interior", col_walls,
        openings=[
            (-4.8, -2.4, 0.02, 2.28, "arch"),         # Großzügiger Durchgang WZ <-> Küche
        ]
    )
    # Wand zwischen Gästeklo und Spielzimmer bei Y = -2.5 (X = +2.0 .. +8.4)
    build_wall_x(
        "EG_Innenwand_GK_SZ", 2.0, 8.4, -2.5, tw_int, z1, z2, "Wall_Interior", col_walls,
        openings=[]
    )

    # ==========================================================================
    # MÖBEL 1: EG_Wohnzimmer (GROSS: X = -8.4 .. -1.2, Y = -6.3 .. +0.3 -> 47.5 m²)
    # ==========================================================================
    # Großes geblümtes Familiensofa (Sitzquader + Rückenlehne + 2 Armlehnen + 3 Kissen) an der Westwand
    add_box("WZ_Sofa_Sitz", -8.00, -6.65, -4.60, -1.20, 0.02, 0.45, "Sofa_Floral_Gold", col_wz)
    add_box("WZ_Sofa_Rueckenlehne", -8.12, -7.70, -4.60, -1.20, 0.45, 0.96, "Sofa_Floral_Gold", col_wz)
    add_box("WZ_Sofa_Armlehne_S", -8.12, -6.65, -4.82, -4.55, 0.02, 0.68, "Sofa_Floral_Gold", col_wz)
    add_box("WZ_Sofa_Armlehne_N", -8.12, -6.65, -1.25, -0.98, 0.02, 0.68, "Sofa_Floral_Gold", col_wz)
    add_box("WZ_Sofa_Kissen_1", -7.68, -7.32, -4.30, -3.55, 0.45, 0.82, "Sofa_Cushion_Coral", col_wz)
    add_box("WZ_Sofa_Kissen_2", -7.68, -7.32, -3.20, -2.50, 0.45, 0.82, "Tent_Yellow", col_wz)
    add_box("WZ_Sofa_Kissen_3", -7.68, -7.32, -2.15, -1.45, 0.45, 0.82, "Sofa_Cushion_Coral", col_wz)

    # Gemütlicher Vorlese-Sessel (Quader) schräg am Südfenster
    add_box("WZ_Sessel_Sitz", -6.10, -5.05, -5.75, -4.75, 0.02, 0.44, "Sofa_Cushion_Coral", col_wz)
    add_box("WZ_Sessel_Lehne", -6.10, -5.05, -5.85, -5.52, 0.44, 0.92, "Sofa_Cushion_Coral", col_wz)
    add_box("WZ_Sessel_Arm_W", -6.18, -5.95, -5.80, -4.75, 0.02, 0.64, "Sofa_Cushion_Coral", col_wz)
    add_box("WZ_Sessel_Arm_O", -5.20, -4.97, -5.80, -4.75, 0.02, 0.64, "Sofa_Cushion_Coral", col_wz)

    # Stehlampe (Ständer + Schirm-Quader) in der Süd-West-Ecke (auf der freien anderen Seite der Couch, damit das Bücherregal frei bleibt)
    add_box("WZ_Stehlampe_Fuss", -7.82, -7.26, -5.52, -4.96, 0.02, 0.08, "Wood_Dark", col_wz)
    add_box("WZ_Stehlampe_Stab", -7.59, -7.49, -5.29, -5.19, 0.08, 1.55, "Wood_Dark", col_wz)
    add_box("WZ_Stehlampe_Schirm", -7.90, -7.18, -5.60, -4.88, 1.48, 1.92, "Lamp_Warm", col_wz)

    # Großer Geometrie-Teppich (flacher mehrfarbiger Quader) + Couchtisch in der Raummitte
    add_box("WZ_Teppich_Rot", -6.20, -3.00, -4.60, -1.20, 0.02, 0.045, "Rug_Terra", col_wz)
    add_box("WZ_Teppich_Blau", -5.75, -3.45, -4.15, -1.65, 0.045, 0.055, "Rug_Blue", col_wz)
    add_box("WZ_Teppich_Gold", -5.20, -4.00, -3.60, -2.20, 0.055, 0.065, "Rug_Gold", col_wz)
    add_box("WZ_Couchtisch_Platte", -5.15, -4.05, -3.50, -2.30, 0.38, 0.44, "Wood_Medium", col_wz)
    for lx in (-5.08, -4.12):
        for ly in (-3.42, -2.38):
            add_box(f"WZ_Couchtisch_Bein_{lx}_{ly}", lx - 0.04, lx + 0.04, ly - 0.04, ly + 0.04, 0.06, 0.38, "Wood_Dark", col_wz)

    # Großes Bücherregal an der Nordwand (X = -7.95 .. -5.15, Y = -0.22 .. +0.20)
    add_box("WZ_Buecherregal_Korpus", -7.95, -5.15, -0.22, 0.20, 0.02, 2.15, "Wood_Medium", col_wz)
    for sz in (0.52, 1.04, 1.56):
        add_box(f"WZ_Buecherregal_Boden_{sz}", -7.90, -5.20, -0.24, 0.18, sz, sz + 0.05, "Wood_Dark", col_wz)
    add_box("WZ_Buecher_Block_1", -7.75, -7.05, -0.20, 0.14, 1.09, 1.48, "Box_Red", col_wz)
    add_box("WZ_Buecher_Block_2", -6.85, -6.10, -0.20, 0.14, 1.09, 1.44, "Box_Blue", col_wz)
    add_box("WZ_Teddy_Block", -5.85, -5.35, -0.20, 0.14, 1.61, 1.98, "Sofa_Floral_Gold", col_wz)

    # TV-Lowboard + großer Fernseher an der Ostwand (X = -1.95 .. -1.30, Y = -5.60 .. -3.95)
    add_box("WZ_TV_Lowboard", -1.95, -1.30, -5.60, -3.95, 0.02, 0.56, "Wood_Dark", col_wz)
    add_box("WZ_Fernseher_Fuss", -1.72, -1.48, -4.95, -4.60, 0.56, 0.64, "TV_Black", col_wz)
    add_box("WZ_Fernseher_Screen", -1.66, -1.54, -5.40, -4.15, 0.64, 1.38, "TV_Black", col_wz)
    add_box("WZ_Webcam", -1.68, -1.52, -4.84, -4.70, 1.38, 1.45, "Metal_Silver", col_wz)

    # ==========================================================================
    # MÖBEL 2: EG_Kueche (GROSS: X = -8.4 .. -1.2, Y = +0.3 .. +6.3 -> 43.2 m²)
    # ==========================================================================
    # Große L-förmige Küchenzeile (salbeigrüne Quader) + Eichen-Arbeitsplatte
    add_box("KU_Zeile_West_Korpus", -8.25, -7.45, 1.55, 6.12, 0.02, 0.88, "Kitchen_Sage", col_ku)
    add_box("KU_Zeile_West_Platte", -8.26, -7.40, 1.52, 6.14, 0.88, 0.94, "Counter_Oak", col_ku)
    add_box("KU_Zeile_Nord_Korpus", -7.45, -4.55, 5.35, 6.12, 0.02, 0.88, "Kitchen_Sage", col_ku)
    add_box("KU_Zeile_Nord_Platte", -7.45, -4.52, 5.30, 6.14, 0.88, 0.94, "Counter_Oak", col_ku)
    # Herdplatte & großes Spülbecken
    add_box("KU_Kochfeld", -8.12, -7.52, 3.00, 4.00, 0.94, 0.97, "TV_Black", col_ku)
    add_box("KU_Spuelbecken", -6.65, -5.65, 5.45, 6.00, 0.94, 0.98, "Metal_Silver", col_ku)
    add_box("KU_Wasserhahn", -6.20, -6.08, 5.92, 6.08, 0.98, 1.26, "Metal_Silver", col_ku)

    # Oberschränke an der Westwand
    add_box("KU_Oberschrank_1", -8.26, -7.78, 1.65, 2.95, 1.50, 2.26, "Kitchen_Sage", col_ku)
    add_box("KU_Oberschrank_2", -8.26, -7.78, 4.25, 5.65, 1.50, 2.26, "Kitchen_Sage", col_ku)

    # Großer Familien-Kühlschrank (hoher Quader) am Südende der Westzeile + Vorratsschrank
    add_box("KU_Kuehlschrank", -8.26, -7.40, 0.55, 1.45, 0.02, 2.05, "Fridge_Cream", col_ku)
    add_box("KU_Kuehlschrank_Zeichnung1", -7.40, -7.36, 0.75, 1.02, 1.30, 1.58, "Lamp_Warm", col_ku)
    add_box("KU_Kuehlschrank_Zeichnung2", -7.40, -7.36, 1.08, 1.32, 1.05, 1.32, "Slide_Coral", col_ku)

    # Maxis Tritthocker (2-Stufen-Quader) vor der Spüle
    add_box("KU_Tritthocker_Unten", -6.45, -5.85, 4.72, 5.25, 0.02, 0.22, "Wood_Light", col_ku)
    add_box("KU_Tritthocker_Oben", -6.45, -5.85, 4.95, 5.25, 0.22, 0.44, "Wood_Medium", col_ku)

    # Großer Familien-Esstisch + 6 Stühle (Quader) + Apfelschale in der geräumigen Osthälfte der Küche
    add_box("KU_Esstisch_Platte", -4.65, -2.25, 2.15, 3.85, 0.74, 0.80, "Wood_Medium", col_ku)
    for tx in (-4.52, -2.38):
        for ty in (2.28, 3.72):
            add_box(f"KU_Esstisch_Bein_{tx}_{ty}", tx - 0.05, tx + 0.05, ty - 0.05, ty + 0.05, 0.02, 0.74, "Wood_Dark", col_ku)
    add_box("KU_Apfelschale", -3.65, -3.25, 2.82, 3.18, 0.80, 0.94, "Apple_Red", col_ku)

    # 6 Stühle um den großen Esstisch
    chair_specs = [
        ("KU_Stuhl_N1", -4.40, -3.90, 3.95, 4.42, 4.34, 4.42),
        ("KU_Stuhl_N2", -3.70, -3.20, 3.95, 4.42, 4.34, 4.42),
        ("KU_Stuhl_N3", -3.00, -2.50, 3.95, 4.42, 4.34, 4.42),
        ("KU_Stuhl_S1", -4.40, -3.90, 1.58, 2.05, 1.58, 1.66),
        ("KU_Stuhl_S2", -3.70, -3.20, 1.58, 2.05, 1.58, 1.66),
        ("KU_Stuhl_S3", -3.00, -2.50, 1.58, 2.05, 1.58, 1.66),
    ]
    for cname, cx1, cx2, cy1, cy2, by1, by2 in chair_specs:
        add_box(f"{cname}_Sitz", cx1, cx2, cy1, cy2, 0.02, 0.46, "Wood_Light", col_ku)
        add_box(f"{cname}_Lehne", cx1, cx2, by1, by2, 0.46, 0.94, "Wood_Medium", col_ku)

    # ==========================================================================
    # MÖBEL 3: EG_Flur (X = -1.2 .. +2.0, Y = -6.3 .. +6.3)
    # ==========================================================================
    # Schuhbank + Garderobe an der Westwand nahe Haustür
    add_box("FL_Schuhbank", -1.08, -0.55, -5.95, -4.45, 0.02, 0.46, "Wood_Medium", col_fl)
    add_box("FL_Garderobe_Paneel", -1.10, -1.00, -5.85, -4.55, 1.05, 1.92, "Wood_Light", col_fl)
    add_box("FL_Jacke_1", -1.00, -0.80, -5.65, -5.25, 1.15, 1.74, "Box_Red", col_fl)
    add_box("FL_Jacke_2", -1.00, -0.80, -5.05, -4.65, 1.15, 1.74, "Box_Blue", col_fl)

    # Holztreppe (Stufen-Quader) ins 1. OG (X = +0.85 .. +1.90, Y = +1.80 .. +5.40)
    num_steps = 14
    y_st_start, y_st_end = 1.80, 5.40
    dy_step = (y_st_end - y_st_start) / num_steps
    dz_step = 2.80 / num_steps
    for i in range(num_steps):
        ys1 = y_st_start + i * dy_step
        ys2 = ys1 + dy_step
        zs1 = i * dz_step
        zs2 = (i + 1) * dz_step
        add_box(f"FL_Treppe_Stufe_{i+1}", 0.88, 1.90, ys1, ys2, max(0.02, zs1 - 0.15), zs2, "Wood_Medium", col_fl)
    # Treppengeländer
    add_sloped_slab("FL_Treppe_Handlauf", 0.80, 0.88, 1.80, 0.85, 5.40, 3.65, 0.08, "Wood_Dark", col_fl)

    # ==========================================================================
    # MÖBEL 4: EG_Gaesteklo (X = +2.0 .. +8.4, Y = -6.3 .. -2.5)
    # ==========================================================================
    # WC-Schüssel + Spülkasten an der Ostwand
    add_box("GK_WC_Spuelkasten", 7.98, 8.25, -4.25, -3.55, 0.42, 0.96, "Sanitary_White", col_gk)
    add_box("GK_WC_Schuessel", 7.45, 8.00, -4.20, -3.60, 0.02, 0.44, "Sanitary_White", col_gk)
    add_box("GK_WC_Deckel", 7.48, 7.96, -4.18, -3.62, 0.44, 0.48, "Frame_Window", col_gk)

    # Handwaschbecken + Unterschrank an der Nordwand
    add_box("GK_Unterschrank", 4.60, 5.80, -3.15, -2.58, 0.02, 0.78, "Wood_Medium", col_gk)
    add_box("GK_Waschbecken", 4.55, 5.85, -3.18, -2.58, 0.78, 0.90, "Sanitary_White", col_gk)
    add_box("GK_Armatur", 5.15, 5.25, -2.75, -2.60, 0.90, 1.08, "Metal_Silver", col_gk)

    # Wandspiegel (flacher Quader) über dem Waschbecken
    add_box("GK_Wandspiegel_Rahmen", 4.68, 5.72, -2.64, -2.58, 1.05, 1.90, "Wood_Light", col_gk)
    add_box("GK_Wandspiegel_Glas", 4.74, 5.66, -2.66, -2.62, 1.10, 1.85, "Mirror_Cyan", col_gk)

    # Kleiner Kinder-Tritthocker vor dem Waschbecken
    add_box("GK_Kinder_Tritthocker", 4.92, 5.48, -3.62, -3.22, 0.02, 0.28, "Wood_Light", col_gk)

    # ==========================================================================
    # MÖBEL 5: EG_Spielzimmer (GROSS: X = +2.0 .. +8.4, Y = -2.5 .. +6.3 -> 56.3 m²)
    # ==========================================================================
    # Großer bunter Spielteppich (flacher Quader) in der Raummitte
    add_box("SZ_Spielteppich", 3.10, 7.20, -0.50, 4.10, 0.02, 0.05, "Rug_Play", col_sz)
    add_box("SZ_Spielteppich_Mitte", 3.75, 6.55, 0.15, 3.45, 0.05, 0.06, "Rug_Gold", col_sz)

    # Langes Spielzeug-Würfelregal (Quader-Regal mit 8 Spalten) an der Südwand (Y = -2.42 .. -1.88)
    add_box("SZ_Wuerfelregal_Rahmen", 2.55, 6.55, -2.42, -1.88, 0.02, 1.24, "Wood_Light", col_sz)
    cube_colors = ["Box_Red", "Box_Blue", "Box_Green", "Lamp_Warm", "Slide_Coral", "Beanbag_Teal"]
    for ci in range(8):
        cx = 2.68 + ci * 0.48
        add_box(f"SZ_Wuerfelbox_Unten_{ci}", cx, cx + 0.40, -2.38, -1.86, 0.08, 0.56, cube_colors[ci % len(cube_colors)], col_sz)
        add_box(f"SZ_Wuerfelbox_Oben_{ci}", cx, cx + 0.40, -2.38, -1.86, 0.68, 1.16, cube_colors[(ci + 2) % len(cube_colors)], col_sz)

    # Großer Kinder-Maltisch + 4 bunte Hocker (Quader) in der Raummitte
    add_box("SZ_Maltisch_Platte", 4.35, 5.95, 0.95, 2.35, 0.52, 0.58, "Frame_Window", col_sz)
    for mx in (4.45, 5.85):
        for my in (1.05, 2.25):
            add_box(f"SZ_Maltisch_Bein_{mx}_{my}", mx - 0.04, mx + 0.04, my - 0.04, my + 0.04, 0.06, 0.52, "Wood_Light", col_sz)
    add_box("SZ_Malpapier", 4.75, 5.55, 1.35, 1.95, 0.58, 0.60, "Lamp_Warm", col_sz)
    add_box("SZ_Hocker_1", 3.82, 4.24, 1.42, 1.84, 0.06, 0.35, "Box_Red", col_sz)
    add_box("SZ_Hocker_2", 6.06, 6.48, 1.42, 1.84, 0.06, 0.35, "Box_Blue", col_sz)
    add_box("SZ_Hocker_3", 4.94, 5.36, 2.48, 2.90, 0.06, 0.35, "Box_Green", col_sz)
    add_box("SZ_Hocker_4", 4.94, 5.36, 0.40, 0.82, 0.06, 0.35, "Beanbag_Mustard", col_sz)

    # Indoor-Rutsche / Kletterblock (Quader-Stufen) in der Nord-West-Ecke
    add_box("SZ_Kletterblock_Stufe1", 2.35, 3.45, 5.35, 5.85, 0.02, 0.34, "Wood_Light", col_sz)
    add_box("SZ_Kletterblock_Stufe2", 2.35, 3.45, 4.85, 5.35, 0.02, 0.66, "Wood_Medium", col_sz)
    add_box("SZ_Kletterblock_Podest", 2.35, 3.45, 4.20, 4.85, 0.02, 0.98, "Wood_Light", col_sz)
    add_sloped_slab("SZ_Indoor_Rutsche", 2.48, 3.32, 2.75, 0.04, 4.20, 0.98, 0.08, "Slide_Coral", col_sz)

    # Große Sitzsack- / Kuschelpolster-Ecke in der Nord-Ost-Ecke
    add_box("SZ_Kuschelmatte", 5.85, 8.15, 3.95, 6.05, 0.02, 0.15, "Rug_Bedroom", col_sz)
    add_box("SZ_Sitzsack_1", 6.15, 7.25, 4.85, 5.85, 0.15, 0.72, "Beanbag_Teal", col_sz)
    add_box("SZ_Sitzsack_2", 7.05, 8.05, 4.15, 5.05, 0.15, 0.66, "Beanbag_Mustard", col_sz)

    #Große Spielzeugkiste (Quader) an der Ostwand
    add_box("SZ_Spielzeugkiste_Korpus", 7.35, 8.18, -1.55, -0.35, 0.02, 0.54, "Wood_Medium", col_sz)
    add_box("SZ_Spielzeugkiste_Deckel", 7.32, 8.21, -1.58, -0.32, 0.54, 0.62, "Slide_Coral", col_sz)



# ==============================================================================
# 6. BEREICH 02: 1. OBERGESCHOSS (16.8 m x 12.6 m, Z = 2.80 m bis Z = 5.50 m)
#    Vergrößerte Räume:
#    - OG_Kinderzimmer: X = -8.4 .. -1.2, Y = -6.3 .. +6.3  (7.2 m x 12.6 m)
#    - OG_Flur:         X = -1.2 .. +2.0, Y = -6.3 .. +6.3  (3.2 m x 12.6 m)
#    - OG_Elternzimmer: X = +2.0 .. +8.4, Y = +0.3 .. +6.3  (6.4 m x 6.0 m)
#    - OG_Badezimmer:   X = +2.0 .. +8.4, Y = -6.3 .. +0.3  (6.4 m x 6.6 m = 42.2 m²)
#      -> MIT GROSSER, AUSGEHÖHLTER FREISTEHENDER BADEWANNE + ARMATUR + QUIETSCHEENTE!
# ==============================================================================

def build_02_og():
    col_og = get_collection("02_OG")
    col_walls = get_collection("OG_Waende_und_Boeden", "02_OG")
    col_fl = get_collection("OG_Flur", "02_OG")
    col_kz = get_collection("OG_Kinderzimmer", "02_OG")
    col_ez = get_collection("OG_Elternzimmer", "02_OG")
    col_bd = get_collection("OG_Badezimmer", "02_OG")

    z_floor_bot, z_floor_top = 2.72, 2.82
    z1, z2 = 2.80, 5.50
    tw_ext = 0.24
    tw_int = 0.16

    # --- GESCHOSSDECKE / BÖDEN 1. OG (mit echtem Treppenloch bei X = 0.85..1.95, Y = 1.80..5.40!) ---
    add_box("OG_Boden_Kinderzimmer", -8.4, -1.2, -6.3, 6.3, z_floor_bot, z_floor_top, "Floor_Oak", col_walls)
    add_box("OG_Boden_Elternzimmer", 2.0, 8.4, 0.3, 6.3, z_floor_bot, z_floor_top, "Floor_Oak", col_walls)
    add_box("OG_Boden_Badezimmer", 2.0, 8.4, -6.3, 0.3, z_floor_bot, z_floor_top, "Floor_Bath", col_walls)
    # Oberer Flur Boden um das Treppenloch herum
    add_box("OG_Boden_Flur_West", -1.2, 0.85, -6.3, 6.3, z_floor_bot, z_floor_top, "Floor_Oak", col_walls)
    add_box("OG_Boden_Flur_Sued", 0.85, 2.0, -6.3, 1.80, z_floor_bot, z_floor_top, "Floor_Oak", col_walls)
    add_box("OG_Boden_Flur_Nord", 0.85, 2.0, 5.40, 6.3, z_floor_bot, z_floor_top, "Floor_Oak", col_walls)

    # --- AUSSENWÄNDE 1. OBERGESCHOSS ---
    # Südwand (Y = -6.3): Kinderzimmer-Fenster, Flur-Fenster, Badezimmer-Fenster
    build_wall_x(
        "OG_Aussenwand_Sued", -8.52, 8.52, -6.3, tw_ext, z1, z2, "Wall_Exterior", col_walls,
        openings=[
            (-6.2, -3.4, 3.55, 5.05, "window"),       # Kinderzimmer Südfenster
            (0.0, 1.2, 3.65, 4.95, "window"),         # Oberer Flur Südfenster
            (4.4, 6.6, 3.80, 5.05, "window"),         # Badezimmer Südfenster
        ]
    )
    # Nordwand (Y = +6.3): Großes Kinderzimmer-Fenster zum Apfelbaum, großes Elternzimmer-Fenster
    build_wall_x(
        "OG_Aussenwand_Nord", -8.52, 8.52, 6.3, tw_ext, z1, z2, "Wall_Exterior", col_walls,
        openings=[
            (-6.6, -3.0, 3.55, 5.05, "window"),       # Kinderzimmer Nordfenster (Apfelbaum)
            (3.6, 6.8, 3.55, 5.05, "window"),         # Elternzimmer Nordfenster
        ]
    )
    # Westwand (X = -8.4): Großes Kinderzimmer-Westfenster zum Apfelbaum
    build_wall_y(
        "OG_Aussenwand_West", -8.4, -6.3, 6.3, tw_ext, z1, z2, "Wall_Exterior", col_walls,
        openings=[
            (0.4, 3.8, 3.55, 5.05, "window"),         # Kinderzimmer Westfenster
        ]
    )
    # Ostwand (X = +8.4): Badezimmer-Ostfenster & Elternzimmer-Ostfenster
    build_wall_y(
        "OG_Aussenwand_Ost", 8.4, -6.3, 6.3, tw_ext, z1, z2, "Wall_Exterior", col_walls,
        openings=[
            (-4.2, -2.2, 3.85, 5.00, "window"),       # Badezimmer Ostfenster über der Badewanne
            (1.8, 4.4, 3.55, 5.05, "window"),         # Elternzimmer Ostfenster
        ]
    )

    # --- INNENWÄNDE 1. OBERGESCHOSS ---
    # Wand zwischen Kinderzimmer und oberem Flur bei X = -1.2
    build_wall_y(
        "OG_Innenwand_KZ_Flur", -1.2, -6.3, 6.3, tw_int, z1, z2, "Wall_Interior", col_walls,
        openings=[
            (0.4, 1.6, 2.82, 4.92, "door"),           # Tür zum Kinderzimmer
        ]
    )
    # Wand zwischen oberem Flur und Bad/Elternzimmer bei X = +2.0
    build_wall_y(
        "OG_Innenwand_Flur_Ost", 2.0, -6.3, 6.3, tw_int, z1, z2, "Wall_Interior", col_walls,
        openings=[
            (-3.2, -2.0, 2.82, 4.92, "door"),         # Tür zum Familien-Badezimmer
            (0.9, 2.1, 2.82, 4.92, "door"),           # Tür zum Elternzimmer
        ]
    )
    # Wand zwischen Badezimmer und Elternzimmer bei Y = +0.3 (X = +2.0 .. +8.4)
    build_wall_x(
        "OG_Innenwand_Bad_Eltern", 2.0, 8.4, 0.3, tw_int, z1, z2, "Wall_Interior", col_walls,
        openings=[]
    )

    # ==========================================================================
    # MÖBEL 6: OG_Flur (X = -1.2 .. +2.0, Y = -6.3 .. +6.3)
    # ==========================================================================
    # Brüstungsgeländer am EG-Treppenloch
    add_box("OG_Flur_Gelaender_West", 0.80, 0.88, 1.80, 4.60, 2.82, 3.72, "Wood_Medium", col_fl)
    add_box("OG_Flur_Gelaender_Sued", 0.80, 1.92, 1.75, 1.83, 2.82, 3.72, "Wood_Medium", col_fl)

    # Treppe weiter hoch zum Dachboden (DG) (X = -0.85 .. +0.35, Y = -5.10 .. -1.60, ansteigend nach Norden!)
    num_steps_dg = 14
    y_dg_start, y_dg_end = -5.10, -1.60
    dy_dg = (y_dg_end - y_dg_start) / num_steps_dg
    dz_dg = 2.70 / num_steps_dg
    for i in range(num_steps_dg):
        ys1 = y_dg_start + i * dy_dg
        ys2 = ys1 + dy_dg
        zs1 = 2.80 + i * dz_dg
        zs2 = 2.80 + (i + 1) * dz_dg
        add_box(f"OG_Dachbodentreppe_Stufe_{i+1}", -0.85, 0.35, ys1, ys2, max(2.82, zs1 - 0.14), zs2, "Wood_Medium", col_fl)
    add_sloped_slab("OG_Dachbodentreppe_Handlauf", 0.30, 0.38, -5.10, 3.65, -1.60, 6.25, 0.08, "Wood_Dark", col_fl)

    # ==========================================================================
    # MÖBEL 7: OG_Kinderzimmer (X = -8.4 .. -1.2, Y = -6.3 .. +6.3)
    # ==========================================================================
    # Kinderbett (Quader + Kopfteil + Hasi-Block auf dem Kissen) an der Westwand
    add_box("KZ_Kinderbett_Rahmen", -8.20, -5.65, -4.40, -2.65, 2.82, 3.20, "Wood_Medium", col_kz)
    add_box("KZ_Kinderbett_Kopfteil", -8.20, -8.02, -4.40, -2.65, 3.20, 3.98, "Wood_Medium", col_kz)
    add_box("KZ_Kinderbett_Matratze", -8.00, -5.75, -4.30, -2.75, 3.20, 3.46, "Bed_Blue", col_kz)
    add_box("KZ_Kinderbett_Kissen", -7.92, -7.30, -3.95, -3.10, 3.46, 3.62, "Pillow_White", col_kz)
    # Hasi-Block auf dem Kissen (rosa Kuschelhase-Quader mit 2 Ohren-Quadern)
    add_box("KZ_Hasi_Koerper", -7.65, -7.28, -3.68, -3.38, 3.62, 3.86, "Hasi_Pink", col_kz)
    add_box("KZ_Hasi_Ohr_L", -7.60, -7.50, -3.64, -3.56, 3.86, 4.05, "Hasi_Pink", col_kz)
    add_box("KZ_Hasi_Ohr_R", -7.60, -7.50, -3.48, -3.40, 3.86, 4.05, "Hasi_Pink", col_kz)

    # Nachttisch (Quader) + kleine Nachttischlampe
    add_box("KZ_Nachttisch", -8.20, -7.50, -2.45, -1.75, 2.82, 3.40, "Wood_Light", col_kz)
    add_box("KZ_Nachtlampe", -7.98, -7.70, -2.22, -1.98, 3.40, 3.74, "Lamp_Warm", col_kz)

    # Kissenburg-Zelt in der Nord-West-Ecke (Quader/Prisma)
    add_box("KZ_Kissenburg_Matte", -8.15, -5.95, 3.85, 6.05, 2.82, 2.98, "Rug_Gold", col_kz)
    add_box("KZ_Kissenburg_Polster1", -8.00, -7.25, 4.10, 5.80, 2.98, 3.36, "Sofa_Cushion_Coral", col_kz)
    add_box("KZ_Kissenburg_Polster2", -7.20, -6.20, 5.15, 5.85, 2.98, 3.32, "Bed_Blue", col_kz)
    add_pitched_prism("KZ_Kissenburg_Zeltdach", -8.18, -6.00, 3.85, 6.05, 3.36, 4.65, "Tent_Yellow", col_kz, peak_axis='Y')

    # Großer Spielteppich + Holzeisenbahn-Strecke (flache Quader) in der Raummitte
    add_box("KZ_Spielteppich", -5.85, -2.45, -1.35, 2.85, 2.82, 2.85, "Rug_Sage", col_kz)
    # Holzeisenbahn-Acht als Quader-Schienen + kleiner Zug
    add_box("KZ_Schiene_West", -5.25, -5.00, -0.65, 2.15, 2.85, 2.89, "Wood_Light", col_kz)
    add_box("KZ_Schiene_Ost", -3.20, -2.95, -0.65, 2.15, 2.85, 2.89, "Wood_Light", col_kz)
    add_box("KZ_Schiene_Sued", -5.25, -2.95, -0.65, -0.40, 2.85, 2.89, "Wood_Light", col_kz)
    add_box("KZ_Schiene_Nord", -5.25, -2.95, 1.90, 2.15, 2.85, 2.89, "Wood_Light", col_kz)
    add_box("KZ_Schiene_Mitte", -5.25, -2.95, 0.62, 0.88, 2.85, 2.89, "Wood_Light", col_kz)
    add_box("KZ_Holzzug_Lok", -4.45, -4.00, 0.56, 0.94, 2.89, 3.08, "Apple_Red", col_kz)
    add_box("KZ_Holzzug_Waggon", -3.90, -3.48, 0.58, 0.92, 2.89, 3.04, "Box_Blue", col_kz)

    # Kleiderschrank (hoher Quader) an der Süd-Ost-Wand
    add_box("KZ_Kleiderschrank", -3.45, -1.45, -6.12, -5.25, 2.82, 4.92, "Wood_Medium", col_kz)

    # Bücherregale (Quader) an der Ostwand nördlich der Tür
    add_box("KZ_Buecherregal", -1.85, -1.30, 2.15, 5.15, 2.82, 4.45, "Wood_Light", col_kz)
    add_box("KZ_Buecherreihe_1", -1.78, -1.35, 2.35, 3.45, 3.40, 3.80, "Box_Red", col_kz)
    add_box("KZ_Buecherreihe_2", -1.78, -1.35, 3.75, 4.85, 3.88, 4.28, "Box_Green", col_kz)

    # ==========================================================================
    # MÖBEL 8: OG_Elternzimmer (X = +2.0 .. +8.4, Y = +0.3 .. +6.3)
    # ==========================================================================
    # Großer Teppich unter dem Doppelbett
    add_box("EZ_Teppich", 2.80, 6.85, 2.05, 5.55, 2.82, 2.85, "Rug_Bedroom", col_ez)

    # Großes Doppelbett (Matratzen-Quader + Kopfteil + 2 Kissen-Quader) an der Westwand
    add_box("EZ_Doppelbett_Rahmen", 2.15, 5.05, 2.55, 4.95, 2.82, 3.24, "Wood_Medium", col_ez)
    add_box("EZ_Doppelbett_Kopfteil", 2.15, 2.38, 2.55, 4.95, 3.24, 4.12, "Wood_Dark", col_ez)
    add_box("EZ_Doppelbett_Matratze", 2.38, 4.95, 2.65, 4.85, 3.24, 3.52, "Bed_Master_Teal", col_ez)
    add_box("EZ_Doppelbett_Kissen_1", 2.45, 3.00, 2.82, 3.65, 3.52, 3.68, "Pillow_White", col_ez)
    add_box("EZ_Doppelbett_Kissen_2", 2.45, 3.00, 3.85, 4.68, 3.52, 3.68, "Pillow_White", col_ez)

    # 2 Nachttische mit Lampen-Quadern
    add_box("EZ_Nachttisch_Nord", 2.15, 2.75, 5.08, 5.68, 2.82, 3.40, "Wood_Medium", col_ez)
    add_box("EZ_Lampe_Nord", 2.30, 2.60, 5.22, 5.54, 3.40, 3.76, "Lamp_Warm", col_ez)
    add_box("EZ_Nachttisch_Sued", 2.15, 2.75, 1.82, 2.42, 2.82, 3.40, "Wood_Medium", col_ez)
    add_box("EZ_Lampe_Sued", 2.30, 2.60, 1.96, 2.28, 3.40, 3.76, "Lamp_Warm", col_ez)

    # Großer Kleiderschrank (Quader) an der Südwand
    add_box("EZ_Kleiderschrank", 2.85, 5.85, 0.42, 1.15, 2.82, 4.92, "Wood_Medium", col_ez)

    # Kommode / Wäscheschrank (Quader) an der Ostwand
    add_box("EZ_Kommode", 7.45, 8.22, 0.85, 2.65, 2.82, 3.80, "Wood_Light", col_ez)

    # Gemütlicher Lesesessel (Quader) in der Nord-Ost-Ecke am Fenster
    add_box("EZ_Lesesessel_Sitz", 6.85, 8.00, 4.55, 5.65, 2.85, 3.30, "Sofa_Cushion_Coral", col_ez)
    add_box("EZ_Lesesessel_Lehne", 7.65, 8.05, 4.55, 5.65, 3.30, 3.84, "Sofa_Cushion_Coral", col_ez)
    add_box("EZ_Lesesessel_Arm_S", 6.85, 8.00, 4.42, 4.62, 2.85, 3.54, "Sofa_Cushion_Coral", col_ez)
    add_box("EZ_Lesesessel_Arm_N", 6.85, 8.00, 5.58, 5.78, 2.85, 3.54, "Sofa_Cushion_Coral", col_ez)

    # ==========================================================================
    # MÖBEL 9: OG_Badezimmer (GROSS: X = +2.0 .. +8.4, Y = -6.3 .. +0.3 -> 42.2 m²)
    #          MIT FREISTEHENDER, ECHT AUSGEHÖHLTER 3D-BADEWANNE!
    # ==========================================================================
    # 1. GROSSE, AUSGEHÖHLTE FREISTEHENDE BADEWANNE (X = 4.85 .. 7.35, Y = -3.95 .. -2.55 -> 2.50m x 1.40m!)
    #    Frei im Raum platziert (mit großem Abstand zur Südwand!), damit sie in ALLEN
    #    Kameraansichten (Cutaway Iso, CAM_BD_01 & CAM_BD_02) zu 100% unverdeckt sichtbar ist!
    bx1, bx2 = 4.85, 7.35
    by1, by2 = -3.95, -2.55
    wt = 0.16  # Wandstärke der Badewanne (16 cm)
    # Wannen-Sockel & Wannen-Bodenplatte
    add_box("BD_Badewanne_Sockel", bx1 + 0.08, bx2 - 0.08, by1 + 0.08, by2 - 0.08, 2.82, 2.92, "Wood_Medium", col_bd)
    add_box("BD_Badewanne_Boden", bx1, bx2, by1, by2, 2.92, 3.02, "Sanitary_White", col_bd)
    # 4 echte weiße Wannen-Seitenwände (Z = 3.02 .. 3.52), die eine echte vertiefte Wanne bilden!
    add_box("BD_Badewanne_Wand_Sued", bx1, bx2, by1, by1 + wt, 3.02, 3.52, "Sanitary_White", col_bd)
    add_box("BD_Badewanne_Wand_Nord", bx1, bx2, by2 - wt, by2, 3.02, 3.52, "Sanitary_White", col_bd)
    add_box("BD_Badewanne_Wand_West", bx1, bx1 + wt, by1 + wt, by2 - wt, 3.02, 3.52, "Sanitary_White", col_bd)
    add_box("BD_Badewanne_Wand_Ost", bx2 - wt, bx2, by1 + wt, by2 - wt, 3.02, 3.52, "Sanitary_White", col_bd)
    # Breiter oberer Wannenrand (Kragen) mit klarer Kante für Freestyle-Linien
    add_box("BD_Badewanne_Rand_Sued", bx1 - 0.04, bx2 + 0.04, by1 - 0.04, by1 + wt + 0.02, 3.46, 3.54, "Sanitary_White", col_bd)
    add_box("BD_Badewanne_Rand_Nord", bx1 - 0.04, bx2 + 0.04, by2 - wt - 0.02, by2 + 0.04, 3.46, 3.54, "Sanitary_White", col_bd)
    add_box("BD_Badewanne_Rand_West", bx1 - 0.04, bx1 + wt + 0.02, by1 + wt, by2 - wt, 3.46, 3.54, "Sanitary_White", col_bd)
    add_box("BD_Badewanne_Rand_Ost", bx2 - wt - 0.02, bx2 + 0.04, by1 + wt, by2 - wt, 3.46, 3.54, "Sanitary_White", col_bd)

    # Vertiefte türkisfarbene Wasseroberfläche (Z = 3.30 .. 3.36 -> 18 cm unter dem Wannenrand!)
    add_box("BD_Badewanne_Wasser", bx1 + wt, bx2 - wt, by1 + wt, by2 - wt, 3.02, 3.35, "Water_Aqua", col_bd)
    # Weiße Badeschaum-Inseln auf dem Wasser
    add_box("BD_Badeschaum_1", 5.25, 5.75, -3.55, -3.10, 3.35, 3.42, "Pillow_White", col_bd)
    add_box("BD_Badeschaum_2", 6.45, 6.95, -3.45, -2.95, 3.35, 3.43, "Pillow_White", col_bd)
    # Große gelbe Quietscheente (Körper + Kopf + oranger Schnabel) + rotes Spielzeugboot in der Badewanne
    add_box("BD_Quietscheente_Koerper", 5.85, 6.18, -3.28, -3.02, 3.35, 3.52, "Tent_Yellow", col_bd)
    add_box("BD_Quietscheente_Kopf", 5.82, 6.00, -3.22, -3.08, 3.52, 3.66, "Tent_Yellow", col_bd)
    add_box("BD_Quietscheente_Schnabel", 5.74, 5.83, -3.19, -3.11, 3.55, 3.61, "Slide_Coral", col_bd)
    add_box("BD_Spielzeugboot", 6.25, 6.55, -3.65, -3.42, 3.35, 3.49, "Apple_Red", col_bd)

    # Hohe silberne Stand-Wannenarmatur (Standrohr + Wasserhahn-Auslauf + Handbrause) am Ostende der Badewanne
    add_box("BD_Wannenarmatur_Standrohr", 7.42, 7.54, -3.32, -3.18, 2.82, 3.82, "Metal_Silver", col_bd)
    add_box("BD_Wannenarmatur_Auslauf", 7.12, 7.54, -3.30, -3.20, 3.74, 3.82, "Metal_Silver", col_bd)
    add_box("BD_Wannenarmatur_Griff", 7.40, 7.56, -3.08, -2.96, 3.58, 3.68, "Metal_Silver", col_bd)

    # Weiche Badematte + kleiner Badhocker vor der Badewanne
    add_box("BD_Badematte_Wanne", 5.20, 6.95, -2.42, -1.75, 2.82, 2.86, "Beanbag_Teal", col_bd)

    # 2. Große Walk-In Duschkabine (Quader) in der Nord-Ost-Ecke (X = 6.65 .. 8.25, Y = -1.25 .. +0.18)
    add_box("BD_Duschtasse", 6.65, 8.25, -1.25, 0.18, 2.82, 2.95, "Sanitary_White", col_bd)
    add_box("BD_Duschrahmen_W", 6.65, 6.73, -1.25, 0.18, 2.95, 4.90, "Mirror_Cyan", col_bd)
    add_box("BD_Duschrahmen_Oben", 6.65, 8.25, -1.25, -1.16, 4.82, 4.90, "Metal_Silver", col_bd)
    add_box("BD_Duschkopf", 7.75, 8.18, -0.65, -0.35, 4.68, 4.82, "Metal_Silver", col_bd)
    add_box("BD_Duscharmatur", 8.12, 8.25, -0.60, -0.40, 3.85, 4.05, "Metal_Silver", col_bd)

    # 3. Großer Doppel-Waschtisch + 2 Waschbecken + großer Spiegel an der Nordwand (X = 2.65 .. 5.45, Y = -0.55 .. +0.18)
    add_box("BD_Waschtisch_Schrank", 2.65, 5.45, -0.55, 0.18, 2.82, 3.65, "Wood_Medium", col_bd)
    add_box("BD_Waschtisch_Platte", 2.60, 5.50, -0.58, 0.20, 3.65, 3.71, "Counter_Oak", col_bd)
    add_box("BD_Waschbecken_1", 2.90, 3.85, -0.48, 0.10, 3.71, 3.84, "Sanitary_White", col_bd)
    add_box("BD_Armatur_1", 3.32, 3.44, -0.02, 0.14, 3.84, 4.04, "Metal_Silver", col_bd)
    add_box("BD_Waschbecken_2", 4.25, 5.20, -0.48, 0.10, 3.71, 3.84, "Sanitary_White", col_bd)
    add_box("BD_Armatur_2", 4.66, 4.78, -0.02, 0.14, 3.84, 4.04, "Metal_Silver", col_bd)
    add_box("BD_Spiegel_Rahmen", 2.80, 5.30, 0.10, 0.18, 3.92, 4.88, "Wood_Light", col_bd)
    add_box("BD_Spiegel_Glas", 2.88, 5.22, 0.08, 0.12, 3.98, 4.80, "Mirror_Cyan", col_bd)

    # Maxis Tritthocker (2-stufiger Quader) vor dem linken Waschbecken
    add_box("BD_Tritthocker_Unten", 3.05, 3.72, -1.12, -0.60, 2.82, 3.04, "Wood_Light", col_bd)
    add_box("BD_Tritthocker_Oben", 3.05, 3.72, -0.92, -0.60, 3.04, 3.24, "Wood_Medium", col_bd)

    # 4. Toilette (Quader) an der Westwand südlich der Badezimmertür
    add_box("BD_WC_Spuelkasten", 2.10, 2.38, -5.25, -4.55, 3.24, 3.80, "Sanitary_White", col_bd)
    add_box("BD_WC_Schuessel", 2.36, 2.92, -5.20, -4.60, 2.82, 3.26, "Sanitary_White", col_bd)
    add_box("BD_WC_Deckel", 2.38, 2.90, -5.18, -4.62, 3.26, 3.30, "Frame_Window", col_bd)


# ==============================================================================
# 7. BEREICH 03: DACHGESCHOSS / DACHBODEN (16.8 m x 12.6 m, Z = 5.50 m bis 8.60 m)
# ==============================================================================

def build_03_dg():
    col_dg = get_collection("03_DG")
    col_struct = get_collection("DG_Struktur_und_Balken", "03_DG")
    col_roof_skin = get_collection("DG_Dachhaut", "03_DG")
    col_db = get_collection("DG_Dachboden", "03_DG")

    z_floor_bot, z_floor_top = 5.42, 5.52
    z_eaves = 6.25
    z_ridge = 8.60

    # --- DACHBODEN-PLATTE (mit Treppenöffnung bei X = -0.85..+0.35, Y = -5.10..-1.60) ---
    add_box("DG_Boden_West", -8.4, -0.85, -6.3, 6.3, z_floor_bot, z_floor_top, "Floor_Attic", col_struct)
    add_box("DG_Boden_Ost", 0.35, 8.4, -6.3, 6.3, z_floor_bot, z_floor_top, "Floor_Attic", col_struct)
    add_box("DG_Boden_Sued", -0.85, 0.35, -6.3, -5.10, z_floor_bot, z_floor_top, "Floor_Attic", col_struct)
    add_box("DG_Boden_Nord", -0.85, 0.35, -1.60, 6.3, z_floor_bot, z_floor_top, "Floor_Attic", col_struct)

    # Treppengeländer im Dachboden
    add_box("DG_Gelaender_West", -0.92, -0.84, -5.10, -1.60, 5.52, 6.40, "Wood_Medium", col_struct)
    add_box("DG_Gelaender_Ost", 0.34, 0.42, -5.10, -1.60, 5.52, 6.40, "Wood_Medium", col_struct)
    add_box("DG_Gelaender_Sued", -0.92, 0.42, -5.16, -5.08, 5.52, 6.40, "Wood_Medium", col_struct)

    # Kniestock-Wände (Süd & Nord, Z = 5.50 .. 6.25)
    add_box("DG_Kniestock_Sued", -8.52, 8.52, -6.42, -6.18, 5.50, z_eaves, "Wall_Exterior", col_struct)
    add_box("DG_Kniestock_Nord", -8.52, 8.52, 6.18, 6.42, 5.50, z_eaves, "Wall_Exterior", col_struct)

    # Giebelwände West (X = -8.4) und Ost (X = +8.4) passgenau unter der Dachschräge mit Giebelfenstern!
    def build_exact_gable_wall(prefix, x_pos):
        x1 = x_pos - 0.12
        x2 = x_pos + 0.12
        # Untere Zone bis Kniestockhöhe (Z = 5.50 .. 6.25) durchgehend von Y = -6.3 bis +6.3
        add_box(f"{prefix}_Basis", x1, x2, -6.3, 6.3, 5.50, z_eaves, "Wall_Exterior", col_struct)
        # Fensteröffnung: Y = -1.10 .. +1.10, Z = 6.25 .. 7.55
        wy1, wy2 = -1.10, 1.10
        wz1, wz2 = z_eaves, 7.55
        # Dachhöhe bei Y = ±1.10:
        z_at_win = z_eaves + (z_ridge - z_eaves) * (1.0 - abs(wy2) / 6.3)

        # Südliches Schräg-Trapez (Y = -6.3 .. -1.10)
        m_s = bpy.data.meshes.new(f"{prefix}_Schraege_Sued")
        o_s = bpy.data.objects.new(f"{prefix}_Schraege_Sued", m_s)
        v_s = [
            (x1, -6.3, z_eaves), (x2, -6.3, z_eaves),
            (x2, wy1, z_eaves), (x1, wy1, z_eaves),
            (x1, wy1, z_at_win), (x2, wy1, z_at_win),
        ]
        f_s = [(0, 1, 2, 3), (0, 3, 4), (1, 5, 2), (0, 4, 5, 1), (3, 2, 5, 4)]
        m_s.from_pydata(v_s, [], f_s)
        m_s.update()
        o_s.data.materials.append(MATERIALS["Wall_Exterior"])
        link_to_col(o_s, col_struct)

        # Nördliches Schräg-Trapez (Y = +1.10 .. +6.3)
        m_n = bpy.data.meshes.new(f"{prefix}_Schraege_Nord")
        o_n = bpy.data.objects.new(f"{prefix}_Schraege_Nord", m_n)
        v_n = [
            (x1, wy2, z_eaves), (x2, wy2, z_eaves),
            (x2, 6.3, z_eaves), (x1, 6.3, z_eaves),
            (x1, wy2, z_at_win), (x2, wy2, z_at_win),
        ]
        f_n = [(0, 1, 2, 3), (0, 3, 4), (1, 5, 2), (0, 4, 5, 1), (3, 2, 5, 4)]
        m_n.from_pydata(v_n, [], f_n)
        m_n.update()
        o_n.data.materials.append(MATERIALS["Wall_Exterior"])
        link_to_col(o_n, col_struct)

        # Sturz + Giebelspitze über dem Fenster
        add_box(f"{prefix}_Sturz", x1, x2, wy1, wy2, wz2, z_at_win, "Wall_Exterior", col_struct)
        add_pitched_prism(f"{prefix}_Spitze", x1, x2, wy1, wy2, z_at_win, z_ridge, "Wall_Exterior", col_struct, peak_axis='Y')

        # Fensterrahmen für das Giebelfenster
        build_opening_details_y(f"{prefix}_Giebelfenster", x_pos, wy1, wy2, 0.24, wz1, wz2, "window", col_struct)

    build_exact_gable_wall("DG_Giebel_West", -8.4)
    build_exact_gable_wall("DG_Giebel_Ost", 8.4)

    # --- SICHTBARE DACHBALKEN (Quader) ---
    add_box("DG_Firstbalken", -8.35, 8.35, -0.12, 0.12, 8.38, 8.56, "Beam_DarkWood", col_struct)
    add_box("DG_Mittelpfette_Sued", -8.35, 8.35, -3.18, -3.00, 7.30, 7.48, "Beam_DarkWood", col_struct)
    add_box("DG_Mittelpfette_Nord", -8.35, 8.35, 3.00, 3.18, 7.30, 7.48, "Beam_DarkWood", col_struct)
    # Dachsparren & hohe Kehlbalken (Z = 7.85)
    for bx in (-6.0, -3.0, 0.0, 3.0, 6.0):
        add_sloped_slab(f"DG_Sparren_Sued_{bx}", bx - 0.08, bx + 0.08, -6.3, z_eaves, 0.0, 8.52, 0.15, "Beam_DarkWood", col_struct)
        add_sloped_slab(f"DG_Sparren_Nord_{bx}", bx - 0.08, bx + 0.08, 6.3, z_eaves, 0.0, 8.52, 0.15, "Beam_DarkWood", col_struct)
        add_box(f"DG_Kehlbalken_{bx}", bx - 0.07, bx + 0.07, -1.85, 1.85, 7.82, 7.96, "Beam_DarkWood", col_struct)

    # --- DACHHAUT (Satteldach-Platten mit heller Holz-Innenverkleidung in Sub-Collection für sauberes Cutaway) ---
    add_sloped_slab("DG_Dachschraege_Innen_Sued", -8.50, 8.50, -6.35, 6.20, 0.0, z_ridge + 0.02, 0.06, "Wood_Light", col_roof_skin)
    add_sloped_slab("DG_Dachschraege_Innen_Nord", -8.50, 8.50, 6.35, 6.20, 0.0, z_ridge + 0.02, 0.06, "Wood_Light", col_roof_skin)
    add_sloped_slab("DG_Dachflaeche_Sued", -8.80, 8.80, -6.65, 6.18, 0.0, z_ridge + 0.10, 0.16, "Roof_Tiles", col_roof_skin)
    add_sloped_slab("DG_Dachflaeche_Nord", -8.80, 8.80, 6.65, 6.18, 0.0, z_ridge + 0.10, 0.16, "Roof_Tiles", col_roof_skin)
    add_box("DG_Firstkappe", -8.85, 8.85, -0.20, 0.20, z_ridge + 0.08, z_ridge + 0.32, "Roof_Tiles", col_roof_skin)

    # ==========================================================================
    # MÖBEL 10: DG_Dachboden (X = -8.4 .. +8.4, Y = -6.3 .. +6.3)
    # ==========================================================================
    # 1. Alte Schatztruhe (Quader) nahe der Mitte-West
    add_box("DB_Schatztruhe_Korpus", -3.25, -1.85, -0.55, 0.35, 5.52, 6.08, "Treasure_Chest", col_db)
    add_box("DB_Schatztruhe_Deckel", -3.28, -1.82, -0.58, 0.38, 6.08, 6.28, "Wood_Medium", col_db)
    add_box("DB_Schatztruhe_Schloss", -2.65, -2.45, -0.62, -0.55, 5.92, 6.14, "Brass_Gold", col_db)

    # 2. Altes Sofa / Matratzen-Geheimversteck der Kinder (Quader) im Nord-Westen
    add_box("DB_Geheimversteck_Matratze", -6.65, -3.65, 1.15, 4.35, 5.52, 5.70, "Rug_Bedroom", col_db)
    add_box("DB_Geheimversteck_Sofa_Sitz", -6.50, -5.15, 1.45, 4.05, 5.70, 6.10, "Hideout_Purple", col_db)
    add_box("DB_Geheimversteck_Sofa_Lehne", -6.65, -6.20, 1.45, 4.05, 6.10, 6.62, "Hideout_Purple", col_db)
    add_box("DB_Geheimversteck_Kissen1", -6.15, -5.70, 1.75, 2.55, 6.10, 6.42, "Tent_Yellow", col_db)
    add_box("DB_Geheimversteck_Kissen2", -6.15, -5.70, 2.95, 3.75, 6.10, 6.42, "Sofa_Cushion_Coral", col_db)
    add_box("DB_Geheimversteck_Kistentisch", -4.75, -3.95, 2.25, 3.15, 5.70, 6.08, "Wood_Light", col_db)
    add_box("DB_Geheimversteck_Laterne", -4.48, -4.22, 2.58, 2.82, 6.08, 6.38, "Lamp_Warm", col_db)

    # 3. Gestapelte Erinnerungskisten / Kartons (verschieden große Quader)
    boxes_data = [
        ("DB_Karton_1", -1.25, -0.35, 3.85, 4.75, 5.52, 6.08, "Box_Cardboard"),
        ("DB_Karton_2", -1.10, -0.50, 4.00, 4.60, 6.08, 6.55, "Box_Blue"),
        ("DB_Karton_3", -0.15, 0.85, 3.80, 4.80, 5.52, 6.15, "Box_Cardboard"),
        ("DB_Karton_4", 0.00, 0.70, 3.95, 4.65, 6.15, 6.60, "Box_Red"),
        ("DB_Karton_5", 1.05, 2.05, 3.95, 4.85, 5.52, 6.05, "Box_Green"),
        ("DB_Karton_6", -6.20, -5.20, -4.80, -3.85, 5.52, 6.10, "Box_Cardboard"),
        ("DB_Karton_7", -5.05, -4.10, -4.75, -3.90, 5.52, 6.00, "Box_Cardboard"),
        ("DB_Karton_8", -6.05, -5.35, -4.65, -3.95, 6.10, 6.55, "Box_Blue"),
    ]
    for bname, bx1, bx2, by1, by2, bz1, bz2, bmat in boxes_data:
        add_box(bname, bx1, bx2, by1, by2, bz1, bz2, bmat, col_db)

    # 4. Alter Standspiegel / Kleiderständer (Quader)
    add_box("DB_Standspiegel_Fuss", 2.45, 3.35, 2.25, 2.75, 5.52, 5.62, "Wood_Dark", col_db)
    add_box("DB_Standspiegel_Rahmen", 2.52, 3.28, 2.42, 2.56, 5.62, 7.15, "Wood_Medium", col_db)
    add_box("DB_Standspiegel_Glas", 2.60, 3.20, 2.38, 2.44, 5.72, 7.05, "Mirror_Cyan", col_db)
    add_box("DB_Kleiderstaender_Fuss", 3.65, 4.25, 2.20, 2.80, 5.52, 5.60, "Wood_Dark", col_db)
    add_box("DB_Kleiderstaender_Stange", 3.90, 4.00, 2.45, 2.55, 5.60, 7.10, "Wood_Dark", col_db)
    add_box("DB_Kleiderstaender_Mantel", 3.74, 4.16, 2.34, 2.66, 6.12, 6.92, "Sofa_Floral_Gold", col_db)

    # 5. Opas altes Fernrohr / Werkbank-Tisch (Quader) am Ost-Giebelfenster
    add_box("DB_Werkbank_Gestell", 5.85, 7.55, -2.65, -0.85, 5.52, 6.32, "Wood_Medium", col_db)
    add_box("DB_Werkbank_Platte", 5.78, 7.62, -2.72, -0.78, 6.32, 6.40, "Wood_Light", col_db)
    add_box("DB_Werkbank_Kiste", 6.10, 6.85, -2.35, -1.70, 6.40, 6.72, "Box_Red", col_db)
    # Opas Fernrohr auf Stativ vor dem Ost-Giebelfenster
    add_box("DB_Fernrohr_Stativ", 6.35, 7.00, 0.05, 0.70, 5.52, 6.52, "Wood_Dark", col_db)
    add_box("DB_Fernrohr_Tubus", 6.20, 7.45, 0.28, 0.48, 6.52, 6.70, "Brass_Gold", col_db)


# ==============================================================================
# ==============================================================================
# 7B. FLACHE RUNDE DECKENLEUCHTEN IN ALLEN ZIMMERN (1 PRO ZIMMER, 2 BEI LANGEN RÄUMEN)
# ==============================================================================

def add_round_ceiling_lamp(name, cx, cy, z_ceil, radius=0.24, ring_mat="Wood_Medium", col=None):
    """
    Erzeugt eine dezente, flache runde Deckenleuchte (16-Eck-Zylinderring + Milchglas-Scheibe)
    direkt unter der Decke im ausgeschalteten Tageslicht-Zustand (keine große Hängelampe).
    """
    def make_cylinder(obj_name, r, z1, z2, mat_name):
        verts = []
        faces = []
        n = 16
        for i in range(n):
            ang = 2.0 * math.pi * i / n
            verts.append((cx + r * math.cos(ang), cy + r * math.sin(ang), z1))
        for i in range(n):
            ang = 2.0 * math.pi * i / n
            verts.append((cx + r * math.cos(ang), cy + r * math.sin(ang), z2))
        # Deckel unten & oben
        faces.append(tuple(range(n - 1, -1, -1)))
        faces.append(tuple(range(n, 2 * n)))
        # Mantelflächen
        for i in range(n):
            nxt = (i + 1) % n
            faces.append((i, nxt, n + nxt, n + i))
        mesh = bpy.data.meshes.new(obj_name)
        obj = bpy.data.objects.new(obj_name, mesh)
        mesh.from_pydata(verts, [], faces)
        mesh.update()
        mat = MATERIALS.get(mat_name)
        if mat:
            obj.data.materials.append(mat)
        link_to_col(obj, col)
        return obj

    make_cylinder(f"{name}_Ring", radius, z_ceil - 0.05, z_ceil, ring_mat)
    make_cylinder(f"{name}_Glas", radius * 0.82, z_ceil - 0.09, z_ceil - 0.04, "Lamp_Glass_Off")


def build_all_ceiling_lamps():
    """
    Baut pro normalem Zimmer genau EINE dezente flache runde Deckenleuchte
    (und in den langen Räumen Flur & Dachboden jeweils ZWEI flache runde Deckenleuchten)
    im ausgeschalteten Tageslicht-Zustand. Keine großen Hängelampen.
    """
    col_eg_lamps = get_collection("EG_Deckenleuchten", "01_EG")
    col_og_lamps = get_collection("OG_Deckenleuchten", "02_OG")
    col_dg_lamps = get_collection("DG_Deckenleuchten", "03_DG")

    z_eg_ceil = 2.72  # Unterkante der EG-Decke
    z_og_ceil = 5.42  # Unterkante der OG-Decke

    # 1. EG Wohnzimmer: 1 flache runde Deckenleuchte mittig über dem Wohnbereich
    add_round_ceiling_lamp("WZ_Deckenleuchte", -4.60, -2.90, z_eg_ceil, radius=0.25, ring_mat="Wood_Medium", col=col_eg_lamps)

    # 2. EG Küche: 1 flache runde Deckenleuchte mittig im Raum
    add_round_ceiling_lamp("KU_Deckenleuchte", -4.60, 3.20, z_eg_ceil, radius=0.25, ring_mat="Lamp_Shade_Sage", col=col_eg_lamps)

    # 3. EG Spielzimmer: 1 flache runde Deckenleuchte mittig im Raum
    add_round_ceiling_lamp("SZ_Deckenleuchte", 5.15, 1.90, z_eg_ceil, radius=0.25, ring_mat="Lamp_Shade_Sky", col=col_eg_lamps)

    # 4. EG Gästeklo: 1 kleine flache runde Deckenleuchte mittig im Raum
    add_round_ceiling_lamp("GK_Deckenleuchte", 5.20, -4.25, z_eg_ceil, radius=0.20, ring_mat="Wood_Medium", col=col_eg_lamps)

    # 5. EG Flur (langer Raum, 12.6 m): 2 flache runde Deckenleuchten
    add_round_ceiling_lamp("FL_EG_Deckenleuchte_1", 0.40, -3.20, z_eg_ceil, radius=0.21, ring_mat="Wood_Medium", col=col_eg_lamps)
    add_round_ceiling_lamp("FL_EG_Deckenleuchte_2", 0.40, 1.20, z_eg_ceil, radius=0.21, ring_mat="Wood_Medium", col=col_eg_lamps)

    # 6. 1. OG Flur / Galerie (langer Raum): 2 flache runde Deckenleuchten
    add_round_ceiling_lamp("FL_OG_Deckenleuchte_1", 0.20, -0.50, z_og_ceil, radius=0.21, ring_mat="Wood_Medium", col=col_og_lamps)
    add_round_ceiling_lamp("FL_OG_Deckenleuchte_2", 0.20, 3.10, z_og_ceil, radius=0.21, ring_mat="Wood_Medium", col=col_og_lamps)

    # 7. 1. OG Kinderzimmer: 1 flache runde Deckenleuchte mittig im Raum
    add_round_ceiling_lamp("KZ_Deckenleuchte", -4.50, 0.50, z_og_ceil, radius=0.25, ring_mat="Lamp_Shade_Sky", col=col_og_lamps)

    # 8. 1. OG Elternzimmer: 1 flache runde Deckenleuchte mittig im Raum
    add_round_ceiling_lamp("EZ_Deckenleuchte", 4.80, 3.20, z_og_ceil, radius=0.25, ring_mat="Wood_Medium", col=col_og_lamps)

    # 9. 1. OG Badezimmer: 1 flache runde Deckenleuchte mittig im Raum
    add_round_ceiling_lamp("BD_Deckenleuchte", 5.00, -2.50, z_og_ceil, radius=0.24, ring_mat="Brass_Gold", col=col_og_lamps)

    # 10. DG Dachboden (langer Raum, 16.8 m): 2 flache runde Deckenleuchten an den Kehlbalken
    add_round_ceiling_lamp("DB_Deckenleuchte_1", -3.00, 0.20, 7.82, radius=0.24, ring_mat="Brass_Gold", col=col_dg_lamps)
    add_round_ceiling_lamp("DB_Deckenleuchte_2", 3.00, 0.20, 7.82, radius=0.24, ring_mat="Brass_Gold", col=col_dg_lamps)


# ==============================================================================
# 7C. BEREICH 04: EINFAHRT & FAMILIEN-GARAGE MIT GROSSER WERKBANK
#     (X = +11.2 .. +17.4, Y = -16.8 .. +2.2)
# ==============================================================================

def build_04_einfahrt_und_garage():
    """
    Baut rechts (östlich) neben Maxis Haus die gepflasterte Einfahrt (von der
    Straße Ahornweg bei Y = -16.8 durch die Zaunöffnung bei Y = -14.0 bis Y = -5.8)
    sowie die geräumige Familien-Garage (6.2 m x 8.0 m = 49.6 m², X = 11.2..17.4,
    Y = -5.8..+2.2) mit geöffnetem Sektionaltor, großer Werkbank, Schraubstock,
    Werkzeugkasten, Werkzeug-Lochwand, Schwerlastregal, Rasenmäher, Fahrrädern
    und 2 Garagen-Deckenleuchten.
    """
    col_garten = get_collection("00_Garten")
    col_gar = get_collection("EG_Garage", "01_EG")
    col_gar_roof = get_collection("Garage_Dach_und_Decke", "01_EG")

    # --------------------------------------------------------------------------
    # 1. GEPFLASTERTE EINFAHRT (X = 11.4 .. 17.2, Y = -16.75 .. -5.80)
    # --------------------------------------------------------------------------
    add_box("Einfahrt_Pflaster_Haupt", 11.40, 17.20, -16.75, -5.80, 0.01, 0.05, "Driveway_Stone", col_garten)
    add_box("Einfahrt_Randstein_West", 11.20, 11.40, -16.75, -5.80, 0.01, 0.09, "Driveway_Border", col_garten)
    add_box("Einfahrt_Randstein_Ost", 17.20, 17.40, -16.75, -5.80, 0.01, 0.09, "Driveway_Border", col_garten)
    # Pflaster-Querfugen für klare Freestyle-Struktur auf der Einfahrt
    for idx, py in enumerate([-15.2, -13.6, -12.0, -10.4, -8.8, -7.2]):
        add_box(f"Einfahrt_Pflasterstreifen_{idx+1}", 11.42, 17.18, py - 0.08, py + 0.08, 0.05, 0.058, "Driveway_Border", col_garten)

    # Markante Einfahrts-Torpfosten am Zaun (Y = -14.0)
    add_box("Einfahrt_Pfosten_West", 11.08, 11.38, -14.15, -13.85, 0.0, 1.18, "Wall_Exterior", col_garten)
    add_box("Einfahrt_Pfosten_West_Kappe", 11.04, 11.42, -14.19, -13.81, 1.18, 1.28, "Roof_Tiles", col_garten)
    add_box("Einfahrt_Pfosten_Ost", 17.22, 17.52, -14.15, -13.85, 0.0, 1.18, "Wall_Exterior", col_garten)
    add_box("Einfahrt_Pfosten_Ost_Kappe", 17.18, 17.56, -14.19, -13.81, 1.18, 1.28, "Roof_Tiles", col_garten)

    # --------------------------------------------------------------------------
    # 2. GARAGEN-GEBÄUDE (X = 11.2 .. 17.4, Y = -5.8 .. +2.2, Z = 0.0 .. 2.80)
    # --------------------------------------------------------------------------
    gx1, gx2 = 11.20, 17.40
    gy1, gy2 = -5.80, 2.20
    gz1, gz2 = 0.00, 2.80
    tw = 0.22

    # Garagenboden
    add_box("GAR_Boden", gx1, gx2, gy1, gy2, -0.02, 0.03, "Garage_Floor", col_gar)

    # Südwand (Y = -5.8) mit 4.80 m breiter Garagentor-Öffnung (X = 11.90 .. 16.70, Z = 0.03 .. 2.32)
    build_wall_x(
        "GAR_Wand_Sued", gx1 - 0.10, gx2 + 0.10, gy1, tw, gz1, gz2, "Wall_Exterior", col_gar,
        openings=[
            (11.90, 16.70, 0.03, 2.32, "arch"),
        ]
    )
    # Nordwand (Y = +2.2) mit breitem Werkstattfenster über der Werkbank (X = 12.85 .. 15.75)
    build_wall_x(
        "GAR_Wand_Nord", gx1 - 0.10, gx2 + 0.10, gy2, tw, gz1, gz2, "Wall_Exterior", col_gar,
        openings=[
            (12.85, 15.75, 1.08, 2.20, "window"),
        ]
    )
    # Westwand (X = +11.2, zum Haupthaus) mit Gartentür & Seitenfenster
    build_wall_y(
        "GAR_Wand_West", gx1, gy1, gy2, tw, gz1, gz2, "Wall_Exterior", col_gar,
        openings=[
            (-4.20, -2.20, 1.00, 2.18, "window"),
            (-0.45, 0.75, 0.03, 2.15, "door"),
        ]
    )
    # Ostwand (X = +17.4) mit Oberlicht-Fenster
    build_wall_y(
        "GAR_Wand_Ost", gx2, gy1, gy2, tw, gz1, gz2, "Wall_Exterior", col_gar,
        openings=[
            (-3.60, -1.20, 1.45, 2.20, "window"),
        ]
    )

    # Geöffnetes Sektional-Garagentor (untere Lamelle am Torsturz sichtbar + 4 Lamellen unter der Decke!)
    add_box("GAR_Tor_Sturzlamelle", 11.94, 16.66, -5.86, -5.74, 2.18, 2.34, "Garage_Door_Panel", col_gar)
    add_box("GAR_Torschiene_West", 11.92, 12.00, -5.70, -2.85, 2.30, 2.36, "Metal_Silver", col_gar_roof)
    add_box("GAR_Torschiene_Ost", 16.60, 16.68, -5.70, -2.85, 2.30, 2.36, "Metal_Silver", col_gar_roof)
    for idx, ty in enumerate([-5.55, -4.85, -4.15, -3.45]):
        add_box(f"GAR_Tor_Deckenlamelle_{idx+1}", 11.98, 16.62, ty, ty + 0.62, 2.33, 2.39, "Garage_Door_Panel", col_gar_roof)

    # Garagen-Decke (Z = 2.74 .. 2.84) + Satteldach in Haus-Terrakotta (Z = 2.84 .. 4.15)
    add_box("GAR_Deckenplatte", gx1, gx2, gy1, gy2, 2.74, 2.84, "Wall_Interior", col_gar_roof)
    add_pitched_prism("GAR_Giebel_Sued", gx1 - 0.10, gx2 + 0.10, gy1 - 0.10, gy1 + 0.12, 2.80, 4.10, "Wall_Exterior", col_gar_roof, peak_axis='X')
    add_pitched_prism("GAR_Giebel_Nord", gx1 - 0.10, gx2 + 0.10, gy2 - 0.12, gy2 + 0.10, 2.80, 4.10, "Wall_Exterior", col_gar_roof, peak_axis='X')
    add_pitched_prism("GAR_Dach_Ziegel", gx1 - 0.35, gx2 + 0.35, gy1 - 0.35, gy2 + 0.35, 2.82, 4.22, "Roof_Tiles", col_gar_roof, peak_axis='X')

    # 1 dezente flache runde Garagen-Deckenleuchte mittig an der Garagendecke (ausgeschaltet)
    add_round_ceiling_lamp("GAR_Deckenleuchte", 14.30, -1.20, 2.74, radius=0.25, ring_mat="Lamp_Shade_Sage", col=col_gar_roof)

    # --------------------------------------------------------------------------
    # 3. GROSSE WERKBANK MIT SCHRAUBSTOCK, WERKZEUGKASTEN & WERKZEUG-LOCHWAND
    #    an der Nordwand der Garage (X = 11.85 .. 16.55, Y = 1.10 .. 2.02)
    # --------------------------------------------------------------------------
    # Massives Werkbank-Untergestell + Schubladenblock + Zwischenboden
    add_box("GAR_Werkbank_Bein_W", 11.95, 12.15, 1.15, 1.98, 0.03, 0.84, "Wood_Dark", col_gar)
    add_box("GAR_Werkbank_Bein_M", 14.15, 14.35, 1.15, 1.98, 0.03, 0.84, "Wood_Dark", col_gar)
    add_box("GAR_Werkbank_Bein_O", 16.25, 16.45, 1.15, 1.98, 0.03, 0.84, "Wood_Dark", col_gar)
    add_box("GAR_Werkbank_Ablage_Unten", 12.00, 14.25, 1.22, 1.95, 0.16, 0.22, "Wood_Medium", col_gar)
    # Schubladenschrank rechts unter der Werkbank (rot/holz)
    add_box("GAR_Werkbank_Schubladenschrank", 14.35, 16.35, 1.18, 1.96, 0.08, 0.84, "Box_Red", col_gar)
    for sz in (0.24, 0.44, 0.64):
        add_box(f"GAR_Werkbank_Schublade_Griff_{sz}", 14.55, 16.15, 1.14, 1.18, sz, sz + 0.05, "Metal_Silver", col_gar)
    # Dicke Eichen-Arbeitsplatte (4.60 m breit!)
    add_box("GAR_Werkbank_Arbeitsplatte", 11.88, 16.52, 1.08, 2.02, 0.84, 0.92, "Counter_Oak", col_gar)

    # Blauer Schraubstock vorne links auf der Werkbank
    add_box("GAR_Schraubstock_Basis", 12.25, 12.68, 1.06, 1.42, 0.92, 1.06, "Vise_Blue", col_gar)
    add_box("GAR_Schraubstock_Backen", 12.28, 12.65, 1.02, 1.32, 1.06, 1.18, "Vise_Blue", col_gar)
    add_box("GAR_Schraubstock_Spindel", 12.42, 12.52, 0.90, 1.06, 1.00, 1.08, "Metal_Silver", col_gar)

    # Standbohrmaschine / Tischsäge links-mittig auf der Werkbank
    add_box("GAR_Bohrmaschine_Fuss", 13.05, 13.48, 1.48, 1.88, 0.92, 0.98, "Metal_Silver", col_gar)
    add_box("GAR_Bohrmaschine_Saeule", 13.22, 13.32, 1.72, 1.82, 0.98, 1.54, "Metal_Silver", col_gar)
    add_box("GAR_Bohrmaschine_Kopf", 13.08, 13.46, 1.48, 1.85, 1.42, 1.58, "Vise_Blue", col_gar)

    # Holz-Vogelhäuschen / Bastelprojekt in der Mitte der Werkbank
    add_box("GAR_Bastelprojekt_Haus", 14.02, 14.48, 1.38, 1.76, 0.92, 1.24, "Wood_Light", col_gar)
    add_pitched_prism("GAR_Bastelprojekt_Dach", 13.96, 14.54, 1.34, 1.80, 1.24, 1.44, "Apple_Red", col_gar, peak_axis='X')

    # Großer roter Werkzeugkasten rechts auf der Werkbank
    add_box("GAR_Werkzeugkasten_Korpus", 15.35, 16.25, 1.35, 1.85, 0.92, 1.24, "Apple_Red", col_gar)
    add_box("GAR_Werkzeugkasten_Griff", 15.55, 16.05, 1.55, 1.65, 1.24, 1.32, "Metal_Silver", col_gar)

    # Werkstatthocker vor der Werkbank
    add_box("GAR_Werkstatthocker_Sitz", 13.95, 14.45, 0.38, 0.88, 0.52, 0.58, "Wood_Medium", col_gar)
    add_box("GAR_Werkstatthocker_Beine", 14.02, 14.38, 0.45, 0.81, 0.03, 0.52, "Wood_Dark", col_gar)

    # Werkzeug-Lochwände (Pegboards) links und rechts neben dem Nordfenster mit hängendem Werkzeug
    add_box("GAR_Lochwand_Links", 11.95, 12.78, 1.98, 2.05, 1.08, 2.15, "Pegboard_Wood", col_gar)
    add_box("GAR_Werkzeug_Saege", 12.08, 12.32, 1.94, 1.98, 1.45, 1.98, "Metal_Silver", col_gar)
    add_box("GAR_Werkzeug_SaegeGriff", 12.06, 12.34, 1.93, 1.98, 1.92, 2.05, "Apple_Red", col_gar)
    add_box("GAR_Werkzeug_Hammer", 12.48, 12.66, 1.94, 1.98, 1.48, 1.92, "Wood_Dark", col_gar)

    add_box("GAR_Lochwand_Rechts", 15.82, 16.65, 1.98, 2.05, 1.08, 2.15, "Pegboard_Wood", col_gar)
    add_box("GAR_Werkzeug_Schluessel1", 15.95, 16.08, 1.94, 1.98, 1.52, 1.96, "Metal_Silver", col_gar)
    add_box("GAR_Werkzeug_Schluessel2", 16.18, 16.30, 1.94, 1.98, 1.56, 1.92, "Metal_Silver", col_gar)
    add_box("GAR_Werkzeug_Wasserwaage", 15.92, 16.52, 1.94, 1.98, 1.24, 1.34, "Lamp_Shade_Yellow", col_gar)

    # --------------------------------------------------------------------------
    # 4. SCHWERLAST-LAGERREGAL, AUTOREIFEN, RASENMÄHER & FAHRRÄDER
    # --------------------------------------------------------------------------
    # Großes Schwerlastregal an der Ostwand (X = 16.52 .. 17.25, Y = -4.30 .. +0.55)
    add_box("GAR_Regal_Rahmen", 16.55, 17.24, -4.25, 0.55, 0.03, 2.08, "Wood_Dark", col_gar)
    for rz in (0.08, 0.62, 1.16, 1.70):
        add_box(f"GAR_Regalboden_{rz}", 16.52, 17.25, -4.22, 0.52, rz, rz + 0.05, "Wood_Light", col_gar)
    # Kisten, Farbdosen & Gießkanne im Regal
    add_box("GAR_Regal_Box_Blau", 16.60, 17.18, -3.95, -2.95, 0.67, 1.08, "Box_Blue", col_gar)
    add_box("GAR_Regal_Box_Gruen", 16.60, 17.18, -2.65, -1.65, 0.67, 1.08, "Box_Green", col_gar)
    add_box("GAR_Regal_Box_Rot", 16.60, 17.18, -1.35, -0.35, 1.21, 1.62, "Box_Red", col_gar)
    add_box("GAR_Regal_Karton", 16.60, 17.18, -3.80, -2.50, 1.21, 1.62, "Box_Cardboard", col_gar)

    # Stapel mit 4 Autoreifen (Winterreifen) in der Süd-Ost-Ecke (X = 16.45 .. 17.22, Y = -5.45 .. -4.45)
    for ti in range(4):
        tz1 = 0.03 + ti * 0.24
        add_box(f"GAR_Autoreifen_{ti+1}", 16.48, 17.20, -5.42, -4.55, tz1, tz1 + 0.22, "Tire_Rubber", col_gar)

    # Roter Familien-Rasenmäher an der Westwand (X = 11.45 .. 12.35, Y = -1.95 .. -0.95)
    add_box("GAR_Rasenmaeher_Chassis", 11.50, 12.30, -1.90, -1.00, 0.14, 0.42, "Apple_Red", col_gar)
    add_box("GAR_Rasenmaeher_Motor", 11.65, 12.15, -1.68, -1.22, 0.42, 0.58, "TV_Black", col_gar)
    add_sloped_slab("GAR_Rasenmaeher_Holm", 11.60, 12.20, -1.85, 0.38, -2.35, 0.98, 0.05, "Metal_Silver", col_gar)

    # Maxis Kinderfahrrad & Eltern-Fahrrad an der Westwand (X = 11.45 .. 12.40, Y = -4.95 .. -2.55)
    add_box("GAR_Kinderfahrrad_Rad1", 11.55, 12.05, -4.85, -4.35, 0.03, 0.52, "Tire_Rubber", col_gar)
    add_box("GAR_Kinderfahrrad_Rad2", 11.55, 12.05, -3.95, -3.45, 0.03, 0.52, "Tire_Rubber", col_gar)
    add_box("GAR_Kinderfahrrad_Rahmen", 11.72, 11.88, -4.65, -3.65, 0.32, 0.68, "Box_Blue", col_gar)
    add_box("GAR_Kinderfahrrad_Lenker", 11.58, 12.02, -3.75, -3.62, 0.68, 0.88, "Metal_Silver", col_gar)


# ==============================================================================
# 8. BELEUCHTUNG (SONNE, HIMMEL & RAUMLICHTER IN JEDEM ZIMMER)
# ==============================================================================

def setup_lighting():
    col_lights = get_collection("98_Beleuchtung")

    # Welt-Hintergrund (helles, freundliches Tageslicht)
    world = bpy.data.worlds.new("BlockoutWorld")
    bpy.context.scene.world = world
    bg = world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs[0].default_value = (0.78, 0.86, 0.95, 1.0)
        bg.inputs[1].default_value = 0.85

    # Sonnenlicht (Haupt- und Gegenlicht für plastische Außen- und Cutaway-Ansichten)
    def add_sun(name, energy, rot_deg):
        ldata = bpy.data.lights.new(name=name, type='SUN')
        ldata.energy = energy
        ldata.color = (1.0, 0.97, 0.90)
        ldata.angle = math.radians(15.0)
        lobj = bpy.data.objects.new(name=name, object_data=ldata)
        lobj.rotation_euler = tuple(math.radians(a) for a in rot_deg)
        link_to_col(lobj, col_lights)

    add_sun("Sun_Main", 2.8, (48, 18, -35))
    add_sun("Sun_Fill", 1.2, (55, -25, 145))

    # Warme Decken-Punktlichter in jedem einzelnen Raum für helle Innenraum-Kameraansichten
    room_lights = [
        ("Light_EG_WZ_1", (-5.5, -3.2, 2.48), 220.0),
        ("Light_EG_WZ_2", (-3.0, -2.5, 2.48), 180.0),
        ("Light_EG_Kueche_1", (-6.0, 3.8, 2.48), 220.0),
        ("Light_EG_Kueche_2", (-3.2, 3.0, 2.48), 190.0),
        ("Light_EG_Flur_S", (0.4, -3.5, 2.48), 160.0),
        ("Light_EG_Flur_N", (0.4, 2.5, 2.48), 160.0),
        ("Light_EG_Gaesteklo", (5.2, -4.2, 2.48), 160.0),
        ("Light_EG_Spielzimmer_1", (5.2, 0.5, 2.48), 220.0),
        ("Light_EG_Spielzimmer_2", (5.2, 4.0, 2.48), 200.0),
        ("Light_OG_Kinderzimmer_1", (-5.0, -2.5, 5.18), 220.0),
        ("Light_OG_Kinderzimmer_2", (-5.0, 3.0, 5.18), 220.0),
        ("Light_OG_Flur", (0.4, 0.0, 5.18), 170.0),
        ("Light_OG_Elternzimmer_1", (5.2, 3.8, 5.18), 210.0),
        ("Light_OG_Elternzimmer_2", (5.2, 1.5, 5.18), 170.0),
        ("Light_OG_Badezimmer_1", (4.2, -2.2, 5.18), 200.0),
        ("Light_OG_Badezimmer_2", (6.5, -3.2, 5.18), 200.0),
        ("Light_DG_Dachboden_W", (-4.5, 0.5, 7.65), 230.0),
        ("Light_DG_Dachboden_M", (0.0, 0.5, 7.75), 210.0),
        ("Light_DG_Dachboden_E", (4.5, 0.0, 7.65), 230.0),
        ("Light_EG_Garage_Sued", (14.3, -3.0, 2.40), 220.0),
        ("Light_EG_Garage_Nord", (14.3, 0.2, 2.40), 240.0),
    ]
    for lname, loc, energy in room_lights:
        pdata = bpy.data.lights.new(name=lname, type='POINT')
        pdata.energy = energy
        pdata.color = (1.0, 0.96, 0.88)
        pdata.shadow_soft_size = 0.65
        pdata.use_shadow = False
        pobj = bpy.data.objects.new(name=lname, object_data=pdata)
        pobj.location = loc
        link_to_col(pobj, col_lights)


# ==============================================================================
# 9. KAMERAS ANLEGEN & RENDERN
# ==============================================================================

def add_camera(name, loc, target, lens=22.0, col_name="99_Kameras"):
    col_cam = get_collection(col_name)
    cdata = bpy.data.cameras.new(name=name)
    cdata.lens = lens
    cdata.clip_start = 0.08
    cdata.clip_end = 250.0
    cobj = bpy.data.objects.new(name=name, object_data=cdata)
    cobj.location = Vector(loc)

    direction = Vector(target) - Vector(loc)
    rot_quat = direction.to_track_quat('-Z', 'Y')
    cobj.rotation_euler = rot_quat.to_euler()
    link_to_col(cobj, col_cam)
    return cobj


def configure_render_engine():
    scene = bpy.context.scene
    scene.render.engine = 'BLENDER_EEVEE'
    scene.render.resolution_x = 1600
    scene.render.resolution_y = 1000
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    if hasattr(scene.eevee, "taa_render_samples"):
        scene.eevee.taa_render_samples = 16

    # Freestyle (schwarze Kantenlinien auf allen Quadern!)
    scene.render.use_freestyle = True
    scene.render.line_thickness = 1.45
    vl = scene.view_layers[0]
    vl.use_freestyle = True
    fs = vl.freestyle_settings
    fs.crease_angle = math.radians(134.0)
    if len(fs.linesets) == 0:
        ls = fs.linesets.new("BlockoutEdges")
    else:
        ls = fs.linesets[0]
    if ls.linestyle is None:
        ls.linestyle = bpy.data.linestyles.new("BlockoutLineStyle")
    ls.select_silhouette = True
    ls.select_border = True
    ls.select_crease = True
    ls.select_contour = True
    ls.select_external_contour = True
    ls.linestyle.color = (0.10, 0.08, 0.07)
    ls.linestyle.thickness = 1.45


def set_collection_visibility(col_name, visible):
    col = COLLECTIONS.get(col_name)
    if not col:
        return
    col.hide_render = not visible
    for child in col.children_recursive:
        child.hide_render = not visible
    for obj in col.all_objects:
        obj.hide_render = not visible


def build_and_render_all_cameras():
    configure_render_engine()
    scene = bpy.context.scene

    # --------------------------------------------------------------------------
    # A. 4 CUTAWAY / ISO ÜBERSICHTS-KAMERAS
    # --------------------------------------------------------------------------
    cam_iso_all = add_camera(
        "CAM_00_Gesamthaus_und_Garten_Iso",
        loc=(-26.5, -24.5, 22.0),
        target=(0.0, 3.5, 2.2),
        lens=26.0
    )
    cam_iso_eg = add_camera(
        "CAM_01_Erdgeschoss_Cutaway_Iso",
        loc=(-15.5, -18.5, 25.5),
        target=(0.0, 0.2, 0.6),
        lens=26.0
    )
    cam_iso_og = add_camera(
        "CAM_02_Obergeschoss_Cutaway_Iso",
        loc=(-11.5, -14.2, 23.5),
        target=(0.0, 0.1, 3.6),
        lens=30.0
    )
    cam_iso_dg = add_camera(
        "CAM_03_Dachboden_Cutaway_Iso",
        loc=(-10.8, -13.0, 22.5),
        target=(0.0, 0.0, 6.2),
        lens=32.0
    )

    # 1) 00_Gesamthaus_und_Garten_Blockout_Iso.png (Alle Etagen & großer Garten sichtbar)
    set_collection_visibility("00_Garten", True)
    set_collection_visibility("01_EG", True)
    set_collection_visibility("02_OG", True)
    set_collection_visibility("03_DG", True)
    scene.camera = cam_iso_all
    scene.render.filepath = os.path.join(RENDER_DIR, "00_Gesamthaus_und_Garten_Blockout_Iso.png")
    bpy.ops.render.render(write_still=True)

    # 2) 01_Erdgeschoss_Cutaway_Iso.png (02_OG, 03_DG und Garagendach ausgeblendet)
    set_collection_visibility("01_EG", True)
    set_collection_visibility("EG_Deckenleuchten", False)
    set_collection_visibility("Garage_Dach_und_Decke", False)
    set_collection_visibility("02_OG", False)
    set_collection_visibility("03_DG", False)
    scene.camera = cam_iso_eg
    scene.render.filepath = os.path.join(RENDER_DIR, "01_Erdgeschoss_Cutaway_Iso.png")
    bpy.ops.render.render(write_still=True)

    # 3) 02_Obergeschoss_Cutaway_Iso.png (03_DG ausgeblendet, 02_OG mit Badewanne sichtbar)
    set_collection_visibility("01_EG", True)
    set_collection_visibility("EG_Deckenleuchten", True)
    set_collection_visibility("Garage_Dach_und_Decke", True)
    set_collection_visibility("02_OG", True)
    set_collection_visibility("OG_Deckenleuchten", False)
    set_collection_visibility("03_DG", False)
    scene.camera = cam_iso_og
    scene.render.filepath = os.path.join(RENDER_DIR, "02_Obergeschoss_Cutaway_Iso.png")
    bpy.ops.render.render(write_still=True)

    # 4) 03_Dachboden_Cutaway_Iso.png (Nur DG_Dachhaut ausgeblendet, damit Dachbalken & Möbel frei sichtbar sind!)
    set_collection_visibility("01_EG", True)
    set_collection_visibility("Garage_Dach_und_Decke", True)
    set_collection_visibility("02_OG", True)
    set_collection_visibility("OG_Deckenleuchten", True)
    set_collection_visibility("03_DG", True)
    set_collection_visibility("DG_Dachhaut", False)
    scene.camera = cam_iso_dg
    scene.render.filepath = os.path.join(RENDER_DIR, "03_Dachboden_Cutaway_Iso.png")
    bpy.ops.render.render(write_still=True)

    # Vor den Innen- und Außenkameras ALLE Etagen, Deckenleuchten, Garagendach & Dachhaut wieder zu 100% sichtbar schalten!
    set_collection_visibility("00_Garten", True)
    set_collection_visibility("01_EG", True)
    set_collection_visibility("EG_Deckenleuchten", True)
    set_collection_visibility("Garage_Dach_und_Decke", True)
    set_collection_visibility("02_OG", True)
    set_collection_visibility("OG_Deckenleuchten", True)
    set_collection_visibility("03_DG", True)
    set_collection_visibility("DG_Deckenleuchten", True)
    set_collection_visibility("DG_Dachhaut", True)

    # --------------------------------------------------------------------------
    # B. INNENRAUM- & AUSSEN-KAMERAS FÜR ALLE BEREICHE (MIT DECKENLEUCHTEN IM BILD!)
    # --------------------------------------------------------------------------
    interior_and_exterior_cameras = [
        # 1. Haus Außen, Straße, Bürgersteig, Nachbarhäuser & großer Garten
        (
            "Blockout_CAM_Aussen_01_Vorderansicht_Vorgarten",
            (3.2, -23.5, 4.2), (0.0, -6.3, 2.8), 20.0
        ),
        (
            "Blockout_CAM_Aussen_02_Rueckansicht_Hausgarten",
            (2.5, 25.5, 5.2), (-0.5, 8.5, 2.4), 21.0
        ),
        (
            "Blockout_CAM_Aussen_03_Terrasse_und_Apfelbaum",
            (7.5, 9.5, 2.15), (-9.5, 11.5, 2.0), 21.0
        ),
        (
            "Blockout_CAM_Aussen_04_Strasse_Buergersteig_und_Nachbarhaeuser",
            (-28.5, -18.5, 2.45), (12.0, -14.5, 2.2), 19.0
        ),
        (
            "Blockout_CAM_Aussen_05_Nachbarschaft_Totale_Drei_Haeuser",
            (0.0, -52.0, 18.5), (0.0, 0.0, 2.5), 22.0
        ),

        # 2. Großes Wohnzimmer (01_EG_Wohnzimmer: X = -8.4..-1.2, Y = -6.3..+0.3)
        (
            "Blockout_CAM_WZ_01_Sofa_und_Fenster",
            (-1.60, -5.45, 1.55), (-6.60, -2.15, 1.18), 17.5
        ),
        (
            "Blockout_CAM_WZ_02_Gegenschuss_TV_Regal_und_Durchgang",
            (-7.35, -0.55, 1.55), (-3.10, -4.45, 1.18), 17.0
        ),

        # 3. Große Küche (01_EG_Kueche: X = -8.4..-1.2, Y = +0.3..+6.3)
        (
            "Blockout_CAM_KU_01_Kuechenzeile_und_Esstisch",
            (-1.6, 1.1, 1.55), (-6.5, 4.4, 1.18), 18.0
        ),
        (
            "Blockout_CAM_KU_02_Gegenschuss_Esstisch_zur_Terrasse",
            (-7.4, 1.2, 1.55), (-2.6, 5.4, 1.18), 18.0
        ),

        # 4. Großes Spielzimmer im EG (01_EG_Spielzimmer: X = +2.0..+8.4, Y = -2.5..+6.3)
        (
            "Blockout_CAM_SZ_01_Totale_Spielteppich_Regal_und_Rutsche",
            (2.55, -1.65, 1.58), (5.65, 3.25, 1.15), 17.5
        ),
        (
            "Blockout_CAM_SZ_02_Gegenschuss_Maltisch_und_Kuschelecke",
            (7.65, 5.45, 1.58), (4.45, -0.85, 1.15), 17.5
        ),

        # 5. Gästeklo im EG (01_EG_Gaesteklo: X = +2.0..+8.4, Y = -6.3..-2.5)
        (
            "Blockout_CAM_GK_01_Waschbecken_Spiegel_und_WC",
            (2.55, -5.75, 1.48), (6.20, -3.20, 1.18), 17.5
        ),
        (
            "Blockout_CAM_GK_02_Gegenschuss_WC_und_Waschplatz",
            (7.80, -5.75, 1.48), (4.50, -3.10, 1.18), 17.5
        ),

        # 6. Flur & Treppenhaus (01_EG_Flur & 02_OG_Flur)
        (
            "Blockout_CAM_FL_01_Haustuer_Garderobe_und_Treppe",
            (0.2, 5.2, 1.55), (0.4, -4.8, 1.22), 18.5
        ),
        (
            "Blockout_CAM_FL_02_Oberer_Flur_und_Dachbodentreppe",
            (1.4, 5.2, 4.30), (-0.1, -3.5, 4.00), 18.5
        ),

        # 7. Kinderzimmer im OG (02_OG_Kinderzimmer: X = -8.4..-1.2, Y = -6.3..+6.3)
        (
            "Blockout_CAM_KZ_01_Kinderbett_Kissenburg_und_Eisenbahn",
            (-1.65, -4.20, 4.30), (-6.10, 1.60, 3.85), 17.5
        ),
        (
            "Blockout_CAM_KZ_02_Gegenschuss_Schrank_und_Tuer",
            (-5.20, 5.40, 4.30), (-3.10, -3.60, 3.85), 17.5
        ),

        # 8. Elternzimmer im OG (02_OG_Elternzimmer: X = +2.0..+8.4, Y = +0.3..+6.3)
        (
            "Blockout_CAM_EZ_01_Doppelbett_und_Fenster",
            (7.65, 1.05, 4.30), (3.85, 4.15, 3.90), 17.5
        ),
        (
            "Blockout_CAM_EZ_02_Gegenschuss_Kleiderschrank_und_Leseecke",
            (2.65, 5.55, 4.30), (6.25, 1.25, 3.90), 17.5
        ),

        # 9. Badezimmer im OG MIT GROSSER BADEWANNE (02_OG_Badezimmer: X = +2.0..+8.4, Y = -6.3..+0.3)
        (
            "Blockout_CAM_BD_01_Waschtisch_Tritthocker_und_Badewanne",
            (2.45, -5.55, 4.32), (5.35, -1.85, 3.85), 17.0
        ),
        (
            "Blockout_CAM_BD_02_Badewanne_und_Dusche",
            (2.55, -0.45, 4.28), (6.25, -2.85, 3.82), 17.5
        ),

        # 10. Dachboden im DG (03_DG_Dachboden: X = -8.4..+8.4, Y = -6.3..+6.3)
        (
            "Blockout_CAM_DB_01_Totale_Dachbalken_Schatztruhe_und_Fenster",
            (-7.2, -1.2, 6.70), (4.5, 0.4, 6.35), 18.5
        ),
        (
            "Blockout_CAM_DB_02_Geheimversteck_und_Kisten_Ecke",
            (6.8, -1.0, 6.70), (-4.8, 1.8, 6.35), 18.5
        ),

        # 11. Einfahrt & Familien-Garage mit großer Werkbank (X = +11.2..+17.4, Y = -16.8..+2.2)
        (
            "Blockout_CAM_GAR_01_Einfahrt_und_Garagentor_Aussen",
            (13.8, -20.5, 2.35), (14.1, -3.5, 1.55), 20.0
        ),
        (
            "Blockout_CAM_GAR_02_Garage_Innen_Werkbank_und_Werkzeugwand",
            (13.2, -5.2, 1.62), (14.4, 1.6, 1.22), 18.0
        ),
        (
            "Blockout_CAM_GAR_03_Garage_Gegenschuss_durch_Tor_zur_Einfahrt",
            (15.6, 1.2, 1.65), (13.4, -8.5, 1.20), 18.0
        ),
    ]

    for cam_name, loc, target, lens in interior_and_exterior_cameras:
        cobj = add_camera(cam_name, loc=loc, target=target, lens=lens)
        scene.camera = cobj
        scene.render.filepath = os.path.join(RENDER_DIR, f"{cam_name}.png")
        bpy.ops.render.render(write_still=True)

    # Setze Haupt-Übersichtskamera aktiv & speichere die komplette .blend-Datei
    scene.camera = cam_iso_all
    bpy.ops.wm.save_as_mainfile(filepath=BLEND_PATH)
    print("FERTIG! Gespeichert unter:", BLEND_PATH)


def main():
    import sys
    if BASE_DIR not in sys.path:
        sys.path.insert(0, BASE_DIR)
    from neighbor_anna_ahornweg2 import build_anna_house
    from neighbor_ben_ahornweg6 import build_ben_house
    from street_and_nature import build_street_and_nature

    reset_scene()
    init_palette()
    build_00_garten()
    build_01_eg()
    build_02_og()
    build_03_dg()
    build_all_ceiling_lamps()
    build_04_einfahrt_und_garage()
    build_anna_house(add_box, add_pitched_prism, add_sloped_slab, get_collection, make_mat)
    build_ben_house(add_box, add_pitched_prism, add_sloped_slab, get_collection, make_mat)
    build_street_and_nature(add_box, get_collection, make_mat)
    setup_lighting()
    build_and_render_all_cameras()


if __name__ == "__main__":
    main()


