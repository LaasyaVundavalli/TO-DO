from ..controllers.auth import is_logged_in, get_current_user
from ..models.task_model import Task
from datetime import date, datetime, timedelta

def add_task(title, description=None, priority='medium', due_date=None):
    if not is_logged_in():
        return "User not logged in"
    current_user = get_current_user()
    user_id = current_user.id
    if priority not in ['low', 'medium', 'high']:
        return "Invalid priority"
    if due_date:
        try:
            datetime.strptime(due_date, '%Y-%m-%d')
        except ValueError:
            return "Invalid date format. Use YYYY-MM-DD"
    try:
        task = Task.create_task(user_id, title, description, priority, due_date)
        return "Task added successfully"
    except Exception as e:
        return f"Error: {str(e)}"

def edit_task(task_id, title=None, description=None, priority=None, due_date=None):
    if not is_logged_in():
        return "User not logged in"
    current_user = get_current_user()
    user_id = current_user.id
    task = Task.find_by_id(task_id)
    if not task or task.user_id != user_id:
        return "Task not found or access denied"
    if priority and priority not in ['low', 'medium', 'high']:
        return "Invalid priority"
    if due_date:
        try:
            datetime.strptime(due_date, '%Y-%m-%d')
        except ValueError:
            return "Invalid date format. Use YYYY-MM-DD"
    kwargs = {k: v for k, v in [('title', title), ('description', description), ('priority', priority), ('due_date', due_date)] if v is not None}
    try:
        updated_task = Task.update_task(task_id, **kwargs)
        if updated_task:
            return "Task updated successfully"
        else:
            return "Error updating task"
    except Exception as e:
        return f"Error: {str(e)}"

def delete_task(task_id):
    if not is_logged_in():
        return "User not logged in"
    current_user = get_current_user()
    user_id = current_user.id
    task = Task.find_by_id(task_id)
    if not task or task.user_id != user_id:
        return "Task not found or access denied"
    try:
        if Task.delete_task(task_id):
            return "Task deleted successfully"
        else:
            return "Error deleting task"
    except Exception as e:
        return f"Error: {str(e)}"

def list_tasks(status=None, priority=None, sort_by='created_at', order='ASC', show_completed=False, show_pending=True, show_overdue=False, show_due_soon=False):
    if not is_logged_in():
        return "User not logged in"
    current_user = get_current_user()
    user_id = current_user.id
    tasks = Task.find_by_user_id(user_id, status=status, priority=priority, sort_by=sort_by, order=order)
    today = date.today()
    tomorrow = today + timedelta(days=1)
    filtered_tasks = []
    for task in tasks:
        include = False
        if task.status == 'completed' and show_completed:
            include = True
        elif task.status == 'pending':
            if show_pending:
                include = True
            if show_overdue and task.due_date:
                try:
                    task_date = datetime.strptime(task.due_date, '%Y-%m-%d').date()
                    if task_date < today:
                        include = True
                except ValueError:
                    pass
            if show_due_soon and task.due_date:
                try:
                    task_date = datetime.strptime(task.due_date, '%Y-%m-%d').date()
                    if task_date <= tomorrow:
                        include = True
                except ValueError:
                    pass
        if include:
            filtered_tasks.append(task)
    # Sort filtered_tasks by sort_by and order
    reverse = order.upper() == 'DESC'
    if sort_by == 'created_at':
        filtered_tasks.sort(key=lambda t: t.created_at, reverse=reverse)
    elif sort_by == 'updated_at':
        filtered_tasks.sort(key=lambda t: t.updated_at, reverse=reverse)
    elif sort_by == 'due_date':
        filtered_tasks.sort(key=lambda t: datetime.strptime(t.due_date, '%Y-%m-%d').date() if t.due_date else date.max, reverse=reverse)
    elif sort_by == 'priority':
        priority_order = {'low': 0, 'medium': 1, 'high': 2}
        filtered_tasks.sort(key=lambda t: priority_order.get(t.priority, 1), reverse=reverse)
    elif sort_by == 'status':
        status_order = {'pending': 0, 'completed': 1}
        filtered_tasks.sort(key=lambda t: status_order.get(t.status, 0), reverse=reverse)
    return filtered_tasks

def view_task(task_id):
    if not is_logged_in():
        return None
    current_user = get_current_user()
    user_id = current_user.id
    task = Task.find_by_id(task_id)
    if not task or task.user_id != user_id:
        return None
    return task

def mark_done(task_id):
    if not is_logged_in():
        return "User not logged in"
    current_user = get_current_user()
    user_id = current_user.id
    task = Task.find_by_id(task_id)
    if not task or task.user_id != user_id:
        return "Task not found or access denied"
    try:
        if Task.mark_done(task_id):
            return "Task marked as done"
        else:
            return "Error marking task as done"
    except Exception as e:
        return f"Error: {str(e)}"

def reopen(task_id):
    if not is_logged_in():
        return "User not logged in"
    current_user = get_current_user()
    user_id = current_user.id
    task = Task.find_by_id(task_id)
    if not task or task.user_id != user_id:
        return "Task not found or access denied"
    try:
        if Task.reopen(task_id):
            return "Task reopened"
        else:
            return "Error reopening task"
    except Exception as e:
        return f"Error: {str(e)}"

def get_reminders():
    if not is_logged_in():
        return "User not logged in"
    current_user = get_current_user()
    user_id = current_user.id
    tasks = Task.find_by_user_id(user_id, status='pending')
    today = date.today()
    reminders = []
    for task in tasks:
        if task.due_date:
            try:
                task_date = datetime.strptime(task.due_date, '%Y-%m-%d').date()
                if task_date <= today:
                    reminders.append(task)
            except ValueError:
                pass
    return reminders
