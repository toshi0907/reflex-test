# GitHub Copilot Instructions

## プロジェクト概要
このプロジェクトは、Reflexフレームワークを使用したアプリケーションです。
プロジェクトに含む機能は特に限定されていません。

## 技術スタック
- **フレームワーク**: Reflex (Python Webフレームワーク)
- **データベース**: PostgreSQL
- **ORM**: SQLAlchemy with Alembic for migrations
- **デプロイ**: Docker/Docker Compose

## プロジェクト構造
- `reflex_test/`: メインアプリケーションディレクトリ
  - `pages/`: ページコンポーネント
  - `component/`: 再利用可能なUIコンポーネント
  - `states/`: Reflexステート管理
  - `models/`: データベースモデル
  - `services/`: ビジネスロジック層
  - `api/`: API エンドポイント
- `alembic/`: データベースマイグレーション
- `scripts/`: デプロイ・セットアップスクリプト

## コーディング規約

### Python
- **スタイル**: PEP 8に準拠
- **型ヒント**: 可能な限り型アノテーションを使用
- **Docstring**: 関数やクラスには日本語でdocstringを記述
- **インポート順**: 標準ライブラリ → サードパーティ → ローカルモジュール

### Reflexコンポーネント
- コンポーネント関数は `rx.Component` を返す
- ファイル先頭にモジュールのdocstringを記述（日本語）
- イベントハンドラーはStateクラスのメソッドとして定義

### データベース
- モデルは `models/` ディレクトリに配置
- Alembicを使用してマイグレーションを管理
- カラム名は snake_case を使用

### 日時フォーマット
- データベース保存形式: ISO 8601 (`YYYY-MM-DDTHH:MM`)

### 命名規則
- **ファイル名**: snake_case
- **クラス名**: PascalCase (State classes: `State{FeatureName}`)
- **関数名**: snake_case
- **変数名**: snake_case
- **定数**: UPPER_SNAKE_CASE

### エラーハンドリング
- 適切な例外処理を実装
- ユーザーフレンドリーなエラーメッセージ（日本語）
- ログ出力を適切に使用

## 機能一覧
- Todo機能
- Bookmark機能

## 開発時の注意点
- 環境変数は `.env` ファイルで管理（Git管理外）
- データベース変更時は必ずAlembicマイグレーションを作成
- 開発はgithub codespaces上で行うことを推奨
  - github codespaces起動時に `setup_codespace.sh` を実行して環境構築
- コミット前に `requirements.txt` を更新

## テスト
- `sandbox/` ディレクトリでプロトタイプや実験的なコードをテスト

## デプロイ
- `DEPLOY.md` を参照
- Docker Composeを使用したコンテナデプロイ
- `scripts/entrypoint.sh` でコンテナ起動時の処理を実行
- アップデート時は `update_docker.sh` を使用
