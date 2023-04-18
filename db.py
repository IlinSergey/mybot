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


def get_or_create_user(db, effective_user, chat_id: int) -> dict:
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


def save_questionnaire(db, user_id: int, questionnaire_data: dict) -> None:
    logging.info("Сохраняем анкету в базу данных")
    user = db.users.find_one({"user_id": user_id})
    questionnaire_data["created"] = datetime.now()
    if "questionnaire" not in user:
        db.users.update_one(
            {"_id": user["_id"]}, {"$set": {"questionnaire": [questionnaire_data]}}
        )
    else:
        db.users.update_one(
            {"_id": user["_id"]}, {"$push": {"questionnaire": [questionnaire_data]}}
        )


def subscribe_user(db, user_data: dict) -> None:
    logging.info("Оформляем подписку в ДБ")
    if not user_data.get("subscribed"):
        db.users.update_one({"_id": user_data["_id"]}, {"$set": {"subscribed": True}})


def unsubscribe_user(db, user_data: dict) -> None:
    logging.info("Удаляем подписку в ДБ")
    db.users.update_one({"_id": user_data["_id"]}, {"$set": {"subscribed": False}})


def get_subscribed(db) -> bool:
    logging.info("Проверяем подписку в ДБ")
    return db.users.find({"subscribed": True})


def save_cat_image_vote(db, user_data: dict, image_name: str, vote: int) -> None:
    logging.info("Сохраняем голос для картинки в ДБ")
    image = db.images.find_one({"image_name": image_name})
    if not image:
        image = {
            "image_name": image_name,
            "votes": [{"user_id": user_data["user_id"], "vote": vote}]
        }
        db.images.insert_one(image)
    elif not user_voted(db, image_name, user_data["user_id"]):
        db.images.update_one(
            {"image_name": image_name},
            {"$push": {"votes": {"user_id": user_data["user_id"], "vote": vote}}}
        )


def user_voted(db, image_name: str, user_id: int) -> bool:
    if db.images.find_one({"image_name": image_name, "votes.user_id": user_id}):
        return True
    return False


def get_image_rating(db, image_name: str) -> int:
    logging.info("Получаем рейтинг картинки")
    rating = db.images.aggregate([
        {
            '$match': {
                'image_name': image_name
            }
        }, {
            '$unwind': {
                'path': '$votes'
            }
        }, {
            '$group': {
                '_id': '$image_name',
                'rating': {
                    '$sum': '$votes.vote'
                }
            }
        }
    ])
    rating = next(rating, None)
    if rating:
        return rating["rating"]
    return 0
