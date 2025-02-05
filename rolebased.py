# rolebased.py
def is_role_based(email):
    """
    Check if an email address is role-based (e.g., info, support, admin).

    Returns:
        bool: True if the local part is one of the common role names, False otherwise.
    """
    try:
        local_part, _ = email.split('@')
    except ValueError:
        return False

    # Common role-based prefixes.
    role_names = {
        'admin', 'support', 'info', 'sales', 'contact', 'help', 'marketing', 'service', 'office', 'billing'
    }
    return local_part.lower() in role_names


