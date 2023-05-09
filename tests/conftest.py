
import pytest
from telegram import User


@pytest.fixture
def effective_user():
    return User(id=123, first_name="Билли", is_bot=False, last_name="Бонс", username="best_pirat")
