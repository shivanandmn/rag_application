from email.message import EmailMessage
import smtplib

import ssl
from email.utils import formataddr
from dotenv import load_dotenv, find_dotenv
import os

_ = load_dotenv(find_dotenv())

SMTP_CONFIG = {
    "outlook.com": {
        "SMTP_SERVER": "smtp-mail.outlook.com",
        "PORT": 587,
        "is_need_ssl_encryption": True,
    },
    "gmail.com": {
        "SMTP_SERVER": "smtp.gmail.com",
        "PORT": 465,
        "is_need_ssl_encryption": False,
    },
}


def send_email(service):
    service_provider = service["sender_email"].split("@")[1]
    if service_provider not in SMTP_CONFIG:
        raise Exception("Invalid email provider")
    service.update(SMTP_CONFIG[service_provider])
    msg = EmailMessage()
    msg["Subject"] = service["Subject"]
    msg["From"] = formataddr(
        (str(service["sender_name"]), str(service["sender_email"]))
    )
    msg["To"] = service["To"]
    msg.set_content(service["body"], subtype=service.get("body_subtype", "plain"))
    # msg.add_alternative(service["body"], subtype="html")
    if service["is_need_ssl_encryption"]:
        with smtplib.SMTP(service["SMTP_SERVER"], service["PORT"]) as server:
            server.ehlo("lowercasehost")
            server.starttls()
            server.ehlo("lowercasehost")
            server.login(service["sender_email"], os.getenv("EMAIL_PASSWORD"))
            server.send_message(msg)
    else:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(
            service["SMTP_SERVER"], service["PORT"], context=context
        ) as server:
            server.login(service["sender_email"], os.getenv("EMAIL_PASSWORD"))
            server.send_message(msg)

    return True


if __name__ == "__main__":
    service = {}

    # sender config
    service["sender_email"] = "shivanand.jnv@gmail.com"
    service["sender_name"] = "Shivanand"

    # send config
    service["To"] = "ticifi6817@newcupon.com"
    service["Subject"] = "subject"
    service["body"] = """This message is sent from Python."""
    service["body_subtype"] = "plain"

    import json

    print(json.dumps(service, indent=4))
    res = send_email(service)
    print(f"{res}:Email sent successfully")
