# fformat_checker.py
from email_validator import validate_email, EmailNotValidError

def check_format(email):
    """
    Validate an email address using the email_validator package.

    Returns:
        tuple: (is_valid, message)
            - is_valid (bool): True if the email format is valid.
            - message (str): Normalized email if valid, or error message if invalid.
    """
    try:
        result = validate_email(email)
        # result["email"] contains the normalized email.
        return (True, result["email"])
    except EmailNotValidError as e:
        return (False, str(e))

if __name__ == '__main__':
    test_emails = ["plainaddress", "missingatsign.com", "email@example.com"]
    for email in test_emails:
        valid, message = check_format(email)
        print(f"{email}: Valid? {valid}. {message}")
