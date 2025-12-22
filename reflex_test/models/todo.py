"""Todo関連のデータベースモデル"""

import reflex as rx


class DBTodoListItem(rx.Model, table=True):
    """データベースのテーブル定義"""

    hash: int
    create_at: str
    update_at: str
    title: str
    url: str
    datetime: str

    repeat_daily: bool
    repeat_weekly: bool
    repeat_monthly: bool

    notify_webhook: bool
    notify_email: bool

    done: bool = False
