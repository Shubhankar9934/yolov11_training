import torch
import yaml
import os
import time
from ultralytics import YOLO
from datetime import datetime

# Check for GPU availability
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Using device: {device}")

# Load configuration
with open('data.yaml') as f:
    data = yaml.safe_load(f)

# Initialize model
model = YOLO('yolov8n.pt')  # Load a pretrained YOLOv8 nano model

# Training parameters
params = {
    'data': 'data.yaml',
    'epochs': 100,
    'imgsz': 640,
    'batch': 16 if device == 'cuda' else 8,
    'device': device,
    'workers': 4 if device == 'cuda' else 2,
    'project': 'runs/detect',
    'name': 'train',
    'patience': 10,  # Early stopping patience
    'lr0': 0.01,     # Initial learning rate
    'lrf': 0.01,     # Final learning rate (lr0 * lrf)
    'momentum': 0.937,
    'weight_decay': 0.0005,
    'optimizer': 'AdamW',
    'cos_lr': True,  # Cosine learning rate scheduler
    'save_period': 5, # Save checkpoint every N epochs
    'val': True      # Validate during training
}

# Create output directories
os.makedirs('runs/detect/train', exist_ok=True)

# Training callback for progress reporting
def on_train_epoch_end(trainer):
    epoch = trainer.epoch
    total_epochs = trainer.args.epochs
    progress = int((epoch / total_epochs) * 100)
    
    # Get current metrics
    metrics = {
        'precision': trainer.metrics.get('metrics/precision', 0),
        'recall': trainer.metrics.get('metrics/recall', 0),
        'mAP50': trainer.metrics.get('metrics/mAP50', 0),
        'mAP50_95': trainer.metrics.get('metrics/mAP50-95', 0)
    }
    
    # Print progress to stdout for PythonShell to capture
    print(f"PROGRESS:{progress}")
    print(f"DEVICE:{device}")
    print(f"METRICS:{json.dumps(metrics)}")

# Start training
try:
    start_time = datetime.now()
    print(f"Training started at: {start_time}")
    
    # Train the model
    results = model.train(
        **params,
        callbacks={'on_train_epoch_end': on_train_epoch_end}
    )
    
    end_time = datetime.now()
    duration = end_time - start_time
    print(f"Training completed in: {duration}")
    print("Training results:", results)

except Exception as e:
    print(f"ERROR:{str(e)}")
    raise e