from abc import ABC, abstractmethod


class BaseNotify:
    """通知のBaseクラス"""

    @abstractmethod
    def send_notification(self, title: str, url: str, message: str) -> None:
        pass
