"""Bookmark page"""

import reflex as rx
import reflex_test.pages.common as common


def bookmark_page() -> rx.Component:
    """Bookmarkページ"""
    return rx.container(
        common.CommonHeader(title="Bookmark"),
        minwidth="300px",
        width="100%",
    )
