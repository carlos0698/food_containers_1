import torch
import torchvision.transforms as T
from torchvision.transforms import functional as F
from PIL import Image
import os
import random

# Rutas de carpetas (ajusta según tus necesidades)
input_images_folder = "/Volumes/Disco Ana/food_containers/data/filtered/images_ft"
input_labels_folder = "/Volumes/Disco Ana/food_containers/data/filtered/labels_ft"
output_images_folder = "/Volumes/Disco Ana/food_containers/data/filtered/augmented_images"
output_labels_folder = "/Volumes/Disco Ana/food_containers/data/filtered/augmented_labels"

# Crear carpetas de salida si no existen
os.makedirs(output_images_folder, exist_ok=True)
os.makedirs(output_labels_folder, exist_ok=True)

# Número de imágenes aumentadas por imagen original
num_augmented_images = 5

# Definir las transformaciones de aumento de datos (solo color y brillo)
transform = T.Compose([
    T.ColorJitter(brightness=0.5, contrast=0.5, saturation=0.5),  # Cambio de brillo, contraste y saturación
])

# Recorrer todas las imágenes en la carpeta de entrada
for filename in os.listdir(input_images_folder):
    if filename.lower().endswith((".png", ".jpg", ".jpeg")):
        # Cargar la imagen
        image_path = os.path.join(input_images_folder, filename)
        image = Image.open(image_path)

        # Cargar las anotaciones (YOLO format)
        label_filename = os.path.splitext(filename)[0] + ".txt"
        label_path = os.path.join(input_labels_folder, label_filename)

        # Parsear las anotaciones
        bboxes = []
        class_labels = []
        try:
            with open(label_path, "r") as f:
                lines = f.readlines()

            for line in lines:
                # Ignorar líneas vacías o mal formateadas
                if line.strip():  # Verifica que la línea no esté vacía
                    values = line.split()
                    if len(values) == 5:  # Verifica que la línea tenga exactamente 5 valores
                        class_id, x_center, y_center, width, height = map(float, values)
                        bboxes.append([x_center, y_center, width, height])
                        class_labels.append(int(class_id))
                    else:
                        print(f"Advertencia: Formato incorrecto en {label_path}, línea: {line.strip()}")
        except FileNotFoundError:
            print(f"Advertencia: No se encontró el archivo de anotaciones {label_path}")
            continue

        # Convertir la imagen a un tensor de PyTorch
        image_tensor = F.to_tensor(image)

        # Aplicar data augmentation a la imagen
        for i in range(num_augmented_images):
            # Aplicar transformaciones de color y brillo
            augmented_image_tensor = transform(image_tensor)

            # Convertir la imagen aumentada de vuelta a PIL Image
            augmented_image = F.to_pil_image(augmented_image_tensor)

            # Guardar la imagen aumentada
            output_image_filename = f"{os.path.splitext(filename)[0]}_aug_{i}.jpg"
            output_image_path = os.path.join(output_images_folder, output_image_filename)
            augmented_image.save(output_image_path)

            # Guardar las anotaciones (no cambian)
            output_label_filename = f"{os.path.splitext(filename)[0]}_aug_{i}.txt"
            output_label_path = os.path.join(output_labels_folder, output_label_filename)
            with open(output_label_path, "w") as f:
                for bbox, class_id in zip(bboxes, class_labels):
                    f.write(f"{class_id} {bbox[0]} {bbox[1]} {bbox[2]} {bbox[3]}\n")

            print(f"Imagen aumentada {output_image_filename} y anotaciones guardadas")