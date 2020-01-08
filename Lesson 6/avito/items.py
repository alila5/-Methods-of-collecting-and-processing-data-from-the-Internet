# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst


def cleaner_photo(values):
    if values[:2] == '//':
        return f'http:{values}'
    return values


def clean_param(values):
    if values != ' ':
        return values





class AvitoItem(scrapy.Item):
    # define the fields for your item here like:
    print('AvitoItem')
    _id = scrapy.Field()
    photos = scrapy.Field(input_processor=MapCompose(cleaner_photo))
    title = scrapy.Field(output_processor=TakeFirst())
    sale = scrapy.Field(output_processor=TakeFirst())
    param = scrapy.Field(input_processor=MapCompose(clean_param))

