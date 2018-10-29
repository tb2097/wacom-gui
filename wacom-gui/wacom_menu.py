# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'wacom_menu.ui'
#
# Created: Thu Sep 20 15:13:55 2018
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.setEnabled(True)
        MainWindow.resize(600, 900)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(600, 800))
        MainWindow.setMaximumSize(QtCore.QSize(600, 900))
        MainWindow.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.formLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 0, 581, 301))
        self.formLayoutWidget.setObjectName(_fromUtf8("formLayoutWidget"))
        self.controlLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.controlLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.controlLayout.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.controlLayout.setMargin(4)
        self.controlLayout.setSpacing(4)
        self.controlLayout.setObjectName(_fromUtf8("controlLayout"))
        self.tabletLbl = QtGui.QLabel(self.formLayoutWidget)
        self.tabletLbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.tabletLbl.setObjectName(_fromUtf8("tabletLbl"))
        self.controlLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.tabletLbl)
        self.toolLbl = QtGui.QLabel(self.formLayoutWidget)
        self.toolLbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.toolLbl.setObjectName(_fromUtf8("toolLbl"))
        self.controlLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.toolLbl)
        self.toolScroll = QtGui.QScrollArea(self.formLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolScroll.sizePolicy().hasHeightForWidth())
        self.toolScroll.setSizePolicy(sizePolicy)
        self.toolScroll.setMinimumSize(QtCore.QSize(0, 90))
        self.toolScroll.setStyleSheet(_fromUtf8("QScrollBar:horizontal {\n"
"            border: none;\n"
"            background: none;\n"
"            height: 6px;\n"
"            margin: 0px 26px 0 26px;\n"
"        }\n"
"\n"
"        QScrollBar::handle:horizontal {\n"
"            background: rgb(90,90,90,90);\n"
"            border-width: 2px;\n"
"            border-radius: 2px;\n"
"            border-color: rgb(0,0,0,100);\n"
"            min-width: 6px;\n"
"            \n"
"        }\n"
"\n"
"        QScrollBar::add-line:horizontal {\n"
"            background: none;\n"
"            width: 6px;\n"
"            subcontrol-position: right;\n"
"            subcontrol-origin: margin;\n"
"            \n"
"        }\n"
"\n"
"        QScrollBar::sub-line:horizontal {\n"
"            background: none;\n"
"            width: 6px;\n"
"            subcontrol-position: top left;\n"
"            subcontrol-origin: margin;\n"
"            position: absolute;\n"
"        }"))
        self.toolScroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.toolScroll.setWidgetResizable(True)
        self.toolScroll.setObjectName(_fromUtf8("toolScroll"))
        self.scrollAreaWidgetContents_2 = QtGui.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 521, 86))
        self.scrollAreaWidgetContents_2.setObjectName(_fromUtf8("scrollAreaWidgetContents_2"))
        self.toolScroll.setWidget(self.scrollAreaWidgetContents_2)
        self.controlLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.toolScroll)
        self.configLbl = QtGui.QLabel(self.formLayoutWidget)
        self.configLbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.configLbl.setObjectName(_fromUtf8("configLbl"))
        self.controlLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.configLbl)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.tabletScroll = QtGui.QScrollArea(self.formLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabletScroll.sizePolicy().hasHeightForWidth())
        self.tabletScroll.setSizePolicy(sizePolicy)
        self.tabletScroll.setMinimumSize(QtCore.QSize(0, 100))
        self.tabletScroll.setMaximumSize(QtCore.QSize(480, 16777215))
        self.tabletScroll.setAutoFillBackground(False)
        self.tabletScroll.setStyleSheet(_fromUtf8("QScrollBar:horizontal {\n"
"            border: none;\n"
"            background: none;\n"
"            height: 6px;\n"
"            margin: 0px 26px 0 26px;\n"
"        }\n"
"\n"
"        QScrollBar::handle:horizontal {\n"
"            background: rgb(90,90,90,90);\n"
"            border-width: 2px;\n"
"            border-radius: 2px;\n"
"            border-color: rgb(0,0,0,100);\n"
"            min-width: 6px;\n"
"            \n"
"        }\n"
"\n"
"        QScrollBar::add-line:horizontal {\n"
"            background: none;\n"
"            width: 6px;\n"
"            subcontrol-position: right;\n"
"            subcontrol-origin: margin;\n"
"            \n"
"        }\n"
"\n"
"        QScrollBar::sub-line:horizontal {\n"
"            background: none;\n"
"            width: 6px;\n"
"            subcontrol-position: top left;\n"
"            subcontrol-origin: margin;\n"
"            position: absolute;\n"
"        }"))
        self.tabletScroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tabletScroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.tabletScroll.setWidgetResizable(True)
        self.tabletScroll.setObjectName(_fromUtf8("tabletScroll"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 476, 96))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.tabletScroll.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout.addWidget(self.tabletScroll)
        self.tabletRefresh = QtGui.QPushButton(self.formLayoutWidget)
        self.tabletRefresh.setMaximumSize(QtCore.QSize(30, 30))
        self.tabletRefresh.setText(_fromUtf8(""))
        self.tabletRefresh.setObjectName(_fromUtf8("tabletRefresh"))
        self.horizontalLayout.addWidget(self.tabletRefresh)
        self.controlLayout.setLayout(0, QtGui.QFormLayout.FieldRole, self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.configScroll = QtGui.QScrollArea(self.formLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.configScroll.sizePolicy().hasHeightForWidth())
        self.configScroll.setSizePolicy(sizePolicy)
        self.configScroll.setMinimumSize(QtCore.QSize(0, 90))
        self.configScroll.setMaximumSize(QtCore.QSize(500, 80))
        self.configScroll.setStyleSheet(_fromUtf8("QScrollBar:horizontal {\n"
"            border: none;\n"
"            background: none;\n"
"            height: 6px;\n"
"            margin: 0px 26px 0 26px;\n"
"        }\n"
"\n"
"        QScrollBar::handle:horizontal {\n"
"            background: rgb(90,90,90,90);\n"
"            border-width: 2px;\n"
"            border-radius: 2px;\n"
"            border-color: rgb(0,0,0,100);\n"
"            min-width: 6px;\n"
"            \n"
"        }\n"
"\n"
"        QScrollBar::add-line:horizontal {\n"
"            background: none;\n"
"            width: 6px;\n"
"            subcontrol-position: right;\n"
"            subcontrol-origin: margin;\n"
"            \n"
"        }\n"
"\n"
"        QScrollBar::sub-line:horizontal {\n"
"            background: none;\n"
"            width: 6px;\n"
"            subcontrol-position: top left;\n"
"            subcontrol-origin: margin;\n"
"            position: absolute;\n"
"        }"))
        self.configScroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.configScroll.setWidgetResizable(True)
        self.configScroll.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.configScroll.setObjectName(_fromUtf8("configScroll"))
        self.scrollAreaWidgetContents_3 = QtGui.QWidget()
        self.scrollAreaWidgetContents_3.setGeometry(QtCore.QRect(0, 0, 425, 86))
        self.scrollAreaWidgetContents_3.setObjectName(_fromUtf8("scrollAreaWidgetContents_3"))
        self.configScroll.setWidget(self.scrollAreaWidgetContents_3)
        self.horizontalLayout_2.addWidget(self.configScroll)
        self.configControls = QtGui.QVBoxLayout()
        self.configControls.setSpacing(0)
        self.configControls.setObjectName(_fromUtf8("configControls"))
        self.addConfig = QtGui.QPushButton(self.formLayoutWidget)
        self.addConfig.setEnabled(False)
        self.addConfig.setMaximumSize(QtCore.QSize(30, 30))
        self.addConfig.setObjectName(_fromUtf8("addConfig"))
        self.configControls.addWidget(self.addConfig)
        self.removeConfig = QtGui.QPushButton(self.formLayoutWidget)
        self.removeConfig.setEnabled(False)
        self.removeConfig.setMaximumSize(QtCore.QSize(30, 30))
        self.removeConfig.setObjectName(_fromUtf8("removeConfig"))
        self.configControls.addWidget(self.removeConfig)
        self.saveConfig = QtGui.QPushButton(self.formLayoutWidget)
        self.saveConfig.setObjectName(_fromUtf8("saveConfig"))
        self.configControls.addWidget(self.saveConfig)
        self.horizontalLayout_2.addLayout(self.configControls)
        self.controlLayout.setLayout(2, QtGui.QFormLayout.FieldRole, self.horizontalLayout_2)
        self.controlBox = QtGui.QGroupBox(self.centralwidget)
        self.controlBox.setGeometry(QtCore.QRect(10, 310, 581, 551))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.controlBox.sizePolicy().hasHeightForWidth())
        self.controlBox.setSizePolicy(sizePolicy)
        self.controlBox.setStyleSheet(_fromUtf8("background-color: rgb(222, 222, 222);"))
        self.controlBox.setTitle(_fromUtf8(""))
        self.controlBox.setFlat(False)
        self.controlBox.setObjectName(_fromUtf8("controlBox"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setEnabled(True)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 600, 20))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        MainWindow.setMenuBar(self.menuBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Wacom GUI", None))
        self.tabletLbl.setText(_translate("MainWindow", "Tablet:", None))
        self.toolLbl.setText(_translate("MainWindow", "Tool:", None))
        self.configLbl.setText(_translate("MainWindow", "Config:", None))
        self.addConfig.setText(_translate("MainWindow", "+", None))
        self.removeConfig.setText(_translate("MainWindow", "-", None))
        self.saveConfig.setText(_translate("MainWindow", "Save Config", None))

