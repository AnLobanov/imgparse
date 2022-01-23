from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import csv, os
from bs4 import BeautifulSoup
from urllib.request import urlretrieve

# Отключаем GUI браузера

options = Options()
options.headless = True

rootdir = os.getcwd()

# Подключаемся к файлу в формате CSV с разделителем ;

f = open('СписокНоменклатур.csv', 'r', encoding='utf-8')
reader = csv.reader(f, delimiter=';')

# Если папки нет - создаем

if not os.path.exists('imgs'):
    os.mkdir('imgs')

for row in list(reader)[1:26]:
    os.chdir(rootdir)

    # Загружаем страницу и ее код
    # ОБЯЗАТЕЛЬНО УКАЗЫВАЕМ ПУТЬ К FIREFOX

    driver = Firefox(firefox_binary = FirefoxBinary('/usr/bin/firefox'), executable_path=os.getcwd() + '/geckodriver', options = options)
    driver.get('https://yandex.ru/images/search?text=' + row[0])
    soup = BeautifulSoup(driver.page_source, features='html5lib')
    driver.quit()
    img = 'https:' + soup.find('img', {"class": "serp-item__thumb justifier__thumb"}, src = True)['src']
    os.chdir('imgs')

    # Скачиваем 1 изображение из Яндекс.Картинок в папку с артикулом

    if not os.path.exists(row[1]):
        os.mkdir(row[1])
        os.chdir(row[1])
        urlretrieve(img, row[1] + '.png')
