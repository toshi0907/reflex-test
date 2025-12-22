"""Todo page"""

import reflex as rx
from reflex_test.component.todo_page import todo_page_regist_item, todo_page_view_items
from reflex_test.states import StateTodo
from reflex_test.pages.index import CommonHeader


def todo_page() -> rx.Component:
    """Todoページ"""
    return rx.container(
        CommonHeader(title="Todo"),
        todo_page_regist_item(),
        rx.spacer(height="20px"),
        rx.divider(),
        rx.spacer(height="20px"),
        todo_page_view_items(),
        rx.spacer(height="20px"),
        rx.divider(),
        rx.spacer(height="20px"),
        minwidth="300px",
        width="100%",
    )
