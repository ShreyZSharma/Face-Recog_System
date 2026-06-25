# Face-Recog_System
AI-powered real-time mood detector using DeepFace and OpenCV. Tracks facial emotions live, logs to SQLite, and visualizes mood trends with matplotlib.
# Mood Detector 🎭

A real-time facial emotion detection system that analyzes your mood via webcam, logs data to a local database, and visualizes emotion trends live.

## Features
- Real-time face and emotion detection using DeepFace
- Live animated graph showing mood over the last 10 minutes
- Session summary with pie chart and bar chart breakdowns
- SQLite logging for persistent mood history

## Tech Stack
- Python
- DeepFace
- OpenCV
- Matplotlib
- SQLite

## Setup

1. Clone the repo
2. Create a virtual environment
3. Install dependencies
4. Run

## Usage
- Press `Q` to quit
- On exit, a session summary chart is displayed automatically

## Project Structure
- `main.py` — entry point
- `detector.py` — DeepFace emotion analysis
- `overlay.py` — webcam display and emotion overlay
- `visualizer.py` — live chart and session summary
- `logger.py` — SQLite logging
- `config.py` — configuration constants
