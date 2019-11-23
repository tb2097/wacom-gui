#!/usr/bin/python

from PyQt5 import QtWebKit
from PyQt5 import QtCore, QtGui
import sys, os, re

class Help(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.initUI()

    def initUI(self):
        self.browser = QtWebKit.QWebView()
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "help.html"))
        local_url = QtCore.QUrl.fromLocalFile(file_path)
        self.browser.load(local_url)

        self.mainLayout = QtGui.QHBoxLayout()
        self.mainLayout.addWidget(self.browser)
        self.setLayout(self.mainLayout)
