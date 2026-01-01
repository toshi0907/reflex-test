"""bookmarkアイテム表示コンポーネント"""

import reflex as rx
from reflex_test.states import (
    StateBookmark,
    StateBookmarkCategory,
)


def bookmark_page_view_items() -> rx.Component:
    """bookmarkアイテム一覧表示"""
    return rx.vstack(
        rx.heading("Bookmark Items", as_="h2"),
        rx.foreach(
            StateBookmark.dbitemsCategory,
            lambda item_cate: rx.vstack(
                rx.heading(f"{item_cate.category_name}", as_="h3"),
                rx.foreach(
                    StateBookmark.dbitems,
                    lambda item: rx.cond(
                        item_cate.id == item.category_id,
                        rx.vstack(
                            rx.hstack(
                                rx.link(
                                    f"・{item.category_id} : {item.title}",
                                    href=item.url,
                                    is_external=True,
                                ),
                            ),
                            rx.cond(
                                (item.description != "")
                                & (item.description is not None),
                                rx.foreach(
                                    item.description.split("\n"),
                                    lambda line: rx.text(f"des:{line}"),
                                ),
                                None,
                            ),
                        ),
                        None,
                    ),
                ),
            ),
        ),
        width="100%",
        minwidth="300px",
    )
