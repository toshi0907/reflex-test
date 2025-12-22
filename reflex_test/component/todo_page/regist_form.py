"""Todo登録フォームコンポーネント"""

import reflex as rx
from reflex_test.states import StateTodo


def todo_page_regist_item() -> rx.Component:
    """Todoアイテム登録フォーム"""
    return (
        rx.vstack(
            rx.heading("Add Item", as_="h2"),
            rx.vstack(
                rx.text(f"ID[{StateTodo.textHash}]"),
                rx.input(
                    value=StateTodo.inputStrTitle,
                    on_change=StateTodo.update_inputStrTitle,
                    placeholder="Enter Item Title",
                    width="100%",
                    minwidth="300px",
                ),
                rx.input(
                    value=StateTodo.inputStrURL,
                    on_change=StateTodo.update_inputStrURL,
                    placeholder="Enter URL",
                    width="100%",
                    minwidth="300px",
                ),
                rx.input(
                    value=StateTodo.inputdatetime,
                    on_change=StateTodo.update_inputdatetime,
                    placeholder="Select Date and Time",
                    type="datetime-local",
                ),
                rx.hstack(
                    rx.text("Notify", width="100px", margin_left="20px"),
                    rx.checkbox(
                        "Webhook",
                        checked=StateTodo.checkBoxNotifyWebhook,
                        on_change=StateTodo.update_checkBoxNotifyWebhook,
                    ),
                    rx.checkbox(
                        "Email",
                        checked=StateTodo.checkBoxNotifyEmail,
                        on_change=StateTodo.update_checkBoxNotifyEmail,
                    ),
                    rx.text("Repeat", width="100px", margin_left="20px"),
                    rx.checkbox(
                        "Daily",
                        checked=StateTodo.checkBoxRepeatDayly,
                        on_change=StateTodo.update_checkBoxRepeatDayly,
                    ),
                    rx.checkbox(
                        "Weekly",
                        checked=StateTodo.checkBoxRepeatWeekly,
                        on_change=StateTodo.update_checkBoxRepeatWeekly,
                    ),
                    rx.checkbox(
                        "Monthly",
                        checked=StateTodo.checkBoxRepeatMonthly,
                        on_change=StateTodo.update_checkBoxRepeatMonthly,
                    ),
                ),
                rx.hstack(
                    rx.button(
                        "Add Item",
                        on_click=lambda: StateTodo.add_todo_item(),
                    ),
                    rx.button(
                        "Clear",
                        on_click=lambda: StateTodo.clear_inputs(),
                    ),
                    width="100%",
                ),
                rx.cond(
                    StateTodo.isErrorMessageVisible,
                    rx.text(
                        StateTodo.textErrorMessage,
                        color="red",
                    ),
                ),
                minwidth="300px",
                width="100%",
            ),
        ),
    )
