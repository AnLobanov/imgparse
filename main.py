from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
import csv, os, random, time
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
from urllib.parse import unquote
from PIL import Image

# Отключаем GUI браузера

options = Options()
options.headless = True

rootdir = os.getcwd()

por = int(input('Какое изобрежение из выдачи по счету скачать: '))

# Подключаемся к файлу в формате CSV с разделителем ;

f = open('НетфотоУютсити.csv', 'r', encoding='utf-8')
reader = csv.reader(f, delimiter=';')

# Если папки нет - создаем

if not os.path.exists('imgs'):
    os.mkdir('imgs')

delay = random.randint(2, 7)

queue = 0
category = ''
for row in list(reader):
    if row[0] == '':
        category = row[1]
    if not os.path.exists(rootdir + '/imgs/' + category):
        os.mkdir(rootdir + '/imgs/' + category)
    if not row[0] == '':
        if not os.path.isfile(rootdir + '/imgs/' + category + '/' + row[0] + '_' + str(por) + '.png'):
            os.chdir(rootdir)

            # Загружаем страницу и ее код
            try:
                driver = Firefox(executable_path=os.getcwd() + '/geckodriver', options = options)
                driver.get('https://yandex.ru/images/search?text=' + row[1])
                soup = BeautifulSoup(driver.page_source, features='html5lib')
                driver.quit()
                img = unquote(soup.findAll('a', {"class": "serp-item__link"})[por - 1]['href'].split('&')[1][8:])
            except IndexError:
                time.sleep(random.uniform(10, 20))
                driver = Firefox(executable_path=os.getcwd() + '/geckodriver', options = options)
                driver.get('https://yandex.ru/images/search?text=' + row[1])
                soup = BeautifulSoup(driver.page_source, features='html5lib')
                driver.quit()
                img = unquote(soup.findAll('a', {"class": "serp-item__link"})[por - 1]['href'].split('&')[1][8:])
            os.chdir(rootdir + '/imgs/' + category)

            # Скачиваем 1 изображение из Яндекс.Картинок в папку с артикулом

            os.chdir(rootdir + '/imgs/' + category)
            urlretrieve(img, row[0] + '_' + str(por) + '.png')

            # Ждем следующий запрос

            queue += 1
            if queue == delay:
                time.sleep(random.uniform(30, 120))
                delay = random.randint(2, 7)
                queue = 0