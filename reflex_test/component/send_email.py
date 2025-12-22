import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

import tn_base_class

# --- 設定項目 ---
load_dotenv()


class SendEmail(tn_base_class.BaseNotify):
    gmail_user = os.getenv("GMAIL_USER")
    gmail_password = os.getenv("GMAIL_PASSWORD")
    to_email = os.getenv("GMAIL_TO")

    def send_notification(self, title: str, url: str, message: str) -> None:
        self.send_email(title, url, message)

    def send_email(self, title: str, url: str, message: str):
        # --- メールの作成 ---
        msg = MIMEMultipart()
        msg["From"] = self.gmail_user
        msg["To"] = self.to_email
        msg["Subject"] = title
        msg.attach(MIMEText(f"URL: {url}\n\nMESSAGE: {message}", "plain"))

        try:
            # --- SMTPサーバへの接続と送信 ---
            # GmailのSMTPサーバ: smtp.gmail.com / ポート番号: 587
            server = smtplib.SMTP("smtp.gmail.com", 587)
            # セキュリティ(TLS)の開始
            server.starttls()
            # ログイン
            server.login(self.gmail_user, self.gmail_password)
            # メールの送信
            server.send_message(msg)
            # サーバの終了
            server.close()

            print("SendEmail.send_email: メール送信完了")

        except Exception as e:
            print(f"SendEmail.send_email: メール送信失敗 : {e}")
