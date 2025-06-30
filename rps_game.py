import cv2
import mediapipe as mp
import time
import pyttsx3
import numpy as np

# Initialize pyttsx3
engine = pyttsx3.init()
engine.setProperty('rate', 150)

# Load gesture images
gesture_images = {
    "rock": cv2.imread("rock.jpeg"),
    "paper": cv2.imread("paper.jpeg"),
    "scissors": cv2.imread("scissors.jpeg")
}

# Resize gesture icons
for key in gesture_images:
    gesture_images[key] = cv2.resize(gesture_images[key], (100, 100))

# Initialize MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7)

# Gesture detection function (improved)
def get_hand_gesture(landmarks):
    def is_finger_open(tip_id, pip_id):
        return landmarks[tip_id].y < landmarks[pip_id].y - 0.03

    thumb_open = False
    if landmarks[17].x < landmarks[5].x:
        thumb_open = landmarks[4].x < landmarks[3].x - 0.04
    else:
        thumb_open = landmarks[4].x > landmarks[3].x + 0.04

    index_open = is_finger_open(8, 6)
    middle_open = is_finger_open(12, 10)
    ring_open = is_finger_open(16, 14)
    pinky_open = is_finger_open(20, 18)

    fingers = [thumb_open, index_open, middle_open, ring_open, pinky_open]
    finger_states = [1 if f else 0 for f in fingers]

    if finger_states == [0, 0, 0, 0, 0]:
        return "rock"
    elif sum(finger_states) >= 4:  # relaxed condition for paper
        return "paper"
    elif finger_states[1] == 1 and finger_states[2] == 1 and finger_states[3] == 0 and finger_states[4] == 0:
        return "scissors"
    else:
        return "unknown"

# Decide winner
def get_winner(p1, p2):
    if p1 == p2:
        return "Draw"
    elif (p1 == "rock" and p2 == "scissors") or \
         (p1 == "scissors" and p2 == "paper") or \
         (p1 == "paper" and p2 == "rock"):
        return "Player 1"
    else:
        return "Player 2"

# Speak result
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Initialize webcam
cap = cv2.VideoCapture(0)
start_time = 0
show_result = False
p1_move = ""
p2_move = ""
result = ""
p1_score = 0
p2_score = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)
    h, w, c = frame.shape

    if results.multi_hand_landmarks and len(results.multi_hand_landmarks) == 2:
        hand1 = results.multi_hand_landmarks[0]
        hand2 = results.multi_hand_landmarks[1]

        # Draw hands
        mp_drawing.draw_landmarks(
            frame, hand1, mp_hands.HAND_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=4),
            mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2)
        )
        mp_drawing.draw_landmarks(
            frame, hand2, mp_hands.HAND_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=4),
            mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2)
        )

        if not show_result:
            start_time = time.time()
            show_result = True

        elapsed = time.time() - start_time
        cv2.putText(frame, f"Show Moves In: {3 - int(elapsed)}", (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 3)

        if elapsed > 3:
            p1_move = get_hand_gesture(hand1.landmark)
            p2_move = get_hand_gesture(hand2.landmark)
            result = get_winner(p1_move, p2_move)

            if result == "Player 1":
                p1_score += 1
            elif result == "Player 2":
                p2_score += 1

            if result != "Draw" and p1_move != "unknown" and p2_move != "unknown":
                speak(f"{result} wins!")
            elif result == "Draw":
                speak("It's a draw!")

            show_result = False

    # Show moves
    if p1_move in gesture_images:
        frame[10:110, 400:500] = gesture_images[p1_move]
        cv2.putText(frame, "P1", (400, 105), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

    if p2_move in gesture_images:
        frame[10:110, 510:610] = gesture_images[p2_move]
        cv2.putText(frame, "P2", (510, 105), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

    # Show result and scores
    if result:
        cv2.putText(frame, f"Result: {result}", (10, 140), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
    cv2.putText(frame, f"Score - P1: {p1_score}  P2: {p2_score}", (10, 180),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

    cv2.imshow("Rock Paper Scissors - 2 Players", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
