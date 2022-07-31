import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import QRect, QSize, Qt, QSortFilterProxyModel
from PyQt5.QtGui import QFont, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QVBoxLayout, QLabel, QStatusBar, \
    QApplication, QLineEdit, QTableView, QAbstractScrollArea

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

        self.show()

        self.pubs_table = []

    def run_crawler_btn_clicked(self):
        self.ShowPubsBtn.setEnabled(False)
        self.RunCrawlerBtn.setEnabled(False)
        self.RunCrawlerBtn.setText("Crawling nauka.offnews.bg...")

        BASE_URL = 'https://nauka.offnews.bg'
        crawler = Crawler(BASE_URL)
        crawler.run()

        self.RunCrawlerBtn.setEnabled(True)
        self.ShowPubsBtn.setEnabled(True)
        self.RunCrawlerBtn.setText("Crawl nauka.offnews.bg")

    def view_pubs(self):
        self.pubs_table = Table()


class Table(QWidget):
    def __init__(self):
        super().__init__()

        self.setup_db()
        self.setup_model()
        self.setup_view()

    def setup_db(self):
        # Setup db data
        self.db = DB()
        self.publications = self.db.select_all_publications()
        self.rows = len(self.publications)

    def setup_model(self):
        # setup the model
        self.model = QStandardItemModel(0, 3)
        self.model.setHorizontalHeaderLabels(['Категория', 'Дата', 'Заглавие'])

        for i, row in enumerate(self.publications):
            # items = [QStandardItem(str(item)[0:100]) for item in row[0:3]]
            items = []
            for item in row[0:3]:
                std_item = QStandardItem(str(item))
                std_item.setEditable(False)
                items.append(std_item)

            self.model.insertRow(i, items)
            # self.setItem(i, j, QStandardItem(str(item)))

    def setup_view(self):
        # setup layout
        table_layout = QVBoxLayout()

        # setup filter
        filter_proxy_model = QSortFilterProxyModel()
        filter_proxy_model.setSourceModel(self.model)
        filter_proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        filter_proxy_model.setFilterKeyColumn(2)

        # setup search field
        self.search = QLineEdit()
        self.search.setPlaceholderText('Търси по заглавие')
        self.search.textChanged.connect(filter_proxy_model.setFilterRegExp)
        table_layout.addWidget(self.search)

        # setup the view
        self.table_view = QTableView()
        table_layout.addWidget(self.table_view)
        self.table_view.SelectionMode(1)

        self.table_view.setWindowTitle('Nauka.offnews.bg publications')
        self.table_view.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.table_view.setMinimumWidth(800)
        self.table_view.setMinimumHeight(500)
        self.table_view.setSortingEnabled(True)
        self.table_view.sortByColumn(1, Qt.DescendingOrder)
        self.table_view.setModel(filter_proxy_model)
        self.setLayout(table_layout)

        # self.table_view.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        # self.adjustSize()

        self.show()

class Publication():
    pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())
