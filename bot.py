import logging
import datetime

import ephem
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, \
    MessageHandler, CallbackQueryHandler, filters

from config import TG_API_KEY


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="bot.log",
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Я бот, поговори со мной!")


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=f"Привет {update.effective_user.first_name}")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=update.message.text)


async def planet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("Меркурий", callback_data="Mercury"),
            InlineKeyboardButton("Венера", callback_data="Venus"),
            InlineKeyboardButton("Марс", callback_data="Mars"),
            InlineKeyboardButton("Юпитер", callback_data="Jupiter"),
            ],
        [
            InlineKeyboardButton("Сатурн", callback_data="Saturn"),
            InlineKeyboardButton("Уран", callback_data="Uranus"),
            InlineKeyboardButton("Нептун", callback_data="Neptune"),
            InlineKeyboardButton("Плутон", callback_data="Pluto"),
            ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выберите планету:", reply_markup=reply_markup)


def find_constellation(planet: str) -> tuple:
    now = datetime.datetime.now()
    date = f"{now.year}/{now.month}/{now.day}"
    planet_query = None
    if planet == "Mercury":
        planet_query = ephem.Mercury(date)
    elif planet == "Venus":
        planet_query = ephem.Venus(date)
    elif planet == "Mars":
        planet_query = ephem.Mars(date)
    elif planet == "Jupiter":
        planet_query = ephem.Jupiter(date)
    elif planet == "Saturn":
        planet_query = ephem.Saturn(date)
    elif planet == "Uranus":
        planet_query = ephem.Uranus(date)
    elif planet == "Neptune":
        planet_query = ephem.Neptune(date)
    elif planet == "Pluto":
        planet_query = ephem.Pluto(date)
    constellation = ephem.constellation(planet_query)
    return constellation


async def take_constellation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    constellation = find_constellation(query.data)
    await query.edit_message_text(text=f"Сегодня планета {query.data} в созвездии {constellation}")


def main():
    mybot = ApplicationBuilder().token(TG_API_KEY).build()

    start_handler = CommandHandler("start", start)
    hello_handler = CommandHandler("hello", hello)
    planet_handler = CommandHandler("planet", planet)
    take_constellation_handler = CallbackQueryHandler(take_constellation)
    talk_to_me_handler = MessageHandler(filters.TEXT, echo)

    logging.info("Бот стартовал")

    mybot.add_handler(start_handler)
    mybot.add_handler(hello_handler)
    mybot.add_handler(planet_handler)
    mybot.add_handler(take_constellation_handler)
    mybot.add_handler(talk_to_me_handler)

    mybot.run_polling()


if __name__ == "__main__":
    main()
