import sys

from PyQt5.QtWidgets import QApplication

from nauka.crawler import Crawler
from ui.ui import MainWindow

if __name__ == '__main__':
    # BASE_URL = 'https://nauka.offnews.bg'
    # crawler = Crawler(BASE_URL)

    app = QApplication(sys.argv)

    with open('ui/styles.qss', 'r') as f:
        style = f.read()
    app.setStyleSheet(style)

    main_window = MainWindow()
    sys.exit(app.exec_())

