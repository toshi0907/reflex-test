"""Todo service layer for database operations"""

import reflex as rx
from reflex_test.models import DBTodoListItem


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
