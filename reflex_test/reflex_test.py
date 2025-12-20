"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from rxconfig import config


class State(rx.State):
    """The app state."""

    arr = ["aaa", "bbb"]

    def remove_item(self, item):
        self.arr.remove(item)


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
            rx.link("index", href="/"),
            rx.link("subpage", href="/subindex"),
        ),
        rx.divider(),
    )


def index() -> rx.Component:
    # indexページ
    return rx.container(
        CommonHeader(title=""),
        rx.vstack(
            # rx.button("Click me"),
            # rx.link("Subpage", href="/subindex"),
            rx.hstack(
                rx.text("test1"),
                rx.text("test2"),
            ),
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


def subindex() -> rx.Component:
    return rx.container(
        CommonHeader(title="SubPage"),
        rx.heading("This is a subpage", size="7"),
        rx.link(
            rx.button("Go back to Home"),
            href="/",
        ),
        rx.text("You can add more pages to your app by defining new functions."),
        spacing="5",
        justify="center",
        min_height="85vh",
    )


app = rx.App()
app.add_page(index, title="Welcome")
app.add_page(subindex, title="Subpage")
