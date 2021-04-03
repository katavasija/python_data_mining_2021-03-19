import bs4
import requests_helper as rh
from urllib.parse import urljoin


class MagnitParse:
    def __init__(self, start_url):
        self.start_url = start_url

    def get_soup(self, *args, **kwargs) -> bs4.BeautifulSoup:
        soup = bs4.BeautifulSoup(rh.get_response(self.start_url).text, "lxml")
        return soup

    @property
    def template(self):
        data_template = {
            "url": lambda a: urljoin(self.start_url, a.attrs.get("href", "/")),
            "product_name": lambda a: a.find("div", attrs={"class": "card-sale__title"}).text,
            "image_url": lambda a: urljoin(
                self.start_url, a.find("picture").find("img").attrs.get("data-src", "/")
            ),
        }
        return data_template

    def run(self):
        for product in self._parse(self.get_soup()):
            self.save(product)

    def _parse(self, soup):
        products_a = soup.find_all("a", attrs={"class": "card-sale"})
        for prod_tag in products_a:
            product_data = {}
            for key, func in self.template.items():
                try:
                    product_data[key] = func(prod_tag)
                except AttributeError:
                    pass
            yield product_data

    def save(self, data):
        from mongo_helper import MongoHelper
        mh = MongoHelper()
        mh.save(data)


if __name__ == "__main__":
    url = "https://magnit.ru/promo/"
    magnit_parse = MagnitParse(url)
    magnit_parse.run()