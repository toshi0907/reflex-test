"""bookmarkアイテム表示コンポーネント"""

import reflex as rx


def bookmark_page_view_items() -> rx.Component:
    """bookmarkアイテム一覧表示"""
    return rx.vstack(
        rx.heading("Bookmark Items", as_="h2"),
        rx.heading("Category1", as_="h3"),
        rx.link("google", href="https://www.google.com", is_external=True),
        rx.link("yahoo", href="https://www.yahoo.co.jp", is_external=True),
        rx.heading("Category2", as_="h3"),
        rx.link("google", href="https://www.google.com", is_external=True),
        rx.link("yahoo", href="https://www.yahoo.co.jp", is_external=True),
        width="100%",
        minwidth="300px",
    )
