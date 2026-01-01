"""Bookmark関連のデータベースモデル"""

import reflex as rx


class DBBookmarkListItems(rx.Model, table=True):
    """データベースのテーブル定義 : ブックマーク"""

    hash: int
    create_at: str
    update_at: str
    title: str
    url: str
    description: str
    category_id: int

    removed: bool = False


class DBBookmarkCategoryListItems(rx.Model, table=True):
    """データベースのテーブル定義 : カテゴリ"""

    create_at: str
    update_at: str
    category_name: str

    removed: bool = False
