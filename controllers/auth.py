import bcrypt
import os
from ..models.user_model import User

current_user = None
SESSION_FILE = '.todo_session'

def signup(username, password):
    try:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user = User.create_user(username, hashed_password.decode('utf-8'))
        return user is not None
    except Exception as e:
        print(f"Error during signup: {e}")
        return False

def login(username, password):
    global current_user
    try:
        user = User.find_by_username(username)
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
            current_user = user
            save_session()
            return True
        return False
    except Exception as e:
        print(f"Error during login: {e}")
        return False

def logout():
    global current_user
    current_user = None
    save_session()

def get_current_user():
    return current_user

def is_logged_in():
    return current_user is not None

def save_session():
    if current_user:
        with open(SESSION_FILE, 'w') as f:
            f.write(current_user.username)
    else:
        if os.path.exists(SESSION_FILE):
            os.remove(SESSION_FILE)

def load_session():
    global current_user
    if os.path.exists(SESSION_FILE):
        try:
            with open(SESSION_FILE, 'r') as f:
                username = f.read().strip()
                user = User.find_by_username(username)
                if user:
                    current_user = user
        except Exception:
            pass  # Ignore errors

load_session()
