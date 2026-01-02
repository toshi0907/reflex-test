# https://timesaving.hatenablog.com/entry/2025/03/29/150000

# SQLAlchemy

```python
import reflex as rx

class User(rx.Model, table=True):
    """データベースのテーブル定義"""
    name: str
    age: int

class UserState(rx.State):
    def add_user(self):
        with rx.session() as session:
            # クラスとしてデータを扱う
            new_user = User(name="Jiro", age=30)
            session.add(new_user)
            session.commit()
```

# 公式（？）ドキュメント
https://reflex.dev/docs/library/

# requirements.txtの更新

```bash
pip freeze > requirements.txt
```

# API curl

```bash
curl localhost:8000/api/bookmark/list
curl localhost:8000/api/todo/list
curl localhost:8000/api/bookmark/category/list
```

```bash
curl -X POST -H "Content-Type: application/json" -d '{"name":"apitest"}' localhost:8000/api/bookmark/category/add
curl -X POST -H "Content-Type: application/json" -d '{"id":0, "title":"api1", "url":"http://abc.com", "description": "", "category_id":0}' localhost:8000/api/bookmark/add
curl -X POST -H "Content-Type: application/json" -d '{"id":0, "title":"api1", "url":"http://abc.com", "description": "", "category_id":0}' localhost:8000/api/todo/add
```
