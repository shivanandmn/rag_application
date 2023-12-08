# import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv, find_dotenv
import requests
import os

_ = load_dotenv(find_dotenv())
# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     level=logging.INFO
# )

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


async def prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = requests.post(
        "http://127.0.0.1:5000/answer", data=update.message.text
    ).json()["response"]
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def app():
    application = ApplicationBuilder().token(TOKEN).build()
    text_handler = MessageHandler(filters.TEXT, prompt)
    application.add_handler(text_handler)
    print("Telegram Bot running!!!")
    application.run_polling()
    


if __name__ == "__main__":
    app()
