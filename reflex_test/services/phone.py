"""Phone service layer for database operations"""

import reflex as rx
from reflex_test.models import DBPhoneInfoItems
from datetime import datetime
from zoneinfo import ZoneInfo


def add_phone_info(
    latitude: float,
    longitude: float,
    battery_level: float,
    free_storage: int,
) -> tuple[bool, str]:

    now = datetime.now(ZoneInfo("Asia/Tokyo")).strftime("%Y-%m-%d %H:%M:%S")

    _latitude = latitude
    if _latitude < 0:
        _latitude = None
    _longitude = longitude
    if _longitude < 0:
        _longitude = None
    _battery_level = battery_level
    if _battery_level < 0:
        _battery_level = None
    _free_storage = free_storage
    if _free_storage < 0:
        _free_storage = None

    try:
        with rx.session() as session:
            # Create new item
            new_item = DBPhoneInfoItems(
                create_at=now,
                latitude=latitude,
                longitude=longitude,
                battery_level=battery_level,
                free_storage=free_storage,
            )
            session.add(new_item)
            session.commit()

        return True, ""
    except Exception as e:
        return False, f"Error adding todo item: {str(e)}"
