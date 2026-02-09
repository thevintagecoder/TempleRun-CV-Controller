import cv2
import mediapipe as mp
import pyautogui
import time
from collections import Counter

# --- CONFIGURATION ---
JUMP_KEY = 'up'
SLIDE_KEY = 'down'
LEFT_KEY = 'left'
RIGHT_KEY = 'right'

# 1. Setup MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    max_num_hands=1, 
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)

# 2. Setup Webcam
cap = cv2.VideoCapture(0)

# 3. Game State Variables
current_action = "IDLE"
history = []  # We will store the last 5 frames of gestures here
history_length = 5  # How many frames to check for stability

def get_gesture(hand_landmarks):
    """
    Returns the name of the gesture based on landmarks.
    """
    fingers = []
    
    # Check Thumb (Horizontal) - Assuming Right Hand
    if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Check 4 Fingers (Vertical)
    # Tip (8,12,16,20) must be HIGHER (smaller Y) than Pip (6,10,14,18)
    tips = [8, 12, 16, 20]
    pips = [6, 10, 14, 18]
    
    for i in range(4):
        if hand_landmarks.landmark[tips[i]].y < hand_landmarks.landmark[pips[i]].y:
            fingers.append(1)
        else:
            fingers.append(0)
            
    total_fingers = fingers.count(1)
    
    # Return Gesture Name
    if total_fingers >= 4:
        return "JUMP"
    elif total_fingers <= 1:
        return "SLIDE"
    else:
        return "IDLE"

print("System Ready! Press 'q' to quit.")

while cap.isOpened():
    success, image = cap.read()
    if not success:
        break

    # Flip image
    image = cv2.flip(image, 1)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

    frame_gesture = "IDLE"

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # 1. Check Movement (Left/Right) - Priority #1
            wrist_x = hand_landmarks.landmark[0].x
            
            if wrist_x < 0.2:
                frame_gesture = "LEFT"
            elif wrist_x > 0.8:
                frame_gesture = "RIGHT"
            else:
                # 2. Check Fingers (Jump/Slide)
                frame_gesture = get_gesture(hand_landmarks)

    # --- STABILITY CHECK (The Fix) ---
    history.append(frame_gesture)
    if len(history) > history_length:
        history.pop(0)

    # Find the most common gesture in the last 5 frames
    # If we see ["JUMP", "JUMP", "IDLE", "JUMP", "JUMP"], it decides "JUMP"
    most_common_gesture = Counter(history).most_common(1)[0][0]

    # Only trigger if the stable gesture changes!
    if most_common_gesture != current_action:
        current_action = most_common_gesture
        
        if current_action == "LEFT":
            pyautogui.press(LEFT_KEY)
        elif current_action == "RIGHT":
            pyautogui.press(RIGHT_KEY)
        elif current_action == "JUMP":
            pyautogui.press(JUMP_KEY)
        elif current_action == "SLIDE":
            pyautogui.press(SLIDE_KEY)

    # UI Display
    color = (0, 255, 0) if current_action != "IDLE" else (0, 0, 255)
    cv2.putText(image, f"Action: {current_action}", (10, 50), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    
    cv2.imshow('Temple Run Controller', image)

    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()