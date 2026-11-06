#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Erstellt in Blender 3D (EEVEE / Studio-Pixar-Shading mit Subsurface & Bevels) die
offiziellen Objekt-Referenzbilder (OBJ_01 bis OBJ_12) für Folge 1: "Die große Kissen-Expedition".
Für OBJ_01 (Hasi) wird das offizielle 3D-Pixar-Modelsheet kopiert.
"""

import bpy
import os
import math
import shutil

OUT_DIR = "/home/felix/projects/dump/Maxis_Welt_Korrekturmappe/05_Folge_01_Die_grosse_Kissen_Expedition/00_Objekt_Referenzbilder_Props"
os.makedirs(OUT_DIR, exist_ok=True)

# Copy Hasi modelsheet as OBJ_01
HASI_SRC = "/home/felix/projects/dump/Maxis_Welt_Korrekturmappe/02_Charaktere_Steckbriefe_und_Bilder/02_Hasi_Kuschelhase_Modelsheet.jpg"
if os.path.exists(HASI_SRC):
    shutil.copyfile(HASI_SRC, os.path.join(OUT_DIR, "OBJ_01_Hasi_Maxis_Stoffhase.jpg"))


def reset_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scn = bpy.context.scene
    for eng in ["BLENDER_EEVEE_NEXT", "BLENDER_EEVEE"]:
        try:
            scn.render.engine = eng
            break
        except Exception:
            pass
    scn.render.resolution_x = 1280
    scn.render.resolution_y = 720
    scn.render.image_settings.file_format = "JPEG"
    scn.render.image_settings.quality = 95

    # Warm Pixar studio world
    world = bpy.data.worlds.new("StudioWorld")
    scn.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs[0].default_value = (0.22, 0.24, 0.28, 1.0)
        bg.inputs[1].default_value = 1.1

    # Studio backdrop cyclorama
    bpy.ops.mesh.primitive_plane_add(size=12.0, location=(0, 0, 0))
    floor = bpy.context.active_object
    mat_bg = make_mat("StudioFloor", (0.78, 0.80, 0.84), rough=0.65)
    floor.data.materials.append(mat_bg)

    # 3-Point Pixar Studio Lighting
    add_light("KeyLight", "AREA", (2.2, -2.4, 2.8), (math.radians(42), 0, math.radians(38)), 180.0, (1.0, 0.96, 0.88), size=2.2)
    add_light("FillLight", "AREA", (-2.5, -1.8, 1.8), (math.radians(55), 0, math.radians(-42)), 90.0, (0.88, 0.94, 1.0), size=2.5)
    add_light("RimLight", "AREA", (0.0, 2.4, 2.4), (math.radians(-45), 0, 0), 130.0, (1.0, 0.98, 0.92), size=2.0)

    # Camera
    cam_data = bpy.data.cameras.new("StudioCam")
    cam_data.lens = 45.0
    cam_obj = bpy.data.objects.new("StudioCam", cam_data)
    scn.collection.objects.link(cam_obj)
    scn.camera = cam_obj
    return scn, cam_obj


def add_light(name, ltype, loc, rot, energy, color, size=1.5):
    ld = bpy.data.lights.new(name, type=ltype)
    ld.energy = energy
    ld.color = color
    if hasattr(ld, "size"):
        ld.size = size
    lo = bpy.data.objects.new(name, ld)
    bpy.context.scene.collection.objects.link(lo)
    lo.location = loc
    lo.rotation_euler = rot


def make_mat(name, rgb, rough=0.4, metal=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (rgb[0], rgb[1], rgb[2], 1.0)
        bsdf.inputs["Roughness"].default_value = rough
        bsdf.inputs["Metallic"].default_value = metal
    return m


def look_at(cam, loc, target, lens=45.0):
    cam.location = loc
    cam.data.lens = lens
    from mathutils import Vector
    direction = Vector(target) - Vector(loc)
    rot_quat = direction.to_track_quat("-Z", "Y")
    cam.rotation_euler = rot_quat.to_euler()


def bevel_and_subsurf(obj, width=0.015, levels=2):
    bev = obj.modifiers.new("Bevel", "BEVEL")
    bev.width = width
    bev.segments = 3
    sub = obj.modifiers.new("Subsurf", "SUBSURF")
    sub.levels = levels
    sub.render_levels = levels
    for poly in obj.data.polygons:
        poly.use_smooth = True


def render_to(filename):
    path = os.path.join(OUT_DIR, filename)
    bpy.context.scene.render.filepath = path
    bpy.ops.render.render(write_still=True)
    print("Rendered:", path)


# ==============================================================================
# OBJ_02: BENS GELBER HOLZZOLLSTOCK (Folding Ruler)
# ==============================================================================
scn, cam = reset_scene()
mat_yellow = make_mat("RulerYellow", (0.95, 0.72, 0.12), rough=0.32)
mat_red_pin = make_mat("RulerPin", (0.82, 0.18, 0.14), rough=0.35)
mat_tick = make_mat("RulerTick", (0.12, 0.12, 0.12), rough=0.5)

angles = [15, -25, 35, -35, 25]
cx, cy = -0.55, 0.0
for i, ang in enumerate(angles):
    rad = math.radians(ang)
    seg_len = 0.34
    nx = cx + math.cos(rad) * seg_len
    ny = cy + math.sin(rad) * seg_len
    mx, my = (cx + nx) / 2.0, (cy + ny) / 2.0
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(mx, my, 0.03 + i * 0.016))
    seg = bpy.context.active_object
    seg.scale = (seg_len * 0.52, 0.038, 0.007)
    seg.rotation_euler = (0, 0, rad)
    seg.data.materials.append(mat_yellow)
    bevel_and_subsurf(seg, width=0.003, levels=1)

    # Tick marks along segment
    for t in range(-4, 5):
        tx = mx + math.cos(rad) * (t * 0.032) - math.sin(rad) * 0.022
        ty = my + math.sin(rad) * (t * 0.032) + math.cos(rad) * 0.022
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(tx, ty, 0.038 + i * 0.016))
        tk = bpy.context.active_object
        tk.scale = (0.003, 0.010, 0.002)
        tk.rotation_euler = (0, 0, rad)
        tk.data.materials.append(mat_tick)

    # Pivot pin
    bpy.ops.mesh.primitive_cylinder_add(radius=0.014, depth=0.025, location=(nx, ny, 0.035 + i * 0.016))
    pin = bpy.context.active_object
    pin.data.materials.append(mat_red_pin)
    cx, cy = nx, ny

look_at(cam, (0.0, -1.15, 0.82), (0.05, 0.0, 0.05), lens=48.0)
render_to("OBJ_02_Bens_Gelber_Holzzollstock.jpg")

# ==============================================================================
# OBJ_03: HOLZBAUSTEINE & ROTES HOLZ-FEUERWEHRAUTO
# ==============================================================================
scn, cam = reset_scene()
mat_wood = make_mat("NaturalOak", (0.76, 0.52, 0.30), rough=0.42)
mat_red = make_mat("BlockRed", (0.86, 0.22, 0.18), rough=0.35)
mat_blue = make_mat("BlockBlue", (0.18, 0.46, 0.78), rough=0.35)
mat_yel = make_mat("BlockYellow", (0.95, 0.75, 0.15), rough=0.35)
mat_grn = make_mat("BlockGreen", (0.24, 0.68, 0.38), rough=0.35)
mat_blk = make_mat("WheelBlack", (0.14, 0.14, 0.16), rough=0.45)

# Harbor tower of wooden blocks on the left
for x_off, col in [(-0.42, mat_blue), (-0.18, mat_blue)]:
    bpy.ops.mesh.primitive_cylinder_add(radius=0.055, depth=0.26, location=(x_off, 0.05, 0.13))
    c = bpy.context.active_object
    c.data.materials.append(col)
    bevel_and_subsurf(c, 0.006, 1)

bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.30, 0.05, 0.30))
beam = bpy.context.active_object
beam.scale = (0.20, 0.06, 0.04)
beam.data.materials.append(mat_red)
bevel_and_subsurf(beam, 0.005, 1)

bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=0.14, depth=0.16, location=(-0.30, 0.05, 0.42))
roof = bpy.context.active_object
roof.rotation_euler = (0, 0, math.radians(45))
roof.data.materials.append(mat_yel)
bevel_and_subsurf(roof, 0.005, 1)

bpy.ops.mesh.primitive_cube_add(size=0.11, location=(-0.56, -0.08, 0.055))
b_grn = bpy.context.active_object
b_grn.data.materials.append(mat_grn)
bevel_and_subsurf(b_grn, 0.005, 1)

# Red wooden fire truck on the right
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.28, -0.02, 0.10))
chassis = bpy.context.active_object
chassis.scale = (0.22, 0.10, 0.06)
chassis.data.materials.append(mat_red)
bevel_and_subsurf(chassis, 0.008, 2)

bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.40, -0.02, 0.20))
cab = bpy.context.active_object
cab.scale = (0.09, 0.095, 0.07)
cab.data.materials.append(mat_red)
bevel_and_subsurf(cab, 0.008, 2)

# Wooden ladder on top of fire truck
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.22, -0.02, 0.20))
lad = bpy.context.active_object
lad.scale = (0.14, 0.05, 0.015)
lad.data.materials.append(mat_wood)
bevel_and_subsurf(lad, 0.003, 1)

# 4 wheels
for wx in [0.14, 0.42]:
    for wy in [-0.13, 0.09]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.055, depth=0.03, location=(wx, wy, 0.055), rotation=(math.radians(90), 0, 0))
        wh = bpy.context.active_object
        wh.data.materials.append(mat_blk)
        bevel_and_subsurf(wh, 0.004, 1)

look_at(cam, (0.0, -1.35, 0.62), (-0.02, 0.0, 0.18), lens=48.0)
render_to("OBJ_03_Holzbausteine_und_Feuerwehrauto.jpg")

# ==============================================================================
# OBJ_04: MAMAS HOLZSCHALE MIT FRISCHEN APFELSCHNITZEN
# ==============================================================================
scn, cam = reset_scene()
mat_bowl = make_mat("OakBowl", (0.68, 0.44, 0.22), rough=0.38)
mat_apple_skin = make_mat("AppleRed", (0.85, 0.14, 0.12), rough=0.25)
mat_apple_flesh = make_mat("AppleCream", (0.98, 0.94, 0.78), rough=0.35)

bpy.ops.mesh.primitive_uv_sphere_add(radius=0.28, location=(0, 0, 0.18))
bowl = bpy.context.active_object
bowl.scale = (1.0, 1.0, 0.62)
bowl.data.materials.append(mat_bowl)
bevel_and_subsurf(bowl, 0.005, 2)

# Fill top of bowl with sculpted apple wedges
for i in range(10):
    ang = i * (2 * math.pi / 10.0)
    r = 0.11 if i % 2 == 0 else 0.05
    ax, ay = math.cos(ang) * r, math.sin(ang) * r
    bpy.ops.mesh.primitive_cylinder_add(radius=0.075, depth=0.035, location=(ax, ay, 0.25 + (i % 3) * 0.018), rotation=(math.radians(25), math.radians(15), ang))
    wedge = bpy.context.active_object
    wedge.scale = (1.0, 0.55, 0.8)
    wedge.data.materials.append(mat_apple_flesh if i % 2 == 0 else mat_apple_skin)
    bevel_and_subsurf(wedge, 0.004, 1)

look_at(cam, (0.0, -0.95, 0.58), (0.0, 0.0, 0.18), lens=50.0)
render_to("OBJ_04_Mamas_Holzschale_mit_Apfelschnitzen.jpg")

# ==============================================================================
# OBJ_05: BLAUER WISCHEIMER & WISCHMOPP
# ==============================================================================
scn, cam = reset_scene()
mat_bucket = make_mat("BucketBlue", (0.24, 0.56, 0.86), rough=0.28)
mat_handle = make_mat("HandleWhite", (0.92, 0.94, 0.96), rough=0.3)
mat_pole = make_mat("MopWood", (0.78, 0.58, 0.36), rough=0.4)
mat_mop = make_mat("MopCotton", (0.92, 0.93, 0.95), rough=0.75)

bpy.ops.mesh.primitive_cone_add(radius1=0.14, radius2=0.18, depth=0.34, location=(-0.18, 0, 0.17))
bkt = bpy.context.active_object
bkt.data.materials.append(mat_bucket)
bevel_and_subsurf(bkt, 0.005, 2)

bpy.ops.mesh.primitive_torus_add(major_radius=0.18, minor_radius=0.015, location=(-0.18, 0, 0.34))
rim = bpy.context.active_object
rim.data.materials.append(mat_bucket)

# Mop pole & cotton head
bpy.ops.mesh.primitive_cylinder_add(radius=0.016, depth=0.85, location=(0.16, 0, 0.42), rotation=(0, math.radians(-12), 0))
pole = bpy.context.active_object
pole.data.materials.append(mat_pole)

for i in range(16):
    ang = i * (2 * math.pi / 16.0)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.018, depth=0.16, location=(0.25 + math.cos(ang)*0.06, math.sin(ang)*0.06, 0.06), rotation=(math.sin(ang)*0.4, math.cos(ang)*0.4, ang))
    strand = bpy.context.active_object
    strand.data.materials.append(mat_mop)
    bevel_and_subsurf(strand, 0.003, 1)

look_at(cam, (0.0, -1.45, 0.65), (0.0, 0.0, 0.28), lens=45.0)
render_to("OBJ_05_Blauer_Wischeimer_und_Wischmopp.jpg")

# ==============================================================================
# OBJ_06: SOFAKISSEN KORALLENROT (Kissen-Insel 1)
# ==============================================================================
scn, cam = reset_scene()
mat_coral = make_mat("CushionCoral", (0.86, 0.33, 0.25), rough=0.62)
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.11))
c1 = bpy.context.active_object
c1.scale = (0.34, 0.34, 0.095)
c1.data.materials.append(mat_coral)
bevel_and_subsurf(c1, 0.035, 2)
look_at(cam, (0.0, -1.05, 0.58), (0.0, 0.0, 0.10), lens=50.0)
render_to("OBJ_06_Sofakissen_Insel_Korallenrot.jpg")

# ==============================================================================
# OBJ_07: SOFAKISSEN SENFGELB (Kissen-Insel 2)
# ==============================================================================
scn, cam = reset_scene()
mat_mustard = make_mat("CushionMustard", (0.94, 0.74, 0.18), rough=0.62)
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.11))
c2 = bpy.context.active_object
c2.scale = (0.34, 0.34, 0.095)
c2.data.materials.append(mat_mustard)
bevel_and_subsurf(c2, 0.035, 2)
look_at(cam, (0.0, -1.05, 0.58), (0.0, 0.0, 0.10), lens=50.0)
render_to("OBJ_07_Sofakissen_Insel_Senfgelb.jpg")

# ==============================================================================
# OBJ_08: SOFAKISSEN TÜRKIS & BELLOS BLAUES HUNDEKISSEN
# ==============================================================================
scn, cam = reset_scene()
mat_teal = make_mat("CushionTeal", (0.20, 0.62, 0.64), rough=0.62)
mat_dogblue = make_mat("CushionDogBlue", (0.22, 0.38, 0.62), rough=0.65)

bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.22, 0, 0.10))
c3 = bpy.context.active_object
c3.scale = (0.28, 0.28, 0.085)
c3.data.materials.append(mat_teal)
bevel_and_subsurf(c3, 0.03, 2)

bpy.ops.mesh.primitive_cylinder_add(radius=0.20, depth=0.11, location=(0.26, 0, 0.06))
c4 = bpy.context.active_object
c4.data.materials.append(mat_dogblue)
bevel_and_subsurf(c4, 0.025, 2)

look_at(cam, (0.0, -1.25, 0.62), (0.0, 0.0, 0.09), lens=48.0)
render_to("OBJ_08_Sofakissen_Tuerkis_und_Bellos_Hundekissen.jpg")

# ==============================================================================
# OBJ_09: BENS LANGE GELBE SOFAROLLE (Die Zugbrücke!)
# ==============================================================================
scn, cam = reset_scene()
mat_bolster = make_mat("BolsterYellow", (0.88, 0.66, 0.16), rough=0.58)
mat_btn = make_mat("BolsterButton", (0.72, 0.48, 0.10), rough=0.5)

bpy.ops.mesh.primitive_cylinder_add(radius=0.13, depth=0.76, location=(0, 0, 0.14), rotation=(0, math.radians(90), math.radians(18)))
bol = bpy.context.active_object
bol.data.materials.append(mat_bolster)
bevel_and_subsurf(bol, 0.03, 2)

look_at(cam, (0.0, -1.15, 0.56), (0.0, 0.0, 0.14), lens=50.0)
render_to("OBJ_09_Bens_Gelbe_Sofarolle_Zugbruecke.jpg")

# ==============================================================================
# OBJ_10: PAPAS CREMEFARBENE KAFFEETASSE
# ==============================================================================
scn, cam = reset_scene()
mat_mug = make_mat("CreamCeramic", (0.94, 0.90, 0.82), rough=0.22)
mat_coffee = make_mat("CoffeeDark", (0.22, 0.12, 0.06), rough=0.15)

bpy.ops.mesh.primitive_cylinder_add(radius=0.12, depth=0.28, location=(0, 0, 0.14))
mug = bpy.context.active_object
mug.data.materials.append(mat_mug)
bevel_and_subsurf(mug, 0.008, 2)

bpy.ops.mesh.primitive_torus_add(major_radius=0.085, minor_radius=0.022, location=(0.13, 0, 0.14), rotation=(math.radians(90), 0, 0))
hdl = bpy.context.active_object
hdl.data.materials.append(mat_mug)

bpy.ops.mesh.primitive_cylinder_add(radius=0.105, depth=0.02, location=(0, 0, 0.27))
cf = bpy.context.active_object
cf.data.materials.append(mat_coffee)

look_at(cam, (0.0, -0.85, 0.45), (0.03, 0.0, 0.15), lens=52.0)
render_to("OBJ_10_Papas_Cremefarbene_Kaffeetasse.jpg")

# ==============================================================================
# OBJ_11: ROT-WEISS KARIERTE PICKNICKDECKE & WEIDENKORB
# ==============================================================================
scn, cam = reset_scene()
mat_red_chk = make_mat("CheckRed", (0.84, 0.22, 0.20), rough=0.65)
mat_wht_chk = make_mat("CheckWhite", (0.96, 0.94, 0.90), rough=0.65)
mat_wicker = make_mat("WickerBasket", (0.72, 0.48, 0.24), rough=0.55)

# Checkered blanket grid
for gx in range(-4, 4):
    for gy in range(-3, 3):
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(gx * 0.14 + 0.07, gy * 0.14 + 0.07, 0.01))
        tile = bpy.context.active_object
        tile.scale = (0.07, 0.07, 0.006)
        tile.data.materials.append(mat_red_chk if (gx + gy) % 2 == 0 else mat_wht_chk)

# Wicker basket in center
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0.05, 0.14))
bsk = bpy.context.active_object
bsk.scale = (0.22, 0.15, 0.12)
bsk.data.materials.append(mat_wicker)
bevel_and_subsurf(bsk, 0.015, 2)

bpy.ops.mesh.primitive_torus_add(major_radius=0.16, minor_radius=0.016, location=(0, 0.05, 0.26), rotation=(math.radians(90), 0, 0))
bhdl = bpy.context.active_object
bhdl.data.materials.append(mat_wicker)

look_at(cam, (0.0, -1.35, 0.78), (0.0, 0.0, 0.10), lens=45.0)
render_to("OBJ_11_Picknickdecke_und_Weidenkorb.jpg")

# ==============================================================================
# OBJ_12: DER 5ER-APFELSCHNITZ-STERN (Das Abschluss-Ritual)
# ==============================================================================
scn, cam = reset_scene()
mat_red_chk = make_mat("CheckRed2", (0.84, 0.22, 0.20), rough=0.65)
mat_wht_chk = make_mat("CheckWhite2", (0.96, 0.94, 0.90), rough=0.65)
mat_apple_skin = make_mat("AppleRed2", (0.86, 0.14, 0.12), rough=0.25)
mat_apple_flesh = make_mat("AppleCream2", (0.98, 0.94, 0.78), rough=0.35)

for gx in range(-3, 3):
    for gy in range(-3, 3):
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(gx * 0.14 + 0.07, gy * 0.14 + 0.07, 0.01))
        tile = bpy.context.active_object
        tile.scale = (0.07, 0.07, 0.006)
        tile.data.materials.append(mat_red_chk if (gx + gy) % 2 == 0 else mat_wht_chk)

for i in range(5):
    ang = math.radians(90 + i * 72)
    rx, ry = math.cos(ang) * 0.16, math.sin(ang) * 0.16
    bpy.ops.mesh.primitive_cylinder_add(radius=0.085, depth=0.04, location=(rx, ry, 0.04), rotation=(0, math.radians(18), ang))
    sl = bpy.context.active_object
    sl.scale = (1.0, 0.48, 0.85)
    sl.data.materials.append(mat_apple_flesh)
    bevel_and_subsurf(sl, 0.006, 2)

    bpy.ops.mesh.primitive_cylinder_add(radius=0.088, depth=0.015, location=(rx * 1.08, ry * 1.08, 0.025), rotation=(0, math.radians(18), ang))
    peel = bpy.context.active_object
    peel.scale = (1.0, 0.48, 0.4)
    peel.data.materials.append(mat_apple_skin)

look_at(cam, (0.0, -0.78, 0.68), (0.0, 0.0, 0.03), lens=50.0)
render_to("OBJ_12_Der_5er_Apfelschnitz_Stern.jpg")
