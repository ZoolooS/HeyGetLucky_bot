import re
from collections import ChainMap
from random import randint, randrange
# from uuid import uuid4
from telegram import (
    # InlineQueryResultArticle,
    # InputTextMessageContent,
    Update,
)
from telegram.ext import (
    ContextTypes,
)


async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    MSG_START = """Hi! I'm Random bot.
I can generate some random data.
For more info send /help."""
    await context.bot.send_message(chat_id=update.effective_chat.id, text=MSG_START)


async def handle_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    MSG_HELP = """Here is the list of commands that I understand:
    /start - Start the bot;
    /help - Show this message;
    /roll d<num from (2, 4, 6, 8, 10, 12, 20, 100)>[x<num from (1-10)]> - Roll dices (default d6x3)."""
    # /caps <text> - Show your text in caps
    await context.bot.send_message(chat_id=update.effective_chat.id, text=MSG_HELP)


# async def handle_echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


# TODO: Переписать get_dice_set() и is_str_dice_set() согласно DRY
def get_dice_set(raw_dice_set):
    pattern = r'^d(?P<dice>\d+)(?:x(?P<amt>\d+))?$'
    match = re.match(pattern, raw_dice_set)
    dice = int(match.group('dice'))
    amt = int(match.group('amt')) if match.group('amt') else None
    return {'dice': dice, 'dice_amt': amt} if amt else {'dice': dice}


def is_str_dice_set(raw_dice_set):
    pattern = r'^d(?P<dice>\d+)(?:x(?P<amt>\d+))?$'
    dices_range = (2, 4, 6, 8, 10, 12, 20, 100)
    dice_amt_range = range(1, 11)

    match = re.match(pattern, raw_dice_set)
    if (not raw_dice_set
        or not match
        or int(match.group('dice')) not in dices_range
        or int(match.group('amt')) not in dice_amt_range if match.group('amt') else False):
        return False
    return True


def get_roll(dice):
    if dice == 100:
        return f'{randrange(0, 100, 10):02}, {randint(0, 9)}'
    if dice == 10:
        return f'{randint(0, 9)}'
    return f'{randint(1, dice)}'


async def handle_roll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    default_dice_set = {'dice': 6, 'dice_amt': 3}

    dice, dice_amt = ChainMap(get_dice_set(context.args[0]) if (context.args and is_str_dice_set(context.args[0])) else {}, default_dice_set).values()
    rolls = [get_roll(dice) for i in range(dice_amt)]
    MSG_ROLL = f'{' | '.join(rolls)}'

    await context.bot.send_message(chat_id=update.effective_chat.id, text=MSG_ROLL)


# async def handle_caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     text_caps = ' '.join(context.args).upper()
#     await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


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
    MSG_UNKNOWN = """Nope, there's no such command."""
    await context.bot.send_message(chat_id=update.effective_chat.id, text=MSG_UNKNOWN)
