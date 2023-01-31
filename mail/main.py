# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_email_sendgrid(subject, content, recipient):
    print("recipient: ", recipient)
    message = Mail(
        from_email='e.murairi@alustudent.com',
        to_emails=recipient,
        subject=subject,
        html_content=content)

    try:
        API_KEY=os.environ.get('SENDGRID_API_KEY')
        sg = SendGridAPIClient(API_KEY)
        response = sg.send(message)

    except Exception as e:
        print(e.message)

