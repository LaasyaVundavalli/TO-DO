from datetime import datetime, date
from colorama import Fore, init

def check_reminders(tasks):
    overdue = []
    due_today = []
    today = date.today()
    for task in tasks:
        if task.due_date and task.status == 'pending':
            try:
                due = datetime.strptime(task.due_date, '%Y-%m-%d').date()
                if due < today:
                    overdue.append(task)
                elif due == today:
                    due_today.append(task)
            except ValueError:
                pass  # invalid date, skip
    return {'overdue': overdue, 'due_today': due_today}

def display_notifications(notifications):
    init()
    for task in notifications['overdue']:
        print(f"{Fore.RED}🔔 Task Overdue: {task.title}{Fore.RESET}")
    for task in notifications['due_today']:
        print(f"{Fore.BLUE}🔔 Task Due Today: {task.title}{Fore.RESET}")
