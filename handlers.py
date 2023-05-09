import logging
import os
from glob import glob
from random import choice

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from db import (db, get_or_create_user, subscribe_user, unsubscribe_user,
                save_cat_image_vote, user_voted, get_image_rating)
from jobs import alarm
from utils import (find_constellation, get_bot_number, has_object_on_image, main_keyboard,
                   play_random_number, cat_rating_inline_keyboard)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="bot.log",
    level=logging.INFO,
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("Вызвана команда /start")
    user = get_or_create_user(db, update.effective_user, update.message.chat_id)
    smile = user["emoji"]
    await update.message.reply_text(
        f"Привет {update.effective_user.first_name}{smile}",
        reply_markup=main_keyboard(),
    )


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("Вызвана команда /echo")
    user = get_or_create_user(db, update.effective_user, update.message.chat_id)
    smile = user["emoji"]
    await update.message.reply_text(
        f"{update.message.text}{smile}", reply_markup=main_keyboard()
    )


async def planet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("Вызвана команда /planet")
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
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выберите планету:", reply_markup=reply_markup)


async def take_constellation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("Вызвана команда /take_constellation")
    query = update.callback_query
    await query.answer()
    constellation = find_constellation(query.data)
    await query.edit_message_text(
        text=f"Сегодня планета {query.data} в созвездии {constellation}"
    )


async def guess_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("Вызвана команда /guess_number")
    if context.args:
        try:
            user_number = int(context.args[0])
            bot_number = get_bot_number(user_number)
            message = play_random_number(user_number, bot_number)
        except (TypeError, ValueError):
            message = "Введите целое число"
    else:
        message = "Введите число"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)


async def send_cat_picture(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("Вызвана команда /send_cat_picture")
    user = get_or_create_user(db, update.effective_user, update.message.chat_id)
    cat_pictures_list = glob("images/cat*.jp*g")
    cat_picture_filename = choice(cat_pictures_list)
    if user_voted(db, cat_picture_filename, user["user_id"]):
        rating = get_image_rating(db, cat_picture_filename)
        keyboard = None
        caption = f"Рейтинг картинки: {rating}"
    else:
        keyboard = cat_rating_inline_keyboard(cat_picture_filename)
        caption = None

    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=open(cat_picture_filename, mode="rb"),
        reply_markup=keyboard,
        caption=caption
    )


async def user_coordinates(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("Присланы координаты пользователя")
    user = get_or_create_user(db, update.effective_user, update.message.chat_id)
    coords = update.message.location
    await update.message.reply_text(
        f"Ваши координаты: широта = {coords.latitude} долгота = {coords.longitude}, \
                                    {user['emoji']}!",
        reply_markup=main_keyboard(),
    )


async def check_user_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Проверяем присланное фото, если на фото присутствует нужный обьект (по умолчанию 'cat')
    - сохраняем фото в библиотеку
    """
    logging.info("Прислана фотография, обрабатываем")
    await update.message.reply_text("Обрабатываем фото...")
    photo_file_from_messsage = await context.bot.get_file(
        update.message.photo[-1].file_id
    )
    if has_object_on_image(photo_file_from_messsage["file_path"], "cat"):
        await update.message.reply_text("Обнаружен котик, сохраняю в библиотеку")
        file_name = os.path.join(
            "images", f"cat_{photo_file_from_messsage.file_id}.jpg"
        )
        await photo_file_from_messsage.download_to_drive(file_name)
    else:
        await update.message.reply_text("Котик не обнаружен!")


async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("Вызвана комманда оформления подписки")
    user = get_or_create_user(db, update.effective_user, update.message.chat_id)
    subscribe_user(db, user)
    await update.message.reply_text("Вы успешно подписались!")


async def unsubscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("Вызвана комманда удаления подписки")
    user = get_or_create_user(db, update.effective_user, update.message.chat_id)
    unsubscribe_user(db, user)
    await update.message.reply_text("Вы успешно отписались!")


async def set_alarm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("Вызвана комманда /alarm")
    try:
        alarm_seconds = abs(int(context.args[0]))
        context.job_queue.run_once(alarm, alarm_seconds, chat_id=update.message.chat.id)
        await update.message.reply_text(f"Уведомление через {alarm_seconds} секунд")
    except (ValueError, TypeError):
        await update.message.reply_text("Введите целое число секунд после команды")


async def cat_picture_rating(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("Вызвана комманда рейтинг картинки")
    query = update.callback_query
    await query.answer()
    callback_type, image_name, vote = update.callback_query.data.split("|")
    vote = int(vote)
    user = get_or_create_user(db, update.effective_user, update.effective_chat.id)
    save_cat_image_vote(db, user, image_name, vote)
    rating = get_image_rating(db, image_name)
    await update.callback_query.edit_message_caption(caption=f"Рейтинг картинки: {rating}")
