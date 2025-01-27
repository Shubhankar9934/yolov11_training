# scripts/split_dataset.py
 
import os
import shutil
import random
 
def split_dataset(images_dir, labels_dir, output_dir, train_ratio=0.8, seed=42):
    """
    Split dataset into training and validation sets, including only images that have corresponding label files.
 
    :param images_dir: Directory containing all images.
    :param labels_dir: Directory containing all label files.
    :param output_dir: Base directory to save train and val splits.
    :param train_ratio: Proportion of data to use for training (default: 0.8).
    :param seed: Random seed for reproducibility (default: 42).
    """
    # Ensure output directories exist
    train_images_dir = os.path.join(output_dir, 'train', 'images')
    train_labels_dir = os.path.join(output_dir, 'train', 'labels')
    val_images_dir = os.path.join(output_dir, 'val', 'images')
    val_labels_dir = os.path.join(output_dir, 'val', 'labels')
 
    for directory in [train_images_dir, train_labels_dir, val_images_dir, val_labels_dir]:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")
 
    # List all image files
    all_image_files = [f for f in os.listdir(images_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    print(f"Total images found: {len(all_image_files)}")
 
    # Filter images that have corresponding label files
    labeled_image_files = []
    for img_file in all_image_files:
        label_file = os.path.splitext(img_file)[0] + '.txt'
        label_path = os.path.join(labels_dir, label_file)
        if os.path.exists(label_path):
            labeled_image_files.append(img_file)
        else:
            print(f"Excluded {img_file}: Label file {label_file} does not exist.")
 
    print(f"Total labeled images: {len(labeled_image_files)}")
 
    if not labeled_image_files:
        print("Error: No labeled images found. Please ensure that label files are present.")
        return
 
    # Shuffle the labeled images list for random splitting
    random.seed(seed)
    random.shuffle(labeled_image_files)
 
    # Calculate split index
    split_index = int(len(labeled_image_files) * train_ratio)
    train_files = labeled_image_files[:split_index]
    val_files = labeled_image_files[split_index:]
 
    print(f"Training samples: {len(train_files)}")
    print(f"Validation samples: {len(val_files)}")
 
    # Function to copy files
    def copy_files(file_list, src_images, src_labels, dst_images, dst_labels, split_name):
        for img_file in file_list:
            label_file = os.path.splitext(img_file)[0] + '.txt'
 
            src_img_path = os.path.join(src_images, img_file)
            src_label_path = os.path.join(src_labels, label_file)
 
            dst_img_path = os.path.join(dst_images, img_file)
            dst_label_path = os.path.join(dst_labels, label_file)
 
            # Copy image
            shutil.copy2(src_img_path, dst_img_path)
 
            # Copy label
            shutil.copy2(src_label_path, dst_label_path)
 
        print(f"Copied {len(file_list)} files to {split_name} set.")
 
    # Copy training files
    copy_files(
        train_files,
        src_images=images_dir,
        src_labels=labels_dir,
        dst_images=train_images_dir,
        dst_labels=train_labels_dir,
        split_name='training'
       
    )
 
    # Copy validation files
    copy_files(
        val_files,
        src_images=images_dir,
        src_labels=labels_dir,
        dst_images=val_images_dir,
        dst_labels=val_labels_dir,
        split_name='validation'
    )
 
    print("Dataset splitting completed successfully.")
 
if __name__ == "__main__":
    import argparse
 
    parser = argparse.ArgumentParser(description="Split dataset into training and validation sets, including only labeled images.")
    parser.add_argument("--images_dir", type=str, default=os.path.abspath("../dataset/extracted_frames"), help="Directory containing all extracted images.")
    parser.add_argument("--labels_dir", type=str, default=os.path.abspath("../dataset/labels"), help="Directory containing all label files.")
    parser.add_argument("--output_dir", type=str, default=os.path.abspath("../dataset/images"), help="Directory to save the split datasets.")
    parser.add_argument("--train_ratio", type=float, default=0.8, help="Proportion of data to use for training (default: 0.8).")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for shuffling (default: 42).")
    args = parser.parse_args()
 
    split_dataset(
        images_dir=args.images_dir,
        labels_dir=args.labels_dir,
        output_dir=args.output_dir,
        train_ratio=args.train_ratio,
        seed=args.seed
    )


