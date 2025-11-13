import sqlite3
from datetime import datetime
from ..database.db import get_connection

class Task:
    def __init__(self, id, user_id, title, description, priority, due_date, status, created_at, updated_at):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.description = description
        self.priority = priority
        self.due_date = due_date
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def create_task(cls, user_id, title, description=None, priority='medium', due_date=None):
        if priority not in ['low', 'medium', 'high']:
            raise ValueError("Invalid priority")
        conn = get_connection()
        try:
            cursor = conn.cursor()
            created_at = datetime.now()
            updated_at = created_at
            cursor.execute(
                "INSERT INTO tasks (user_id, title, description, priority, due_date, status, created_at, updated_at) VALUES (?, ?, ?, ?, ?, 'pending', ?, ?)",
                (user_id, title, description, priority, due_date, created_at, updated_at)
            )
            conn.commit()
            task_id = cursor.lastrowid
            return cls(task_id, user_id, title, description, priority, due_date, 'pending', created_at, updated_at)
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            raise
        finally:
            conn.close()

    @classmethod
    def find_by_id(cls, task_id):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, user_id, title, description, priority, due_date, status, created_at, updated_at FROM tasks WHERE id = ?", (task_id,))
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
    def find_by_user_id(cls, user_id, status=None, priority=None, sort_by='created_at', order='ASC'):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            query = "SELECT id, user_id, title, description, priority, due_date, status, created_at, updated_at FROM tasks WHERE user_id = ?"
            params = [user_id]
            if status:
                query += " AND status = ?"
                params.append(status)
            if priority:
                query += " AND priority = ?"
                params.append(priority)
            if sort_by in ['created_at', 'updated_at', 'due_date', 'priority', 'status']:
                query += f" ORDER BY {sort_by} {order.upper()}"
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [cls(*row) for row in rows]
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            raise
        finally:
            conn.close()

    @classmethod
    def update_task(cls, task_id, **kwargs):
        allowed_fields = ['title', 'description', 'priority', 'due_date', 'status']
        updates = {}
        for key, value in kwargs.items():
            if key in allowed_fields:
                if key == 'priority' and value not in ['low', 'medium', 'high']:
                    raise ValueError("Invalid priority")
                if key == 'status' and value not in ['pending', 'completed']:
                    raise ValueError("Invalid status")
                updates[key] = value
        if not updates:
            return None
        updates['updated_at'] = datetime.now()
        set_clause = ', '.join(f"{k} = ?" for k in updates.keys())
        values = list(updates.values()) + [task_id]
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(f"UPDATE tasks SET {set_clause} WHERE id = ?", values)
            conn.commit()
            if cursor.rowcount > 0:
                return cls.find_by_id(task_id)
            return None
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            raise
        finally:
            conn.close()

    @classmethod
    def delete_task(cls, task_id):
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            raise
        finally:
            conn.close()

    @classmethod
    def mark_done(cls, task_id):
        return cls.update_task(task_id, status='completed')

    @classmethod
    def reopen(cls, task_id):
        return cls.update_task(task_id, status='pending')
