from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
import csv, os, random, time
from bs4 import BeautifulSoup
from urllib.request import URLopener, urlretrieve
from urllib.parse import unquote
from tqdm import tqdm
from glob import glob
URLopener.version = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0'

# Отключаем GUI браузера

options = Options()
options.headless = True

rootdir = os.getcwd()

por = int(input('Какое изобрежение из выдачи по счету скачать: '))

# Подключаемся к файлу в формате CSV с разделителем ;

f = open('НетфотоУютсити.csv', 'r', encoding='utf-8')
reader = list(csv.reader(f, delimiter=';'))
artkls = []
for i in reader:
    artkls.append(i[0])
# Если папки нет - создаем

if not os.path.exists('imgs'):
    os.mkdir('imgs')

delay = random.randint(2, 7)

for elm in glob(rootdir + '/imgs/*/*'):
    fl = elm.split('/')[-1][:-6]
    if fl in artkls:
        indx = artkls.index(fl)
        artkls.pop(indx)
        reader.pop(indx)

queue = 0
category = ''
for row in tqdm(reader):
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
            except IndexError:
                time.sleep(random.uniform(10, 20))
                driver = Firefox(executable_path=os.getcwd() + '/geckodriver', options = options)
                driver.get('https://yandex.ru/images/search?text=' + row[1])
                soup = BeautifulSoup(driver.page_source, features='html5lib')
                driver.quit()
            os.chdir(rootdir + '/imgs/' + category)
            # Скачиваем 1 изображение из Яндекс.Картинок в папку с артикулом
            result = None
            x = por 
            while result is None:
                try:
                    # connect
                    img = unquote(soup.findAll('a', {"class": "serp-item__link"})[x]['href'].split('&')[1][8:])
                    result = urlretrieve(img, row[0] + '_' + str(x) + '.png')
                except:
                    x += 1
                    pass
            # Ждем следующий запрос

            queue += 1
            if queue == delay:
                time.sleep(random.uniform(30, 120))
                delay = random.randint(2, 7)
                queue = 0