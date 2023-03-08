import logging

from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from config import TG_API_KEY
from handlers import (
    check_user_photo,
    echo,
    guess_number,
    planet,
    send_cat_picture,
    start,
    take_constellation,
    user_coordinates,
    subscribe,
    unsubscribe,
)
from questionnaire import (
    questionnaire_comment,
    questionnaire_dontknow,
    questionnaire_name,
    questionnaire_rating,
    questionnaire_skip,
    questionnaire_start,
)
from jobs import send_updates

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="bot.log",
    level=logging.INFO,
)


def main():
    mybot = ApplicationBuilder().token(TG_API_KEY).build()
    logging.info("Бот стартовал")

    jq = mybot.job_queue
    jq.run_repeating(send_updates, interval=10, first=0)

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
