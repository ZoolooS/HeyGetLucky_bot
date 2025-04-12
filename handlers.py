import re
from random import randint, randrange
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


async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    MSG_START = """Hi! I'm Random bot.
I can generate some random data.
For more info send /help"""
    await context.bot.send_message(chat_id=update.effective_chat.id, text=MSG_START)


async def handle_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    MSG_HELP = """Here is the list of commands that I understand:
    /start - Start the bot
    /help - Show this message
    /caps <text> - Show your text in caps
    /roll d<num from (2, 4, 6, 8, 10, 12, 20, 100)>x<num from (1-10)> - Roll dices (default d6x3)"""
    # /d6 <number from (1 - 10)> - roll d6 dices
    await context.bot.send_message(chat_id=update.effective_chat.id, text=MSG_HELP)


# async def handle_echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


# async def handle_roll_d6(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     default_dice_amt = 3
#     dice_amt_range = (1, 11)

#     dice_amt_raw = context.args[0] if context.args else default_dice_amt
#     dice_amt_raw = int(dice_amt_raw) if dice_amt_raw.isdigit() else default_dice_amt
#     dice_amt = dice_amt_raw if dice_amt_raw in range(*dice_amt_range) else default_dice_amt
#     rolls = [str(randint(1, 6)) for i in range(dice_amt)]
#     MSG_ROLL = f'{' | '.join(rolls)}'

#     await context.bot.send_message(chat_id=update.effective_chat.id, text=MSG_ROLL)


# TODO: Переписать get_dice_set() и is_str_dice_set() согласно DRY
def get_dice_set(raw_dice_set):
    pattern = r'^d(?P<dice>\d+)x(?P<amt>\d+)$'
    match = re.match(pattern, raw_dice_set)
    return (int(match.group('dice')), int(match.group('amt')))


def is_str_dice_set(raw_dice_set):
    pattern = r'^d(?P<dice>\d+)x(?P<amt>\d+)$'
    dices_range = (2, 4, 6, 8, 10, 12, 20, 100)
    dice_amt_range = (1, 11)

    match = re.match(pattern, raw_dice_set)
    if (not raw_dice_set
        or not match
        or int(match.group('dice')) not in dices_range
        or int(match.group('amt')) not in dice_amt_range):
        return False
    return True


def get_roll(dice):
    if dice == 100:
        return f'{randrange(0, 100, 10):02}, {randint(0, 9)}'
    if dice == 10:
        return f'{randint(0, 9)}'
    return f'{randint(1, dice)}'


# FIX: Не воспринимает количество дайсов и в итоге берёт дефолтные настройки
# TODO: Научить принимаеть только тип дайса и выдавать дефолтное количество его роллов
async def handle_roll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    default_dice = 6
    default_dice_amt = 3

    dice, dice_amt = get_dice_set(context.args[0]) if (context.args and is_str_dice_set(context.args[0])) else (default_dice, default_dice_amt)
    rolls = [get_roll(dice) for i in range(dice_amt)]
    MSG_ROLL = f'{' | '.join(rolls)}'

    await context.bot.send_message(chat_id=update.effective_chat.id, text=MSG_ROLL)


async def handle_caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


# async def handle_inline_caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
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


async def handle_unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    MSG_UNKNOWN = """Sorry, I didn't understand that command."""
    await context.bot.send_message(chat_id=update.effective_chat.id, text=MSG_UNKNOWN)
