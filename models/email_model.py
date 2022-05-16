import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from g import EMAIL_PASSWORD as password

class Email:
    email_password = password

    def __init__(self, sender, reciever, subject, content_text = None, content_html = None):
        self.sender_email = sender
        self.receiver_email = reciever
        self.subject_line = subject
        self.content_text = content_text
        self.content_html = content_html

    def send_email(self):
        message = MIMEMultipart("alternative")
        message["Subject"] = self.subject_line
        message["From"] = self.sender_email
        message["To"] = self.receiver_email
        
        # Turn message into plain/html MIMEText objects
        part1 = MIMEText(self.content_text, "plain")
        part2 = MIMEText(self.content_html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)
        message.attach(part2)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            try:
                server.login(self.sender_email, self.email_password)
                server.sendmail(self.sender_email, self.receiver_email, message.as_string())
                print("sent")
                return "yes, email sent"
            except Exception as ex:
                print("ex")
                print(ex)
                return "uppps... could not send the email"