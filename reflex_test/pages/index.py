"""Index page"""

import reflex as rx
import reflex_test.pages.common as common


def index() -> rx.Component:
    """トップページ"""
    return rx.container(
        common.CommonHeader(title=""),
    )
