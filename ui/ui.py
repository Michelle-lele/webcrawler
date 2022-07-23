import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import QRect, QSize, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QVBoxLayout, QLabel, QStatusBar, \
    QApplication, QTableWidget, QTableWidgetItem

from nauka.crawler import Crawler
from nauka.db import DB


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(200, 100, 294, 203)
        self.setWindowTitle("Nauka.offnews.bg - Web Crawler")

        font = QFont()
        font.setPointSize(13)
        self.setFont(font)

        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName(u"centralwidget")
        self.setCentralWidget(self.centralwidget)

        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(20, 60, 241, 101))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")

        self.RunCrawlerBtn = QPushButton(self.verticalLayoutWidget)
        self.RunCrawlerBtn.setObjectName(u"RunCrawlerBtn")
        self.RunCrawlerBtn.setText("Crawl nauka.offnews.bg")
        self.RunCrawlerBtn.clicked.connect(self.run_crawler_btn_clicked)

        btns_font = QFont()
        btns_font.setFamily(u"Calibri")
        btns_font.setPointSize(12)

        self.RunCrawlerBtn.setFont(btns_font)
        self.RunCrawlerBtn.setToolTipDuration(5)

        self.verticalLayout.addWidget(self.RunCrawlerBtn)

        self.ShowPubsBtn = QPushButton(self.verticalLayoutWidget)
        self.ShowPubsBtn.setObjectName(u"ShowPubsBtn")
        self.ShowPubsBtn.setFont(btns_font)
        self.ShowPubsBtn.setToolTipDuration(5)
        self.ShowPubsBtn.setText('Show publications')
        self.ShowPubsBtn.clicked.connect(self.view_pubs)

        self.verticalLayout.addWidget(self.ShowPubsBtn)

        self.WelcomeLabel = QLabel(self.centralwidget)
        self.WelcomeLabel.setObjectName(u"WelcomeLabel")
        self.WelcomeLabel.setGeometry(QRect(100, 20, 74, 30))
        self.WelcomeLabel.setText('Welcome!')

        self.WelcomeLabel.setMaximumSize(QSize(16777215, 30))
        self.WelcomeLabel.setAlignment(Qt.AlignJustify | Qt.AlignVCenter)

        self.statusbar = QStatusBar(self)
        self.statusbar.setObjectName(u"statusbar")
        self.setStatusBar(self.statusbar)

        # QMetaObject.connectSlotsByName(self)

        self.show()

    def run_crawler_btn_clicked(self):
        self.RunCrawlerBtn.setEnabled(False)
        self.RunCrawlerBtn.setText("Crawling nauka.offnews.bg...")
        self.RunCrawlerBtn.adjustSize()
        self.ShowPubsBtn.setEnabled(False)

        BASE_URL = 'https://nauka.offnews.bg'
        crawler = Crawler(BASE_URL)
        crawler.run()

    def view_pubs(self):
        pubs_table = PubsTable()
        self.pubs_table = pubs_table


class PubsTable(QTableWidget):
    def __init__(self):
        super().__init__()
        self.db = DB()
        self.publications = self.db.select_all_publications()
        self.rows = len(self.publications)

        self.setRowCount(self.rows)
        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(['Категория', 'Дата', 'Заглавие', 'Текст'])
        self.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(2,QtWidgets.QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        self.setMinimumWidth(500)
        self.setMinimumHeight(300)

        for i, row in enumerate(self.publications):
            for j, item in enumerate(row):
                self.setItem(i, j, QTableWidgetItem(str(item)))

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())
