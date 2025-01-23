# scripts/check_labels.py
 
import os
 
def check_labels(labels_dir):
    label_files = [f for f in os.listdir(labels_dir) if f.endswith('.txt')]
    for label_file in label_files:
        path = os.path.join(labels_dir, label_file)
        with open(path, 'r') as file:
            content = file.read().strip()
            if not content:
                print(f"Empty label file: {label_file}")
            else:
                # Check each line for correct number of elements
                for line_num, line in enumerate(content.split('\n'), start=1):
                    parts = line.strip().split()
                    if len(parts) != 5:
                        print(f"Malformed line in {label_file} on line {line_num}: {line}")
 
if __name__ == "__main__":
    train_labels_dir = os.path.abspath("../dataset/images/train/labels")
    val_labels_dir = os.path.abspath("../dataset/images/val/labels")
   
    print("Checking training labels...")
    check_labels(train_labels_dir)
   
    print("\nChecking validation labels...")
    check_labels(val_labels_dir)