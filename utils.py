import ephem
from datetime import datetime


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