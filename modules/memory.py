import sqlite3
import datetime
from config import DB_PATH, JARVIS_NAME

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            user_input TEXT NOT NULL,
            jarvis_response TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS facts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT UNIQUE NOT NULL,
            value TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT NOT NULL,
            remind_at TEXT NOT NULL,
            done INTEGER DEFAULT 0
        )
    ''')

    conn.commit()
    conn.close()
    print(f"[{JARVIS_NAME}] Memory database initialized.")

def save_conversation(user_input: str, jarvis_response: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO conversations (timestamp, user_input, jarvis_response) VALUES (?, ?, ?)",
        (timestamp, user_input, jarvis_response)
    )
    conn.commit()
    conn.close()

def get_recent_conversations(limit: int = 10) -> list:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT timestamp, user_input, jarvis_response FROM conversations ORDER BY id DESC LIMIT ?",
        (limit,)
    )
    rows = cursor.fetchall()
    conn.close()
    return rows

def save_fact(key: str, value: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    updated_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO facts (key, value, updated_at) VALUES (?, ?, ?) ON CONFLICT(key) DO UPDATE SET value=?, updated_at=?",
        (key, value, updated_at, value, updated_at)
    )
    conn.commit()
    conn.close()

def get_fact(key: str) -> str:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM facts WHERE key = ?", (key,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

def get_all_facts() -> list:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT key, value FROM facts")
    rows = cursor.fetchall()
    conn.close()
    return rows

def clear_conversations():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM conversations")
    conn.commit()
    conn.close()
    return "Conversation history cleared from memory."

def search_conversations(keyword: str) -> list:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT timestamp, user_input, jarvis_response FROM conversations WHERE user_input LIKE ? OR jarvis_response LIKE ? ORDER BY id DESC LIMIT 5",
        (f"%{keyword}%", f"%{keyword}%")
    )
    rows = cursor.fetchall()
    conn.close()
    return rows
