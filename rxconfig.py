import reflex as rx

config = rx.Config(
    app_name="reflex_test",
    db_url="sqlite:///reflex.db", # ここで保存先とファイル名が定義されています
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)