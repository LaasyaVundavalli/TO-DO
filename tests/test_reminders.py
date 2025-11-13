import unittest
from datetime import date
from todo_app.models.task_model import Task
from todo_app.utils.notifications import check_reminders

class TestReminders(unittest.TestCase):
    def test_check_reminders(self):
        # Create mock tasks
        task_overdue = Task(1, 1, 'Overdue Task', None, 'medium', '2023-01-01', 'pending', None, None)
        task_today = Task(2, 1, 'Today Task', None, 'medium', str(date.today()), 'pending', None, None)
        task_future = Task(3, 1, 'Future Task', None, 'medium', '2025-12-31', 'pending', None, None)
        task_completed = Task(4, 1, 'Completed Task', None, 'medium', '2023-01-01', 'completed', None, None)

        tasks = [task_overdue, task_today, task_future, task_completed]
        result = check_reminders(tasks)

        self.assertEqual(len(result['overdue']), 1)
        self.assertEqual(result['overdue'][0].title, 'Overdue Task')
        self.assertEqual(len(result['due_today']), 1)
        self.assertEqual(result['due_today'][0].title, 'Today Task')

if __name__ == '__main__':
    unittest.main()
