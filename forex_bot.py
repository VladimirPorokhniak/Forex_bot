import datetime
import threading
import telebot
from Function import *
from telebot.types import Message
import time

coll_neyronov_na_uravne = 1
coll_skrytyh_uravney = 2
Constanta = 1
Iteration = 15
Epoch = 10000000
speed_of_learn = 1
Mistake_of_learn_new = 0
Mistake_of_learn_old = 1000
Mistake_of_test_new = 0
Mistake_of_test_old = 1000
answer_of_predict = 0
status_of_work = False
status_of_data = 0
Data_test = [0 for i in range(Iteration + coll_neyronov_na_uravne)]
Data_learn = [0 for i in range(Iteration + coll_neyronov_na_uravne)]
Neyron = [[0 for i11 in range(coll_neyronov_na_uravne)] for i12 in range(coll_skrytyh_uravney + 1)]
Mistake = [[0 for i11 in range(coll_neyronov_na_uravne)] for i12 in range(coll_skrytyh_uravney + 1)]
OUT_Neyron = 0
Weights = []
for i23 in range(coll_skrytyh_uravney):
    Weights.append(
        [[randomer(True) for i21 in range(coll_neyronov_na_uravne)] for i22 in range(coll_neyronov_na_uravne)])
Weight = [randomer(True) for i in range(coll_neyronov_na_uravne)]
Weights_d = []
for i23 in range(coll_skrytyh_uravney):
    Weights_d.append([[0 for i21 in range(coll_neyronov_na_uravne)] for i22 in range(coll_neyronov_na_uravne)])
Weight_d = [0 for i in range(coll_neyronov_na_uravne)]
Weights_old = []
for i23 in range(coll_skrytyh_uravney):
    Weights_old.append([[0 for i21 in range(coll_neyronov_na_uravne)] for i22 in range(coll_neyronov_na_uravne)])
Weight_old = [0 for i in range(coll_neyronov_na_uravne)]

bot = telebot.TeleBot(TOKEN, threaded=False)


def Data_for_learn() -> object:
    global Data_test, Data_learn, Iteration, coll_neyronov_na_uravne, Constanta
    index = 0
    size = coll_neyronov_na_uravne + Iteration
    while index < size:
        now = datetime.datetime.now()
        if now.minute in [4, 9, 14, 19, 24, 29, 34, 39, 44, 49, 54, 59] and now.second == 58 and (955000 < now.microsecond <= 960000):
            b = curs_online()
            if not b == (-1):
                Data_learn[index] = b - Constanta
                index += 1
            else:
                index = 0
    index = 0
    while index < size:
        now = datetime.datetime.now()
        if now.minute in [4, 9, 14, 19, 24, 29, 34, 39, 44, 49, 54, 59] and now.second == 58 and (955000 < now.microsecond <= 960000):
            b = curs_online()
            if not b == (-1):
                Data_test[index] = b - Constanta
                index += 1
            else:
                index = 0


def change_curs():
    global Neyron, status_of_work, coll_neyronov_na_uravne, answer_of_predict, status_of_data
    status_of_work = True
    for i in range(1, coll_neyronov_na_uravne - 1):
        Neyron[0][i] = Neyron[0][i + 1]
    a = curs_online()
    if not (a == (-1)):
        Neyron[0][coll_neyronov_na_uravne - 1] = a - Constanta
        if status_of_data < (coll_neyronov_na_uravne - 1):
            status_of_data += 1
    else:
        for i in range(1, coll_neyronov_na_uravne):
            Neyron[0][i] = 0
        status_of_data = 0
    status_of_work = False


def predict(index) -> object:
    OUT_Neyron_Test = 0
    global Neyron, Weight, Weights, coll_neyronov_na_uravne, coll_skrytyh_uravney, Mistake_of_test_new, OUT_Neyron
    for j1 in range(1, coll_skrytyh_uravney + 1):
        for j2 in range(0, coll_neyronov_na_uravne):
            Neyron[j1][j2] = 0
            for j3 in range(0, coll_neyronov_na_uravne):
                Neyron[j1][j2] += (Neyron[j1 - 1][j3] * Weights[j1 - 1][j2][j3])
            Neyron[j1][j2] = activation(Neyron[j1][j2])
    for j in range(0, coll_neyronov_na_uravne):
        OUT_Neyron_Test += (Neyron[coll_skrytyh_uravney][j] * Weight[j])
    OUT_Neyron_Test = round(activation(OUT_Neyron_Test), 5)
    if index:
        return OUT_Neyron_Test
    else:
        Mistake_of_test_new += (abs(1 - (OUT_Neyron_Test / OUT_Neyron)) * 100)


def save(index):
    global Weight, Weights, Weight_old, Weights_old
    if index:
        for j1 in range(0, coll_skrytyh_uravney):
            for j2 in range(0, coll_neyronov_na_uravne):
                for j3 in range(0, coll_neyronov_na_uravne):
                    Weights_old[j1][j2][j3] = Weights[j1][j2][j3]
        for j3 in range(0, coll_neyronov_na_uravne):
            Weight_old[j3] = Weight[j3]
    else:
        for j1 in range(0, coll_skrytyh_uravney):
            for j2 in range(0, coll_neyronov_na_uravne):
                for j3 in range(0, coll_neyronov_na_uravne):
                    Weights[j1][j2][j3] = Weights_old[j1][j2][j3]
        for j3 in range(0, coll_neyronov_na_uravne):
            Weight[j3] = Weight_old[j3]


def Testy(index, iteraciya):
    global Data_learn, Data_test, Iteraciya, Neyron, OUT_Neyron
    if index:
        for i in range(coll_neyronov_na_uravne):
            Neyron[0][i] = Data_learn[iteraciya + i]
        OUT_Neyron = Data_learn[iteraciya + coll_neyronov_na_uravne]
    else:
        for i in range(coll_neyronov_na_uravne):
            Neyron[0][i] = Data_test[iteraciya + i]
        OUT_Neyron = Data_test[iteraciya + coll_neyronov_na_uravne]


def learn_net():
    OUT_Neyron_Learn = 0
    global Neyron, Weight, Weights, coll_neyronov_na_uravne, coll_skrytyh_uravney, Mistake_of_test_new, Weight_d, Weights_d
    for j1 in range(1, coll_skrytyh_uravney + 1):
        for j2 in range(0, coll_neyronov_na_uravne):
            Neyron[j1][j2] = 0
            for j3 in range(0, coll_neyronov_na_uravne):
                Neyron[j1][j2] += (Neyron[j1 - 1][j3] * Weights[j1 - 1][j2][j3])
            Neyron[j1][j2] = activation(Neyron[j1][j2])
    for j in range(0, coll_neyronov_na_uravne):
        OUT_Neyron_Learn += (Neyron[coll_skrytyh_uravney][j] * Weight[j])
    OUT_Neyron_Learn = round(activation(OUT_Neyron_Learn), 5)
    Mistake_of_test_new += (abs(1 - (OUT_Neyron_Learn / OUT_Neyron)) * 100)
    OUT_Mistake = proizvodnaya(OUT_Neyron_Learn) * (OUT_Neyron - OUT_Neyron_Learn)
    for i1 in range(coll_neyronov_na_uravne):
        Weight_d[i1] = speed_of_learn * OUT_Mistake * Neyron[coll_skrytyh_uravney][i1]
        Mistake[coll_skrytyh_uravney][i1] = OUT_Mistake * proizvodnaya(Neyron[coll_skrytyh_uravney][i1]) * Weight[i1]
        for i2 in range(coll_neyronov_na_uravne):
            Weights_d[coll_skrytyh_uravney - 1][i2][i1] = speed_of_learn * Mistake[coll_skrytyh_uravney][i1] * \
                                                          Neyron[coll_skrytyh_uravney - 1][i2]
    for i1 in range(coll_skrytyh_uravney - 1, 0):
        for i2 in range(coll_neyronov_na_uravne):
            Mistake[i1][i2] = 0
            for i3 in range(coll_neyronov_na_uravne):
                Mistake[i1][i2] += (Mistake[i1 + 1][i3] * Weights[i1][i3][i2])
            Mistake[i1][i2] *= proizvodnaya(Neyron[i1][i2])
            for i3 in range(coll_neyronov_na_uravne):
                Weights_d[i1 - 1][i3][i2] = speed_of_learn * Mistake[i1][i2] * Neyron[i1 - 1][i3]

    for j1 in range(0, coll_skrytyh_uravney):
        for j2 in range(0, coll_neyronov_na_uravne):
            for j3 in range(0, coll_neyronov_na_uravne):
                Weights[j1][j2][j3] += Weights_d[j1][j2][j3]
    for j3 in range(0, coll_neyronov_na_uravne):
        Weight[j3] += Weight_d[j3]


def Learn():
    global Epoch, Iteration, Mistake_of_test_new, Mistake_of_test_old, Mistake_of_learn_old, Mistake_of_learn_new, speed_of_learn
    bot.send_message(Chat_id_root, "Сбор данных...")
    Data_for_learn()
    bot.send_message(Chat_id_root, "Сбор данных завершен")
    bot.send_message(Chat_id_root, "Обучение нейронной сети...")
    for epoha in range(Epoch):
        save(True)
        for iteration in range(Iteration):
            Testy(True, iteration)
            learn_net()
        Mistake_of_learn_new /= Iteration
        for iteration in range(Iteration):
            Testy(False, iteration)
            predict(False)
        Mistake_of_test_new /= Iteration
        if Mistake_of_learn_new < Mistake_of_learn_old:
            Mistake_of_learn_old = Mistake_of_learn_new
        elif abs(Mistake_of_learn_new - Mistake_of_learn_old) < 1e-10:
            speed_of_learn += speed_of_learn / 1000
        else:
            speed_of_learn -= speed_of_learn / 100
            save(False)
        if Mistake_of_test_new < Mistake_of_test_old:
            Mistake_of_test_old = Mistake_of_test_new
        elif Mistake_of_test_new > Mistake_of_test_old:
            save(False)
            bot.send_message(Chat_id_root, str(Mistake_of_test_old))
            break
    bot.send_message(Chat_id_root, "Обучение нейронной сети завершено")


@bot.message_handler(commands=['start'])
def start(message: Message):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    curs = telebot.types.KeyboardButton("Курс")
    prediction = telebot.types.KeyboardButton("Прогнозировать")
    keyboard.add(*[curs, prediction])
    bot.send_message(message.chat.id, text="Добро пожаловать в Forex_Curs_Play", reply_markup=keyboard)


@bot.message_handler(commands=['stop'])
def stop(message: Message):
    bot.send_message(message.chat.id, text="Бот остановлен!")
    bot.stop_polling()
    time.sleep(30)
    bot.polling()


@bot.message_handler(func=lambda message: True)
def answer_to_message(message: Message):
    answer = message.text
    global Neyron, status_of_work, status_of_data, minute
    if answer in ["curs", "Курс", "курс"]:
        bot.reply_to(message, "Курс Евро к Доллару:\n" + str(curs_online()))
    elif answer in ["predict", "Прогнозировать", "прогнозировать"]:
        if not status_of_work:
            if status_of_data == (coll_neyronov_na_uravne - 1):
                bot.send_message(message.chat.id,
                                 "Прогнозируемый курс Евро к Доллару через 5 минут:\n" + str(predict(True)))
            else:
                Time = coll_neyronov_na_uravne - status_of_data - 1
                if (Time % 10 == 1) and (not Time == 11):
                    minute = " минута!"
                elif (Time % 10 in [2, 3, 4]) and (not (Time in [12, 13, 14])):
                    minute = " минуты!"
                elif (Time % 10 >= 5) or (Time % 10 == 0) or (Time in [11, 12, 13, 14]):
                    minute = " минут!"
                bot.reply_to(message,
                             "Мы не готовы к прогнозированию! \n Повторите попытку через " + str(Time) + minute)
        else:
            bot.reply_to(message, "Повторите попытку через 5 секунд!")
    else:
        bot.reply_to(message, "Запрос не понятен!")

def start_bot():
    bot.polling(none_stop=True)


def start_checker() -> object:
    while True:
        now = datetime.datetime.now()
        if (now.hour == 23 - DeltaTime) and now.minute == 56:
            Learn()
        if now.minute in [4, 9, 14, 19, 24, 29, 34, 39, 44, 49, 54, 59] and now.second == 58 and (
                955000 < now.microsecond <= 960000):
            change_curs()


bot_process = threading.Thread(target=start_bot)
checker = threading.Thread(target=start_checker)
checker.start()
bot_process.start()
