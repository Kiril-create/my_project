import json

from telegram.ext import CallbackContext
from telegram.error import BadRequest

from db_funcs import get_all_users


def check_discounts(context: CallbackContext):
    with open('result.json', 'r', encoding='utf-8') as f:
        games = json.load(f)

    games = [game for game in games if game['discount'] > 50]
    if games:
        users = get_all_users()
        for user in users:
            telegram_id = user.telegram_id
            for game in games:
                text = f'Игра {game["title"]} продается со скидкой {game["discount"]}'
                try:
                    context.bot.send_message(
                        chat_id=telegram_id,
                        text=text,
                    )
                except BadRequest:
                    print(f'пользователь {telegram_id} заблокировал бота')
