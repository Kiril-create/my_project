from datetime import time
from pytz import timezone
from telegram.ext import Updater, CallbackQueryHandler, ConversationHandler, CommandHandler, MessageHandler, Filters

import jobs
import handlers
import settings


def main():
    bot = Updater(settings.API_TOKEN_TELEGRAM)

    dp = bot.dispatcher
    dp.add_handler(CommandHandler('start', handlers.say_hello))

    conv = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex(r'^(Регистрация)$'), handlers.start_registration),
            MessageHandler(Filters.regex(r'^(Сделать рассылку)$'), handlers.input_message),
        ],
        states={
            'save_user_name': [MessageHandler(Filters.text, handlers.save_user_name)],
            'save_wishlist': [MessageHandler(Filters.text, handlers.save_wishlist)],
            'save_region': [CallbackQueryHandler(handlers.save_region, pattern=r'Россия|Казахстан|Турция')],
            'send_message': [MessageHandler(Filters.text, handlers.send_message)],
        },
        fallbacks=[],
    )

    dp.add_handler(conv)

    jq = bot.job_queue
    jq.run_daily(
        jobs.check_discounts,
        time=time(17, 44, 45, tzinfo=timezone('Europe/Moscow')),
        days=(0, 1, 2, 3, 4, 5),  # минус вс
    )

    bot.start_polling()
    bot.idle()


if __name__ == '__main__':
    main()
