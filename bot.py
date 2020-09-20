from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler
from telegram import ReplyKeyboardMarkup
from time import sleep


class LanguageBot:
    def __init__(self):
        self.dictionary = {"1": ['123', '345', '678'], "2": [3, 4], "3": [5, 6], "4": [7, 8]}
        self.remaining_words = list()
        self.while_learning = False

        self.main()

    def start(self, update, context):
        self.while_learning = False
        reply_keyboard = [['Да', 'Нет']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

        update.message.reply_text('Привет, я бот, предназначенный для изучения чешского языка.\n'
                                  'Тебе будут представлены разделы с новыми словами,'
                                  ' с последующей проверкой твоих знаний.\n'
                                  'Также ты можешь поиграть со мной в "слова".')
        sleep(0.2)

        update.message.reply_text("Начнем?", reply_markup=markup)

    def on_message(self, update, context):
        if not self.while_learning:
            if update.message.text.lower() == "да":
                reply_keyboard = [["1", "2"], ["3", "4"]]
                markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

                update.message.reply_text("Вот разделы, которые ты можешь изучить/повторить",
                                          reply_markup=markup)

            if update.message.text.lower() == "нет":
                update.message.reply_text(":^(\n Приходи как созреешь")

        else:
            if update.message.text == "Да":
                if len(self.remaining_words) > 1:
                    reply_keyboard = [["Да"], ["Нет"]]
                    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

                    msg = str(self.remaining_words[0]) + "\nОсталось " + str(
                        len(self.remaining_words) - 1) \
                        + " слов.\nПродолжаем?"
                    update.message.reply_text(msg, reply_markup=markup)
                    self.remaining_words.pop(0)
                else:
                    self.while_learning = False
                    update.message.reply_text(str(self.remaining_words[0]) + "\nУрок кончился!")

            elif update.message.text == "Нет":
                self.while_learning = False
                update.message.reply_text("Лучше учись! Возвращайся и закончи урок позже.")

        if update.message.text in self.dictionary.keys():
            self.while_learning = True
            self.remaining_words = self.dictionary[update.message.text]

            reply_keyboard = [["Да"], ["Нет"]]
            markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

            msg = str(self.remaining_words[0]) + "\nОсталось " + str(len(self.remaining_words) - 1)\
                  + " слов.\nПродолжаем?"
            update.message.reply_text(msg, reply_markup=markup)
            self.remaining_words.pop(0)

    def main(self):
        request_kwargs = {
            'proxy_url': 'socks5://88.202.177.242:1080',
        }

        updater = Updater('1301742315:AAGoj-W_HPm-uVG85gmtkft7bAn5zNhoRVY',
                          use_context=True,
                          request_kwargs=request_kwargs)

        dp = updater.dispatcher

        dp.add_handler(CommandHandler('start', self.start))
        dp.add_handler(MessageHandler(Filters.all, self.on_message))
        updater.start_polling()

        updater.idle()


if __name__ == '__main__':
    bot = LanguageBot()
