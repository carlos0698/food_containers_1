from PIL import Image
import os

# Ruta de la carpeta con las imágenes originales
input_folder = "/Volumes/Disco Ana/food_containers/data/filtered/fine_tunning_images_2"

# Ruta de la carpeta donde se guardarán las imágenes redimensionadas
output_folder = "/Volumes/Disco Ana/food_containers/data/filtered/resized_images_ft"

# Crear la carpeta de salida si no existe
os.makedirs(output_folder, exist_ok=True)

# Tamaño deseado (512x512)
new_size = (512, 512)

# Contador para renombrar las imágenes
counter = 1

# Recorrer todas las imágenes en la carpeta de entrada
for filename in os.listdir(input_folder):
    # Ignorar archivos ocultos (comienzan con "." o "_")
    if filename.startswith(".") or filename.startswith("_"):
        print(f"Ignorando archivo oculto: {filename}")
        continue

    # Solo procesar archivos de imagen válidos
    if filename.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):
        # Cargar la imagen
        image_path = os.path.join(input_folder, filename)
        try:
            image = Image.open(image_path)
        except Exception as e:
            print(f"No se pudo abrir {filename}: {e}")
            continue

        # Convertir imágenes PNG a JPG (o mantener el formato original)
        if filename.lower().endswith(".png"):
            # Convertir a JPG
            image = image.convert("RGB")  # Convertir a modo RGB (necesario para JPG)
            output_extension = ".jpg"
        else:
            # Mantener la extensión original
            output_extension = os.path.splitext(filename)[1].lower()

        # Redimensionar la imagen
        resized_image = image.resize(new_size)

        # Renombrar la imagen
        new_filename = f"{counter}{output_extension}"
        output_path = os.path.join(output_folder, new_filename)

        # Guardar la imagen redimensionada
        resized_image.save(output_path)

        print(f"Imagen {filename} redimensionada y guardada como {new_filename}")

        # Incrementar el contador
        counter += 1