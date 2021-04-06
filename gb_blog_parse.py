import bs4
from urllib.parse import urljoin
import json
from pathlib import Path
import requests_helper as rh


class GbBlogParse:

    def __init__(self, start_url):
        """constructor"""
        self.start_url = start_url
        self.done_urls = set()
        # tasks list
        self.tasks = [
            self._get_task(self.start_url, self._parse_feed),
        ]
        self.done_urls.add(self.start_url)

    def _get_task(self, url, callback):
        """get task as function
           of callback(url, soup(url))
        """

        def task():
            soup = self._get_soup(url)
            return callback(url, soup)

        return task

    def _get_soup(self, url):
        soup = bs4.BeautifulSoup(rh.get_response(url).text, "lxml")
        return soup

    def _parse_feed(self, url, soup):
        """
        parse a page with the posts table
        :param url:
        :param soup:

        :affects: fills task list
        :return None
        """
        ul = soup.find("ul", attrs={"class": "gb__pagination"})
        pag_urls = set(
            urljoin(url, href.attrs.get("href"))
            for href in ul.find_all("a")
            if href.attrs.get("href")
        )
        for pag_url in pag_urls:
            if pag_url not in self.done_urls:
                self.tasks.append(self._get_task(pag_url, self._parse_feed))

        # find all posts on a page
        post_items = soup.find("div", attrs={"class": "post-items-wrapper"})
        posts_urls = set(
            urljoin(url, href.attrs.get("href"))
            for href in post_items.find_all("a", attrs={"class": "post-item__title"})
            if href.attrs.get("href")
        )

        # parse every post
        for post_url in posts_urls:
            if post_url not in self.done_urls:
                self.tasks.append(self._get_task(post_url, self._parse_post))

    def _parse_post(self, url, soup):
        """
        parse single post
        :param url:
        :param soup:
        :return: post data
        """
        author_tag = soup.find("div", attrs={"itemprop": "author"})
        data = {
            "post_data": {
                "title": soup.find("h1", attrs={"class": "blogpost-title"}).text,
                "url": url,
                "id": soup.find("comments").attrs.get("commentable-id"),
            },
            "author_data": {
                "url": urljoin(url, author_tag.parent.attrs.get("href")),
                 "name": author_tag.text,
            },
            "tags_data": [
                {"name": tag.text, "url": urljoin(url, tag.attrs.get("href"))}
                for tag in soup.find_all("a", attrs={"class": "small"})
            ],
        }
        return data

    def run(self):
        i = 0
        for task in self.tasks:
            task_result = task()
            i+=1
            if task_result:
                self.save(task_result, i)

    def save(self, data, i):
        save_path = Path(__file__).parent.joinpath("products").joinpath(str(i) + ".json")
        save_path.write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')


if __name__ == "__main__":
    # database = Database("sqlite:///gb_blog.db")
    parser = GbBlogParse("https://geekbrains.ru/posts")
    parser.run()
