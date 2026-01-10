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
                        width="50%",
                    ),
                    rx.flex(
                        rx.cond(
                            item.datetime != "",
                            rx.hstack(
                                rx.text("【"),
                                rx.text(f"{item.datetime[5:16].replace('T', ' ')}"),
                                # rx.text(f"{item.datetime}"),
                                rx.text("/"),
                                rx.cond(item.notify_webhook, rx.text("🔗"), None),
                                rx.cond(item.notify_email, rx.text("✉"), None),
                                rx.text("/"),
                                rx.cond(item.repeat_daily, rx.text("①"), None),
                                rx.cond(item.repeat_weekly, rx.text("⑦"), None),
                                rx.cond(item.repeat_monthly, rx.text("㉚"), None),
                                rx.cond(
                                    (~item.repeat_daily)
                                    & (~item.repeat_weekly)
                                    & (~item.repeat_monthly),
                                    rx.text("Once"),
                                    None,
                                ),
                                rx.text("】"),
                            ),
                            rx.text("【---】"),
                        ),
                        width="50%",
                    ),
                    width="100%",
                ),
                rx.cond(
                    item.url != "",
                    rx.link(
                        f"URL: {item.url}",
                        href=item.url,
                        is_external=True,
                    ),
                    None,
                ),
                rx.cond(
                    (item.description != "") & (item.description is not None),
                    rx.foreach(
                        item.description.split("\n"),
                        lambda line: rx.text(
                            f"{line}",
                            margin_left="15px",
                            padding_top="0px",
                            padding_bottom="0px",
                            margin_top="0px",
                            margin_bottom="0px",
                        ),
                    ),
                    None,
                ),
                # For debug
                # rx.text(f"ID:{item.id}"),
                # rx.text(f"Create at:{item.create_at}"),
                # rx.text(f"Update at:{item.update_at}"),
                width="100%",
                minwidth="300px",
            ),
        ),
        width="100%",
        minwidth="300px",
    )
