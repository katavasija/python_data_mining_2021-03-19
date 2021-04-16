import scrapy


class AvitoSpider(scrapy.Spider):
    name = 'avito'
    allowed_domains = ['avito.ru']
    start_urls = ['https://www.avito.ru/krasnoyarsk/kvartiry/prodam']

    def parse(self, response):
        pass
