# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from avito.items import AvitoItem
from scrapy.loader import ItemLoader

class AvitoSpiderSpider(scrapy.Spider):
    name = 'avito_spider'
    allowed_domains = ['avito.ru']
    start_urls = ['https://www.avito.ru/rossiya/avtomobili']

    def parse(self, response: HtmlResponse):
        # <a class="js-item-slider item-slider" href="/groznyy/avtomobili/kia_rio_2019_1707005120" target="_blank" xpath="1">
        #<ul class="item-slider-list js-item-slider-list"></ul>
        #</a>
        ads_links = response.xpath('//a[@class="js-item-slider item-slider"]/@href').extract() #'//a[@class="item-description-title-link"]/@href').extract()
        print('all',ads_links)
        for link in ads_links:
            yield response.follow(link, self.parse_ads)

    def parse_ads(self, response:HtmlResponse):

        loader = ItemLoader(item=AvitoItem(), response=response)

        #<div class="gallery-img-wrapper js-gallery-img-wrapper" xpath="1">
        #   <div class="gallery-img-frame js-gallery-img-frame" data-url="//27.img.avito.st/640x480/7945137027.jpg" data-title="Skoda Rapid, 2017, с пробегом, цена 650 000 руб. — Автомобили в Самаре"></div>
        #</div>
        loader.add_xpath('photos',
                         '//div[contains(@class, "gallery-img-wrapper")]//div[contains(@class, "gallery-img-frame")]/@data-url')

        #<meta property="product:price:amount" content="650000" style="" xpath="1">
        loader.add_xpath('sale', '//meta[@property="product:price:amount"]/@content')

        #<h1 class="title-info-title" style="" xpath="1">
        #   <span class="title-info-title-text" itemprop="name" style="">Skoda Rapid, 2017</span>
        #</h1>
        loader.add_css('title', 'h1.title-info-title span.title-info-title-text::text')
        #title = response.xpath('//h1[@class ="title-info-title"] / span[@ class ="title-info-title-text"]').extract_first()

        #<li class="item-params-list-item" xpath="1">
        #    <span class="item-params-label" style=""></span>
             #не битый
        #</li>
        loader.add_css('param', 'li.item-params-list-item *::text')
        #param =  response.xpath('//li[@class ="item-params-list-item"]').extract()

        print('parse_ads')
        yield loader.load_item()
