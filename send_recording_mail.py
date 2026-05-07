import os
import smtplib
from pathlib import Path
from email.message import EmailMessage
from datetime import datetime
from dotenv import load_dotenv

RECORDINGS_DIR = Path("recordings")


def get_required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def find_latest_mp3() -> Path:
    files = list(RECORDINGS_DIR.glob("*.mp3"))

    if not files:
        raise FileNotFoundError(f"No mp3 files found in {RECORDINGS_DIR}")

    return max(files, key=lambda p: p.stat().st_mtime)


def send_mail_with_attachment(file_path: Path):
    load_dotenv()

    smtp_host = get_required_env("SMTP_HOST")
    smtp_port = int(get_required_env("SMTP_PORT"))
    smtp_user = get_required_env("SMTP_USER")
    smtp_password = get_required_env("SMTP_PASSWORD")
    mail_from = get_required_env("MAIL_FROM")
    mail_to = get_required_env("MAIL_TO")

    today = datetime.now().strftime("%Y-%m-%d")

    msg = EmailMessage()
    msg["Subject"] = f"EBS 라디오 녹음 파일 - {today}"
    msg["From"] = mail_from
    msg["To"] = mail_to
    msg.set_content(
        f"{today} EBS 라디오 녹음 파일입니다.\n\n"
        f"첨부 파일: {file_path.name}"
    )

    with open(file_path, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="audio",
            subtype="mpeg",
            filename=file_path.name,
        )

    with smtplib.SMTP_SSL(smtp_host, smtp_port) as smtp:
        smtp.login(smtp_user, smtp_password)
        smtp.send_message(msg)

    print(f"Mail sent successfully: {file_path.name}")


def main():
    latest_file = find_latest_mp3()
    print(f"Latest recording found: {latest_file}")
    send_mail_with_attachment(latest_file)


if __name__ == "__main__":
    main()
