from telegram import Update
from telegram.ext import CallbackContext

from db import db_session
from models import Game, User, UserGame

# миграции!!!!


def add_game(user_id, game_info):
    new_game = Game(
            name=game_info['name'],
            url=game_info['url'],
            price=game_info['price'],
            actual_price=game_info['actual_price'],
            discount=game_info['discount'],
    )
    db_session.add(new_game)
    db_session.commit()
    game_id = new_game.id
    new_row = UserGame(
        user_id=user_id,
        game_id=game_id,
    )
    db_session.add(new_row)
    db_session.commit()


def get_all_users():
    all_users = User.query.all()
    return all_users


def save_data(update: Update, context: CallbackContext):
    new_user = User(
        telegram_id=context.user_data['telegram_id'],
        full_name=context.user_data['user_name'],
        wishlist=context.user_data['wishlist'],
        region=context.user_data['region'],
    )
    db_session.add(new_user)
    db_session.commit()
    user_id = new_user.id
    return user_id
