import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# --- 設定項目 ---
load_dotenv()

gmail_user = os.getenv("GMAIL_USER")
gmail_password = os.getenv("GMAIL_PASSWORD")

to_email = os.getenv("GMAIL_TO")
subject = "Pythonからのテストメール"
body = "こんにちは！これはPythonから送信されたメールです。"

# --- メールの作成 ---
msg = MIMEMultipart()
msg["From"] = gmail_user
msg["To"] = to_email
msg["Subject"] = subject
msg.attach(MIMEText(body, "plain"))

try:
    # --- SMTPサーバへの接続と送信 ---
    # GmailのSMTPサーバ: smtp.gmail.com / ポート番号: 587
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()  # セキュリティ(TLS)の開始
    server.login(gmail_user, gmail_password)
    
    server.send_message(msg)
    server.close()
    
    print("メールの送信に成功しました！")

except Exception as e:
    print(f"エラーが発生しました: {e}")