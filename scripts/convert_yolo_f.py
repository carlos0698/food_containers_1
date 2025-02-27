import os
import json

# Ruta al disco externo
external_disk = "/Volumes/Disco Ana/food_containers"

# Rutas de los archivos
data_dir = os.path.join(external_disk, "data")
annotations_file = os.path.join(data_dir, "filtered", "annotations", "filtered_annotations_val_3.json")
images_dir = os.path.join(data_dir, "filtered", "images")
output_dir = os.path.join(data_dir, "filtered", "val_annotations")

# Crear la carpeta de salida si no existe
os.makedirs(output_dir, exist_ok=True)

# Cargar las anotaciones filtradas
with open(annotations_file, "r") as f:
    annotations = json.load(f)

# Mapeo de categorías a IDs de YOLO
category_map = {cat["id"]: idx for idx, cat in enumerate(annotations["categories"])}

# Procesar cada imagen
for img in annotations["images"]:
    img_id = img["id"]
    img_file_name = img["file_name"]
    img_width = img["width"]
    img_height = img["height"]

    # Filtrar anotaciones para esta imagen
    img_annotations = [ann for ann in annotations["annotations"] if ann["image_id"] == img_id]

    # Crear el archivo de anotaciones en formato YOLO
    yolo_annotations = []
    for ann in img_annotations:
        category_id = category_map[ann["category_id"]]
        bbox = ann["bbox"]  # [x_min, y_min, width, height]
        
        # Convertir a formato YOLO (normalizado)
        x_center = (bbox[0] + bbox[2] / 2) / img_width
        y_center = (bbox[1] + bbox[3] / 2) / img_height
        width = bbox[2] / img_width
        height = bbox[3] / img_height

        yolo_annotations.append(f"{category_id} {x_center} {y_center} {width} {height}")

    # Guardar las anotaciones en un archivo .txt
    output_file = os.path.join(output_dir, img_file_name.replace(".jpg", ".txt"))
    with open(output_file, "w") as f:
        f.write("\n".join(yolo_annotations))

print("Anotaciones convertidas a formato YOLO.")