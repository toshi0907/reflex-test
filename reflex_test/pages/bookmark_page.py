"""Bookmark page"""

import reflex as rx
import reflex_test.pages.common as common
from reflex_test.component.bookmark_page import (
    bookmark_page_regist_item,
    bookmark_category_regist_item,
    bookmark_page_view_items,
)

# from reflex_test.states import StateTodo # TODO


def bookmark_page() -> rx.Component:
    """Bookmarkページ"""
    return rx.container(
        common.CommonHeader(title="Bookmark"),
        bookmark_page_view_items(),
        rx.spacer(height="20px"),
        rx.divider(),
        rx.spacer(height="20px"),
        bookmark_page_regist_item(),
        rx.spacer(height="20px"),
        rx.divider(),
        rx.spacer(height="20px"),
        bookmark_category_regist_item(),
        rx.spacer(height="20px"),
        rx.divider(),
        rx.spacer(height="20px"),
        minwidth="300px",
        width="100%",
    )
