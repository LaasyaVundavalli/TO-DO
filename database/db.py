import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'todo.db')
current_db_path = DB_PATH

def set_db_path(path):
    global current_db_path
    current_db_path = path

def get_connection():
    return sqlite3.connect(current_db_path)

def initialize_database():
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
        if not cursor.fetchone():
            migrations_path = os.path.join(os.path.dirname(__file__), 'migrations.sql')
            with open(migrations_path, 'r') as f:
                sql = f.read()
            conn.executescript(sql)
            conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        raise
    finally:
        conn.close()
