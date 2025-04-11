# import sys
import logging
from gl_conf.config import TOKEN
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import filters, MessageHandler, ApplicationBuilder, ContextTypes, CommandHandler, InlineQueryHandler
from random import randint
from uuid import uuid4


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    MSG_START = """Hi! I'm Random bot.
I can generate some random data.
For more info send /help"""
    await context.bot.send_message(chat_id=update.effective_chat.id, text=MSG_START)

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    MSG_HELP = """Here is the list of commands that I understand:
    /start - Start the bot
    /help - Show this message
    /caps <text> - Show your text in caps
    /d6 <number from (1 - 10)> - roll d6 dices"""
    await context.bot.send_message(chat_id=update.effective_chat.id, text=MSG_HELP)

# async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

async def roll_d6(update: Update, context: ContextTypes.DEFAULT_TYPE):
    default_dice_amt = 3
    dice_amt_range = (1, 11)

    dice_amt_raw = context.args[0] if context.args else default_dice_amt
    dice_amt_raw = int(dice_amt_raw) if dice_amt_raw.isdigit() else default_dice_amt
    dice_amt = dice_amt_raw if dice_amt_raw in range(*dice_amt_range) else default_dice_amt
    rolls = [str(randint(1, 6)) for i in range(dice_amt)]
    MSG_ROLL = f'{' | '.join(rolls)}'

    await context.bot.send_message(chat_id=update.effective_chat.id, text=MSG_ROLL)

async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

# async def inline_caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     query = update.inline_query.query
#     if not query:
#         return
#     results = []
#     results.append(
#         InlineQueryResultArticle(
#             id=str(uuid4()),
#             title='Caps',
#             input_message_content=InputTextMessageContent(query.upper())
#         )
#     )
#     await context.bot.answer_inline_query(update.inline_query.id, results)

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    MSG_UNKNOWN = """Sorry, I didn't understand that command."""
    await context.bot.send_message(chat_id=update.effective_chat.id, text=MSG_UNKNOWN)


def main():
    application = ApplicationBuilder().token(TOKEN).build()

    handlers = [
        CommandHandler('start', start),
        CommandHandler('help', help),
        CommandHandler('d6', roll_d6),
        # MessageHandler(filters.TEXT & (~filters.COMMAND), echo),
        CommandHandler('caps', caps),
        # InlineQueryHandler(inline_caps),
        MessageHandler(filters.COMMAND, unknown),
    ]

    for handler in handlers:
        application.add_handler(handler)

    # start_handler = CommandHandler('start', start)
    # help_handler = CommandHandler('help', help)
    # roll_d6_handler = CommandHandler('d6', roll_d6)
    # # echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    # caps_handler = CommandHandler('caps', caps)
    # # inline_caps_handler = InlineQueryHandler(inline_caps)
    # unknown_handler = MessageHandler(filters.COMMAND, unknown)

    # application.add_handler(start_handler)
    # application.add_handler(help_handler)
    # application.add_handler(roll_d6_handler)
    # # application.add_handler(echo_handler)
    # application.add_handler(caps_handler)
    # # application.add_handler(inline_caps_handler)
    # application.add_handler(unknown_handler)

    application.run_polling()


if __name__ == '__main__':
    main()
