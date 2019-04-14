import datetime
import math
import telebot
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

TOKEN = '706327123:AAHVz1o6OxOMwl4Vma5RAG5RlQ8f-U44tjM'
Chat_id_root = 448157691
coll_neyronov_na_uravne: int = 3  # 1 + 2
coll_skrytyh_uravney: int = 2
Constanta = 1
ANSWER = 0
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
    global Neyron, status_full, coll_neyronov_na_uravne, ANSWER
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
    if status_full == (coll_neyronov_na_uravne - 1):
        msg = str(ANSWER) + "\n" + str(Neyron[0][coll_neyronov_na_uravne - 1]) + "\n Mistake is :" + str(abs(1 - (ANSWER / Neyron[0][coll_neyronov_na_uravne - 1])) * 100) + "%"
        bot.send_message(Chat_id_root, msg)
        ANSWER = predict()


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
    return out_neyron


def start_checker():
    while True:
        while True:
            now = datetime.datetime.now()
            if now.minute in [4, 9, 14, 19, 24, 29, 34, 39, 44, 49, 54, 59] and now.second == 58 and (
                    955000 < now.microsecond <= 960000):
                change_curs()
                break


start_program()
start_checker()
