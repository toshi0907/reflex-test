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