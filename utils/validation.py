from datetime import datetime

def validate_date(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return None

def validate_priority(priority):
    return priority.lower() in ['low', 'medium', 'high']

def validate_status(status):
    return status.lower() in ['pending', 'completed']
