# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'keystroke_dialog.ui'
#
# Created: Wed Oct 24 15:09:24 2018
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(625, 139)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.formLayoutWidget = QtWidgets.QWidget(Dialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 10, 601, 121))
        self.formLayoutWidget.setObjectName(_fromUtf8("formLayoutWidget"))
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setMargin(0)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.keystrokesLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.keystrokesLabel.setObjectName(_fromUtf8("keystrokesLabel"))
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.keystrokesLabel)
        self.keystrokeinput = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.keystrokeinput.setReadOnly(True)
        self.keystrokeinput.setObjectName(_fromUtf8("keystrokeinput"))
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.keystrokeinput)
        self.shortcutLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.shortcutLabel.setObjectName(_fromUtf8("shortcutLabel"))
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.shortcutLabel)
        self.shortcutinput = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.shortcutinput.setObjectName(_fromUtf8("shortcutinput"))
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.shortcutinput)
        self.runLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.runLabel.setObjectName(_fromUtf8("runLabel"))
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.runLabel)
        self.runinput = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.runinput.setObjectName(_fromUtf8("runinput"))
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.runinput)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.keystroke = QtWidgets.QPushButton(self.formLayoutWidget)
        self.keystroke.setMaximumSize(QtCore.QSize(100, 16777215))
        self.keystroke.setObjectName(_fromUtf8("keystroke"))
        self.horizontalLayout_2.addWidget(self.keystroke)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.formLayoutWidget)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.horizontalLayout_2.addWidget(self.buttonBox)
        self.formLayout.setLayout(3, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_2)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.keystrokesLabel.setText(_translate("Dialog", "Keystrokes", None))
        self.shortcutLabel.setText(_translate("Dialog", "Shortcut Name", None))
        self.runLabel.setText(_translate("Dialog", "Run Command", None))
        self.keystroke.setText(_translate("Dialog", "Keystroke...", None))

