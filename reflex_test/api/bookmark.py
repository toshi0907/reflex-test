"""ブックマーク関連の API エンドポイント"""

from reflex_test.services.bookmark import *
from pydantic import BaseModel


async def api_get_bookmarks():
    """ブックマーク一覧を取得"""
    return get_bookmark_items()


class ApiAddBookmark(BaseModel):
    title: str
    url: str
    description: str
    category_id: int


async def api_add_bookmark(body: ApiAddBookmark):
    """ブックマークを追加"""
    success, message = add_bookmark_item(
        0,
        body.title,
        body.url,
        body.description,
        body.category_id,
    )
    return {"success": success, "message": message}


async def api_get_categories():
    """ブックマークカテゴリ一覧を取得"""
    items, count = get_category_items()
    return {"items": items, "count": count}


class ApiAddCategoryItem(BaseModel):
    name: str


async def api_add_category_item(body: ApiAddCategoryItem) -> dict[str, bool | str]:
    """ブックマークカテゴリを追加"""
    success, message = add_category_item(0, body.name)
    return {"result": success, "message": message}
