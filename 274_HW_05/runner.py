from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from gbparse import settings
from gbparse.spiders.geekbrains import GeekbrainsSpider
from gbparse.spiders.avito import AvitoSpider
from gbparse.spiders.instagram import InstagramSpider

if __name__ == '__main__':
    scr_settings = Settings()
    scr_settings.setmodule(settings)
    process = CrawlerProcess(settings=scr_settings)
    # process.crawl(GeekbrainsSpider)
    process.crawl(InstagramSpider)
    process.start()
