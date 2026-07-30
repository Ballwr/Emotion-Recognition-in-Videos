import ctypes

# ---------------- HIDE CONSOLE ----------------
kernel32 = ctypes.windll.kernel32
console_hwnd = kernel32.GetConsoleWindow()

if console_hwnd:
    # 0 = SW_HIDE → hide console
    ctypes.windll.user32.ShowWindow(console_hwnd, 0)

# ---------------- SCRIPT STARTS HERE ----------------
import cv2
import time
from deepface import DeepFace
import os
import numpy as np

# --- Configuration ---
video_path = "Static.mp4"
folder = os.path.dirname(os.path.abspath(__file__))

emotion_images = {
    "happy": os.path.join(folder, "happy.jpg"),
    "sad": os.path.join(folder, "sad.jpg"),
    "angry": os.path.join(folder, "angry.jpg"),
    "surprise": os.path.join(folder, "surprise.jpg"),
    "neutral": os.path.join(folder, "neutral.jpg")
}

video_window = "Video Feed"
emotion_window = "Emotion Display"

# --- Load Images ---
emotion_imgs = {}
for emotion, path in emotion_images.items():
    img = cv2.imread(path)
    if img is not None:
        img = cv2.resize(img, (480, 360))
        emotion_imgs[emotion] = img
    else:
        emotion_imgs[emotion] = 255 * np.ones((360, 480, 3), dtype=np.uint8)

# --- Open Video ---
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print("Error: Cannot open video file.")
    exit()

cv2.namedWindow(video_window, cv2.WINDOW_NORMAL)
cv2.namedWindow(emotion_window, cv2.WINDOW_NORMAL)
cv2.resizeWindow(video_window, 720, 480)
cv2.resizeWindow(emotion_window, 480, 480)

fps = int(cap.get(cv2.CAP_PROP_FPS))
delay = int(1000 / (fps if fps > 0 else 25))

last_checked_time = time.time()
emotion_start_time = None
prev_emotion = "neutral"
current_emotion = "neutral"

# --- Helper Function ---
def map_emotion(emotion):
    emotion = emotion.lower()
    if emotion in ["happiness", "happy"]:
        return "happy"
    elif emotion in ["sadness", "sad"]:
        return "sad"
    elif emotion in ["anger", "angry", "disgust", "fear"]:
        return "angry"
    elif emotion in ["surprise"]:
        return "surprise"
    else:
        return "neutral"

# --- Main Loop ---
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_small = cv2.resize(frame, (480, 360))

    current_time = time.time()
    if current_time - last_checked_time >= 2:
        last_checked_time = current_time
        try:
            result = DeepFace.analyze(frame_small, actions=['emotion'], enforce_detection=False)
            dominant_emotion = map_emotion(result[0]['dominant_emotion'])
        except Exception:
            dominant_emotion = prev_emotion

        if dominant_emotion == prev_emotion:
            if emotion_start_time is None:
                emotion_start_time = current_time
            elif current_time - emotion_start_time >= 2:
                current_emotion = dominant_emotion
        else:
            emotion_start_time = current_time
            prev_emotion = dominant_emotion

    # Display emotion text
    label_text = f"Emotion: {current_emotion.upper()}"
    cv2.putText(frame_small, label_text, (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    cv2.imshow(video_window, frame_small)
    display_img = emotion_imgs.get(current_emotion, emotion_imgs.get("neutral"))
    cv2.imshow(emotion_window, display_img)

    key = cv2.waitKey(delay) & 0xFF
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# ---------------- SHOW CONSOLE AGAIN ----------------
if console_hwnd:
    # 1 = SW_SHOWNORMAL → show console again
    ctypes.windll.user32.ShowWindow(console_hwnd, 1)
