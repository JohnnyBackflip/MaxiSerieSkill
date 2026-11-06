#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gemeinsame Blender-Hilfsbibliothek für Maxis Welt (Blockout-Stil wie das Haus-Blockout):
  * Standardfiguren aus Primitiven (Maxi, Mama Katrin, Papa Thomas, Karl) mit einfachen Posen
  * Props (Pilzkorb, Pilze, Familienauto, BMX-Fahrrad, Pfanne, Teller, Bäume, Baumstumpf, Laub)
  * Welt/Sonne, Eevee+Freestyle-Renderkonfiguration, Kameras

Wird von den Build-Skripten per sys.path importiert (liegt im Korrekturmappen-Root).
"""
import math
import random

import bpy
from mathutils import Vector, Matrix

# ----------------------------------------------------------------------------- Basis

def get_collection(name, parent=None):
    col = bpy.data.collections.get(name)
    if col is None:
        col = bpy.data.collections.new(name)
        (parent or bpy.context.scene.collection).children.link(col)
    elif parent is not None and col.name not in [c.name for c in parent.children] and col.name not in [c.name for c in bpy.context.scene.collection.children]:
        parent.children.link(col)
    return col


def link(obj, col):
    for c in list(obj.users_collection):
        c.objects.unlink(obj)
    col.objects.link(obj)


def mat(name, rgba, rough=0.75):
    m = bpy.data.materials.get(name)
    if m is None:
        m = bpy.data.materials.new(name)
        m.use_nodes = True
        bsdf = m.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs["Base Color"].default_value = rgba
            bsdf.inputs["Roughness"].default_value = rough
        m.diffuse_color = rgba
    return m


def _finish(o, name, material, col, smooth=True):
    o.name = name
    if material is not None:
        o.data.materials.append(material)
    if smooth:
        for p in o.data.polygons:
            p.use_smooth = True
    link(o, col)
    return o


def box(name, center, size, material, col, rot_z=0.0, parent=None):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=center)
    o = bpy.context.active_object
    o.scale = (size[0], size[1], size[2])
    o.rotation_euler = (0, 0, rot_z)
    _finish(o, name, material, col, smooth=False)
    if parent is not None:
        o.parent = parent
    return o


def sphere(name, loc, r, material, col, scale=(1, 1, 1), parent=None):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc, segments=24, ring_count=16)
    o = bpy.context.active_object
    o.scale = scale
    _finish(o, name, material, col)
    if parent is not None:
        o.parent = parent
    return o


def cyl(name, loc, r, depth, material, col, rot=(0, 0, 0), scale=(1, 1, 1), parent=None, verts=24):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=depth, location=loc, vertices=verts)
    o = bpy.context.active_object
    o.rotation_euler = rot
    o.scale = scale
    _finish(o, name, material, col)
    if parent is not None:
        o.parent = parent
    return o


def cone(name, loc, r1, r2, depth, material, col, parent=None):
    bpy.ops.mesh.primitive_cone_add(radius1=r1, radius2=r2, depth=depth, location=loc, vertices=24)
    o = bpy.context.active_object
    _finish(o, name, material, col)
    if parent is not None:
        o.parent = parent
    return o


def torus(name, loc, major, minor, material, col, rot=(0, 0, 0), parent=None):
    bpy.ops.mesh.primitive_torus_add(major_radius=major, minor_radius=minor, location=loc, rotation=rot,
                                     major_segments=32, minor_segments=12)
    o = bpy.context.active_object
    _finish(o, name, material, col)
    if parent is not None:
        o.parent = parent
    return o


def cyl_between(name, a, b, r, material, col, parent=None):
    a, b = Vector(a), Vector(b)
    d = b - a
    L = max(d.length, 1e-4)
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=L, location=(a + b) / 2, vertices=20)
    o = bpy.context.active_object
    o.rotation_euler = d.to_track_quat('Z', 'Y').to_euler()
    _finish(o, name, material, col)
    if parent is not None:
        o.parent = parent
    return o


def empty(name, loc, rot_z_deg, col):
    e = bpy.data.objects.new(name, None)
    e.location = loc
    e.rotation_euler = (0, 0, math.radians(rot_z_deg))
    e.empty_display_size = 0.3
    col.objects.link(e)
    return e


def world_of(parent_empty, local):
    """Lokale Koordinate eines Parent-Empties in Weltkoordinaten (ohne Depsgraph-Update)."""
    M = Matrix.Translation(parent_empty.location) @ parent_empty.rotation_euler.to_matrix().to_4x4()
    return M @ Vector(local)


# ----------------------------------------------------------------------------- Figuren

FIGURES = {
    # h = Gesamthöhe, head = Kopfhöhe, shoulder = Schulterbreite; Farben = grobe Kleidungsfarben der Modelsheets
    "Papa_Thomas": dict(h=1.80, head=0.30, shoulder=0.46, skin=(0.93, 0.76, 0.62, 1), top=(0.42, 0.52, 0.25, 1),
                        pants=(0.22, 0.33, 0.55, 1), shoes=(0.40, 0.22, 0.10, 1), hair=(0.35, 0.20, 0.08, 1)),
    "Mama_Katrin": dict(h=1.68, head=0.29, shoulder=0.38, skin=(0.95, 0.80, 0.70, 1), top=(0.90, 0.68, 0.20, 1),
                        pants=(0.28, 0.40, 0.60, 1), shoes=(0.45, 0.25, 0.12, 1), hair=(0.40, 0.24, 0.10, 1), long_hair=True),
    "Maxi":        dict(h=1.06, head=0.28, shoulder=0.30, skin=(0.96, 0.80, 0.70, 1), top=(0.25, 0.50, 0.85, 1),
                        pants=(0.15, 0.20, 0.35, 1), shoes=(0.85, 0.12, 0.10, 1), hair=(0.45, 0.28, 0.12, 1)),
    "Karl":        dict(h=1.30, head=0.29, shoulder=0.34, skin=(0.94, 0.78, 0.66, 1), top=(0.91, 0.46, 0.12, 1),
                        pants=(0.25, 0.25, 0.28, 1), shoes=(0.08, 0.08, 0.08, 1), hair=(0.06, 0.05, 0.05, 1)),
    # seit Folge „Tante Frieda“ (2026-11-06): Puppenfarben türkis Anna, braun Opa, violett Frieda
    "Anna":        dict(h=1.06, head=0.28, shoulder=0.29, skin=(0.96, 0.80, 0.70, 1), top=(0.10, 0.62, 0.62, 1),
                        pants=(0.06, 0.45, 0.48, 1), shoes=(0.06, 0.45, 0.48, 1), hair=(0.62, 0.36, 0.14, 1), long_hair=True),
    "Opa_Heinrich": dict(h=1.74, head=0.30, shoulder=0.44, skin=(0.93, 0.76, 0.64, 1), top=(0.48, 0.30, 0.14, 1),
                        pants=(0.25, 0.25, 0.27, 1), shoes=(0.35, 0.20, 0.10, 1), hair=(0.80, 0.80, 0.80, 1)),
    "Tante_Frieda": dict(h=1.60, head=0.29, shoulder=0.36, skin=(0.95, 0.80, 0.72, 1), top=(0.48, 0.12, 0.42, 1),
                        pants=(0.45, 0.45, 0.47, 1), shoes=(0.06, 0.06, 0.06, 1), hair=(0.82, 0.82, 0.86, 1)),
}


def build_figure(key, origin, facing_deg, pose, col, seat_z=0.45, floor_z=0.0, suffix="", head_turn_deg=0.0, arms=None, mood=None):
    """
    Baut eine Standardfigur aus Primitiven.
      origin      : Bodenpunkt (x, y) – stehend: zwischen den Füßen; sitzend: Hüfte-Projektion; Hüfthöhe = seat_z
      facing_deg  : Blickrichtung (0 = +X, 90 = +Y)
      pose        : stand | walk | wave | point | kneel | crouch | sit | bike | hold_front | lift | hands_hip | stir
      seat_z      : Sitzflächen-Oberkante (für sit/bike)
      floor_z     : Bodenhöhe unter den Füßen (z. B. 0.62 im Auto)
    Rückgabe: dict mit Weltpositionen (hand_L, hand_R, head, head_top, hip)
    """
    p = FIGURES[key]
    tag = f"{key}{suffix}"
    h, head = p["h"], p["head"]
    f = Vector((math.cos(math.radians(facing_deg)), math.sin(math.radians(facing_deg)), 0))
    s = Vector((-f.y, f.x, 0))  # links der Figur
    up = Vector((0, 0, 1))
    O = Vector((origin[0], origin[1], floor_z))

    m_skin, m_top, m_pants, m_shoes, m_hair = (mat(f"MAT_Fig_{key}_{k}", p[k]) for k in ("skin", "top", "pants", "shoes", "hair"))
    m_eye = mat("MAT_Fig_Auge", (0.05, 0.03, 0.02, 1))

    leg_len = h * 0.47
    torso_len = h * 0.33
    neck = h * 0.03
    sh_w = p["shoulder"]
    r_leg, r_arm, r_torso = h * 0.045, h * 0.035, sh_w * 0.42
    arm_len = h * 0.36

    def leg(nm, hp, knee, foot):
        cyl_between(f"FIG_{tag}_Oberschenkel_{nm}", hp, knee, r_leg, m_pants, col)
        cyl_between(f"FIG_{tag}_Unterschenkel_{nm}", knee, foot, r_leg * 0.9, m_pants, col)
        sphere(f"FIG_{tag}_Knie_{nm}", knee, r_leg * 0.95, m_pants, col)

    def shoe(nm, foot, direction):
        sphere(f"FIG_{tag}_Schuh_{nm}", foot + direction * 0.05, r_leg * 1.1, m_shoes, col, scale=(1.5, 1.5, 0.6))

    # ---- Beine
    if pose in ("sit",):
        thigh, shin = leg_len * 0.52, leg_len * 0.48
        hip = Vector((O.x, O.y, seat_z + r_leg))
        for sign, nm in ((1, "L"), (-1, "R")):
            hp = hip + s * (sign * sh_w * 0.25)
            knee = hp + f * thigh
            foot = Vector((knee.x, knee.y, floor_z + r_leg))
            if (knee.z - foot.z) > shin:  # Füße baumeln (hoher Sitz) -> Unterschenkel hängt
                foot = knee - up * shin
            leg(nm, hp, knee, foot)
            shoe(nm, foot, f)
    elif pose == "bike":
        thigh, shin = leg_len * 0.52, leg_len * 0.48
        hip = Vector((O.x, O.y, seat_z + r_leg))
        for sign, nm, ped in ((1, "L", 0.12), (-1, "R", -0.12)):
            hp = hip + s * (sign * sh_w * 0.25)
            knee = hp + f * (thigh * 0.75) - up * (thigh * 0.45)
            foot = Vector((hp.x, hp.y, 0)) + f * 0.12 + up * (floor_z + 0.28 + ped)
            leg(nm, hp, knee, foot)
            shoe(nm, foot, f)
    elif pose == "kneel":
        thigh, shin = leg_len * 0.52, leg_len * 0.48
        hip = O + up * (thigh + r_leg)  # Oberschenkel senkrecht, Unterschenkel liegen hinten am Boden
        for sign, nm in ((1, "L"), (-1, "R")):
            hp = hip + s * (sign * sh_w * 0.22)
            knee = Vector((hp.x, hp.y, floor_z + r_leg))
            foot = knee - f * shin
            leg(nm, hp, knee, foot)
            shoe(nm, foot, -f)
    elif pose == "crouch":
        thigh, shin = leg_len * 0.52, leg_len * 0.48
        hip = O + up * (shin * 0.75 + r_leg) - f * (thigh * 0.5)
        for sign, nm in ((1, "L"), (-1, "R")):
            hp = hip + s * (sign * sh_w * 0.25)
            knee = hp + f * thigh * 0.95 + up * (thigh * 0.25)
            foot = Vector((knee.x, knee.y, floor_z + r_leg)) - f * 0.1
            leg(nm, hp, knee, foot)
            shoe(nm, foot, f)
    elif pose == "lie":      # liegend auf dem Rücken, Kopf in Blickrichtung f, Beine entgegen
        thigh, shin = leg_len * 0.52, leg_len * 0.48
        hip = Vector((O.x, O.y, floor_z + r_leg * 1.3))
        for sign, nm in ((1, "L"), (-1, "R")):
            hp = hip + s * (sign * sh_w * 0.22)
            knee = hp - f * thigh
            foot = knee - f * shin
            leg(nm, hp, knee, foot)
            shoe(nm, foot, -f)
    else:  # stand / walk / wave / point / hold_front / lift / hands_hip / stir
        hip = O + up * leg_len
        for sign, nm in ((1, "L"), (-1, "R")):
            hp = hip + s * (sign * sh_w * 0.22)
            stride = f * (sign * 0.14) if pose == "walk" else Vector((0, 0, 0))
            foot = Vector((hp.x, hp.y, floor_z + r_leg)) + stride
            knee = (hp + foot) / 2 + (f * 0.04 if pose == "walk" and sign > 0 else Vector((0, 0, 0)))
            leg(nm, hp, knee, foot)
            shoe(nm, foot, f)

    # ---- Rumpf
    shoulder_c = hip + up * torso_len
    if pose in ("crouch", "kneel") or pose == "bike":
        shoulder_c = hip + up * (torso_len * 0.92) + f * (torso_len * 0.3)
    if pose == "lie":
        shoulder_c = hip + f * torso_len + up * 0.10
    cyl_between(f"FIG_{tag}_Rumpf", hip, shoulder_c, r_torso, m_top, col)
    sphere(f"FIG_{tag}_Schulterkugel", shoulder_c, r_torso, m_top, col, scale=(1, 1, 0.6))
    sphere(f"FIG_{tag}_Hueftkugel", hip, r_torso * 0.95, m_pants, col, scale=(1, 1, 0.6))

    # ---- Arme (arms überschreibt die Armhaltung der Pose, z. B. sitzend + lift)
    hands = {}
    leg_pose = pose
    pose = arms or pose
    for sign, nm in ((1, "L"), (-1, "R")):
        sp = shoulder_c + s * (sign * sh_w * 0.5)
        if pose == "wave" and nm == "R":
            elbow = sp + up * (arm_len * 0.45) + s * (sign * arm_len * 0.25)
            hand = elbow + up * (arm_len * 0.5) + s * (sign * arm_len * 0.1)
        elif pose == "open":       # Arme weit auseinander (Begrüßung)
            elbow = sp + s * (sign * arm_len * 0.50) + f * (arm_len * 0.18) - up * (arm_len * 0.12)
            hand = elbow + s * (sign * arm_len * 0.46) + f * (arm_len * 0.28) - up * (arm_len * 0.03)
        elif pose == "sip" and nm == "R":   # Ellbogen auf dem Tisch, Tasse am Mund
            elbow = sp + f * (arm_len * 0.30) - up * (arm_len * 0.30)
            hand = elbow + up * (arm_len * 0.50) - f * (arm_len * 0.10)
        elif pose == "face":       # Hände vors Gesicht
            elbow = sp - up * (arm_len * 0.05) + f * (arm_len * 0.30) + s * (sign * arm_len * 0.22)
            hand = elbow + up * (arm_len * 0.42) - f * (arm_len * 0.02) - s * (sign * arm_len * 0.20)
        elif pose == "point_down" and nm == "R":
            elbow = sp + f * (arm_len * 0.4) - up * (arm_len * 0.35)
            hand = elbow + f * (arm_len * 0.45) - up * (arm_len * 0.4)
        elif pose == "point" and nm == "R":
            elbow = sp + f * (arm_len * 0.45) + up * (arm_len * 0.1)
            hand = elbow + f * (arm_len * 0.5) + up * (arm_len * 0.15)
        elif pose == "lift":
            elbow = sp + up * (arm_len * 0.4) + f * (arm_len * 0.25)
            hand = elbow + up * (arm_len * 0.45) + f * (arm_len * 0.05) - s * (sign * 0.03)
        elif pose in ("hold_front", "stir"):
            elbow = sp - up * (arm_len * 0.45) + f * (arm_len * 0.15)
            hand = elbow + f * (arm_len * 0.45) - s * (sign * sh_w * 0.15)
            if pose == "stir":
                hand = elbow + f * (arm_len * 0.4) + up * (arm_len * 0.15)
        elif pose == "hands_hip":
            elbow = sp - up * (arm_len * 0.4) + s * (sign * arm_len * 0.3)
            hand = hip + s * (sign * r_torso * 1.05) + up * 0.05
        elif pose == "bike":
            elbow = sp + f * (arm_len * 0.4) - up * (arm_len * 0.2)
            hand = elbow + f * (arm_len * 0.4) - up * (arm_len * 0.15) + s * (sign * 0.05)
        elif pose in ("sit",):
            elbow = sp - up * (arm_len * 0.5)
            hand = elbow + f * (arm_len * 0.5)
        elif pose in ("kneel", "crouch"):
            elbow = sp - up * (arm_len * 0.35) + f * (arm_len * 0.3)
            hand = elbow - up * (arm_len * 0.3) + f * (arm_len * 0.35)
        elif pose == "walk":
            swing = f * (sign * 0.12)
            elbow = sp - up * (arm_len * 0.5) + swing * 0.6
            hand = elbow - up * (arm_len * 0.45) + swing
        else:
            elbow = sp - up * (arm_len * 0.5) + s * (sign * 0.03)
            hand = elbow - up * (arm_len * 0.5) + s * (sign * 0.03)
        cyl_between(f"FIG_{tag}_Oberarm_{nm}", sp, elbow, r_arm, m_top, col)
        cyl_between(f"FIG_{tag}_Unterarm_{nm}", elbow, hand, r_arm * 0.9, m_skin, col)
        sphere(f"FIG_{tag}_Hand_{nm}", hand, r_arm * 1.15, m_skin, col)
        hands[nm] = hand

    pose = leg_pose
    # ---- Hals & Kopf
    lie = (leg_pose == "lie")
    neck_top = shoulder_c + (f if lie else up) * (neck + r_torso * 0.3)
    cyl_between(f"FIG_{tag}_Hals", shoulder_c, neck_top, r_arm, m_skin, col)
    head_c = neck_top + (f if lie else up) * (head * 0.5)
    hf = f
    if head_turn_deg:
        a = math.radians(facing_deg + head_turn_deg)
        hf = Vector((math.cos(a), math.sin(a), 0))
    hs = Vector((-hf.y, hf.x, 0))
    if lie:                          # liegend: Gesicht zur Decke
        hf = up; hs = s
    sphere(f"FIG_{tag}_Kopf", head_c, head * 0.5, m_skin, col, scale=(0.9, 0.9, 1.0))
    sphere(f"FIG_{tag}_Haare", head_c + up * (head * 0.1) - hf * (head * 0.08), head * 0.5 * 1.02, m_hair, col, scale=(0.9, 0.9, 0.8))
    if p.get("long_hair"):
        cyl_between(f"FIG_{tag}_Haare_Lang", head_c - hf * (head * 0.3), head_c - hf * (head * 0.3) - up * (head * 1.0), head * 0.3, m_hair, col)
    for sign, nm in ((1, "L"), (-1, "R")):
        sphere(f"FIG_{tag}_Auge_{nm}", head_c + hf * (head * 0.42) + hs * (sign * head * 0.17) + up * (head * 0.05), head * 0.05, m_eye, col)
    if mood and not lie:             # Augenbrauen: angry | startled | suspicious | sad
        for sign, nm in ((1, "L"), (-1, "R")):
            def P(side, dy):
                return head_c + hf * (head * 0.43) + hs * (sign * head * side) + up * (head * (0.15 + dy))
            do, di = {"angry": (0.03, -0.04), "startled": (0.09, 0.09), "sad": (-0.02, 0.06)}.get(mood, (0.0, 0.0))
            if mood == "suspicious":
                do = di = (0.08 if sign > 0 else -0.03)
            cyl_between(f"FIG_{tag}_Braue_{nm}", P(0.32, do), P(0.06, di), head * 0.020, m_hair, col)
    return dict(hand_L=hands["L"], hand_R=hands["R"], head=head_c, head_top=head_c + up * (head * 0.5), hip=hip, shoulder=shoulder_c)


# ----------------------------------------------------------------------------- Props

def prop_basket(name, loc, facing_deg, col, full=False, tilt_deg=0.0):
    """Ovaler Weidenkorb mit Bügel. loc = Korbboden-Mitte."""
    m_w = mat("MAT_Korb_Weide", (0.62, 0.42, 0.20, 1))
    e = empty(name, loc, facing_deg, col)
    e.rotation_euler = (math.radians(tilt_deg), 0, math.radians(facing_deg))
    cyl(f"{name}_Korb", (0, 0, 0.09), 0.17, 0.18, m_w, col, scale=(1.25, 0.9, 1.0), parent=e)
    torus(f"{name}_Buegel", (0, 0, 0.18), 0.19, 0.012, m_w, col, rot=(math.radians(90), 0, 0), parent=e)
    if full:
        m_cap = mat("MAT_Pilz_Steinpilz_Hut", (0.50, 0.30, 0.13, 1))
        m_pf = mat("MAT_Pilz_Pfifferling", (0.95, 0.70, 0.18, 1))
        for i, (x, y, r, m) in enumerate([(-0.08, 0.02, 0.06, m_cap), (0.06, -0.03, 0.055, m_cap), (0.0, 0.06, 0.04, m_pf), (0.1, 0.05, 0.035, m_pf), (-0.02, -0.06, 0.045, m_cap)]):
            sphere(f"{name}_Inhalt_{i}", (x, y, 0.17), r, m, col, scale=(1, 1, 0.6), parent=e)
    return e


def prop_mushroom(name, loc, col, kind="steinpilz", h=0.15, rot_deg=0.0):
    if kind == "steinpilz":
        m_cap, m_stem = mat("MAT_Pilz_Steinpilz_Hut", (0.50, 0.30, 0.13, 1)), mat("MAT_Pilz_Stiel", (0.92, 0.86, 0.72, 1))
        cyl(f"{name}_Stiel", (loc[0], loc[1], loc[2] + h * 0.35), h * 0.18, h * 0.7, m_stem, col)
        sphere(f"{name}_Hut", (loc[0], loc[1], loc[2] + h * 0.72), h * 0.42, m_cap, col, scale=(1, 1, 0.65))
    elif kind == "knollenblaetterpilz":
        m_cap, m_stem = mat("MAT_Pilz_Knollen_Hut", (0.80, 0.82, 0.64, 1)), mat("MAT_Pilz_Knollen_Stiel", (0.95, 0.95, 0.90, 1))
        cyl(f"{name}_Stiel", (loc[0], loc[1], loc[2] + h * 0.45), h * 0.09, h * 0.9, m_stem, col)
        sphere(f"{name}_Knolle", (loc[0], loc[1], loc[2] + h * 0.08), h * 0.16, m_stem, col)
        torus(f"{name}_Ring", (loc[0], loc[1], loc[2] + h * 0.68), h * 0.13, h * 0.03, m_stem, col)
        sphere(f"{name}_Hut", (loc[0], loc[1], loc[2] + h * 0.9), h * 0.38, m_cap, col, scale=(1, 1, 0.4))
    elif kind == "pfifferlinge":
        m_pf = mat("MAT_Pilz_Pfifferling", (0.95, 0.70, 0.18, 1))
        m_moos = mat("MAT_Moos", (0.30, 0.52, 0.22, 1))
        sphere(f"{name}_Moos", (loc[0], loc[1], loc[2]), 0.22, m_moos, col, scale=(1.3, 1.0, 0.3))
        rnd = random.Random(7)
        for i in range(6):
            dx, dy = rnd.uniform(-0.12, 0.12), rnd.uniform(-0.08, 0.08)
            hh = rnd.uniform(0.05, 0.08)
            cone(f"{name}_Pf_{i}", (loc[0] + dx, loc[1] + dy, loc[2] + 0.04 + hh / 2), 0.012, 0.035, hh, m_pf, col)


def prop_car(name, loc, facing_deg, col, door_open=None, color=(0.16, 0.40, 0.72, 1)):
    """Blauer Kombi als offenes Blockout (Chassis, Haube, Heck, Seitenwände, Dach auf Säulen, Sitze, Räder).
    Lokal: +X = vorn. door_open = 'FR' | 'RR' | 'FL' | 'RL' (geöffnete Tür). Rückgabe: Empty + Sitzpositionen (Welt)."""
    m_body = mat("MAT_Auto_Blau", color)
    m_dark = mat("MAT_Auto_Dunkel", (0.12, 0.12, 0.13, 1))
    m_glass = mat("MAT_Auto_Glas", (0.75, 0.85, 0.92, 1))
    m_seat = mat("MAT_Auto_Sitz", (0.35, 0.35, 0.38, 1))
    m_light = mat("MAT_Auto_Licht", (1.0, 0.95, 0.75, 1))
    m_chrome = mat("MAT_Auto_Chrom", (0.80, 0.82, 0.85, 1))
    e = empty(name, loc, facing_deg, col)
    box(f"{name}_Chassis", (0, 0, 0.47), (4.4, 1.8, 0.30), m_body, col, parent=e)
    box(f"{name}_Haube", (1.65, 0, 0.78), (1.1, 1.78, 0.32), m_body, col, parent=e)
    box(f"{name}_Heck", (-1.95, 0, 0.82), (0.5, 1.78, 0.40), m_body, col, parent=e)
    box(f"{name}_Windschutz", (1.0, 0, 1.22), (0.06, 1.6, 0.6), m_glass, col, parent=e)
    box(f"{name}_Dach", (-0.35, 0, 1.52), (2.7, 1.76, 0.07), m_body, col, parent=e)
    doors = {"FL": (0.35, 0.86), "FR": (0.35, -0.86), "RL": (-0.95, 0.86), "RR": (-0.95, -0.86)}
    for key, (dx, dy) in doors.items():
        if door_open == key:
            hinge_x = dx + 0.6
            a = math.radians(65)
            side = 1 if dy > 0 else -1
            cx = hinge_x - 0.6 * math.cos(a)
            cy = dy + side * 0.6 * math.sin(a)
            box(f"{name}_Tuer_{key}", (cx, cy, 0.80), (1.2, 0.07, 0.36), m_body, col, rot_z=-side * a, parent=e)
            box(f"{name}_Tuerfenster_{key}", (cx, cy, 1.20), (1.2, 0.04, 0.45), m_glass, col, rot_z=-side * a, parent=e)
        else:
            box(f"{name}_Tuer_{key}", (dx, dy, 0.80), (1.2, 0.07, 0.36), m_body, col, parent=e)
    # Säulen
    for x in (1.0, -0.25, -1.6):
        for y in (0.84, -0.84):
            box(f"{name}_Saeule_{x}_{y}", (x, y, 1.25), (0.08, 0.08, 0.6), m_body, col, parent=e)
    # Sitze (Oberkante Sitzfläche z=0.76, Boden z=0.62)
    for key, (sx, sy, w) in {"VL": (0.2, 0.42, 0.5), "VR": (0.2, -0.42, 0.5), "H": (-1.0, 0.0, 1.5)}.items():
        box(f"{name}_Sitz_{key}", (sx, sy, 0.69), (0.5, w, 0.14), m_seat, col, parent=e)
        box(f"{name}_Lehne_{key}", (sx - 0.28, sy, 1.0), (0.12, w, 0.55), m_seat, col, parent=e)
    box(f"{name}_Lenkrad", (0.62, -0.42, 1.0), (0.04, 0.34, 0.34), m_dark, col, parent=e)
    for x in (1.4, -1.4):
        for y in (0.85, -0.85):
            cyl(f"{name}_Rad_{x}_{y}", (x, y, 0.33), 0.33, 0.22, m_dark, col, rot=(math.radians(90), 0, 0), parent=e)
            cyl(f"{name}_Radkappe_{x}_{y}", (x, y * 1.06, 0.33), 0.18, 0.1, m_chrome, col, rot=(math.radians(90), 0, 0), parent=e)
    for y in (0.6, -0.6):
        sphere(f"{name}_Scheinwerfer_{y}", (2.2, y, 0.75), 0.13, m_light, col, parent=e)
    box(f"{name}_Grill", (2.2, 0, 0.6), (0.06, 0.8, 0.18), m_chrome, col, parent=e)
    seats = {k: world_of(e, (v[0], v[1], 0.76)) for k, v in {"VL": (0.2, 0.42), "VR": (0.2, -0.42), "HL": (-1.0, 0.42), "HR": (-1.0, -0.42)}.items()}
    return e, seats


def prop_bike(name, loc, facing_deg, col):
    """Schwarz-oranges BMX. Lokal +X = Fahrtrichtung. Rückgabe: Empty, Sattel-Weltposition (Oberkante), Lenker-Weltposition."""
    m_blk = mat("MAT_Rad_Schwarz", (0.10, 0.10, 0.10, 1))
    m_org = mat("MAT_Rad_Orange", (0.91, 0.46, 0.12, 1))
    e = empty(name, loc, facing_deg, col)
    for x in (0.52, -0.52):
        torus(f"{name}_Rad_{x}", (x, 0, 0.26), 0.23, 0.035, m_blk, col, rot=(math.radians(90), 0, 0), parent=e)
    cyl_between(f"{name}_Rahmen_1", (-0.52, 0, 0.26), (0.0, 0, 0.72), 0.025, m_blk, col, parent=e)
    cyl_between(f"{name}_Rahmen_2", (0.0, 0, 0.72), (0.45, 0, 0.78), 0.025, m_blk, col, parent=e)
    cyl_between(f"{name}_Rahmen_3", (0.1, 0, 0.3), (0.45, 0, 0.78), 0.025, m_blk, col, parent=e)
    cyl_between(f"{name}_Rahmen_4", (0.1, 0, 0.3), (0.0, 0, 0.72), 0.025, m_blk, col, parent=e)
    cyl_between(f"{name}_Gabel", (0.45, 0, 0.78), (0.52, 0, 0.26), 0.02, m_org, col, parent=e)
    cyl_between(f"{name}_Lenkerstange", (0.45, 0, 0.78), (0.42, 0, 0.98), 0.02, m_blk, col, parent=e)
    cyl(f"{name}_Lenker", (0.42, 0, 0.98), 0.018, 0.55, m_org, col, rot=(math.radians(90), 0, 0), parent=e)
    box(f"{name}_Sattel", (-0.05, 0, 0.76), (0.24, 0.12, 0.05), m_org, col, parent=e)
    cyl(f"{name}_Tretlager", (0.1, 0, 0.3), 0.06, 0.1, m_blk, col, rot=(math.radians(90), 0, 0), parent=e)
    for y, dz in ((0.12, 0.1), (-0.12, -0.1)):
        box(f"{name}_Pedal_{y}", (0.1, y, 0.3 + dz), (0.1, 0.06, 0.03), m_org, col, parent=e)
    return e, world_of(e, (-0.05, 0, 0.785)), world_of(e, (0.42, 0, 0.98))


def prop_pan(name, loc, col):
    m_pan = mat("MAT_Pfanne", (0.15, 0.15, 0.15, 1))
    m_sauce = mat("MAT_Sauce", (0.92, 0.86, 0.72, 1))
    m_wood = mat("MAT_Holz_Hell", (0.76, 0.58, 0.36, 1))
    cyl(f"{name}_Pfanne", (loc[0], loc[1], loc[2] + 0.03), 0.14, 0.06, m_pan, col)
    cyl(f"{name}_Sauce", (loc[0], loc[1], loc[2] + 0.055), 0.125, 0.015, m_sauce, col)
    cyl(f"{name}_Griff", (loc[0] - 0.22, loc[1], loc[2] + 0.05), 0.015, 0.2, m_wood, col, rot=(0, math.radians(90), 0))


def prop_plate(name, loc, col):
    m_plate = mat("MAT_Teller", (0.95, 0.93, 0.88, 1))
    m_noodle = mat("MAT_Nudeln", (0.95, 0.80, 0.40, 1))
    m_sauce = mat("MAT_Sauce", (0.92, 0.86, 0.72, 1))
    cyl(f"{name}_Teller", (loc[0], loc[1], loc[2] + 0.01), 0.13, 0.02, m_plate, col)
    sphere(f"{name}_Nudeln", (loc[0], loc[1], loc[2] + 0.03), 0.09, m_noodle, col, scale=(1, 1, 0.4))
    sphere(f"{name}_Sauce", (loc[0], loc[1], loc[2] + 0.055), 0.06, m_sauce, col, scale=(1, 1, 0.35))


def prop_tree(name, loc, col, h=7.0, kind="round", crown=(0.85, 0.45, 0.12, 1), trunk_r=0.28, seed=0):
    m_trunk = mat("MAT_Baum_Stamm", (0.36, 0.25, 0.15, 1))
    m_crown = mat(f"MAT_Laub_{int(crown[0]*100)}_{int(crown[1]*100)}_{int(crown[2]*100)}", crown)
    rnd = random.Random(seed)
    cyl(f"{name}_Stamm", (loc[0], loc[1], loc[2] + h * 0.4), trunk_r, h * 0.8, m_trunk, col, verts=12)
    if kind == "round":
        for i in range(3):
            dx, dy, dz = rnd.uniform(-0.6, 0.6), rnd.uniform(-0.6, 0.6), rnd.uniform(-0.3, 0.4)
            sphere(f"{name}_Krone_{i}", (loc[0] + dx, loc[1] + dy, loc[2] + h * 0.72 + dz), h * 0.26, m_crown, col)
    else:  # Nadelbaum
        m_fir = mat("MAT_Nadel_Dunkelgruen", (0.14, 0.32, 0.18, 1))
        for i, (rr, zz) in enumerate([(h * 0.26, h * 0.45), (h * 0.21, h * 0.65), (h * 0.14, h * 0.85)]):
            cone(f"{name}_Krone_{i}", (loc[0], loc[1], loc[2] + zz), rr, 0.0, h * 0.32, m_fir, col)


def prop_stump(name, loc, col, r=0.35, h=0.45):
    m_trunk = mat("MAT_Baum_Stamm", (0.36, 0.25, 0.15, 1))
    m_cut = mat("MAT_Holz_Schnitt", (0.80, 0.66, 0.42, 1))
    m_moos = mat("MAT_Moos", (0.30, 0.52, 0.22, 1))
    cyl(f"{name}_Stumpf", (loc[0], loc[1], loc[2] + h / 2), r, h, m_trunk, col)
    cyl(f"{name}_Schnitt", (loc[0], loc[1], loc[2] + h + 0.01), r * 0.96, 0.02, m_cut, col)
    sphere(f"{name}_Moos", (loc[0] + r * 0.6, loc[1] - r * 0.4, loc[2] + h * 0.5), r * 0.5, m_moos, col, scale=(1, 1, 1.4))


def scatter_leaves(name, col, x_range, y_range, n=200, seed=1, z=0.012):
    cols = [(0.90, 0.55, 0.12, 1), (0.95, 0.75, 0.15, 1), (0.70, 0.25, 0.10, 1), (0.60, 0.40, 0.15, 1)]
    rnd = random.Random(seed)
    mats = [mat(f"MAT_Blatt_{i}", c) for i, c in enumerate(cols)]
    for i in range(n):
        x, y = rnd.uniform(*x_range), rnd.uniform(*y_range)
        o = cyl(f"{name}_{i}", (x, y, z), rnd.uniform(0.08, 0.16), 0.01, mats[rnd.randrange(4)], col,
                rot=(0, 0, rnd.uniform(0, 3.14)), scale=(1.0, 0.65, 1.0), verts=8)


# ----------------------------------------------------------------------------- Welt / Render / Kamera

def setup_world_and_sun(col, sky=(0.78, 0.86, 0.95, 1.0), strength=0.85):
    scene = bpy.context.scene
    world = bpy.data.worlds.get("BlockoutWorld") or bpy.data.worlds.new("BlockoutWorld")
    world.use_nodes = True
    scene.world = world
    bg = world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs[0].default_value = sky
        bg.inputs[1].default_value = strength
    for nm, energy, rot in (("Sun_Main", 2.8, (48, 18, -35)), ("Sun_Fill", 1.2, (55, -25, 145))):
        if bpy.data.objects.get(nm):
            continue
        ld = bpy.data.lights.new(name=nm, type='SUN')
        ld.energy, ld.color, ld.angle = energy, (1.0, 0.97, 0.90), math.radians(15.0)
        lo = bpy.data.objects.new(nm, ld)
        lo.rotation_euler = tuple(math.radians(a) for a in rot)
        col.objects.link(lo)


def configure_render(w=1600, h=1000):
    scene = bpy.context.scene
    scene.render.engine = 'BLENDER_EEVEE'
    scene.render.resolution_x, scene.render.resolution_y = w, h
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    if hasattr(scene.eevee, "taa_render_samples"):
        scene.eevee.taa_render_samples = 16
    scene.render.use_freestyle = True
    scene.render.line_thickness = 1.45
    vl = scene.view_layers[0]
    vl.use_freestyle = True
    fs = vl.freestyle_settings
    fs.crease_angle = math.radians(134.0)
    ls = fs.linesets.new("BlockoutEdges") if len(fs.linesets) == 0 else fs.linesets[0]
    if ls.linestyle is None:
        ls.linestyle = bpy.data.linestyles.new("BlockoutLineStyle")
    ls.select_silhouette = ls.select_border = ls.select_crease = ls.select_contour = ls.select_external_contour = True
    ls.linestyle.color = (0.10, 0.08, 0.07)
    ls.linestyle.thickness = 1.45


def add_camera(name, loc, target, lens, col):
    old = bpy.data.objects.get(name)
    if old:
        bpy.data.objects.remove(old, do_unlink=True)
    cd = bpy.data.cameras.new(name)
    cd.lens, cd.clip_start, cd.clip_end = lens, 0.08, 400.0
    co = bpy.data.objects.new(name, cd)
    co.location = Vector(loc)
    co.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler()
    col.objects.link(co)
    return co


def render_camera(cam, path):
    scene = bpy.context.scene
    scene.camera = cam
    scene.render.filepath = path
    bpy.ops.render.render(write_still=True)
    print("Gerendert:", path)


# ----------------------------------------------------------------------------- Props Folge „Tante Frieda“ (2026-11-06)

def prop_hasi(name, loc, col, facing_deg=0.0, scale=1.0):
    """Maxis Kuschelhase (hellgrau, ca. 30 cm). loc = Unterkante Körpermitte."""
    m = mat("MAT_Hasi", (0.86, 0.86, 0.88, 1)); m_in = mat("MAT_Hasi_Ohr_Innen", (0.95, 0.70, 0.75, 1))
    e = empty(name, loc, facing_deg, col); e.scale = (scale, scale, scale)
    sphere(f"{name}_Koerper", (0, 0, 0.09), 0.08, m, col, scale=(0.9, 0.8, 1.1), parent=e)
    sphere(f"{name}_Kopf", (0, 0, 0.21), 0.065, m, col, parent=e)
    for sgn, nm in ((1, "L"), (-1, "R")):
        sphere(f"{name}_Ohr_{nm}", (0, sgn * 0.03, 0.31), 0.022, m_in, col, scale=(0.8, 1, 3.2), parent=e)
    return e


def prop_dog(name, loc, facing_deg, col):
    """Beagle Bello (braun/weiß/schwarz, Schulterhöhe ca. 38 cm). loc = Bodenpunkt Körpermitte."""
    m_b = mat("MAT_Bello_Braun", (0.62, 0.38, 0.16, 1)); m_w = mat("MAT_Bello_Weiss", (0.95, 0.93, 0.90, 1))
    m_k = mat("MAT_Bello_Schwarz", (0.08, 0.07, 0.07, 1))
    e = empty(name, loc, facing_deg, col)
    sphere(f"{name}_Rumpf", (0, 0, 0.30), 0.13, m_b, col, scale=(1.9, 1.0, 0.95), parent=e)
    sphere(f"{name}_Sattel", (-0.04, 0, 0.38), 0.10, m_k, col, scale=(1.5, 1.0, 0.5), parent=e)
    for x in (0.16, -0.16):
        for y in (0.07, -0.07):
            cyl(f"{name}_Bein_{x}_{y}", (x, y, 0.12), 0.03, 0.24, m_w, col, parent=e)
    sphere(f"{name}_Kopf", (0.30, 0, 0.46), 0.09, m_b, col, scale=(1.2, 0.9, 0.95), parent=e)
    sphere(f"{name}_Schnauze", (0.40, 0, 0.42), 0.05, m_w, col, scale=(1.3, 1, 0.8), parent=e)
    for y in (0.08, -0.08):
        sphere(f"{name}_Ohr_{y}", (0.28, y, 0.40), 0.04, m_b, col, scale=(0.6, 0.4, 1.8), parent=e)
    cyl(f"{name}_Rute", (-0.28, 0, 0.42), 0.015, 0.16, m_w, col, rot=(0, math.radians(-35), 0), parent=e)
    return e


def prop_parrot(name, loc, col, facing_deg=0.0, wet=False, wings_open=False, scale=1.0):
    """Papagei Lorchen, Amazone (grün, gelbe Stirn, rote Flügelflecken, große Augen, Hakenschnabel), ca. 42 cm. loc = Fußpunkt."""
    g = (0.10, 0.42, 0.10, 1) if wet else (0.18, 0.62, 0.14, 1)
    m_g = mat("MAT_Lorchen_Gruen" + ("_nass" if wet else ""), g); m_y = mat("MAT_Lorchen_Gelb", (0.98, 0.85, 0.10, 1))
    m_r = mat("MAT_Lorchen_Rot", (0.85, 0.12, 0.10, 1)); m_s = mat("MAT_Lorchen_Schnabel", (0.88, 0.82, 0.68, 1))
    m_w = mat("MAT_Lorchen_AugeWeiss", (0.98, 0.98, 0.96, 1)); m_k = mat("MAT_Lorchen_Pupille", (0.03, 0.02, 0.02, 1))
    m_f = mat("MAT_Lorchen_Fuss", (0.45, 0.45, 0.47, 1))
    e = empty(name, loc, facing_deg, col); e.scale = (scale, scale, scale)
    k = 1.18 if wet else 1.0                      # nass = plustrig
    sphere(f"{name}_Rumpf", (0, 0, 0.19), 0.10, m_g, col, scale=(0.9 * k, 0.8 * k, 1.5 * k), parent=e)
    sphere(f"{name}_Brust", (0.05, 0, 0.17), 0.07, mat("MAT_Lorchen_Brust", (0.40, 0.75, 0.25, 1)), col, scale=(0.8, 0.9, 1.4), parent=e)
    sphere(f"{name}_Kopf", (0.025, 0, 0.385), 0.078, m_g, col, scale=(1.0 * k, 1.0 * k, 1.0 * k), parent=e)
    sphere(f"{name}_Stirn", (0.06, 0, 0.44), 0.05, m_y, col, scale=(1.0, 1.1, 0.6), parent=e)
    for sg in (1, -1):
        sphere(f"{name}_Wange_{sg}", (0.07, sg * 0.05, 0.37), 0.03, m_y, col, scale=(1, 0.5, 1), parent=e)
        sphere(f"{name}_AugeW_{sg}", (0.085, sg * 0.05, 0.40), 0.024, m_w, col, parent=e)
        sphere(f"{name}_AugeP_{sg}", (0.103, sg * 0.052, 0.40), 0.013, m_k, col, parent=e)
    sphere(f"{name}_SchnabelO", (0.125, 0, 0.365), 0.04, m_s, col, scale=(1.35, 0.9, 1.15), parent=e)
    sphere(f"{name}_SchnabelU", (0.115, 0, 0.335), 0.025, m_s, col, scale=(1.2, 0.9, 0.8), parent=e)
    for sg in (1, -1):
        if wings_open:
            sphere(f"{name}_Fluegel_{sg}", (0, sg * 0.24, 0.24), 0.07, m_g, col, scale=(1.1, 3.4, 0.35), parent=e)
            sphere(f"{name}_Spiegel_{sg}", (0.01, sg * 0.20, 0.26), 0.03, m_r, col, scale=(1, 1.6, 0.5), parent=e)
        else:
            sphere(f"{name}_Fluegel_{sg}", (-0.015, sg * 0.092, 0.20), 0.075, m_g, col, scale=(0.75, 0.28, 1.7), parent=e)
            sphere(f"{name}_Spiegel_{sg}", (0.01, sg * 0.105, 0.27), 0.03, m_r, col, scale=(0.8, 0.4, 1.0), parent=e)
        cyl(f"{name}_Fuss_{sg}", (0.02, sg * 0.035, 0.012), 0.012, 0.05, m_f, col, parent=e)
    cyl(f"{name}_Schwanz", (-0.13, 0, 0.035), 0.035, 0.32, m_g, col, rot=(0, math.radians(18), 0), parent=e)
    cyl(f"{name}_SchwanzSpitze", (-0.185, 0, -0.095), 0.03, 0.1, m_y, col, rot=(0, math.radians(18), 0), parent=e)
    return e


def prop_cage(name, loc, col, facing_deg=0.0, bird=True, wet=False, wings_open=False):
    """Lorchens Messingkäfig, groß und rund mit Kuppeldach: 0,95 m hoch, Ø 0,56 m. loc = Bodenmitte. Rückgabe: Empty."""
    m = mat("MAT_Kaefig_Messing", (0.90, 0.68, 0.20, 1), rough=0.30); m_w = mat("MAT_Kaefig_Stange", (0.55, 0.38, 0.22, 1))
    m_cup = mat("MAT_Kaefig_Napf", (0.95, 0.95, 0.95, 1)); m_f = mat("MAT_Kaefig_Futter", (0.85, 0.65, 0.25, 1))
    e = empty(name, loc, facing_deg, col)
    cyl(f"{name}_Sockel", (0, 0, 0.05), 0.29, 0.10, m, col, parent=e)
    cyl(f"{name}_Boden", (0, 0, 0.11), 0.27, 0.02, mat("MAT_Kaefig_Einstreu", (0.80, 0.70, 0.50, 1)), col, parent=e)
    for i in range(24):
        a = 2 * math.pi * i / 24
        cyl(f"{name}_Stab_{i}", (0.27 * math.cos(a), 0.27 * math.sin(a), 0.43), 0.007, 0.64, m, col, verts=6, parent=e)
    torus(f"{name}_RingUnten", (0, 0, 0.12), 0.27, 0.010, m, col, parent=e)
    torus(f"{name}_RingMitte", (0, 0, 0.43), 0.27, 0.008, m, col, parent=e)
    torus(f"{name}_RingOben", (0, 0, 0.75), 0.27, 0.012, m, col, parent=e)
    sphere(f"{name}_Kuppel", (0, 0, 0.75), 0.27, m, col, scale=(1, 1, 0.55), parent=e)
    cyl(f"{name}_Knauf", (0, 0, 0.92), 0.022, 0.06, m, col, parent=e)
    torus(f"{name}_Griff", (0, 0, 0.97), 0.07, 0.012, m, col, rot=(math.radians(90), 0, 0), parent=e)
    cyl(f"{name}_Sitzstange", (0, 0, 0.30), 0.014, 0.50, m_w, col, rot=(math.radians(90), 0, 0), parent=e)
    cyl(f"{name}_Napf", (0.0, 0.20, 0.38), 0.05, 0.05, m_cup, col, parent=e)
    sphere(f"{name}_Futter", (0.0, 0.20, 0.41), 0.04, m_f, col, scale=(1, 1, 0.5), parent=e)
    if bird:
        p = prop_parrot(f"{name}_Lorchen", (0, 0, 0.31), col, wet=wet, wings_open=wings_open, scale=0.85)
        p.parent = e
    return e


def prop_suitcase(name, loc, facing_deg, col, open_lid=False):
    """Friedas pflaumenfarbener Riesen-Rollkoffer (85 × 55 × 32 cm). loc = Bodenmitte."""
    m = mat("MAT_Koffer_Pflaume", (0.45, 0.10, 0.25, 1)); m_d = mat("MAT_Koffer_Dunkel", (0.1, 0.1, 0.1, 1))
    e = empty(name, loc, facing_deg, col)
    if open_lid:
        box(f"{name}_Schale", (0, 0, 0.09), (0.85, 0.55, 0.16), m, col, parent=e)
        box(f"{name}_Deckel", (0, 0.32, 0.30), (0.85, 0.06, 0.55), m, col, parent=e)
    else:
        box(f"{name}_Koerper", (0, 0, 0.47), (0.55, 0.32, 0.85), m, col, parent=e)
        cyl(f"{name}_Griff", (0, -0.12, 0.98), 0.01, 0.22, m_d, col, parent=e)
        for x in (0.22, -0.22):
            for y in (0.12, -0.12):
                sphere(f"{name}_Rolle_{x}_{y}", (x, y, 0.03), 0.03, m_d, col, parent=e)
    return e


def prop_sprayer(name, loc, col):
    """Mamas grüner Blumensprüher (25 cm)."""
    m = mat("MAT_Sprueher_Gruen", (0.25, 0.70, 0.30, 1)); m_w = mat("MAT_Sprueher_Kopf", (0.95, 0.95, 0.95, 1))
    e = empty(name, loc, 0, col)
    cyl(f"{name}_Flasche", (0, 0, 0.08), 0.04, 0.16, m, col, parent=e)
    box(f"{name}_Kopf", (0.01, 0, 0.19), (0.06, 0.03, 0.06), m_w, col, parent=e)
    return e


def prop_cake(name, loc, col, cut=True):
    """Apfelkuchen auf weißer Tortenplatte. loc = Tischoberfläche."""
    m_p = mat("MAT_Tortenplatte", (0.96, 0.96, 0.96, 1)); m_k = mat("MAT_Apfelkuchen", (0.85, 0.60, 0.25, 1))
    e = empty(name, loc, 0, col)
    cyl(f"{name}_Platte", (0, 0, 0.01), 0.18, 0.02, m_p, col, parent=e)
    cyl(f"{name}_Kuchen", (0, 0, 0.055), 0.14, 0.07, m_k, col, parent=e)
    return e


def prop_cakebox(name, loc, col):
    """Himmelblaue Kuchendose (Ø 24 cm)."""
    return cyl(name, (loc[0], loc[1], loc[2] + 0.05), 0.12, 0.10, mat("MAT_Kuchendose", (0.50, 0.75, 0.95, 1)), col)


def prop_cup(name, loc, col):
    return cyl(name, (loc[0], loc[1], loc[2] + 0.045), 0.04, 0.09, mat("MAT_Tasse", (0.97, 0.97, 0.95, 1)), col)


def prop_glitterstone(name, loc, col):
    return sphere(name, loc, 0.03, mat("MAT_Glitzerstein", (0.55, 0.25, 0.85, 1), rough=0.2), col, scale=(1, 1, 1.3))


def prop_cap(name, loc, col):
    """Opas graue Schiebermütze."""
    return sphere(name, loc, 0.12, mat("MAT_Muetze_Grau", (0.45, 0.45, 0.45, 1)), col, scale=(1.1, 1, 0.35))


def prop_tin(name, loc, col):
    """Opas rote Mut-Dose (Ø 15 cm)."""
    return cyl(name, (loc[0], loc[1], loc[2] + 0.04), 0.08, 0.08, mat("MAT_Mut_Dose", (0.65, 0.12, 0.10, 1)), col)


def prop_book(name, loc, col, facing_deg=0.0):
    e = empty(name, loc, facing_deg, col)
    box(f"{name}_Buch", (0, 0, 0.12), (0.03, 0.28, 0.24), mat("MAT_Bilderbuch", (0.95, 0.45, 0.15, 1)), col, parent=e)
    return e


def prop_chair(name, loc, facing_deg, col):
    """Einfacher Holzstuhl (Sitz 46 cm) für Tischenden."""
    m = mat("MAT_Stuhl_Holz", (0.62, 0.45, 0.28, 1))
    e = empty(name, loc, facing_deg, col)
    box(f"{name}_Sitz", (0, 0, 0.44), (0.46, 0.46, 0.04), m, col, parent=e)
    box(f"{name}_Lehne", (-0.21, 0, 0.70), (0.04, 0.46, 0.48), m, col, parent=e)
    for x in (0.2, -0.2):
        for y in (0.2, -0.2):
            box(f"{name}_Bein_{x}_{y}", (x, y, 0.21), (0.04, 0.04, 0.42), m, col, parent=e)
    return e


def prop_wardrobe(name, loc, col, open_deg=100.0, cage=False, facing_deg=0.0):
    """Offener Kleiderschrank (2,0 × 0,9 × 2,1 m), Front nach +Y. loc = Bodenmitte. open_deg 0 = zu. Rückgabe: Empty."""
    m = mat("MAT_Schrank_Holz2", (0.72, 0.52, 0.30, 1)); m_in = mat("MAT_Schrank_Innen", (0.85, 0.72, 0.55, 1))
    e = empty(name, loc, facing_deg, col)
    W, D, H, t = 2.0, 0.9, 2.1, 0.03
    box(f"{name}_Rueck", (0, -D / 2 + t / 2, H / 2), (W, t, H), m_in, col, parent=e)
    box(f"{name}_SeiteL", (-W / 2 + t / 2, 0, H / 2), (t, D, H), m, col, parent=e)
    box(f"{name}_SeiteR", (W / 2 - t / 2, 0, H / 2), (t, D, H), m, col, parent=e)
    box(f"{name}_Dach", (0, 0, H - t / 2), (W, D, t), m, col, parent=e)
    box(f"{name}_Boden", (0, 0, 0.05), (W, D, 0.1), m, col, parent=e)
    box(f"{name}_Regal", (0, 0, 1.55), (W - 2 * t, D - 0.1, t), m_in, col, parent=e)
    th = math.radians(open_deg)
    for sg in (-1, 1):                       # zwei Türen, Scharnier außen
        hx, hy = sg * (W / 2), D / 2
        ang = th if sg < 0 else math.pi - th
        c = (hx + math.cos(ang) * 0.5, hy + math.sin(ang) * 0.5, H / 2)
        box(f"{name}_Tuer_{sg}", c, (W / 2, t, H - 0.1), m, col, rot_z=ang, parent=e)
    if cage:
        prop_cage(f"{name}_Kaefig", (0.35, -0.05, 0.1), col, facing_deg=0).parent = e
    return e
