import scrapy


class HhSpider(scrapy.Spider):
    name = 'hh'
    allowed_domains = ['krasnoyarsk.hh.ru']
    start_urls = ['https://krasnoyarsk.hh.ru/']

    def parse(self, response):
        pass
