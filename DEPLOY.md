# Docker Deployment Guide

## 前提条件
- Docker と Docker Compose がインストールされていること
- `.env` ファイルがプロジェクトルートに存在すること
- `reflex_test.db` ファイルが存在すること（初回は自動作成）

## ⚠️ 重要な注意事項

### GitHub Codespaces環境での制限
GitHub Codespaces環境でDockerコンテナを使用すると、WebSocketの接続に問題が発生する場合があります。
Codespaces環境では、**Dockerを使用せず直接reflexを起動することを強く推奨します**：

```bash
# 仮想環境をアクティベート
source .venv/bin/activate

# 直接起動（推奨）
reflex run
```

**Dockerデプロイは本番環境またはローカル開発環境で使用してください。**

---

## デプロイ手順

### 1. 環境変数ファイルの準備
```bash
# .env ファイルを作成または編集
cp .env.example .env

# 必要な環境変数を設定
# - DATABASE_URL=sqlite:///reflex.db
# - GMAIL_USER=your_email@gmail.com
# - GMAIL_PASSWORD=your_app_password
# - GMAIL_TO=destination@example.com
```

### 2. Dockerイメージのビルド
```bash
docker compose build
```

### 3. コンテナの起動
```bash
docker compose up -d
```

### 4. ログの確認
```bash
docker compose logs -f reflex-app
```

### 5. アプリケーションへのアクセス
- フロントエンド: http://localhost:3000
- バックエンドAPI: http://localhost:8000

## 管理コマンド

### コンテナの停止
```bash
docker compose down
```

### コンテナの再起動
```bash
docker compose restart
```

### コンテナの再ビルド
```bash
docker compose build --no-cache
docker compose up -d
```

### データベースのバックアップ
```bash
# SQLiteの場合（ホスト側のファイルをコピー）
cp reflex_test.db reflex_test.db.backup.$(date +%Y%m%d_%H%M%S)
```

### コンテナ内でコマンドを実行
```bash
docker compose exec reflex-app bash
```

### コンテナ内でAlembicマイグレーション実行
```bash
docker compose exec reflex-app alembic upgrade head
```

## PostgreSQLを使用する場合

1. `docker compose.yml` のコメントアウトされた `postgres` サービスを有効化
2. `.env` に PostgreSQL接続情報を追加：
```bash
DATABASE_URL=postgresql://reflex:reflex@postgres:5432/reflex_db
POSTGRES_USER=reflex
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DB=reflex_db
```

3. docker compose.yml の postgres セクションと volumes セクションのコメントを外す

4. 再ビルドして起動：
```bash
docker compose down
docker compose up -d
```

## トラブルシューティング

### ポートが既に使用されている
```bash
# docker compose.yml の ports セクションを編集
# 例: "3001:3000" に変更
```

### データベースファイルのパーミッションエラー
```bash
chmod 666 reflex_test.db
```

### .env ファイルが読み込まれない
```bash
# .env ファイルのパーミッションを確認
ls -la .env
chmod 644 .env
```

### コンテナが起動しない
```bash
# ログを確認
docker compose logs reflex-app

# コンテナの状態を確認
docker compose ps
```

### イメージのクリーンアップ
```bash
# 未使用のイメージを削除
docker image prune -a

# すべてをクリーンアップ
docker compose down -v
docker system prune -a
```

## セキュリティ注意事項

- 本番環境では `.env` ファイルを Git にコミットしないこと
- `.gitignore` に `.env` と `*.db` を追加済み
- PostgreSQL を使用する場合は強力なパスワードを設定すること
- 本番環境では適切なファイアウォール設定を行うこと
- HTTPS を使用すること（リバースプロキシ経由）

## 本番環境への推奨設定

### 1. リバースプロキシの使用（Nginx例）
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 2. HTTPS の設定
Let's Encrypt などで SSL 証明書を取得

### 3. 定期バックアップスクリプト
```bash
#!/bin/bash
# backup.sh
BACKUP_DIR="/path/to/backups"
DATE=$(date +%Y%m%d_%H%M%S)
cp reflex_test.db "$BACKUP_DIR/reflex_test.db.$DATE"
# 古いバックアップを削除（30日以上前）
find "$BACKUP_DIR" -name "reflex_test.db.*" -mtime +30 -delete
```

### 4. リソース制限の追加
docker compose.yml に以下を追加：
```yaml
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
```

## 開発環境での使用

開発中は以下のようにホットリロードを有効にできます：
```yaml
    volumes:
      - ./reflex_test:/app/reflex_test
      - ./.env:/app/.env:ro
      - ./reflex_test.db:/app/reflex_test.db
    command: reflex run --loglevel debug
```
