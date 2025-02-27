
# Food Containers Detection & Tracking - Computer Vision Task

This repository contains the code and resources for detecting and tracking food containers in a dining hall. The goal is to monitor food consumption and refills using a video feed.

---

## **Approach**

### **Dataset**
We use the **COCO dataset** ([COCO Dataset](https://cocodataset.org/#home)), filtering it to include only the following classes:
- **Bowl**
- **Wine Glass**
- **Cup**
- **Bottle**

### **Model**
We use **YOLOv8n** for object detection because:
- It is **lightweight** and optimized for real-time processing.
- It provides a good balance between **accuracy** and **speed**.

### **Fine-Tuning**
The model is fine-tuned using **half of the COCO validation dataset** to avoid overfitting. Data augmentation techniques (brightness, contrast, noise, flips) are applied to improve robustness.

### **Training**
Training is done on a local machine using:
- **PyTorch** and **Ultralytics** for YOLOv8.
- **Adam optimizer** for efficient training.

### **Inference**
A test video (`video_containers_3.mp4`) is used to detect movements, disappearances, and refills of bowls. The model outputs timestamps for each event in **JSON format**.

---

## **Project Structure**





food_containers/
│── data/                  # Filtered and organized data
│   ├── annotations/       # Annotations in COCO or other formats
│   ├── filtered/          # Filtered COCO data
│   ├── train/             # Training data
│   ├── val/               # Validation data
│   ├── fine_tuning/       # Data for fine-tuning
│   ├── augmented_images/  # Augmented images
│   ├── video_containers_3.mp4  # Test video
│── scripts/               # Project scripts
│   ├── preprocessing.py   # Data preprocessing
│   ├── training.py        # Model training
│   ├── fine_tuning.py     # Model fine-tuning
│   ├── inference_visualization.py       # Inference with new data
│── results/               # Inference results
│── runs/                  # Folder for checkpoints and logs and training results
│── requirements.txt       # Project dependencies
│── README.md              # Main documentation
│── .gitignore             


## **Setup**

1. Clone this repository:
   ```bash
   git clone https://github.com/carlos0698/food_containers_1.git

2. Download the filtered dataset (`data.zip`) from [Google Drive](https://drive.google.com/file/d/1Zxv3HY_Af106pfPUGRNlRixkh6nIgd6R/view?usp=share_link) and unzip it