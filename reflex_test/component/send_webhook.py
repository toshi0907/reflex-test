import requests
import os
from dotenv import load_dotenv
from reflex_test.component.tn_base_class import BaseNotify

# --- 設定項目 ---
load_dotenv()


class SendWebhook(BaseNotify):
    _webhook_url = os.getenv("WEBHOOK_URL")

    def send_notification(self, title: str, url: str, message: str) -> None:
        self.send_webhook(title, url, message)

    def send_webhook(self, title: str, url: str, message: str):
        _params = {
            "title": title,
            "url": url,
            "message": message,
        }

        try:
            response = requests.post(self._webhook_url, params=_params)
            response.raise_for_status()
            print("SendWebhook.send_webhook: Webhook送信完了")
        except requests.exceptions.RequestException as e:
            print(f"SendWebhook.send_webhook: Webhook送信失敗 : {e}")
