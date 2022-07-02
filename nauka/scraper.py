import datetime
import sys

import dateparser
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

    def get_publications(self):
        """
            Extracts and returns the page publications.

            :param :None
            :return :list :HTML?

        """
        all_pubs = self._soup.find(class_="cat_list_s").findAll(class_=['cat_list_s_int', 'cat_list_box'])
        print(f"{len(all_pubs)} publications found on page")
        ''' TODO think how to optimize check for older publications, 
        can we consider if we find a pub on the page that is older than 30 days that we do not need to search more?
        '''
        if all_pubs:
            latest_pubs = []
            for pub in all_pubs:
                pub_date = self.get_pub_date(pub)
                if pub_date and self.is_last_30_days(pub_date):
                    latest_pubs.append(pub)
            print(f"{len(latest_pubs)} pubs from last 30 days found!")
            return latest_pubs

    @staticmethod
    def is_last_30_days(pub_date):
        """
        Checks if a date is in last 30 days

        :param :date
        :return: :bool
        """

        a_month_ago = datetime.date.today() - datetime.timedelta(days=90)

        if pub_date > a_month_ago:
            return True
        else:
            return False

    @staticmethod
    def get_pub_date(publication):
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
            return None

    def get_pub_title(self):
        pass

    def get_pub_description(self):
        pass

    def get_max_page(self):
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
