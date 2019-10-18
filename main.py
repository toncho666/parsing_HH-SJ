from pprint import pprint
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd


# ДЛЯ SUPERJOB
headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/77.0.3865.120 Safari/537.36'}
# задаем глубину поиска информации (количество страниц)
pgs_sj = 3
# задаем должность для поиска
post_sj = 'python'
# ссылка для поиска вакансий
link_sj = 'https://www.superjob.ru/vacancy/search/?keywords=python&geo%5Bc%5D%5B0%5D=1'
# главная страница
main_link_sj = 'https://www.superjob.ru'
geo = '&geo%5Bc%5D%5B0%5D=1'

html_sj = requests.get(link_sj, headers=headers).text
parsed_html_sj = bs(html_sj, 'lxml')#собираем данные с ссылки запроса

# получаем ссылку перехода на следующую страницу (кнопка "дальше")
next_link=parsed_html_sj.find('a', {'class': 'icMQ_ _1_Cht _3ze9n f-test-button-dalshe f-test-link-dalshe'})['href']

# форируем из этой ссылки "рабочую заготовку" (без последней цифры)
link_new_sj = main_link_sj + next_link[:-1]

# создаем список ссылок (первые три страницы)
pages_sj = []
# создаем список для хранения данных со страниц по запросам (цикл "for vac in vacancies_list_hh")

vacancies_sj = []

# наполняем список pages ссылками
for i in range(1, pgs_sj+1):
    url = link_new_sj + str(i)
    pages_sj.append(url)


for item in pages_sj:

    # опять же обращение к странице
    page_sj = requests.get(item, headers=headers).text
    parser_sj = bs(page_sj, 'lxml')



    vacancies_list_sj = parser_sj.findChildren('div', {'class': ['_3zucV _2GPIV f-test-vacancy-item i6-sc _3VcZr']})



    for vac in vacancies_list_sj:

        vac_data_sj={}
        #наименование вакансии
        vac_name = vac.find('div', {'class': '_3mfro CuJz5 PlM3e _2JVkc _3LJqf'}).getText()

        #ссылка на вакансию
        vac_link = vac.find('div', {'class': '_3mfro CuJz5 PlM3e _2JVkc _3LJqf'}).findParent()
        link = main_link_sj+vac_link['href']

        # ЗП
        vac_sal = vac.find('span',
                           {'class': '_3mfro _2Wp8I f-test-text-company-item-salary PlM3e _2JVkc _2VHxz'}).getText()

        # город
        vac_city = vac.find('span',
                            {'class': '_3mfro _9fXTd _2JVkc _3e53o _3Ll36'}).find_next().getText()

        #наименование работодателя
        if vac.find('span', {'class': '_3mfro _3Fsn4 f-test-text-vacancy-item-company-name _9fXTd _2JVkc _3e53o _15msI'})is None:
            vac_emp = "Работодатель не указан"
        else:
            vac_emp = vac.find('span', {'class': '_3mfro _3Fsn4 f-test-text-vacancy-item-company-name _9fXTd _2JVkc _3e53o _15msI'}).getText()


        vac_data_sj = {'Name': vac_name,
                        'Earn': vac_sal,
                        'Link': link,
                        'Main_link': main_link_sj,
                        'Employer': vac_emp,
                        'City': vac_city
                       }
        vacancies_sj.append(vac_data_sj)



#-----------------------------------------------------------------------------------------------------------------------
# ДЛЯ HEADHUNTER
# задаем глубину поиска информации (количество страниц)
pgs_hh = 3
# задаем должность для поиска
post_hh = 'python'
# ссылка для поиска вакансий
link_hh = 'https://hh.ru/search/vacancy?st=searchVacancy&text='
# главная страница
main_link_hh = 'https://hh.ru'

html_hh = requests.get(link_hh+post_hh, headers=headers).text
parsed_html_hh = bs(html_hh, 'lxml') #собираем данные с ссылки запроса

# получаем ссылку перехода на следующую страницу (кнопка "дальше")
next_link=parsed_html_hh.find('a', {'class': 'bloko-button HH-Pager-Controls-Next HH-Pager-Control'})['href']
# форируем из этой ссылки "рабочую заготовку" (без последней цифры)
link_new_hh = main_link_hh + next_link[:-1]
# создаем список ссылок (первые три страницы)
pages_hh = []
# создаем список для хранения данных со страниц по запросам (цикл "for vac in vacancies_list_hh")
vacancies_hh = []
# наполняем список pages ссылками
for i in range(0, pgs_hh):
    url = link_new_hh + str(i)
    pages_hh.append(url)

# рабочий цикл for для сбора со страниц нужных данных
for item in pages_hh:

    # опять же обращение к странице
    page_hh = requests.get(item, headers=headers).text
    parser_hh = bs(page_hh, 'lxml')

    # определие блока с вакансиями
    vacancies_list_hh = parser_hh.find('div', {'class': 'vacancy-serp'})

    for vac in vacancies_list_hh:
        vac_data_hh={}

        # условие для "отсева" блоков (внутри блока с вакансиями), содержащих рекламу
        if vac.find('span', {'class': 'g-user-content'}) is None:
            continue
        else:
            # наименование вакансии
            vac_name = vac.find('span', {'class': 'g-user-content'}).getText()
            # ссылка на вакансию
            vac_link = vac.find('a', {'class': 'bloko-link HH-LinkModifier'})['href']

            # ЗП
            if vac.find('div', {'class': 'vacancy-serp-item__compensation'}) is None:
                vac_sal = 'Не указано'
            else:
                vac_sal = vac.find('div', {'class': 'vacancy-serp-item__compensation'}).getText()

            # город
            vac_city = vac.find('span', {'class': 'vacancy-serp-item__meta-info'}).getText()

            # наименование работодателя
            if vac.find('a', {'data-qa': 'vacancy-serp__vacancy-employer'})is None:
                vac_emp = 'Работодатель не указан'
            else:
                vac_emp = vac.find('a', {'data-qa': 'vacancy-serp__vacancy-employer'}).getText()
        # формируем словарь с выужеными данными
        vac_data_hh = {'Name': vac_name,
                        'Earn': vac_sal,
                        'Link': vac_link,
                        'Main_link': main_link_hh,
                        'Employer': vac_emp,
                        'City': vac_city}
        # и добавляем всё в один список
        vacancies_hh.append(vac_data_hh)




# объединяем два списка
all_vac =  vacancies_sj + vacancies_hh
# формируем датафрейм
df = pd.DataFrame(all_vac)
# добавляем столбцы минимума и максимума ЗП
df['Salary min'], df['Salary max'] = df['Earn'].str.split('—|-', 1).str
df = df.drop('Earn', 1)
# сохраняем результат в файл
df.to_excel('excel_df.xlsx')