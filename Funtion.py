import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

TOKEN = '706327123:AAHuPNEyFC57Y5XbIXOWCQ32e6ii9Gfpon0'
Chat_id_root = 448157691
DeltaTime = 3
MAX_neyronov_na_uravne = 100 + 1
MAX_skrytyh_uravney = 100
MAX_na_vhod = 30
Constanta = 1
Iteration = 10
Epoch = 10000000
Coll_NeyroNETS = 1000000


def curs_online(curs='eur-usd'):
    wd = webdriver.PhantomJS(executable_path=os.path.abspath('phantomjs'))
    url = "https://www.fxclub.org/markets/forex/" + curs + "/"
    wd.get(url)
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



