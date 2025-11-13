import sqlite3
from datetime import datetime
from ..database.db import get_connection

class User:
    def __init__(self, id, username, password_hash, created_at):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.created_at = created_at

    @classmethod
    def create_user(cls, username, password_hash):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            created_at = datetime.now()
            cursor.execute(
                "INSERT INTO users (username, password_hash, created_at) VALUES (?, ?, ?)",
                (username, password_hash, created_at)
            )
            conn.commit()
            user_id = cursor.lastrowid
            return cls(user_id, username, password_hash, created_at)
        except sqlite3.IntegrityError:
            # Duplicate username
            return None
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            raise
        finally:
            conn.close()

    @classmethod
    def find_by_username(cls, username):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, username, password_hash, created_at FROM users WHERE username = ?", (username,))
            row = cursor.fetchone()
            if row:
                return cls(*row)
            return None
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            raise
        finally:
            conn.close()

    @classmethod
    def find_by_id(cls, user_id):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, username, password_hash, created_at FROM users WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            if row:
                return cls(*row)
            return None
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            raise
        finally:
            conn.close()
