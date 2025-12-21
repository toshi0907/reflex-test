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
    repeat_dayly: bool
    repeat_weekly: bool
    repeat_monthly: bool


class StateTodo(rx.State):
    inputStrTitle: str = ""
    inputStrURL: str = ""
    inputdatetime: str = ""  # 形式:2025-12-21T12:33
    checkBoxRepeatDayly: bool = False
    checkBoxRepeatWeekly: bool = False
    checkBoxRepeatMonthly: bool = False

    dbitems: list[DBTodoListItem] = []

    textErrorMessage: str = ""
    isErrorMessageVisible: bool = False

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

    def update_textErrorMessage(self, value: str):
        print(f"update_textErrorMessage : {value}")
        self.textErrorMessage = value
        self.isErrorMessageVisible = True

    def add_todo_item(self):
        print("add_todo_item")
        with rx.session() as session:
            new_item = DBTodoListItem(
                hash=1,
                create_at="2024-01-01 12:00:00",
                update_at="2024-01-01 12:00:00",
                title=self.inputStrTitle,
                url=self.inputStrURL,
                datetime=self.inputdatetime,
                repeat_dayly=self.checkBoxRepeatDayly,
                repeat_weekly=self.checkBoxRepeatWeekly,
                repeat_monthly=self.checkBoxRepeatMonthly,
            )
            session.add(new_item)
            session.commit()

    def get_todo_item(self):
        with rx.session() as session:
            # select文で全件取得
            self.dbitems = session.exec(DBTodoListItem.select()).all()
            print(len(self.dbitems))

    def clear_inputs(self):
        self.inputStrTitle = ""
        self.inputStrURL = ""
        self.inputdatetime = ""
        self.checkBoxRepeatDayly = False
        self.checkBoxRepeatWeekly = False
        self.checkBoxRepeatMonthly = False


def todo_page_regist_item() -> rx.Component:
    return (
        rx.vstack(
            rx.heading("Add Item", as_="h2"),
            rx.vstack(
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
                    rx.checkbox(
                        "Repeat Daily", is_checked=StateTodo.checkBoxRepeatDayly
                    ),
                    rx.checkbox(
                        "Repeat Weekly", is_checked=StateTodo.checkBoxRepeatWeekly
                    ),
                    rx.checkbox(
                        "Repeat Monthly", is_checked=StateTodo.checkBoxRepeatMonthly
                    ),
                ),
                rx.button(
                    "Clear",
                    on_click=lambda: StateTodo.clear_inputs(),
                ),
                rx.button(
                    "Add Item",
                    on_click=lambda: StateTodo.add_todo_item(),
                ),
                rx.button(
                    "Get Item",
                    on_click=lambda: StateTodo.get_todo_item(),
                ),
                rx.cond(
                    StateTodo.isErrorMessageVisible,
                    rx.text(
                        StateTodo.textErrorMessage,
                        status="error",
                    ),
                ),
                minwidth="300px",
                width="100%",
            ),
        ),
    )

def todo_page_view_items() -> rx.Component:
    StateTodo.get_todo_item()
    return rx.vstack(
        rx.heading("Todo Items", as_="h2"),
        # rx.text(len(StateTodo.get_todo_item())),
        rx.foreach(
            StateTodo.dbitems,
            lambda item: rx.vstack(
                rx.text(f"Title: {item.title}"),
                rx.text(f"URL: {item.url}"),
                rx.text(f"Datetime: {item.datetime}"),
                rx.divider(),
            ),
        ),
    )

def todo_page() -> rx.Component:
    return rx.container(
        CommonHeader(title="Todo"),
        todo_page_regist_item(),
        todo_page_view_items(),
    )


app = rx.App()
app.add_page(index, title="TopPage")
app.add_page(todo_page, title="TodoPage", route="/todo_page")
