"""Todo service layer for database operations"""

import reflex as rx
from reflex_test.models import DBTodoListItem
from datetime import datetime
from zoneinfo import ZoneInfo


def get_todo_items() -> tuple[list[DBTodoListItem], int]:
    """
    Get todo items from database that are not done

    Returns:
        tuple[list[DBTodoListItem], int]: List of todo items and count
    """
    with rx.session() as session:
        items = session.exec(
            DBTodoListItem.select().where(DBTodoListItem.done == False)
        ).all()
        count = len(items)
    return items, count


def get_todo_item_all(hash: int) -> DBTodoListItem | None:
    """
    Get all todo items from database

    Returns:
        tuple[list[DBTodoListItem], int]: List of todo items and count
    """
    with rx.session() as session:
        item = session.exec(DBTodoListItem.select()).all()
    return item


def add_todo_item(
    text_hash: int,
    title: str,
    url: str,
    datetime_str: str,
    repeat_daily: bool,
    repeat_weekly: bool,
    repeat_monthly: bool,
    notify_webhook: bool,
    notify_email: bool,
    description: str = "",
) -> tuple[bool, str]:
    """
    Add or update a todo item in the database

    Args:
        text_hash: ID of item (0 for new item)
        title: Title of the todo item
        url: URL associated with the todo item
        datetime_str: Datetime in format "2025-12-21T12:33"
        repeat_daily: Whether to repeat daily
        repeat_weekly: Whether to repeat weekly
        repeat_monthly: Whether to repeat monthly
        notify_webhook: Whether to notify via webhook
        notify_email: Whether to notify via email
        description: Description of the todo item

    Returns:
        tuple[bool, str]: (success, error_message)
    """
    # Validation
    if not title:
        return False, "Title is required."

    if not notify_email and not notify_webhook:
        return False, "At least one notification method is required."

    # URLの形式確認
    if not (url.startswith("http://") or url.startswith("https://")):
        return False, "URL must start with http:// or https://."

    # Get current datetime in JST
    now = datetime.now(ZoneInfo("Asia/Tokyo")).strftime("%Y-%m-%d %H:%M:%S")

    try:
        with rx.session() as session:
            if text_hash != 0:
                # Update existing item
                item_todos = session.exec(
                    DBTodoListItem.select().where(DBTodoListItem.id == text_hash)
                ).all()

                for item_todo in item_todos:
                    item_todo.update_at = now
                    item_todo.title = title
                    item_todo.url = url
                    item_todo.datetime = datetime_str
                    item_todo.repeat_daily = repeat_daily
                    item_todo.repeat_weekly = repeat_weekly
                    item_todo.repeat_monthly = repeat_monthly
                    item_todo.notify_webhook = notify_webhook
                    item_todo.notify_email = notify_email
                    item_todo.description = description
                    session.add(item_todo)

                session.commit()
            else:
                # Create new item
                new_item = DBTodoListItem(
                    hash=1,
                    create_at=now,
                    update_at=now,
                    title=title,
                    url=url,
                    datetime=datetime_str,
                    repeat_daily=repeat_daily,
                    repeat_weekly=repeat_weekly,
                    repeat_monthly=repeat_monthly,
                    notify_webhook=notify_webhook,
                    notify_email=notify_email,
                    description=description,
                    done=False,
                )
                session.add(new_item)
                session.commit()

        return True, ""
    except Exception as e:
        return False, f"Error adding todo item: {str(e)}"


def remove_todo_item(item_id: str) -> tuple[bool, str]:
    """
    Mark a todo item as done (soft delete)

    Args:
        item_id: ID of the todo item to remove

    Returns:
        tuple[bool, str]: (success, error_message)
    """
    try:
        with rx.session() as session:
            item_todos = session.exec(
                DBTodoListItem.select().where(DBTodoListItem.id == item_id)
            ).all()

            for item_todo in item_todos:
                item_todo.done = True
                session.add(item_todo)

            session.commit()

        return True, ""
    except Exception as e:
        return False, f"Error removing todo item: {str(e)}"
