"""TODO関連の API エンドポイント"""

from reflex_test.services.todo import *
from pydantic import BaseModel
from typing import Optional


async def test_function(msg: str):
    print(msg)
    return "OK!!!"


async def api_get_todos():
    """TODO一覧を取得"""
    items, count = get_todo_items()
    return {"items": items, "count": count}


class ApiAddTodo(BaseModel):
    title: str
    url: Optional[str] = ""
    datetime_str: Optional[str] = ""
    repeat_daily: Optional[bool] = False
    repeat_weekly: Optional[bool] = False
    repeat_monthly: Optional[bool] = False
    notify_webhook: Optional[bool] = False
    notify_email: Optional[bool] = False
    description: Optional[str] = ""


async def api_add_todo(body: ApiAddTodo):
    """TODOを追加"""
    success, message = add_todo_item(
        0,
        body.title,
        body.url or "",
        body.datetime_str or "",
        body.repeat_daily or False,
        body.repeat_weekly or False,
        body.repeat_monthly or False,
        body.notify_webhook or False,
        body.notify_email or False,
        body.description or "",
    )
    return {"success": success, "message": message}
