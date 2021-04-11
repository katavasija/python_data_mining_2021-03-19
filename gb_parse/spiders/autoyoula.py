import scrapy
import path_helper as ph

class AutoyoulaSpider(scrapy.Spider):
    name = 'autoyoula'
    allowed_domains = ['auto.youla.ru']
    start_urls = ['https://auto.youla.ru/krasnoyarsk']
    cars_counter = 0

    _css_selectors = {
        "brands": "div.TransportMainFilters_brandsList__2tIkv a.blackLink",
        "pagination": "div.Paginator_block__2XAPy a.Paginator_button__u1e7D",
        "car": ".SerpSnippet_titleWrapper__38bZM a.SerpSnippet_name__3F7Yu"
    }

    car_data_query = {
        "title": lambda resp: resp.css("div.AdvertCard_advertTitle__1S1Ak::text").get(),
        "price": lambda resp: float(
            resp.css("div.AdvertCard_price__3dDCr::text").get().replace("\u2009", "")
        ),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cars_path = ph.get_save_path("cars")

    def _get_follow(self, response, css_selector_str, callback, **kwargs):
        for a in response.css(css_selector_str):
            url = a.attrib.get("href")
            yield response.follow(url, callback=callback, **kwargs)

    def parse(self, response):
        # brands urls
        yield from self._get_follow(
            response,
            self._css_selectors["brands"],
            self.brand_parse
        )

    def brand_parse(self, response):
        # an i-page url of a brand url
        yield from self._get_follow(
            response,
            self._css_selectors["pagination"],
            self.brand_parse
        )
        # a car url on a brand url
        yield from self._get_follow(
            response,
            self._css_selectors["car"],
            self.car_parse
        )

    def car_parse(self, response):
        AutoyoulaSpider.cars_counter += 1
        data = {"url": response.url}
        for key, css_selector_func in self.car_data_query.items():
            try:
                data[key] = css_selector_func(response)
            except (ValueError, AttributeError):
                continue

        ph.save_json(data, self.cars_path.joinpath(f"{AutoyoulaSpider.cars_counter}.json"))
