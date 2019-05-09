from Funtion import MAX_neyronov_na_uravne, MAX_skrytyh_uravney, Coll_NeyroNETS, Iteration, Epoch, TOKEN, Chat_id_root
from math import exp
import random, telebot

bot1 = telebot.TeleBot(TOKEN, threaded=False)

coll_skrytyh_uravney = 0
coll_neyronov_na_vhod = 0
speed_of_learn = 1
Mistake_of_learn_new = 0
Mistake_of_learn_old = 0
Mistake_of_test_new = 0
Mistake_of_test_old = 0
coll_neyronov_na_uravne = [0 for i in range(MAX_skrytyh_uravney + 1)]
Neyron = [[0 for i1 in range(MAX_neyronov_na_uravne)] for i2 in range(MAX_skrytyh_uravney + 1)]
OUT_Neyron = 0
Mistake = [[0 for i1 in range(MAX_neyronov_na_uravne)] for i2 in range(MAX_skrytyh_uravney + 1)]
Weights = [[[0 for i1 in range(MAX_neyronov_na_uravne)] for i2 in range(MAX_neyronov_na_uravne)] for i3 in
           range(MAX_skrytyh_uravney)]
Weights_d = [[[0 for i1 in range(MAX_neyronov_na_uravne)] for i2 in range(MAX_neyronov_na_uravne)] for i3 in
             range(MAX_skrytyh_uravney)]
Weights_old = [[[0 for i1 in range(MAX_neyronov_na_uravne)] for i2 in range(MAX_neyronov_na_uravne)] for i3 in
               range(MAX_skrytyh_uravney)]
Data_test = []
Data_learn = []


def activation(x):
    try:
        a = (1 / (1 + exp(-x)))
    except OverflowError:
        a = -10
    return a


def proizvodnaya(x):
    return x * (1 - x)


def randomer(index=True) -> object:
    b = 10000
    if index:
        a = random.randint(0 - b, b)
        a /= (b / 10)
    else:
        a = random.randint(1, MAX_neyronov_na_uravne)
    return a


def Make_Data(Data_list, coll_na_vhode):
    global Data_test, Data_learn
    size = coll_na_vhode + Iteration
    for i in range(size):
        Data_learn.append(Data_list[i])
    for i in range(size, 2 * size):
        Data_test.append(Data_list[i])


def random_weight():
    global Weights, Weights_old, Weights_d
    global coll_skrytyh_uravney, coll_neyronov_na_uravne, Neyron, Mistake
    global Mistake_of_test_old, Mistake_of_test_new, Mistake_of_learn_old, Mistake_of_learn_new, speed_of_learn
    coll_neyronov_na_uravne[0] = coll_neyronov_na_vhod
    coll_neyronov_na_uravne[coll_skrytyh_uravney] = 1
    for i1 in range(1, coll_skrytyh_uravney):
        coll_neyronov_na_uravne[i1] = randomer(False)
    for i1 in range(coll_skrytyh_uravney):
        for i2 in range(coll_neyronov_na_uravne[i1]):
            for i3 in range(coll_neyronov_na_uravne[i1 + 1]):
                Weights[i1][i2][i3] = randomer()
    speed_of_learn = 1
    Mistake_of_learn_old = 1000
    Mistake_of_test_old = 1000
    Mistake_of_learn_new = 0
    Mistake_of_test_new = 0


def test_net(index) -> object:
    global Neyron, OUT_Neyron, Weights, coll_neyronov_na_uravne, coll_skrytyh_uravney, Mistake_of_test_new
    for j1 in range(1, coll_skrytyh_uravney + 1):
        for j3 in range(0, coll_neyronov_na_uravne[j1]):
            Neyron[j1][j3] = 0
            for j2 in range(0, coll_neyronov_na_uravne[j1 - 1]):
                Neyron[j1][j3] += (Neyron[j1 - 1][j2] * Weights[j1 - 1][j2][j3])
            b = activation(Neyron[j1][j3])
            if not b == (-10):
                Neyron[j1][j3] = b
            else:
                return 100
    OUT_Neyron_Test = Neyron[coll_skrytyh_uravney][0]
    Mistake_of_test_new += (abs(1 - (OUT_Neyron_Test / OUT_Neyron)) * 100)


def save(index):
    global Weights, Weights_old, coll_neyronov_na_uravne, coll_skrytyh_uravney
    if index:
        for j1 in range(coll_skrytyh_uravney):
            for j2 in range(coll_neyronov_na_uravne[j1]):
                for j3 in range(coll_neyronov_na_uravne[j1 + 1]):
                    Weights_old[j1][j2][j3] = Weights[j1][j2][j3]
    else:
        for j1 in range(coll_skrytyh_uravney):
            for j2 in range(coll_neyronov_na_uravne[j1]):
                for j3 in range(coll_neyronov_na_uravne[j1 + 1]):
                    Weights[j1][j2][j3] = Weights_old[j1][j2][j3]


def testy(index, iteration):
    global Data_learn, Data_test, Neyron, OUT_Neyron
    if index:
        for i in range(coll_neyronov_na_vhod):
            Neyron[0][i] = Data_learn[iteration + i]
        OUT_Neyron = Data_learn[iteration + coll_neyronov_na_vhod]
    else:
        for i in range(coll_neyronov_na_vhod):
            Neyron[0][i] = Data_test[iteration + i]
        OUT_Neyron = Data_test[iteration + coll_neyronov_na_vhod]


def learn_net():
    global Neyron, OUT_Neyron, Weights, Weights_d, coll_neyronov_na_uravne, coll_skrytyh_uravney, Mistake_of_learn_new
    for j1 in range(1, coll_skrytyh_uravney + 1):
        for j3 in range(0, coll_neyronov_na_uravne[j1]):
            Neyron[j1][j3] = 0
            for j2 in range(0, coll_neyronov_na_uravne[j1 - 1]):
                Neyron[j1][j3] += (Neyron[j1 - 1][j2] * Weights[j1 - 1][j2][j3])
            b = activation(Neyron[j1][j3])
            if not b == (-10):
                Neyron[j1][j3] = b
            else:
                return 100
    OUT_Neyron_Learn = Neyron[coll_skrytyh_uravney][0]
    Mistake_of_learn_new += (abs(1 - (OUT_Neyron_Learn / OUT_Neyron)) * 100)
    Mistake[coll_skrytyh_uravney][0] = proizvodnaya(OUT_Neyron_Learn) * (OUT_Neyron - OUT_Neyron_Learn)
    for i in range(coll_neyronov_na_uravne[coll_skrytyh_uravney - 1]):
        Weights_d[coll_skrytyh_uravney - 1][i][0] = \
            speed_of_learn * Mistake[coll_skrytyh_uravney][0] * Neyron[coll_skrytyh_uravney - 1][i]
    for i1 in range(coll_skrytyh_uravney - 1, 0):
        for i3 in range(coll_neyronov_na_uravne[i1]):
            Mistake[i1][i3] = 0
            for i4 in range(coll_neyronov_na_uravne[i1 + 1]):
                Mistake[i1][i3] += Mistake[i1 + 1][i4] * Weights[i1][i3][i4]
            Mistake[i1][i3] *= proizvodnaya(Neyron[i1][i3])
            for i2 in range(coll_neyronov_na_uravne[i1 - 1]):
                Weights_d[i1 - 1][i2][i3] = speed_of_learn * Mistake[i1][i3] * Neyron[i1 - 1][i2]
    for j1 in range(coll_skrytyh_uravney):
        for j2 in range(coll_neyronov_na_uravne[j1]):
            for j3 in range(coll_neyronov_na_uravne[j1 + 1]):
                Weights[j1][j2][j3] += Weights_d[j1][j2][j3]


def Learning():
    global speed_of_learn
    global Mistake_of_test_new, Mistake_of_test_old, Mistake_of_learn_old, Mistake_of_learn_new
    random_weight()
    for epoch in range(Epoch):
        save(True)
        for iteration in range(Iteration):
            testy(True, iteration)
            if learn_net() == 100:
                return 0
        Mistake_of_learn_new /= Iteration
        for iteration in range(Iteration):
            testy(False, iteration)
            if test_net(False) == 100:
                return 0
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
            return Mistake_of_test_old


def LearnNet(Data_list, coll_skr, coll_neyronov_na_vhode):
    global coll_skrytyh_uravney, coll_neyronov_na_vhod
    coll_skrytyh_uravney = coll_skr
    coll_neyronov_na_vhod = coll_neyronov_na_vhode
    Make_Data(Data_list, coll_neyronov_na_vhode)
    WELL_Mistake_of_Net = 1000
    WELL_coll_neyronov_na_uravne = 0
    for i in range(Coll_NeyroNETS):
        a = Learning()
        if i % 200000 == 0:
            bot1.send_message(Chat_id_root, "Обучение сети(" + str(coll_neyronov_na_vhod) + "_" + str(coll_skr - 1)
                              + "): " + str(int(i / 10000)) + "%")
        if a < WELL_Mistake_of_Net:
            WELL_Mistake_of_Net = a
            WELL_coll_neyronov_na_uravne = coll_neyronov_na_uravne
    return WELL_Mistake_of_Net, WELL_coll_neyronov_na_uravne
