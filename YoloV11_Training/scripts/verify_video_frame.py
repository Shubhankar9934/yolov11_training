# # scripts/verify_video.py

from ultralytics import YOLO
import cv2
import os
import sys
import time
import torch  # Import torch to check for CUDA availability
 
def verify_and_save_frame(input_video, model, save_frame_dir, output_message="This text verified", confidence_threshold=0.5):
    """
    Detect specific text in a video, save the specific frame where detection occurred,
    and print the time taken for processing.
 
    :param input_video: Path to the input video.
    :param save_frame_dir: Directory to save the detected frame image.
    :param model: Trained YOLOv8 model.
    :param output_message: Message to display when text is verified.
    :param confidence_threshold: Minimum confidence to consider detection valid.
    """
    start_time = time.time()
 
    cap = cv2.VideoCapture(input_video)
    if not cap.isOpened():
        print(f"Error: Could not open video {input_video}.")
        return
 
    frame_count = 0
    detected = False
    detected_frame_number = 0
    detected_frame_image_path = ""
 
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Total frames in video: {total_frames}")
 
    while True:
        ret, frame = cap.read()
        if not ret:
            print("End of video reached or cannot read frame.")
            break
 
        # Check if the current video position exceeds 3 minutes
        current_time_ms = cap.get(cv2.CAP_PROP_POS_MSEC)
        if current_time_ms > 3 * 60 * 1000:  # 3 minutes in milliseconds
            print("Reached the 3-minute mark. Stopping further processing.")
            break
 
        frame_count += 1
 
        if frame_count % 100 == 0:
            print(f"Processing frame {frame_count}/{total_frames}")
 
        frame_start_time = time.time()
 
        # Perform inference
        results = model(frame)
 
        frame_end_time = time.time()
        frame_elapsed_time = frame_end_time - frame_start_time
        print(f"Frame {frame_count} processed in {frame_elapsed_time:.2f} seconds")
 
        # Iterate through detections
        for result in results:
            boxes = result.boxes
            for box in boxes:
                class_id = int(box.cls[0])
                confidence = box.conf[0]
                if class_id == 0 and confidence >= confidence_threshold:
                    detected = True
                    detected_frame_number = frame_count
 
                    # Draw bounding box
                    box_coords = box.xyxy[0].cpu().numpy()
                    x1, y1, x2, y2 = map(int, box_coords)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
 
                    # Add class label and confidence
                    label = f"{model.names[class_id]} {confidence:.2f}"
                    cv2.putText(frame, label, (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
 
                    # Overlay the verification message on the frame
                    cv2.putText(frame, output_message, (50, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
 
                    # Save the detected frame as an image
                    if not os.path.exists(save_frame_dir):
                        os.makedirs(save_frame_dir)
                        print(f"Created directory for detected frames: {save_frame_dir}")
 
                    detected_frame_image_path = os.path.join(
                        save_frame_dir, f"detected_frame_{detected_frame_number}.png")
                    cv2.imwrite(detected_frame_image_path, frame)
                    print(f"Detected text in frame {detected_frame_number}. Saved frame image to {detected_frame_image_path}.")
 
                    # Terminate processing
                    break  # Exit the boxes loop
 
            if detected:
                break  # Exit the results loop
 
        if detected:
            break  # Exit the frame processing loop
 
    cap.release()
    print("Video capture released.")
 
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Time taken for processing: {elapsed_time:.2f} seconds")
 
    if detected:
        print(f"\nText was verified in frame {detected_frame_number}.")
        print(f"Detected frame image saved to: {detected_frame_image_path}")
    else:
        print("\nFrame not detected.")
 
if __name__ == "__main__":
    import argparse
 
    parser = argparse.ArgumentParser(description="Verify video frames for specific text and save the detected frame if found.")
    parser.add_argument("--input", type=str, required=True, help="Path to the input video.")
    parser.add_argument("--model", type=str, required=True, help="Path to the trained YOLOv8 model (.pt file).")
    parser.add_argument("--confidence", type=float, default=0.95, help="Confidence threshold for detections (default: 0.5).")
    parser.add_argument("--save_frame_dir", type=str, default=os.path.abspath("../dataset/detected_frames"), help="Directory to save the detected frame image.")
    args = parser.parse_args()
 
    # Validate input arguments
    if not os.path.exists(args.input):
        print(f"Error: Input video {args.input} does not exist.")
        sys.exit(1)
    if not os.path.exists(args.model):
        print(f"Error: Model file {args.model} does not exist.")
        sys.exit(1)
 
    # Load the trained model and set device
    print("Loading the YOLOv8 model...")
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Using device: {device}")
    model = YOLO(args.model)
    model.to(device)
    print("Model loaded successfully.")
 
    # Run verification and save the frame if detected
    verify_and_save_frame(
        input_video=args.input,
        model=model,
        save_frame_dir=args.save_frame_dir,
        output_message="This text verified",
        confidence_threshold=args.confidence
    )