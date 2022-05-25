import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView


def get_query(web_view):
        print(web_view.url().toString())


def web_view(url):
    app = QApplication(sys.argv)
    widget = QWidget()
    widget.setWindowTitle('Query')

    web_view = QWebEngineView()
    web_view.setUrl(QUrl(url))

    button = QPushButton('Get URL', widget)
    button.resize(button.sizeHint())
    button.clicked.connect(lambda: get_query(web_view))

    lay = QVBoxLayout(widget)
    lay.addWidget(button)
    lay.addWidget(web_view)

    widget.show()
    app.exec_()

web_view()