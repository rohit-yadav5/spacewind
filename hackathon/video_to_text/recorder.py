import cv2
import numpy as np

def detect_hand(frame):
    """Detects the largest skin-colored contour in the frame and returns its contour and bounding rect."""
    # Convert to HSV for skin color detection
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define lower and upper bounds for skin color in HSV
    lower_skin = np.array([0, 20, 70], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)
    mask = cv2.inRange(hsv, lower_skin, upper_skin)

    # Morphological operations to clean up the mask
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.dilate(mask, kernel, iterations=4)
    mask = cv2.GaussianBlur(mask, (7, 7), 0)

    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        # Find the largest contour
        max_contour = max(contours, key=cv2.contourArea)
        if cv2.contourArea(max_contour) > 1000:
            x, y, w, h = cv2.boundingRect(max_contour)
            return max_contour, (x, y, w, h)
    return None, None

def mock_classify_hand(contour, bbox, frame_shape):
    """
    Mock classifier:
      - If the hand is on the left 1/3 of the frame, return 'A'
      - If in the center 1/3, return 'B'
      - Else, return 'C'
    """
    if bbox is None:
        return None
    x, y, w, h = bbox
    center_x = x + w // 2
    width = frame_shape[1]
    if center_x < width // 3:
        return 'A'
    elif center_x < 2 * width // 3:
        return 'B'
    else:
        return 'C'

cap = cv2.VideoCapture(0)
sentence = ''
last_letter = None
letter_cooldown = 12  # frames to wait before accepting new same letter
cooldown_counter = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break
    # Flip the frame horizontally for natural (selfie-view) visualization.
    frame = cv2.flip(frame, 1)

    contour, bbox = detect_hand(frame)
    letter = None
    if contour is not None and bbox is not None:
        # Draw the contour and bounding box
        cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)
        x, y, w, h = bbox
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        letter = mock_classify_hand(contour, bbox, frame.shape)
        # Only append if cooldown expired or letter changed
        if letter is not None:
            if letter != last_letter or cooldown_counter == 0:
                sentence += letter
                last_letter = letter
                cooldown_counter = letter_cooldown
    if cooldown_counter > 0:
        cooldown_counter -= 1

    # Display the sentence on the frame.
    cv2.putText(frame, 'Sentence: ' + sentence, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

    cv2.imshow('Live Hand-to-Alphabet Recognition', frame)

    key = cv2.waitKey(1)
    if key == 27:  # ESC key to break
        break
    elif key == ord(' '):  # Space key to clear sentence
        sentence = ''
        last_letter = None
        cooldown_counter = 0

cap.release()
cv2.destroyAllWindows()
