# scripts/continue_training.py
 
from ultralytics import YOLO
 
def continue_training(existing_model_path, data_yaml_path, epochs=50, imgsz=640, batch=16, name="text_verification_model_finetuned"):
    """
    Continue training an existing YOLOv8 model with additional data.
 
    :param existing_model_path: Path to the existing trained YOLOv8 model (.pt file).
    :param data_yaml_path: Path to the data.yaml configuration file.
    :param epochs: Number of additional epochs to train.
    :param imgsz: Image size.
    :param batch: Batch size.
    :param name: Name for the training run.
    """
    # Load the existing model
    model = YOLO(existing_model_path)
 
    # Continue training
    model.train(
        data=data_yaml_path,
        epochs=epochs,
        imgsz=imgsz,
        batch=batch,
        name=name,
        resume=True,  # Resume from the existing weights
        optimizer="SGD",  # Optional: specify optimizer
        lr0=0.01,         # Optional: initial learning rate
        augment=True,     # Optional: enable data augmentation
        # Add any other hyperparameters as needed
    )
 
    print("Training completed successfully.")
 
if __name__ == "__main__":
    import argparse
 
    parser = argparse.ArgumentParser(description="Continue training YOLOv8 model with additional data.")
    parser.add_argument("--model", type=str, required=True, help="Path to the existing YOLOv8 model (.pt file).")
    parser.add_argument("--data", type=str, required=True, help="Path to data.yaml file.")
    parser.add_argument("--epochs", type=int, default=50, help="Number of additional epochs.")
    parser.add_argument("--imgsz", type=int, default=640, help="Image size.")
    parser.add_argument("--batch", type=int, default=16, help="Batch size.")
    parser.add_argument("--name", type=str, default="text_verification_model_finetuned", help="Name for the training run.")
 
    args = parser.parse_args()
 
    continue_training(
        existing_model_path=args.model,
        data_yaml_path=args.data,
        epochs=args.epochs,
        imgsz=args.imgsz,
        batch=args.batch,
        name=args.name
    )
 
 
