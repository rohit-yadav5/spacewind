import cv2
import os
import re
import logging
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Set absolute paths for 'signs' and 'outputs' directories relative to this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
signs_dir = os.path.join(SCRIPT_DIR, "signs")
outputs_dir = os.path.join(SCRIPT_DIR, "outputs")
os.makedirs(outputs_dir, exist_ok=True)

def generate_video_from_text(text: str, duration_per_word: int = 2) -> dict:
    # Find the highest existing output file number in outputs directory
    output_pattern = re.compile(r'output(\d+)\.mp4')
    existing_numbers = []
    for filename in os.listdir(outputs_dir):
        match = output_pattern.match(filename)
        if match:
            existing_numbers.append(int(match.group(1)))
    next_number = max(existing_numbers) + 1 if existing_numbers else 1

    # Output video file with incremental numbering inside outputs directory
    output_file = os.path.join(outputs_dir, f"output{next_number}.mp4")

    words = text.strip().lower().split()

    if not words:
        logging.warning("⚠️ No valid words found in input.")
        return {"video_path": "", "processed_words": []}

    # Validate if all sign videos exist
    sign_videos = []
    processed_words = []
    for word in words:
        video_path = os.path.join(signs_dir, f"{word}.mp4")
        if not os.path.exists(video_path):
            logging.error(f"❌ Error: No video found for word '{word}' in {signs_dir}")
            raise FileNotFoundError(f"No video found for word '{word}' in {signs_dir}")
        sign_videos.append(video_path)
        processed_words.append(word)

    # Read all videos and collect frames resized to first video's size
    frames = []
    fps = None
    width = None
    height = None

    for video_path in sign_videos:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            logging.error(f"❌ Error: Could not open video file {video_path}")
            raise IOError(f"Could not open video file {video_path}")

        # Get video properties
        video_fps = cap.get(cv2.CAP_PROP_FPS)
        video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        if fps is None:
            fps = video_fps
        else:
            if abs(fps - video_fps) > 0.01:
                logging.warning(f"⚠️ FPS mismatch: expected {fps}, got {video_fps} in {video_path}")

        if width is None or height is None:
            width, height = video_width, video_height
        else:
            if width != video_width or height != video_height:
                logging.warning(f"⚠️ Resolution mismatch: expected {width}x{height}, got {video_width}x{video_height} in {video_path}")

        # Calculate number of frames to extract for duration_per_word seconds
        frames_needed = int(fps * duration_per_word)

        # Read frames from video
        video_frames = []
        frame_count = 0
        while frame_count < frames_needed:
            ret, frame = cap.read()
            if not ret:
                break
            # Resize frame if needed
            if frame.shape[1] != width or frame.shape[0] != height:
                frame = cv2.resize(frame, (width, height))
            video_frames.append(frame)
            frame_count += 1

        # If video has fewer frames than needed, repeat last frame
        if len(video_frames) < frames_needed:
            if video_frames:
                last_frame = video_frames[-1]
                while len(video_frames) < frames_needed:
                    video_frames.append(last_frame)
            else:
                logging.warning(f"⚠️ Video {video_path} has no frames, skipping.")
                cap.release()
                continue

        frames.extend(video_frames)
        cap.release()

    if not frames:
        logging.error("❌ Error: No frames to write to output video.")
        return {"video_path": "", "processed_words": processed_words}

    # Define video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

    for frame in frames:
        out.write(frame)

    out.release()
    logging.info(f"✅ Video generated: {output_file}")
    return {"video_path": output_file, "processed_words": processed_words}




if __name__ == "__main__":
    # Example test text
    text = input("Enter text to generate sign video: ").strip()
    try:
        result = generate_video_from_text(text)
        print("Processed words:", result["processed_words"])
        print("Video saved at:", result["video_path"])
    except Exception as e:
        print("Error:", e)