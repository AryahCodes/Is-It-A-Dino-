import os
import shutil
import random
from pathlib import Path

def select_random_images(source_path, dest_path, images_per_species=50):
    """
    Select random images from each species folder and copy them to a destination folder.
    
    Args:
        source_path: Path to the dinosaur_dataset folder with species subfolders
        dest_path: Path where selected images will be copied
        images_per_species: Number of random images to select per species (default: 50)
    """
    
    # Create destination folder if it doesn't exist
    os.makedirs(dest_path, exist_ok=True)
    
    # List of all species folders
    species_folders = [
        "Ankylosaurus",
        "Brachiosaurus", 
        "Compsognathus",
        "Corythosaurus",
        "Dilophosaurus",
        "Dimorphodon",
        "Gallimimus",
        "Microceratus",
        "Pachycephalosaurus",
        "Parasaurolophus",
        "Spinosaurus",
        "Stegosaurus",
        "Triceratops",
        "Tyrannosaurus_Rex",
        "Velociraptor"
    ]
    
    total_copied = 0
    stats = {}
    
    print("🦖 Starting random image selection...\n")
    
    for species in species_folders:
        species_path = Path(source_path) / species
        
        # Check if folder exists
        if not species_path.exists():
            print(f"⚠️  Warning: Folder '{species}' not found, skipping...")
            continue
        
        # Get all image files (jpg, jpeg, png)
        image_files = []
        for ext in ['*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG']:
            image_files.extend(list(species_path.glob(ext)))
        
        total_images = len(image_files)
        
        if total_images == 0:
            print(f"⚠️  Warning: No images found in '{species}', skipping...")
            continue
        
        # Select random images
        num_to_select = min(images_per_species, total_images)
        selected_images = random.sample(image_files, num_to_select)
        
        # Copy selected images to destination
        copied_count = 0
        for i, img_path in enumerate(selected_images):
            try:
                # Create a new filename: species_number.extension
                new_filename = f"{species}_{i+1:03d}{img_path.suffix}"
                dest_file = Path(dest_path) / new_filename
                
                shutil.copy2(img_path, dest_file)
                copied_count += 1
                
            except Exception as e:
                print(f"❌ Error copying {img_path.name}: {e}")
        
        stats[species] = {
            'total': total_images,
            'selected': num_to_select,
            'copied': copied_count
        }
        
        total_copied += copied_count
        print(f"✅ {species}: Selected {copied_count}/{total_images} images")
    
    # Print summary
    print("\n" + "="*60)
    print("📊 SELECTION SUMMARY")
    print("="*60)
    
    for species, info in stats.items():
        print(f"{species:25s} | Available: {info['total']:3d} | Selected: {info['copied']:2d}")
    
    print("="*60)
    print(f"🎉 Total images copied: {total_copied}")
    print(f"📁 Destination: {dest_path}")
    print("="*60)

def main():
    """Main function to run the script"""
    
    # CONFIGURATION - Change these paths to match your setup
    
    # Option 1: If you have the Kaggle dataset downloaded locally
    SOURCE_PATH = "/Users/aryahb/IsItADino/is-it-a-dino/data/dinosaur_dataset"  # Change this!
    
    # Option 2: If you're using the folders from your screenshot
    # SOURCE_PATH = "/path/to/folder/containing/species/folders"
    
    DESTINATION_PATH = "/Users/aryahb/IsItADino/is-it-a-dino/data/raw/dinosaur"
    IMAGES_PER_SPECIES = 50
    
    # Check if source path exists
    if not os.path.exists(SOURCE_PATH) or SOURCE_PATH == "/Users/aryahb/IsItADino/is-it-a-dino/data/dinosaur_dataset":
        print("⚠️  ERROR: Please update SOURCE_PATH in the script!")
        print("\nInstructions:")
        print("1. Open this script in your editor")
        print("2. Find the SOURCE_PATH variable in main()")
        print("3. Change it to your actual dataset path")
        print("\nExample:")
        print('   SOURCE_PATH = "C:/Users/YourName/Downloads/dinosaur_dataset"')
        print('   or')
        print('   SOURCE_PATH = "/Users/YourName/Downloads/dinosaur_dataset"')
        return
    
    # Run the selection
    select_random_images(SOURCE_PATH, DESTINATION_PATH, IMAGES_PER_SPECIES)
    
    print("\n✨ Done! You can now proceed with data preparation.")
    print("   Next step: Run 'python scripts/data_prep.py'")

if __name__ == "__main__":
    # Set random seed for reproducibility
    random.seed(42)
    main()