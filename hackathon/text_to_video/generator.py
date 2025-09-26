import cv2
import os
import re
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Path to folder containing collected sign images
signs_dir = "signs"

# Ensure 'outputs' directory exists
outputs_dir = "outputs"
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

    # Validate if all images exist
    images = []
    processed_words = []
    for word in words:
        img_path = os.path.join(signs_dir, f"{word}.jpg")
        if not os.path.exists(img_path):
            logging.error(f"❌ Error: No image found for word '{word}' in {signs_dir}")
            raise FileNotFoundError(f"No image found for word '{word}' in {signs_dir}")
        images.append(img_path)
        processed_words.append(word)

    # Load first image to get dimensions
    frame = cv2.imread(images[0])
    if frame is None:
        logging.error("❌ Error: Could not read the first image.")
        raise IOError("Could not read the first image.")

    height, width, layers = frame.shape
    size = (width, height)

    # Define video writer (30 frames per second, slideshow style)
    fps = 30
    out = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*'mp4v'), fps, size)

    # Write each image multiple times to simulate video duration
    frames_per_image = int(fps * duration_per_word)
    for img_path in images:
        img = cv2.imread(img_path)
        if img is None:
            logging.warning(f"⚠️ Skipping unreadable image: {img_path}")
            continue
        resized = cv2.resize(img, size)
        for _ in range(frames_per_image):
            out.write(resized)

    out.release()
    logging.info(f"✅ Video generated: {output_file}")
    return {"video_path": output_file, "processed_words": processed_words}