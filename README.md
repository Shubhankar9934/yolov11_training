# YOLOv8 Training Platform

A full-stack application for training YOLOv8 models with a user-friendly web interface.

## Features

- Dataset preparation and validation
- Real-time training monitoring
- Model download functionality
- Training history tracking
- Performance metrics visualization

## Installation

### Prerequisites

- Node.js (v18 or higher)
- Python (v3.8 or higher)
- SQLite

### Backend Setup

1. Navigate to the project root directory:
   ```bash
   cd YoloV11_Training
   ```

2. Install backend dependencies:
   ```bash
   npm install
   ```

3. Install Python dependencies:
   ```bash
   pip install ultralytics python-shell
   ```

### Frontend Setup

1. Navigate to the client directory:
   ```bash
   cd client
   ```

2. Install frontend dependencies:
   ```bash
   npm install
   ```

3. Return to the project root:
   ```bash
   cd ..
   ```

## Running the Application

1. Start the development server:
   ```bash
   npm run dev
   ```

2. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5001

## Usage Guide

### Dataset Preparation

1. Upload your dataset (zip file containing images and labels)
2. Use the preparation steps:
   - Split dataset
   - Count files
   - Check labels
   - Create data.yaml

### Training

1. Start training from the main interface
2. Monitor progress in real-time
3. View training metrics (precision, recall, mAP)
4. Download trained model when complete

### API Endpoints

- `POST /api/upload` - Upload dataset
- `POST /api/prepare-dataset` - Prepare dataset
- `POST /api/train` - Start training
- `GET /api/training-status` - Get training status
- `GET /api/download-trained-model` - Download trained model

## Troubleshooting

### Common Issues

1. **Port conflicts**:
   - Check if ports 3000 and 5001 are available
   - Update ports in `.env` file if needed

2. **Python dependencies**:
   - Ensure Python environment is properly configured
   - Verify ultralytics and python-shell are installed

3. **Database issues**:
   - Delete `yolov8_training.db` to reset database
   - Restart the server

4. **Frontend errors**:
   - Clear browser cache
   - Run `npm install` in client directory
   - Restart development server

## Project Structure

```
YoloV11_Training/
├── client/               # React frontend
│   ├── public/           # Static assets
│   └── src/              # React components
├── dataset/              # Training datasets
├── scripts/              # Python training scripts
├── server.js             # Express backend
├── data.yaml             # Dataset configuration
└── package.json          # Backend dependencies
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.