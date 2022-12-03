import sys
from PyQt5.QtCore import QUrl, QEventLoop
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView


APP = QApplication(['', '--no-sandbox'])


class Widget(QWidget):
    def __init__(self, url):
        super().__init__()
        self.url = url
        self.initUI()

    def initUI(self):

        # set title
        self.setWindowTitle('Query')

        # create web view
        web_view = QWebEngineView()
        web_view.setUrl(QUrl(self.url))

        # create button
        button = QPushButton('Get Query', self)
        button.resize(button.sizeHint())
        button.clicked.connect(lambda: self.set_url(web_view))

        # create layout
        lay = QVBoxLayout(self)
        lay.addWidget(button)
        lay.addWidget(web_view)

    def set_url(self, web_view):
        self.url = web_view.url().toString()
        self.close()


    def get_url(self):
        return self.url


def webView(url):
    
    app = QApplication.instance()
    app.processEvents(QEventLoop.ExcludeUserInputEvents | QEventLoop.ExcludeSocketNotifiers | QEventLoop.WaitForMoreEvents)

    widget = Widget(url)
    widget.showMaximized()

    return_code = app.exec_()
    if return_code:
        print(f"Return code: {return_code}... exiting")
        exit(return_code)

    app.quit()

    return widget.get_url()