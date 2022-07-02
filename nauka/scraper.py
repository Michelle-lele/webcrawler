import sys

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

            :param :HTML :string
            :return :publications :list

        """
        pubs_list = self._soup.find(class_="cat_list_s").findAll(class_=['cat_list_s_int', 'cat_list_box'])
        return pubs_list

    def is_pub_last_30_days(self, publication):
        """

        :param publication:
        :return:
        """

        """
            <div class="cat_list_box">
            <a href="/news/Razni_17/Uchenite-se-sheguvat_7102.html" title="Учените се шегуват">
            <img src="//i2.offnews.bg/nauka/events/2015/03/28/7102/1427563124_2_152x158.jpg">
            </img></a>
            <div class="cat_list">
            <h1 class="cat_list_title"><a href="/news/Razni_17/Uchenite-se-sheguvat_7102.html" title="Учените се шегуват">Учените се шегуват</a></h1>
            <div class="news_info">01 април 2015 в 10:45<span class="eye_icon left_10px">17951</span><span class="comment_icon left_10px">2</span></div>
            <div class="clb"></div><span class="cat_list_text">И учените обичат да се шегуват. Опитахме се да съберем малко доказателства за това твърдение. 
            Какви са шегите на химици, физици, математици и биолози?
            Химиците
            
            Таблицата на Менделеев отначало се е присънила на Пушкин, само че той нищо не е разбрал.
            
            "Пази се! Влажен...</span>
            </div>
            </div>

        """
        # r"\d\d \w[а-я,a-z]+ \d\d\d\d"gm
        pub_date_div = self._soup.find(class_="news_info")
        print(pub_date_div)
        pass

    def get_pub_date(self):
        pass

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
