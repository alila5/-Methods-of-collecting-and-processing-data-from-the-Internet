from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient
import time

client = MongoClient('localhost', 27017)
mongo_base = client.mail
collection = mongo_base["mail_YA"]

driver = webdriver.Chrome()
driver.get('https://passport.yandex.ru/auth/add?origin=home_desktop_ru&retpath=https%3A%2F%2Fmail.yandex.ru%2F&backpath=https%3A%2F%2Fyandex.ru')
# assert "GeekBrains" in driver.title

elem = driver.find_element_by_id('passp-field-login')
elem.send_keys('ppp1418@yandex.ru')
elem.send_keys(Keys.RETURN)

#time.sleep(10)
try:
    elem = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "passp-field-passwd"))
    )
except Exception as e:
    print(e)
    driver.quit()

#elem = driver.find_element_by_id('passp-field-passwd')
elem.send_keys('petr1975')
elem.send_keys(Keys.RETURN)

time.sleep(10)

elem = driver.find_elements_by_xpath("//span[@class='mail-App-Footer-Item mail-App-Footer-Item_lite']")
elem1= elem[0].find_element_by_tag_name('a')
elem1.send_keys(Keys.RETURN)

time.sleep(5)

item = []

#letters = driver.find_elements_by_xpath("//span[@class='b-messages__message__left']")
letters = driver.find_elements_by_xpath("//a[@class='b-messages__from']")

# Этот цикл не рабочим оказался! Отладчик показывает, что после перехода объекты  letter теряют связь с драйвером.

#for letter in letters:
#    #cl_lett = letter.find_element_by_tag_name('a')
#    letter.send_keys(Keys.RETURN)
#    print('1')
#    time.sleep(1)
#    #driver.back()
#    back_ = driver.find_element_by_class_name("b-folders__folder__link")
#    back_.send_keys(Keys.RETURN)

# _________________________________________________________________________________________________________________


for i in range(0,len(letters)):
    letter =  driver.find_elements_by_xpath("//a[@class='b-messages__from']")[i]
    #cl_lett = letter.find_element_by_tag_name('a')
    letter.send_keys(Keys.RETURN)
    lfrom = driver.find_element_by_class_name('b-message-head__person').text
    ldata = driver.find_element_by_class_name('b-message-head__date').text
    lsub = driver.find_element_by_class_name('b-message-head__subject-text').text
    lbody = driver.find_element_by_class_name('b-message-body').text
    item = {'FROM':lfrom,'WHEN': ldata, "SUB": lsub,'BODY': lbody}
    collection.insert_one(item)
    print(lsub)
    print('-'*100)
    #time.sleep(1)
#    #driver.back()
    back_ = driver.find_element_by_class_name("b-folders__folder__link")
    back_.send_keys(Keys.RETURN)

driver.quit()
