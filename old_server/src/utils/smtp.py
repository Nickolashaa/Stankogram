from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib

from ..config import SMTP_LOGIN, SMTP_PASSWORD, SMTP_PORT, SMTP_SERVER


async def send_email(to_email: str, subject: str, body: str):
    msg = MIMEMultipart()
    msg["From"] = SMTP_LOGIN
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "html", "utf-8"))

    await aiosmtplib.send(
        msg,
        hostname=SMTP_SERVER,
        port=SMTP_PORT,
        username=SMTP_LOGIN,
        password=SMTP_PASSWORD,
        start_tls=True,
    )
