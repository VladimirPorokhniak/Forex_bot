import telebot
from Funtion import *
from NeyroNetLearn import LearnNet

bot = telebot.TeleBot(TOKEN, threaded=False)


def Data() -> object:
    size = MAX_na_vhod + Iteration
    Data_list = [0 for i in range(2 * size)]
    with open("Data_test.txt", "r") as data:
        for i in range(2 * size):
            Data_list[i] = float(data.readline()) - Constanta
    return Data_list


def look_for_net():
    bot.send_message(Chat_id_root, "Сбор данных...")
    Data_list = Data()
    bot.send_message(Chat_id_root, "Сбор данных завершен")
    bot.send_message(Chat_id_root, "Обучение нейронных сетей...")
    id_number = 1
    for vhod in range(1, MAX_na_vhod + 1):
        for skr in range(1, MAX_skrytyh_uravney + 1):
            Mistake_of_net, coll_neyronov_na_uravne = LearnNet(Data_list, skr, vhod)
            neyron = ""
            for i in range(skr + 1):
                neyron += str(coll_neyronov_na_uravne[i])
                if not i == skr:
                    neyron += "_"
            bot.send_message(Chat_id_root, str(id_number) + " Mistake_of(" + str(vhod) + "_" + str(skr - 1) + ")= " +
                             str(Mistake_of_net) + "  " + neyron)
            id_number += 1
    bot.send_message(Chat_id_root, "Обучение нейронных сетей завершено")


look_for_net()
