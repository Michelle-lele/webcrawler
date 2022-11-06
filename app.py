import sys

from PyQt5.QtWidgets import QApplication

from nauka.crawler import Crawler
from ui.ui import MainWindow

if __name__ == '__main__':
    # BASE_URL = 'https://nauka.offnews.bg'
    # crawler = Crawler(BASE_URL)

    app = QApplication(sys.argv)

    main_window = MainWindow()
    # main_window.RunCrawlerBtn.clicked.connect(main_window.run_crawler_btn_clicked)
    # main_window.RunCrawlerBtn.clicked.connect(crawler.run)

    sys.exit(app.exec_())

