import datetime
import telebot
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

TOKEN = "872334684:AAFOj0LlgVPW5RQhNNPYR7mqLyUkzkSa6BQ"
Chat_id_root: int = 448157691
count = 0
bot = telebot.TeleBot(TOKEN, threaded=False)


def curs_online():
    global count
    wd = webdriver.PhantomJS(executable_path=os.path.abspath('phantomjs'))
    wd.get("https://www.fxclub.org/markets/forex/eur-usd/")
    WebDriverWait(wd, 1)
    page = wd.page_source
    wd.quit()
    p = page
    index = page.find("Котировка:")
    a = page[index + 11:index + 200]
    index = a.find("</span>")
    a = a[index - 10:index]
    a = a[a.find(">") + 1:index]
    a = a.replace(",", '.')
    try:
        a = round(float(a), 5)
    except ValueError:
        count -= 1
        bot.send_message(Chat_id_root, "ERROR")
        print(p)
    return a


for count in range(108):
    while True:
        now = datetime.datetime.now()
        if now.minute in [4, 9, 14, 19, 24, 29, 34, 39, 44, 49, 54, 59] and now.second == 58 and (955000 < now.microsecond <= 960000):
            bot.send_message(Chat_id_root, str(curs_online()))
            Time = (coll_neyronov_na_uravne - status_of_full - 1) * 5
            break
