import logging
from glob import glob
import os
from random import choice

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from utils import find_constellation, get_smile, play_random_number, main_keyboard, has_object_on_image

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="bot.log",
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("Вызвана команда /start")
    context.user_data["emoji"] = get_smile(context.user_data)
    smile = context.user_data["emoji"]    
    await update.message.reply_text(f"Я бот{smile}, поговори со мной!",
                                     reply_markup=main_keyboard())    


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("Вызвана команда /hello")
    context.user_data["emoji"] = get_smile(context.user_data)
    smile = context.user_data["emoji"]
    await update.message.reply_text(f"Привет {update.effective_user.first_name}{smile}",
                                     reply_markup=main_keyboard())      
   

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("Вызвана команда /echo")
    context.user_data["emoji"] = get_smile(context.user_data)
    smile = context.user_data["emoji"]
    await update.message.reply_text(f"{update.message.text}{smile}",
                                     reply_markup=main_keyboard())


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
            ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выберите планету:", reply_markup=reply_markup)


async def take_constellation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("Вызвана команда /take_constellation")
    query = update.callback_query
    await query.answer()
    constellation = find_constellation(query.data)
    await query.edit_message_text(text=f"Сегодня планета {query.data} в созвездии {constellation}")


async def guess_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("Вызвана команда /guess_number")
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
    logging.info("Вызвана команда /send_cat_picture")
    cat_pictures_list = glob("images/cat*.jp*g")
    cat_picture_filename = choice(cat_pictures_list)
    await context.bot.send_photo(chat_id=update.effective_chat.id,
                                   photo=open(cat_picture_filename, mode="rb"), 
                                   reply_markup=main_keyboard())


async def user_coordinates(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("Присланы координаты пользователя")
    context.user_data["emoji"] = get_smile(context.user_data)
    coords = update.message.location  
    await update.message.reply_text(f"Ваши координаты: широта = {coords.latitude} долгота = {coords.longitude}, \
                                    {context.user_data['emoji']}!", reply_markup=main_keyboard())
    

async def check_user_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Обрабатываем фото")
    os.makedirs("downloads", exist_ok=True)
    photo_file = await context.bot.get_file(update.message.photo[-1].file_id)    
    file_name = os.path.join("downloads", f"{update.message.photo[-1].file_id}.jpg")    
    await photo_file.download_to_drive(file_name)    
    if has_object_on_image(file_name, "cat"):
        await update.message.reply_text("Обнаружен котик, сохраняю в библиотеку")
        new_file_name = os.path.join("images", f"cat_{photo_file.file_id}.jpg")
        os.rename(file_name, new_file_name)
    else:
        os.remove(file_name)
        await update.message.reply_text("Котик не обнаружен!")
