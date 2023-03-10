from datetime import datetime

from telegram.error import BadRequest
from telegram.ext import CallbackContext, ContextTypes

from db import db, get_subscribed


async def send_updates(context: CallbackContext) -> None:
    now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    for user in get_subscribed(db):
        try:
            await context.bot.send_message(
                chat_id=user["chat_id"], text=f"Точное время {now}"
            )
        except BadRequest:
            print(f"Чат {user['chat_id']} не найден.")


async def alarm(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=context._chat_id, text="Сработал таймер")
