# smtp.py
import random
import string
import threading
import smtplib
import dns.resolver

# --- Sender Email Rotator ---
class SenderEmailRotator:
    def __init__(self, domain="example.com"):
        self.domain = domain
        self.current_sender = self.generate_sender_email()
        self.usage_count = 0
        self.threshold = random.randint(2, 5)
        self.lock = threading.Lock()

    def generate_sender_email(self):
        username = ''.join(random.choices(string.ascii_lowercase, k=8))
        return f"{username}@{self.domain}"

    def get_sender(self):
        with self.lock:
            self.usage_count += 1
            if self.usage_count >= self.threshold:
                self.current_sender = self.generate_sender_email()
                self.usage_count = 0
                self.threshold = random.randint(2, 5)
            return self.current_sender

# Global instance of the sender rotator.
sender_rotator = SenderEmailRotator()

def check_email(email, ports=[25, 587, 465], use_tls=False):
    """
    Verify an email address by performing an SMTP handshake over a list of ports.

    Parameters:
        email (str): The email address to verify.
        ports (list): A list of SMTP ports to try (default: [25, 587, 465]).
        use_tls (bool): Whether to force a TLS upgrade on non-465 ports (default: False).
                        Note: Port 587 typically requires TLS.

    Returns:
        tuple: (email, status) where status is "valid" if any port returns a 250 acceptance
               code for the RCPT command, otherwise "invalid".
    """
    # Extract the domain from the email address.
    try:
        local_part, domain = email.split('@')
    except ValueError:
        return (email, "invalid")  # Incorrect email format.

    # Get the MX record for the domain.
    try:
        answers = dns.resolver.resolve(domain, 'MX')
        records = sorted(answers, key=lambda r: r.preference)
        mx_record = str(records[0].exchange).rstrip('.')  # Remove any trailing dot.
    except Exception:
        return (email, "invalid")  # Unable to retrieve MX records.

    # Get a sender email from the rotator.
    sender = sender_rotator.get_sender()

    # Try connecting on each provided port.
    for port in ports:
        try:
            if port == 465:
                # Port 465 expects an SSL connection.
                server = smtplib.SMTP_SSL(mx_record, port, timeout=10)
            else:
                server = smtplib.SMTP(timeout=10)
                server.connect(mx_record, port)
                # For port 587 (submission) TLS is generally required.
                if use_tls or port == 587:
                    server.starttls()
            server.helo(server.local_hostname)
            server.mail(sender)
            code, message = server.rcpt(email)
            server.quit()

            # A 250 response generally means the recipient is accepted.
            if code == 250:
                return (email, "valid")
        except Exception:
            # On any connection or protocol error, try the next port.
            continue

    return (email, "invalid")

# smtp.py
import random
import string
import threading
import smtplib
import dns.resolver

# --- Sender Email Rotator ---
class SenderEmailRotator:
    def __init__(self, domain="example.com"):
        self.domain = domain
        self.current_sender = self.generate_sender_email()
        self.usage_count = 0
        self.threshold = random.randint(2, 5)
        self.lock = threading.Lock()

    def generate_sender_email(self):
        username = ''.join(random.choices(string.ascii_lowercase, k=8))
        return f"{username}@{self.domain}"

    def get_sender(self):
        with self.lock:
            self.usage_count += 1
            if self.usage_count >= self.threshold:
                self.current_sender = self.generate_sender_email()
                self.usage_count = 0
                self.threshold = random.randint(2, 5)
            return self.current_sender

# Global instance of the sender rotator.
sender_rotator = SenderEmailRotator()

def check_email(email, ports=[25, 587, 465], use_tls=False):
    """
    Verify an email address by performing an SMTP handshake over a list of ports.

    Parameters:
        email (str): The email address to verify.
        ports (list): A list of SMTP ports to try (default: [25, 587, 465]).
        use_tls (bool): Whether to force a TLS upgrade on non-465 ports (default: False).
                        Note: Port 587 typically requires TLS.

    Returns:
        tuple: (email, status) where status is "valid" if any port returns a 250 acceptance
               code for the RCPT command, otherwise "invalid".
    """
    # Extract the domain from the email address.
    try:
        local_part, domain = email.split('@')
    except ValueError:
        return (email, "invalid")  # Incorrect email format.

    # Get the MX record for the domain.
    try:
        answers = dns.resolver.resolve(domain, 'MX')
        records = sorted(answers, key=lambda r: r.preference)
        mx_record = str(records[0].exchange).rstrip('.')  # Remove any trailing dot.
    except Exception:
        return (email, "invalid")  # Unable to retrieve MX records.

    # Get a sender email from the rotator.
    sender = sender_rotator.get_sender()

    # Try connecting on each provided port.
    for port in ports:
        try:
            if port == 465:
                # Port 465 expects an SSL connection.
                server = smtplib.SMTP_SSL(mx_record, port, timeout=10)
            else:
                server = smtplib.SMTP(timeout=10)
                server.connect(mx_record, port)
                # For port 587 (submission) TLS is generally required.
                if use_tls or port == 587:
                    server.starttls()
            server.helo(server.local_hostname)
            server.mail(sender)
            code, message = server.rcpt(email)
            server.quit()

            # A 250 response generally means the recipient is accepted.
            if code == 250:
                return (email, "valid")
        except Exception:
            # On any connection or protocol error, try the next port.
            continue

    return (email, "invalid")
'''
# Optional self-test.
if __name__ == '__main__':
    test_email = "dangwalabhishek5@gmail.com"
    result = check_email(test_email)
    print(f"{result[0]} is {result[1]}")

'''