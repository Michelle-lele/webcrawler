import sys
import requests
from PyQt5.QtCore import QThread

from nauka.scraper import Scraper
from nauka.db import DB

class WorkerThread(QThread):

    def run(self):
        BASE_URL = 'https://nauka.offnews.bg'
        crawler = Crawler(BASE_URL)
        crawler.run()

class Crawler:

    def __init__(self, base_url):
        self._base_url = base_url
        self._categories = []
        self._seed = []
        self._publications = []
        self.db = DB()

    def run(self):
        """
        Runs the crawler and stores the extracted data.

        :param: None
        :return: None

        """
        self.save_categories()
        self.get_seed()
        self.save_publications()
        self.save_crawler_data()

    def save_categories(self):
        """
        Extracts and returns the site categories - url and title.

        :param :None
        :return :list of tuples

        """
        print("Crawling categories...")
        html = self.get_html(self._base_url)
        scraper = Scraper(html)
        self._categories = scraper.get_categories()
        print(f"{len(self._categories)} categories extracted!")
        return self._categories

    def get_seed(self):
        """
        Finds all pages in the site categories and extracts the urls in a list.

        :param :None
        :return :string :list of tuples

        """
        if self._categories:
            print("Crawling categories to get seed URLs...")
            for path, category_name in self._categories:
                current_page = 0
                # TODO consider joining path under different OS
                url = self._base_url + path + "?page_which=" + str(current_page)
                html = self.get_html(url)
                scraper = Scraper(html)
                max_page = scraper.get_max_page()
                while current_page < max_page:
                    # TODO consider joining path under different OS
                    url = self._base_url + path + "?page_which=" + str(current_page)
                    self._seed.append((url, category_name))
                    current_page += 20
                # TODO consider joining path under different OS
                self._seed.append((self._base_url + path + "?page_which=" + str(max_page), category_name))
            print(f"{len(self._seed)} URLs extracted!")
            return self._seed
        else:
            return sys.exit("No categories to crawl!")

    def save_publications(self):
        """
        Crawls and saves the data for a publication - title, date, content, url & others.

        :param: None
        :return: publications data: list of dictionaries
        """
        if self._seed:
            print("Crawling publications seed...")
            for url, category_name in self._seed:
                html = self.get_html(url)
                scraper = Scraper(html)
                self._publications.extend(scraper.get_publications(category_name))
            for pub in self._publications:
                pub_html = self.get_html(self._base_url + pub['URL'])  # TODO consider better way to join url
                scraper = Scraper(pub_html)
                pub['content'] = scraper.get_pub_content()
            print(f"{len(self._publications)} publications extracted")

            self.db.drop_publications_table()
            self.db.create_publications_table()

            for publication in self._publications:
                self.db.add_publication(publication)
            return self._publications
        else:
            print("No seed urls to be crawled!")

    def save_crawler_data(self):
        self.db.delete_crawler_data()
        self.db.add_crawler_data()

    @staticmethod
    def get_html(url):
        """
        Extracts the html of an url.
        :param url: string
        :return string

        """

        try:
            r = requests.get(url)
        except requests.RequestException:
            try:
                r = requests.get(url, verify=False)
            except Exception as e:
                print(f'Cannot get url: {url}: {str(e)}!')
                exit(-1)

        r.encoding = "utf-8"

        if r.ok:
            html = r.text
            return html
