import os
import shutil

# Ruta al disco externo
external_disk = "/Volumes/Disco Ana/food_containers"

# Rutas de las carpetas
data_dir = os.path.join(external_disk, "data")
image_ids_file = os.path.join(data_dir, "filtered", "filtered_image_ids_1.txt")
images_dir = os.path.join(data_dir, "trainl2017")  # Cambiae a val2017 si es validación
output_dir = os.path.join(data_dir, "filtered", "val")

# Crear la carpeta de salida si no existe
os.makedirs(output_dir, exist_ok=True)

# Leer los IDs de las imágenes
with open(image_ids_file, "r") as f:
    image_ids = [line.strip() for line in f.readlines()]

# Copiar las imágenes filtradas
for img_id in image_ids:
    img_file_name = f"{int(img_id):012d}.jpg"  # Formato: 000000532505.jpg
    img_path = os.path.join(images_dir, img_file_name)
    output_path = os.path.join(output_dir, img_file_name)
    
    # Copiar la imagen
    if os.path.exists(img_path):
        shutil.copy(img_path, output_path)
        print(f"Copiada: {img_path} -> {output_path}")
    else:
        print(f"Imagen no encontrada: {img_path}")

print("Copia completada.")