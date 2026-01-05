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
        rx.accordion.root(
            rx.foreach(
                StateBookmark.dbitemsCategory,
                lambda item_cate: rx.accordion.item(
                    header=f"{item_cate.category_name}",
                    content=rx.foreach(
                        StateBookmark.dbitems,
                        lambda item: rx.cond(
                            item_cate.id == item.category_id,
                            rx.vstack(
                                rx.hstack(
                                    rx.image(
                                        src=f"https://www.google.com/s2/favicons?domain={item.url}&sz=20",
                                        alt="Favicon",
                                        box_size="16px",
                                    ),
                                    rx.link(
                                        f"{item.title}",
                                        href=item.url,
                                        is_external=True,
                                    ),
                                    rx.button(
                                        "Edit",
                                        on_click=lambda: StateBookmark.update_item(
                                            item
                                        ),  # type: ignore
                                    ),
                                    width="100%",
                                    minwidth="300px",
                                ),
                                rx.cond(
                                    (item.description != "")
                                    & (item.description is not None),
                                    rx.foreach(
                                        item.description.split("\n"),
                                        lambda line: rx.text(f"{line}"),
                                    ),
                                    None,
                                ),
                                padding="14px",
                            ),
                            None,
                        ),
                    ),
                    value=f"item_{item_cate.id}",
                ),
            ),
            collapsible=True,
            type="single",
            width="100%",
            minwidth="300px",
            variant="ghost",  # variantをghostにすると、もともと背景がほぼ透明になります
        ),
        width="100%",
        minwidth="300px",
    )
