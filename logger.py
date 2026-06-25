# Logs mood detections to SQLite

import sqlite3
import time
from config import DB_PATH

def init_db():
    con = sqlite3.connect(DB_PATH)
    con.execute("""
        CREATE TABLE IF NOT EXISTS mood_log (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp REAL,
            emotion   TEXT,
            happy     REAL,
            sad       REAL,
            angry     REAL,
            fear      REAL,
            surprise  REAL,
            disgust   REAL,
            neutral   REAL
        )
    """)
    con.commit()
    con.close()

def log_mood(emotion, scores):
    con = sqlite3.connect(DB_PATH)
    con.execute("""
        INSERT INTO mood_log
            (timestamp, emotion, happy, sad, angry, fear, surprise, disgust, neutral)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        time.time(),
        emotion,
        scores.get("happy", 0),
        scores.get("sad", 0),
        scores.get("angry", 0),
        scores.get("fear", 0),
        scores.get("surprise", 0),
        scores.get("disgust", 0),
        scores.get("neutral", 0),
    ))
    con.commit()
    con.close()

def fetch_recent(minutes):
    since = time.time() - (minutes * 60)
    con = sqlite3.connect(DB_PATH)
    rows = con.execute("""
        SELECT timestamp, emotion, happy, sad, angry, fear, surprise, disgust, neutral
        FROM mood_log
        WHERE timestamp >= ?
        ORDER BY timestamp ASC
    """, (since,)).fetchall()
    con.close()
    return rows

def fetch_all_session():
    con = sqlite3.connect(DB_PATH)
    rows = con.execute("""
        SELECT timestamp, emotion, happy, sad, angry, fear, surprise, disgust, neutral
        FROM mood_log ORDER BY timestamp ASC
    """).fetchall()
    con.close()
    return rows