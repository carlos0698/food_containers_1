import os
import json
import shutil
from pycocotools.coco import COCO

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # food_containers/
DATA_DIR = os.path.join(BASE_DIR, "data")
ANNOTATIONS_DIR = os.path.join(DATA_DIR, "annotations")
FILTERED_DIR = os.path.join(DATA_DIR, "filtered")

os.makedirs(FILTERED_DIR, exist_ok=True)

def filter_images(category="bowl", annotations_file="image_info_test-dev2017.json", output_file="filtered_image_ids.txt"):
    print("\nFiltering images...")

    coco = COCO(os.path.join(ANNOTATIONS_DIR, annotations_file))
    category_ids = coco.getCatIds(catNms=[category])
    image_ids = coco.getImgIds(catIds=category_ids)

    with open(os.path.join(FILTERED_DIR, output_file), "w") as f:
        for img_id in image_ids:
            f.write(f"{img_id}\n")

    print(f"Found {len(image_ids)} images for '{category}'. Saved to '{output_file}'.")
    return image_ids

def filter_annotations(annotations_file="instances_val2017.json", image_ids_file="filtered_image_ids.txt", output_file="filtered_annotations.json"):
    print("\nFiltering annotations...")

    coco = COCO(os.path.join(ANNOTATIONS_DIR, annotations_file))

    with open(os.path.join(FILTERED_DIR, image_ids_file), "r") as f:
        image_ids = [int(line.strip()) for line in f.readlines()]

    filtered_annotations = [ann for ann in coco.dataset["annotations"] if ann["image_id"] in image_ids]
    filtered_images = coco.loadImgs(image_ids)

    filtered_data = {
        "info": coco.dataset.get("info", {}),
        "licenses": coco.dataset.get("licenses", []),
        "images": filtered_images,
        "annotations": filtered_annotations,
        "categories": coco.loadCats(coco.getCatIds()),
    }

    with open(os.path.join(FILTERED_DIR, output_file), "w") as f:
        json.dump(filtered_data, f)

    print(f"Annotations saved to '{output_file}'.")

def copy_filtered_images(image_ids_file="filtered_image_ids.txt", source_dir="train2017", output_subdir="train"):
    print("\nCopying filtered images...")

    source_path = os.path.join(DATA_DIR, source_dir)
    output_path = os.path.join(FILTERED_DIR, output_subdir)

    os.makedirs(output_path, exist_ok=True)

    with open(os.path.join(FILTERED_DIR, image_ids_file), "r") as f:
        image_ids = [line.strip() for line in f.readlines()]

    for img_id in image_ids:
        img_file_name = f"{int(img_id):012d}.jpg"
        img_src = os.path.join(source_path, img_file_name)
        img_dst = os.path.join(output_path, img_file_name)

        if os.path.exists(img_src):
            shutil.copy(img_src, img_dst)
            print(f"Copied: {img_file_name}")
        else:
            print(f"Missing: {img_file_name}")

    print("Image copying completed.")

if __name__ == "__main__":
    category = "bowl"
    source_folder = "train2017"
    output_folder = "train"

    filter_images(category=category)
    filter_annotations()
    copy_filtered_images(source_dir=source_folder, output_subdir=output_folder)

    print("\nPreprocessing completed.")
