import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os

class EmailNotifier:
    def __init__(self, service, email, password):
        if service == 'gmail':
            self.smtp_server = 'smtp.gmail.com'
            self.smtp_port = 465
        elif service == 'outlook':
            self.smtp_server = 'smtp-mail.outlook.com'
            self.smtp_port = 587
        else:
            raise ValueError("Unsupported email service")
        
        self.email = email
        self.password = password

    def send_email(self, recipient, subject, message):
        msg = MIMEMultipart()
        msg['From'] = self.email
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        try:
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
                server.login(self.email, self.password)
                server.sendmail(self.email, recipient, msg.as_string())
            print("Email sent successfully")
        except Exception as e:
            print(f"Failed to send email: {e}")

    def send_email_with_attachment(self, recipient, subject, message, attachment_path):
        msg = MIMEMultipart()
        msg['From'] = self.email
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        with open(attachment_path, "rb") as attachment:
            part = MIMEApplication(attachment.read(), Name=os.path.basename(attachment_path))
            part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_path)}"'
            msg.attach(part)

        try:
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
                server.login(self.email, self.password)
                server.sendmail(self.email, recipient, msg.as_string())
            print("Email with attachment sent successfully")
        except Exception as e:
            print(f"Failed to send email with attachment: {e}")