import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import QRect, QSize, Qt, QSortFilterProxyModel
from PyQt5.QtGui import QFont, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QVBoxLayout, QLabel, QStatusBar, \
    QApplication, QLineEdit, QTableView

from nauka.db import DB
from nauka.crawler import WorkerThread


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_db()

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

        self.CrawlerLabel = QLabel(self.centralwidget)
        self.CrawlerLabel.setObjectName(u"CrawlerLabel")
        self.CrawlerLabel.setGeometry(QRect(50, 40, 200, 30))
        if self.last_crawled_date:
            self.CrawlerLabel.setText(f'Last crawled on {self.last_crawled_date[0].date()}')

        self.CrawlerLabel.setMaximumSize(QSize(16777215, 30))
        self.CrawlerLabel.setAlignment(Qt.AlignJustify | Qt.AlignVCenter)

        crawler_lbl_font = QFont()
        crawler_lbl_font.setFamily(u"Calibri")
        crawler_lbl_font.setPointSize(10)

        self.CrawlerLabel.setFont(crawler_lbl_font)

        self.statusbar = QStatusBar(self)
        self.statusbar.setObjectName(u"statusbar")
        self.setStatusBar(self.statusbar)

        self.show()

        self.pubs_table = []

    def run_crawler_btn_clicked(self):
        self.ShowPubsBtn.setEnabled(False)
        self.RunCrawlerBtn.setEnabled(False)
        self.RunCrawlerBtn.setText("Crawling nauka.offnews.bg...")
        print("Buttons disabled")

        self.worker = WorkerThread()
        self.worker.start()
        print("Worker started")
        self.worker.finished.connect(self.crawler_run_finished)

    def crawler_run_finished(self):
        print("Worker finished")
        self.RunCrawlerBtn.setEnabled(True)
        self.ShowPubsBtn.setEnabled(True)
        self.RunCrawlerBtn.setText("Crawl nauka.offnews.bg")
        print("Buttons enabled")

        self.last_crawled_date = self.db.select_crawler_data()
        if self.last_crawled_date:
            self.CrawlerLabel.setText(f'Last crawled on {self.last_crawled_date[0].date()}')

    def view_pubs(self):
        self.pubs_table = Table()
        print("Publication table created!")

    def setup_db(self):
        # Setup db data
        self.db = DB()
        self.last_crawled_date = self.db.select_crawler_data()

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
        self.model.setHorizontalHeaderLabels(['Категория', 'Дата', 'Заглавие', 'Детайли'])

        for i, row in enumerate(self.publications):
            # items = [QStandardItem(str(item)[0:100]) for item in row[0:3]]
            items = []
            for item in row[0:3]:
                std_item = QStandardItem(str(item))
                std_item.setEditable(False)
                items.append(std_item)
            details_item = QStandardItem("прочети статията...")
            details_item.setEditable(False)
            items.append(details_item)

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
        self.table_view.doubleClicked.connect(self.view_pub_details)

        # self.table_view.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        # self.adjustSize()

        self.show()
        print("Pubs table view setup!")

    def view_pub_details(self):
        for index in self.table_view.selectionModel().selectedIndexes():
            row_number = index.row()
            global pub
            pub = Publication(self.publications[row_number])
            print(pub)


class Publication(QWidget):
    def __init__(self, pub):
        super().__init__()
        self.category, self.date, self.title, self.text = pub

        self.setup_model()
        self.setup_view()

    def setup_model(self):
        self.model = QStandardItemModel(3,0)
        self.model.setVerticalHeaderLabels(['Категория', 'Дата', 'Заглавие', 'Текст'])
        items = []
        for item in [self.category, self.date, self.title, self.text]:
            std_item = QStandardItem(str(item))
            std_item.setEditable(False)
            items.append(std_item)

        self.model.insertColumn(0, items)

    def setup_view(self):
        # setup layout
        pub_layout = QVBoxLayout()

        # setup the view
        self.pub_view = QTableView()
        pub_layout.addWidget(self.pub_view)
        self.pub_view.SelectionMode(1)

        self.pub_view.setWindowTitle(f'{self.title}')
        self.pub_view.setMinimumWidth(900)
        self.pub_view.setMaximumWidth(1200)
        self.pub_view.setMinimumHeight(600)
        self.pub_view.horizontalScrollBar()
        # self.pub_view.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.pub_view.setModel(self.model)
        self.setLayout(pub_layout)
        self.pub_view.setColumnWidth(0, 800)
        self.pub_view.resizeRowsToContents()


        self.show()

    def __str__(self):
        return f"{self.category}, {self.date}, {self.title}"

if __name__ == '__main__':
    app = QApplication(sys.argv)
    publication = Publication(["Category", "12/12/22", "This is my title", "Text"])
    sys.exit(app.exec_())
