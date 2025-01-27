# scripts/count_files.py
 
import os
 
def count_files(dir_path, extension):
    return len([f for f in os.listdir(dir_path) if f.lower().endswith(extension)])
 
if __name__ == "__main__":
    train_images = os.path.abspath("../dataset/images/train/images")
    train_labels = os.path.abspath("../dataset/images/train/labels")
    val_images = os.path.abspath("../dataset/images/val/images")
    val_labels = os.path.abspath("../dataset/images/val/labels")
   
    print(f"Training images: {count_files(train_images, '.jpg') + count_files(train_images, '.png')}")
    print(f"Training labels: {count_files(train_labels, '.txt')}")
    print(f"Validation images: {count_files(val_images, '.jpg') + count_files(val_images, '.png')}")
    print(f"Validation labels: {count_files(val_labels, '.txt')}")
 
 