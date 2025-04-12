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
    handle_start,
    handle_help,
    # handle_roll_d6,
    handle_roll,
    handle_caps,
    handle_unknown,
)


def main():
    application = ApplicationBuilder().token(TOKEN).build()

    handlers = [
        CommandHandler('start', handle_start),
        CommandHandler('help', handle_help),
        # CommandHandler('d6', handle_roll_d6),
        CommandHandler('roll', handle_roll),
        # MessageHandler(filters.TEXT & (~filters.COMMAND), handle_echo),
        CommandHandler('caps', handle_caps),
        # InlineQueryHandler(handle_inline_caps),
        MessageHandler(filters.COMMAND, handle_unknown),
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
