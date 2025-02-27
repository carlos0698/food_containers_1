

import os
import json

# Ruta al disco externo
external_disk = "/Volumes/Disco Ana/food_containers"

# Directorio donde están los JSON
annotations_dir = os.path.join(external_disk, "data","filtered","annotations")

# Lista de archivos a combinar
archivos = [
    os.path.join(annotations_dir, "filtered_annotations_val_1.json"),
    os.path.join(annotations_dir, "filtered_annotations_val_2.json"),
    os.path.join(annotations_dir, "filtered_annotations_val_3.json")
]

# Lista donde vamos a ir agregando cada JSON
coco_combinado = []

for archivo in archivos:
    with open(archivo, "r", encoding="utf-8") as f:
        datos = json.load(f)
        coco_combinado.append(datos)  # Agregar cada archivo como un bloque separado

# Crear carpeta de salida si no existe
output_dir = os.path.join(external_disk, "data", "filtered")
os.makedirs(output_dir, exist_ok=True)

# Guardar el JSON combinado
output_file = os.path.join(output_dir, "filtered_annotations_val.json")
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(coco_combinado, f, indent=4)

print(f"✅ Archivos COCO combinados correctamente en '{output_file}'")
