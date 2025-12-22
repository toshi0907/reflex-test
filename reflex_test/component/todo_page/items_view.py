"""Todoアイテム表示コンポーネント"""

import reflex as rx
from reflex_test.states import StateTodo


def todo_page_view_items() -> rx.Component:
    """Todoアイテム一覧表示"""
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
                    rx.button(
                        "Remove",
                        on_click=lambda: StateTodo.remove_todo_item(item.id),
                    ),
                    rx.text(f"Done[{item.done}]"),
                    rx.text(f"Title: {item.title}"),
                ),
                rx.text(f"URL: {item.url}"),
                rx.text(
                    f"D: {item.repeat_daily} / W: {item.repeat_weekly} / M: {item.repeat_monthly}"
                ),
                rx.text(f"Webhook: {item.notify_webhook} / Email: {item.notify_email}"),
                rx.text(f"Datetime: {item.datetime}"),
            ),
        ),
        width="100%",
        minwidth="300px",
    )
