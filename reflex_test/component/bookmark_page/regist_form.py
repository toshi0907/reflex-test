"""bookmark登録フォームコンポーネント"""

import reflex as rx


def bookmark_page_regist_item() -> rx.Component:
    """bookmarkアイテム登録フォーム"""
    return (
        rx.vstack(
            rx.heading("Add Bookmark", as_="h2"),
            rx.input(
                placeholder="Title",
                # value=StateBookmark.form_title,
                # on_change=StateBookmark.set_form_title,
                minwidth="300px",
                width="100%",
            ),
            rx.input(
                placeholder="Url",
                # value=StateBookmark.form_url,
                # on_change=StateBookmark.set_form_url,
                minwidth="300px",
                width="100%",
            ),
            rx.input(
                placeholder="Description",
                # value=StateBookmark.form_description,
                # on_change=StateBookmark.set_form_description,
                minwidth="300px",
                width="100%",
            ),
            rx.select(
                ["A", "B"],
                placeholder="Category",
                # value=StateBookmark.form_category,
                # on_change=StateBookmark.set_form_category,
                minwidth="300px",
                width="100%",
            ),
            rx.heading("Add Category", as_="h2"),
            rx.input(
                placeholder="CategoryName",
                # value=StateBookmark.form_category_name,
                # on_change=StateBookmark.set_form_category_name,
                minwidth="300px",
                width="100%",
            ),
            minwidth="300px",
            width="100%",
        ),
    )  # pyright: ignore[reportReturnType]
