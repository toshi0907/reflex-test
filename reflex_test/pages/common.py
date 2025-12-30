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
        rx.heading(title_disp, as_="h1"),
        rx.hstack(
            rx.link("Top", href="/"),
            rx.link("Todo", href="/todo_page"),
            rx.link("Bookmark", href="/bookmark_page"),
        ),
        rx.divider(),
        rx.spacer(height="20px"),
    )
