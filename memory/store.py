# memory/store.py

import sqlite3
from datetime import datetime

DB_PATH = "memory/apk_memory.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            user_message TEXT NOT NULL,
            assistant_reply TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            timestamp TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def save_message(session_id, user_message, assistant_reply):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO conversations (session_id, user_message, assistant_reply, timestamp)
        VALUES (?, ?, ?, ?)
    """, (
        session_id,
        user_message,
        assistant_reply,
        datetime.utcnow().isoformat()
    ))

    conn.commit()
    conn.close()


def save_lead(session_id, email=None, phone=None):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO leads (session_id, email, phone, timestamp)
        VALUES (?, ?, ?, ?)
    """, (
        session_id,
        email,
        phone,
        datetime.utcnow().isoformat()
    ))

    conn.commit()
    conn.close()
