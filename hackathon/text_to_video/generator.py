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

def generate_video_from_text(text: str, duration_per_char: float = 0.5) -> dict:
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

    chars = [ch.lower() for ch in text if ch != ' ']

    if not chars:
        logging.warning("⚠️ No valid characters found in input.")
        return {"video_path": "", "processed_chars": []}

    # Validate if all sign images exist
    sign_images = []
    processed_chars = []
    for ch in chars:
        image_path = os.path.join(signs_dir, f"{ch}.jpg")
        if not os.path.exists(image_path):
            logging.error(f"❌ Error: No image found for character '{ch}' in {signs_dir}")
            raise FileNotFoundError(f"No image found for character '{ch}' in {signs_dir}")
        sign_images.append(image_path)
        processed_chars.append(ch)

    # Read all images and collect them resized to the first image's size
    images = []
    width = None
    height = None

    for image_path in sign_images:
        img = cv2.imread(image_path)
        if img is None:
            logging.error(f"❌ Error: Could not read image file {image_path}")
            raise IOError(f"Could not read image file {image_path}")

        if width is None or height is None:
            height, width = img.shape[:2]
        else:
            if (img.shape[1], img.shape[0]) != (width, height):
                logging.warning(f"⚠️ Resolution mismatch: expected {width}x{height}, got {img.shape[1]}x{img.shape[0]} in {image_path}")
                img = cv2.resize(img, (width, height))

        images.append(img)

    # Define video properties
    fps = 30  # frames per second
    frames_per_image = int(duration_per_char * fps)

    # Prepare frames for video
    frames = []
    for img in images:
        for _ in range(frames_per_image):
            frames.append(img)

    if not frames:
        logging.error("❌ Error: No frames to write to output video.")
        return {"video_path": "", "processed_chars": processed_chars}

    # Define video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

    for frame in frames:
        out.write(frame)

    out.release()
    logging.info(f"✅ Video generated: {output_file}")
    return {"video_path": output_file, "processed_chars": processed_chars}




if __name__ == "__main__":
    # Example test text
    text = input("Enter text to generate sign video: ").strip()
    try:
        result = generate_video_from_text(text)
        print("Processed characters:", result["processed_chars"])
        print("Video saved at:", result["video_path"])
    except Exception as e:
        print("Error:", e)