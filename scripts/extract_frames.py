# scripts/extract_frames.py
 
import cv2

import os
 
def extract_frames_from_videos(videos_dir, output_dir, frame_rate=1):

    """

    Extract frames from all videos in the specified directory.
 
    :param videos_dir: Directory containing video files.

    :param output_dir: Directory to save extracted frames.

    :param frame_rate: Number of frames to extract per second.

    """

    if not os.path.exists(output_dir):

        os.makedirs(output_dir)

        print(f"Created directory: {output_dir}")
 
    video_files = [f for f in os.listdir(videos_dir) if f.lower().endswith(('.mp4', '.avi', '.mov', '.mkv'))]
 
    for video_file in video_files:

        video_path = os.path.join(videos_dir, video_file)

        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():

            print(f"Error: Could not open video {video_file}. Skipping.")

            continue
 
        fps = cap.get(cv2.CAP_PROP_FPS)

        interval = max(int(fps / frame_rate), 1)  # Ensure interval is at least 1
 
        count = 0

        frame_count = 0

        while True:

            ret, frame = cap.read()

            if not ret:

                break

            if count % interval == 0:

                frame_filename = os.path.join(output_dir, f"{os.path.splitext(video_file)[0]}_frame_{frame_count}.jpg")

                cv2.imwrite(frame_filename, frame)

                frame_count += 1

            count += 1
 
        cap.release()

        print(f"Extracted {frame_count} frames from {video_file}.")
 
if __name__ == "__main__":

    extract_frames_from_videos(

        videos_dir=os.path.abspath("../dataset/videos"),

        output_dir=os.path.abspath("../dataset/extracted_frames"),

        frame_rate=1  # Extract 1 frame per second

    )
