import cv2
import time
import matplotlib.pyplot as plt
from config import ANALYSIS_INTERVAL, CAMERA_INDEX
from detector import analyze_mood
from overlay import draw_overlay, draw_no_face
from logger import init_db, log_mood
from visualizer import start_live_chart, show_summary

def main():
    init_db()

    print("Starting mood detector... (press Q to quit)")
    cap = cv2.VideoCapture(CAMERA_INDEX)
    if not cap.isOpened():
        print("Error: Cannot access webcam.")
        return

    fig, ani = start_live_chart()
    plt.pause(0.1)

    emotion, scores = None, None
    last_analysis   = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        now = time.time()
        if now - last_analysis >= ANALYSIS_INTERVAL:
            new_emotion, new_scores = analyze_mood(frame)
            if new_emotion:
                emotion, scores = new_emotion, new_scores
                log_mood(emotion, scores)
            last_analysis = now

        display = frame.copy()
        if emotion:
            draw_overlay(display, emotion, scores)
        else:
            draw_no_face(display)

        cv2.imshow("Mood Detector", display)
        plt.pause(0.001)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    plt.close(fig)
    show_summary()

if __name__ == "__main__":
    main()