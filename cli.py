import argparse
import getpass
from .controllers.auth import signup, login, logout, is_logged_in
from .controllers.tasks import add_task, edit_task, delete_task, list_tasks, view_task, mark_done, reopen, get_reminders
from .utils.formatter import format_task, format_task_list
from .utils.notifications import check_reminders, display_notifications
from .utils.logger import setup_logger, get_logger

def create_parser():
    parser = argparse.ArgumentParser(description="Todo App CLI")
    parser.add_argument('--verbose', action='store_true', help='Enable verbose logging')

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # signup
    parser_signup = subparsers.add_parser('signup', help='Sign up a new user')
    parser_signup.add_argument('username', help='Username for signup')

    # login
    parser_login = subparsers.add_parser('login', help='Log in to the app')
    parser_login.add_argument('username', help='Username for login')

    # logout
    subparsers.add_parser('logout', help='Log out from the app')

    # add
    parser_add = subparsers.add_parser('add', help='Add a new task')
    parser_add.add_argument('title', help='Task title')
    parser_add.add_argument('--desc', help='Task description')
    parser_add.add_argument('--priority', choices=['low', 'medium', 'high'], default='medium', help='Task priority')
    parser_add.add_argument('--due', help='Due date in YYYY-MM-DD format')

    # edit
    parser_edit = subparsers.add_parser('edit', help='Edit an existing task')
    parser_edit.add_argument('id', type=int, help='Task ID')
    parser_edit.add_argument('--title', help='New title')
    parser_edit.add_argument('--desc', help='New description')
    parser_edit.add_argument('--priority', choices=['low', 'medium', 'high'], help='New priority')
    parser_edit.add_argument('--due', help='New due date in YYYY-MM-DD format')

    # delete
    parser_delete = subparsers.add_parser('delete', help='Delete a task')
    parser_delete.add_argument('id', type=int, help='Task ID')

    # view
    parser_view = subparsers.add_parser('view', help='View a task')
    parser_view.add_argument('id', type=int, help='Task ID')

    # list
    parser_list = subparsers.add_parser('list', help='List tasks')
    parser_list.add_argument('--completed', action='store_true', help='Show completed tasks')
    parser_list.add_argument('--pending', action='store_true', help='Show pending tasks')
    parser_list.add_argument('--priority', choices=['low', 'medium', 'high'], help='Filter by priority')
    parser_list.add_argument('--sort-by', choices=['created_at', 'updated_at', 'due_date', 'priority', 'status'], default='created_at', help='Sort by field')
    parser_list.add_argument('--order', choices=['ASC', 'DESC'], default='ASC', help='Sort order')
    parser_list.add_argument('--overdue', action='store_true', help='Show overdue tasks')
    parser_list.add_argument('--due-soon', action='store_true', help='Show tasks due soon')

    # done
    parser_done = subparsers.add_parser('done', help='Mark a task as done')
    parser_done.add_argument('id', type=int, help='Task ID')

    # reopen
    parser_reopen = subparsers.add_parser('reopen', help='Reopen a completed task')
    parser_reopen.add_argument('id', type=int, help='Task ID')

    # whoami
    subparsers.add_parser('whoami', help='Show current logged-in user')

    return parser

def handle_command(args):
    setup_logger(args.verbose)
    log = get_logger()

    try:
        if args.command == 'signup':
            username = args.username
            password = getpass.getpass('Password: ')
            result = signup(username, password)
            if result:
                print("Signup successful")
            else:
                print("Signup failed")
                if args.verbose:
                    log.error("Signup failed")

        elif args.command == 'login':
            username = args.username
            password = getpass.getpass('Password: ')
            if login(username, password):
                print("Login successful")
            else:
                print("Login failed")
                if args.verbose:
                    log.error("Login failed")

        elif args.command == 'logout':
            logout()
            print("Logged out")

        elif args.command == 'whoami':
            user = get_current_user()
            if user:
                print(f"Logged in as: {user.username}")
            else:
                print("Not logged in")

        else:
            # Commands that require login
            if not is_logged_in():
                print("Please login first")
                return

            # Get and display reminders
            reminders = get_reminders()
            if reminders:
                notifs = check_reminders(reminders)
                display_notifications(notifs)

            if args.command == 'add':
                result = add_task(args.title, args.desc, args.priority, args.due)
                print(result)

            elif args.command == 'edit':
                result = edit_task(args.id, title=args.title, description=args.desc, priority=args.priority, due_date=args.due)
                print(result)

            elif args.command == 'delete':
                result = delete_task(args.id)
                print(result)

            elif args.command == 'view':
                task = view_task(args.id)
                if task:
                    print(format_task(task))
                else:
                    print("Task not found")

            elif args.command == 'list':
                # Determine filters
                show_completed = args.completed
                show_pending = args.pending
                show_overdue = args.overdue
                show_due_soon = args.due_soon
                if not (show_completed or show_pending or show_overdue or show_due_soon):
                    show_pending = True  # Default to show pending tasks

                tasks_list = list_tasks(
                    status=None,  # Get all, filter in function
                    priority=args.priority,
                    sort_by=args.sort_by,
                    order=args.order,
                    show_completed=show_completed,
                    show_pending=show_pending,
                    show_overdue=show_overdue,
                    show_due_soon=show_due_soon
                )
                if tasks_list:
                    print(format_task_list(tasks_list))
                else:
                    print("No tasks found.")

            elif args.command == 'done':
                result = mark_done(args.id)
                print(result)

            elif args.command == 'reopen':
                result = reopen(args.id)
                print(result)

    except Exception as e:
        print(f"An error occurred: {e}")
        if args.verbose:
            log.error(f"An error occurred: {e}")
