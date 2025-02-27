from diffusers import StableDiffusionPipeline
import torch
import os

# Definir la carpeta donde se guardarán las imágenes
annotations_dir = "/Volumes/Disco Ana/food_containers/data/filtered/fine_tunning_data"

# Crear la carpeta si no existe
os.makedirs(annotations_dir, exist_ok=True)

# Cargar el modelo (usar torch.float32 para CPU)
model_id = "stabilityai/stable-diffusion-2-1"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float32)

# Mover el pipeline a CPU (esto es opcional, ya que por defecto se usa CPU si no hay GPU)
pipe = pipe.to("cpu")

# Lista de prompts (puedes modificarlos según tus necesidades)
prompts = [
    "A clear glass bottle on a wooden table, natural lighting, high resolution, realistic texture, professional photography.",
    "A red wine glass on a dining table, with a blurred background, elegant setting, high resolution, realistic lighting.",
    "A white ceramic cup on a wooden desk, morning light, steam rising, high resolution, realistic texture.",
    "A metal bowl with fruits on a dining table, natural lighting, high resolution, realistic texture."
]

# Número de imágenes por prompt
num_images_per_prompt = 1  # Cambia este valor según cuántas imágenes quieras por prompt

# Generar imágenes
for i, prompt in enumerate(prompts):
    print(f"Generando imágenes para el prompt: {prompt}")
    for j in range(num_images_per_prompt):
        # Generar la imagen
        image = pipe(prompt).images[0]
        
        # Guardar la imagen en la carpeta especificada
        image_path = os.path.join(annotations_dir, f"image_{i}_{j}.png")
        image.save(image_path)
        print(f"Imagen {j+1} guardada como {image_path}")