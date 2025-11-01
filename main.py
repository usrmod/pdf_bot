# def main():
#     print("Hello from telgram-my-util-bot!")


# if __name__ == "__main__":
#     main()

import logging

from telegram.ext import Application, CommandHandler, MessageHandler, filters

from bot import *
from config import BOT_TOKEN

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("test", test))
    app.add_handler(CommandHandler("echo", echo))
    app.add_handler(CommandHandler("img_to_pdf", img_to_pdf))

    # app.add_handler(MessageHandler(filters.PHOTO, img_to_pdf))

    app.add_handler(MessageHandler(filters.PHOTO, remove_bg))

    print("🤖 Bot running...")
    app.run_polling()


if __name__ == "__main__":
    main()
