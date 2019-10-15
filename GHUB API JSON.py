import requests
import re
import json
import datetime
import os
from  bs4 import BeautifulSoup as BS




username = 'alila5'
password = '****'
mlink = 'https://api.github.com'

r= requests.get('https://api.github.com/user', auth=(username, password))

print(r.text)
print(r.json())

repos = requests.get(mlink+'/user/repos', auth=(username, password))
print(mlink+'/users/'+username+'/repos')
print(repos)
print(repos.json())
repos = requests.get(mlink+'/users/'+username+'/repos')
print(repos)
print(repos.json())


with open('1.json','w', encoding='utf-8') as f:
    json.dump(repos.json(), f)
    f.close()


city = 'London'
app_id = '17e8d87ca4e8e32c7eaf0bb0bd115046'
req_txt = requests.get('http://api.openweathermap.org/data/2.5/forecast?q='+city+'&&APPID='+app_id).text
str_url = 'http://api.openweathermap.org/data/2.5/forecast?q='+city+'&&APPID='+app_id
print(str_url)
city_weather = json.loads(req_txt)
#print(type(city_weather))
print(city_weather['list'][0]['main']['temp'])
print(f"В городе {city_weather['city']['name']} {city_weather['list'][0]['main']['temp']-273} градусов по Цельсию")
