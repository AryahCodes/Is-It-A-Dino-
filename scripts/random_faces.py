import os
import random
import shutil
from pathlib import Path

def copy_random_faces(source_folder, target_folder, sample_size=300):
    
    source = Path(source_folder)
    target = Path(target_folder)

    if not source.exists():
        print(f"❌ Source folder not found: {source}")
        return

    target.mkdir(parents=True, exist_ok=True)

    # Collect all images
    image_files = []
    for ext in ['*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG']:
        image_files.extend(list(source.glob(ext)))

    total = len(image_files)
    print(f"📸 Found {total} images in {source}")

    if total == 0:
        print("⚠️ No images found.")
        return

    # Randomly sample
    num_to_copy = min(sample_size, total)
    selected = random.sample(image_files, num_to_copy)

    print(f"🎯 Copying {num_to_copy} random images to {target}")

    # Copy selected files
    for img_path in selected:
        shutil.copy2(img_path, target / img_path.name)

    print(f"✅ Done! {num_to_copy} images copied to {target}")

if __name__ == "__main__":
    random.seed(42)

    SOURCE_FOLDER = "/Users/aryahb/IsItADino/temp_faces/images"
    TARGET_FOLDER = "/Users/aryahb/IsItADino/is-it-a-dino/data/raw/not_dinosaur"
    SAMPLE_SIZE = 300

    copy_random_faces(SOURCE_FOLDER, TARGET_FOLDER, SAMPLE_SIZE)