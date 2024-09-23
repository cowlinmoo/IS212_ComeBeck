import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from backend.config.Environment import get_environment_variables

env = get_environment_variables()

class EmailService:
    def __init__(self):
        self.smtp_server = env.SMTP_SERVER
        self.smtp_port = env.SMTP_PORT
        self.sender_email = env.SENDER_EMAIL
        self.sender_password = env.SENDER_PASSWORD

    def send_email(self, recipient_email, subject, body):
        message = MIMEMultipart()
        message['From'] = self.sender_email
        message['To'] = recipient_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)
            print(f"Email sent successfully to {recipient_email}")
            return True
        except Exception as e:
            print(f"Failed to send email: {str(e)}")
            return False