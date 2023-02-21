from emoji import emojize
import ephem
from datetime import datetime
from random import randint, choice
from config import USER_EMOJI


def get_smile(user_data: dict):
    if "emoji" not in user_data:
        smile = choice(USER_EMOJI)
        return emojize(smile, language='alias')
    return user_data["emoji"]


def find_constellation(planet: str) -> tuple:
    now = datetime.now()
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


def play_random_number(user_number: int) -> str:
    bot_number = randint(user_number - 10, user_number + 10)
    if bot_number < user_number:
        message = f"Ваше число {user_number}, мое число {bot_number}. Вы выиграли!"
    elif bot_number > user_number:
        message = f"Ваше число {user_number}, мое число {bot_number}. Я выиграл!"
    else:
        message = f"Ваше число {user_number}, мое число {bot_number}. Ничья!"
    return message
