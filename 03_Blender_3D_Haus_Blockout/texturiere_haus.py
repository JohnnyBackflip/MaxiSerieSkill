#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Haus texturieren und detaillieren (2026-11-06).
  blender -b Maxis_Haus_Komplett_Blockout.blend --python texturiere_haus.py
  -> Maxis_Haus_Komplett_Texturiert.blend (Original bleibt unverändert; Texturen relativ in //Texturen/)

1. Details: Fußleisten innen, Sockel außen, Treppenverkleidung (EG-Treppe und Dachbodentreppe), Küchenschrank-Fronten mit Griffen, Fensterscheiben.
2. Materialien: jedes Blockout-Material (und jeder Raumboden einzeln) -> Flow-Textur (Texturen/<id>.jpg, nahtlos).
3. UV-Maps: je Objekt eine Box-Projektion im Weltmaß (Meter je Textur aus texturen_katalog.py); Türen: eine Textur je Türfläche (fit).
"""
import os, sys, re, math
import bpy, bmesh
from mathutils import Vector

E = os.path.dirname(os.path.abspath(bpy.data.filepath)) if bpy.data.filepath else os.getcwd()
E = os.environ.get("HAUS_DIR", E)
sys.path.insert(0, E)
from texturen_katalog import T  # noqa: E402

OUT = os.environ.get("HAUS_OUT", os.path.join(E, "Maxis_Haus_Komplett_Texturiert.blend"))
COL = bpy.data.collections.get("07_Details_Texturiert") or bpy.data.collections.new("07_Details_Texturiert")
if COL.name not in bpy.context.scene.collection.children:
    bpy.context.scene.collection.children.link(COL)

# ------------------------------------------------------------------ Material-Fabrik
_img = {}
_tm = {}


def image(tid):
    if tid not in _img:
        _img[tid] = bpy.data.images.load(os.path.join(E, "Texturen", f"{tid}.jpg"), check_existing=True)
    return _img[tid]


def tex_mat(tid, rough=0.85):
    """Material mit Flow-Textur; tile (m je Bild) und mode stehen als Eigenschaften am Material (für die UV-Erzeugung)."""
    if tid in _tm:
        return _tm[tid]
    if not os.path.exists(os.path.join(E, "Texturen", f"{tid}.jpg")):
        print("FEHLT Textur:", tid); _tm[tid] = None
        return None
    tile, mode = T[tid][1], T[tid][2]
    m = bpy.data.materials.new("TX_" + tid)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    tx = nt.nodes.new("ShaderNodeTexImage")
    uv = nt.nodes.new("ShaderNodeUVMap")
    uv.uv_map = "UVMap"
    tx.image = image(tid)
    tx.extension = "EXTEND" if mode == "fit" else "REPEAT"
    tx.interpolation = "Linear"
    nt.links.new(uv.outputs["UV"], tx.inputs["Vector"])
    nt.links.new(tx.outputs["Color"], bsdf.inputs["Base Color"])
    nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    bsdf.inputs["Roughness"].default_value = rough
    for n in ("Specular IOR Level", "Specular"):
        if n in bsdf.inputs:
            bsdf.inputs[n].default_value = 0.25
    m["tile"] = float(tile)
    m["mode"] = mode
    _tm[tid] = m
    return m


def plain_mat(name, rgba, rough=0.5, metal=0.0):
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes.get("Principled BSDF")
    b.inputs["Base Color"].default_value = rgba
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    return m


def glass_mat():
    m = bpy.data.materials.get("TX_Fensterglas")
    if m:
        return m
    m = bpy.data.materials.new("TX_Fensterglas")
    m.use_nodes = True
    b = m.node_tree.nodes.get("Principled BSDF")
    b.inputs["Base Color"].default_value = (0.75, 0.88, 0.95, 1)
    b.inputs["Roughness"].default_value = 0.05
    b.inputs["Alpha"].default_value = 0.12
    for attr, val in (("surface_render_method", "BLENDED"), ("blend_method", "BLEND")):
        if hasattr(m, attr):
            try:
                setattr(m, attr, val)
            except Exception:
                pass
    if hasattr(m, "use_transparency_overlap"):
        m.use_transparency_overlap = False
    return m


# ------------------------------------------------------------------ Geometrie-Helfer
def add_box(name, center, size, mat, tile_mode=None):
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co.x *= size[0]; v.co.y *= size[1]; v.co.z *= size[2]
        v.co += Vector(center)
    bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me)
    ob.data.materials.append(mat)
    COL.objects.link(ob)
    return ob


def add_cyl(name, center, r, depth, mat, axis="Z"):
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=12, radius1=r, radius2=r, depth=depth)
    rot = {"Z": (0, 0, 0), "X": (0, math.radians(90), 0), "Y": (math.radians(90), 0, 0)}[axis]
    from mathutils import Euler
    for v in bm.verts:
        v.co.rotate(Euler(rot)); v.co += Vector(center)
    bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me)
    ob.data.materials.append(mat)
    COL.objects.link(ob)
    return ob


def add_prism(name, pts, axis, c0, c1, mat):
    """Polygon pts (2D) in der Ebene senkrecht zu 'axis' ('X': Punkte = (y,z)), extrudiert von c0 nach c1 entlang der Achse."""
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    def p3(pt, c):
        return Vector((c, pt[0], pt[1])) if axis == "X" else Vector((pt[0], c, pt[1]))
    a = [bm.verts.new(p3(p, c0)) for p in pts]
    b = [bm.verts.new(p3(p, c1)) for p in pts]
    bm.faces.new(a); bm.faces.new(list(reversed(b)))
    for i in range(len(pts)):
        j = (i + 1) % len(pts)
        bm.faces.new([a[i], a[j], b[j], b[i]])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me)
    ob.data.materials.append(mat)
    COL.objects.link(ob)
    return ob


def wbbox(o):
    b = [o.matrix_world @ Vector(c) for c in o.bound_box]
    return Vector([min(v[i] for v in b) for i in range(3)]), Vector([max(v[i] for v in b) for i in range(3)])


# ------------------------------------------------------------------ 1. Details
def details():
    objs = {o.name: o for o in bpy.data.objects if o.type == "MESH"}
    n_base = n_plinth = 0
    m_white = tex_mat("paint_white") or plain_mat("DET_Weiss", (0.95, 0.95, 0.93, 1)); m_stone = tex_mat("curb_granite") or plain_mat("DET_Stein", (0.55, 0.55, 0.55, 1))
    # Fußleisten innen / Sockel außen an allen vollen Wandsegmenten
    for name, o in list(objs.items()):
        m = re.match(r"^(EG|OG)_(Innenwand|Aussenwand)_(\w+?)_seg_\d+$", name) or re.match(r"^(GAR)_(Wand)_(\w+?)_seg_\d+$", name)
        if not m:
            continue
        mn, mx = wbbox(o)
        if mx.z - mn.z < 1.5:
            continue
        ext = mx - mn
        run_x = ext.x > ext.y
        outside = None
        if m.group(2) in ("Aussenwand", "Wand"):
            outside = {"Nord": (1, +1), "Sued": (1, -1), "Ost": (0, +1), "West": (0, -1)}.get(m.group(3).split("_")[0])
        for axis_i in ((1,) if run_x else (0,)):
            for sign in (+1, -1):
                is_out = outside is not None and outside[0] == axis_i and outside[1] == sign
                th, hh = (0.03, 0.35) if is_out else (0.02, 0.10)
                mat = m_stone if is_out else m_white
                ctr = Vector(((mn.x + mx.x) / 2, (mn.y + mx.y) / 2, mn.z + hh / 2))
                size = [ext.x if run_x else th, th if run_x else ext.y, hh]
                ctr[axis_i] = (mx[axis_i] if sign > 0 else mn[axis_i]) + sign * th / 2
                add_box(f"DET_{'Sockel' if is_out else 'Fussleiste'}_{name}_{sign}", ctr, size, mat)
                n_plinth += is_out; n_base += (not is_out)
    print("Fußleisten:", n_base, "Sockel:", n_plinth)
    # Treppenverkleidung
    m_wood = tex_mat("stair_wood") or plain_mat("DET_Holz", (0.55, 0.38, 0.22, 1))
    t1, t14 = objs.get("FL_Treppe_Tritt_1"), objs.get("FL_Treppe_Tritt_14")
    if t1 and t14:
        a, b = wbbox(t1), wbbox(t14)
        y0, y1, z0, z1 = a[0].y, b[1].y, a[1].z, b[1].z
        add_prism("DET_Treppe_Seite_EG", [(y0 - 0.02, 0.0), (y1 + 0.17, 0.0), (y1 + 0.17, z1 + 0.14), (y0 - 0.02, z0 + 0.14)], "X", 0.78, 0.82, m_wood)
        # Wangenleiste obenauf (schräger Balken)
        L = math.hypot(y1 - y0, z1 - z0)
        ang = math.atan2(z1 - z0, y1 - y0)
        ob = add_box("DET_Treppe_Wangenleiste_EG", ((0.80), (y0 + y1) / 2, (z0 + z1) / 2 + 0.15), (0.06, L + 0.1, 0.05), m_wood)
        ob.rotation_euler = (-ang, 0, 0)
    w = objs.get("OG_Dachbodentreppe_Wange")
    if w:
        mn, mx = wbbox(w)
        add_prism("DET_Treppe_Seite_DG", [(mn.y, mn.z - 0.05), (mx.y, mx.z - 0.45), (mx.y, mx.z - 0.05), (mn.y, mn.z + 0.28)], "X", mn.x - 0.05, mn.x, m_wood)
    # Küchenschränke: Fronten mit Griffen
    m_sage, m_metal = (tex_mat("kitchen_sage") or plain_mat("DET_Salbei", (0.55, 0.68, 0.55, 1))), plain_mat("DET_Griff", (0.78, 0.74, 0.62, 1), 0.3, 0.9)
    def fronts(o, face_axis, face_sign, z0, z1, tag):
        mn, mx = wbbox(o)
        run_axis = 1 if face_axis == 0 else 0
        L = mx[run_axis] - mn[run_axis]
        n = max(1, round(L / 0.6)); w = L / n
        for i in range(n):
            c = mn[run_axis] + w * (i + 0.5)
            cen = Vector((0, 0, (z0 + z1) / 2))
            cen[run_axis] = c
            cen[face_axis] = (mx[face_axis] if face_sign > 0 else mn[face_axis]) + face_sign * 0.011
            size = [0.02, 0.02, z1 - z0]; size[face_axis] = 0.022; size[run_axis] = w - 0.012
            add_box(f"DET_Front_{tag}_{i}", cen, size, m_sage)
            gc = Vector(cen); gc[face_axis] += face_sign * 0.03; gc[run_axis] += (w / 2 - 0.07); gc[2] = z1 - 0.12 if z0 < 0.5 else z0 + 0.12
            ax = "Y" if face_axis == 0 else "X"
            add_cyl(f"DET_Griff_{tag}_{i}", gc, 0.011, 0.05, m_metal, "X" if face_axis == 0 else "Y")
    if "KU_Zeile_West_Korpus" in objs:
        fronts(objs["KU_Zeile_West_Korpus"], 0, +1, 0.09, 0.84, "West")
    if "KU_Zeile_Nord_Korpus" in objs:
        fronts(objs["KU_Zeile_Nord_Korpus"], 1, -1, 0.09, 0.84, "Nord")
    for nm in ("KU_Oberschrank_1", "KU_Oberschrank_2"):
        if nm in objs:
            mn, mx = wbbox(objs[nm]); fronts(objs[nm], 0, +1, mn.z + 0.03, mx.z - 0.03, nm[-12:])
    # Fensterscheiben (Haus)
    glass = glass_mat()
    wins = {}
    for name, o in objs.items():
        m = re.match(r"^(EG|OG|DG)_(Aussenwand|Giebel)_(\w+?)_window_(\d+)_(left|right|top|sillboard)$", name)
        if m:
            wins.setdefault(name.rsplit("_", 1)[0], []).append(o)
    for key, parts in wins.items():
        mins = [wbbox(p)[0] for p in parts]; maxs = [wbbox(p)[1] for p in parts]
        mn = Vector([min(v[i] for v in mins) for i in range(3)]); mx = Vector([max(v[i] for v in maxs) for i in range(3)])
        ext = mx - mn
        run_x = ext.x > ext.y
        ctr = (mn + mx) / 2
        if run_x:
            size = (ext.x - 0.1, 0.02, ext.z - 0.1)
        else:
            size = (0.02, ext.y - 0.1, ext.z - 0.1)
        add_box("DET_Glas_" + key, ctr, size, glass)
    print("Fensterscheiben:", len(wins))


# ------------------------------------------------------------------ 2. Materialzuordnung
MAT_MAP = {
    "Wall_Interior": "wall_interior", "Wall_Exterior": "wall_exterior", "Roof_Tiles": "roof_tiles",
    "Door_Leaf": "door_leaf", "Door_Front": "door_front", "Frame_Window": "paint_white", "Frame_Door": "paint_white",
    "Kitchen_Sage": "kitchen_sage", "Counter_Oak": "counter_oak",
    "Wood_Dark": "wood_dark", "Wood_Medium": "wood_medium", "Wood_Light": "wood_light", "Beam_DarkWood": "wood_dark", "Pegboard_Wood": "wood_light",
    "Sofa_Floral_Gold": "sofa_floral", "Rug_Blue": "rug_blue", "Rug_Terra": "rug_terra", "Rug_Play": "rug_play", "Rug_Sage": "rug_play",
    "Terrace_Wood": "terrace_deck", "Porch_Wood": "terrace_deck", "Fence_Wood": "fence_wood",
    "Garden_Path": "paving_path", "Anna_Path_Stone": "paving_path", "Driveway_Stone": "paving_blocks", "Sidewalk_Gray": "paving_blocks",
    "Driveway_Border": "curb_granite", "Curb_Stone": "curb_granite", "Street_Asphalt": "asphalt",
    "Grass_Lawn": "grass_lawn", "Anna_Lawn_Green": "grass_lawn", "Meadow_Green": "meadow",
    "Hedge_Green": "foliage", "Hedge_LightGreen": "foliage", "Tree_Leaves": "foliage", "Anna_Tree_Foliage": "foliage", "Tree_Trunk": "bark",
    "Shed_Wood": "shed_wood", "Shed_Roof": "bitumen_roof", "Garage_Door_Panel": "garage_door", "Garage_Floor": "floor_garage",
    "Ben_Wall_Brick": "brick_red", "Anna_Roof_Slate": "slate_roof", "Ben_Roof_Dark": "bitumen_roof", "Anna_Wall_Mint": "plaster_mint",
    "Floor_Attic": "floor_dg_dachboden",
}
NAME_MAP = [  # (Regex auf Objektname, Textur) – gewinnt vor MAT_MAP; Raumböden einzeln
    (r"^EG_Boden_Flur$", "floor_eg_flur"), (r"^EG_Boden_Wohnzimmer$", "floor_eg_wohnzimmer"), (r"^EG_Boden_Kueche$", "floor_eg_kueche"),
    (r"^EG_Boden_Spielzimmer$", "floor_eg_spielzimmer"), (r"^EG_Boden_Gaesteklo$", "floor_eg_gaesteklo"),
    (r"^OG_Boden_Badezimmer$", "floor_og_bad"), (r"^OG_Boden_Elternzimmer$", "floor_og_eltern"), (r"^OG_Boden_Flur", "floor_og_flur"),
    (r"^OG_Boden_Kinderzimmer$", "floor_og_kinderzimmer"), (r"^DG_Boden", "floor_dg_dachboden"),
    (r"^(FL_Treppe_Stufe_\d+|OG_Dachbodentreppe_Stufe_\d+)$", "paint_white"),
    (r"^(FL_Treppe|OG_Dachbodentreppe)_(Tritt|Wange|Handlauf|Antrittspfosten|Stab)", "stair_wood"),
    (r"^Anna_Tree_(?!Crown)", "bark"),
]


def apply_materials():
    n = 0
    for o in bpy.data.objects:
        if o.type != "MESH" or o.name.startswith("DET_"):
            continue
        forced = next((t for rx, t in NAME_MAP if re.search(rx, o.name)), None)
        if o.data.users > 1:
            o.data = o.data.copy()
        for slot in o.material_slots:
            old = slot.material.name if slot.material else None
            tid = forced or MAT_MAP.get(old)
            if tid:
                tm = tex_mat(tid)
                if tm:
                    slot.material = tm; n += 1
    print("Materialien ersetzt:", n)


def split_ceiling_and_inside():
    """Decken (Unterseite der Stockwerksböden) und Innenseiten der Außenwände bekommen Innenputz statt Boden-/Fassadentextur."""
    wi = tex_mat("wall_interior")
    if not wi:
        return
    OUTV = {"Nord": Vector((0, 1, 0)), "Sued": Vector((0, -1, 0)), "Ost": Vector((1, 0, 0)), "West": Vector((-1, 0, 0))}
    n = 0
    for o in bpy.data.objects:
        if o.type != "MESH" or o.name.startswith("DET_"):
            continue
        floor = re.match(r"^(OG|DG)_Boden", o.name)
        wall = re.match(r"^(EG|OG)_Aussenwand_(Nord|Sued|Ost|West)_", o.name) or re.match(r"^(GAR)_Wand_(Nord|Sued|Ost|West)_", o.name)
        if not (floor or wall):
            continue
        if o.data.users > 1:
            o.data = o.data.copy()
        o.data.materials.append(wi)
        idx = len(o.data.materials) - 1
        N = o.matrix_world.to_3x3().inverted_safe().transposed()
        for p in o.data.polygons:
            wn = (N @ p.normal).normalized()
            cur = o.material_slots[p.material_index].material
            if floor and wn.z < -0.5:
                p.material_index = idx; n += 1
            elif wall and cur and cur.name == "TX_wall_exterior" and wn.dot(OUTV[wall.group(2)]) < -0.5:
                p.material_index = idx; n += 1
    print("Decken/Wandinnenseiten:", n, "Flächen")


# ------------------------------------------------------------------ 3. UV-Maps (Weltmaß, Box-Projektion)
def make_uvs():
    n_obj = 0
    for o in bpy.data.objects:
        if o.type != "MESH" or not o.data.polygons:
            continue
        if o.data.users > 1:
            o.data = o.data.copy()
        me = o.data
        bm = bmesh.new(); bm.from_mesh(me)
        uvl = bm.loops.layers.uv.get("UVMap") or bm.loops.layers.uv.new("UVMap")
        M = o.matrix_world; N = M.to_3x3().inverted_safe().transposed()
        slots = [s.material for s in o.material_slots]
        for f in bm.faces:
            mat = slots[f.material_index] if f.material_index < len(slots) else None
            tile = float(mat.get("tile", 1.0)) if mat else 1.0
            mode = mat.get("mode", "kachel") if mat else "kachel"
            n = (N @ f.normal).normalized()
            ax = max(range(3), key=lambda i: abs(n[i]))
            pts = [M @ l.vert.co for l in f.loops]
            if mode == "fit" and ax != 2:
                h = 1 - ax if ax in (0, 1) else 0          # waagerechte Achse der Fläche
                hs = [p[h] for p in pts]; zs = [p.z for p in pts]
                h0, h1, z0, z1 = min(hs), max(hs), min(zs), max(zs)
                for l, p in zip(f.loops, pts):
                    u = (p[h] - h0) / max(h1 - h0, 1e-6)
                    if n[ax] < 0: u = 1 - u
                    l[uvl].uv = (u, (p.z - z0) / max(z1 - z0, 1e-6))
                continue
            for l, p in zip(f.loops, pts):
                if ax == 2:
                    uv = (p.x, p.y)
                elif ax == 0:
                    uv = (p.y, p.z)
                else:
                    uv = (p.x, p.z)
                l[uvl].uv = (uv[0] / tile, uv[1] / tile)
        bm.to_mesh(me); bm.free()
        n_obj += 1
    print("UV-Maps:", n_obj, "Objekte")


def main():
    details()
    apply_materials()
    split_ceiling_and_inside()
    make_uvs()
    # Linien zarter (Kontur-Look bleibt, aber ohne schwarze Outlines)
    sc = bpy.context.scene
    try:
        ls = sc.view_layers[0].freestyle_settings.linesets[0].linestyle
        ls.color = (0.30, 0.24, 0.20); ls.thickness = 0.9
    except Exception:
        pass
    try:
        bpy.ops.file.make_paths_relative()
    except Exception:
        pass
    bpy.ops.wm.save_as_mainfile(filepath=OUT)
    print("Gespeichert:", OUT)


main()
