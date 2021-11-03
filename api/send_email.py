import smtplib
import ssl

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import dotenv_values

from path_resolver import get_full_path

CONFIG = dotenv_values(get_full_path(__file__, ".env.secret"))

def send_email(recepient):
    message = MIMEMultipart("alternative")
    message["Subject"] = "Testing HTML"
    message["From"] = CONFIG["CRON_EMAIL"]
    message["To"] = recepient
    text = "Plain Text Message Test"
    html="""
    <html>
        <body>
            <p>HTML Message Test</p>
        </body>
    </html>
    """
    message.attach(MIMEText(text, "plain"))
    message.attach(MIMEText(html, "html"))
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(
        "smtp.gmail.com", CONFIG["SSL_PORT"], context=context) as server:
        server.login(CONFIG["CRON_EMAIL"], CONFIG["CRON_PASSWORD"])
        server.sendmail(CONFIG["CRON_EMAIL"], recepient, message.as_string())