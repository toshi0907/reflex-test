"""bookmarkアイテム表示コンポーネント"""

import reflex as rx


def bookmark_page_view_items() -> rx.Component:
    """bookmarkアイテム一覧表示"""
    return rx.vstack(
        rx.heading("Bookmark Items", as_="h2"),
        rx.drawer.root(
            rx.drawer.trigger(rx.button("Open")),
            rx.drawer.overlay(z_index="5"),
            rx.drawer.portal(
                rx.drawer.content(
                    rx.vstack(
                        rx.drawer.close(rx.button("Close", width="100%")),
                        rx.text("category 1"),
                        rx.text("category 2"),
                        rx.text("category 3"),
                        width="100%",
                    ),
                    top="auto",
                    right="auto",
                    height="100%",
                    width="30%",
                    min_width="100px",
                    padding="2em",
                    background_color="#FFF",
                )
            ),
            direction="left",
        ),
        width="100%",
        minwidth="300px",
    )
