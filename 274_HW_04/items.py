# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    title = scrapy.Field()
    vac_href = scrapy.Field()
    salary_max = scrapy.Field()
    salary_min = scrapy.Field()
    salary_comment= scrapy.Field()
    vac_from = scrapy.Field()
    compet = scrapy.Field()
    comp_title = scrapy.Field()
    comp_href = scrapy.Field()
    comp_logo = scrapy.Field()
    pass
