# -*- coding: utf-8 -*-
"""
2026-11-05: Flur-Treppe im Haus-Blockout neu aufbauen (die alten Stufen-Quader schwebten
frei in der Luft, von unten sah es aus wie eine hängende Treppe) + neue Flur-Kameras rendern.
Aufruf: blender -b Maxis_Haus_Komplett_Blockout.blend --python fix_flur_treppe_und_kameras.py
"""
import os, bpy, bmesh
from mathutils import Vector

OUT = "/home/felix/projects/dump/Maxis_Welt_Korrekturmappe/11_Flur_Neu_Treppe_Blender_und_Flow"
M = bpy.data.materials


def col_of(name):
    c = bpy.data.collections.get(name)
    if c is None:
        c = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(c)
    return c


def box(name, x1, x2, y1, y2, z1, z2, mat, col):
    old = bpy.data.objects.get(name)
    if old:
        bpy.data.objects.remove(old, do_unlink=True)
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co.x = (x1 + x2) / 2 + v.co.x * (x2 - x1)
        v.co.y = (y1 + y2) / 2 + v.co.y * (y2 - y1)
        v.co.z = (z1 + z2) / 2 + v.co.z * (z2 - z1)
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me)
    o.data.materials.append(M.get(mat))
    col.objects.link(o)
    return o


def slab(name, x1, x2, ya, za, yb, zb, th, mat, col):
    """geneigte Platte von (ya,za) nach (yb,zb), Dicke th senkrecht nach unten"""
    old = bpy.data.objects.get(name)
    if old:
        bpy.data.objects.remove(old, do_unlink=True)
    d = Vector((0, yb - ya, zb - za)).normalized()
    n = Vector((0, d.z, -d.y)) * th  # nach unten
    if n.z > 0:
        n = -n
    vs = [(x1, ya, za), (x2, ya, za), (x2, yb, zb), (x1, yb, zb)]
    vs += [(x, y + n.y, z + n.z) for (x, y, z) in vs]
    fs = [(0, 1, 2, 3), (4, 7, 6, 5), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]
    me = bpy.data.meshes.new(name); me.from_pydata(vs, [], fs); me.update()
    o = bpy.data.objects.new(name, me); o.data.materials.append(M.get(mat)); col.objects.link(o)
    return o


def stair(prefix, x1, x2, y0, y1, z0, rise, n, rail_x, col, rail_side_outer):
    """massive Treppe: jede Stufe ist ein Block vom Treppenfuß bis zur Trittfläche,
    plus helle Setzstufen-Kante, Wange auf der offenen Seite, Geländerstäbe, Handlauf"""
    dy = (y1 - y0) / n
    dz = rise / n
    for i in range(n):
        ya, yb = y0 + i * dy, y0 + (i + 1) * dy
        zt = z0 + (i + 1) * dz
        box(f"{prefix}_Stufe_{i+1}", x1, x2, ya, yb, z0 + 0.0, zt - 0.035, "Wall_Interior", col)   # heller Stufenkörper
        box(f"{prefix}_Tritt_{i+1}", x1 - 0.02, x2, ya - 0.025, yb, zt - 0.035, zt, "Wood_Medium", col)  # Holz-Trittfläche
    # Wange (offene Seite) als geneigte Holzplatte, unten bis zum Boden geschlossen (Dreieck als Kasten-Näherung)
    wx1, wx2 = (x1 - 0.06, x1) if rail_side_outer == "west" else (x2, x2 + 0.06)
    slab(f"{prefix}_Wange", wx1, wx2, y0 - 0.05, z0 + dz + 0.10, y1, z0 + rise + 0.10, 0.30, "Wood_Dark", col)
    # Geländerstäbe (weiß) je Stufe + Handlauf
    for i in range(n):
        yc = y0 + (i + 0.5) * dy
        zt = z0 + (i + 1) * dz
        box(f"{prefix}_Stab_{i+1}", rail_x - 0.02, rail_x + 0.02, yc - 0.02, yc + 0.02, zt, zt + 0.90, "Frame_Window", col)
    box(f"{prefix}_Antrittspfosten", rail_x - 0.05, rail_x + 0.05, y0 - 0.05, y0 + 0.05, z0, z0 + dz + 0.98, "Wood_Dark", col)
    slab(f"{prefix}_Handlauf", rail_x - 0.04, rail_x + 0.04, y0, z0 + dz + 0.95, y1, z0 + rise + 0.95, 0.07, "Wood_Dark", col)


def main():
    # 1) alte schwebende Stufen + Handläufe entfernen
    names = [o.name for o in bpy.data.objects
             if o.name.startswith(("FL_Treppe_", "OG_Dachbodentreppe_", "OG_Galerie_"))]
    for nm in names:
        bpy.data.objects.remove(bpy.data.objects[nm], do_unlink=True)
    print("entfernt:", len(names))

    col_fl = col_of("EG_Flur")
    col_og = col_of("OG_Flur")
    # EG -> OG: X 0.88..1.90, Y 1.80..5.40, 0 -> 2.80 m, offene Seite West (rail bei x=0.84)
    stair("FL_Treppe", 0.88, 1.90, 1.80, 5.40, 0.0, 2.80, 14, 0.84, col_fl, "west")
    # OG -> DG: X -0.85..0.35, Y -5.10..-1.60, 2.80 -> 5.50 m, offene Seite Ost (rail bei x=0.39)
    stair("OG_Dachbodentreppe", -0.85, 0.35, -5.10, -1.60, 2.82, 2.68, 14, 0.39, col_og, "east")

    # Galerie-Brüstung oben: statt massiver Holzplatte Handlauf + weiße Stäbe
    for nm in ("OG_Flur_Gelaender_West", "OG_Flur_Gelaender_Sued"):
        o = bpy.data.objects.get(nm)
        if o:
            bpy.data.objects.remove(o, do_unlink=True)
    box("OG_Galerie_Handlauf_West", 0.79, 0.89, 1.75, 5.40, 3.70, 3.78, "Wood_Dark", col_og)
    box("OG_Galerie_Handlauf_Sued", 0.79, 1.95, 1.74, 1.84, 3.70, 3.78, "Wood_Dark", col_og)
    k = 0
    y = 1.85
    while y < 5.35:
        box(f"OG_Galerie_Stab_W_{k}", 0.82, 0.86, y - 0.02, y + 0.02, 2.84, 3.70, "Frame_Window", col_og); y += 0.14; k += 1
    x = 0.95
    while x < 1.92:
        box(f"OG_Galerie_Stab_S_{k}", x - 0.02, x + 0.02, 1.77, 1.81, 2.84, 3.70, "Frame_Window", col_og); x += 0.14; k += 1

    # 2) neue Flur-Kameras
    col_cam = col_of("99_Flur_Neu_Kameras")
    cams = [
        ("FLUR_CAM_01_Haustuer_Garderobe_Blick_Sued", (0.3, 0.3, 1.40), (0.3, -6.3, 1.05), 20.0),
        ("FLUR_CAM_02_Eingang_Blick_zur_Treppe_Nord", (0.15, -2.9, 1.50), (1.15, 4.6, 1.55), 18.0),
        ("FLUR_CAM_03_Kinderaugenhoehe_Haustuer_und_Garderobe", (0.9, -2.2, 0.95), (-0.4, -6.3, 1.05), 20.0),
        ("FLUR_CAM_04_Treppenfuss_Nah_Blick_nach_oben", (-0.6, 0.4, 1.20), (1.4, 4.6, 2.30), 17.0),
        ("FLUR_CAM_05_OG_Galerie_und_Dachbodentreppe", (0.05, 5.75, 4.35), (-0.15, -5.0, 3.95), 17.0),
    ]
    sc = bpy.context.scene
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 1600, 1000, 100
    sc.render.image_settings.file_format = 'PNG'
    only = os.environ.get("RENDER_ONLY", "")
    for name, loc, tgt, lens in cams:
        old = bpy.data.objects.get(name)
        if old:
            bpy.data.objects.remove(old, do_unlink=True)
        cd = bpy.data.cameras.new(name); cd.lens, cd.clip_start, cd.clip_end = lens, 0.08, 250.0
        co = bpy.data.objects.new(name, cd)
        co.location = Vector(loc)
        co.rotation_euler = (Vector(tgt) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
        col_cam.objects.link(co)
        if only and not name.startswith(only):
            continue
        sc.camera = co
        sc.render.filepath = os.path.join(OUT, name + ".png")
        bpy.ops.render.render(write_still=True)
        print("Gerendert:", sc.render.filepath)
    bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
    print("gespeichert")


main()
