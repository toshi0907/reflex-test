"""Bookmark service layer for database operations"""

import reflex as rx
from reflex_test.models import DBBookmarkListItem
from datetime import datetime
from zoneinfo import ZoneInfo


def get_bookmark_items() -> tuple[list[DBBookmarkListItem], int]:
    with rx.session() as session:
        items = session.exec(
            DBBookmarkListItem.select().where(DBBookmarkListItem.removed == False)
        ).all()
        count = len(items)
    return items, count


def get_todo_item_all(hash: int) -> DBBookmarkListItem | None:
    with rx.session() as session:
        item = session.exec(DBBookmarkListItem.select()).all()
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
                    DBBookmarkListItem.select().where(
                        DBBookmarkListItem.id == text_hash
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
                new_item = DBBookmarkListItem(
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
        with rx.session() as session:
            item_bookmarks = session.exec(
                DBBookmarkListItem.select().where(DBBookmarkListItem.id == item_id)
            ).all()

            for item_bookmark in item_bookmarks:
                item_bookmark.removed = True
                session.add(item_bookmark)

            session.commit()

        return True, ""
    except Exception as e:
        return False, f"Error removing bookmark item: {str(e)}"
