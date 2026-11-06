#!/usr/bin/env python3
"""Texturkatalog fürs Haus (2026-11-06): id -> (Flow-Beschreibung, Meter je Bild, Modus).
Modus 'kachel' = nahtlos kachelnd (Weltmaß), 'fit' = ein Bild je Fläche (Türen).
Ausgabe: make_textur_jobs() -> jobs_texturen.json für agy_generate_image.py batch."""
import json, os
E = os.path.dirname(os.path.abspath(__file__))
STIL = ("Seamless tileable texture, perfectly flat top-down orthographic view, fills the whole image edge to edge, even soft ambient light, "
        "no shadows, no highlights, no reflections, no perspective, matte albedo only, stylized 3D-animation painted look (Pixar-like, clean, warm), "
        "no text, no letters, no logos, no objects lying on it, no border, no vignette. ")
T = {
 # --- Böden, je Raum individuell
 "floor_eg_flur":        ("terracotta and cream square ceramic floor tiles in a checker arrangement, 4 by 4 tiles visible, thin light grout lines, slightly worn", 1.6, "kachel"),
 "floor_eg_wohnzimmer":  ("warm honey oak herringbone parquet floor, about 8 by 8 plank rows visible, fine wood grain", 1.2, "kachel"),
 "floor_eg_kueche":      ("sage-green and cream checkerboard ceramic kitchen floor tiles, 4 by 4 tiles visible, thin grout", 1.2, "kachel"),
 "floor_eg_spielzimmer": ("soft pale blue-grey rubber play floor with tiny confetti speckles in yellow, coral and teal", 1.2, "kachel"),
 "floor_eg_gaesteklo":   ("small white hexagonal bathroom floor tiles with light grey grout, many tiles visible", 0.6, "kachel"),
 "floor_og_bad":         ("small turquoise and white square mosaic bathroom tiles, fine grout, many tiles visible", 0.6, "kachel"),
 "floor_og_flur":        ("dark walnut wide wooden plank floor, 5 planks visible running in one direction, subtle grain", 1.2, "kachel"),
 "floor_og_kinderzimmer":("light birch wooden plank floor, 6 planks visible running in one direction, soft grain, friendly", 1.2, "kachel"),
 "floor_og_eltern":      ("calm warm grey-brown oak wide plank floor, 5 planks visible running in one direction", 1.2, "kachel"),
 "floor_dg_dachboden":   ("old weathered dusty wide wooden attic floor planks with few nails and knots, 5 planks visible", 1.2, "kachel"),
 "floor_garage":         ("light grey concrete garage floor with faint oil stains and fine hairline cracks", 2.0, "kachel"),
 # --- Wände, Dach, Fassade
 "wall_interior":        ("very fine off-white cream woodchip wallpaper plaster, soft subtle grain", 1.0, "kachel"),
 "wall_exterior":        ("warm cream-yellow stucco facade plaster with fine sandy grain", 1.5, "kachel"),
 "roof_tiles":           ("terracotta red-brown clay roof tiles in overlapping rows, 6 rows visible", 1.2, "kachel"),
 "brick_red":            ("red-brown brick wall with light mortar joints, running bond, about 10 rows visible", 1.2, "kachel"),
 "slate_roof":           ("dark grey-blue slate roof shingles in overlapping rows", 1.0, "kachel"),
 "plaster_mint":         ("soft mint green stucco wall plaster with fine grain", 1.5, "kachel"),
 # --- Außen
 "fence_wood":           ("weathered brown wooden fence boards, vertical planks with grain and a few knots", 1.0, "kachel"),
 "terrace_deck":         ("outdoor grey-brown wooden decking planks with thin gaps, 6 planks visible", 1.2, "kachel"),
 "paving_path":          ("beige-grey irregular flagstone garden path paving with thin grass-free joints", 1.5, "kachel"),
 "paving_blocks":        ("light grey rectangular concrete paving blocks in running bond, thin joints", 1.2, "kachel"),
 "asphalt":              ("dark grey street asphalt with fine gravel grain and tiny hairline cracks", 2.0, "kachel"),
 "grass_lawn":           ("lush green mown lawn grass seen from above, fine blades, natural variation", 2.0, "kachel"),
 "meadow":               ("wild green meadow with clover and a few tiny white flowers seen from above", 2.0, "kachel"),
 "foliage":              ("dense green leaves foliage hedge texture, many overlapping leaves in several greens", 1.0, "kachel"),
 "bark":                 ("brown tree bark with vertical grooves", 1.0, "kachel"),
 "curb_granite":         ("grey granite curb stone surface with fine speckles", 1.0, "kachel"),
 "garage_door":          ("white sectional garage door panels with horizontal grooves, 4 panels visible, no handle", 1.2, "kachel"),
 "shed_wood":            ("reddish-brown vertical wooden shed boards with grain", 1.0, "kachel"),
 "bitumen_roof":         ("dark grey-green bitumen roof shingles in rows", 1.0, "kachel"),
 # --- Türen, Rahmen, Küche, Holz
 "door_leaf":            ("a single white painted wooden interior door with six raised rectangular panels, seen straight from the front, the door fills the whole image, plain white background not needed", 0.9, "fit"),
 "door_front":           ("a single dark teal painted wooden front door with vertical raised panels and a brass letter slot, seen straight from the front, fills the whole image", 0.9, "fit"),
 "paint_white":          ("smooth white painted wood with very fine brush grain, clean, for window frames and trim", 0.6, "kachel"),
 "kitchen_sage":         ("sage green painted wood with subtle brush grain for kitchen cabinets", 0.6, "kachel"),
 "counter_oak":          ("oak butcher-block kitchen countertop wood, light honey colour, strips visible", 1.0, "kachel"),
 "wood_dark":            ("dark walnut wood grain surface for furniture", 1.0, "kachel"),
 "wood_medium":          ("medium oak wood grain surface for furniture", 1.0, "kachel"),
 "wood_light":           ("light pine wood grain surface for furniture", 1.0, "kachel"),
 "stair_wood":           ("warm medium oak wood stair stringer panel wood with fine vertical grain, clean", 1.0, "kachel"),
 # --- Stoffe
 "sofa_floral":          ("retro golden-yellow floral upholstery fabric with cream and coral flowers and green leaves", 0.8, "kachel"),
 "rug_blue":             ("woven wool rug with geometric diamond pattern in navy blue and cream", 1.0, "kachel"),
 "rug_terra":            ("woven wool rug with terracotta and cream stripe and diamond pattern", 1.0, "kachel"),
 "rug_play":             ("colourful children's play rug pattern with little roads, small houses and trees seen from above, soft pastel colours", 1.2, "kachel"),
}
def make_textur_jobs():
    jobs = []
    for k, (txt, m, mode) in T.items():
        jobs.append({"id": k, "style": "none", "out": f"{E}/Texturen/roh/{k}.jpg", "refs": [],
                     "prompt": ("" if mode == "fit" else STIL) + ("Straight-on front view, stylized 3D-animation painted look (Pixar-like), flat even light, no shadows, no text. " if mode == "fit" else "") + txt + ". Landscape 16:9."})
    json.dump({"jobs": jobs}, open(f"{E}/jobs_texturen.json", "w"), ensure_ascii=False, indent=1)
    return len(jobs)
if __name__ == "__main__":
    print(make_textur_jobs(), "Texturen")
