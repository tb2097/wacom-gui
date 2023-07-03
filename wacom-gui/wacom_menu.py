# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'wacom_menu.ui'
#
# Created: Wed Nov 14 16:02:43 2018
#      by: PyQt5 UI code generator 4.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.setEnabled(True)
        MainWindow.resize(900, 900)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(900, 900))
        MainWindow.setMaximumSize(QtCore.QSize(900, 900))
        MainWindow.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.formLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 0, 881, 301))
        self.formLayoutWidget.setObjectName(_fromUtf8("formLayoutWidget"))
        self.controlLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.controlLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.controlLayout.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        # self.controlLayout.setMargin(4)
        self.controlLayout.setSpacing(4)
        self.controlLayout.setObjectName(_fromUtf8("controlLayout"))
        self.tabletLbl = QtWidgets.QLabel(self.formLayoutWidget)
        self.tabletLbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.tabletLbl.setObjectName(_fromUtf8("tabletLbl"))
        self.controlLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.tabletLbl)
        self.toolLbl = QtWidgets.QLabel(self.formLayoutWidget)
        self.toolLbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.toolLbl.setObjectName(_fromUtf8("toolLbl"))
        self.controlLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.toolLbl)
        self.toolScroll = QtWidgets.QScrollArea(self.formLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
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
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 821, 86))
        self.scrollAreaWidgetContents_2.setObjectName(_fromUtf8("scrollAreaWidgetContents_2"))
        self.toolScroll.setWidget(self.scrollAreaWidgetContents_2)
        self.controlLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.toolScroll)
        self.configLbl = QtWidgets.QLabel(self.formLayoutWidget)
        self.configLbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.configLbl.setObjectName(_fromUtf8("configLbl"))
        self.controlLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.configLbl)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.tabletScroll = QtWidgets.QScrollArea(self.formLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabletScroll.sizePolicy().hasHeightForWidth())
        self.tabletScroll.setSizePolicy(sizePolicy)
        self.tabletScroll.setMinimumSize(QtCore.QSize(0, 100))
        self.tabletScroll.setMaximumSize(QtCore.QSize(780, 16777215))
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
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 776, 96))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.tabletScroll.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout.addWidget(self.tabletScroll)
        self.tabletRefresh = QtWidgets.QPushButton(self.formLayoutWidget)
        self.tabletRefresh.setMaximumSize(QtCore.QSize(30, 30))
        self.tabletRefresh.setText(_fromUtf8(""))
        self.tabletRefresh.setObjectName(_fromUtf8("tabletRefresh"))
        self.horizontalLayout.addWidget(self.tabletRefresh)
        self.controlLayout.setLayout(0, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.configScroll = QtWidgets.QScrollArea(self.formLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.configScroll.sizePolicy().hasHeightForWidth())
        self.configScroll.setSizePolicy(sizePolicy)
        self.configScroll.setMinimumSize(QtCore.QSize(0, 90))
        self.configScroll.setMaximumSize(QtCore.QSize(740, 80))
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
        self.scrollAreaWidgetContents_3 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_3.setGeometry(QtCore.QRect(0, 0, 725, 86))
        self.scrollAreaWidgetContents_3.setObjectName(_fromUtf8("scrollAreaWidgetContents_3"))
        self.configScroll.setWidget(self.scrollAreaWidgetContents_3)
        self.horizontalLayout_2.addWidget(self.configScroll)
        self.configControls = QtWidgets.QVBoxLayout()
        self.configControls.setSpacing(0)
        self.configControls.setObjectName(_fromUtf8("configControls"))
        self.addConfig = QtWidgets.QPushButton(self.formLayoutWidget)
        self.addConfig.setEnabled(False)
        self.addConfig.setMaximumSize(QtCore.QSize(30, 30))
        self.addConfig.setObjectName(_fromUtf8("addConfig"))
        self.configControls.addWidget(self.addConfig)
        self.removeConfig = QtWidgets.QPushButton(self.formLayoutWidget)
        self.removeConfig.setEnabled(False)
        self.removeConfig.setMaximumSize(QtCore.QSize(30, 30))
        self.removeConfig.setObjectName(_fromUtf8("removeConfig"))
        self.configControls.addWidget(self.removeConfig)
        self.saveConfig = QtWidgets.QPushButton(self.formLayoutWidget)
        self.saveConfig.setObjectName(_fromUtf8("saveConfig"))
        self.configControls.addWidget(self.saveConfig)
        self.horizontalLayout_2.addLayout(self.configControls)
        self.controlLayout.setLayout(2, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_2)
        self.controlBox = QtWidgets.QGroupBox(self.centralwidget)
        self.controlBox.setGeometry(QtCore.QRect(10, 310, 880, 540))
        self.controlBox.setMinimumSize(QtCore.QSize(880, 540))
        self.controlBox.setMaximumSize(QtCore.QSize(880, 540))
        self.controlBox.setStyleSheet(_fromUtf8(""))
        self.controlBox.setTitle(_fromUtf8(""))
        self.controlBox.setObjectName(_fromUtf8("controlBox"))
        self.aboutButton = QtWidgets.QPushButton(self.centralwidget)
        self.aboutButton.setGeometry(QtCore.QRect(770, 860, 90, 20))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.aboutButton.sizePolicy().hasHeightForWidth())
        self.aboutButton.setSizePolicy(sizePolicy)
        self.aboutButton.setObjectName(_fromUtf8("aboutButton"))
        self.helpButton = QtWidgets.QPushButton(self.centralwidget)
        self.helpButton.setGeometry(QtCore.QRect(870, 860, 20, 20))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.helpButton.sizePolicy().hasHeightForWidth())
        self.helpButton.setSizePolicy(sizePolicy)
        self.helpButton.setStyleSheet(_fromUtf8("border-radius: 10px;\n"
"border-style: inset;\n"
"border-width: 1px;\n"
""))
        self.helpButton.setObjectName(_fromUtf8("helpButton"))
        self.deviceDefaults = QtWidgets.QPushButton(self.centralwidget)
        self.deviceDefaults.setGeometry(QtCore.QRect(650, 860, 111, 20))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.deviceDefaults.sizePolicy().hasHeightForWidth())
        self.deviceDefaults.setSizePolicy(sizePolicy)
        self.deviceDefaults.setObjectName(_fromUtf8("deviceDefaults"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 900, 20))
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
        self.aboutButton.setText(_translate("MainWindow", "About", None))
        self.helpButton.setText(_translate("MainWindow", "?", None))
        self.deviceDefaults.setText(_translate("MainWindow", "Restore Defaults", None))

