"""bookmark登録フォームコンポーネント"""

import reflex as rx
from reflex_test.states import (
    StateBookmark,
    StateBookmarkCategory,
)


def bookmark_page_regist_item() -> rx.Component:
    """bookmarkアイテム登録フォーム"""
    return (
        rx.vstack(
            rx.heading("Add Bookmark", as_="h2"),
            rx.text(f"ID[{StateBookmark.textHash}]"),
            rx.input(
                placeholder=StateBookmark.inputStrTitleAuto,
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
            rx.cond(
                StateBookmarkCategory.has_category_items,  # type: ignore
                rx.select(
                    StateBookmarkCategory.listCategoryItems,
                    placeholder="Category",
                    value=StateBookmark.selectStrCategoryItem,
                    on_change=StateBookmark.update_selectStrCategoryItem,  # type: ignore
                    minwidth="300px",
                    width="100%",
                ),
            ),
            rx.flex(
                rx.button(
                    "Regist",
                    on_click=lambda: StateBookmark.add_bookmark_item(),  # type: ignore
                ),
                rx.spacer(width="10px"),
                rx.button(
                    "Delete",
                    on_click=lambda: StateBookmark.remove_bookmark_item(),  # type: ignore
                ),
            ),
            rx.cond(
                StateBookmark.isErrorMessageVisible,
                rx.text(StateBookmark.textErrorMessage, color="red"),
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
                value=StateBookmarkCategory.inputStrCategoryName,
                placeholder="CategoryName",
                minwidth="300px",
                width="100%",
                on_change=StateBookmarkCategory.update_inputStrCategoryName,  # type: ignore
            ),
            rx.button(
                "Regist",
                on_click=StateBookmarkCategory.add_category_item(),  # type: ignore
            ),
            rx.cond(
                StateBookmarkCategory.isErrorMessageVisible,
                rx.text(StateBookmarkCategory.textErrorMessage, color="red"),
            ),
        ),
    )  # type: ignore[reportReturnType]
