# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'stylus_ui.ui'
#
# Created: Tue Nov 20 09:08:43 2018
#      by: PyQt4 UI code generator 4.10.1
#
# WARNING! All changes made in this file will be lost!

from Qt import QtCore, QtCompat, QtWidgets

try:
    _fromUtf8 = str
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtCompat.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtCompat.translate(context, text, disambig)

class Ui_StylusWidget(object):
    def setupUi(self, StylusWidget):
        StylusWidget.setObjectName(_fromUtf8("StylusWidget"))
        StylusWidget.resize(840, 520)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(StylusWidget.sizePolicy().hasHeightForWidth())
        StylusWidget.setSizePolicy(sizePolicy)
        StylusWidget.setMinimumSize(QtCore.QSize(840, 520))
        StylusWidget.setMaximumSize(QtCore.QSize(840, 520))
        StylusWidget.setStyleSheet(_fromUtf8("QTabBar::tab:selected {\n"
"                                    border-bottom: 3px solid qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #6DD7E8);\n"
"                                }\n"
"                                QTabBar::tab {\n"
"                                    padding: 5px 15px 3px 15px;\n"
"                                    margin-top: 10px;\n"
"                                    color: #080808;\n"
"                                    border-radius: 4px;\n"
"                                }\n"
"QProgressBar {\n"
"border: 1px solid black;\n"
"text-align: top;\n"
"padding: 1px;\n"
"border-radius: 2px;\n"
"background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1,\n"
"stop: 0 #fff,\n"
"stop: 0.4999 #eee,\n"
"stop: 0.5 #ddd,\n"
"stop: 1 #eee );\n"
"width: 15px;\n"
"}\n"
"\n"
"QProgressBar::chunk {\n"
"background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1,\n"
"stop: 0 #a2e7f2,\n"
"stop: 0.4999 #6DD7E8,\n"
"stop: 0.5 #58aebc,\n"
"stop: 1 #213f44 );\n"
"border-radius: 1px;\n"
"border: 1px solid black;\n"
"}\n"
"border-style: none;\n"
"border-width: 0px;"))
        self.keys = QtWidgets.QWidget()
        self.keys.setObjectName(_fromUtf8("keys"))
        self.penImage = QtWidgets.QLabel(self.keys)
        self.penImage.setGeometry(QtCore.QRect(390, 20, 106, 440))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.penImage.sizePolicy().hasHeightForWidth())
        self.penImage.setSizePolicy(sizePolicy)
        self.penImage.setMinimumSize(QtCore.QSize(106, 440))
        self.penImage.setMaximumSize(QtCore.QSize(106, 440))
        self.penImage.setObjectName(_fromUtf8("penImage"))
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(self.keys)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(0, 20, 301, 451))
        self.verticalLayoutWidget_4.setObjectName(_fromUtf8("verticalLayoutWidget_4"))
        self.penToolLeft = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.penToolLeft.setSpacing(0)
        self.penToolLeft.setMargin(0)
        self.penToolLeft.setObjectName(_fromUtf8("penToolLeft"))
        self.verticalLayoutWidget_5 = QtWidgets.QWidget(self.keys)
        self.verticalLayoutWidget_5.setGeometry(QtCore.QRect(530, 20, 301, 421))
        self.verticalLayoutWidget_5.setObjectName(_fromUtf8("verticalLayoutWidget_5"))
        self.penToolRight = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_5)
        self.penToolRight.setSpacing(0)
        self.penToolRight.setMargin(0)
        self.penToolRight.setObjectName(_fromUtf8("penToolRight"))
        self.penDefault = QtWidgets.QPushButton(self.keys)
        self.penDefault.setGeometry(QtCore.QRect(740, 450, 84, 25))
        self.penDefault.setObjectName(_fromUtf8("penDefault"))
        StylusWidget.addTab(self.keys, _fromUtf8(""))
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.eraserImage = QtWidgets.QLabel(self.tab)
        self.eraserImage.setGeometry(QtCore.QRect(390, 20, 106, 440))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.eraserImage.sizePolicy().hasHeightForWidth())
        self.eraserImage.setSizePolicy(sizePolicy)
        self.eraserImage.setMinimumSize(QtCore.QSize(106, 440))
        self.eraserImage.setMaximumSize(QtCore.QSize(106, 440))
        self.eraserImage.setObjectName(_fromUtf8("eraserImage"))
        self.verticalLayoutWidget_6 = QtWidgets.QWidget(self.tab)
        self.verticalLayoutWidget_6.setGeometry(QtCore.QRect(0, 20, 301, 451))
        self.verticalLayoutWidget_6.setObjectName(_fromUtf8("verticalLayoutWidget_6"))
        self.eraserToolLeft = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_6)
        self.eraserToolLeft.setSpacing(0)
        self.eraserToolLeft.setMargin(0)
        self.eraserToolLeft.setObjectName(_fromUtf8("eraserToolLeft"))
        self.verticalLayoutWidget_7 = QtWidgets.QWidget(self.tab)
        self.verticalLayoutWidget_7.setGeometry(QtCore.QRect(530, 20, 301, 421))
        self.verticalLayoutWidget_7.setObjectName(_fromUtf8("verticalLayoutWidget_7"))
        self.eraserToolRight = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_7)
        self.eraserToolRight.setSpacing(0)
        self.eraserToolRight.setMargin(0)
        self.eraserToolRight.setObjectName(_fromUtf8("eraserToolRight"))
        self.eraserDefault = QtWidgets.QPushButton(self.tab)
        self.eraserDefault.setGeometry(QtCore.QRect(740, 450, 84, 25))
        self.eraserDefault.setObjectName(_fromUtf8("eraserDefault"))
        StylusWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.verticalLayoutWidget_8 = QtWidgets.QWidget(self.tab_2)
        self.verticalLayoutWidget_8.setGeometry(QtCore.QRect(530, 20, 301, 421))
        self.verticalLayoutWidget_8.setObjectName(_fromUtf8("verticalLayoutWidget_8"))
        self.mappingToolRight = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_8)
        self.mappingToolRight.setSpacing(0)
        self.mappingToolRight.setMargin(0)
        self.mappingToolRight.setObjectName(_fromUtf8("mappingToolRight"))
        self.mappingImage = QtWidgets.QLabel(self.tab_2)
        self.mappingImage.setGeometry(QtCore.QRect(40, 20, 340, 440))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mappingImage.sizePolicy().hasHeightForWidth())
        self.mappingImage.setSizePolicy(sizePolicy)
        self.mappingImage.setMinimumSize(QtCore.QSize(340, 440))
        self.mappingImage.setMaximumSize(QtCore.QSize(340, 440))
        self.mappingImage.setObjectName(_fromUtf8("mappingImage"))
        self.mappingDefault = QtWidgets.QPushButton(self.tab_2)
        self.mappingDefault.setGeometry(QtCore.QRect(740, 450, 84, 25))
        self.mappingDefault.setObjectName(_fromUtf8("mappingDefault"))
        StylusWidget.addTab(self.tab_2, _fromUtf8(""))

        self.retranslateUi(StylusWidget)
        StylusWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(StylusWidget)

    def retranslateUi(self, StylusWidget):
        StylusWidget.setWindowTitle(_translate("StylusWidget", "TabWidget", None))
        self.penImage.setText(_translate("StylusWidget", "TextLabel", None))
        self.penDefault.setText(_translate("StylusWidget", "Default", None))
        StylusWidget.setTabText(StylusWidget.indexOf(self.keys), _translate("StylusWidget", "Pen", None))
        self.eraserImage.setText(_translate("StylusWidget", "TextLabel", None))
        self.eraserDefault.setText(_translate("StylusWidget", "Default", None))
        StylusWidget.setTabText(StylusWidget.indexOf(self.tab), _translate("StylusWidget", "Eraser", None))
        self.mappingImage.setText(_translate("StylusWidget", "TextLabel", None))
        self.mappingDefault.setText(_translate("StylusWidget", "Default", None))
        StylusWidget.setTabText(StylusWidget.indexOf(self.tab_2), _translate("StylusWidget", "Mapping", None))

