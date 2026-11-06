#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Realistisches Licht fürs texturierte Haus (2026-11-06): warme tiefe Novembersonne von außen durch die Fenster, weiche Schatten,
blauer Himmel mit leichtem Dunst (Luft-Volumen, ferne Dinge werden blasser), alle Lampen aus, keine künstliche Aufhellung, keine Konturlinien.
Cycles (GPU, falls vorhanden) mit Denoiser.

  blender -b Maxis_Haus_Komplett_Texturiert.blend --python licht_haus.py -- [--raeume Wohnzimmer,Kueche,...] [--aussen] [--samples 128] [--out DIR]
Ohne Argumente: alle Räume + Außen rendern und das Ergebnis als Maxis_Haus_Komplett_Texturiert_Licht.blend speichern.
Je Raum steht die Sonne so, dass sie durch dessen Fenster hereinfällt (Azimut, Höhe aus ROOMS).
"""
import os, sys, math, re
import bpy
from mathutils import Vector

E = os.path.dirname(os.path.abspath(bpy.data.filepath))
OUT_BLEND = os.path.join(E, "Maxis_Haus_Komplett_Texturiert_Licht.blend")

# Raum: (Kameras (Präfixe), Sonnen-Azimut in Grad [0 = Ost, 90 = Nord, 180 = West, 270 = Süd; Richtung ZUR Sonne], Höhe, Belichtung)
ROOMS = {
    "EG_Wohnzimmer":  (["KOM_CAM_07", "KOM_CAM_08", "KOM_CAM_30"], 228, 26, 0.9),
    "EG_Kueche":      (["KOM_CAM_09", "KOM_CAM_10"],              150, 28, 1.0),
    "EG_Spielzimmer": (["KOM_CAM_11", "KOM_CAM_12"],               38, 30, 0.9),
    "EG_Gaesteklo":   (["KOM_CAM_13", "KOM_CAM_14"],              318, 30, 0.9),
    "EG_Flur":        (["FLUR_CAM_01", "FLUR_CAM_02"],             95, 32, 1.6),
    "OG_Kinderzimmer":(["KOM_CAM_17", "KOM_CAM_32", "KOM_CAM_18"],232, 27, 0.9),
    "OG_Elternzimmer":(["KOM_CAM_19", "KOM_CAM_20"],               50, 30, 0.9),
    "OG_Bad":         (["KOM_CAM_21", "KOM_CAM_22"],              320, 30, 0.9),
    "OG_Flur":        (["FLUR_CAM_05", "FLUR_CAM_04"],           270, 38, 3.6),
    "DG_Dachboden":   (["KOM_CAM_23", "KOM_CAM_24"],              178, 34, 2.3),
    "Garage":         (["KOM_CAM_26", "KOM_CAM_27"],              262, 24, 1.1),
    "Aussen":         (["KOM_CAM_01", "KOM_CAM_03", "KOM_CAM_04", "KOM_CAM_05"], 222, 26, 0.0),
}


def args():
    a = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    d = {"raeume": None, "samples": 128, "out": os.path.join(E, "Raumbilder_Licht"), "w": 1600, "h": 900}
    i = 0
    while i < len(a):
        if a[i] == "--raeume": d["raeume"] = a[i + 1].split(","); i += 2
        elif a[i] == "--aussen": d["raeume"] = ["Aussen"]; i += 1
        elif a[i] == "--save": d["save"] = True; i += 1
        elif a[i] == "--samples": d["samples"] = int(a[i + 1]); i += 2
        elif a[i] == "--out": d["out"] = a[i + 1]; i += 2
        elif a[i] == "--w": d["w"] = int(a[i + 1]); i += 2
        elif a[i] == "--h": d["h"] = int(a[i + 1]); i += 2
        else: i += 1
    return d


# ------------------------------------------------------------------ Lampen aus, keine Pseudo-Aufhellung
def lights_off():
    n = 0
    for o in list(bpy.data.objects):
        if o.type == "LIGHT":
            bpy.data.objects.remove(o, do_unlink=True); n += 1
    for m in bpy.data.materials:
        if not m.use_nodes:
            continue
        for nd in m.node_tree.nodes:
            if nd.bl_idname == "ShaderNodeBsdfPrincipled":
                for k in ("Emission Strength",):
                    if k in nd.inputs:
                        nd.inputs[k].default_value = 0.0
            elif nd.bl_idname == "ShaderNodeEmission":
                nd.inputs["Strength"].default_value = 0.0
    print("Lampen entfernt:", n)


# ------------------------------------------------------------------ Sonne + Himmel + Dunst
def make_sun():
    ld = bpy.data.lights.new("Sonne_Warm", "SUN")
    ld.energy = 8.0
    ld.color = (1.0, 0.70, 0.40)
    ld.angle = math.radians(2.2)                 # weiche Schattenkanten
    ob = bpy.data.objects.new("Sonne_Warm", ld)
    bpy.context.scene.collection.objects.link(ob)
    return ob


def aim_sun(sun, az_deg, el_deg):
    az, el = math.radians(az_deg), math.radians(el_deg)
    to_sun = Vector((math.cos(el) * math.cos(az), math.cos(el) * math.sin(az), math.sin(el)))
    sun.rotation_euler = (-to_sun).to_track_quat("-Z", "Y").to_euler()
    return to_sun


def make_world():
    sc = bpy.context.scene
    w = bpy.data.worlds.new("Licht_Welt")
    w.use_nodes = True
    nt = w.node_tree; nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputWorld")
    bg = nt.nodes.new("ShaderNodeBackground")
    sky = nt.nodes.new("ShaderNodeTexSky")
    sky.sky_type = "MULTIPLE_SCATTERING"
    sky.sun_disc = False                          # die Sonne ist die Sonnenlampe
    for attr, val in (("air_density", 1.0), ("aerosol_density", 2.0), ("ozone_density", 1.0), ("dust_density", 2.2)):
        if hasattr(sky, attr):
            setattr(sky, attr, val)                  # Namen unterscheiden sich je Blender-Version
    bg.inputs["Strength"].default_value = 0.55
    nt.links.new(sky.outputs["Color"], bg.inputs["Color"])
    nt.links.new(bg.outputs["Background"], out.inputs["Surface"])
    sc.world = w
    return sky


def make_haze():
    """Begrenztes Dunst-Volumen über dem Viertel (ein Welt-Volumen wäre unendlich und würde auch die Sonne auslöschen).
    Wirkt erst über viele Meter: Hecken, Nachbarhäuser und Bäume im Hintergrund werden blasser, Sonnenstrahlen glühen leicht."""
    import bmesh
    me = bpy.data.meshes.new("Dunst_Volumen")
    bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co.x *= 2400; v.co.y *= 2400; v.co.z *= 300; v.co.z += 120
    bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new("Dunst_Volumen", me)
    bpy.context.scene.collection.objects.link(ob)
    mat = bpy.data.materials.new("Dunst")
    mat.use_nodes = True
    nt = mat.node_tree; nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    vol = nt.nodes.new("ShaderNodeVolumePrincipled")
    vol.inputs["Color"].default_value = (0.82, 0.89, 1.0, 1)
    vol.inputs["Density"].default_value = float(os.environ.get("CY_DENS", "0.0013"))
    vol.inputs["Anisotropy"].default_value = 0.5
    nt.links.new(vol.outputs["Volume"], out.inputs["Volume"])
    me.materials.append(mat)
    ob.display_type = "BOUNDS"
    return ob


def aim_sky(sky, az_deg, el_deg):
    sky.sun_elevation = math.radians(el_deg)
    sky.sun_rotation = math.radians(az_deg - 90.0) % (2 * math.pi)   # Blender: 0 = Nord, dreht gegen den Uhrzeigersinn? Gegenprobe über Render


def setup_render(w, h, samples):
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    cy = sc.cycles
    cy.samples = samples
    cy.use_denoising = True
    try:
        cy.denoiser = "OPENIMAGEDENOISE"
    except Exception:
        pass
    cy.max_bounces = 8; cy.diffuse_bounces = 5; cy.glossy_bounces = 3; cy.transmission_bounces = 6; cy.transparent_max_bounces = 12
    cy.volume_bounces = int(os.environ.get("CY_VB", "1"))
    if os.environ.get("CY_VMAX"): cy.volume_max_steps = int(os.environ["CY_VMAX"])
    if os.environ.get("CY_VSTEP"): cy.volume_step_rate = float(os.environ["CY_VSTEP"])
    cy.use_adaptive_sampling = True
    cy.sample_clamp_indirect = 8.0
    try:
        prefs = bpy.context.preferences.addons["cycles"].preferences
        for t in (() if os.environ.get("CY_CPU") else (os.environ.get("CY_GPU", "CUDA"),)):
            try:
                prefs.compute_device_type = t
                prefs.get_devices()
                gpus = [d for d in prefs.devices if d.type != "CPU"]
                if gpus:
                    for d in prefs.devices:
                        d.use = (d.type != "CPU")
                    cy.device = "GPU"; print("GPU:", t, [d.name for d in gpus]); break
            except Exception as e:
                print("GPU-Versuch", t, "fehlgeschlagen:", e)
    except Exception as e:
        print("Cycles-Prefs:", e)
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = w, h, 100
    sc.render.use_freestyle = False
    for vl in sc.view_layers:
        vl.use_freestyle = False
    sc.render.image_settings.file_format = "JPEG"; sc.render.image_settings.quality = 94
    vs = sc.view_settings
    vs.view_transform = "AgX"
    try:
        vs.look = "AgX - Medium High Contrast"
    except Exception:
        pass


def glass_transparent():
    m = bpy.data.materials.get("TX_Fensterglas")
    if m and m.use_nodes:
        b = m.node_tree.nodes.get("Principled BSDF")
        if b:
            b.inputs["Alpha"].default_value = 0.06


def main():
    a = args()
    lights_off()
    glass_transparent()
    sky = make_world()
    sun = make_sun()
    if not os.environ.get("CY_NOVOL"):
        make_haze()
    setup_render(a["w"], a["h"], a["samples"])
    for c in bpy.data.collections:
        c.hide_render = False
    sc = bpy.context.scene
    os.makedirs(a["out"], exist_ok=True)
    todo = a["raeume"] or list(ROOMS)
    for room in todo:
        cams, az, el, ev = ROOMS[room]
        aim_sun(sun, az, el); aim_sky(sky, az, el)
        sc.view_settings.exposure = ev
        for cp in cams:
            cam = next((o for o in bpy.data.objects if o.type == "CAMERA" and o.name.startswith(cp)), None)
            if not cam:
                print("Kamera fehlt:", cp); continue
            sc.camera = cam
            sc.render.filepath = os.path.join(a["out"], f"{room}_{cam.name.split('_Standard')[0][:40]}.jpg")
            bpy.ops.render.render(write_still=True)
            print("Gerendert:", sc.render.filepath, flush=True)
    aim_sun(sun, 228, 26); aim_sky(sky, 228, 26); sc.view_settings.exposure = 0.9
    if a.get("save") or not a["raeume"] or len(a["raeume"]) == len(ROOMS):
        bpy.ops.wm.save_as_mainfile(filepath=OUT_BLEND)
        print("Gespeichert:", OUT_BLEND)


main()
