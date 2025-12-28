"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
from sqlalchemy import create_engine, inspect
import asyncio

from rxconfig import config
from reflex_test.pages import index, todo_page
from reflex_test.states import StateTodo
from reflex_test.scheduler import start_scheduler


# データベース初期化
def _init_db():
    """アプリケーション起動時にデータベーステーブルを初期化"""
    try:
        engine = create_engine(config.db_url)
        inspector = inspect(engine)

        # テーブルが存在しない場合は作成
        if "dbtodolistitem" not in inspector.get_table_names():
            print("Creating DBTodoListItem table...")
            rx.Model.metadata.create_all(engine)
            print("DBTodoListItem table created successfully.")
    except Exception as e:
        print(f"Database initialization error: {e}")


app = rx.App()
app.add_page(
    index,
    title="TNApp : TopPage",
)
app.add_page(
    todo_page,
    title="TNApp : TodoPage",
    route="/todo_page",
    on_load=StateTodo.init_page(),
)

# Initialize database on startup
_init_db()

# スケジューラーの起動
# バックエンドサーバーが起動した後にスケジューラーを開始するため、
# rxconfig.pyではなくここで呼び出す
try:
    start_scheduler()
except Exception as e:
    print(f"[scheduler] failed to start scheduler: {e}")
