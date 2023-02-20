from glob import glob
from random import choice
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from utils import find_constellation, play_random_number


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


async def take_constellation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    constellation = find_constellation(query.data)
    await query.edit_message_text(text=f"Сегодня планета {query.data} в созвездии {constellation}")


async def guess_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(context.args)
    if context.args:
        try:
            user_number = int(context.args[0])
            message = play_random_number(user_number)
        except (TypeError, ValueError):
            message = "Введите целое число"
    else:
        message = "Введите число"
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=message)


async def send_cat_picture(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cat_pictures_list = glob("images/cat*.jp*g")
    cat_picture_filename = choice(cat_pictures_list)
    await context.bot.send_photo(chat_id=update.effective_chat.id,
                                   photo=open(cat_picture_filename, mode="rb"))
