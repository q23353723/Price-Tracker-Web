import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import os
from dotenv import load_dotenv

# 載入根目錄的 .env 檔案
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

# SMTP 設定（從 .env 讀取）
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

def send_email(to_email: str, subject: str, body: str):
    if not SMTP_USER or not SMTP_PASSWORD:
        print("SMTP credentials not set. Skipping email.")
        return

    msg = MIMEMultipart()
    msg['From'] = SMTP_USER
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        text = msg.as_string()
        server.sendmail(SMTP_USER, to_email, text)
        server.quit()
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")

def send_line_message(user_id: str, message: str):
    """
    使用 Line Messaging API 的 Push Message 發送訊息給指定使用者。

    Args:
        user_id: 使用者的 Line User ID（以 'U' 開頭），
                 使用者需先將 Bot 加為好友才能接收訊息。
        message: 要發送的訊息內容。
    """
    channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

    if not user_id:
        print("Line User ID not provided. Skipping Line notification.")
        return

    if not channel_access_token:
        print("LINE_CHANNEL_ACCESS_TOKEN not set in environment. Skipping Line notification.")
        return

    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {channel_access_token}"
    }
    payload = {
        "to": user_id,
        "messages": [
            {
                "type": "text",
                "text": message
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            print(f"Line message sent to user {user_id}.")
        else:
            print(f"Failed to send Line message: {response.status_code} {response.text}")
    except Exception as e:
        print(f"Error sending Line message: {e}")
