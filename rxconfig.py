import os
import reflex as rx
from dotenv import load_dotenv

# .envファイルを読み込み
load_dotenv()

# 環境変数からデータベースURLを取得（デフォルトはSQLite）
env_db_url = os.getenv("DATABASE_URL", "sqlite:///reflex.db")

config = rx.Config(
    app_name="reflex_test",
    db_url=env_db_url,
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)