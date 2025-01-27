# scripts/train_yolov8.py

import os

from ultralytics import YOLO
 
def train_yolov8(yaml_path="../dataset/data.yaml", model_variant="yolo11m.pt", epochs=10, imgsz=640, batch=16, name="text_verification_model"):

    """

    Train YOLOv8 model.
 
    :param yaml_path: Path to data.yaml.

    :param model_variant: YOLOv8 model variant to use.

    :param epochs: Number of training epochs.

    :param imgsz: Image size.

    :param batch: Batch size.

    :param name: Name of the training run.

    """

    model = YOLO(model_variant)

    model.train(

        data=yaml_path,

        epochs=epochs,

        imgsz=imgsz,

        batch=batch,

        name=name,

        project="runs/detect"

    )

    print("Training completed.")
 
if __name__ == "__main__":

    train_yolov8(

        yaml_path=os.path.abspath("../dataset/data.yaml"),

        model_variant="yolo11m.pt", 

        epochs=10,

        imgsz=640,

        batch=16,

        name="text_verification_model"

    )
