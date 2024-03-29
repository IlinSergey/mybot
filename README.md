# MyBot 

Mybot - это учебный бот для Telegram, развлекательного характера.

## Установка

1. Клонируйте репозиторий с github
2. Создайте виртуальное окружение
3. Установите зависимости `pip install requirements.txt`
(Для использования функций планировщика нужно дополнительно установить модуль JobQueue командой `pip install 'python-telegram-bot[job-queue]'`)
4. Создайте файл `config.py`
5. Впишите в `config.py` переменные:
```
TG_API_KEY = "API ключ бота, полученный в BotFather"
USER_EMOJI = [
    ":smile:",  ":stuck_out_tongue_closed_eyes:", ":grimacing:", ":cat:",
    ":dog:", ":mouse:", ":rabbit:", ":bear:",
]

```
В сисок USER_EMOJI можно добавить любые emoji на ваше усмотрение. Например, с сайта https://www.webfx.com/tools/emoji-cheat-sheet/

6. Запустите бота командой `python bot.py`

### Функционал бота
1. `/start` Начать работу с ботом.
2. `/planet` Выбрать планету и узнать в каком созвездии она расположена на текущий момент.
3. `/cat` или `Прислать котика` Получить картинку с котиками.
4. `/guess {число}` Бот возьмет рандомное число из диапазона +10 и -10 от вашего числа и если ваше число
окажется больше, то вы победили, если меньше - вы проиграли.
5. Если отправить боту фото, он с помощью ИИ определит есть ли на фото котик, 
если есть, то добавит фото в свою библиотеку.
6. На произвольные сообщения бот возвращает текст сообщения.
7. `/subscribe` оформить подписку (при оформлении подписки, будет присылаться точное время (см. п.10))
8. `/unsubscribe` отписаться
9. `/alarm {sec}` где sec - количество секунд, через которые сработает таймер (бот пришлет сообщение с текстом 'сработал таймер')
10. При подписке бот присылает точное время (по умолчанию в 12:00 (Московское время) по будням. Корректируется в bot.py в переменных `target_time` и `target_days`)

![Меню](https://github.com/IlinSergey/mybot/blob/master/photo_for_readme/menu.png)
![Проверка фото](https://github.com/IlinSergey/mybot/blob/master/photo_for_readme/check_dog.png)
![Проверка фото](https://github.com/IlinSergey/mybot/blob/master/photo_for_readme/check_cat.png)
![Команда "Прислать котика"](https://github.com/IlinSergey/mybot/blob/master/photo_for_readme/send_cat.png)
