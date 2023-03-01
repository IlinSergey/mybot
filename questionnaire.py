import logging
from telegram import ReplyKeyboardRemove, Update, ReplyKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, ConversationHandler
from utils import main_keyboard

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="bot.log",
    level=logging.INFO,
)


async def questionnaire_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("Вызвана команда 'Заполнить анкету'")
    await update.message.reply_text(
        "Привет, как вас зовут? (Имя и Фамилия)", reply_markup=ReplyKeyboardRemove()
    )
    return "name"


async def questionnaire_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("Вызван запрос Имени")
    user_name = update.message.text
    if len(user_name.split()) < 2:
        await update.message.reply_text("Пожалуйста введите имя и фамилию!")
        return "name"
    else:
        context.user_data["questionnaire"] = {"name": user_name}
        reply_keyboard = [["1", "2", "3", "4", "5"]]
        await update.message.reply_text(
            "Пожалуйста оцените нашего бота от 1 до 5",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, resize_keyboard=True
            ),
        )
        return "rating"


async def questionnaire_rating(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("Вызван запрос рейтинга")
    context.user_data["questionnaire"]["rating"] = int(update.message.text)
    await update.message.reply_text(
        "Напишите комментарий, или нажмите /skip чтобы пропустить"
    )
    return "comment"


async def questionnaire_comment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("Вызван запрос комментария")
    context.user_data["questionnaire"]["comment"] = update.message.text
    user_text = format_questionnaire(context.user_data["questionnaire"])
    await update.message.reply_text(
        user_text, reply_markup=main_keyboard(), parse_mode=ParseMode.HTML
    )
    return ConversationHandler.END


async def questionnaire_skip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("Вызвана команда 'пропустить комментарий'")
    user_text = format_questionnaire(context.user_data["questionnaire"])
    await update.message.reply_text(
        user_text, reply_markup=main_keyboard(), parse_mode=ParseMode.HTML
    )
    return ConversationHandler.END


def format_questionnaire(questionnaire):
    user_text = f"""<b> Имя Фамилия</b>: {questionnaire["name"]}
<b>Оценка</b>: {questionnaire["rating"]}"""
    if "comment" in questionnaire:
        user_text += f'\n<b>Комментарий</b>: {questionnaire["comment"]}'
    return user_text


async def questionnaire_dontknow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Я вас не понимаю")
