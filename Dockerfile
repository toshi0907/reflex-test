# Dockerfile for Reflex Todo Application
FROM python:3.12-slim

# 作業ディレクトリを設定
WORKDIR /app

# システム依存関係をインストール
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Pythonの依存関係をコピーしてインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションファイルをコピー
COPY rxconfig.py .
COPY alembic.ini .
COPY alembic/ ./alembic/
COPY assets/ ./assets/
COPY reflex_test/ ./reflex_test/

# Reflexアプリケーションを初期化
RUN reflex init

ARG REFLEX_FRONTEND_HOST
ARG REFLEX_BACKEND_HOST

# Viteサーバーの設定を修正（allowedHostsを追加）
# TODO: Reflexで公式対応されるまでの暫定対応
RUN python3 << EOF
import re
import os

config_file = '/app/.web/vite.config.js'
with open(config_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 環境変数を取得
frontend_host = os.environ.get('REFLEX_FRONTEND_HOST', 'localhost')
backend_host = os.environ.get('REFLEX_BACKEND_HOST', 'localhost')

# server設定を拡張
replacement = r'\1' + f'\n    allowedHosts: ["{frontend_host}", "{backend_host}", "localhost", "127.0.0.1"],\n    host: "0.0.0.0",'
new_content = re.sub(
    r"(server:\s*\{\s*port:\s*process\.env\.PORT,)",
    replacement,
    content
)

with open(config_file, 'w', encoding='utf-8') as f:
    f.write(new_content)
EOF

# ポートを公開
EXPOSE 3000 8000

# アプリケーションを起動（開発モードで起動）
CMD ["reflex", "run", "--loglevel", "info"]
