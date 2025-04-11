from random import randint
# from uuid import uuid4
from telegram import (
    # InlineQueryResultArticle,
    # InputTextMessageContent,
    Update,
)
from telegram.ext import (
    # ApplicationBuilder,
    ContextTypes,
    # CommandHandler,
    # filters,
    # InlineQueryHandler,
    # MessageHandler,
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
