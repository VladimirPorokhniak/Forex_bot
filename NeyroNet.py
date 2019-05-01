from Function import *
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
Data_test = [0 for i in range(Iteration + coll_neyronov_na_uravne)]
Data_learn = [0 for i in range(Iteration + coll_neyronov_na_uravne)]
Neyron = [[0 for i11 in range(coll_neyronov_na_uravne)] for i12 in range(coll_skrytyh_uravney + 1)]
Mistake = [[0 for i11 in range(coll_neyronov_na_uravne)] for i12 in range(coll_skrytyh_uravney + 1)]
OUT_Neyron = 0
Weights = []
for i23 in range(coll_skrytyh_uravney):
    Weights.append(
        [[randomer() for i21 in range(coll_neyronov_na_uravne)] for i22 in range(coll_neyronov_na_uravne)])
Weight = [randomer() for i in range(coll_neyronov_na_uravne)]
Weights_d = []
for i23 in range(coll_skrytyh_uravney):
    Weights_d.append([[0 for i21 in range(coll_neyronov_na_uravne)] for i22 in range(coll_neyronov_na_uravne)])
Weight_d = [0 for i in range(coll_neyronov_na_uravne)]
Weights_old = []
for i23 in range(coll_skrytyh_uravney):
    Weights_old.append([[0 for i21 in range(coll_neyronov_na_uravne)] for i22 in range(coll_neyronov_na_uravne)])
Weight_old = [0 for i in range(coll_neyronov_na_uravne)]


def start() -> object:
    global Data_learn, Data_test, Iteration, coll_neyronov_na_uravne
    b = Iteration + coll_neyronov_na_uravne
    with open("learn.txt") as learn:
        for i in range(b):
            Data_learn[i] = float(learn.readline()) - Constanta
    with open("test.txt") as test:
        for i in range(b):
            Data_test[i] = float(test.readline()) - Constanta


def save(index):
    global Weight, Weights, Weight_old, Weights_old, coll_neyronov_na_uravne, coll_skrytyh_uravney
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


def Testy(index, iteration):
    global Data_learn, Data_test, Neyron, OUT_Neyron
    if index:
        for i in range(coll_neyronov_na_uravne):
            Neyron[0][i] = Data_learn[iteration + i]
        OUT_Neyron = Data_learn[iteration + coll_neyronov_na_uravne]
    else:
        for i in range(coll_neyronov_na_uravne):
            Neyron[0][i] = Data_test[iteration + i]
        OUT_Neyron = Data_test[iteration + coll_neyronov_na_uravne]


def learn_net():
    OUT_Neyron_Learn = 0
    global Neyron, Weight, Weights, coll_neyronov_na_uravne, coll_skrytyh_uravney, Mistake_of_learn_new, Weight_d, Weights_d
    for j1 in range(1, coll_skrytyh_uravney + 1):
        for j2 in range(0, coll_neyronov_na_uravne):
            Neyron[j1][j2] = 0
            for j3 in range(0, coll_neyronov_na_uravne):
                Neyron[j1][j2] += (Neyron[j1 - 1][j3] * Weights[j1 - 1][j2][j3])
            Neyron[j1][j2] = activation(Neyron[j1][j2])
    for j in range(0, coll_neyronov_na_uravne):
        OUT_Neyron_Learn += (Neyron[coll_skrytyh_uravney][j] * Weight[j])
    OUT_Neyron_Learn = round(activation(OUT_Neyron_Learn), 5)
    Mistake_of_learn_new += (abs(1 - (OUT_Neyron_Learn / OUT_Neyron)) * 100)
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


def test_net():
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
    Mistake_of_test_new += (abs(1 - (OUT_Neyron_Test / OUT_Neyron)) * 100)


def Learn():
    global Epoch, Iteration, Mistake_of_test_new, Mistake_of_test_old, Mistake_of_learn_old, Mistake_of_learn_new, speed_of_learn
    for epoch in range(Epoch):
        save(True)
        for iteration in range(Iteration):
            Testy(True, iteration)
            learn_net()
        Mistake_of_learn_new /= Iteration
        for iteration in range(Iteration):
            Testy(False, iteration)
            test_net()
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
            print("Mistake of net is :" + str(Mistake_of_test_old))
            break


start()
Learn()

