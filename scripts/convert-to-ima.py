import pickle
import numpy as np
from PIL import Image
import os
from pathlib import Path

def unpickle(file):
    """Load CIFAR-10 batch file"""
    with open(file, 'rb') as fo:
        dict = pickle.load(fo, encoding='bytes')
    return dict

def extract_cifar10_images(cifar_path, output_path, max_per_class=100):
    """
    Extract CIFAR-10 images from pickle files to JPG (only extract what we need)
    
    Args:
        cifar_path: Path to folder containing CIFAR-10 batch files
        output_path: Where to save extracted images
        max_per_class: Maximum images to extract per class (default: 100)
    """
    
    # CIFAR-10 class names
    class_names = [
        'airplane',
        'automobile', 
        'bird',
        'cat',
        'deer',
        'dog',
        'frog',
        'horse',
        'ship',
        'truck'
    ]
    
    # Use all 10 classes for more diversity
    object_classes = class_names  # All 10 categories
    
    # Create output folders
    for class_name in class_names:
        os.makedirs(os.path.join(output_path, class_name), exist_ok=True)
    
    print("🖼️  Extracting CIFAR-10 images...\n")
    
    # Process all data batches
    batch_files = [
        'data_batch_1',
        'data_batch_2', 
        'data_batch_3',
        'data_batch_4',
        'data_batch_5',
        'test_batch'
    ]
    
    total_extracted = {name: 0 for name in class_names}
    class_counters = {name: 0 for name in class_names}  # Track per-class count
    
    for batch_file in batch_files:
        batch_path = os.path.join(cifar_path, batch_file)
        
        if not os.path.exists(batch_path):
            print(f"⚠️  Skipping {batch_file} - not found")
            continue
        
        print(f"📦 Processing {batch_file}...")
        
        # Load batch
        batch_data = unpickle(batch_path)
        
        # Extract images and labels
        images = batch_data[b'data']
        labels = batch_data[b'labels']
        
        # Reshape images (CIFAR-10 images are 32x32x3)
        images = images.reshape(-1, 3, 32, 32).transpose(0, 2, 3, 1)
        
        # Save each image (but only up to max_per_class)
        for i, (img_data, label) in enumerate(zip(images, labels)):
            class_name = class_names[label]
            
            # Skip if we already have enough of this class
            if class_counters[class_name] >= max_per_class:
                continue
            
            # Convert to PIL Image
            img = Image.fromarray(img_data)
            
            # Save as JPG
            filename = f"{batch_file}_{i:04d}.jpg"
            save_path = os.path.join(output_path, class_name, filename)
            img.save(save_path)
            
            class_counters[class_name] += 1
            total_extracted[class_name] += 1
        
        # Check if we have enough images for all classes
        if all(count >= max_per_class for count in class_counters.values()):
            print(f"✅ Reached {max_per_class} images per class, stopping early!")
            break
    
    # Print summary
    print("\n" + "="*60)
    print("📊 CIFAR-10 EXTRACTION SUMMARY")
    print("="*60)
    
    for class_name in class_names:
        marker = "🎯" if class_name in object_classes else "🚫"
        print(f"{marker} {class_name:12s}: {total_extracted[class_name]:4d} images")
    
    print("="*60)
    print("\n✅ Extraction complete!")
    print(f"📁 Images saved to: {output_path}")
    
    print("\n📋 For your project, use these OBJECT categories:")
    for obj_class in object_classes:
        print(f"   - {obj_class}: {total_extracted[obj_class]} images available")

def select_objects_from_cifar(cifar_extracted_path, dest_path, images_per_class=40):
    """
    Select random images from extracted CIFAR-10 classes
    
    Args:
        cifar_extracted_path: Path where CIFAR images were extracted
        dest_path: data/raw/not_dinosaur folder
        images_per_class: Number of images per class (default: 40)
    """
    import random
    import shutil
    
    # Use all 10 CIFAR-10 classes
    all_classes = [
        'airplane', 'automobile', 'bird', 'cat', 'deer',
        'dog', 'frog', 'horse', 'ship', 'truck'
    ]
    
    os.makedirs(dest_path, exist_ok=True)
    
    print("\n🚗 Selecting random images from all CIFAR-10 categories...\n")
    
    total_copied = 0
    
    for cifar_class in all_classes:
        class_path = Path(cifar_extracted_path) / cifar_class
        
        if not class_path.exists():
            print(f"⚠️  Warning: {cifar_class} folder not found")
            continue
        
        # Get all images
        image_files = list(class_path.glob('*.jpg'))
        total_available = len(image_files)
        
        if total_available == 0:
            print(f"⚠️  Warning: No images found in '{cifar_class}', skipping...")
            continue
        
        # Select random subset
        num_to_select = min(images_per_class, total_available)
        selected_images = random.sample(image_files, num_to_select)
        
        # Copy to destination
        for i, img_path in enumerate(selected_images):
            new_filename = f"cifar_{cifar_class}_{i+1:03d}.jpg"
            dest_file = Path(dest_path) / new_filename
            shutil.copy2(img_path, dest_file)
        
        total_copied += num_to_select
        print(f"✅ {cifar_class:12s}: Selected {num_to_select}/{total_available} images")
    
    print(f"\n🎉 Total CIFAR-10 images added: {total_copied}")
    print(f"📁 Destination: {dest_path}")
    
    return total_copied

def main():
    """Main function"""
    
    # CONFIGURATION - UPDATE THESE!
    CIFAR_PATH = "/Users/aryahb/IsItADino/temp_cifar10/cifar-10-batches-py"
    EXTRACT_PATH = "/Users/aryahb/IsItADino/temp_cifar10/extracted"
    DEST_PATH = "/Users/aryahb/IsItADino/is-it-a-dino/data/raw/not_dinosaur"
    
    print("🦖 CIFAR-10 Object Extractor\n")
    
    # Check if CIFAR path exists
    if not os.path.exists(CIFAR_PATH):
        print("⚠️  ERROR: CIFAR-10 batch files not found!")
        print(f"Looking for: {CIFAR_PATH}")
        print("\nTry:")
        print("1. Check what's in temp_cifar10/:")
        print("   ls temp_cifar10/")
        print("2. Update CIFAR_PATH in this script")
        print("\nCommon locations:")
        print("   - temp_cifar10/cifar-10-batches-py/")
        print("   - temp_cifar10/cifar-10-python/")
        return
    
    # Step 1: Extract images from pickle files (only 100 per class)
    print("Step 1: Extracting CIFAR-10 images (100 per class for efficiency)...")
    extract_cifar10_images(CIFAR_PATH, EXTRACT_PATH, max_per_class=100)
    
    # Step 2: Select random objects for your project
    print("\nStep 2: Selecting images from all 10 CIFAR categories...")
    select_objects_from_cifar(EXTRACT_PATH, DEST_PATH, images_per_class=40)
    
    # Final count
    dest_path = Path(DEST_PATH)
    if dest_path.exists():
        total_files = len(list(dest_path.glob('*.jpg'))) + len(list(dest_path.glob('*.png')))
        print("\n" + "="*60)
        print("📊 FINAL DATASET STATUS")
        print("="*60)
        print(f"Total 'not_dinosaur' images: {total_files}")
        print("   - Human faces: ~250")
        print("   - Animals: ~250")
        print("   - CIFAR-10 (all 10 categories): ~400")
        print("="*60)
        print("\n🎉 Dataset is COMPLETE!")
        print("📋 Next step: Run 'python scripts/data_prep.py'")

if __name__ == "__main__":
    import random
    random.seed(42)
    main()