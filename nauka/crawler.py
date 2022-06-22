import requests
from nauka.scraper import Scraper


class Crawler:
    CATEGORIES = []

    def __init__(self, base_url, data_path='/data'):
        self.base_url = base_url
        self.data_path = data_path

    def run(self):
        self.save_cat_urls(self.base_url)

    def save_cat_urls(self, base_url):
        """
        Extracts and returns a list of tuples including the category url and title.

        :param :base_url :string

        """
        html = self.get_html(self.base_url)
        scraper = Scraper(html)
        Crawler.CATEGORIES = scraper.get_categories()

        # TODO crawl each category
        # TODO if publication is in the past 30 days save the current category name, publication title, date and description
        # TODO crawl each page in a category

    @staticmethod
    def get_html(url):

        try:
            r = requests.get(url)
        except requests.RequestException:
            # TODO handle
            r = requests.get(url, verify=False)
        except Exception as e:
            print(f'Cannot get url: {url}: {str(e)}!')
            exit(-1)

        r.encoding = "utf-8"

        if r.ok:
            html = r.text
            return html