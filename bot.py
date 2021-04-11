from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler
from telegram import ReplyKeyboardMarkup


class LanguageBot:
    def __init__(self):

        self.dictionary = {'Части тела': ['tvář - лицо́', 'břicho - живо́т'],
                           'Прилагательные': ['čerstvý - све́жий', 'okoralý - чёрствый']}
        self.remaining_words = dict()
        self.current_theme = dict()

        self.while_learning = dict()
        self.possible_tests = dict()
        self.while_chatting = dict()
        self.words_for_test = dict()
        self.correct_words = dict()
        self.variants = dict()
        self.count_of_words = dict()
        self.rightness = dict()
        self.current_test = dict()
        self.seeking = dict()
        self.in_chat_with = dict()
        self.answer = dict()

        self.main()

    def start(self, update, context):

        self.while_learning.setdefault(str(update.message.chat.id), False)
        self.possible_tests.setdefault(str(update.message.chat.id), list())
        self.while_chatting.setdefault(str(update.message.chat.id), False)
        self.words_for_test.setdefault(str(update.message.chat.id), list())
        self.correct_words.setdefault(str(update.message.chat.id), list())
        self.variants.setdefault(str(update.message.chat.id), list())
        self.count_of_words.setdefault(str(update.message.chat.id), 0)
        self.rightness.setdefault(str(update.message.chat.id), 0)
        self.current_test.setdefault(str(update.message.chat.id), 0)
        self.answer.setdefault(str(update.message.chat.id), 0)

        update.message.reply_text('Привет, я бот, предназначенный для изучения чешского языка.\n'
                                  'Тебе будут представлены разделы с новыми словами,'
                                  ' с последующей проверкой твоих знаний.')

        reply_keyboard = [['Да', 'Нет']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

        update.message.reply_text("Начнем?", reply_markup=markup)

    def on_message(self, update, context):
        if not self.while_chatting.get(str(update.message.chat.id)):
            if update.message.text == "Искать чат":
                reply_keyboard = [["Прекратить чат"]]
                markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
                update.message.reply_text("Мы ищем вам собеседника\n", reply_markup=markup)
                self.while_chatting[str(update.message.chat.id)] = True
                self.chat(update, context)

            if update.message.text == "Да" or update.message.text == "Уроки":
                reply_keyboard = [self.dictionary.keys()]
                markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

                update.message.reply_text("Вот разделы, которые ты можешь изучить/повторить",
                                          reply_markup=markup)

            if update.message.text == "Нет":
                update.message.reply_text(":^(\nПриходи как созреешь")

            if update.message.text in self.dictionary.keys() and not self.while_learning.get(
                    str(update.message.chat.id)):
                self.current_theme[str(update.message.chat.id)] = update.message.text
                if self.current_theme[str(update.message.chat.id)] not in self.possible_tests[
                    str(update.message.chat.id)]:
                    self.possible_tests[str(update.message.chat.id)].append(
                        self.current_theme[str(update.message.chat.id)])

                self.remaining_words[str(update.message.chat.id)] = '\n'.join(
                    self.dictionary[update.message.text])

                reply_keyboard = [["Хочу"], ["Не хочу"]]
                markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

                update.message.reply_text(
                    self.remaining_words[
                        str(update.message.chat.id)] + '\nХотите провести тест по пройденным'
                                                       ' урокам?', reply_markup=markup)

            if update.message.text == "Хочу":
                self.while_learning[str(update.message.chat.id)] = True

                reply_keyboard = [self.possible_tests[str(update.message.chat.id)]]
                markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

                update.message.reply_text("Вот возможные тесты", reply_markup=markup)

            if update.message.text == "Не хочу":
                update.message.reply_text("Ладно, в следующий раз")

            if self.while_learning[str(update.message.chat.id)]:
                self.answer[str(update.message.chat.id)] = 1

            if update.message.text in self.possible_tests[str(update.message.chat.id)] and \
                    self.while_learning[str(update.message.chat.id)]:
                for string in self.dictionary[update.message.text]:
                    words = string.split()
                    self.words_for_test[str(update.message.chat.id)].append(words[0])

                self.variants[str(update.message.chat.id)].append(
                    [self.dictionary[update.message.text][0].split()[2],
                     self.dictionary[update.message.text][1].split()[2]])
                self.variants[str(update.message.chat.id)].append(
                    [self.dictionary[update.message.text][0].split()[2],
                     self.dictionary[update.message.text][1].split()[2]])
                self.count_of_words[str(update.message.chat.id)] = 2
                self.rightness[str(update.message.chat.id)] = 0
                self.current_test[str(update.message.chat.id)] = update.message.text

                reply_keyboard = [self.variants[str(update.message.chat.id)][0]]
                markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
                update.message.reply_text("Выбери правильный перевод слова\n"
                                          + self.words_for_test[str(update.message.chat.id)][0],
                                          reply_markup=markup)

                self.answer[str(update.message.chat.id)] = 0

            if self.while_learning[str(update.message.chat.id)] and self.answer[
                str(update.message.chat.id)]:
                correct = self.dictionary[self.current_test[str(update.message.chat.id)]][
                    2 - self.count_of_words[str(update.message.chat.id)]].split()[2]

                if update.message.text == correct:
                    self.count_of_words[str(update.message.chat.id)] -= 1
                    self.rightness[str(update.message.chat.id)] += 1
                    if self.count_of_words[str(update.message.chat.id)]:
                        reply_keyboard = [
                            self.variants[str(update.message.chat.id)][
                                1 - self.count_of_words[str(update.message.chat.id)]]]
                        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
                        update.message.reply_text("Верно, вот следующее слово\n"
                                                  +
                                                  self.words_for_test[str(update.message.chat.id)][
                                                      1],
                                                  reply_markup=markup)

                else:
                    self.count_of_words[str(update.message.chat.id)] -= 1
                    if self.count_of_words[str(update.message.chat.id)]:
                        reply_keyboard = [
                            self.variants[str(update.message.chat.id)][
                                1 - self.count_of_words[str(update.message.chat.id)]]]
                        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
                        update.message.reply_text("Неверно, правильно " +
                                                  correct + ", вот следующее слово\n"
                                                  +
                                                  self.words_for_test[str(update.message.chat.id)][
                                                      1],
                                                  reply_markup=markup)

                if self.count_of_words[str(update.message.chat.id)] == 0:
                    self.while_learning[str(update.message.chat.id)] = False
                    reply_keyboard = [["Уроки"], ["Искать чат"]]
                    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
                    if self.rightness[str(update.message.chat.id)] / 2 > 0.69:
                        update.message.reply_text("Ты прошел тест, молодец!", reply_markup=markup)
                        self.possible_tests[str(update.message.chat.id)].remove(
                            self.current_test[str(update.message.chat.id)])
                    else:
                        update.message.reply_text("Ты плохо написал тест, пройди его еще раз,"
                                                  " чтобы лучше запомнить слова",
                                                  reply_markup=markup)

                    self.words_for_test[str(update.message.chat.id)] = list()
                    self.variants[str(update.message.chat.id)] = list()
        if update.message.text == "Прекратить чат":
            self.end_chat(update, context)
        else:
            update.message.forward(self.in_chat_with[str(update.message.chat.id)])

    def chat(self, update, context):
        self.seeking[str(update.message.chat.id)] = 1
        print(self.seeking)
        flag = False
        chatting = []

        for value in dict.items(self.seeking):
            if value[1] == 1:
                chatting.append(value[0])
                print(chatting)

        if len(chatting) > 1:
            flag = True

        if flag:
            update.message.forward(chatting[0])
            update.message.forward(chatting[1])
            self.seeking[chatting[0]] = 0
            self.seeking[chatting[1]] = 0
            self.in_chat_with[chatting[0]] = chatting[1]
            self.in_chat_with[chatting[1]] = chatting[0]
            self.while_chatting[str(update.message.chat.id)] = True

    def end_chat(self, update, context):
        update.message.reply_text("Вы больше не ищите чат, либо прекратили действуйющий.")
        self.while_chatting[str(update.message.chat.id)] = False
        self.seeking[str(update.message.chat.id)] = 0
        self.in_chat_with[str(update.message.chat.id)], self.in_chat_with[
            self.in_chat_with[str(update.message.chat.id)]] = 0, 0

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
