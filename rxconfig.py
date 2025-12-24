import os
import reflex as rx
from dotenv import load_dotenv

# .envファイルを読み込み
load_dotenv()

# 環境変数からデータベースURLを取得（デフォルトはSQLite）
env_db_url = os.getenv("DATABASE_URL", "sqlite:///data/reflex.db")

# ホスト名を環境変数から取得（デフォルトは従来の値）
frontend_host = os.getenv("FRONTEND_HOST", "localhost:3000")
backend_host = os.getenv("BACKEND_HOST", "localhost:8000")

config = rx.Config(
    app_name="reflex_test",
    db_url=env_db_url,
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
    api_url=f"https://{backend_host}",  # SSL化したバックエンドURL
    vite_config={
        "server": {
            "middlewareMode": True,
            "allowedHosts": [
                frontend_host,
                backend_host,
                "localhost",
                "127.0.0.1",
            ],
            "hmr": {
                "host": frontend_host,
                "port": 443,
                "protocol": "wss",
            },
        }
    },
)
