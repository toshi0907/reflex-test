import os
import reflex as rx
from dotenv import load_dotenv

# .envファイルを読み込み
load_dotenv()

# 環境変数からデータベースURLを取得（デフォルトはSQLite）
env_db_url = os.getenv("DATABASE_URL", "sqlite:///data/reflex.db")

# ホスト名を環境変数から取得（デフォルトは従来の値）
frontend_host = os.getenv("FRONTEND_HOST", "localhost:3000")
backend_host = os.getenv("BACKEND_HOST", None)

# プラグインの設定
plugins = [
    rx.plugins.SitemapPlugin(),
    rx.plugins.TailwindV4Plugin(),
]

# Configオブジェクトの作成
config_kwargs = {
    "app_name": "reflex_test",
    "db_url": env_db_url,
    "plugins": plugins,
}

# backend_host が設定されている場合のみ api_url を渡す
# github codespaces では localhost:8000 ではうまく動作しないため
if backend_host:
    config_kwargs["api_url"] = "https://" + backend_host  # backend_host が設定されている時のみ渡す

config = rx.Config(**config_kwargs)

# End of file
