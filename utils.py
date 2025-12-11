from telegram import (ReplyKeyboardMarkup, InlineKeyboardButton,
                      InlineKeyboardMarkup)


def get_kb(is_admin=False):
    btns = [
        ['Регистрация'],
    ]
    if is_admin:
        btns.append(['Сделать рассылку'])
    return ReplyKeyboardMarkup(btns)


def get_region():
    btns = [
        [InlineKeyboardButton('Россия', callback_data='Россия')],
        [InlineKeyboardButton('Казахстан', callback_data='Казахстан')],
        [InlineKeyboardButton('Турция', callback_data='Турция')],
    ]
    return InlineKeyboardMarkup(btns)
