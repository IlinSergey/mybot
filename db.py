import logging
from datetime import datetime
from random import choice

from emoji import emojize
from pymongo import MongoClient

import config

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="bot.log",
    level=logging.INFO,
)


client = MongoClient(config.MONGO_LINK)

db = client[config.MONGO_DB]


def get_or_create_user(db, effective_user, chat_id) -> dict:
    logging.info("Проверяем наличие пользователя в базе данных")
    user = db.users.find_one({"user_id": effective_user.id})
    if not user:
        logging.info("Записываем данные о пользователе в базу данных")
        user = {
            "user_id": effective_user.id,
            "first_name": effective_user.first_name,
            "last_name": effective_user.last_name,
            "username": effective_user.username,
            "chat_id": chat_id,
            "emoji": emojize(choice(config.USER_EMOJI), language="alias"),
        }
        db.users.insert_one(user)
    return user


def save_questionnaire(db, user_id, questionnaire_data):
    logging.info("Сохраняем анкету в базу данных")
    user = db.users.find_one({"user_id": user_id})
    questionnaire_data["created"] = datetime.now()
    if "questionnaire" not in user:
        db.users.update_one(
            {"_id": user["_id"]},
            {"$set": {"questionnaire": [questionnaire_data]}}
        )
    else:
        db.users.update_one(
            {"_id": user["_id"]},
            {"$push": {"questionnaire": [questionnaire_data]}}
        )
