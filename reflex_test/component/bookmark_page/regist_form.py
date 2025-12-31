"""bookmark登録フォームコンポーネント"""

import reflex as rx
from reflex_test.states import StateBookmark


def bookmark_page_regist_item() -> rx.Component:
    """bookmarkアイテム登録フォーム"""
    return (
        rx.vstack(
            rx.heading("Add Bookmark", as_="h2"),
            rx.text(f"ID[{StateBookmark.textHash}]"),
            rx.input(
                placeholder="Title",
                value=StateBookmark.inputStrTitle,
                on_change=StateBookmark.update_inputStrTitle,  # type: ignore
                minwidth="300px",
                width="100%",
            ),
            rx.input(
                placeholder="Url",
                value=StateBookmark.inputStrURL,
                on_change=StateBookmark.update_inputStrURL,  # type: ignore
                minwidth="300px",
                width="100%",
            ),
            rx.input(
                placeholder="Description",
                value=StateBookmark.inputStrDescription,
                on_change=StateBookmark.update_inputStrDescription,  # type: ignore
                minwidth="300px",
                width="100%",
            ),
            rx.select(
                StateBookmark.selectCategoryItems,
                placeholder="Category",
                value=StateBookmark.selectStrCategoryItem,
                on_change=StateBookmark.update_selectStrCategoryItem,  # type: ignore
                minwidth="300px",
                width="100%",
            ),
            rx.button(
                "Regist",
                on_click=lambda: StateBookmark.add_bookmark_item(),  # type: ignore
            ),
            rx.cond(
                StateBookmark.isErrorMessageVisible,
                rx.text(
                    StateBookmark.textErrorMessage,
                    color="red",
                ),
            ),
            minwidth="300px",
            width="100%",
        ),
    )  # type: ignore[reportReturnType]


def bookmark_category_regist_item() -> rx.Component:
    """bookmarkカテゴリ登録フォーム"""
    return (
        rx.vstack(
            rx.heading("Add Category", as_="h2"),
            rx.input(
                placeholder="CategoryName",
                minwidth="300px",
                width="100%",
            ),
            rx.button("Regist"),
        ),
    )  # type: ignore[reportReturnType]
