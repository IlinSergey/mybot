import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

from config import TG_API_KEY


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='bot.log',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):    
    await context.bot.send_message(chat_id=update.effective_chat.id, 
    text="Я бот, поговори со мной!")


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,   
    text=f'Привет {update.effective_user.first_name}')


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


def main():    
    mybot = ApplicationBuilder().token(TG_API_KEY).build()

    start_handler = CommandHandler('start', start)
    hello_handler = CommandHandler("hello", hello)
    talk_to_me_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)

    logging.info('Бот стартовал')
    
    mybot.add_handler(start_handler)
    mybot.add_handler(hello_handler)
    mybot.add_handler(talk_to_me_handler)


    mybot.run_polling()


if __name__ == '__main__':
    main()
