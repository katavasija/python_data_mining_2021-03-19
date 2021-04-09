import scrapy


class AutoyoulaSpider(scrapy.Spider):
    name = 'autoyoula'
    allowed_domains = ['auto.youla.ru']
    start_urls = ['https://auto.youla.ru/krasnoyarsk/']

    _css_selectors = {
        "pagination": "a.Paginator_button__u1e7D",
    }

    def __init__(self, *args, **kwargs):
        print("init spider")
        super().__init__(*args, **kwargs)

    def parse(self, response):
        yield from self._get_follow(
            response, self._css_selectors["pagination"], self.page_parse, hello="moto"
        )

    def _get_follow(self, response, select_str, callback, **kwargs):
        for a in response.css(select_str):
            link = a.attrib.get("href")
            yield response.follow(link, callback=callback, cb_kwargs=kwargs)

    def page_parse(self, response):
        print(response.url)