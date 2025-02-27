from ultralytics import YOLO
import os

# Cargar el modelo preentrenado (best.pt)
model = YOLO("/Volumes/Disco Ana/food_containers/scripts/runs/detect/train/weights/best.pt")

# Fine-tuning con ajustes recomendados
results = model.train(
    data=os.path.join(os.path.dirname(__file__), "dataset_tunning.yaml"),  # Ruta del archivo YAML
    epochs=20,                         # Aumentar a 20 épocas
    batch=32,                          # Aumentar el tamaño del lote a 32 (ajusta según la memoria de la GPU)
    imgsz=640,                         # Aumentar el tamaño de la imagen a 640x640
    name="fine_tuning_v3_adamw",       # Nombre descriptivo del experimento
    pretrained=True,                   # Usar pesos preentrenados (best.pt)
    optimizer="AdamW",                 # Usar AdamW como optimizador
    lr0=0.001,                         # Aumentar la tasa de aprendizaje inicial
    lrf=0.01,                          # Learning rate final (como fracción de lr0)
    weight_decay=0.0005,               # Añadir weight decay para regularización
    momentum=0.937,                    # Momentum para SGD (si usas SGD)
    dropout=0.2,                       # Añadir Dropout para regularización
    patience=10                        # Early stopping después de 10 épocas sin mejora
)