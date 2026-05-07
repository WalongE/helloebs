import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv


def get_required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def send_test_mail():
    load_dotenv()

    smtp_host = get_required_env("SMTP_HOST")
    smtp_port = int(get_required_env("SMTP_PORT"))
    smtp_user = get_required_env("SMTP_USER")
    smtp_password = get_required_env("SMTP_PASSWORD")
    mail_from = get_required_env("MAIL_FROM")
    mail_to = get_required_env("MAIL_TO")

    msg = EmailMessage()
    msg["Subject"] = "helloebs 메일 발송 테스트"
    msg["From"] = mail_from
    msg["To"] = mail_to
    msg.set_content("helloebs 서버에서 보낸 테스트 메일입니다.")

    with smtplib.SMTP_SSL(smtp_host, smtp_port) as smtp:
        smtp.login(smtp_user, smtp_password)
        smtp.send_message(msg)

    print("메일 발송 완료")


if __name__ == "__main__":
    send_test_mail()
