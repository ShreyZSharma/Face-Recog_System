# Live chart + session summary using matplotlib

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime
from collections import Counter
from config import LIVE_WINDOW_MINUTES, MOOD_EMOJI
from logger import fetch_recent, fetch_all_session

EMOTIONS      = ["happy", "sad", "angry", "fear", "surprise", "disgust", "neutral"]
COLORS        = ["#2ecc71","#3498db","#e74c3c","#9b59b6","#f39c12","#1abc9c","#95a5a6"]
EMOTION_COLOR = dict(zip(EMOTIONS, COLORS))

def start_live_chart():
    fig, ax = plt.subplots(figsize=(9, 4))
    fig.patch.set_facecolor("#1a1a2e")
    ax.set_facecolor("#16213e")
    fig.suptitle("Live Mood — Last 10 Minutes", color="white", fontsize=13)
    plt.tight_layout(pad=2)

    def update(_frame):
        ax.clear()
        ax.set_facecolor("#16213e")
        ax.set_ylim(0, 100)
        ax.set_ylabel("Confidence %", color="white")
        ax.tick_params(colors="white")
        for spine in ax.spines.values():
            spine.set_edgecolor("#444")

        rows = fetch_recent(LIVE_WINDOW_MINUTES)
        if not rows:
            ax.set_title("Waiting for data...", color="#888", fontsize=10)
            return

        times = [datetime.fromtimestamp(r[0]) for r in rows]
        for i, emotion in enumerate(EMOTIONS):
            scores = [r[i + 2] for r in rows]
            ax.plot(times, scores, label=emotion,
                    color=EMOTION_COLOR[emotion], linewidth=1.8)

        ax.legend(loc="upper left", fontsize=7,
                  facecolor="#1a1a2e", labelcolor="white", framealpha=0.6)
        fig.autofmt_xdate(rotation=30)

    ani = animation.FuncAnimation(fig, update, interval=2000, cache_frame_data=False)
    plt.show(block=False)
    return fig, ani

def show_summary():
    rows = fetch_all_session()
    if not rows:
        print("No mood data to summarise.")
        return

    emotions_logged = [r[1] for r in rows]
    counts  = Counter(emotions_logged)
    labels  = [f"{MOOD_EMOJI.get(e,'')}{e}  ({c})" for e, c in counts.most_common()]
    sizes   = [c for _, c in counts.most_common()]
    colors  = [EMOTION_COLOR.get(e, "#888") for e, _ in counts.most_common()]

    fig, (ax_pie, ax_bar) = plt.subplots(1, 2, figsize=(12, 5))
    fig.patch.set_facecolor("#1a1a2e")
    fig.suptitle("Session Summary", color="white", fontsize=15, fontweight="bold")

    ax_pie.set_facecolor("#16213e")
    ax_pie.pie(sizes, labels=labels, colors=colors,
               autopct="%1.1f%%", textprops={"color": "white", "fontsize": 9},
               wedgeprops={"linewidth": 0.5, "edgecolor": "#1a1a2e"})
    ax_pie.set_title("Emotion Breakdown", color="white")

    ax_bar.set_facecolor("#16213e")
    avg_scores = {e: sum(r[i+2] for r in rows) / len(rows)
                  for i, e in enumerate(EMOTIONS)}
    bars = ax_bar.bar(avg_scores.keys(), avg_scores.values(),
                      color=[EMOTION_COLOR[e] for e in avg_scores])
    ax_bar.set_ylim(0, 100)
    ax_bar.set_ylabel("Avg Confidence %", color="white")
    ax_bar.set_title("Average Score per Emotion", color="white")
    ax_bar.tick_params(colors="white")
    for spine in ax_bar.spines.values():
        spine.set_edgecolor("#444")
    for bar in bars:
        ax_bar.text(bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + 1,
                    f"{bar.get_height():.1f}",
                    ha="center", color="white", fontsize=8)

    plt.tight_layout(pad=2)
    plt.show()