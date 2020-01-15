import requests
from bs4 import BeautifulSoup
import time


def MakeUniqAutList(all_aut, aut_inf):
    try:
        inx= all_aut.index(aut_inf)
    except:
        all_aut.append(aut_inf)
        inx = len(all_aut)-1
    return all_aut, inx

def MakeUniqTagsList(all_tags, tag ):
    try:
        inx = all_tags.index(tag)
    except:
        all_tags.append(tag)
        inx = len(all_tags) - 1
    return all_tags, inx

def TakeDataFromPage(domain, link, all_tags, all_aut):
    response = requests.get(link)
    if response.status_code == 200:

        soap = BeautifulSoup(response.text, 'lxml')
        #li = soap.find('h1', attrs={'class': 'blogpost-title text-left text-dark m-t-sm'}).find('li', attrs={'class': 'page'})
        title = soap.find('h1', attrs={'class': 'blogpost-title text-left text-dark m-t-sm'}).text
        data= soap.find('time', attrs={'class': 'text-md text-muted m-r-md'}).text
        #print(data)
        aut= soap.find('div', attrs={'class': 'text-lg text-dark'}).text
        #print(aut)
        aut_link= domain+ soap.find('a', attrs={'style': 'text-decoration:none;'}).attrs['href']
        all_aut, aut_inx = MakeUniqAutList(all_aut, (aut, aut_link))
        tags =  soap.findAll('a', attrs={'class': 'small'})#.attrs['href']
        inxs_lett_tag = []
        for tag in tags:
            all_tags, inxt = MakeUniqTagsList(all_tags, (domain + tag.attrs['href'],tag.text))
            inxs_lett_tag.append(inxt)

        return title, data, link, aut_inx, inxs_lett_tag, all_tags, all_aut

# todo Пройти ленту блога
def MStart(domain, start_url ):
    domain = 'https://geekbrains.ru'
    start_url = 'https://geekbrains.ru/posts?page=0'
    response = requests.get(start_url)
    soap = BeautifulSoup(response.text, 'lxml')
    letters = soap.findAll('a', attrs={'class': 'post-item__title h3 search_text'})
    list_letters= []
    all_tags = []
    all_aut=[]
    while letters : #and len(list_letters) <29:
        print(letters and len(list_letters))
        for letter in letters:
            print('-' * 100)
            print(domain + letter.attrs['href'])
            title, data, link, aut_inx, inxs_lett_tag, all_tags, all_aut = TakeDataFromPage(domain, domain + letter.attrs['href'],all_tags, all_aut)
            list_letters.append((title, data,  link, aut_inx, inxs_lett_tag))
            letters = None
            print('Статей обработано',len(list_letters))
            print('Размер словаря тэгов', len(all_tags))
        next_objs = soap.findAll('li', attrs={'class': 'page'})
        if next_objs:
            for obj in next_objs:
                next = obj.find('a', attrs={'rel': 'next'})
                if next:
                    next_link= domain + next.attrs['href']
                    response = requests.get(next_link)
                    if response.status_code == 200 :
                        soap = BeautifulSoup(response.text, 'lxml')
                        letters = soap.findAll('a', attrs={'class': 'post-item__title h3 search_text'})
    return  all_tags, list_letters, all_aut

if __name__ == '__main__' :
   MStart('https://geekbrains.ru', 'https://geekbrains.ru/posts?page=0')



