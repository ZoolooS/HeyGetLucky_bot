import logging
# import sys
# from random import randint
# from uuid import uuid4
# from telegram import (
#     # InlineQueryResultArticle,
#     # InputTextMessageContent,
#     Update,
# )
from telegram.ext import (
    ApplicationBuilder,
    # ContextTypes,
    CommandHandler,
    filters,
    # InlineQueryHandler,
    MessageHandler,
)

from gl_conf.config import TOKEN
from handlers import (
    start,
    help,
    roll_d6,
    # roll,
    caps,
    unknown,
)


def main():
    application = ApplicationBuilder().token(TOKEN).build()

    handlers = [
        CommandHandler('start', start),
        CommandHandler('help', help),
        CommandHandler('d6', roll_d6),
        # CommandHandler('roll', roll),
        # MessageHandler(filters.TEXT & (~filters.COMMAND), echo),
        CommandHandler('caps', caps),
        # InlineQueryHandler(inline_caps),
        MessageHandler(filters.COMMAND, unknown),
    ]

    for handler in handlers:
        application.add_handler(handler)

    application.run_polling()


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.WARNING
)

if __name__ == '__main__':
    main()
