import os
import json
from pycocotools.coco import COCO

# Ruta al disco externo
external_disk = "/Volumes/Disco Ana/food_containers"

# Rutas de los archivos
data_dir = os.path.join(external_disk, "data")
annotations_file = os.path.join(data_dir, "annotations", "image_info_test-dev2017.json")  # Archivo correcto
output_dir = os.path.join(data_dir, "filtered")

# Crear la carpeta de salida si no existe
os.makedirs(output_dir, exist_ok=True)

# Cargar las anotaciones
coco = COCO(annotations_file)

# Definir las categorías que quieres filtrar
categories = ["bowl"]

category_ids = coco.getCatIds(catNms=categories)

# Obtener los IDs de las imágenes que contienen estas categorías
image_ids = coco.getImgIds(catIds=category_ids)

# Guardar los IDs en un archivo
with open(os.path.join(output_dir, "filtered_image_ids_3.txt"), "w") as f:
    for img_id in image_ids:
        f.write(f"{img_id}\n")

print(f"Se encontraron {len(image_ids)} imágenes. Los IDs se guardaron en 'filtered_image_ids_3.txt'.")


