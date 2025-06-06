import re

def validate_email(email):
    """
    Validate email format
    Returns True if valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_name(name):
    """
    Validate name (first name or last name)
    Returns True if valid, False otherwise
    """
    # Name should be at least 2 characters and contain only letters
    return bool(name) and len(name) >= 2 and name.replace(' ', '').replace('-', '').isalpha()

def validate_group_name(group_name):
    """
    Validate group name
    Returns True if valid, False otherwise
    """
    # Group name should be at least 2 characters
    return bool(group_name) and len(group_name) >= 2

def validate_grade(grade):
    """
    Validate grade (should be between 1 and 5)
    Returns True if valid, False otherwise
    """
    try:
        grade_value = int(grade)
        return 1 <= grade_value <= 5
    except (ValueError, TypeError):
        return False

def validate_date_format(date_str):
    """
    Validate date format (YYYY-MM-DD)
    Returns True if valid, False otherwise
    """
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    return bool(re.match(pattern, date_str))