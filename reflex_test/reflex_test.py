"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
from sqlalchemy import create_engine, inspect

from rxconfig import config
from reflex_test.pages import (
    index,
    todo_page,
    bookmark_page,
)
from reflex_test.states import (
    StateTodo,
    StateBookmark,
    StateBookmarkCategory,
)
from reflex_test.api import create_api_app


# データベース初期化
def _init_db():
    """アプリケーション起動時にデータベーステーブルを初期化"""
    try:
        engine = create_engine(config.db_url)  # type: ignore
        inspector = inspect(engine)

        # テーブルが存在しない場合は作成
        if (
            "dbtodolistitem" not in inspector.get_table_names()
            or "dbbookmarklistitem" not in inspector.get_table_names()
            or "dbbookmarkcategorylistitem" not in inspector.get_table_names()
        ):
            print("Creating DBTodoListItem table...")
            rx.Model.metadata.create_all(engine)
            print("DBTodoListItem table created successfully.")
    except Exception as e:
        print(f"Database initialization error: {e}")


# Create a FastAPI app
fastapi_app = create_api_app()

# Global styles
style_app = {
    "font_family": "BIZ UDPGothic",
}

app = rx.App(
    api_transformer=fastapi_app,
    theme=rx.theme(accent_color="sky"),
    style=style_app,
)
app.add_page(
    index,
    title="TNApp : TopPage",
)
app.add_page(
    todo_page,
    title="TNApp : TodoPage",
    route="/todo_page",
    on_load=StateTodo.init_page(),  # type: ignore
)
app.add_page(
    bookmark_page,
    title="TNApp : BookmarkPage",
    route="/bookmark_page",
    on_load=[StateBookmark.init_page(), StateBookmarkCategory.init_page()],  # type: ignore
)

# Initialize database on startup
_init_db()

# スケジューラーの起動
# バックエンドサーバーが起動した後にスケジューラーを開始するため、
# rxconfig.pyではなくここで呼び出す
from reflex_test.scheduler import start_scheduler

try:
    start_scheduler()
except Exception as e:
    print(f"[scheduler] failed to start scheduler: {e}")
