import cv2
import os
import time

# List of sign words you want to capture
sign_words = [

'hello','hi','hey','good morning','good afternoon','good evening','good night','bye','goodbye','see you','take care','welcome',
"how are you","nice to meet you","long time no see","what's up",'hiya','yo','cheers','peace',

    
    ]

# Create folder to save images
save_dir = "signs"
os.makedirs(save_dir, exist_ok=True)

# Open webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Error: Could not open webcam.")
    exit()

print("✅ Webcam started. Follow the prompts.")
print("Press SPACE to start recording 2-second video, ESC to quit.")

fps = 30
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
duration = 2  # seconds
num_frames = int(fps * duration)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')

for word in sign_words:
    print(f"\n➡️ Perform the sign for: {word.upper()}")
    recorded = False

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to grab frame.")
            break

        # Show the frame with instructions
        cv2.putText(frame, f"Show sign for: {word.upper()}", (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, "Press SPACE to start recording", (30, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2, cv2.LINE_AA)
        cv2.imshow("Sign Capture", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == 27:  # ESC key
            print("🚪 Exiting...")
            cap.release()
            cv2.destroyAllWindows()
            exit()

        elif key == 32:  # SPACE key
            filename = os.path.join(save_dir, f"{word}.mp4")
            out = cv2.VideoWriter(filename, fourcc, fps, (frame_width, frame_height))
            print(f"🎥 Recording 2-second video for '{word}'...")
            frames_recorded = 0
            start_time = time.time()
            while frames_recorded < num_frames:
                ret, frame = cap.read()
                if not ret:
                    print("❌ Failed to grab frame during recording.")
                    break
                cv2.putText(frame, f"Recording: {word.upper()}", (30, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                cv2.imshow("Sign Capture", frame)
                out.write(frame)
                frames_recorded += 1

                if cv2.waitKey(1) & 0xFF == 27:
                    print("🚪 Exiting during recording...")
                    out.release()
                    cap.release()
                    cv2.destroyAllWindows()
                    exit()
            out.release()
            print(f"💾 Saved: {filename}")
            recorded = True
            break

    if not recorded:
        print(f"⚠️ Skipped: {word}")

cap.release()
cv2.destroyAllWindows()
print("✅ Video collection completed.")