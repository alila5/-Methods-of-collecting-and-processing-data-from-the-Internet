from pprint import pprint
from bs4 import BeautifulSoup as bs
import requests
import re
import transliterate
import pandas as pd

#print(transliterate.translit('Привет', reversed=True))

#vac2 = transliterate.translit(vac1, reversed=True)
#head2 = {'User-agent':'PostmanRuntime/7.18.0'}
#main_link2=f'https://www.superjob.ru/vacancy/search/?keywords={vac2}?page=4'
#print(f'{main_link2}{vac2}.html')
#html2 = requests.get(f'{main_link2}{vac2}', headers = head2)
#print(html2)

def work_with_page_SJ(page, vac):
    head = {'User-agent':'PostmanRuntime/7.18.0'}
    main_link=f'https://www.superjob.ru/vakansii/'  #   #https://www.superjob.ru/vacancy/search/?keywords=Повар
    page = f'?page={str(page)}'
    print(f'{main_link}{vac}.html{page}')
    html = requests.get(f'{main_link}{vac}.html{page}', headers = head)
    print(html)
    parsed_html = bs(html.text,'lxml')
    return parsed_html

def make_dict_SJ(parsed_html, page):
    l = []
    vac_sj = parsed_html.find_all('div',{'class':'_3zucV _2GPIV f-test-vacancy-item i6-sc _3VcZr'})
    print('page', page, 'кол-во вакансий',len(vac_sj))
    for v in vac_sj:
        v_block = v.find('div',{'class':'_3mfro CuJz5 PlM3e _2JVkc _3LJqf'})
        name = v_block.getText()
        link_from_sj =  'https://www.superjob.ru/'+v.find('a',{'target':'_blank'})['href']
        salary_sj = v.find('span',{'class':'_3mfro _2Wp8I f-test-text-company-item-salary PlM3e _2JVkc _2VHxz'})
        employer =  v.find('span', {'class': '_3mfro _3Fsn4 f-test-text-vacancy-item-company-name _9fXTd _2JVkc _3e53o _15msI'})
        #print(name, link_from_sj)
        #print(salary_sj, employer)
        if not employer:
            emplorer = 'No Date'
        else:
            employer = employer.getText()

        if not salary_sj or salary_sj.getText() == 'По договорённости':
            sal_min = 0
            sal_max = 0
        else:
            sal = salary_sj.text.replace(u'\xa0', ' ')
            sal_range = list(filter(None, re.split('—', sal)))
            #print(sal_range)
            s = []
            i = 0
            for ss in sal_range:
                s.append(int(re.sub('\D', '', ss)))
                # print(s[i])
                i = i + 1
            sal_min = min(s)
            sal_max = max(s)

        l.append({'vname': name, 'href': link_from_sj, 'employer': employer.replace(u'\xa0', ' ') ,  'salary_min':sal_min,  'salary_max':sal_max, 'from':'https://.superjob.ru'})
    #print(l)
    return l

def PageWorker (max_page, vac_hh):
    all_page_l = []
    for page in range(0, max_page, 1):
        par_html = work_with_page_SJ(page, vac_hh)
        d = make_dict_SJ(par_html, page)
        all_page_l.extend(d)
    return all_page_l


if __name__ == '__main__':
    vac_sj = input('Какую вакансию ищем? ')
    vac = transliterate.translit(vac_sj, reversed=True)
    max_page = int(input('Сколько страниц анализировать? '))
    page = 0
    all_page_l = PageWorker(max_page, vac)
    df = pd.DataFrame(all_page_l)
    pprint(df)
    #df.to_csv('result.csv')



