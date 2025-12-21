"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from rxconfig import config


### Common Item ###


def CommonHeader(title: str) -> rx.Component:
    """共通ヘッダ"""
    title_disp = ""
    if title == "":
        title_disp = "TN App"
    else:
        title_disp = "TN App : " + title
    return rx.vstack(
        rx.heading(title_disp),
        rx.hstack(
            rx.link("TopPage", href="/"),
            rx.link("TodoPage", href="/todo_page"),
        ),
        rx.divider(),
    )


### For Top Page ###


def index() -> rx.Component:
    # indexページ
    return rx.container(
        CommonHeader(title=""),
    )


### For Todo Page ###


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


class StateTodo(rx.State):
    """TodoページのState定義"""

    textHash: str = ""

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

        if self.textHash != "":
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
            self.dbitems = session.exec(DBTodoListItem.select()).all()
            self.dbitemnum = len(self.dbitems)

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
        self.textHash = ""
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


def todo_page_regist_item() -> rx.Component:
    return (
        rx.vstack(
            rx.heading("Add Item", as_="h2"),
            rx.vstack(
                rx.text(f"ID {StateTodo.textHash}"),
                rx.input(
                    value=StateTodo.inputStrTitle,
                    on_change=StateTodo.update_inputStrTitle,
                    placeholder="Enter Item Title",
                    width="100%",
                    minwidth="300px",
                ),
                rx.input(
                    value=StateTodo.inputStrURL,
                    on_change=StateTodo.update_inputStrURL,
                    placeholder="Enter URL",
                    width="100%",
                    minwidth="300px",
                ),
                rx.input(
                    value=StateTodo.inputdatetime,
                    on_change=StateTodo.update_inputdatetime,
                    placeholder="Select Date and Time",
                    type="datetime-local",
                ),
                rx.hstack(
                    rx.text("Notify", width="100px", margin_left="20px"),
                    rx.checkbox(
                        "Webhook",
                        checked=StateTodo.checkBoxNotifyWebhook,
                        on_change=StateTodo.update_checkBoxNotifyWebhook,
                    ),
                    rx.checkbox(
                        "Email",
                        checked=StateTodo.checkBoxNotifyEmail,
                        on_change=StateTodo.update_checkBoxNotifyEmail,
                    ),
                    rx.text("Repeat", width="100px", margin_left="20px"),
                    rx.checkbox(
                        "Daily",
                        checked=StateTodo.checkBoxRepeatDayly,
                        on_change=StateTodo.update_checkBoxRepeatDayly,
                    ),
                    rx.checkbox(
                        "Weekly",
                        checked=StateTodo.checkBoxRepeatWeekly,
                        on_change=StateTodo.update_checkBoxRepeatWeekly,
                    ),
                    rx.checkbox(
                        "Monthly",
                        checked=StateTodo.checkBoxRepeatMonthly,
                        on_change=StateTodo.update_checkBoxRepeatMonthly,
                    ),
                ),
                rx.hstack(
                    rx.button(
                        "Clear",
                        on_click=lambda: StateTodo.clear_inputs(),
                        width="30%",
                    ),
                    rx.button(
                        "Add Item",
                        on_click=lambda: StateTodo.add_todo_item(),
                        width="30%",
                    ),
                    rx.button(
                        "Get Item",
                        on_click=lambda: StateTodo.get_todo_item(),
                        width="30%",
                    ),
                    width="100%",
                ),
                rx.cond(
                    StateTodo.isErrorMessageVisible,
                    rx.text(StateTodo.textErrorMessage, status="error"),
                ),
                minwidth="300px",
                width="100%",
            ),
        ),
    )


def todo_page_view_items() -> rx.Component:
    return rx.vstack(
        rx.heading("Todo Items", as_="h2"),
        rx.text(f"{StateTodo.dbitemnum}" + " items found."),
        rx.foreach(
            StateTodo.dbitems,
            lambda item: rx.vstack(
                rx.hstack(
                    rx.button(
                        "Edit",
                        on_click=lambda: StateTodo.update_item(item),
                    ),
                    rx.text(f"Title: {item.title}"),
                ),
                rx.text(f"URL: {item.url}"),
                rx.text(
                    f"Daily: {item.repeat_daily} / Weekly: {item.repeat_weekly} / Monthly: {item.repeat_monthly}"
                ),
                rx.text(f"Webhook: {item.notify_webhook} / Email: {item.notify_email}"),
                rx.text(f"Datetime: {item.datetime}"),
            ),
        ),
        width="100%",
        minwidth="300px",
    )


def todo_page() -> rx.Component:
    return rx.container(
        CommonHeader(title="Todo"),
        todo_page_regist_item(),
        rx.divider(),
        todo_page_view_items(),
        rx.divider(),
        minwidth="300px",
        width="100%",
    )


app = rx.App()
app.add_page(
    index,
    title="TNApp : TopPage",
)
app.add_page(
    todo_page,
    title="TNApp : TodoPage",
    route="/todo_page",
    on_load=StateTodo.init_page(),
)
