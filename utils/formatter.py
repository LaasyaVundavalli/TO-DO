from datetime import datetime, date
from colorama import Fore, init

init()

def format_task(task):
    today = date.today()
    color = Fore.YELLOW  # default pending
    if task.status == 'completed':
        color = Fore.GREEN
    elif task.due_date:
        try:
            due = datetime.strptime(task.due_date, '%Y-%m-%d').date()
            if due < today:
                color = Fore.RED
            elif due == today:
                color = Fore.BLUE
        except ValueError:
            pass
    card = f"""{color}---------------------------
Task ID: {task.id}
Title: {task.title}
Description: {task.description or 'N/A'}
Priority: {task.priority.title()}
Due Date: {task.due_date or 'N/A'}
Status: {task.status.title()}
Created At: {task.created_at}
Updated At: {task.updated_at}
---------------------------{Fore.RESET}"""
    return card

def format_task_list(tasks):
    return '\n\n'.join(format_task(task) for task in tasks)
