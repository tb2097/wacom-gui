# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'keystroke_dialog.ui'
#
# Created: Wed Oct 24 15:09:24 2018
#      by: PyQt5 UI code generator 4.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui

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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(625, 139)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.formLayoutWidget = QtGui.QWidget(Dialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 10, 601, 121))
        self.formLayoutWidget.setObjectName(_fromUtf8("formLayoutWidget"))
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setMargin(0)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.keystrokesLabel = QtGui.QLabel(self.formLayoutWidget)
        self.keystrokesLabel.setObjectName(_fromUtf8("keystrokesLabel"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.keystrokesLabel)
        self.keystrokeinput = QtGui.QLineEdit(self.formLayoutWidget)
        self.keystrokeinput.setReadOnly(True)
        self.keystrokeinput.setObjectName(_fromUtf8("keystrokeinput"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.keystrokeinput)
        self.shortcutLabel = QtGui.QLabel(self.formLayoutWidget)
        self.shortcutLabel.setObjectName(_fromUtf8("shortcutLabel"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.shortcutLabel)
        self.shortcutinput = QtGui.QLineEdit(self.formLayoutWidget)
        self.shortcutinput.setObjectName(_fromUtf8("shortcutinput"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.shortcutinput)
        self.runLabel = QtGui.QLabel(self.formLayoutWidget)
        self.runLabel.setObjectName(_fromUtf8("runLabel"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.runLabel)
        self.runinput = QtGui.QLineEdit(self.formLayoutWidget)
        self.runinput.setObjectName(_fromUtf8("runinput"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.runinput)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.keystroke = QtGui.QPushButton(self.formLayoutWidget)
        self.keystroke.setMaximumSize(QtCore.QSize(100, 16777215))
        self.keystroke.setObjectName(_fromUtf8("keystroke"))
        self.horizontalLayout_2.addWidget(self.keystroke)
        self.buttonBox = QtGui.QDialogButtonBox(self.formLayoutWidget)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.horizontalLayout_2.addWidget(self.buttonBox)
        self.formLayout.setLayout(3, QtGui.QFormLayout.FieldRole, self.horizontalLayout_2)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.keystrokesLabel.setText(_translate("Dialog", "Keystrokes", None))
        self.shortcutLabel.setText(_translate("Dialog", "Shortcut Name", None))
        self.runLabel.setText(_translate("Dialog", "Run Command", None))
        self.keystroke.setText(_translate("Dialog", "Keystroke...", None))

