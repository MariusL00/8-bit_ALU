import gdstk
import os

MACRO_NAME = "silicon_art"
TEXT = "MARIUS"
TEXT_SIZE = 10
LAYER = 72         # Metal 5 (Pour le visuel)
DATATYPE_ART = 44  # 44 = Annotation (Totalement ignoré par le DRC)
TARGET_LOGO_WIDTH = 40.0

lib = gdstk.Library()
art_cell = lib.new_cell(MACRO_NAME)

# 1. Texte (Visuel -> Type 44)
text_polys = gdstk.text(TEXT, TEXT_SIZE, (0, 0), layer=LAYER, datatype=DATATYPE_ART)
for p in text_polys:
    art_cell.add(p)
text_bbox = art_cell.bounding_box()
text_height = text_bbox[1][1] - text_bbox[0][1] if text_bbox else 0

# 2. Logo (Visuel -> Type 44)
logo_path = "macros/logo_brut.gds"
if os.path.exists(logo_path):
    logo_lib = gdstk.read_gds(logo_path)
    logo_cell = logo_lib.top_level()[0]
    logo_bbox = logo_cell.bounding_box()
    if logo_bbox:
        current_width = logo_bbox[1][0] - logo_bbox[0][0]
        scale_factor = TARGET_LOGO_WIDTH / current_width
        x_offset = -(logo_bbox[0][0] * scale_factor)
        y_offset = text_height + 5.0 - (logo_bbox[0][1] * scale_factor)
        for poly in logo_cell.polygons:
            poly.scale(scale_factor)
            poly.layer = LAYER
            poly.datatype = DATATYPE_ART
            poly.translate(x_offset, y_offset)
            art_cell.add(poly)
        for path in logo_cell.paths:
            path.scale(scale_factor)
            path.translate(x_offset, y_offset)
            for path_poly in path.to_polygons():
                path_poly.layer = LAYER
                path_poly.datatype = DATATYPE_ART
                art_cell.add(path_poly)

# 3. Recalibrage global
bbox = art_cell.bounding_box()
if bbox:
    x_shift = -bbox[0][0]
    y_shift = -bbox[0][1]
    for p in art_cell.polygons + art_cell.paths:
        p.translate(x_shift, y_shift)
    bbox = art_cell.bounding_box()
    width = bbox[1][0]
    height = bbox[1][1]
else:
    width, height = 1.0, 1.0

# --- L'ANCRAGE LVS PHYSIQUE ---
# Couche 69 (Metal 2), Datatype 20 (VRAI METAL). 
# Ce carré parfait de 1x1 µm passera le DRC sans aucun problème.
art_cell.add(gdstk.rectangle((0.0, 0.0), (1.0, 1.0), layer=69, datatype=20))
art_cell.add(gdstk.Label("DUMMY", (0.5, 0.5), layer=69, texttype=16))

# PR BOUNDARY globale
pr_box = gdstk.rectangle((0.0, 0.0), (width, height), layer=235, datatype=4)
art_cell.add(pr_box)

lib.write_gds(f"macros/{MACRO_NAME}.gds")

# --- LE LEF (Inchangé) ---
lef_content = f"""MACRO {MACRO_NAME}
  CLASS COVER ;
  SIZE {width:.3f} BY {height:.3f} ;
  ORIGIN 0.000 0.000 ;
  PIN DUMMY
    DIRECTION OUTPUT ;
    PORT
      LAYER met2 ;
        RECT 0.000 0.000 1.000 1.000 ;
    END
  END DUMMY
END {MACRO_NAME}
"""
with open(f"macros/{MACRO_NAME}.lef", "w") as f:
    f.write(lef_content)

print(f"✅ Macro générée : Art en annotation (44), Ancrage LVS en physique (20).")
