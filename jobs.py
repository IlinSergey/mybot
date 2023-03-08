from telegram.ext import CallbackContext
from datetime import datetime
from db import db, get_subscribed
from telegram.error import BadRequest


async def send_updates(context: CallbackContext) -> None:
    now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    for user in get_subscribed(db):
        try:
            await context.bot.send_message(
                chat_id=user["chat_id"], text=f"Точное время {now}"
            )
        except BadRequest:
            print(f"Чат {user['chat_id']} не найден.")
