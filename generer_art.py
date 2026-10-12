import gdstk
import os

MACRO_NAME = "silicon_art"
TEXT = "MARIUS"
TEXT_SIZE = 10
LAYER = 70      # <--- CHANGÉ : Couche Metal 3 (Beaucoup plus permissive pour le DRC)
DATATYPE = 0
TARGET_LOGO_WIDTH = 40.0

lib = gdstk.Library()
art_cell = lib.new_cell(MACRO_NAME)

# 1. Génération du texte
text_polys = gdstk.text(TEXT, TEXT_SIZE, (0, 0), layer=LAYER, datatype=DATATYPE)
for p in text_polys:
    art_cell.add(p)

text_bbox = art_cell.bounding_box()
text_height = text_bbox[1][1] - text_bbox[0][1] if text_bbox else 0

# 2. Ajout, Mise à l'échelle et Changement de couche du Logo
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

        # Polygones pleins
        for poly in logo_cell.polygons:
            poly.scale(scale_factor)
            poly.layer = LAYER
            poly.datatype = DATATYPE
            poly.translate(x_offset, y_offset)
            art_cell.add(poly)
            
        # Chemins (Lignes)
        for path in logo_cell.paths:
            path.scale(scale_factor)
            path.translate(x_offset, y_offset)
            for path_poly in path.to_polygons():
                path_poly.layer = LAYER
                path_poly.datatype = DATATYPE
                art_cell.add(path_poly)
else:
    print(f"⚠️ Attention : {logo_path} introuvable.")

# 3. Recalibrage global
bbox = art_cell.bounding_box()
if bbox:
    x_shift = 1.0 - bbox[0][0]
    y_shift = 1.0 - bbox[0][1]

    for p in art_cell.polygons + art_cell.paths:
        p.translate(x_shift, y_shift)

    bbox = art_cell.bounding_box()
    width = bbox[1][0] + 1.0
    height = bbox[1][1] + 1.0
else:
    width, height = 1.0, 1.0

# --- PR BOUNDARY (Obligatoire pour OpenLane) ---
PR_BNDRY_LAYER = 235
PR_BNDRY_DATATYPE = 4
pr_box = gdstk.rectangle((0.0, 0.0), (width, height), layer=PR_BNDRY_LAYER, datatype=PR_BNDRY_DATATYPE)
art_cell.add(pr_box)

# 4. Sauvegarde
lib.write_gds(f"macros/{MACRO_NAME}.gds")

# 5. Fichier LEF (On indique au routeur d'éviter le Metal 3 ici)
lef_content = f"""MACRO {MACRO_NAME}
  CLASS BLOCK ;
  SIZE {width:.3f} BY {height:.3f} ;
  ORIGIN 0.0 0.0 ;
  OBS
    LAYER met3 ;
      RECT 0.0 0.0 {width:.3f} {height:.3f} ;
  END
END {MACRO_NAME}
"""
with open(f"macros/{MACRO_NAME}.lef", "w") as f:
    f.write(lef_content)

print(f"✅ Art combiné généré pour le Metal 3 ! Dimensions : {width:.2f}µm x {height:.2f}µm")
