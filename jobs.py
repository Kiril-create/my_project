from telegram.ext import CallbackContext
from telegram.error import BadRequest
from telegram import Update
from db_funcs import get_all_users, update_games
from decorators import task_time
from models import Game
from parsers.igm_parser import parse_html as ph_igm
from parsers.steambuy_parser import parse_html as ph_steambuy


def check_discounts(context: CallbackContext):
    games = Game.query.all()
    if games:
        users = get_all_users()
        for user in users:
            telegram_id = user.telegram_id
            for game in games:
                discounts = {}
                discounts['steam'] = game.discount
                discounts['igm'] = game.igm_actual_price / game.original_price
                discounts['steambuy'] = game.steambuy_actual_price / game.original_price
                max_discount = max(discounts, key=discounts.get)
                if discounts[max_discount] >= 0.1:
                    # + выводить цену в магазине с самой большой скидкой
                    text = f'Игра {game.title} продается со скидкой {discounts[max_discount]} в {max_discount}'
                    try:
                        context.bot.send_message(
                            chat_id=telegram_id,
                            text=text,
                        )
                    except BadRequest:
                        print(f'пользователь {telegram_id} заблокировал бота')


@task_time
def launch_parsers(update: Update, context: CallbackContext):
    db = {}
    db['igm'] = ph_igm()
    # db['steambuy'] = ph_steambuy()

    for shop, games in db.items():
        update_games(shop, games)
