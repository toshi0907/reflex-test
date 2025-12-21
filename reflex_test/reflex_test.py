"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from rxconfig import config


class StateAddItem(rx.State):
    item_name: str = ""

    def update_item_name(self, item):
        self.item_name = item

    def clear_item_name(self):
        self.item_name = ""


class State(rx.State):
    """The app state."""

    arr = ["aaa", "bbb"]

    def remove_item(self, item):
        self.arr.remove(item)

    def add_item(self, item):
        self.arr.append(item)


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


def index() -> rx.Component:
    # indexページ
    return rx.container(
        CommonHeader(title=""),
        rx.vstack(
            rx.text(f"{StateAddItem.item_name}"),
            rx.input(
                value=StateAddItem.item_name,
                on_change=StateAddItem.update_item_name,
                placeholder="Type here to add to the list",
            ),
            rx.button(
                "Clear",
                on_click=StateAddItem.clear_item_name,
            ),
            # rx.button("Click me"),
            # rx.link("Subpage", href="/subindex"),
            # rx.hstack(
            #     rx.text("test1"),
            #     rx.text("test2"),
            #     border="1px solid black",
            # ),
            # タスクリスト
            rx.foreach(
                State.arr,
                lambda item, index: rx.hstack(
                    rx.text(
                        item,
                        width="50%",
                    ),
                    rx.button(
                        "Button", width="50%", on_click=lambda: State.remove_item(item)
                    ),
                ),
            ),
            spacing="5",
            justify="center",
            min_height="85vh",
        ),
    )


### For Todo Page ###


class StateTodo(rx.State):
    inputStrTitle: str = ""
    inputStrURL: str = ""
    inputdatetime: str = "" # 形式:2025-12-21T12:33
    checkBoxRepeatDayly: bool = False
    checkBoxRepeatWeekly: bool = False
    checkBoxRepeatMonthly: bool = False

    def update_inputStrTitle(self, value: str):
        print(f"update_inputStrTitle : {value}")
        self.inputStrTitle = value

    def update_inputStrURL(self, value: str):
        print(f"update_inputStrURL : {value}")
        self.inputStrURL = value

    def update_inputdatetime(self, value: str):
        print(f"update_inputdatetime : {value}")
        self.inputdatetime = value

    def clear_inputs(self):
        self.inputStrTitle = ""
        self.inputStrURL = ""
        self.inputdatetime = ""
        self.checkBoxRepeatDayly = False
        self.checkBoxRepeatWeekly = False
        self.checkBoxRepeatMonthly = False
        return ""


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
                    on_click=lambda: State.add_item(StateTodo.clear_inputs()),
                ),
                minwidth="300px",
                width="100%",
            ),
        ),
    )


def todo_page() -> rx.Component:
    return rx.container(
        CommonHeader(title="Todo"),
        todo_page_regist_item(),
    )


app = rx.App()
app.add_page(index, title="TopPage")
app.add_page(todo_page, title="TodoPage", route="/todo_page")
