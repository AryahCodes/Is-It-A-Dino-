import os
import shutil
from PIL import Image
import numpy as np
from pathlib import Path

def create_folder_structure():
    """Create necessary folders if they don't exist"""
    folders = [
        'data/processed/train/dinosaur',
        'data/processed/train/not_dinosaur',
        'data/processed/test/dinosaur',
        'data/processed/test/not_dinosaur'
    ]
    for folder in folders:
        Path(folder).mkdir(parents=True, exist_ok=True)
    print("✅ Folder structure created")

def resize_and_clean_images(input_folder, output_folder, size=(224, 224)):
    """Resize all images and remove corrupted ones"""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    success_count = 0
    error_count = 0
    
    for img_name in os.listdir(input_folder):
        if img_name.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
            img_path = os.path.join(input_folder, img_name)
            try:
                img = Image.open(img_path)
                img = img.convert('RGB')  # Convert to RGB (handles RGBA, grayscale, etc.)
                img = img.resize(size, Image.Resampling.LANCZOS)
                
                # Save with consistent naming
                output_path = os.path.join(output_folder, f"{success_count:04d}.jpg")
                img.save(output_path, 'JPEG', quality=95)
                success_count += 1
                
                if success_count % 50 == 0:
                    print(f"Processed {success_count} images...")
                    
            except Exception as e:
                print(f"❌ Error with {img_name}: {e}")
                error_count += 1
    
    print(f"✅ Processed {success_count} images successfully")
    if error_count > 0:
        print(f"⚠️  Skipped {error_count} corrupted images")
    return success_count

def split_train_test(input_folder, train_folder, test_folder, test_ratio=0.2):
    """Split images into train and test sets"""
    images = [f for f in os.listdir(input_folder) if f.endswith('.jpg')]
    np.random.shuffle(images)
    
    split_idx = int(len(images) * (1 - test_ratio))
    train_images = images[:split_idx]
    test_images = images[split_idx:]
    
    # Copy to train folder
    for img in train_images:
        shutil.copy(
            os.path.join(input_folder, img),
            os.path.join(train_folder, img)
        )
    
    # Copy to test folder
    for img in test_images:
        shutil.copy(
            os.path.join(input_folder, img),
            os.path.join(test_folder, img)
        )
    
    print(f"✅ Split: {len(train_images)} train, {len(test_images)} test")
    return len(train_images), len(test_images)

def main():
    print("🦖 Starting data preprocessing...")
    
    # Create folder structure
    create_folder_structure()
    
    # Process dinosaur images
    print("\n📁 Processing dinosaur images...")
    temp_dino = 'data/processed/temp_dinosaur'
    os.makedirs(temp_dino, exist_ok=True)
    dino_count = resize_and_clean_images('data/raw/dinosaur', temp_dino)
    
    # Split dinosaur images
    split_train_test(
        temp_dino,
        'data/processed/train/dinosaur',
        'data/processed/test/dinosaur'
    )
    
    # Process not_dinosaur images
    print("\n📁 Processing not_dinosaur images...")
    temp_not = 'data/processed/temp_not_dinosaur'
    os.makedirs(temp_not, exist_ok=True)
    not_dino_count = resize_and_clean_images('data/raw/not_dinosaur', temp_not)
    
    # Split not_dinosaur images
    split_train_test(
        temp_not,
        'data/processed/train/not_dinosaur',
        'data/processed/test/not_dinosaur'
    )
    
    # Clean up temp folders
    shutil.rmtree(temp_dino)
    shutil.rmtree(temp_not)
    
    print(f"\n✅ Preprocessing complete!")
    print(f"Total dinosaur images: {dino_count}")
    print(f"Total not_dinosaur images: {not_dino_count}")
    print("\nReady for training! 🚀")

if __name__ == "__main__":
    main()