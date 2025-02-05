# disposable.py
'''
# Sample list of known disposable email domains.
DISPOSABLE_DOMAINS = {
    "mailinator.com",
    "10minutemail.com",
    "guerrillamail.com",
    "throwawaymail.com",
    "temp-mail.org",
    "dispostable.com",
    "maildrop.cc",
    "trashmail.com",
}

def is_disposable(email):
    """
    Check if an email address belongs to a disposable email domain.

    Returns:
        bool: True if the email's domain is in the disposable domain list, False otherwise.
    """
    try:
        _, domain = email.split('@')
    except ValueError:
        return False

    return domain.lower() in DISPOSABLE_DOMAINS

'''
# disposable.py
from disposable_email_domains import blocklist

def is_disposable(email):
    """
    Checks if an email address belongs to a disposable email domain.
    
    Parameters:
        email (str): The email address to check.
    
    Returns:
        bool: True if the email's domain is in the disposable domains blocklist, False otherwise.
    """
    try:
        _, domain = email.split('@')
        return domain.lower() in blocklist
    except ValueError:
        return False  # Invalid email format.








