import cv2
import os
import re

# Path to folder containing collected sign images
signs_dir = "signs"

# Find the highest existing output file number
output_pattern = re.compile(r'output(\d+)\.mp4')
existing_numbers = []
for filename in os.listdir('.'):
    match = output_pattern.match(filename)
    if match:
        existing_numbers.append(int(match.group(1)))
next_number = max(existing_numbers) + 1 if existing_numbers else 1

# Output video file with incremental numbering
output_file = f"output{next_number}.mp4"

# Get input text
text = input("Enter a sentence to convert into sign video: ").strip().lower()
words = text.split()

# Validate if all images exist
images = []
for word in words:
    img_path = os.path.join(signs_dir, f"{word}.jpg")
    if not os.path.exists(img_path):
        print(f"❌ Error: No image found for word '{word}' in {signs_dir}")
        exit(1)
    images.append(img_path)

if not images:
    print("⚠️ No valid words found in input.")
    exit(1)

# Load first image to get dimensions
frame = cv2.imread(images[0])
if frame is None:
    print("❌ Error: Could not read the first image.")
    exit(1)

height, width, layers = frame.shape
size = (width, height)

# Define video writer (30 frames per second, slideshow style)
out = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*'mp4v'), 30, size)

# Write each image multiple times to simulate video duration (2 seconds per image)
for img_path in images:
    img = cv2.imread(img_path)
    if img is None:
        print(f"⚠️ Skipping unreadable image: {img_path}")
        continue
    resized = cv2.resize(img, size)
    for _ in range(60):  # show each image for ~2 seconds (60 frames at 30fps)
        out.write(resized)

out.release()
print(f"✅ Video generated: {output_file}")