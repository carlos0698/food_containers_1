from ultralytics import YOLO
import os

# Ruta al archivo dataset.yaml dentro de la carpeta scripts
dataset_yaml_path = os.path.join(os.path.dirname(__file__), "dataset.yaml")

# Verificar la ruta del archivo YAML
print("Ruta del archivo dataset.yaml:", dataset_yaml_path)

# Cargar un modelo preentrenado de YOLO
model = YOLO("yolov8n.pt")

# Entrenar el modelo
model.train(data=dataset_yaml_path, epochs=50, imgsz=512)