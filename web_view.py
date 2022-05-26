import sys
from tkinter import NW
from tokenize import String
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView

class Widget(QWidget):
    def __init__(self, url):
        super().__init__()
        self.url = url
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Query')
        web_view = QWebEngineView()
        web_view.setUrl(QUrl(self.url))
        button = QPushButton('Get URL', self)
        button.resize(button.sizeHint())
        button.clicked.connect(lambda: self.set_url(web_view))
        lay = QVBoxLayout(self)
        lay.addWidget(button)
        lay.addWidget(web_view)

    def set_url(self, web_view):
        self.url = web_view.url().toString()
        print("Obtained url: " + self.url)

    def get_url(self):
        return self.url

def web_view(url):
    app = QApplication(sys.argv)
    widget = Widget(url)
    widget.show()
    app.exec_()
    return widget.get_url()
