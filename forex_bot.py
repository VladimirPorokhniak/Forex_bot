import datetime
import math
import threading
import telebot
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from telebot.types import Message

TOKEN = '706327123:AAHVz1o6OxOMwl4Vma5RAG5RlQ8f-U44tjM'
Chat_id_root = 448157691
coll_neyronov_na_uravne: int = 3  # 1 + 2
coll_skrytyh_uravney: int = 2
Constanta = 1
status_process = False
status_full = 0
Neyron = [[0 for i11 in range(coll_neyronov_na_uravne)] for i12 in range(coll_skrytyh_uravney + 1)]
Weights = [[[0 for i21 in range(coll_neyronov_na_uravne)] for i22 in range(coll_neyronov_na_uravne)] for i23 in
           range(coll_skrytyh_uravney)]
Weight = [0 for i in range(coll_neyronov_na_uravne)]

bot = telebot.TeleBot(TOKEN, threaded=False)


def start_program():
    global Weight, Weights, coll_neyronov_na_uravne
    with open('Weight.txt', 'r') as weight_in:
        a = weight_in.read()
    a = a.replace("\n", "")
    a = a.split(" ")
    index = 0
    for j in range(coll_skrytyh_uravney):
        for j1 in range(coll_neyronov_na_uravne):
            for j2 in range(coll_neyronov_na_uravne):
                Weights[j][j1][j2] = float(a[index])
                index += 1
    for j in range(coll_neyronov_na_uravne):
        Weight[j] = float(a[index])
        index += 1


def activation(x):
    a = (2 / (1 + math.exp(-x))) - 1
    return a


def curs_online():
    wd = webdriver.PhantomJS(executable_path=os.path.abspath('phantomjs'))
    wd.get("https://www.fxclub.org/markets/forex/eur-usd/")
    WebDriverWait(wd, 1)
    page = wd.page_source
    wd.quit()
    index = page.find("Котировка:")
    p = page
    a = page[index + 11:index + 200]
    index = a.find("</span>")
    a = a[index - 10:index]
    a = a[a.find(">") + 1:index]
    a = a.replace(",", '.')
    try:
        a = round(float(a), 5)
    except ValueError:
        a = -1
    return a


def change_curs():
    global Neyron, status_process, status_full, coll_neyronov_na_uravne
    status_process = True
    for i in range(1, coll_neyronov_na_uravne - 1):
        Neyron[0][i] = Neyron[0][i + 1]
    a = curs_online()
    if not (a == (-1)):
        Neyron[0][coll_neyronov_na_uravne - 1] = a - Constanta
        if status_full < (coll_neyronov_na_uravne - 1):
            status_full += 1
    else:
        for i in range(1, coll_neyronov_na_uravne):
            Neyron[0][i] = 0
        status_full = 0
    status_process = False


def predict():
    out_neyron = 0
    global Neyron, Weight, Weights, coll_neyronov_na_uravne, coll_skrytyh_uravney
    for j1 in range(1, coll_skrytyh_uravney + 1):
        for j2 in range(1, coll_neyronov_na_uravne):
            Neyron[j1][j2] = 0
            for j3 in range(1, coll_neyronov_na_uravne):
                Neyron[j1][j2] += (Neyron[j1 - 1][j3] * Weights[j1 - 1][j2][j3])
            Neyron[j1][j2] += Weights[j1 - 1][0][j2]
            Neyron[j1][j2] = activation(Neyron[j1][j2])
    for j in range(1, coll_neyronov_na_uravne):
        out_neyron += (Neyron[coll_skrytyh_uravney][j] * Weight[j])
    out_neyron += Weight[0]
    out_neyron = round(activation(out_neyron), 5)
    return out_neyron + Constanta


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


@bot.message_handler(func=lambda message: True)
def answer_to_message(message: Message):
    answer = message.text
    global Neyron, status_full, status_process, minute
    if answer in ["curs", "Курс", "курс"]:
        bot.reply_to(message, "Курс Евро к Доллару:\n" + str(curs_online()))
    if answer in ["predict", "Прогнозировать", "прогнозировать"]:
        if not status_process:
            if status_full == (coll_neyronov_na_uravne - 1):
                bot.send_message(message.chat.id,
                                 "Прогнозируемый курс Евро к Доллару через 5 минут:\n" + str(predict()))
            else:
                Time = coll_neyronov_na_uravne - status_full - 1
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


def start_bot():
    bot.polling(none_stop=True)


def start_checker():
    while True:
        while True:
            now = datetime.datetime.now()
            if now.minute in [4, 9, 14, 19, 24, 29, 34, 39, 44, 49, 54, 59] and now.second == 58 and (955000 < now.microsecond <= 960000):
                change_curs()
                break


start_program()
bot_process = threading.Thread(target=start_bot)
checker = threading.Thread(target=start_checker)
checker.start()
bot_process.start()
