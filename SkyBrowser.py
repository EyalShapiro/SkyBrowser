from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWidgets import (
    QMainWindow,
    QApplication,
    QStatusBar,
    QAction,
    QToolBar,
    QLineEdit,
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
import sys


class MainWindow(QMainWindow):
    def __init__(self, app, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.app = app
        self.init_ui()

    def init_ui(self):
        self.setup_browser()
        self.setup_status_bar()
        self.setup_navigation_toolbar()
        self.show()

    def setup_browser(self):
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("http://google.com"))
        self.browser.urlChanged.connect(self.update_url_bar)
        self.browser.loadFinished.connect(self.update_title)
        self.setCentralWidget(self.browser)

    def setup_status_bar(self):
        self.status = QStatusBar()
        self.setStatusBar(self.status)

    def setup_navigation_toolbar(self):
        nav_bar = QToolBar("Navigation")
        self.addToolBar(nav_bar)

        actions = [
            ("Back", "Back to previous page", self.browser.back, "Alt+Left"),
            ("Forward", "Forward to next page", self.browser.forward, "Alt+Right"),
            ("Reload", "Reload page", self.browser.reload, "F5"),
            ("Home", "Go home", self.navigate_home, "Alt+H"),
            ("Stop", "Stop loading current page", self.browser.stop, "Esc"),
        ]

        for name, tooltip, action, shortcut in actions:
            btn = QAction(name, self)
            btn.setStatusTip(tooltip)
            if action:
                btn.triggered.connect(action)
            if shortcut:
                btn.setShortcut(shortcut)
            nav_bar.addAction(btn)

        nav_bar.addSeparator()

        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        nav_bar.addWidget(self.urlbar)

        # Applying style to the toolbar
        nav_bar.setStyleSheet(
            """
            QToolBar {
                background-color: teal;
                border: 1px groove #ccc;
                padding:1px;
            }
            QToolButton {
                background-color:#fff ;
                border:1px groove #ccc;
                border-radius: 1rem;

            }
            QLineEdit {
                background-color: white;
                border: 1px groove #ccc;
                border-radius: 4px;
                padding: 2px;
            }
            """
        )

    def update_title(self):
        title = self.browser.page().title()
        self.setWindowTitle(f"{title} - SkyBrowser")

    def navigate_home(self):
        self.browser.setUrl(QUrl("https://www.bing.com"))

    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())
        if q.scheme() == "":
            q.setScheme("http")
        self.browser.setUrl(q)

    def update_url_bar(self, q):
        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("SkyBrowser")
    window = MainWindow(app)
    app.exec_()


if __name__ == "__main__":
    main()
