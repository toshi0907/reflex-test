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
                rx.cond(
                    item.description != "",
                    rx.text_area(
                        f"{item.description}",
                        is_read_only=True,
                        width="100%",
                        minwidth="300px",
                    ),
                    None,
                ),
                rx.hstack(
                    rx.cond(
                        item.datetime != "", rx.text(f"{item.datetime}"), "**NoDate**"
                    ),
                    rx.text("/"),
                    rx.cond(item.notify_webhook, rx.text("🔗"), None),
                    rx.cond(item.notify_email, rx.text("✉"), None),
                    rx.text("/"),
                    rx.cond(item.repeat_daily, rx.text("①"), None),
                    rx.cond(item.repeat_weekly, rx.text("⑦"), None),
                    rx.cond(item.repeat_monthly, rx.text("㉚"), None),
                    margin_left="15px",
                ),
                width="100%",
                minwidth="300px",
                # For debug
                # rx.text(f"ID:{item.id}"),
                # rx.text(f"Create at:{item.create_at}"),
                # rx.text(f"Update at:{item.update_at}"),
            ),
        ),
        width="100%",
        minwidth="300px",
    )
