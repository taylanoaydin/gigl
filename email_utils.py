from flask_mail import Message
from flask import current_app
from gigl import mail  # Importing the initialized 'mail' from gigl.py
import sys

def send_email(to_email, subject, body):
    print("send_email called successfully", file=sys.stderr)
    msg = Message(subject,
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[to_email],
                  body=body)
    try:
        with current_app.app_context():
            mail.send(msg)
    except Exception as e:
        print(str(e))
        sys.exit(1)
    return True
