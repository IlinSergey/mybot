import logging
from datetime import time

import pytz
from telegram.ext import (ApplicationBuilder, CallbackQueryHandler,
                          CommandHandler, ConversationHandler, MessageHandler,
                          filters)

from config import TG_API_KEY
from handlers import (check_user_photo, echo, guess_number, planet,
                      send_cat_picture, set_alarm, start, subscribe,
                      take_constellation, unsubscribe, user_coordinates)
from jobs import send_updates
from questionnaire import (questionnaire_comment, questionnaire_dontknow,
                           questionnaire_name, questionnaire_rating,
                           questionnaire_skip, questionnaire_start)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="bot.log",
    level=logging.INFO,
)


def main():
    mybot = ApplicationBuilder().token(TG_API_KEY).build()
    logging.info("Бот стартовал")

    jq = mybot.job_queue
    target_time = time(12, 0, tzinfo=pytz.timezone("Europe/Moscow"))
    target_days = (
        1,
        2,
        3,
        4,
        5,
    )  # 0-6 correspond to sunday - saturday). By default, the job will run every day.
    jq.run_daily(send_updates, target_time, target_days)

    questionnaire = ConversationHandler(
        entry_points=[
            MessageHandler(filters.Regex("^(Заполнить анкету)$"), questionnaire_start)
        ],
        states={
            "name": [MessageHandler(filters.TEXT, questionnaire_name)],
            "rating": [
                MessageHandler(filters.Regex("^(1|2|3|4|5)$"), questionnaire_rating)
            ],
            "comment": [
                CommandHandler("skip", questionnaire_skip),
                MessageHandler(filters.TEXT, questionnaire_comment),
            ],
        },
        fallbacks=[
            MessageHandler(
                filters.TEXT
                | filters.PHOTO
                | filters.VIDEO
                | filters.Document.ALL
                | filters.LOCATION,
                questionnaire_dontknow,
            )
        ],
    )

    mybot.add_handler(questionnaire)
    mybot.add_handler(CommandHandler("start", start))
    mybot.add_handler(CommandHandler("planet", planet))
    mybot.add_handler(CommandHandler("guess", guess_number))
    mybot.add_handler(CommandHandler("cat", send_cat_picture))
    mybot.add_handler(CommandHandler("subscribe", subscribe))
    mybot.add_handler(CommandHandler("unsubscribe", unsubscribe))
    mybot.add_handler(CommandHandler("alarm", set_alarm))
    mybot.add_handler(
        MessageHandler(filters.Regex("^(Прислать котика)$"), send_cat_picture)
    )
    mybot.add_handler(MessageHandler(filters.LOCATION, user_coordinates))
    mybot.add_handler(MessageHandler(filters.PHOTO, check_user_photo))

    mybot.add_handler(CallbackQueryHandler(take_constellation))

    mybot.add_handler(MessageHandler(filters.TEXT, echo))

    mybot.run_polling()


if __name__ == "__main__":
    main()
