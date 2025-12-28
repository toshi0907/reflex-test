"""Todo関連のState管理"""

import reflex as rx
from reflex_test.models import DBTodoListItem
from reflex_test.services.todo import (
    get_todo_items as service_get_todo_items,
    add_todo_item as service_add_todo_item,
    remove_todo_item as service_remove_todo_item,
)


class StateTodo(rx.State):
    """TodoページのState定義"""

    textHash: int = 0

    inputStrTitle: str = ""
    inputStrURL: str = ""
    inputdatetime: str = ""  # 形式:2025-12-21T12:33
    checkBoxRepeatDayly: bool = False
    checkBoxRepeatWeekly: bool = False
    checkBoxRepeatMonthly: bool = False

    checkBoxNotifyWebhook: bool = False
    checkBoxNotifyEmail: bool = False

    dbitems: list[DBTodoListItem] = []
    dbitemnum: int = 0

    textErrorMessage: str = ""
    isErrorMessageVisible: bool = False

    def init_page(self):
        print("StateTodo init_page")
        self.get_todo_item()

    def update_inputStrTitle(self, value: str):
        print(f"update_inputStrTitle : {value}")
        self.inputStrTitle = value

    def update_inputStrURL(self, value: str):
        print(f"update_inputStrURL : {value}")
        self.inputStrURL = value

    def update_inputdatetime(self, value: str):
        print(f"update_inputdatetime : {value}")
        self.inputdatetime = value

    def update_checkBoxRepeatDayly(self, value: bool):
        print(f"update_checkBoxRepeatDayly : {value}")
        self.checkBoxRepeatDayly = value

    def update_checkBoxRepeatWeekly(self, value: bool):
        print(f"update_checkBoxRepeatWeekly : {value}")
        self.checkBoxRepeatWeekly = value

    def update_checkBoxRepeatMonthly(self, value: bool):
        print(f"update_checkBoxRepeatMonthly : {value}")
        self.checkBoxRepeatMonthly = value

    def update_checkBoxNotifyWebhook(self, value: bool):
        print(f"update_checkBoxNotifyWebhook : {value}")
        self.checkBoxNotifyWebhook = value

    def update_checkBoxNotifyEmail(self, value: bool):
        print(f"update_checkBoxNotifyEmail : {value}")
        self.checkBoxNotifyEmail = value

    def update_textErrorMessage(self, value: str):
        print(f"update_textErrorMessage : {value}")
        self.textErrorMessage = value
        self.isErrorMessageVisible = True

    def add_todo_item(self):
        print("add_todo_item")

        # Service層の関数を呼び出す
        success, error_message = service_add_todo_item(
            text_hash=self.textHash,
            title=self.inputStrTitle,
            url=self.inputStrURL,
            datetime_str=self.inputdatetime,
            repeat_daily=self.checkBoxRepeatDayly,
            repeat_weekly=self.checkBoxRepeatWeekly,
            repeat_monthly=self.checkBoxRepeatMonthly,
            notify_webhook=self.checkBoxNotifyWebhook,
            notify_email=self.checkBoxNotifyEmail,
        )

        if not success:
            self.update_textErrorMessage(error_message)
            return

        self.clear_inputs()
        self.get_todo_item()

    def get_todo_item(self):
        self.dbitems, self.dbitemnum = service_get_todo_items()

    def remove_todo_item(self, item_id: str):
        print("remove_todo_item")
        success, error_message = service_remove_todo_item(item_id)

        if not success:
            self.update_textErrorMessage(error_message)
            return

        self.get_todo_item()

    def update_item(self, item: DBTodoListItem):
        print("update_item")
        self.textHash = item.id
        self.inputStrTitle = item.title
        self.inputStrURL = item.url
        self.inputdatetime = item.datetime
        self.checkBoxRepeatDayly = item.repeat_daily
        self.checkBoxRepeatWeekly = item.repeat_weekly
        self.checkBoxRepeatMonthly = item.repeat_monthly
        self.checkBoxNotifyWebhook = item.notify_webhook
        self.checkBoxNotifyEmail = item.notify_email

    def clear_inputs(self):
        self.textHash = 0
        self.inputStrTitle = ""
        self.inputStrURL = ""
        self.inputdatetime = ""
        self.checkBoxRepeatDayly = False
        self.checkBoxRepeatWeekly = False
        self.checkBoxRepeatMonthly = False
        self.checkBoxNotifyWebhook = False
        self.checkBoxNotifyEmail = False
        self.isErrorMessageVisible = False
        self.textErrorMessage = ""
