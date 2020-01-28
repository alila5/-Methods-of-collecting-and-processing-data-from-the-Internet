# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from gbparse.items import  CianItem

class CianSpider(scrapy.Spider):
    name = 'cian'
    allowed_domains = ['krasnodar.cian.ru']
    start_urls = ["https://krasnodar.cian.ru/kupit-kvartiru/"]
    #['https://krasnodar.cian.ru/kupit-kvartiru/']

    def parse(self, response:HtmlResponse):
        pagin = response.xpath("//li[@class='_93444fe79c--list-item--2KxXr']/a/@href").extract()
        for page in pagin:
            yield response.follow(page, callback=self.parse)
        #f'https://krasnodar.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&region=4820&p={num}'

        cur_page_flats_link = response.xpath(
            "//div[@class='undefined c6e8ba5398--main-info--oWcMk']//a/@href").extract()
        for flat_link in cur_page_flats_link:
            yield response.follow(flat_link, callback=self.flat_info_parse)
            #num = num +1


    def flat_info_parse(self, response:HtmlResponse):
        title = response.xpath("//div[@class='a10a3f92e9--header-information--38LX9']/h1/text()").extract_first()
        url = response.url
       # title = response.xpath("//div[@class='vacancy-title ']/h1/text()").extract_first()
        print(title)
        print(url)
        print('-'*20)
        yield CianItem(title=title, url=url)
