from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
import csv, os, random, time
from bs4 import BeautifulSoup
from urllib.request import urlretrieve

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
for row in list(reader)[173:178]:
    print(row)
    if row[0] == '':
        print('КАТЕГОРИЯ')
        category = row[1]
        os.mkdir(rootdir + '/imgs/' + category)
    else:
        if not os.path.isfile(rootdir + '/imgs/' + category +  '/' + row[0] + '/' + row[0] + '_' + str(por) + '.png'):
            os.chdir(rootdir)

            # Загружаем страницу и ее код
            try:
                driver = Firefox(executable_path=os.getcwd() + '/geckodriver', options = options)
                driver.get('https://yandex.ru/images/search?text=' + row[1])
                soup = BeautifulSoup(driver.page_source, features='html5lib')
                driver.quit()
                img = 'https:' + soup.findAll('img', {"class": "serp-item__thumb justifier__thumb"}, src = True)[por - 1]['src']
            except IndexError:
                time.sleep(random.uniform(10, 20))
                driver = Firefox(executable_path=os.getcwd() + '/geckodriver', options = options)
                driver.get('https://yandex.ru/images/search?text=' + row[1])
                soup = BeautifulSoup(driver.page_source, features='html5lib')
                driver.quit()
                img = 'https:' + soup.findAll('img', {"class": "serp-item__thumb justifier__thumb"}, src = True)[por - 1]['src']
            os.chdir(rootdir + '/imgs/' + category)

            # Скачиваем 1 изображение из Яндекс.Картинок в папку с артикулом

            if not os.path.exists(rootdir + '/imgs/' + '/' + row[0]):
                os.mkdir(rootdir + '/imgs/' + category + '/' + row[0])
            os.chdir(rootdir + '/imgs/' + category + '/' + row[0])
            urlretrieve(img, row[0] + '_' + str(por) + '.png')

            # Ждем следующий запрос

            queue += 1
            if queue == delay:
                time.sleep(random.uniform(30, 120))
                delay = random.randint(2, 7)