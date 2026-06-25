# All OpenCV drawing logic

import cv2
from config import MOOD_EMOJI

def draw_overlay(frame, emotion, scores):
    h, w = frame.shape[:2]

    emoji = MOOD_EMOJI.get(emotion, "")
    label = f"Mood: {emotion.upper()} {emoji}"
    cv2.putText(frame, label, (20, 45),
                cv2.FONT_HERSHEY_SIMPLEX, 1.1, (0, 255, 150), 2)

    if scores:
        bar_x, bar_y = 20, 80
        for i, (mood, score) in enumerate(sorted(scores.items(), key=lambda x: -x[1])):
            pct   = int(score)
            color = (0, 255, 150) if mood == emotion else (180, 180, 180)
            cv2.putText(frame, f"{mood:<10} {pct:>3}%",
                        (bar_x, bar_y + i * 24),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
            cv2.rectangle(frame,
                          (bar_x + 160, bar_y + i * 24 - 12),
                          (bar_x + 160 + pct, bar_y + i * 24 - 2),
                          color, -1)

    cv2.putText(frame, "Press Q to quit", (w - 180, h - 15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (120, 120, 120), 1)

def draw_no_face(frame):
    cv2.putText(frame, "No face detected", (20, 45),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 100, 255), 2)