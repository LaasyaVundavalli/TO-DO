import unittest
import os
from todo_app.controllers.auth import signup, login, logout, get_current_user
from todo_app.database.db import set_db_path, initialize_database

class TestAuth(unittest.TestCase):
    def setUp(self):
        self.test_db = 'test_todo.db'
        set_db_path(self.test_db)
        initialize_database()

    def tearDown(self):
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_signup_successful(self):
        result = signup('testuser', 'password')
        self.assertTrue(result)

    def test_signup_duplicate_username(self):
        signup('testuser', 'password')
        result = signup('testuser', 'password2')
        self.assertFalse(result)

    def test_login_valid(self):
        signup('testuser', 'password')
        result = login('testuser', 'password')
        self.assertTrue(result)
        self.assertIsNotNone(get_current_user())

    def test_login_invalid_password(self):
        signup('testuser', 'password')
        result = login('testuser', 'wrong')
        self.assertFalse(result)
        self.assertIsNone(get_current_user())

    def test_login_non_existent_user(self):
        result = login('nonexistent', 'password')
        self.assertFalse(result)
        self.assertIsNone(get_current_user())

    def test_logout(self):
        signup('testuser', 'password')
        login('testuser', 'password')
        self.assertIsNotNone(get_current_user())
        logout()
        self.assertIsNone(get_current_user())

if __name__ == '__main__':
    unittest.main()
