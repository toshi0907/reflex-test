# Todo関連コード分割リファクタリング計画

## 概要
`/todo_page` に関するコードをモダンな構成に分割し、保守性とスケーラビリティを向上させます。

## 目標構成

```
reflex_test/
├── __init__.py
├── models/
│   ├── __init__.py
│   └── todo.py          # DBTodoListItem モデル
├── states/
│   ├── __init__.py
│   └── todo.py          # StateTodo (State管理)
├── component/
│   ├── __init__.py
│   ├── tn_base_class.py (既存)
│   ├── send_email.py (既存)
│   └── todo_page/
│       ├── __init__.py
│       └── todo.py    # todo_page_regist_item() / todo_page_view_items()
├── pages/
│   ├── __init__.py
│   ├── index.py         # index()
│   └── todo_page.py     # todo_page()
└── reflex_test.py       # アプリ初期化とページ登録のみ
```

## 実装ステップ

### Step 1: ディレクトリ・パッケージの作成
- [ ] `reflex_test/models/` ディレクトリ作成
- [ ] `reflex_test/models/__init__.py` 作成
- [ ] `reflex_test/states/` ディレクトリ作成
- [ ] `reflex_test/states/__init__.py` 作成
- [ ] `reflex_test/component/todo_page/` ディレクトリ作成
- [ ] `reflex_test/component/todo_page/__init__.py` 作成
- [ ] `reflex_test/pages/` ディレクトリ作成
- [ ] `reflex_test/pages/__init__.py` 作成

### Step 2: モデル層の実装
- [ ] `reflex_test/models/todo.py` を作成
- [ ] `DBTodoListItem` クラスを移動
- [ ] `reflex_test/models/__init__.py` に export を追加

### Step 3: State管理層の実装
- [ ] `reflex_test/states/todo.py` を作成
- [ ] `StateTodo` クラスを移動
- [ ] `reflex_test/states/__init__.py` に export を追加
- [ ] models のインポートを追加

### Step 4: UIコンポーネント層の実装
- [ ] `reflex_test/component/todo_page/regist_form.py` を作成
- [ ] `todo_page_regist_item()` を移動
- [ ] `reflex_test/component/todo_page/items_view.py` を作成
- [ ] `todo_page_view_items()` を移動
- [ ] `reflex_test/component/todo_page/__init__.py` に export を追加
- [ ] states のインポートを追加

### Step 5: ページレイヤーの実装
- [ ] `reflex_test/pages/index.py` を作成
- [ ] `CommonHeader()`, `index()` を移動
- [ ] `reflex_test/pages/todo_page.py` を作成
- [ ] `todo_page()` を移動
- [ ] `reflex_test/pages/__init__.py` に export を追加
- [ ] component, states のインポートを追加

### Step 6: メインファイルの簡潔化
- [ ] `reflex_test/reflex_test.py` から削除したコードを確認
- [ ] 新しいインポート構文に更新
- [ ] `_init_db()` の位置を確定（models/__init__.py か reflex_test.py か）
- [ ] ページ登録ロジックを確認・修正
- [ ] アプリケーション起動テスト

## ファイル配置の詳細

| コード要素 | 配置ファイル | 理由 |
|-----------|-----------|------|
| `DBTodoListItem` | `models/todo.py` | データベースモデルは専用ディレクトリで管理 |
| `StateTodo` | `states/todo.py` | State管理を集約・再利用可能に |
| `todo_page_regist_item()` | `component/todo_page/regist_form.py` | フォームUIはcomponentに属する |
| `todo_page_view_items()` | `component/todo_page/items_view.py` | アイテム表示UIはcomponentに属する |
| `todo_page()` | `pages/todo_page.py` | ページ全体の構成をpagesディレクトリで管理 |
| `index()` | `pages/index.py` | 全ページをpagesに統一 |
| `CommonHeader()` | `pages/index.py` | 共通コンポーネントはpagesに配置 |
| アプリ登録 | `reflex_test.py` | アプリケーションエントリーポイント |
| `_init_db()` | `reflex_test.py` または `models/__init__.py` | DB初期化は起動時に実行 |

## インポート関係

```
reflex_test.py
├── from pages import index, todo_page
├── from states import StateTodo
└── from models import DBTodoListItem (if needed)

pages/todo_page.py
├── from component.todo_page import regist_form, items_view
├── from states import StateTodo
└── from pages import CommonHeader (from index.py)

component/todo_page/regist_form.py
├── from states import StateTodo
└── import reflex as rx

component/todo_page/items_view.py
├── from states import StateTodo
└── import reflex as rx

states/todo.py
├── from models import DBTodoListItem
├── import reflex as rx
└── その他の依存

models/todo.py
└── import reflex as rx
```

## 注意点

1. **Cyclic Import の回避** - インポート関係を注意深く設計
2. **DB初期化の位置** - `_init_db()` をどこに配置するか確定
3. **export の管理** - 各 `__init__.py` で必要な要素を export
4. **既存機能の保証** - リファクタリング後も動作が変わらないこと
5. **段階的テスト** - 各ステップ後にアプリが起動するか確認

## 期待される利点

- ✅ **スケーラビリティ** - 新しいページ/機能の追加が容易
- ✅ **保守性** - 関心の分離が明確
- ✅ **再利用性** - States、Models、Componentsが独立
- ✅ **テスト性** - 各モジュールの単体テストが可能
- ✅ **チーム開発** - 複数人での並行開発がスムーズ
