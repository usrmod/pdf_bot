import logging
from logging.handlers import TimedRotatingFileHandler  # , RotatingFileHandler

from telegram.ext import Application, CommandHandler, MessageHandler, filters

from bot import *
from config import BOT_TOKEN

# One log per day, file changes at midnight with the date in the file name
handler = TimedRotatingFileHandler(
    "bot.log",
    when="midnight",
    interval=1,
    backupCount=7,  # Keep 7 days
)
handler.setFormatter(
    logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)

logging.basicConfig(level=logging.INFO, handlers=[handler])
# logging.basicConfig(level=logging.INFO, handlers=[handler, logging.StreamHandler()]) # for console as well


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # Basic commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("test", test))

    # PDF workflow commands
    app.add_handler(CommandHandler("start_pdf", start_pdf))
    app.add_handler(CommandHandler("finish", finish_pdf))
    app.add_handler(CommandHandler("cancel", cancel))

    # Photo handler - collects images
    app.add_handler(MessageHandler(filters.PHOTO, collect_photo))

    print("🤖 Bot running...")

    app.run_polling()


if __name__ == "__main__":
    main()
