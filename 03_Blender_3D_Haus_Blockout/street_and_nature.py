#!/usr/bin/env python3
"""
Bürgersteig, Wohnstraße (Ahornweg), Sichtschutz-Hecke, weite Wiese und Bäume
auf der gegenüberliegenden Straßenseite sowie hinter den Häusern.
"""


def build_street_and_nature(add_box, get_collection, make_mat):
    col_env = get_collection("06_Strasse_Buergersteig_Hecke_und_Wiese")

    # Materialien für Straße, Bürgersteig, Hecke & Wiese registrieren
    make_mat("Meadow_Green", (0.48, 0.72, 0.36, 1.0), 0.92)
    make_mat("Sidewalk_Gray", (0.76, 0.75, 0.72, 1.0), 0.85)
    make_mat("Curb_Stone", (0.64, 0.63, 0.60, 1.0), 0.85)
    make_mat("Street_Asphalt", (0.28, 0.29, 0.31, 1.0), 0.88)
    make_mat("Street_Line_White", (0.94, 0.94, 0.92, 1.0), 0.70)
    make_mat("Hedge_Green", (0.24, 0.52, 0.22, 1.0), 0.88)
    make_mat("Hedge_LightGreen", (0.30, 0.58, 0.26, 1.0), 0.88)
    make_mat("Lamp_Post_Dark", (0.20, 0.22, 0.25, 1.0), 0.55)

    # 1. Weite umliegende Wiese (als Grundplatte unter der gesamten Nachbarschaft)
    #    Verhindert jeden grauen Abgrund in Fenster- und Außenkameras!
    add_box("Umgebung_Wiese_Sued_Gegenueber", -95.0, 95.0, -85.0, -26.5, -0.16, -0.02, "Meadow_Green", col_env)
    add_box("Umgebung_Wiese_Nord_Hinter_Gaerten", -95.0, 95.0, 22.0, 80.0, -0.16, -0.02, "Meadow_Green", col_env)
    add_box("Umgebung_Wiese_West_Aussen", -95.0, -52.0, -26.5, 22.0, -0.16, -0.02, "Meadow_Green", col_env)
    add_box("Umgebung_Wiese_Ost_Aussen", 52.0, 95.0, -26.5, 22.0, -0.16, -0.02, "Meadow_Green", col_env)

    # 2. Bürgersteig direkt vor den 3 Häusern (Nordseite der Straße: Y = -16.8 .. -14.0)
    add_box("Buergersteig_Hausseite", -75.0, 75.0, -16.65, -14.0, -0.08, 0.04, "Sidewalk_Gray", col_env)
    add_box("Bordstein_Hausseite", -75.0, 75.0, -16.85, -16.65, -0.08, 0.06, "Curb_Stone", col_env)

    # 3. Wohnstraße "Ahornweg" (Y = -24.0 .. -16.85, 7.15 m breit)
    add_box("Strasse_Ahornweg_Asphalt", -75.0, 75.0, -24.0, -16.85, -0.12, -0.03, "Street_Asphalt", col_env)

    # Gestrichelte weiße Fahrbahn-Mittellinie entlang des Ahornwegs (bei Y = -20.42)
    for sx in range(-68, 70, 6):
        add_box(f"Strasse_Mittelstreifen_{sx}", sx, sx + 3.2, -20.52, -20.32, -0.03, -0.015, "Street_Line_White", col_env)

    # Fußgängerüberweg / Zebrastreifen leicht westlich vor Maxis & Annas Tor (X = -10.5 .. -6.5)
    for zi in range(6):
        zy = -23.4 + zi * 1.05
        add_box(f"Zebrastreifen_{zi}", -10.5, -6.5, zy, zy + 0.55, -0.03, -0.012, "Street_Line_White", col_env)

    # 4. Gegenüberliegender Bürgersteig (Südseite der Straße: Y = -26.5 .. -24.0)
    add_box("Bordstein_Gegenueber", -75.0, 75.0, -24.20, -24.0, -0.08, 0.06, "Curb_Stone", col_env)
    add_box("Buergersteig_Gegenueber", -75.0, 75.0, -26.5, -24.20, -0.08, 0.04, "Sidewalk_Gray", col_env)

    # 5. Straßenlaternen entlang des Bürgersteigs & gelber Briefkasten an Maxis Gartentor
    for idx, lx in enumerate([-37.0, -14.5, 4.5, 29.5]):
        add_box(f"Strassenlaterne_Fuss_{idx}", lx - 0.16, lx + 0.16, -16.45, -16.13, 0.04, 0.45, "Lamp_Post_Dark", col_env)
        add_box(f"Strassenlaterne_Mast_{idx}", lx - 0.07, lx + 0.07, -16.36, -16.22, 0.45, 4.10, "Lamp_Post_Dark", col_env)
        add_box(f"Strassenlaterne_Arm_{idx}", lx - 0.07, lx + 0.07, -16.85, -16.22, 4.00, 4.12, "Lamp_Post_Dark", col_env)
        add_box(f"Strassenlaterne_Kopf_{idx}", lx - 0.22, lx + 0.22, -17.05, -16.65, 3.82, 4.08, "Lamp_Warm", col_env)

    # Maxis Familien-Briefkasten am vorderen Gartenzaun rechts neben dem Gartentor
    add_box("Maxi_Briefkasten_Pfosten", 1.95, 2.07, -14.22, -14.10, 0.0, 1.05, "Lamp_Post_Dark", col_env)
    add_box("Maxi_Briefkasten_Kasten", 1.78, 2.24, -14.32, -14.02, 0.95, 1.32, "Gate_Yellow", col_env)

    # 6. Dichte grüne Hecke als Sichtschutz auf der anderen Straßenseite (Y = -28.1 .. -26.5)
    #    und hinter den hinteren Gartenzäunen (Y = +22.15 .. +23.65)
    for hx in range(-72, 72, 8):
        mat_h = "Hedge_Green" if (hx // 8) % 2 == 0 else "Hedge_LightGreen"
        h_top = 1.95 if (hx // 8) % 2 == 0 else 2.10
        add_box(f"Sichtschutz_Hecke_Strasse_{hx}", hx, hx + 8.05, -28.1, -26.5, 0.0, h_top, mat_h, col_env)
        add_box(f"Sichtschutz_Hecke_Nord_{hx}", hx, hx + 8.05, 22.15, 23.65, 0.0, h_top + 0.15, mat_h, col_env)

    # 7. Bäume auf der Wiese hinter der Sichtschutz-Hecke (andere Straßenseite & hinter den Gärten)
    def add_blockout_tree(prefix, tx, ty, scale=1.0, leaf_mat="Tree_Leaves"):
        tw = 0.45 * scale
        th = 3.2 * scale
        cw = 2.2 * scale
        add_box(f"{prefix}_Stamm", tx - tw, tx + tw, ty - tw, ty + tw, 0.0, th, "Tree_Trunk", col_env)
        add_box(f"{prefix}_Krone_Unten", tx - cw, tx + cw, ty - cw, ty + cw, th - 0.3, th + 2.5 * scale, leaf_mat, col_env)
        add_box(f"{prefix}_Krone_Oben", tx - cw * 0.72, tx + cw * 0.72, ty - cw * 0.72, ty + cw * 0.72, th + 2.2 * scale, th + 3.6 * scale, leaf_mat, col_env)

    # Baumreihe & Baumgruppen auf der anderen Straßenseite hinter der Hecke (Y = -32 .. -55)
    south_trees = [
        (-48.0, -33.0, 1.25, "Tree_Leaves"), (-36.0, -36.5, 1.40, "Hedge_LightGreen"),
        (-24.0, -32.5, 1.15, "Tree_Leaves"), (-12.5, -35.0, 1.35, "Tree_Leaves"),
        (-2.0, -33.0, 1.20, "Hedge_LightGreen"), (9.5, -36.0, 1.45, "Tree_Leaves"),
        (21.0, -32.5, 1.20, "Tree_Leaves"), (33.5, -35.5, 1.35, "Hedge_LightGreen"),
        (46.0, -33.0, 1.25, "Tree_Leaves"), (-42.0, -46.0, 1.50, "Tree_Leaves"),
        (-18.0, -45.0, 1.60, "Hedge_LightGreen"), (3.5, -47.0, 1.55, "Tree_Leaves"),
        (26.0, -44.5, 1.45, "Tree_Leaves"), (42.0, -48.0, 1.50, "Hedge_LightGreen"),
    ]
    for i, (tx, ty, sc, lmat) in enumerate(south_trees):
        add_blockout_tree(f"Baum_Gegenueber_{i}", tx, ty, sc, lmat)

    # Baumreihe & Baumgruppen hinter den Gärten im Norden (Y = +27 .. +48)
    north_trees = [
        (-45.0, 29.0, 1.30, "Tree_Leaves"), (-30.0, 32.0, 1.45, "Hedge_LightGreen"),
        (-16.0, 28.5, 1.25, "Tree_Leaves"), (-3.0, 31.5, 1.40, "Tree_Leaves"),
        (10.5, 29.0, 1.30, "Hedge_LightGreen"), (24.0, 32.5, 1.50, "Tree_Leaves"),
        (38.0, 29.5, 1.25, "Tree_Leaves"), (49.0, 33.0, 1.35, "Hedge_LightGreen"),
        (-22.0, 42.0, 1.55, "Tree_Leaves"), (4.0, 43.5, 1.60, "Hedge_LightGreen"),
        (31.0, 41.5, 1.50, "Tree_Leaves"),
    ]
    for i, (tx, ty, sc, lmat) in enumerate(north_trees):
        add_blockout_tree(f"Baum_HinterGarten_{i}", tx, ty, sc, lmat)
