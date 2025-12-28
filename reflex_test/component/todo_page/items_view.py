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
                    # rx.text(f"Done[{item.done}]"),
                    rx.text.strong(
                        f"・{item.title}",
                        on_click=lambda: StateTodo.update_item(item),
                        margin="0px",
                    ),
                    margin="0px",
                ),
                rx.cond(item.url != "", rx.text(f"URL: {item.url}"), None),
                # rx.text(f"URL: {item.url}"),
                rx.hstack(
                    rx.cond(
                        item.datetime != "", rx.text(f"{item.datetime}"), "**NoDate**"
                    ),
                    rx.text("/"),
                    rx.cond(item.notify_webhook, rx.text("WH"), None),
                    rx.cond(item.notify_email, rx.text("ML"), None),
                    rx.text("/"),
                    rx.cond(item.repeat_daily, rx.text("Daily"), None),
                    rx.cond(item.repeat_weekly, rx.text("Weekly"), None),
                    rx.cond(item.repeat_monthly, rx.text("Monthly"), None),
                    margin_left="15px",
                ),
            ),
        ),
        width="100%",
        minwidth="300px",
    )
