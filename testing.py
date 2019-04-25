import datetime
import telebot
from Function import *

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
status_of_work = 0
status_of_training = 0
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
    global Neyron, status_of_work, coll_neyronov_na_uravne, answer_of_predict
    for i in range(1, coll_neyronov_na_uravne - 1):
        Neyron[0][i] = Neyron[0][i + 1]
    a = curs_online()
    if not (a == (-1)):
        Neyron[0][coll_neyronov_na_uravne - 1] = a - Constanta
        if status_of_work < (coll_neyronov_na_uravne - 1):
            status_of_work += 1
    else:
        for i in range(1, coll_neyronov_na_uravne):
            Neyron[0][i] = 0
        status_of_work = 0
    if status_of_work == (coll_neyronov_na_uravne - 1):
        msg = "{0}\n{1}\n Mistake is :{2}%".format(str(answer_of_predict), str(Neyron[0][coll_neyronov_na_uravne - 1]),
                                                   str(
                                                       round(abs(1 - (answer_of_predict / Neyron[0][
                                                           coll_neyronov_na_uravne - 1])) * 100, 5)))
        bot.send_message(Chat_id_root, msg)
        answer_of_predict = predict(True)


def predict(index) -> object:
    out_neyron = 0
    global Neyron, Weight, Weights, coll_neyronov_na_uravne, coll_skrytyh_uravney, Mistake_of_test_new, OUT_Neyron
    for j1 in range(1, coll_skrytyh_uravney + 1):
        for j2 in range(0, coll_neyronov_na_uravne):
            Neyron[j1][j2] = 0
            for j3 in range(0, coll_neyronov_na_uravne):
                Neyron[j1][j2] += (Neyron[j1 - 1][j3] * Weights[j1 - 1][j2][j3])
            Neyron[j1][j2] = activation(Neyron[j1][j2])
    for j in range(0, coll_neyronov_na_uravne):
        out_neyron += (Neyron[coll_skrytyh_uravney][j] * Weight[j])
    out_neyron = round(activation(out_neyron), 5)
    if index:
        return out_neyron
    else:
        Mistake_of_test_new += (abs(1 - (out_neyron / OUT_Neyron)) * 100)


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
    print("Сбор данных...")
    Data_for_learn()
    bot.send_message(Chat_id_root, "Сбор данных завершен")
    print("Сбор данных завеншен")
    print(Weights)
    print("\n\n")
    print(Weight)
    bot.send_message(Chat_id_root, "Обучение нейронной сети...")
    print("Обучение нейронной сети...")
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
    print("\n\n\n\n")
    print(Weights)
    print("\n\n")
    print(Weight)
    bot.send_message(Chat_id_root, "Обучение нейронной сети завершено")
    print("Обучение нейронной сети завершено")


def start_checker() -> object:
    while True:
        now = datetime.datetime.now()
        if now.hour == 17 and now.minute == 48:
            Learn()
        if now.minute in [4, 9, 14, 19, 24, 29, 34, 39, 44, 49, 54, 59] and now.second == 58 and (
                955000 < now.microsecond <= 960000):
            change_curs()


start_checker()
