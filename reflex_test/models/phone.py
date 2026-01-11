"""スマホ情報関連のデータベースモデル"""

import reflex as rx
from typing import Optional


class DBPhoneInfoItems(rx.Model, table=True):
    """データベースのテーブル定義 : スマホ情報"""

    create_at: str

    ### 位置情報
    latitude: Optional[float] = None  # 緯度
    longitude: Optional[float] = None  # 経度

    ### バッテリー情報
    battery_level: Optional[float] = None  # バッテリー残量(0.0~1.0)
    ### ストレージ情報
    free_storage: Optional[int] = None  # 空きストレージ容量(GB)