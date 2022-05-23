import sys
from tkinter import Widget
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngine import *
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtWebEngineWidgets import QWebEngineView
import os

class Web(QWebEngineView):

    def load(self, url):
        self.setUrl(QUrl(url))

    def adjustTitle(self):
        self.setWindowTitle(self.title())


class Main(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Query')

        web_view = Web()

        web_view.load("https://google.com")

        self.btn = QPushButton('Button', self)
        self.btn.resize(self.btn.sizeHint())
        self.btn.clicked.connect(lambda: self.get_query(web_view))
        lay = QVBoxLayout(self)
        lay.addWidget(self.btn)
        lay.addWidget(web_view)

    def get_query(self, web_view):
        print(web_view.url().toString())


app = QApplication(sys.argv)
main = Main()
main.show()
app.exec_()