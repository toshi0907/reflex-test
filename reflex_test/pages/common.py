"""共通コンポーネント集"""

import reflex as rx


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
            rx.link("BookmarkPage", href="/bookmark_page"),
        ),
        rx.divider(),
        rx.spacer(height="20px"),
    )
