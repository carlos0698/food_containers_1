import os
import glob


# Ruta a la carpeta de anotaciones
annotations_dir = "/Volumes/Disco Ana/food_containers/data/filtered/val/labels_copy"

# IDs de las clases de interés
classes_of_interest = {40,41,42,46} 

# Recorrer todos los archivos de anotaciones
for filename in os.listdir(annotations_dir):
    if filename.endswith(".txt"):
        filepath = os.path.join(annotations_dir, filename)

        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()

        # Filtrar solo las líneas cuyo primer número esté en las clases de interés
        filtered_lines = [line for line in lines if line.split()[0].isdigit() and int(line.split()[0]) in classes_of_interest]

        # Sobrescribir el archivo con las líneas filtradas
        with open(filepath, "w", encoding="utf-8") as f:
            f.writelines(filtered_lines)

print("✅ Líneas filtradas correctamente.")


# Ruta a los archivos de anotaciones
labels_dir = "/Volumes/Disco Ana/food_containers/data/filtered/val/labels_copy"

# Mapeo de clases
class_map = {40: 0, 41: 1, 42: 2, 46: 3}

# Obtener todos los archivos .txt
label_files = glob.glob(os.path.join(labels_dir, "*.txt"))

for file in label_files:
    with open(file, "r") as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        parts = line.split(maxsplit=1)  # Dividir en dos partes: clase y resto
        if parts and parts[0].isdigit():  # Asegurar que la primera parte es un número
            class_id = int(parts[0])
            if class_id in class_map:
                parts[0] = str(class_map[class_id])  # Reemplazar solo la clase
                new_lines.append(" ".join(parts) + "\n")

    # Sobreescribir el archivo con las nuevas etiquetas
    with open(file, "w") as f:
        f.writelines(new_lines)

print("✅ Clases remapeadas correctamente.")


