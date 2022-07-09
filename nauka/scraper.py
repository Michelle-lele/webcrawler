import datetime
import sys

import dateparser
from bs4 import BeautifulSoup
import re

DAYS = 90

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

    def get_publications(self, *args):
        """
            Extracts and returns the page publications data - title, date and url.

            :param :None
            :return :list of dictionaries?

        """
        all_pubs = self._soup.find(class_="cat_list_s").findAll(class_=['cat_list_s_int', 'cat_list_box'])
        print(f"{len(all_pubs)} publications found on page")
        ''' TODO think how to optimize check for older publications, 
        can we consider if we find a pub on the page that is older than defined days that we do not need to search more?
        '''
        if all_pubs:
            latest_pubs = []
            for pub in all_pubs:
                pub_date = self.get_pub_date(pub)
                if pub_date and self.no_older_than(pub_date, DAYS):
                    pub_data = {}
                    pub_data['publication_date'] = pub_date
                    pub_data['title'] = self.get_pub_title(pub)
                    pub_data['URL'] = self.get_pub_url(pub)
                    pub_data['category'] = args[0]
                    latest_pubs.append(pub_data)
            print(f"{len(latest_pubs)} recent publications found!")
            for pub in latest_pubs:
                print(f"{pub['title']}\n"
                      f"{pub['publication_date']}\n"
                      f"{pub['URL']}")
            return latest_pubs

    @staticmethod
    def no_older_than(date, days):
        """
        Checks if a date is no older than the defined days

        :param :date
        :return: :bool
        """

        a_quarter_ago = datetime.date.today() - datetime.timedelta(days=days)

        if date > a_quarter_ago:
            return True
        else:
            return False

    @staticmethod
    def get_pub_date(publication):
        """
        Extracts and returns the publication date.

        :param publication: bs4.Element.Tag object
        :return: publication date: datetime object
        """
        rx = re.compile(r"\d\d \w[а-я,a-z]+ \d\d\d\d")
        result = rx.search(publication.text)
        if result:
            try:
                pub_date = dateparser.parse(result.group(0), settings={'TIMEZONE': 'UTC'}).date()
                return pub_date
            except AttributeError:
                sys.exit("Publication date could not be parsed!")
        else:
            # TODO think how to handle better - publication date not found in soup.
            # raise Warning("Publication date not found in soup")
            return None

    @staticmethod
    def get_pub_title(publication):
        """
        Extracts and returns the publication title.

        :param publication: bs4.Element.Tag object
        :return: publication title: string
        """
        pub_title = publication.find(class_ = ["cat_list_title", "cat_list_s_title"]).findChild("a")['title']
        # TODO handle not found in soup
        return pub_title

    @staticmethod
    def get_pub_url(publication):
        """
        Extracts and returns the relative URL of a publication.

        :param publication: bs4.Element.Tag object
        :return: publication URL: string
        """
        pub_url = publication.find(class_=["cat_list_title", "cat_list_s_title"]).findChild("a")['href']
        # TODO handle not found in soup
        return pub_url

    def get_pub_content(self):
        """
        Extracts and returns the publication content.

        :param None
        :return: publication content: string
        """
        pub_content = self._soup.find(class_="news_text").get_text()
        # TODO handle not found in soup
        return pub_content

    def get_max_page(self):
        """
        Extracts and returns the maximum page for a category.

        :param None
        :return: maximum page: integer
        """
        div = self._soup.find(class_='pageBox')
        if div:
            href = div.findAll('a')[-1]['href']
            rx = re.compile(r'\d+')
            max_page = rx.search(href)
            if max_page:
                return int(max_page.group(0))
            else:
                return 0
        else:
            return sys.exit("Pages div not found!")