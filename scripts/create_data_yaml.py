# scripts/create_data_yaml.py
 
import os
 
def create_data_yaml(output_dir, yaml_path="../dataset/data.yaml"):
    """
    Create data.yaml configuration file for YOLOv8.
    """
    # Ensure the train/val/images subfolders exist
    train_images_dir = os.path.join(output_dir, 'train', 'images')
    val_images_dir = os.path.join(output_dir, 'val', 'images')
   
    os.makedirs(train_images_dir, exist_ok=True)
    os.makedirs(val_images_dir, exist_ok=True)
 
    # Convert to absolute paths
    train_images = os.path.abspath(train_images_dir)
    val_images = os.path.abspath(val_images_dir)
 
    data_yaml_content = f"""
train: {train_images}
val: {val_images}
 
nc: 4
names: ['Billing_Enabled', 'Service_NotEnabled', 'Billing_NotEnabled', 'Service_Enabled']
"""
 
    # Ensure that the folder for data.yaml exists
    os.makedirs(os.path.dirname(yaml_path), exist_ok=True)
 
    with open(yaml_path, 'w') as f:
        f.write(data_yaml_content.strip())
   
    print(f"data.yaml created at {yaml_path}")
 
if __name__ == "__main__":
    # Use absolute paths (or adjust as needed)
    output_dir = r"C:\Users\shubhankar.kumar\Desktop\dot_detection\text_detection_project\dataset\images"
    yaml_path = r"C:\Users\shubhankar.kumar\Desktop\dot_detection\text_detection_project\dataset\data.yaml"
    create_data_yaml(output_dir, yaml_path)
 
 

 

 

 