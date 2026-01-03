"""共通コンポーネント集"""

import reflex as rx
import os
from dotenv import load_dotenv

# .envファイルを読み込み
load_dotenv()


def CommonHeader(title: str) -> rx.Component:
    """共通ヘッダ"""
    title_disp = ""
    title_debug = ""
    if os.getenv("TN_DEBUG") == "True":
        title_debug = "[DEBUG] "
    if title == "":
        title_disp = title_debug + "TN App"
    else:
        title_disp = title_debug + "TN App : " + title
    return rx.vstack(
        rx.heading(
            title_disp,
            trim="both",
            as_="h1",
            color_scheme="red",
        ),
        rx.hstack(
            rx.badge(rx.link("Top", href="/")),
            rx.badge(rx.link("Todo", href="/todo_page")),
            rx.badge(rx.link("Bookmark", href="/bookmark_page")),
        ),
        rx.divider(),
        rx.spacer(height="20px"),
    )
