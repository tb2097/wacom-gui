# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pad_ui.ui'
#
# Created: Wed Nov 14 16:04:03 2018
#      by: PyQt4 UI code generator 4.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_PadWidget(object):
    def setupUi(self, PadWidget):
        PadWidget.setObjectName(_fromUtf8("PadWidget"))
        PadWidget.resize(840, 520)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(PadWidget.sizePolicy().hasHeightForWidth())
        PadWidget.setSizePolicy(sizePolicy)
        PadWidget.setMinimumSize(QtCore.QSize(840, 520))
        PadWidget.setMaximumSize(QtCore.QSize(840, 520))
        PadWidget.setStyleSheet(_fromUtf8("QTabBar::tab:selected {\n"
"                                    border-bottom: 3px solid qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #6DD7E8);\n"
"                                }\n"
"                                QTabBar::tab {\n"
"                                    padding: 5px 15px 3px 15px;\n"
"                                    margin-top: 10px;\n"
"                                    color: #080808;\n"
"                                    border-top-left-radius: 4px;\n"
"                                    border-top-right-radius: 4px;\n"
"                                }\n"
"border-style: none;\n"
"border-width: 0px;"))
        self.keys = QtGui.QWidget()
        self.keys.setObjectName(_fromUtf8("keys"))
        self.gridLayoutWidget = QtGui.QWidget(self.keys)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 831, 481))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.keysLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.keysLayout.setMargin(0)
        self.keysLayout.setObjectName(_fromUtf8("keysLayout"))
        PadWidget.addTab(self.keys, _fromUtf8(""))

        self.retranslateUi(PadWidget)
        PadWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(PadWidget)

    def retranslateUi(self, PadWidget):
        PadWidget.setWindowTitle(_translate("PadWidget", "TabWidget", None))
        PadWidget.setTabText(PadWidget.indexOf(self.keys), _translate("PadWidget", "Express Keys", None))

