from nauka.crawler import Crawler

if __name__ == '__main__':
    BASE_URL = 'https://nauka.offnews.bg'
    crawler = Crawler(BASE_URL)
    crawler.run()
