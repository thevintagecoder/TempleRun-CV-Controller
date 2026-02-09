import cv2
import mediapipe as mp
import pyautogui
import time
from collections import Counter

# --- CONFIGURATION ---
# Key Mappings (Adjust if your game uses 'a'/'d' for lanes)
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
history = [] 
history_length = 5
last_action_time = 0 
cooldown = 0.5 # Seconds

def get_finger_state(hand_landmarks):
    """Returns 'OPEN', 'CLOSED', or 'NEUTRAL' based on fingers."""
    fingers = []
    
    # Thumb (Right Hand Assumption)
    if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # 4 Fingers
    tips = [8, 12, 16, 20]
    pips = [6, 10, 14, 18]
    
    for i in range(4):
        if hand_landmarks.landmark[tips[i]].y < hand_landmarks.landmark[pips[i]].y:
            fingers.append(1)
        else:
            fingers.append(0)
            
    total_fingers = fingers.count(1)
    
    if total_fingers >= 4:
        return "JUMP"
    elif total_fingers <= 1:
        return "SLIDE"
    else:
        return "NEUTRAL"

print("System Ready! Press 'q' to quit.")

while cap.isOpened():
    success, image = cap.read()
    if not success:
        break

    # Flip image
    image = cv2.flip(image, 1)
    height, width, _ = image.shape
    
    # --- DRAW ZONES (Visual Feedback) ---
    # Draw vertical lines at 20% and 80% of the screen
    # Left Zone Line
    cv2.line(image, (int(width * 0.2), 0), (int(width * 0.2), height), (0, 255, 255), 2)
    # Right Zone Line
    cv2.line(image, (int(width * 0.8), 0), (int(width * 0.8), height), (0, 255, 255), 2)
    
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

    frame_gesture = "IDLE"

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            wrist_x = hand_landmarks.landmark[0].x
            
            # 1. Check Zones
            if wrist_x < 0.2:
                frame_gesture = "LEFT"
            elif wrist_x > 0.8:
                frame_gesture = "RIGHT"
            else:
                # Only check jump/slide if we are in the CENTER zone
                frame_gesture = get_finger_state(hand_landmarks)

    # --- STABILITY & ACTION ---
    history.append(frame_gesture)
    if len(history) > history_length:
        history.pop(0)

    most_common_gesture = Counter(history).most_common(1)[0][0]

    # LOGIC CHANGE: Only press key if the ACTION CHANGED
    # This prevents holding the key down forever
    if most_common_gesture != current_action:
        current_action = most_common_gesture
        
        # We only trigger the key press ONCE when the state switches
        if current_action == "LEFT":
            print("Turning Left")
            pyautogui.press(LEFT_KEY)
        elif current_action == "RIGHT":
            print("Turning Right")
            pyautogui.press(RIGHT_KEY)
        elif current_action == "JUMP":
            print("Jumping")
            pyautogui.press(JUMP_KEY)
        elif current_action == "SLIDE":
            print("Sliding")
            pyautogui.press(SLIDE_KEY)

    # UI Display
    cv2.putText(image, f"Current: {current_action}", (10, 50), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    # Add Zone Labels
    cv2.putText(image, "LEFT", (10, height - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    cv2.putText(image, "RIGHT", (width - 100, height - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    cv2.imshow('Temple Run Controller', image)

    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()