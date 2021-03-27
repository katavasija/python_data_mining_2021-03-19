from pathlib import Path
import path_helper as ph
import request_helper as rh


class Parse5ka:

    def __init__(self, start_url: str, root_path: Path):
        """Конструктор"""
        # стартовый url
        self.start_url = start_url
        # путь выходных данных
        self.root_path = root_path

    def run(self):
        for product in self._parse(self.start_url):
            product_path = self.root_path.joinpath(f"{product['id']}.json")
            ph.save_json(product, product_path)

    def _parse(self, url: str):
        """response parsing"""
        while url:
            response = rh.get_response(url)
            data: dict = response.json()
            url = data["next"]
            for product in data["results"]:
                yield product


if __name__ == "__main__":
    url = "https://5ka.ru/api/v2/special_offers/"
    save_path_products = ph.get_save_path("products")
    parser_products = Parse5ka(url, save_path_products)
    parser_products.run()
