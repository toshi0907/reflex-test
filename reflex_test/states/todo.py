"""Todo関連のState管理"""

import reflex as rx
from reflex_test.models import DBTodoListItem


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

        if self.inputStrTitle == "":
            self.update_textErrorMessage("Title is required.")
            return

        if self.checkBoxNotifyEmail is False and self.checkBoxNotifyWebhook is False:
            self.update_textErrorMessage(
                "At least one notification method is required."
            )
            return

        if self.textHash != 0:
            with rx.session() as session:
                # 条件に一致するものを検索
                item_todos = session.exec(
                    DBTodoListItem.select().where(DBTodoListItem.id == self.textHash)
                ).all()

                for item_todo in item_todos:
                    item_todo.title = self.inputStrTitle
                    item_todo.url = self.inputStrURL
                    item_todo.datetime = self.inputdatetime
                    item_todo.repeat_daily = self.checkBoxRepeatDayly
                    item_todo.repeat_weekly = self.checkBoxRepeatWeekly
                    item_todo.repeat_monthly = self.checkBoxRepeatMonthly
                    item_todo.notify_webhook = self.checkBoxNotifyWebhook
                    item_todo.notify_email = self.checkBoxNotifyEmail
                    session.add(item_todo)

                session.commit()
        else:
            with rx.session() as session:
                new_item = DBTodoListItem(
                    hash=1,
                    create_at="2024-01-01 12:00:00",
                    update_at="2024-01-01 12:00:00",
                    title=self.inputStrTitle,
                    url=self.inputStrURL,
                    datetime=self.inputdatetime,
                    repeat_daily=self.checkBoxRepeatDayly,
                    repeat_weekly=self.checkBoxRepeatWeekly,
                    repeat_monthly=self.checkBoxRepeatMonthly,
                    notify_webhook=self.checkBoxNotifyWebhook,
                    notify_email=self.checkBoxNotifyEmail,
                )
            session.add(new_item)
            session.commit()

        self.clear_inputs()
        self.get_todo_item()

    def get_todo_item(self):
        with rx.session() as session:
            # select文で全件取得
            self.dbitems = session.exec(
                # DBTodoListItem.select().where(DBTodoListItem.done == False)
                DBTodoListItem.select()
            ).all()
            self.dbitemnum = len(self.dbitems)

    def remove_todo_item(self, item_id: str):
        print("remove_todo_item")
        with rx.session() as session:
            item_todos = session.exec(
                DBTodoListItem.select().where(DBTodoListItem.id == item_id)
            ).all()

            for item_todo in item_todos:
                item_todo.done = True
                session.add(item_todo)

            session.commit()

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
