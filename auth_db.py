import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_users_table():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

def register_user(username, password):
    try:
        conn = sqlite3.connect("users.db")
        c = conn.cursor()

        hashed = hash_password(password)

        c.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hashed)
        )

        conn.commit()
        conn.close()
        return True
    except:
        return False

def validate_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    hashed = hash_password(password)

    c.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, hashed)
    )

    user = c.fetchone()
    conn.close()
    return user
