from pprint import pprint
from bs4 import BeautifulSoup as bs
import requests
import re
import transliterate
import pandas as pd

print(transliterate.translit('Привет', reversed=True))

vac1 = input('Какую вакансию ищем? ')
max_page =  int(input('Сколько страниц анализировать? '))
page = 0

vac2 = transliterate.translit(vac1, reversed=True)
head2 = {'User-agent':'PostmanRuntime/7.18.0'}
main_link2=f'https://www.superjob.ru/vacancy/search/?keywords={vac2}'
print(f'{main_link2}{vac2}.html')
html2 = requests.get(f'{main_link2}{vac2}', headers = head2)
print(html2)


def work_with_page_hh(page):
    head1 = {'User-agent':'PostmanRuntime/7.18.0'}
    main_link1=f'https://hh.ru/search/vacancy?&text='
    page = f'&page={str(page)}'
    print(f'{main_link1}{vac1} ')
    html1 = requests.get(f'{main_link1}{vac1}{page}', headers = head1)
    print(html1)
    parsed_html_hh = bs(html1.text,'lxml')
    return parsed_html_hh

def make_dict_hh(parsed_html_hh, page):
    l = []
    vac_hh = parsed_html_hh.findAll('div', {'class': 'vacancy-serp-item'})# '#bloko-link HH-LinkModifier'})
    print('page', page, 'кол-во вакансий',len(vac_hh))
    for v in vac_hh:
        name = v.find('a', {'class': 'bloko-link HH-LinkModifier'})
        link_from_hh = name.get('href')
        salary_hh = v.find('div',{'class':'vacancy-serp-item__compensation'})
        employer = v.find('div', {'class': 'vacancy-serp-item__meta-info'})
        if salary_hh == None or salary_hh == []:
            sal_min = ''
            sal_max = ''
        else:
            sal = salary_hh.text.replace(u'\xa0', ' ')
            sal_range =  list(filter(None, re.split('-', sal)))
            #print(sal_range)
            s = []
            i = 0
            for ss in sal_range:
                s.append(int(re.sub('\D', '',ss)))
                #print(s[i])
                i = i + 1
            sal_min = min(s)
            sal_max = max(s)
        l.append({'vname': name.text, 'href': link_from_hh, 'employer': employer.text.replace(u'\xa0', ' ') ,  'salary_min':sal_min,  'salary_max':sal_max, 'from':'https://hh.ru'})
    #print(l)
    return l

all_page_l = []
for page in range(0,max_page,1):
    par_html = work_with_page_hh(page)
    d = make_dict_hh(par_html, page)
    all_page_l.extend(d)

df = pd.DataFrame(all_page_l)
pprint(df)
df.to_csv('result.csv')



