import sys

from PyQt5.QtCore import QRect, QSize, Qt, QMetaObject
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QSizePolicy, QWidget, QPushButton, QVBoxLayout, QLabel, QStatusBar, \
    QApplication


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

        self.verticalLayout.addWidget(self.ShowPubsBtn)

        self.WelcomeLabel = QLabel(self.centralwidget)
        self.WelcomeLabel.setObjectName(u"WelcomeLabel")
        self.WelcomeLabel.setGeometry(QRect(100, 20, 74, 30))
        self.WelcomeLabel.setText('Welcome!')

        self.WelcomeLabel.setMaximumSize(QSize(16777215, 30))
        self.WelcomeLabel.setAlignment(Qt.AlignJustify | Qt.AlignVCenter)

        # self.MessagesLabel = QLabel(self.centralwidget)
        # self.MessagesLabel.setObjectName(u"MessagesLabel")
        # self.MessagesLabel.setGeometry(QRect(50, 40, 150, 30))
        #
        # self.MessagesLabel.setMaximumSize(QSize(16777215, 50))
        # self.MessagesLabel.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        #
        # msg_font = QFont()
        # msg_font.setPointSize(9)
        #
        # self.MessagesLabel.setFont(msg_font)

        self.statusbar = QStatusBar(self)
        self.statusbar.setObjectName(u"statusbar")
        self.setStatusBar(self.statusbar)

        # QMetaObject.connectSlotsByName(self)

        self.show()

    def run_crawler_btn_clicked(self):
        self.RunCrawlerBtn.setEnabled(False)
        self.RunCrawlerBtn.setText("Crawler started...")

        # self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())
