#!/usr/bin/python

# ideas pitched from:
#  https://stackoverflow.com/questions/12768542/parse-and-display-html-in-a-qtextedit-widget
#  http://www.qtcentre.org/threads/29801-Inserting-html-and-plain-text-in-QTextEdit
#  ... and other places ...

from PyQt4 import QtCore, QtGui
import sys, os, re

class Help(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.initUI()
        self.setMinimumWidth(600)

    def initUI(self):
        helpdoc = os.path.dirname(os.path.realpath(__file__)) + "/help.html"
        # layout code
        self.mainLayout = QtGui.QHBoxLayout()
        self.textArea = QtGui.QTextEdit(self)
        self.textArea.setReadOnly(True)
        self.cursor = QtGui.QTextCursor(self.textArea.document())
        f = QtCore.QFile(helpdoc)
        f.open(QtCore.QFile.ReadOnly|QtCore.QFile.Text)
        istream = QtCore.QTextStream(f)
        self.cursor.insertHtml(istream.readAll())
        f.close()
        self.textArea.moveCursor(QtGui.QTextCursor.Start)

        # layout code
        self.mainLayout.setAlignment(QtCore.Qt.AlignCenter)
        self.mainLayout.addWidget(self.textArea)
        self.setLayout(self.mainLayout)