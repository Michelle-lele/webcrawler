from bs4 import BeautifulSoup
import re

class Scraper:
    def __init__(self, html):
        self._html = html
        self._soup = BeautifulSoup(html, 'html.parser')

    def get_categories(self):
        """
                Extracts and returns the site categories - url and title.

                :param :None
                :return :list of tuples

        """
        categories = []
        cat_list = self._soup.find("ul", class_="view-category-list").findAll("a")
        for link in cat_list:
            categories.append((link['href'], link.text))
        return categories

    def get_publications(self, html):
        """
            Extracts and returns the page publications.

            :param :HTML :string
            :return :publications :list

        """
        pubs_list = self._soup.find(class_="cat_list_s").findAll(class_=['cat_list_s_int', 'cat_list_box'])
        print(len(pubs_list))
        return pubs_list

    def is_pub_last_30_days(self):
        pass

    def get_pub_date(self):
        pass

    def get_pub_title(self):
        pass

    def get_pub_description(self):
        pass

    def get_max_page(self):
        div = self._soup.find(class_='pageBox')
        href = div.findAll('a')[-1]['href']
        rx = re.compile(r'\d+')
        max_page = rx.search(href)
        if max_page:
            # print(max_page.group(0))
            return int(max_page.group(0))
        else:
            return 0
