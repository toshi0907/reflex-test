"""スマホ情報関連の API エンドポイント"""

from reflex_test.services.phone import *
from pydantic import BaseModel
from typing import Optional


class APIPhoneInfoAdd(BaseModel):
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    battery_level: Optional[float] = None
    free_storage: Optional[int] = None


async def api_add_phone_info(body: APIPhoneInfoAdd):
    """スマホ情報を追加"""
    success, message = add_phone_info(
        body.latitude or -1,
        body.longitude or -1,
        body.battery_level or -1,
        body.free_storage or -1,
    )

    return {"success": success, "message": message}
