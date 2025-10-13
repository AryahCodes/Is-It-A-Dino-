import os
import shutil
import random
from pathlib import Path

def select_random_images(source_path, dest_path, images_per_class=50):
    """
    Select random images from each animal folder and copy them to a destination folder.
    """

    # Create destination folder if it doesn't exist
    os.makedirs(dest_path, exist_ok=True)

    # Automatically detect all animal class folders inside source_path
    species_folders = [f.name for f in Path(source_path).iterdir() if f.is_dir()]
    print(f"🐾 Found {len(species_folders)} animal folders: {species_folders}\n")

    total_copied = 0
    stats = {}

    for species in species_folders:
        species_path = Path(source_path) / species

        # Get all images
        image_files = []
        for ext in ['*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG']:
            image_files.extend(list(species_path.glob(ext)))

        total_images = len(image_files)
        if total_images == 0:
            print(f"⚠️  Warning: No images found in '{species}', skipping...")
            continue

        # Randomly select images
        num_to_select = min(images_per_class, total_images)
        selected_images = random.sample(image_files, num_to_select)

        # Copy selected images
        copied_count = 0
        for i, img_path in enumerate(selected_images):
            try:
                new_filename = f"{species}_{i+1:03d}{img_path.suffix}"
                dest_file = Path(dest_path) / new_filename
                shutil.copy2(img_path, dest_file)
                copied_count += 1
            except Exception as e:
                print(f"❌ Error copying {img_path.name}: {e}")

        stats[species] = {'total': total_images, 'copied': copied_count}
        total_copied += copied_count
        print(f"✅ {species}: Selected {copied_count}/{total_images} images")

    # Summary
    print("\n" + "="*60)
    print("📊 SELECTION SUMMARY")
    print("="*60)
    for species, info in stats.items():
        print(f"{species:20s} | Available: {info['total']:4d} | Copied: {info['copied']:3d}")
    print("="*60)
    print(f"🎉 Total images copied: {total_copied}")
    print(f"📁 Destination: {dest_path}")
    print("="*60)


def main():
    """Main function to select 50 random images per animal class"""

    # 👇 Change these if needed
    SOURCE_PATH = "/Users/aryahb/IsItADino/temp_animals/raw-img"  # Animals10 dataset
    DESTINATION_PATH = "/Users/aryahb/IsItADino/is-it-a-dino/data/raw/not_dinosaur"
    IMAGES_PER_CLASS = 50

    if not os.path.exists(SOURCE_PATH):
        print(f"⚠️  ERROR: Source folder not found: {SOURCE_PATH}")
        return

    select_random_images(SOURCE_PATH, DESTINATION_PATH, IMAGES_PER_CLASS)
    print("\n✨ Done! You now have 50 random images per animal class added to not_dinosaur.")


if __name__ == "__main__":
    random.seed(42)
    main()
