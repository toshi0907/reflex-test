"""Bookmark関連のデータベースモデル"""

import reflex as rx


class DBBookmarkListItem(rx.Model, table=True):
    """データベースのテーブル定義"""

    hash: int
    create_at: str
    update_at: str
    title: str
    url: str
    description: str
    category_id: int

    removed : bool = False
