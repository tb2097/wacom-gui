#!/usr/bin/python

from Qt import QtCore, QtWidgets
import sys, os, re

class Help(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.initUI()

    def initUI(self):
        self.browser = QtWebKit.QWebView()
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "help.html"))
        local_url = QtCore.QUrl.fromLocalFile(file_path)
        self.browser.load(local_url)

        self.mainLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addWidget(self.browser)
        self.setLayout(self.mainLayout)
