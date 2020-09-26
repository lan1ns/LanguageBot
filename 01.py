from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler
from telegram import ReplyKeyboardMarkup
from time import sleep
import sqlite3


class LanguageBot:
    def __init__(self):

        # создать базу данных в которой будут храниться отдельные параметры для каждого человека,
        # т.к. они используются для каждого человека одновременно

        self.dictionary = {'1': ['1', '2'], '2': ['3', '4'], '3': ['5', '6'], '4': ['7', '8']}
        self.remaining_words = ''
        self.while_learning = False
        self.current_theme = ''
        self.possible_tests = list()  # из файла
        self.words_for_test = list()  # из файла
        self.correct_words = list()  # из файла
        self.variants = list()  # из файла
        self.count_of_words = 0  # из файла взять нужное кол-во слов
        self.rightness = 0
        self.current_test = 0
        self.while_chatting = False

        self.connection = sqlite3.connect("dbname")
        self.cursor = self.connection.cursor()  # подключить базу данных

        self.main()

    def start(self, update, context):
        self.cursor.execute("SELECT id WHERE rowid = ?", (update.message.effective_id))
        data = self.cursor.fetchall()

        if not len(data):
            self.cursor.execute("INSERT INTO dbname VALUES ?", (update.message.effective_id))

            self.connection.commit()

        reply_keyboard = [['Да', 'Нет']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

        update.message.reply_text('Привет, я бот, предназначенный для изучения чешского языка.\n'
                                  'Тебе будут представлены разделы с новыми словами,'
                                  ' с последующей проверкой твоих знаний.\n'
                                  'Также ты можешь поиграть со мной в "слова".')
        sleep(0.2)

        update.message.reply_text("Начнем?", reply_markup=markup)

    def on_message(self, update, context):
        if not self.while_chatting:
            if update.message.text.lower() == "да":
                reply_keyboard = [["1", "2"], ["3", "4"]]
                markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

                update.message.reply_text("Вот разделы, которые ты можешь изучить/повторить",
                                            reply_markup=markup)

            if update.message.text.lower() == "нет":
                update.message.reply_text(":^(\nПриходи как созреешь")

            if update.message.text in self.dictionary.keys() and not self.while_learning:
                self.current_theme = update.message.text
                self.possible_tests.append(self.current_theme)

                self.remaining_words = '\n'.join(self.dictionary[update.message.text])

                reply_keyboard = [["Хочу"], ["Не хочу"]]
                markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

                update.message.reply_text(self.remaining_words + '\nХотите провести тест по пройденным'
                                                                 ' урокам?', reply_markup=markup)

            if update.message.text == "Хочу":
                self.while_learning = True

                reply_keyboard = [self.possible_tests]
                markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

                update.message.reply_text("Вот возможные тесты", reply_markup=markup)

            if update.message.text == "Не хочу":
                print("Ладно, в следующий раз")

            if update.message.text in self.possible_tests and self.while_learning:
                self.words_for_test = list()  # из файла взять слова на тест
                self.variants = list()  # из файла взять слова для вариантов ответа
                self.count_of_words = 0  # из файла взять нужное кол-во слов
                self.rightness = 0
                self.current_test = self.possible_tests[update.message.text]

                reply_keyboard = [self.variants[-self.count_of_words]]
                markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
                update.message.reply_text("Выбери правильный перевод слова\n"
                                          + self.words_for_test[0], reply_markup=markup)
                self.count_of_words -= 1

            if self.while_learning:
                if update.message.text == self.correct_words[-self.count_of_words]:
                    reply_keyboard = [self.variants[-self.count_of_words]]
                    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
                    update.message.reply_text("Верно, вот следующее слово\n"
                                              + self.words_for_test[-self.count_of_words],
                                              reply_markup=markup)
                    self.count_of_words -= 1
                    self.rightness += 1
                else:
                    reply_keyboard = [self.variants[-self.count_of_words]]
                    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
                    update.message.reply_text("Неверно, правильно " +
                                              self.correct_words[-self.count_of_words] +
                                              ", вот следующее слово\n"
                                              + self.words_for_test[-self.count_of_words],
                                              reply_markup=markup)
                    self.count_of_words -= 1
                if self.count_of_words == 0:
                    self.while_learning = False
                    if self.rightness / len(self.correct_words) > 69:
                        self.possible_tests.pop(self.current_test)
                    else:
                        update.message.reply_text("Ты плохо написал тест, пройди его еще раз,"
                                                  " чтобы лучше запомнить слова")
            else:
                pass

    def chat(self, update, context):
        self.cursor.execute("INSERT INTO tabla_name VALUES ?", (update.message.effective_id))
        self.cursor.execute("SELECT ids FROM table_name")
        data = self.cursor.fetchall()

        if len(data) > 1:
            pass

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
        dp.add_handler(CommandHandler("chat", self.chat))

        updater.start_polling()

        updater.idle()


if __name__ == '__main__':
    bot = LanguageBot()