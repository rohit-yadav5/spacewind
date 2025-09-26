

import cv2
import os

# List of sign words you want to capture
sign_words = ["hello", "thankyou", "yes", "no", "help", "food", "water"]

# Create folder to save images
save_dir = "signs"
os.makedirs(save_dir, exist_ok=True)

# Open webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Error: Could not open webcam.")
    exit()

print("✅ Webcam started. Follow the prompts.")
print("Press SPACE to capture, ESC to quit.")

for word in sign_words:
    print(f"\n➡️ Perform the sign for: {word.upper()}")
    captured = False

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to grab frame.")
            break

        # Show the frame with instructions
        cv2.putText(frame, f"Show sign for: {word.upper()}", (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.imshow("Sign Capture", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == 27:  # ESC key
            print("🚪 Exiting...")
            cap.release()
            cv2.destroyAllWindows()
            exit()

        elif key == 32:  # SPACE key
            filename = os.path.join(save_dir, f"{word}.jpg")
            cv2.imwrite(filename, frame)
            print(f"💾 Saved: {filename}")
            captured = True
            break

    if not captured:
        print(f"⚠️ Skipped: {word}")

cap.release()
cv2.destroyAllWindows()
print("✅ Image collection completed.")