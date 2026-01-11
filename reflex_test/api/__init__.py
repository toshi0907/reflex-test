"""API エンドポイントの初期化"""

from fastapi import FastAPI
from reflex_test.api.bookmark import *
from reflex_test.api.todo import *
from reflex_test.api.phone import *


def create_api_app() -> FastAPI:
    """FastAPIアプリを作成し、ルートを登録"""
    app = FastAPI(title="TNApp API")

    ### /api/todo/list
    app.add_api_route("/api/todo/list", api_get_todos, methods=["GET"])

    ### /api/todo/add
    app.add_api_route("/api/todo/add", api_add_todo, methods=["POST"])

    ### /api/bookmark/list
    app.add_api_route("/api/bookmark/list", api_get_bookmarks, methods=["GET"])

    ### /api/bookmark/add
    app.add_api_route("/api/bookmark/add", api_add_bookmark, methods=["POST"])

    ### /api/bookmark/category/list
    app.add_api_route(
        "/api/bookmark/category/list", api_get_categories, methods=["GET"]
    )

    ### /api/bookmark/category/add
    app.add_api_route(
        "/api/bookmark/category/add", api_add_category_item, methods=["POST"]
    )

    ### /api/phone/add
    app.add_api_route("/api/phone/add", api_add_phone_info, methods=["POST"])

    return app
