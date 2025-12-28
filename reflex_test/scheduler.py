"""
定期実行タスクのスケジューラモジュール

使い方:
1. タスク定義時に @register_task デコレータを使う
2. 登録されたタスクが自動的に1分ごとに実行される
"""

import os
from typing import Callable, List
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from zoneinfo import ZoneInfo

_scheduler_registered_tasks: List[Callable] = []  # 登録されたタスクのリスト
_scheduler: BackgroundScheduler | None = None
_started = False  # スケジューラが起動済みかどうかのフラグ


def register_task(func: Callable):
    """
    定期実行タスクを登録するデコレータ

    使用例:
        @register_task
        def my_task():
            print("定期実行されるタスク")
    """
    _scheduler_registered_tasks.append(func)
    # print(f"[scheduler] registered task: {func.__name__}")
    func()
    return func


def _ensure_scheduler():
    """スケジューラのインスタンスを取得または作成"""
    global _scheduler
    if _scheduler is None:
        _scheduler = BackgroundScheduler(timezone="Asia/Tokyo")
    return _scheduler


def start_scheduler():
    """
    スケジューラを起動し、登録されたタスクを1分間隔でスケジュール
    重複起動を防ぐため、既存ジョブは置換される
    """
    global _started
    if _started:
        print("[scheduler] already started, skipping")
        return

    if not _scheduler_registered_tasks:
        print("[scheduler] no tasks registered, skipping")
        return

    sched = _ensure_scheduler()

    # 既存ジョブを置換し、重複起動を避ける
    for func in _scheduler_registered_tasks:
        job_id = f"task:{func.__name__}"
        sched.add_job(
            func,
            "interval",  # 間隔実行
            minutes=1,  # 1分ごとに実行
            id=job_id,  # ジョブID
            replace_existing=True,  # 既存ジョブを置換
            coalesce=True,  # 遅延した実行をまとめる
            max_instances=1,  # 同時実行を1つに制限
            misfire_grace_time=30,  # 30秒以内の遅延は許容
        )
        # func()
        print(f"[scheduler] scheduled task: {func.__name__}")

    sched.start()
    _started = True
    print(f"[scheduler] started with {len(_scheduler_registered_tasks)} task(s)")


def scheduler_autostart():
    """
    スケジューラの起動
    """
    # タスクモジュールをインポートして登録を実行
    start_scheduler()


### サンプルタスク定義 ###


@register_task
def sample_task():
    """
    サンプルタスク - 1分ごとに現在時刻を出力
    実際の用途例:
    - データベースのクリーンアップ
    - 外部APIからのデータ取得
    - 定期レポート生成
    """
    _now = datetime.now(ZoneInfo("Asia/Tokyo")).strftime("%Y-%m-%d %H:%M:%S")
    print(f"[scheduler:sample_task] tick at {_now}Z")


@register_task
def health_check_task():
    """
    ヘルスチェックタスク - スケジューラが正常動作していることを確認
    """
    _now = datetime.now(ZoneInfo("Asia/Tokyo")).strftime("%Y-%m-%d %H:%M:%S")
    print(f"[scheduler:health_check] scheduler is running at {_now}Z")


@register_task
def check_task_fire():
    """
    タスク実行確認用タスク - スケジューラがタスクを実行していることを確認
    """
    _now = datetime.now(ZoneInfo("Asia/Tokyo"))
    print(f"[scheduler:check_task_fire] task fired at {_now}Z")

    from reflex_test.services.todo import (
        get_todo_items as service_get_todo_items,
        add_todo_item as service_add_todo_item,
        remove_todo_item as service_remove_todo_item,
    )
    from reflex_test.models import DBTodoListItem

    dbitems: list[DBTodoListItem] = []
    dbitemnum: int = 0
    dbitems, dbitemnum = service_get_todo_items()
    for item in dbitems:
        _title = item.title
        _url = item.url
        _dt_str = item.datetime
        _is_webhook = item.notify_webhook
        _is_email = item.notify_email
        _is_fire = False
        _dt = datetime.now(ZoneInfo("Asia/Tokyo"))
        try:
            _dt = datetime.strptime(_dt_str, "%Y-%m-%dT%H:%M").replace(
                tzinfo=ZoneInfo("Asia/Tokyo")
            )
            _fire = "       "
            if _dt < _now:
                _is_fire = True
                _fire = "FIRE!!!"
        except Exception as e:
            _fire = "ERROR!!"
        print(f"{_fire}[{_is_fire}] {_title} (datetime={_dt_str} / {_dt})")

        if _is_fire:
            if _is_webhook:
                from reflex_test.component.send_webhook import SendWebhook

                SendWebhook().send_notification(f"[TNR] {_title}", _url, "")
                print(f"  -> Notify Webhook for {_title}")
            if _is_email:
                from reflex_test.component.send_email import SendEmail

                SendEmail().send_notification(f"[TNR] {_title}", _url, "")
                print(f"  -> Notify Email for {_title}")

            service_remove_todo_item(str(item.id))  # Fireしたら削除
