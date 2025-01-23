# scripts/verify_video.py
 
from ultralytics import YOLO

import cv2

import os
 
def verify_text_in_video(video_path, model, output_message="This text verified", confidence_threshold=0.5):

    """

    Detect and verify specific text in a video.
 
    :param video_path: Path to the input video.

    :param model: Trained YOLOv8 model.

    :param output_message: Message to display when text is verified.

    :param confidence_threshold: Minimum confidence to consider detection valid.

    """

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():

        print(f"Error: Could not open video {video_path}.")

        return
 
    while True:

        ret, frame = cap.read()

        if not ret:

            break
 
        # Perform inference

        results = model(frame, verbose=False)
 
        # Initialize detection flag

        detected = False
 
        # Iterate through detections

        for result in results:

            boxes = result.boxes

            for box in boxes:

                class_id = int(box.cls[0])

                confidence = box.conf[0]

                if class_id == 0 and confidence >= confidence_threshold:

                    detected = True

                    # Draw bounding box

                    box_coords = box.xyxy[0].cpu().numpy()

                    x1, y1, x2, y2 = map(int, box_coords)

                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                    # Add class label and confidence

                    label = f"{model.names[class_id]} {confidence:.2f}"

                    cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
 
        if detected:

            # Overlay the verification message on the frame

            cv2.putText(frame, output_message, (50, 50),

                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
 
        # Display the frame (optional)

        cv2.imshow('Video Verification', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):

            break
 
    cap.release()

    cv2.destroyAllWindows()

    print("Verification completed.")
 
def verify_and_save_video(input_video, output_video, model, output_message="This text verified", confidence_threshold=0.5):

    """

    Detect specific text in a video and save the annotated video.
 
    :param input_video: Path to the input video.

    :param output_video: Path to save the annotated output video.

    :param model: Trained YOLOv8 model.

    :param output_message: Message to display when text is verified.

    :param confidence_threshold: Minimum confidence to consider detection valid.

    """

    cap = cv2.VideoCapture(input_video)

    if not cap.isOpened():

        print(f"Error: Could not open video {input_video}.")

        return
 
    # Get video properties

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fps = cap.get(cv2.CAP_PROP_FPS)
 
    # Define the codec and create VideoWriter object

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # You can use other codecs like 'XVID', 'MJPG', etc.

    out = cv2.VideoWriter(output_video, fourcc, fps, (width, height))
 
    while True:

        ret, frame = cap.read()

        if not ret:

            break
 
        # Perform inference

        results = model(frame, verbose=False)
 
        # Initialize detection flag

        detected = False
 
        # Iterate through detections

        for result in results:

            boxes = result.boxes

            for box in boxes:

                class_id = int(box.cls[0])

                confidence = box.conf[0]

                if class_id == 0 and confidence >= confidence_threshold:

                    detected = True

                    # Draw bounding box

                    box_coords = box.xyxy[0].cpu().numpy()

                    x1, y1, x2, y2 = map(int, box_coords)

                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                    # Add class label and confidence

                    label = f"{model.names[class_id]} {confidence:.2f}"

                    cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
 
        if detected:

            # Overlay the verification message on the frame

            cv2.putText(frame, output_message, (50, 50),

                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
 
        # Write the frame to the output video

        out.write(frame)
 
    cap.release()

    out.release()

    print(f"Output video saved to {output_video}")
 
if __name__ == "__main__":

    import argparse
 
    parser = argparse.ArgumentParser(description="Verify and annotate video with detected text.")

    parser.add_argument("--input", type=str, required=True, help="Path to the input video.")

    parser.add_argument("--output", type=str, required=False, help="Path to save the annotated video.")

    parser.add_argument("--model", type=str, required=True, help="Path to the trained YOLOv8 model.")

    parser.add_argument("--save", action='store_true', help="Flag to save the annotated video.")

    args = parser.parse_args()
 
    # Load the trained model

    model = YOLO(args.model)
 
    if args.save and args.output:

        verify_and_save_video(

            input_video=args.input,

            output_video=args.output,

            model=model,

            output_message="This text verified",

            confidence_threshold=0.5

        )

    else:

        verify_text_in_video(

            video_path=args.input,

            model=model,

            output_message="This text verified",

            confidence_threshold=0.5

        )
