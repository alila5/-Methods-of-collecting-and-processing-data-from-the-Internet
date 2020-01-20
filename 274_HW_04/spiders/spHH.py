# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem



class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?text=Python&area=113&st=searchVacancy']

    def parse(self, response: HtmlResponse):
        next_page = response.css('a.HH-Pager-Controls-Next::attr(href)').extract_first()
        print(next_page)
        yield response.follow(next_page,callback=self.parse)
        vacancy = response.css(
            'div.vacancy-serp div.vacancy-serp-item div.vacancy-serp-item__row_header a.bloko-link::attr(href)').extract()
        for link in vacancy:
            yield response.follow(link,self.vacancy_parse)


    def vacancy_parse (self, response: HtmlResponse):
        title = response.xpath("//div[@class='vacancy-title ']/h1/text()").extract_first()
        if title == None :
            title = response.xpath("//div[@class='vacancy-title']/h1/span/text()").extract()[0]
        vac_href = response.url
        salary_max = response.css('div.vacancy-title meta[itemprop="maxValue"]::attr(content)').extract()
        salary_min = response.css('div.vacancy-title meta[itemprop="minValue"]::attr(content)').extract()
        salary_comment = response.css('div.vacancy-title p.vacancy-salary::text').extract_first()
        competition = response.xpath("//div[@class='bloko-tag bloko-tag_inline']//span/text()").extract()
        if competition == [] :
            competition = response.xpath("//span[@class='Bloko-TagList-Text']/text()").extract()
        company_title = response.xpath("//meta[@itemprop = 'name']/@content").extract_first()
        company_href = response.xpath("//a[@class='vacancy-company-name']/@href").extract_first()
        company_logo = response.xpath("//a[@class='vacancy-company-logo']/img/@src").extract_first()
        if  company_logo == None:
            company_logo = response.xpath("//a[@class='vacancy-company-logo ']/img/@src").extract_first()

        print('VParse',title, response, salary_comment, salary_max, salary_min)
        yield JobparserItem(title=title, vac_href=vac_href, salary_max=salary_max, salary_min=salary_min,
                            salary_comment=salary_comment, vac_from='HH', compet = competition,
                            comp_title=company_title, comp_href = company_href, comp_logo = company_logo )


