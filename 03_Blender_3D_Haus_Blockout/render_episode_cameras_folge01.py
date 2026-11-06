#!/usr/bin/env python3
"""
Rendert die neuen, wiederverwendbaren Episoden-Kameras der Folge 01 "Post für Oma"
(Maxi Cartoons) aus Maxis_Haus_Komplett_Blockout.blend – aktuell nur KOM_CAM_38.

Muster: render_committee_cameras.py (KOM_CAM_34–37). Unterschiede:
  * Die Blockout-.blend wird NUR geladen und NIE gespeichert (kein save_as_mainfile).
  * Kamera entsteht nur im Speicher; Ausgabe-PNG 1600x1000 in den Episodenordner
    EP/01_Neue_Wiederverwendbare_Szenen_Blender_und_Flow/, auf Wunsch zusätzlich eine
    Kopie nach M/04_.../03_Blender_Kamera_Screenshots/ (nur hinzufügen, nie überschreiben).
  * Projektionscheck (W06): Schlüsselpunkte des Vorgartens werden durch die Kamera
    projiziert und als Tabelle geloggt (Bildseite, Action-Safe).

Aufruf:
  /home/felix/.local/bin/blender -b <Blockout.blend> --python render_episode_cameras_folge01.py -- [Optionen]
Optionen (nach "--"):
  --out-dir <dir>      Ausgabeordner statt EP/01_Neue_... (für Probe-Renders)
  --copy-m04           PNG zusätzlich nach M/04_.../03_Blender_Kamera_Screenshots/ kopieren
  --only <ID>          nur diese Kamera rendern (z. B. KOM_CAM_38)
  --loc x,y,z          Kameraposition überschreiben (Probe)
  --target x,y,z       Zielpunkt überschreiben (Probe)
  --lens <mm>          Brennweite überschreiben (Probe)
  --no-render          nur Projektionscheck, kein Render
"""

import os
import sys
import time
import math
import shutil
import hashlib

import bpy
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view

BLEND_PATH = "/home/felix/projects/dump/Maxis_Welt_Korrekturmappe/03_Blender_3D_Haus_Blockout/Maxis_Haus_Komplett_Blockout.blend"
EP_DIR = "/home/felix/projects/dump/Maxis_Welt_Korrekturmappe/06_Folge_01_Post_fuer_Oma/01_Neue_Wiederverwendbare_Szenen_Blender_und_Flow"
M04_DIR = "/home/felix/projects/dump/Maxis_Welt_Korrekturmappe/04_Komitee_Kameraplan_und_Flow_Raumszenen/03_Blender_Kamera_Screenshots"

# (ID, Name, loc, target, lens_mm) – Werte = C/execution/WP9/scenes.json "new_cameras" (WP9 Teil C 5.3)
EPISODE_CAMERAS = [
    ("KOM_CAM_38", "Vorgarten_Gartentor_Briefkasten_Nah_Kinderaugenhoehe",
     (-0.60, -10.40, 1.05), (1.60, -14.10, 1.00), 20.0),
]

# Schlüsselpunkte des Vorgartens (Blockout-Koordinaten; WP9 Blocking-Plan v3) für den W06-Projektionscheck
CHECK_POINTS = {
    "KOM_CAM_38": [
        ("Briefkasten Mitte Oberkante",      (2.01, -14.17, 1.32)),
        ("Briefkasten Mitte Unterkante",     (2.01, -14.17, 0.95)),
        ("Briefkasten Ostkante",             (2.24, -14.17, 1.13)),
        ("Gartentor Mitte (Oberkante)",      (0.60, -13.90, 0.98)),
        ("Gartentor Westpfosten",            (-0.40, -14.00, 1.05)),
        ("Gartentor Ostpfosten",             (1.60, -14.00, 1.05)),
        ("Bollerwagen NO-Ecke (Boden)",      (0.40, -13.20, 0.00)),
        ("Bollerwagen NW-Ecke (Boden)",      (-0.60, -13.20, 0.00)),
        ("Bollerwagen SW-Ecke (Oberkante)",  (-0.60, -13.80, 0.50)),
        ("Oma hinten rechts (Kopf 1,60)",    (-0.90, -15.20, 1.60)),
        ("Oma hinten rechts (Fuss)",         (-0.90, -15.20, 0.00)),
        ("Oma Einstieg West (Kopf)",         (-3.00, -15.30, 1.60)),
        ("Oma hinter Tormitte (Kopf)",       (0.60, -14.60, 1.60)),
        ("Ben am Kasten SH040 (Kopf 1,07)",  (1.60, -13.40, 1.07)),
        ("Ben am Kasten SH040 (Fuss)",       (1.60, -13.40, 0.00)),
        ("Maxi SH040 (Kopf 1,07)",           (0.80, -13.10, 1.07)),
        ("Maxi SH040 (Fuss)",                (0.80, -13.10, 0.00)),
        ("Anna SH040 (Kopf 1,07)",           (-0.30, -12.90, 1.07)),
        ("Anna SH040 (Fuss)",                (-0.30, -12.90, 0.00)),
        ("Buergersteig Suedkante Mitte",     (0.60, -16.65, 0.00)),
        ("Strasse gegenueber (Boden)",       (0.60, -24.00, 0.00)),
        ("Horizont-Referenz (Augenhoehe)",   (1.60, -14.10, 1.05)),
    ],
}


def parse_args(argv):
    opts = {"out_dir": EP_DIR, "copy_m04": False, "only": None, "loc": None, "target": None,
            "lens": None, "render": True}
    if "--" in argv:
        argv = argv[argv.index("--") + 1:]
    else:
        argv = []
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--out-dir":
            opts["out_dir"] = argv[i + 1]; i += 2
        elif a == "--copy-m04":
            opts["copy_m04"] = True; i += 1
        elif a == "--only":
            opts["only"] = argv[i + 1]; i += 2
        elif a == "--loc":
            opts["loc"] = tuple(float(v) for v in argv[i + 1].split(",")); i += 2
        elif a == "--target":
            opts["target"] = tuple(float(v) for v in argv[i + 1].split(",")); i += 2
        elif a == "--lens":
            opts["lens"] = float(argv[i + 1]); i += 2
        elif a == "--no-render":
            opts["render"] = False; i += 1
        else:
            raise SystemExit(f"Unbekannte Option: {a}")
    return opts


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def side_word(u):
    if u < 0.46:
        return "links"
    if u > 0.54:
        return "rechts"
    return "Mitte"


def projection_check(scene, cam_obj, cam_id, loc, target):
    pts = CHECK_POINTS.get(cam_id, [])
    if not pts:
        return
    d = Vector(target) - Vector(loc)
    right = Vector((d.y, -d.x, 0.0)).normalized()
    fwd = Vector((d.x, d.y, 0.0)).normalized()
    print(f"[{cam_id}] Projektionscheck (u/v = Bildkoordinaten 0..1, u 0 = links; Winkel = horizontal zur Blickachse, + = rechts):")
    print(f"  {'Punkt':36s} {'u':>6s} {'v':>6s} {'Winkel':>7s} {'Dist':>6s}  Seite   im Bild  ActionSafe(90%)")
    for label, p in pts:
        pv = Vector(p)
        co = world_to_camera_view(scene, cam_obj, pv)
        rel = Vector((pv.x - loc[0], pv.y - loc[1], 0.0))
        ang = math.degrees(math.atan2(rel.dot(right), rel.dot(fwd)))
        dist = rel.length
        inside = (0.0 <= co.x <= 1.0 and 0.0 <= co.y <= 1.0 and co.z > 0)
        safe = (0.05 <= co.x <= 0.95 and 0.05 <= co.y <= 0.95 and co.z > 0)
        print(f"  {label:36s} {co.x:6.3f} {1 - co.y:6.3f} {ang:+7.1f} {dist:6.2f}  {side_word(co.x):6s}  {'ja' if inside else 'NEIN':7s}  {'ja' if safe else 'NEIN'}")


def main():
    opts = parse_args(sys.argv)
    if os.path.abspath(bpy.data.filepath or "") != os.path.abspath(BLEND_PATH):
        bpy.ops.wm.open_mainfile(filepath=BLEND_PATH)
    scene = bpy.context.scene
    scene.render.resolution_x = 1600
    scene.render.resolution_y = 1000
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    print(f"Engine: {scene.render.engine}; View Transform: {scene.view_settings.view_transform}; "
          f"Aufloesung {scene.render.resolution_x}x{scene.render.resolution_y}")

    # Wie im Muster: alle Sammlungen & Objekte renderbar schalten (nur im Speicher)
    for col in bpy.data.collections:
        col.hide_render = False
    for obj in bpy.data.objects:
        obj.hide_render = False

    col_name = "99_Komitee_Standard_Kameras"
    col_cam = bpy.data.collections.get(col_name)
    if col_cam is None:
        col_cam = bpy.data.collections.new(col_name)
        scene.collection.children.link(col_cam)

    os.makedirs(opts["out_dir"], exist_ok=True)
    results = []
    for cam_id, cam_name, loc, target, lens in EPISODE_CAMERAS:
        if opts["only"] and cam_id != opts["only"]:
            continue
        if opts["loc"]:
            loc = opts["loc"]
        if opts["target"]:
            target = opts["target"]
        if opts["lens"]:
            lens = opts["lens"]
        full_name = f"{cam_id}_{cam_name}"
        old = bpy.data.objects.get(full_name)
        if old:
            bpy.data.objects.remove(old, do_unlink=True)
        cdata = bpy.data.cameras.new(name=full_name)
        cdata.lens = lens
        cdata.clip_start = 0.08
        cdata.clip_end = 250.0
        cobj = bpy.data.objects.new(name=full_name, object_data=cdata)
        cobj.location = Vector(loc)
        direction = Vector(target) - Vector(loc)
        cobj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()
        col_cam.objects.link(cobj)
        scene.camera = cobj
        bpy.context.view_layer.update()

        hfov = 2 * math.degrees(math.atan(cdata.sensor_width / (2 * lens)))
        vfov = 2 * math.degrees(math.atan(cdata.sensor_width * 1000 / 1600 / (2 * lens)))
        tilt = math.degrees(math.atan2(target[2] - loc[2], math.hypot(target[0] - loc[0], target[1] - loc[1])))
        print(f"[{cam_id}] {cam_name}: loc {loc} target {target} lens {lens} mm, Sensor {cdata.sensor_width} mm "
              f"({cdata.sensor_fit}), hFOV {hfov:.1f} deg, vFOV {vfov:.1f} deg, Neigung {tilt:+.2f} deg, "
              f"Hoehe {loc[2]:.2f} m, Abstand zum Ziel {direction.length:.2f} m")
        projection_check(scene, cobj, cam_id, loc, target)

        if not opts["render"]:
            continue
        out_file = os.path.join(opts["out_dir"], f"{full_name}.png")
        scene.render.filepath = out_file
        t0 = time.time()
        bpy.ops.render.render(write_still=True)
        dt = time.time() - t0
        print(f"[{cam_id}] Gerendert in {dt:.1f} s: {out_file} (sha256 {sha256(out_file)[:16]}...)")
        results.append((cam_id, out_file, dt))

        if opts["copy_m04"]:
            dst = os.path.join(M04_DIR, f"{full_name}.png")
            if os.path.exists(dst):
                print(f"[{cam_id}] M/04-Kopie NICHT geschrieben – Datei existiert bereits (nur Hinzufuegen erlaubt): {dst}")
            else:
                shutil.copyfile(out_file, dst)
                print(f"[{cam_id}] Kopie nach M/04: {dst} (sha256 {sha256(dst)[:16]}...)")

    print(f"Fertig: {len(results)} Kamera(s) gerendert; .blend NICHT gespeichert (kein save_as_mainfile).")


if __name__ == "__main__":
    main()
