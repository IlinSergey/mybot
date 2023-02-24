import logging

from telegram.ext import (ApplicationBuilder, CallbackQueryHandler,
                          CommandHandler, MessageHandler, filters)

from config import TG_API_KEY
from handlers import (echo, guess_number, hello, planet, send_cat_picture,
                      start, take_constellation, user_coordinates)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="bot.log",
    level=logging.INFO
)


def main():
    mybot = ApplicationBuilder().token(TG_API_KEY).build()
    logging.info("Бот стартовал")

    mybot.add_handler(CommandHandler("start", start))
    mybot.add_handler(CommandHandler("hello", hello))
    mybot.add_handler(CommandHandler("planet", planet))
    mybot.add_handler(CommandHandler("guess", guess_number))
    mybot.add_handler(CommandHandler("cat", send_cat_picture))
    mybot.add_handler(MessageHandler(filters.Regex("^(Прислать котика)$"), send_cat_picture))
    mybot.add_handler(MessageHandler(filters.LOCATION, user_coordinates))

    mybot.add_handler(CallbackQueryHandler(take_constellation))

    mybot.add_handler(MessageHandler(filters.TEXT, echo))

    mybot.run_polling()


if __name__ == "__main__":
    main()
