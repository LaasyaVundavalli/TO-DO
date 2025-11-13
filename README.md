# Todo CLI Application

A Windows-only Python CLI application for managing personal task lists with multi-user support, using SQLite for storage and git-style subcommands.

## Features

- **Multi-user authentication**: Sign up, login, logout with hashed passwords
- **Task management**: Add, edit, delete, view, list tasks with priorities and due dates
- **Reminders**: Terminal notifications for overdue and due-today tasks
- **Filtering & Sorting**: List tasks by status, priority, due date, etc.
- **Colored output**: Human-friendly formatting with colors for task statuses
- **Persistent storage**: SQLite database (todo.db)
- **Logging**: Error logging to app.log with optional verbose mode

## Installation

1. Ensure Python 3.10+ is installed
2. Install dependencies:
   ```
   pip install bcrypt colorama
   ```
3. Clone or download the project files

## Usage

Run the application from the command line:

```
python main.py <command> [options]
```

### Global Options

- `--verbose`: Enable debug logging

### Authentication Commands

#### Sign Up
```
python main.py signup
```
Prompts for username and password to create a new account.

#### Login
```
python main.py login
```
Prompts for username and password to log in.

#### Logout
```
python main.py logout
```
Logs out the current user.

### Task Commands

All task commands require login.

#### Add Task
```
python main.py add "Task Title" --desc "Description" --priority high --due 2025-11-20
```
- `--desc`: Optional description
- `--priority`: low/medium/high (default: medium)
- `--due`: Due date in YYYY-MM-DD format

#### Edit Task
```
python main.py edit <task_id> --title "New Title" --priority low --due 2025-11-21
```
Update any combination of title, description, priority, due date.

#### Delete Task
```
python main.py delete <task_id>
```

#### Mark as Done
```
python main.py done <task_id>
```

#### Reopen Task
```
python main.py reopen <task_id>
```

#### View Task
```
python main.py view <task_id>
```
Shows full task details in expanded format.

#### List Tasks
```
python main.py list [options]
```
Options:
- `--completed`: Show only completed tasks
- `--pending`: Show only pending tasks
- `--overdue`: Show only overdue tasks
- `--due-soon`: Show tasks due today or tomorrow
- `--priority low|medium|high`: Filter by priority
- `--sort-by created_at|updated_at|due_date|priority|status`: Sort field (default: created_at)
- `--order ASC|DESC`: Sort order (default: ASC)

Examples:
```
python main.py list --pending --overdue
python main.py list --priority high --sort-by due_date
```

### Reminders

When running any command after login, the app automatically displays:
- 🔔 Overdue tasks (red)
- 🔔 Tasks due today (blue)

### Output Colors

- Pending tasks: Yellow
- Completed tasks: Green
- Overdue tasks: Red
- Due today: Blue

### Examples

1. Create account and add first task:
   ```
   python main.py signup
   python main.py login
   python main.py add "Finish project" --desc "Complete before deadline" --priority high --due 2025-11-20
   ```

2. List pending tasks:
   ```
   python main.py list --pending
   ```

3. Mark task as done:
   ```
   python main.py done 1
   ```

4. View task details:
   ```
   python main.py view 1
   ```

## Database

- SQLite file: `todo.db` (created automatically)
- Tables: `users`, `tasks`
- Data persists between sessions

## Logging

- Errors logged to `app.log`
- Use `--verbose` for debug information

## Testing

Run unit tests:
```
python -m unittest discover tests
```

## Requirements

- Python 3.10+
- Windows OS
- Dependencies: bcrypt, colorama

## Project Structure

```
todo_app/
├── main.py              # Entry point
├── cli.py               # CLI framework
├── controllers/
│   ├── auth.py          # Authentication logic
│   └── tasks.py         # Task management logic
├── database/
│   ├── db.py            # Database connection
│   └── migrations.sql   # Schema creation
├── models/
│   ├── user_model.py    # User data model
│   └── task_model.py    # Task data model
├── utils/
│   ├── validation.py    # Input validation
│   ├── notifications.py # Reminder logic
│   ├── formatter.py     # Output formatting
│   └── logger.py        # Logging setup
├── tests/
│   ├── test_auth.py     # Auth tests
│   ├── test_tasks.py    # Task tests
│   └── test_reminders.py # Reminder tests
├── todo.db              # SQLite database
├── app.log              # Log file
└── README.md            # This file