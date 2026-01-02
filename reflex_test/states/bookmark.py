"""Bookmark関連のState管理"""

import reflex as rx
from reflex_test.models import (
    DBBookmarkListItems,
    DBBookmarkCategoryListItems,
)
from reflex_test.services.bookmark import (
    get_bookmark_items as service_get_bookmark_items,
    add_bookmark_item as service_add_bookmark_item,
    remove_bookmark_item as service_remove_bookmark_item,
    get_category_items as service_get_category_items,
    add_category_item as service_add_category_item,
    remove_category_item as service_remove_category_item,
)


class StateBookmark(rx.State):
    """BookmarkページのState定義"""

    textHash: int = 0

    inputStrTitle: str = ""
    inputStrURL: str = ""
    inputStrDescription: str = ""

    selectStrCategoryItem: str = ""
    inputCategoryID: int = 0

    dbitems: list[DBBookmarkListItems] = []
    dbitemnum: int = 0

    dbitemsCategory: list[DBBookmarkCategoryListItems] = []
    dbitemnumCategory: int = 0

    textErrorMessage: str = ""
    isErrorMessageVisible: bool = False

    def init_page(self):
        # print("StateBookmark init_page")
        self.get_bookmark_item()

    def update_inputStrTitle(self, value: str):
        print(f"update_inputStrTitle : {value}")
        self.inputStrTitle = value

    def update_inputStrURL(self, value: str):
        print(f"update_inputStrURL : {value}")
        self.inputStrURL = value
        # URLの先頭にhttp://またはhttps://がない場合、エラーメッセージを表示
        if not (value.startswith("http://") or value.startswith("https://")):
            self.update_textErrorMessage("URL must start with http:// or https://.")

    def update_inputStrDescription(self, value: str):
        print(f"update_inputStrDescription : {value}")
        self.inputStrDescription = value

    def update_selectStrCategoryItem(self, value: str):
        print(f"update_selectStrCategoryItem : {value}")
        self.selectStrCategoryItem = value

        # カテゴリ名からカテゴリIDを取得
        self.inputCategoryID = 0
        for item in self.dbitemsCategory:
            if item.category_name == value:
                self.inputCategoryID = item.id  # type: ignore

    def update_textErrorMessage(self, value: str):
        # print(f"update_textErrorMessage : {value}")
        self.textErrorMessage = value
        self.isErrorMessageVisible = True

    def get_bookmark_item(self):
        self.dbitems, self.dbitemnum = service_get_bookmark_items()
        self.dbitemsCategory, self.dbitemnumCategory = service_get_category_items()

        # dbitemsをcategory_id順にソート
        self.dbitems.sort(key=lambda x: x.category_id)

        # dbitemsCategoryをcategory_name順にソート
        self.dbitemsCategory.sort(key=lambda x: x.category_name)

        # dbitemsCategoryに未分類カテゴリを追加
        self.dbitemsCategory.append(
            DBBookmarkCategoryListItems(id=0, category_name="未分類")  # type: ignore
        )

    def add_bookmark_item(self):
        print("add_bookmark_item")

        # Service層の関数を呼び出す
        success, error_message = service_add_bookmark_item(
            text_hash=self.textHash,
            title=self.inputStrTitle,
            url=self.inputStrURL,
            description=self.inputStrDescription,
            category_id=self.inputCategoryID,
        )

        if not success:
            self.update_textErrorMessage(error_message)
            return

        self.clear_inputs()
        self.get_bookmark_item()

    def remove_bookmark_item(self, item_id: str):
        print("remove_bookmark_item")
        success, error_message = service_remove_bookmark_item(item_id)

        if not success:
            self.update_textErrorMessage(error_message)
            return

        self.get_bookmark_item()

    def update_item(self, item: DBBookmarkListItems):
        print("update_item")
        print("item:", item)
        self.textHash = item.id  # type: ignore
        self.inputStrTitle = item.title
        self.inputStrURL = item.url
        self.inputStrDescription = item.description
        self.inputCategoryID = item.category_id
        self.selectStrCategoryItem = "" # TODO :カテゴリidからカテゴリ名を取得
        for item in self.dbitemsCategory: # type: ignore
            if self.inputCategoryID == item.id:
                self.selectStrCategoryItem = item.category_name  # type: ignore

    def clear_inputs(self):
        self.textHash = 0
        self.inputStrTitle = ""
        self.inputStrURL = ""
        self.inputStrDescription = ""
        self.selectStrCategoryItem = ""
        self.inputCategoryID = 0
        self.isErrorMessageVisible = False


class StateBookmarkCategory(rx.State):

    textHash: int = 0
    inputStrCategoryName: str = ""

    dbitems: list[DBBookmarkCategoryListItems] = []
    dbitemnum: int = 0

    listCategoryItems: list[str] = []

    textErrorMessage: str = ""
    isErrorMessageVisible: bool = False

    has_category_items: bool = False

    def init_page(self):
        # print("StateBookmark init_page")
        self.get_category_item()

    def update_inputStrCategoryName(self, value: str):
        # print(f"update_inputStrCategoryName : {value}")
        self.inputStrCategoryName = value
        self.get_category_item()

    def get_category_item(self):
        self.dbitems, self.dbitemnum = service_get_category_items()
        self.listCategoryItems = []
        if len(self.dbitems) == 0:
            self.listCategoryItems = ["N/A"]
            self.has_category_items = False
            return

        for item in self.dbitems:
            if item.category_name != "":
                # print(f"category_item: {item.category_name}")
                self.listCategoryItems.append(item.category_name)
        self.has_category_items = True

        # dbitemsCategoryに未分類カテゴリを追加
        self.listCategoryItems.append("=== 未分類 ===")

    def add_category_item(self):
        print("add_category_item")
        success, error_message = service_add_category_item(
            text_hash=self.textHash,
            category_name=self.inputStrCategoryName,
        )

        if not success:
            self.update_textErrorMessage(error_message)
            return

        self.clear_inputs()
        self.get_category_item()

    def remove_category_item(self, item_id: str):
        print("remove_category_item")
        success, error_message = service_remove_category_item(item_id)

        if not success:
            self.update_textErrorMessage(error_message)
            return

        self.get_category_item()

    def clear_inputs(self):
        self.textHash = 0
        self.inputStrCategoryName = ""
        self.isErrorMessageVisible = False

    def update_textErrorMessage(self, value: str):
        # print(f"update_textErrorMessage : {value}")
        self.textErrorMessage = value
        self.isErrorMessageVisible = True
