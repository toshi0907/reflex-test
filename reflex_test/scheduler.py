"""
定期実行タスクのスケジューラモジュール

使い方:
1. タスク定義時に @register_task デコレータを使う
2. 登録されたタスクが自動的に1分ごとに実行される
"""

import os
from typing import Callable, List
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from zoneinfo import ZoneInfo

_scheduler_registered_tasks: List[Callable] = []  # 登録されたタスクのリスト
_scheduler: AsyncIOScheduler | None = None
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
    print(f"[scheduler] registered task: {func.__name__}")
    return func


def _ensure_scheduler():
    """スケジューラのインスタンスを取得または作成"""
    global _scheduler
    if _scheduler is None:
        _scheduler = AsyncIOScheduler(timezone="Asia/Tokyo")
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
