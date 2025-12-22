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

# ポートを公開
EXPOSE 3000 8000

# アプリケーションを起動（開発モードで起動）
CMD ["reflex", "run", "--loglevel", "info"]
