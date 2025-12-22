"""Index page"""

import reflex as rx
import reflex_test.pages.commom as commom


def index() -> rx.Component:
    """トップページ"""
    return rx.container(
        commom.CommonHeader(title=""),
    )
