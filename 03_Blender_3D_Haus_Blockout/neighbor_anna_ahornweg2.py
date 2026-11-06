# -*- coding: utf-8 -*-
"""
Ahornweg 2 – Annas Nachbarhaus (westlich von Maxis Grundstück).
Kompakter Außen-Blockout (ohne Innenausbau) aus Quadern und Satteldach-Elementen.
Grundstück: X = -52.0 .. -19.0 (33 m), Y = -14.0 .. +22.0 (36 m).
"""


def build_anna_house(add_box, add_pitched_prism, add_sloped_slab, get_collection, make_mat):
    col_anna = get_collection("04_Nachbarhaus_Anna_Ahornweg2")

    # Materialien
    m_mint = make_mat("Anna_Wall_Mint", (0.74, 0.87, 0.79, 1.0))
    m_frame = make_mat("Frame_Window", (0.95, 0.96, 0.97, 1.0))
    m_slate = make_mat("Anna_Roof_Slate", (0.28, 0.33, 0.40, 1.0))
    m_glass = make_mat("Anna_Window_Glass", (0.68, 0.82, 0.92, 1.0))
    m_door = make_mat("Door_Front", (0.44, 0.27, 0.15, 1.0))
    m_wood = make_mat("Fence_Wood", (0.56, 0.39, 0.24, 1.0))
    m_stone = make_mat("Anna_Path_Stone", (0.66, 0.65, 0.62, 1.0))
    m_lawn = make_mat("Anna_Lawn_Green", (0.37, 0.56, 0.29, 1.0))
    m_leaf = make_mat("Anna_Tree_Foliage", (0.25, 0.49, 0.23, 1.0))
    m_flower = make_mat("Anna_Flower_Bloom", (0.88, 0.47, 0.60, 1.0))

    def _slab(name, x0, x1, y0, y1, z0, z1, thick, mat):
        vn = add_sloped_slab.__code__.co_varnames
        if len(vn) > 7 and vn[7].startswith("m"):
            return add_sloped_slab(name, x0, x1, y0, y1, z0, z1, mat, col_anna)
        return add_sloped_slab(name, x0, x1, y0, y1, z0, z1, thick, mat, col_anna)

    def _win(name, x0, x1, y0, y1, z0, z1):
        add_box(f"{name}_Frame", x0, x1, y0, y1, z0, z1, m_frame, col_anna)
        dx = 0.08 if (x1 - x0) > 0.3 else 0.02
        dy = 0.08 if (y1 - y0) > 0.3 else 0.02
        add_box(f"{name}_Glass", x0 + dx, x1 - dx, y0 + dy, y1 - dy, z0 + 0.08, z1 - 0.08, m_glass, col_anna)

    # 1. Grundstücksbasis & Wege
    add_box("Anna_Ground_Lawn", -52.0, -19.0, -14.0, 22.0, -0.15, 0.0, m_lawn, col_anna)
    add_box("Anna_Path_Front", -36.0, -34.0, -14.0, -7.8, 0.0, 0.04, m_stone, col_anna)
    add_box("Anna_Path_To_MaxiGate", -27.0, -19.0, 1.2, 2.4, 0.0, 0.04, m_stone, col_anna)
    add_box("Anna_Path_ErkerLink", -27.0, -22.5, -2.8, 1.2, 0.0, 0.03, m_stone, col_anna)

    # 2. Hauptgebäude (X = -43.0 .. -27.0, Y = -5.5 .. +5.5, Z = 0.0 .. 5.4) + Satteldach
    add_box("Anna_Main_Plinth", -43.1, -26.9, -5.6, 5.6, 0.0, 0.25, m_stone, col_anna)
    add_box("Anna_Main_House", -43.0, -27.0, -5.5, 5.5, 0.2, 5.4, m_mint, col_anna)
    add_box("Anna_Trim_Belt", -43.06, -26.94, -5.56, 5.56, 2.65, 2.80, m_frame, col_anna)
    add_pitched_prism("Anna_Roof_GableCore", -43.0, -27.0, -5.5, 5.5, 5.4, 8.2, m_mint, col_anna, peak_axis='Y')
    add_sloped_slab("Anna_Roof_South", -43.6, -26.4, -6.1, 5.2, 0.0, 8.2, 0.22, m_slate, col_anna)
    add_sloped_slab("Anna_Roof_North", -43.6, -26.4, 6.1, 5.2, 0.0, 8.2, 0.22, m_slate, col_anna)
    add_box("Anna_Chimney", -31.5, -30.5, 1.2, 2.2, 6.5, 8.7, m_stone, col_anna)

    # 3. Wintergarten / Erker-Anbau Richtung Maxis Garten (X = -27.0 .. -23.5, Y = -2.5 .. +3.5, Z = 0.0 .. 3.4)
    add_box("Anna_Sunroom_Base", -27.0, -23.4, -2.6, 3.6, 0.0, 0.25, m_stone, col_anna)
    add_box("Anna_Sunroom_Body", -27.0, -23.5, -2.5, 3.5, 0.2, 3.2, m_mint, col_anna)
    add_box("Anna_Sunroom_Roof", -27.1, -23.2, -2.8, 3.8, 3.2, 3.45, m_slate, col_anna)
    _win("Anna_Sunroom_Win_E1", -23.55, -23.45, -2.0, 0.5, 0.45, 2.95)
    _win("Anna_Sunroom_Win_E2", -23.55, -23.45, 0.7, 3.0, 0.45, 2.95)
    _win("Anna_Sunroom_Win_S", -26.6, -23.9, -2.55, -2.45, 0.45, 2.95)
    _win("Anna_Sunroom_Win_N", -26.6, -23.9, 3.45, 3.55, 0.45, 2.95)

    # 4. Gemütliche Holzveranda vorne (X = -38.5 .. -31.5, Y = -7.8 .. -5.5) + Haustür
    add_box("Anna_Porch_Deck", -38.5, -31.5, -7.8, -5.5, 0.0, 0.25, m_wood, col_anna)
    add_box("Anna_Porch_Step", -36.0, -34.0, -8.2, -7.8, 0.0, 0.13, m_stone, col_anna)
    add_box("Anna_Porch_Roof", -38.7, -31.3, -8.0, -5.4, 2.95, 3.2, m_slate, col_anna)
    for idx, px in enumerate((-38.3, -36.2, -33.8, -31.7)):
        add_box(f"Anna_Porch_Post_{idx}", px - 0.08, px + 0.08, -7.7, -7.54, 0.25, 2.95, m_frame, col_anna)
    add_box("Anna_Porch_Rail_L", -38.4, -36.2, -7.7, -7.55, 0.85, 0.98, m_frame, col_anna)
    add_box("Anna_Porch_Rail_R", -33.8, -31.6, -7.7, -7.55, 0.85, 0.98, m_frame, col_anna)
    add_box("Anna_Planter_L", -38.3, -36.4, -7.95, -7.65, 0.25, 0.65, m_wood, col_anna)
    add_box("Anna_Flowers_L", -38.2, -36.5, -7.9, -7.7, 0.65, 0.85, m_flower, col_anna)
    add_box("Anna_Planter_R", -33.6, -31.7, -7.95, -7.65, 0.25, 0.65, m_wood, col_anna)
    add_box("Anna_Flowers_R", -33.5, -31.8, -7.9, -7.7, 0.65, 0.85, m_flower, col_anna)

    # Haustür & Außenfenster
    add_box("Anna_Front_Door_Frame", -35.75, -34.25, -5.58, -5.45, 0.25, 2.45, m_frame, col_anna)
    add_box("Anna_Front_Door", -35.6, -34.4, -5.62, -5.48, 0.25, 2.35, m_door, col_anna)
    for i, (wx0, wx1) in enumerate(((-41.5, -39.2), (-30.8, -28.5))):
        _win(f"Anna_Win_S_EG_{i}", wx0, wx1, -5.56, -5.44, 0.9, 2.2)
        _win(f"Anna_Win_S_OG_{i}", wx0, wx1, -5.56, -5.44, 3.3, 4.6)
        _win(f"Anna_Win_N_EG_{i}", wx0, wx1, 5.44, 5.56, 0.9, 2.2)
        _win(f"Anna_Win_N_OG_{i}", wx0, wx1, 5.44, 5.56, 3.3, 4.6)
    _win("Anna_Win_S_OG_Mid", -36.1, -33.9, -5.56, -5.44, 3.3, 4.6)
    _win("Anna_Win_Gable_W", -43.06, -42.94, -1.2, 1.2, 5.8, 7.1)
    _win("Anna_Win_Gable_E", -27.06, -26.94, -1.2, 1.2, 5.8, 7.1)
    _win("Anna_Win_W_EG", -43.06, -42.94, -2.5, 2.5, 0.9, 2.2)

    # 5. Gartenzaun (Süd mit Torlücke X = -36.2 .. -33.8, West X = -52.0, Nord Y = +22.0)
    add_box("Anna_Fence_South_W", -52.0, -36.2, -14.08, -13.92, 0.0, 1.15, m_wood, col_anna)
    add_box("Anna_Fence_South_E", -33.8, -19.0, -14.08, -13.92, 0.0, 1.15, m_wood, col_anna)
    add_box("Anna_Gate_Post_W", -36.35, -36.15, -14.12, -13.88, 0.0, 1.35, m_wood, col_anna)
    add_box("Anna_Gate_Post_E", -33.85, -33.65, -14.12, -13.88, 0.0, 1.35, m_wood, col_anna)
    add_box("Anna_Fence_West", -52.08, -51.92, -14.0, 22.0, 0.0, 1.15, m_wood, col_anna)
    add_box("Anna_Fence_North", -52.0, -19.0, 21.92, 22.08, 0.0, 1.15, m_wood, col_anna)

    # 6. Garten-Objekte (Blumenbeete vorne, Kletterturm/Spielhaus hinten, Apfelbaum)
    add_box("Anna_Flowerbed_W_Border", -42.5, -37.5, -12.2, -9.8, 0.0, 0.22, m_stone, col_anna)
    add_box("Anna_Flowerbed_W_Bloom", -42.3, -37.7, -12.0, -10.0, 0.22, 0.55, m_flower, col_anna)
    add_box("Anna_Flowerbed_E_Border", -32.5, -27.5, -12.2, -9.8, 0.0, 0.22, m_stone, col_anna)
    add_box("Anna_Flowerbed_E_Bloom", -32.3, -27.7, -12.0, -10.0, 0.22, 0.55, m_flower, col_anna)

    add_box("Anna_Playhouse_Tower", -46.5, -43.5, 11.0, 14.0, 0.0, 2.8, m_wood, col_anna)
    add_box("Anna_Playhouse_Roof", -46.8, -43.2, 10.7, 14.3, 2.8, 3.4, m_slate, col_anna)
    add_box("Anna_Tree_Trunk", -30.4, -29.6, 12.6, 13.4, 0.0, 2.6, m_door, col_anna)
    add_box("Anna_Tree_Crown_Main", -32.8, -27.2, 10.2, 15.8, 2.3, 5.4, m_leaf, col_anna)
    add_box("Anna_Tree_Crown_Top", -31.8, -28.2, 11.2, 14.8, 5.2, 6.6, m_leaf, col_anna)

    return col_anna
