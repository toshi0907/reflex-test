"""Bookmark service layer for database operations"""

import reflex as rx
from reflex_test.models import (
    DBBookmarkListItems,
    DBBookmarkCategoryListItems,
)
from datetime import datetime
from zoneinfo import ZoneInfo

import requests
from bs4 import BeautifulSoup


def get_bookmark_items() -> tuple[list[DBBookmarkListItems], int]:
    with rx.session() as session:
        items = session.exec(
            DBBookmarkListItems.select().where(DBBookmarkListItems.removed == False)
        ).all()
        count = len(items)
    return items, count


def get_todo_item_all(hash: int) -> DBBookmarkListItems | None:
    with rx.session() as session:
        item = session.exec(DBBookmarkListItems.select()).all()
    return item


def add_bookmark_item(
    text_hash: int,
    title: str,
    url: str,
    description: str,
    category_id: int,
) -> tuple[bool, str]:
    # Validation
    if not url:
        return False, "URL is required."

    # URLの形式確認
    if not (url.startswith("http://") or url.startswith("https://")) and url != "":
        return False, "URL must start with http:// or https://."

    # Get current datetime in JST
    now = datetime.now(ZoneInfo("Asia/Tokyo")).strftime("%Y-%m-%d %H:%M:%S")

    try:
        with rx.session() as session:
            if text_hash != 0:
                # Update existing item
                item_bookmarks = session.exec(
                    DBBookmarkListItems.select().where(
                        DBBookmarkListItems.id == text_hash
                    )
                ).all()

                for item_bookmark in item_bookmarks:
                    item_bookmark.update_at = now
                    item_bookmark.title = title
                    item_bookmark.url = url
                    item_bookmark.description = description
                    item_bookmark.category_id = category_id
                    session.add(item_bookmark)

                session.commit()
            else:
                # Create new item
                new_item = DBBookmarkListItems(
                    hash=0,
                    create_at=now,
                    update_at=now,
                    title=title,
                    url=url,
                    description=description,
                    category_id=category_id,
                )
                session.add(new_item)
                session.commit()

        return True, ""
    except Exception as e:
        return False, f"Error adding bookmark item: {str(e)}"


def remove_bookmark_item(item_id: str) -> tuple[bool, str]:
    try:
        print(item_id)
        with rx.session() as session:
            item_bookmarks = session.exec(
                DBBookmarkListItems.select().where(DBBookmarkListItems.id == item_id)
            ).all()

            for item_bookmark in item_bookmarks:
                item_bookmark.removed = True
                session.add(item_bookmark)

            session.commit()

        return True, ""
    except Exception as e:
        return False, f"Error removing bookmark item: {str(e)}"


def get_category_items() -> tuple[list[DBBookmarkCategoryListItems], int]:
    with rx.session() as session:
        items = session.exec(
            DBBookmarkCategoryListItems.select().where(
                DBBookmarkCategoryListItems.removed == False
            )
        ).all()
        count = len(items)
    return items, count


def get_category_item_all(hash: int) -> DBBookmarkCategoryListItems | None:
    with rx.session() as session:
        item = session.exec(DBBookmarkCategoryListItems.select()).all()
    return item


def add_category_item(
    text_hash: int,
    category_name: str,
) -> tuple[bool, str]:
    # Validation
    if not category_name:
        return False, "Category name is required."

    # カテゴリ名の重複確認
    with rx.session() as session:
        existing_items = session.exec(
            DBBookmarkCategoryListItems.select().where(
                DBBookmarkCategoryListItems.category_name == category_name,
                DBBookmarkCategoryListItems.removed == False,
            )
        ).all()
        if existing_items:
            return False, "Category name already exists."

    # Get current datetime in JST
    now = datetime.now(ZoneInfo("Asia/Tokyo")).strftime("%Y-%m-%d %H:%M:%S")

    try:
        with rx.session() as session:
            if text_hash != 0:
                # Update existing item
                item_categorys = session.exec(
                    DBBookmarkCategoryListItems.select().where(
                        DBBookmarkCategoryListItems.id == text_hash
                    )
                ).all()

                for item_category in item_categorys:
                    item_category.update_at = now
                    item_category.category_name = category_name
                    session.add(item_category)

                session.commit()
            else:
                # Create new item
                new_item = DBBookmarkCategoryListItems(
                    create_at=now,
                    update_at=now,
                    category_name=category_name,
                )
                session.add(new_item)
                session.commit()

        return True, ""
    except Exception as e:
        return False, f"Error adding category item: {str(e)}"


def remove_category_item(item_id: str) -> tuple[bool, str]:
    try:
        with rx.session() as session:
            item_categorys = session.exec(
                DBBookmarkCategoryListItems.select().where(
                    DBBookmarkCategoryListItems.id == item_id
                )
            ).all()

            for item_category in item_categorys:
                item_category.removed = True
                session.add(item_category)

            session.commit()

        return True, ""
    except Exception as e:
        return False, f"Error removing category item: {str(e)}"


def get_page_title(url):
    try:
        # ページの内容を取得（タイムアウトを5秒に設定）
        response = requests.get(url, timeout=5)

        # ステータスコードが200（成功）か確認
        response.raise_for_status()

        # 文字化け防止のためエンコーディングを設定
        response.encoding = response.apparent_encoding

        # BeautifulSoupでHTMLを解析
        soup = BeautifulSoup(response.text, "html.parser")

        # <title>タグを取得
        title = soup.title.string if soup.title else ""

        return title.strip()

    except requests.exceptions.RequestException as e:
        return ""
        # return f"エラーが発生しました: {e}"
