from bs4 import BeautifulSoup


class Scraper:
    def __init__(self, html):
        self.html = html
        self.soup = BeautifulSoup(html, 'html.parser')

    def get_categories(self):
        categories = []
        cat_list = self.soup.find("ul", class_="view-category-list").findAll("a")
        for link in cat_list:
            categories.append((link['href'], link.text))
        return categories
