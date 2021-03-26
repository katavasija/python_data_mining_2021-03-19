from pathlib import Path
import path_helper as ph
import request_helper as rh


class Parse5kaCategory:
    BASE_API_URL = "https://5ka.ru/api/v2/special_offers/"

    def __init__(self, root_path: Path):
        """Конструктор"""
        # путь выходных данных
        self.root_path = root_path
        #  родительские категории
        self.categories = self._get_categories_from_file()

    def update_parent_categories_file(self):
        categories_url = "https://5ka.ru/api/v2/categories/"
        response = rh.get_response(categories_url)
        data: dict = response.json()
        ph.save_json(data, self._get_categories_file_path())

    def fill_categories(self):
        self.categories = self._get_categories_from_file()

    def run(self):
        for category in self.categories[:5]:
            self._parse_single_category(category)

    def _parse_single_category(self, category):
        category_code = category["parent_group_code"]
        params_dict = {"records_per_page": 12, "categories": category_code}
        category_url = rh.get_url_with_params(self.BASE_API_URL, params_dict)
        category_products = []

        for product in self._parse(category_url):
            category_products.append(product)

        category_export = {"code": category_code,
                           "name": category["parent_group_name"],
                           "products": category_products}

        ph.save_json(category_export, self.root_path.joinpath(f'{category_code}.json'))

    def _parse(self, url: str):
        """response parsing"""
        while url:
            response = rh.get_response(url)
            data: dict = response.json()
            url = data["next"]
            for product in data["results"]:
                yield product

    def _get_categories_file_path(self):
        categories_file_name = "categories.json"
        return self.root_path.joinpath(categories_file_name)

    def _get_categories_from_file(self):
        categories_file_path = self._get_categories_file_path()
        self._ensure_categories_file()
        return ph.load_json(categories_file_path)

    def _ensure_categories_file(self):
        categories_file_path = self._get_categories_file_path()
        if not ph.is_file(categories_file_path):
            self.update_parent_categories_file()


if __name__ == "__main__":
    save_path_categories = ph.get_save_path("categories")
    category_parser = Parse5kaCategory(save_path_categories)
    category_parser.run()
