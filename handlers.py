from telegram import Update, ReplyKeyboardRemove
from telegram.error import BadRequest
from telegram.ext import CallbackContext, ConversationHandler

from db_funcs import add_game, get_all_users, save_data
from settings import ADMINS
from steam_parser import get_wishlist
from utils import get_kb, get_region


def input_message(update: Update, context: CallbackContext):
    update.message.reply_text('что отправить пользователям?')
    return 'send_message'


def send_message(update: Update, context: CallbackContext):
    text = update.message.text
    all_users = get_all_users()
    for user in all_users:
        telegram_id = user.telegram_id
        if telegram_id not in ADMINS:
            try:
                context.bot.send_message(
                    chat_id=telegram_id,
                    text=text,
                )
            except BadRequest:
                print(f'пользователь {telegram_id} заблокировал бота')
    update.message.reply_text('рассылка завершена')
    return ConversationHandler.END


def say_hello(update: Update, context: CallbackContext):
    username = update.message.chat.username
    telegram_id = update.message.chat.id
    update.message.reply_text(
        f'Привет, {username.capitalize()}!',
        reply_markup=get_kb(telegram_id in ADMINS)
        )


def start_registration(update: Update, context: CallbackContext):
    context.user_data['telegram_id'] = update.message.chat.id
    update.message.reply_text(
        'Отправь имя и фамилию',
        reply_markup=ReplyKeyboardRemove(),
        )
    return 'save_user_name'


def save_user_name(update: Update, context: CallbackContext):
    name = update.message.text.strip()
    if len(name.split()) == 2 and name.replace(' ', '').isalpha():
        update.message.reply_text('Отправь ссылку на свой wishlist')
        context.user_data['user_name'] = name
        return 'save_wishlist'
    else:
        update.message.reply_text('Введите имя и фамилию через пробел')
        return 'save_user_name'


def save_wishlist(update: Update, context: CallbackContext):
    text = update.message.text
    if (
        text.startswith('store.steampowered.com/wishlist/')
        or text.startswith('https://store.steampowered.com/wishlist/')
    ):
        context.user_data['wishlist'] = text
    else:
        update.message.reply_text('Введите корректную сылку')
        return 'save_wishlist'
    update.message.reply_text(
        'Укажите регион своего аккаунта',
        reply_markup=get_region(),
        )
    return 'save_region'


def save_region(update: Update, context: CallbackContext):
    data = update.callback_query.data
    context.user_data['region'] = data
    update.callback_query.message.reply_text(
        'Данные добавлены, мы пришлем пуш, когда появятся скидки',
        reply_markup=ReplyKeyboardRemove(),
        )
    user_id = save_data(update, context)
    games_from_wishlist = get_wishlist(context.user_data['wishlist'])
    if games_from_wishlist:
        for game in games_from_wishlist:
            add_game(user_id, game)
    return ConversationHandler.END
