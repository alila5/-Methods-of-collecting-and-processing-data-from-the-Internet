# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
import re



class JobparserPipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vac274

    def process_item(self, item, spider):

        print('JobparserPipeline')
        collection = self.mongo_base['vacALL']
        print(item)
        collection.insert_one(item)
        return item

class JobparserPipeline_2(object):

    def __init__(self):
        pass

    def ch_salary(self, salary):
        if salary == []:
            salary = 0
        else:
            try:
                salary = int(str(salary[0]))
            except:
                salary = 0
        return salary

    def process_item(self, item, spider):
        #print('JobparserPipeline_2')
        if spider.name == 'hhru':
            #print(item['vac_href'])
            item['salary_max'] = self.ch_salary(item['salary_max'])
            item['salary_min'] = self.ch_salary(item['salary_min'])
            temp = str(item['comp_title'])
            item['comp_title'] = re.sub(r'[^\w\s]+|[\d]+', r'',temp).replace('\xa0','')
            return item


