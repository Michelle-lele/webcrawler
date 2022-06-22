from bs4 import BeautifulSoup


class Scraper:
    def __init__(self, html):
        self._html = html
        self._soup = BeautifulSoup(html, 'html.parser')

    def get_categories(self):
        categories = []
        cat_list = self._soup.find("ul", class_="view-category-list").findAll("a")
        for link in cat_list:
            categories.append((link['href'], link.text))
        return categories

    def is_pub_last_30_days(self):
        pass

    def get_pub_date(self):
        pass

    def get_pub_title(self):
        pass

    def get_pub_description(self):
        pass
