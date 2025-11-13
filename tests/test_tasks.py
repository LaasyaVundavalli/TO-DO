import unittest
import os
from todo_app.controllers.auth import signup, login
from todo_app.controllers.tasks import add_task, edit_task, delete_task, list_tasks, view_task, mark_done, reopen
from todo_app.database.db import set_db_path, initialize_database

class TestTasks(unittest.TestCase):
    def setUp(self):
        self.test_db = 'test_todo.db'
        set_db_path(self.test_db)
        initialize_database()
        signup('testuser', 'password')
        login('testuser', 'password')

    def tearDown(self):
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_add_task(self):
        result = add_task('Test Task', 'Description', 'high', '2023-12-31')
        self.assertEqual(result, "Task added successfully")

    def test_edit_task(self):
        add_task('Test Task', 'Description')
        tasks = list_tasks()
        task_id = tasks[0].id
        result = edit_task(task_id, title='Updated Task')
        self.assertEqual(result, "Task updated successfully")

    def test_delete_task(self):
        add_task('Test Task')
        tasks = list_tasks()
        task_id = tasks[0].id
        result = delete_task(task_id)
        self.assertEqual(result, "Task deleted successfully")

    def test_list_tasks(self):
        add_task('Task 1')
        add_task('Task 2')
        tasks = list_tasks()
        self.assertEqual(len(tasks), 2)

    def test_view_task(self):
        add_task('Test Task')
        tasks = list_tasks()
        task_id = tasks[0].id
        task = view_task(task_id)
        self.assertIsNotNone(task)
        self.assertEqual(task.title, 'Test Task')

    def test_mark_done(self):
        add_task('Test Task')
        tasks = list_tasks()
        task_id = tasks[0].id
        result = mark_done(task_id)
        self.assertEqual(result, "Task marked as done")
        task = view_task(task_id)
        self.assertEqual(task.status, 'completed')

    def test_reopen(self):
        add_task('Test Task')
        tasks = list_tasks()
        task_id = tasks[0].id
        mark_done(task_id)
        result = reopen(task_id)
        self.assertEqual(result, "Task reopened")
        task = view_task(task_id)
        self.assertEqual(task.status, 'pending')

if __name__ == '__main__':
    unittest.main()
