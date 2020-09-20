from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler
from telegram import ReplyKeyboardMarkup


class LanguageBot:
    def __init__(self):
        self.main()

    def start(self, update, context):
        reply_keyboard = [['Да', 'Нет']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

        update.message.reply_text('infa o bote')

        update.message.reply_text("Начнем?", reply_markup=markup)

    def on_message(self, update, context):
        if update.message.text.lower() == "да":
            update.message.reply_text("ZAGLUSHKA")

        if update.message.text.lower() == "нет":
            update.message.reply_text(":^(\n Приходи как созреешь")

    def main(self):
        REQUEST_KWARGS = {
            'proxy_url': 'socks5://88.202.177.242:1080',
        }

        updater = Updater('1301742315:AAGoj-W_HPm-uVG85gmtkft7bAn5zNhoRVY',
                          use_context=True,
                          request_kwargs=REQUEST_KWARGS)

        dp = updater.dispatcher

        dp.add_handler(CommandHandler('start', self.start))
        dp.add_handler(MessageHandler(Filters.all, self.on_message))
        updater.start_polling()

        updater.idle()


if __name__ == '__main__':
    bot = LanguageBot()
