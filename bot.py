from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler
from telegram import ReplyKeyboardMarkup
import sqlite3


class LanguageBot:
    def __init__(self):
        self.dictionary = {'Части тела': ['tvář - лицо́', 'břicho - живо́т'], 'Прилагательные': ['čerstvý - све́жий', 'okoralý - чёрствый']}
        self.remaining_words = ''
        self.current_theme = ''

        self.while_learning = False
        self.possible_tests = list()
        self.while_chatting = False
        self.words_for_test = list()
        self.correct_words = list()
        self.variants = list()
        self.count_of_words = 0
        self.rightness = 0
        self.current_test = 0

        self.main()

    def start(self, update, context):
        self.connection = sqlite3.connect("database.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute("SELECT id FROM users WHERE id = " + str(update.message.chat.id))
        data = self.cursor.fetchall()

        if not len(data):
            self.cursor.execute("INSERT INTO users (id) VALUES (" + str(update.message.chat.id) + ")")
            self.connection.commit()

        update.message.reply_text('Привет, я бот, предназначенный для изучения чешского языка.\n'
                                  'Тебе будут представлены разделы с новыми словами,'
                                  ' с последующей проверкой твоих знаний.')

        reply_keyboard = [['Да', 'Нет']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

        update.message.reply_text("Начнем?", reply_markup=markup)

    def on_message(self, update, context):
        if not self.while_chatting:
            if update.message.text == "Войти в чат":
                self.while_chatting = True
                self.chat(update, context)

            if update.message.text == "Да" or update.message.text == "Уроки":
                reply_keyboard = [self.dictionary.keys()]
                markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

                update.message.reply_text("Вот разделы, которые ты можешь изучить/повторить",
                                          reply_markup=markup)

            if update.message.text == "Нет":
                update.message.reply_text(":^(\nПриходи как созреешь")

            if update.message.text in self.dictionary.keys() and not self.while_learning:
                self.current_theme = update.message.text
                if self.current_theme not in self.possible_tests:
                    self.possible_tests.append(self.current_theme)

                self.remaining_words = '\n'.join(self.dictionary[update.message.text])

                reply_keyboard = [["Хочу"], ["Не хочу"]]
                markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

                update.message.reply_text(
                    self.remaining_words + '\nХотите провести тест по пройденным'
                                           ' урокам?', reply_markup=markup)

            if update.message.text == "Хочу":
                self.while_learning = True

                reply_keyboard = [self.possible_tests]
                markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

                update.message.reply_text("Вот возможные тесты", reply_markup=markup)

            if update.message.text == "Не хочу":
                update.message.reply_text("Ладно, в следующий раз")

            if self.while_learning:
                self.answer = 1

            if update.message.text in self.possible_tests and self.while_learning:
                for string in self.dictionary[update.message.text]:
                    words = string.split()
                    self.words_for_test.append(words[0])

                self.variants.append([self.dictionary[update.message.text][0].split()[2],
                                      self.dictionary[update.message.text][1].split()[2]])
                self.variants.append([self.dictionary[update.message.text][0].split()[2],
                                      self.dictionary[update.message.text][1].split()[2]])
                self.count_of_words = 2
                self.rightness = 0
                self.current_test = update.message.text

                reply_keyboard = [self.variants[0]]
                markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
                update.message.reply_text("Выбери правильный перевод слова\n"
                                          + self.words_for_test[0], reply_markup=markup)
                self.answer = 0

            if self.while_learning and self.answer:
                correct = self.dictionary[self.current_test][2 - self.count_of_words].split()[2]

                if update.message.text == correct:
                    self.count_of_words -= 1
                    self.rightness += 1
                    if self.count_of_words:
                        reply_keyboard = [self.variants[1 - self.count_of_words]]
                        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
                        update.message.reply_text("Верно, вот следующее слово\n"
                                                  + self.words_for_test[1],
                                                  reply_markup=markup)

                else:
                    self.count_of_words -= 1
                    if self.count_of_words:
                        reply_keyboard = [self.variants[1 - self.count_of_words]]
                        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
                        update.message.reply_text("Неверно, правильно " +
                                                  correct + ", вот следующее слово\n"
                                                  + self.words_for_test[1],
                                                  reply_markup=markup)

                if self.count_of_words == 0:
                    self.while_learning = False
                    reply_keyboard = [["Уроки"], ["Искать чат"]]
                    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
                    if self.rightness / 2 > 0.69:
                        update.message.reply_text("Ты прошел тест, молодец!", reply_markup=markup)
                        self.possible_tests.remove(self.current_test)
                    else:
                        update.message.reply_text("Ты плохо написал тест, пройди его еще раз,"
                                                  " чтобы лучше запомнить слова",
                                                  reply_markup=markup)

                    self.words_for_test = list()
                    self.variants = list()

            else:
                update.message.reply_text("Я робот, я не понимаю человеческий((")

        else:
            if update.message.chat.id == self.data[1][0]:
                update.message.forward(self.data[0][0])
            if update.message.chat.id == self.data[0][0]:
                update.message.forward(self.data[1][0])

    def chat(self, update, context):
        update.message.reply_text("Ожидайте, мы ищем вам собеседника")

        self.cursor.execute("UPDATE users SET seeking = 1 WHERE id = " + str(update.message.chat.id))
        self.connection.commit()
        self.cursor.execute("SELECT id FROM users WHERE seeking = 1")
        self.data = self.cursor.fetchall()

        if len(self.data) > 1:
            update.message.forward(self.data[0][0])
            update.message.forward(self.data[1][0])
            self.cursor.execute("UPDATE users SET seeking = 0 WHERE id = " + str(self.data[0][0]))
            self.cursor.execute("UPDATE users SET seeking = 0 WHERE id = " + str(self.data[1][0]))
            self.cursor.execute("UPDATE users SET in_chat_with = " + str(self.data[0][0]) +
                                " WHERE id = " + str(self.data[1][0]))
            self.cursor.execute("UPDATE users SET in_chat_with = " + str(self.data[1][0]) +
                                " WHERE id = " + str(self.data[0][0]))
            self.connection.commit()
            self.while_chatting = True

    def end_chat(self, update, context):
        update.message.reply_text("Вы больше не ищите чат, либо прекратили действуйющий.")
        self.while_chatting = False
        self.cursor.execute("UPDATE users SET seeking = 0 WHERE id = " + str(update.message.chat.id))
        self.cursor.execute("UPDATE users SET in_chat_with = 0 WHERE id = " + str(self.data[1][0]))
        self.cursor.execute("UPDATE users SET in_chat_with = 0 WHERE id = " + str(self.data[0][0]))
        self.connection.commit()

    def main(self):
        request_kwargs = {
            'proxy_url': 'socks5://195.144.21.185:1080',
        }

        updater = Updater('1301742315:AAGoj-W_HPm-uVG85gmtkft7bAn5zNhoRVY',
                          use_context=True,
                          request_kwargs=request_kwargs)

        dp = updater.dispatcher

        dp.add_handler(CommandHandler('start', self.start))
        dp.add_handler(CommandHandler('chat', self.chat))
        dp.add_handler(CommandHandler('end', self.end_chat))
        dp.add_handler(MessageHandler(Filters.all, self.on_message))

        updater.start_polling()

        updater.idle()


if __name__ == '__main__':
    bot = LanguageBot()
