"""
Nachbarhaus Ben (Ahornweg 6) – Östliches Nachbargrundstück (X = +19.0 .. +52.0, Y = -14.0 .. +22.0)
Grobes Außen-Blockout-Modell (Backstein-EG, Creme-Putz-OG, Anthrazit-Satteldach, Tüftler-Garage).
"""


def _ensure_mat(make_mat, name, hex_col, rgba, roughness=0.75, metallic=0.0):
    try:
        return make_mat(name, hex_col, roughness=roughness, metallic=metallic)
    except TypeError:
        return make_mat(name, rgba)


def _add_win(add_box, name, x1, x2, y1, y2, z1, z2, col, axis='Y'):
    pad = 0.08
    if axis == 'Y':
        add_box(f"{name}_Frame", x1 - pad, x2 + pad, y1, y2, z1 - pad, z2 + pad, "Frame_Window", col)
        add_box(f"{name}_Glass", x1, x2, y1 - 0.02, y2 + 0.02, z1, z2, "Ben_Window_Glass", col)
    else:
        add_box(f"{name}_Frame", x1, x2, y1 - pad, y2 + pad, z1 - pad, z2 + pad, "Frame_Window", col)
        add_box(f"{name}_Glass", x1 - 0.02, x2 + 0.02, y1, y2, z1, z2, "Ben_Window_Glass", col)


def build_ben_house(add_box, add_pitched_prism, add_sloped_slab, get_collection, make_mat):
    col_ben = get_collection("05_Nachbarhaus_Ben_Ahornweg6")

    # Materialien für Bens Haus (kompatibel mit Hex- und RGBA-Aufruf)
    _ensure_mat(make_mat, "Ben_Wall_Brick", "#C26B4C", (0.76, 0.42, 0.30, 1.0), roughness=0.82)
    _ensure_mat(make_mat, "Ben_Roof_Dark", "#3D4047", (0.24, 0.25, 0.28, 1.0), roughness=0.75)
    _ensure_mat(make_mat, "Ben_Garage_Blue", "#4075AD", (0.25, 0.46, 0.68, 1.0), roughness=0.55)
    _ensure_mat(make_mat, "Ben_Window_Glass", "#ADD1EB", (0.68, 0.82, 0.92, 1.0), roughness=0.2, metallic=0.2)

    # 1. Grundstücks-Rasen & Wege (X = 19.0 .. 52.0, Y = -14.0 .. 22.0)
    add_box("Ben_Lawn_Plot", 19.0, 52.0, -14.0, 22.0, -0.12, -0.01, "Grass_Lawn", col_ben)
    add_box("Ben_Path_Front", 32.5, 34.5, -14.0, -7.6, -0.02, 0.04, "Garden_Path", col_ben)
    add_box("Ben_Driveway_Garage", 42.0, 47.0, -14.0, -5.5, -0.02, 0.04, "Garden_Path", col_ben)
    add_box("Ben_Path_To_MaxiGate", 19.0, 26.0, 1.2, 2.4, -0.02, 0.04, "Garden_Path", col_ben)
    add_box("Ben_Path_WestLink", 24.6, 26.0, -6.8, 1.2, -0.02, 0.04, "Garden_Path", col_ben)
    add_box("Ben_Path_PorchLink", 24.6, 31.0, -7.0, -5.9, -0.02, 0.04, "Garden_Path", col_ben)

    # 2. Hauptgebäude-Block (X = 26.0 .. 41.5, Y = -5.8 .. 5.5, Z = 0.0 .. 5.4)
    add_box("Ben_House_EG_Brick", 26.0, 41.5, -5.8, 5.5, 0.0, 2.75, "Ben_Wall_Brick", col_ben)
    add_box("Ben_House_Belt_Trim", 25.92, 41.58, -5.88, 5.58, 2.68, 2.82, "Frame_Window", col_ben)
    add_box("Ben_House_OG_Plaster", 26.0, 41.5, -5.8, 5.5, 2.75, 5.4, "Wall_Exterior", col_ben)

    # 3. Satteldach (Z = 5.4 .. 8.3) mit Giebelprisma entlang X (peak_axis='Y') & Dachflächen
    add_pitched_prism("Ben_Roof_GableCore", 26.0, 41.5, -5.8, 5.5, 5.4, 8.3, "Wall_Exterior", col_ben, peak_axis='Y')
    add_sloped_slab("Ben_Roof_South", 25.5, 42.0, -6.2, 5.25, -0.15, 8.35, 0.22, "Ben_Roof_Dark", col_ben)
    add_sloped_slab("Ben_Roof_North", 25.5, 42.0, 5.9, 5.25, -0.15, 8.35, 0.22, "Ben_Roof_Dark", col_ben)
    add_box("Ben_Roof_Ridge", 25.45, 42.05, -0.35, 0.05, 8.3, 8.58, "Ben_Roof_Dark", col_ben)
    add_box("Ben_Chimney", 37.8, 39.0, 1.2, 2.3, 5.4, 8.9, "Ben_Wall_Brick", col_ben)

    # 4. Überdachter Eingang vorne (X = 31.0 .. 36.0, Y = -7.6 .. -5.8)
    add_box("Ben_Porch_Step", 31.0, 36.0, -7.6, -5.8, 0.0, 0.18, "Porch_Wood", col_ben)
    add_box("Ben_Porch_Roof", 30.8, 36.2, -7.75, -5.7, 2.65, 2.9, "Ben_Roof_Dark", col_ben)
    add_box("Ben_Porch_Trim", 30.85, 36.15, -7.78, -7.68, 2.72, 2.85, "Gate_Yellow", col_ben)
    add_box("Ben_Porch_PostL", 31.2, 31.42, -7.45, -7.23, 0.18, 2.65, "Frame_Window", col_ben)
    add_box("Ben_Porch_PostR", 35.58, 35.8, -7.45, -7.23, 0.18, 2.65, "Frame_Window", col_ben)
    add_box("Ben_Front_DoorFrame", 32.8, 34.2, -5.9, -5.75, 0.18, 2.32, "Frame_Window", col_ben)
    add_box("Ben_Front_Door", 32.92, 34.08, -5.88, -5.74, 0.18, 2.22, "Ben_Garage_Blue", col_ben)
    add_box("Ben_Mailbox_Yellow", 34.45, 34.9, -5.95, -5.78, 1.15, 1.55, "Gate_Yellow", col_ben)

    # 5. Angebaute Tüftler-Garage / Werkstatt (X = 41.5 .. 47.5, Y = -5.5 .. +2.5, Z = 0.0 .. 3.3)
    add_box("Ben_Garage_Body", 41.5, 47.5, -5.5, 2.5, 0.0, 3.1, "Ben_Wall_Brick", col_ben)
    add_box("Ben_Garage_Roof", 41.4, 47.9, -5.9, 2.9, 3.1, 3.35, "Ben_Roof_Dark", col_ben)
    add_box("Ben_Garage_YellowBand", 41.45, 47.85, -5.92, -5.82, 3.15, 3.3, "Gate_Yellow", col_ben)
    add_box("Ben_Garage_DoorFrame", 42.2, 46.8, -5.6, -5.45, 0.0, 2.65, "Frame_Window", col_ben)
    add_box("Ben_Garage_DoorBlue", 42.35, 46.65, -5.58, -5.44, 0.04, 2.55, "Ben_Garage_Blue", col_ben)
    add_box("Ben_Garage_Handle", 44.2, 44.8, -5.63, -5.55, 1.05, 1.18, "Gate_Yellow", col_ben)
    _add_win(add_box, "Ben_Garage_WinE", 47.45, 47.56, -2.5, 0.8, 1.2, 2.3, col_ben, axis='X')

    # 6. Außenfenster (Süd-, Nord-, West- und Ostfassade)
    for idx, (wx1, wx2) in enumerate([(27.2, 29.6), (37.2, 39.8)]):
        _add_win(add_box, f"Ben_Win_S_EG_{idx}", wx1, wx2, -5.86, -5.74, 0.95, 2.15, col_ben, axis='Y')
    for idx, (wx1, wx2) in enumerate([(27.2, 29.6), (32.3, 34.7), (37.2, 39.8)]):
        _add_win(add_box, f"Ben_Win_S_OG_{idx}", wx1, wx2, -5.86, -5.74, 3.35, 4.65, col_ben, axis='Y')
        _add_win(add_box, f"Ben_Win_N_OG_{idx}", wx1, wx2, 5.44, 5.56, 3.35, 4.65, col_ben, axis='Y')
        _add_win(add_box, f"Ben_Win_N_EG_{idx}", wx1, wx2, 5.44, 5.56, 0.95, 2.15, col_ben, axis='Y')
    # Westfassade (zu Maxis Haus hin sichtbar) + Giebelfenster
    for idx, (wy1, wy2) in enumerate([(-3.8, -1.4), (1.0, 3.4)]):
        _add_win(add_box, f"Ben_Win_W_EG_{idx}", 25.94, 26.06, wy1, wy2, 0.95, 2.15, col_ben, axis='X')
        _add_win(add_box, f"Ben_Win_W_OG_{idx}", 25.94, 26.06, wy1, wy2, 3.35, 4.65, col_ben, axis='X')
    _add_win(add_box, "Ben_Win_W_Gable", 25.94, 26.06, -1.2, 0.9, 5.8, 7.1, col_ben, axis='X')
    _add_win(add_box, "Ben_Win_E_Gable", 41.44, 41.56, -1.2, 0.9, 5.8, 7.1, col_ben, axis='X')

    # 7. Gartenzaun (Südseite mit Gehweg- & Einfahrtslücke, Ostseite, Nordseite)
    for name, x1, x2 in [("S1", 19.0, 32.3), ("S2", 34.7, 41.8), ("S3", 47.2, 52.0)]:
        add_box(f"Ben_Fence_{name}_Rail1", x1, x2, -14.08, -13.92, 0.35, 0.48, "Fence_Wood", col_ben)
        add_box(f"Ben_Fence_{name}_Rail2", x1, x2, -14.08, -13.92, 0.82, 0.95, "Fence_Wood", col_ben)
        add_box(f"Ben_Fence_{name}_Slats", x1, x2, -14.05, -13.95, 0.08, 1.08, "Fence_Wood", col_ben)
    add_box("Ben_Fence_East", 51.9, 52.08, -14.0, 22.0, 0.08, 1.1, "Fence_Wood", col_ben)
    add_box("Ben_Fence_North", 19.0, 52.0, 21.9, 22.08, 0.08, 1.1, "Fence_Wood", col_ben)

    # 8. Außen-Objekte: Tüftler-Holzrampe, Konstruktionskisten, Basketballkorb & Bäume
    add_box("Ben_Ramp_Deck", 21.8, 24.4, 5.0, 6.6, 0.0, 0.75, "Porch_Wood", col_ben)
    add_sloped_slab("Ben_Ramp_Slope", 21.8, 24.4, 2.8, 0.02, 5.0, 0.75, 0.1, "Wood_Medium", col_ben)
    add_box("Ben_Crate_1", 22.2, 23.3, 7.2, 8.2, 0.0, 0.85, "Wood_Medium", col_ben)
    add_box("Ben_Crate_2", 23.5, 24.4, 7.3, 8.1, 0.0, 0.65, "Ben_Garage_Blue", col_ben)
    add_box("Ben_Crate_3", 22.5, 23.2, 7.35, 8.05, 0.85, 1.35, "Gate_Yellow", col_ben)

    # Basketballkorb an der Garageneinfahrt / Hofseite
    add_box("Ben_BBall_Pole", 40.8, 41.0, -7.2, -7.0, 0.0, 3.05, "Metal_Silver", col_ben)
    add_box("Ben_BBall_Board", 40.3, 41.5, -6.98, -6.88, 2.45, 3.25, "Frame_Window", col_ben)
    add_box("Ben_BBall_Rim", 40.68, 41.12, -6.88, -6.48, 2.55, 2.63, "Gate_Yellow", col_ben)

    # Zwei große Gartenbäume im hinteren Garten
    for idx, (tx, ty, r_crown) in enumerate([(29.0, 15.0, 2.8), (44.5, 13.5, 2.4)]):
        add_box(f"Ben_Tree_{idx}_Trunk", tx - 0.35, tx + 0.35, ty - 0.35, ty + 0.35, 0.0, 2.8, "Tree_Trunk", col_ben)
        add_box(f"Ben_Tree_{idx}_Crown1", tx - r_crown, tx + r_crown, ty - r_crown, ty + r_crown, 2.4, 5.6, "Tree_Leaves", col_ben)
        add_box(f"Ben_Tree_{idx}_Crown2", tx - 0.7 * r_crown, tx + 0.7 * r_crown, ty - 0.7 * r_crown, ty + 0.7 * r_crown, 5.2, 6.8, "Tree_Leaves", col_ben)

    return col_ben
