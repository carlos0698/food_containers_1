import json
import os

# Ruta del archivo COCO JSON
coco_file = "/Volumes/Disco Ana/food_containers/data/filtered/fine_tunning_images.json"

# Ruta de la carpeta con las imágenes
images_folder = "/Volumes/Disco Ana/food_containers/data/filtered/resized_images"

# Ruta de la carpeta donde se guardarán las anotaciones en formato YOLO
output_folder = "/Volumes/Disco Ana/food_containers/data/filtered/annotations_fine_tunning"

# Crear la carpeta de salida si no existe
os.makedirs(output_folder, exist_ok=True)

# Cargar el archivo COCO
with open(coco_file, "r") as f:
    coco_data = json.load(f)

# Crear un diccionario para mapear category_id a class_id
category_id_to_class_id = {
    category["id"]: idx for idx, category in enumerate(coco_data["categories"])
}

# Procesar cada imagen
for image_info in coco_data["images"]:
    image_id = image_info["id"]
    image_filename = image_info["file_name"]
    image_width = image_info["width"]
    image_height = image_info["height"]

    # Filtrar anotaciones para esta imagen
    annotations = [
        ann for ann in coco_data["annotations"] if ann["image_id"] == image_id
    ]

    # Crear el archivo de anotaciones en formato YOLO
    yolo_annotations = []
    for ann in annotations:
        category_id = ann["category_id"]
        class_id = category_id_to_class_id[category_id]

        # Obtener las coordenadas del bounding box
        x, y, width, height = ann["bbox"]

        # Convertir a formato YOLO (normalizado)
        x_center = (x + width / 2) / image_width
        y_center = (y + height / 2) / image_height
        norm_width = width / image_width
        norm_height = height / image_height

        # Añadir la anotación al archivo YOLO
        yolo_annotations.append(f"{class_id} {x_center} {y_center} {norm_width} {norm_height}")

    # Guardar las anotaciones en un archivo de texto
    output_filename = os.path.splitext(image_filename)[0] + ".txt"
    output_path = os.path.join(output_folder, output_filename)
    with open(output_path, "w") as f:
        f.write("\n".join(yolo_annotations))

    print(f"Anotaciones para {image_filename} guardadas en {output_filename}")