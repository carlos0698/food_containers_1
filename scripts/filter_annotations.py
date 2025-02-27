import os
import json
from pycocotools.coco import COCO

# Ruta al disco externo
external_disk = "/Volumes/Disco Ana/food_containers"

# Rutas de los archivos
data_dir = os.path.join(external_disk, "data")
annotations_file = os.path.join(data_dir, "annotations", "instances_val2017.json")
output_dir = os.path.join(data_dir, "filtered", "annotations")

# Crear la carpeta de salida si no existe
os.makedirs(output_dir, exist_ok=True)

# Cargar las anotaciones
coco = COCO(annotations_file)

# Leer los IDs de las imágenes filtradas
with open(os.path.join(data_dir, "filtered", "filtered_image_ids_1.txt"), "r") as f:
    image_ids = [int(line.strip()) for line in f.readlines()]

# Filtrar las anotaciones
filtered_annotations = []
for ann in coco.dataset["annotations"]:
    if ann["image_id"] in image_ids:
        filtered_annotations.append(ann)

# Filtrar las imágenes
filtered_images = coco.loadImgs(image_ids)

# Guardar las anotaciones filtradas en un nuevo archivo JSON
filtered_data = {
    "info": coco.dataset["info"],
    "licenses": coco.dataset["licenses"],
    "images": filtered_images,
    "annotations": filtered_annotations,
    "categories": coco.loadCats(coco.getCatIds()),
}

with open(os.path.join(output_dir, "filtered_annotations_val_3.json"), "w") as f:
    json.dump(filtered_data, f)

print("Anotaciones filtradas guardadas en 'filtered_annotations_val_3.json'.")