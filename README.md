
# Food Containers Detection & Tracking - Computer Vision Task

This repository contains the code and resources for detecting and tracking food containers in a dining hall video feed. The goal is to monitor food consumption and refills by identifying container movements and events.

## Approach

### Dataset
We use the [COCO dataset](https://cocodataset.org/), filtered to include relevant classes:
- Bowl
- Wine Glass
- Cup
- Bottle

The dataset is split into training, validation, and fine-tuning subsets, with augmentation applied to enhance robustness.

### Model
We use [**YOLOv8n**](https://github.com/ultralytics/ultralytics) for object detection and [**DeepSORT**](https://github.com/ZQPei/deep_sort_pytorch) for tracking because:
- **YOLOv8n**: Lightweight and optimized for real-time processing (~40 FPS on local hardware), balancing precision and latency for this task.
- **DeepSORT**: Provides persistent tracking with unique IDs, enabling event detection across frames.

### Fine-Tuning
The YOLOv8n model is fine-tuned using half of the COCO validation set to avoid overfitting. Data augmentation (brightness, contrast, noise, flips) improves robustness to varying dining hall conditions, such as low-light scenarios.

### Training
Training is performed on a local machine with:
- PyTorch and Ultralytics for YOLOv8.
- AdamW optimizer for efficient convergence.

### Inference
The script processes a test video (`video_containers_3.mp4`) to:
1. Detect containers using YOLOv8n.
2. Track them with DeepSORT, assigning unique IDs.
3. Identify events: 
   - **Movement**: Detected when a container's bounding box shifts >5 pixels.
   - **Refill**: Inferred when a container reappears after disappearing for >3 seconds.
   - **Disappearance**: Logged when a container exits the frame.
4. Output events with timestamps in JSON format (`events_2.json`).

### Optimizations
- **Real-time**: YOLOv8n ensures low latency, achieving ~40 FPS locally (tested on a mid-range CPU).
- **Low-light**: CLAHE preprocessing enhances contrast in frames, complemented by brightness/contrast augmentation during training.
- **Robustness**: DeepSORT reduces false positives by maintaining track consistency, while fine-tuning improves raw detection accuracy.


## 📂 Project Structure

Note: The project structure shown below does not include a script for data augmentation. If data augmentation is needed, please refer to the script: augmenta_torch.py.

```bash
food_containers/
│── data/                     # Filtered and organized data
│   ├── annotations/          # Annotations in COCO or other formats
│   ├── filtered/             # Filtered COCO data
│   ├── train/                # Training data
│   ├── val/                  # Validation data
│   ├── fine_tuning/          # Data for fine-tuning
│   ├── augmented_images/     # Augmented images
│   ├── video_containers_3.mp4 # Test video
│── scripts/                  # Project scripts
│   ├── preprocessing.py      # Data preprocessing
│   ├── training.py           # Model training
│   ├── fine_tuning.py        # Model fine-tuning
│   ├── inference_visualization.py # Inference with new data
│── results/                  # Inference results
│── runs/                     # Checkpoints, logs, and training results
│── requirements.txt          # Project dependencies
│── README.md                 # Main documentation
│── .gitignore                # Ignore unnecessary files
```


## **Setup**

1. Clone this repository:
   ```bash
   git clone https://github.com/carlos0698/food_containers_1.git

2. Download the filtered dataset (`data.zip`) from [Google Drive](https://drive.google.com/file/d/1Zxv3HY_Af106pfPUGRNlRixkh6nIgd6R/view?usp=share_link) and unzip it
