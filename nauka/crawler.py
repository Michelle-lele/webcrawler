import requests
from nauka.scraper import Scraper


class Crawler:

    def __init__(self, base_url, data_path='/data'):
        self._base_url = base_url
        self._data_path = data_path
        self._categories = []
        self._seed = []
        self.publications = []

    def run(self):
        """
        Runs the crawler and stores the extracted data.

        :param: None
        :return: None

        """
        self.save_categories()
        self.get_seed()

    def save_categories(self):
        """
        Extracts and returns the site categories - url and title.

        :param :base_url :string
        :return :list of tuples

        """
        html = self.get_html(self._base_url)
        scraper = Scraper(html)
        self._categories = scraper.get_categories()
        print(f"{len(self._categories)} categories extracted:")
        print(*[category_name for category_url, category_name in self._categories], sep="\n")
        return self._categories

    def get_seed(self):
        '''
        Finds all pages in the site categories and extracts the urls in a list.

        :param :None
        :return :URLs :list

        '''
        for path, category_name in self._categories:
            current_page = 0
            url = self._base_url + path + "?page_which=" + str(current_page)
            html = self.get_html(url)
            scraper = Scraper(html)
            max_page = scraper.get_max_page()
            while current_page < max_page:
                url = self._base_url + path + "?page_which=" + str(current_page)
                self._seed.append(url)
                current_page += 20
            self._seed.append(self._base_url + path + "?page_which=" + str(max_page))
            print(* self._seed, sep='\n')

    def save_publications(self):
        if self._seed:
            for url in self._seed:
                html = self.get_html(url)
                scraper = Scraper(html)
                self.publications = scraper.get_publications(html)
            # for publication in publications:
            #     # TODO if publication is in the past 30 days save the current category name, publication title, date and description
            #     pass

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
            # TODO handle
            r = requests.get(url, verify=False)
        except Exception as e:
            print(f'Cannot get url: {url}: {str(e)}!')
            exit(-1)

        r.encoding = "utf-8"

        if r.ok:
            html = r.text
            return html
