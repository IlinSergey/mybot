import logging
from datetime import datetime
from random import randint

import ephem
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2
from telegram import KeyboardButton, ReplyKeyboardMarkup

from config import CLARYFAI_API_KEY, CLARYFAI_MODEL_ID_VERSION

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="bot.log",
    level=logging.INFO,
)


def find_constellation(planet: str) -> tuple:
    now = datetime.now()
    date = f"{now.year}/{now.month}/{now.day}"
    planets = {
        "Mercury": ephem.Mercury(date),
        "Venus": ephem.Venus(date),
        "Mars": ephem.Mars(date),
        "Jupiter": ephem.Jupiter(date),
        "Saturn": ephem.Saturn(date),
        "Uranus": ephem.Uranus(date),
        "Neptune": ephem.Neptune(date),
        "Pluto": ephem.Pluto(date),
    }
    planet_query = planets[planet]
    constellation = ephem.constellation(planet_query)
    return constellation


def play_random_number(user_number: int) -> str:
    bot_number = randint(user_number - 10, user_number + 10)
    if bot_number < user_number:
        message = f"Ваше число {user_number}, мое число {bot_number}. Вы выиграли!"
    elif bot_number > user_number:
        message = f"Ваше число {user_number}, мое число {bot_number}. Я выиграл!"
    else:
        message = f"Ваше число {user_number}, мое число {bot_number}. Ничья!"
    return message


def main_keyboard():
    return ReplyKeyboardMarkup(
        [
            [
                "Прислать котика",
                KeyboardButton("Мои координаты", request_location=True),
                "Заполнить анкету",
            ]
        ],
        resize_keyboard=True,
    )


def has_object_on_image(file_name: str, object_name: str) -> bool:
    """
    Функция, при помощи сервиса 'Clarifai', проверяет наличие обьекта 'object_name'
    на изображении 'file_name'. При вероятности наличия обьекта на изображении >= 90%
    возвращает 'True', иначе 'False'.
    """
    logging.info("Отправляем фото в Clarifai")
    channel = ClarifaiChannel.get_grpc_channel()
    app = service_pb2_grpc.V2Stub(channel)
    metadata = (("authorization", f"Key {CLARYFAI_API_KEY}"),)

    request = service_pb2.PostModelOutputsRequest(
        model_id=CLARYFAI_MODEL_ID_VERSION["default"],
        inputs=[
            resources_pb2.Input(
                data=resources_pb2.Data(image=resources_pb2.Image(url=file_name))
            )
        ],
    )
    response = app.PostModelOutputs(request, metadata=metadata)
    return check_response_for_object(response, object_name)


def check_response_for_object(response, object_name: str) -> bool:
    if response.status.code == status_code_pb2.SUCCESS:
        for concept in response.outputs[0].data.concepts:
            if concept.name == object_name and concept.value >= 0.90:
                return True
    else:
        print(f"Ошибка распознования картинки {response.ouputs[0].status.datails}")
    return False
