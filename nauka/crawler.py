import sys

import requests
from nauka.scraper import Scraper


class Crawler:

    def __init__(self, base_url):
        self._base_url = base_url
        self._categories = []
        self._seed = []
        self._publications = []

    def run(self):
        """
        Runs the crawler and stores the extracted data.

        :param: None
        :return: None

        """
        self.save_categories()
        self.get_seed()
        self.save_publications()

    def save_categories(self):
        """
        Extracts and returns the site categories - url and title.

        :param :base_url :string
        :return :list of tuples

        """
        print("Crawling categories...")
        html = self.get_html(self._base_url)
        scraper = Scraper(html)
        self._categories = scraper.get_categories()
        print(f"{len(self._categories)} categories extracted!")
        # print(*[category_name for category_url, category_name in self._categories], sep="\n")
        return self._categories

    def get_seed(self):
        """
        Finds all pages in the site categories and extracts the urls in a list.

        :param :None
        :return :string :list

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
                    self._seed.append(url)
                    current_page += 20
                # TODO consider joining path under different OS
                self._seed.append(self._base_url + path + "?page_which=" + str(max_page))
                # print(* self._seed, sep='\n')
            print(f"{len(self._seed)} URLs extracted!")
            return self._seed
        else:
            return sys.exit("No categories to crawl!")

    def save_publications(self):
        """
        :param: None
        :return:
        """
        if self._seed:
            print("Crawling publications seed...")
            all_publications = []
            for url in self._seed:
                html = self.get_html(url)
                scraper = Scraper(html)
                all_publications.extend(scraper.get_publications())
            print(f"{len(all_publications)} publications extracted")
            # # TODO if publication is in the past 30 days save the current category name, publication title, date and description
            # for publication in all_publications:
            #     if scraper.is_pub_last_30_days(publication):
            #         self._publications.append(publication)
            print(self._publications)
            return self._publications

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
