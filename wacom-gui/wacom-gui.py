#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt
import sys
import os
from os.path import expanduser
import subprocess
from wacom_data import Tablets
import wacom_menu
import copy

class WacomGui(QtGui.QMainWindow, wacom_menu.Ui_MainWindow):
    buttonClicked = QtCore.pyqtSignal(int)
    def __init__(self, parent=None):
        super(WacomGui, self).__init__(parent)
        self.setupUi(self)
        # button instances
        self.tabletButtons = ButtonGroup()
        self.toolButtons = ButtonGroup()
        self.configButtons = ButtonGroup()
        # init button functions
        self.tabletButtons.btn_grp.buttonClicked['int'].connect(self.tabletSelect)
        # button layouts
        self.tabletLayout = ButtonLayout()
        self.toolLayout = ButtonLayout()
        self.configLayout = ButtonLayout()
        self.tabletScroll.setWidget(self.tabletLayout.frame)
        self.toolScroll.setWidget(self.toolLayout.frame)
        self.configScroll.setWidget(self.configLayout.frame)
        # ui icon
        self.tabletRefresh.setIcon(QtGui.QIcon('icons/ui/refresh.png'))
        # get connected tablet info
        self.tablet_data = Tablets()
        # attach function to refresh tablets
        self.tabletRefresh.clicked.connect(self.refreshTablets)
        # add buttons for connected tablets
        self.initTabletButtons()
        # generate tool buttons
        self.initToolButtons()
        # refresh tablet list, set tools, configs
        self.refreshTablets()

    def initTabletButtons(self):
        for dev, data in self.tablet_data.tablets.items():
            for dev_id, tablet in enumerate(data):
                icon = "icons/devices/%spng" % tablet['svg'][:-3]
                if not os.path.isfile(os.path.join(os.getcwd(), icon)):
                    icon = 'icons/devices/generic.png'
                self.tabletLayout.addButton(self.tabletButtons.addButton(tablet['cname'], tablet['pad']['id'],
                                                                         str(dev), dev_id, icon))
        tmp = 1

    def refreshTablets(self):
        self.tablet_data.get_connected_tablets()
        # clear current tablets from layout
        self.tabletLayout.removeButtons()
        self.tabletButtons.removeButton()
        self.initTabletButtons()
        if self.tabletButtons.buttons.items().__len__() == 0:
            self.toolButtons.hideButtons()
        else:
            self.tabletSelect(0)

    def initToolButtons(self):
        # Functions/Stylus/Touch/Cursor
        self.toolLayout.addButton(self.toolButtons.addButton("Functions", 0, 0, 0, 'icons/ui/functions.png', 48, True))
        self.toolLayout.addButton(self.toolButtons.addButton("Stylus",  0, 0, 0, 'icons/ui/stylus.png', 48, True))
        self.toolLayout.addButton(self.toolButtons.addButton("Touch",  0, 0, 0, 'icons/ui/touch.png', 48, True))
        self.toolLayout.addButton(self.toolButtons.addButton("Mouse", 0, 0, 0, 'icons/ui/mouse.png', 48, True))

    def setToolsAvail(self, idx):
        dev = self.tabletButtons.buttons[(idx, 1)]
        dev_id = self.tabletButtons.buttons[(idx, 3)]
        if 'pad' in self.tablet_data.tablets[dev][dev_id].keys():
            self.toolButtons.buttons[(0, 0)].setVisible(True)
            self.toolButtons.buttons[(0, 1)] = dev
            self.toolButtons.buttons[(0, 2)] = self.tablet_data.tablets[dev][dev_id]['pad']['id']
            self.toolButtons.buttons[(0, 3)] = dev_id
        else:
            self.toolButtons.buttons[(0, 0)].setVisible(False)
            self.toolButtons.buttons[(0, 1)] = 0
            self.toolButtons.buttons[(0, 2)] = 0
            self.toolButtons.buttons[(0, 3)] = 0
        if 'stylus' in self.tablet_data.tablets[dev][dev_id].keys():
            self.toolButtons.buttons[(1, 0)].setVisible(True)
            self.toolButtons.buttons[(1, 1)] = dev
            self.toolButtons.buttons[(1, 2)] = self.tablet_data.tablets[dev][dev_id]['stylus']['id']
            self.toolButtons.buttons[(1, 3)] = dev_id
        else:
            self.toolButtons.buttons[(1, 0)].setVisible(False)
            self.toolButtons.buttons[(1, 1)] = 0
            self.toolButtons.buttons[(1, 2)] = 0
            self.toolButtons.buttons[(1, 3)] = 0
        if 'touch' in self.tablet_data.tablets[dev][dev_id].keys():
            self.toolButtons.buttons[(2, 0)].setVisible(True)
            self.toolButtons.buttons[(2, 1)] = dev
            self.toolButtons.buttons[(2, 2)] = self.tablet_data.tablets[dev][dev_id]['touch']['id']
            self.toolButtons.buttons[(2, 3)] = dev_id
        else:
            self.toolButtons.buttons[(2, 0)].setVisible(False)
            self.toolButtons.buttons[(2, 1)] = 0
            self.toolButtons.buttons[(2, 2)] = 0
            self.toolButtons.buttons[(2, 3)] = 0
        if 'cursor' in self.tablet_data.tablets[dev][dev_id].keys():
            self.toolButtons.buttons[(3, 0)].setVisible(True)
            self.toolButtons.buttons[(3, 1)] = dev
            self.toolButtons.buttons[(3, 2)] = self.tablet_data.tablets[dev][dev_id]['cursor']['id']
            self.toolButtons.buttons[(3, 3)] = dev_id
        else:
            self.toolButtons.buttons[(3, 0)].setVisible(False)
            self.toolButtons.buttons[(3, 1)] = 0
            self.toolButtons.buttons[(3, 2)] = 0
            self.toolButtons.buttons[(3, 3)] = 0

    def getConfigs(self, idx):
        # get dev id
        self.configLayout.removeButtons()
        self.configButtons.removeButton()
        dev = self.tabletButtons.buttons[(idx, 1)]
        dev_id = self.tabletButtons.buttons[(idx, 3)]
        home = "%s/.wacom-gui" % expanduser("~")
        conf_path = os.path.join(home, dev)
        self.tablet_data.tablets[dev][dev_id]['conf_path'] = os.path.join(home, dev)
        if os.path.exists(conf_path):
            # get configs in path
            configs = []
            for config in os.listdir(conf_path):
                if os.path.isfile(os.path.join(conf_path, config)) and config.endswith(".sh"):
                    configs.append(config[:-3])
            if 'default' in configs:
                # we are loading default config for now...
                self.loadConfig(dev, dev_id, "default")
            self.configLayout.addButton(
                self.configButtons.addButton("default", 0, 0, 0, 'icons/ui/config.png', 48))
            for config in sorted(configs):
                if config != 'default':
                    self.configLayout.addButton(
                        self.configButtons.addButton(config, 0, 0, 0, 'icons/ui/config.png', 48))
        else:
            os.mkdir(self.tablet_data.tablets[dev][dev_id]['conf_path'])
            self.configLayout.addButton(
                self.configButtons.addButton("default", 0, 0, 0, 'icons/ui/config.png', 48))

    def loadConfig(self, dev, dev_id, config):
        conf_path = self.tablet_data.tablets[dev][dev_id]['conf_path']
        if os.access(os.path.join(conf_path, "default.sh"), os.X_OK):
            # get device ids
            ids = {'pad': 0, 'stylus': 0, 'eraser': 0, 'touch': 0, 'cursor': 0}
            for dev_input in self.tablet_data.tablets[dev][dev_id].keys():
                if dev_input in ids.keys():
                    ids[dev_input] = int(self.tablet_data.tablets[dev][dev_id][dev_input]['id'])
            tmp = 1
            #p = subprocess.Popen("%s.sh %d %d %d %d %d" %
            #                     (os.path.join(conf_path, 'default'),),
            #                     shell=True, stdout=subprocess.PIPE)
            #p.wait()
            # os.system(os.path.join(conf_path, "default.sh"))

    def tabletSelect(self, idx):
        self.setToolsAvail(idx)
        self.getConfigs(idx)
        self.toolButtons.buttons[(0, 0)].setChecked(True)
        tmp = 1

class ButtonLayout():
    def __init__(self):
        self.layout = QtGui.QHBoxLayout()
        self.layout.setAlignment(Qt.AlignLeft)
        self.frame = QtGui.QFrame()
        self.frame.setLayout(self.layout)

    def addButton(self, button):
        self.layout.addWidget(button)

    def removeButtons(self):
        for i in reversed(range(self.layout.count())):
            widgetToRemove = self.layout.itemAt(i).widget()
            # remove it from the layout list
            self.layout.removeWidget(widgetToRemove)
            # remove it from the gui
            widgetToRemove.setParent(None)
        tmp = 1

class ButtonGroup(QtCore.QObject):
    buttonClicked = QtCore.pyqtSignal(int)

    def __init__(self):
        super(ButtonGroup, self).__init__()
        self.initUI()

    def initUI(self):
        self.buttonMapper = QtCore.QSignalMapper(self)
        self.buttons = {}
        self.btn_grp = QtGui.QButtonGroup()
        self.btn_style = ("QToolButton {\n"
            "   background-color: rgb(220, 220, 220);\n"
            "   border-radius: 4px;\n"
            "}\n"
            "QToolButton:checked{\n"
            "   background-color: rgb(109, 215, 232);\n"
            "   border-style: outset;\n"
            "   border-width: 1px;\n"
            "   border-color: rgb(40, 40, 40);\n"
            "}\n")

    def addButton(self, label, wid=0, dev=0, dev_id=0, icon=None, isize=48, hide=False):
        select = False
        idx = self.buttons.__len__() / 4
        self.buttons[(idx, 0)] = QtGui.QToolButton()
        self.btn_grp.addButton(self.buttons[(idx, 0)], idx)
        self.buttons[(idx, 1)] = dev
        self.buttons[(idx, 2)] = wid
        self.buttons[(idx, 3)] = dev_id
        self.buttons[(idx, 0)].clicked[()].connect(self.buttonMapper.map)
        if label.split("Wacom ").__len__() == 2:
            self.buttons[(idx, 0)].setText(QtCore.QString(label[6:]))
        else:
            self.buttons[(idx, 0)].setText(QtCore.QString(label))
        if icon is not None:
            self.buttons[(idx, 0)].setIcon(QtGui.QIcon(icon))
            self.buttons[(idx, 0)].setIconSize(QtCore.QSize(isize, isize))
            self.buttons[(idx, 0)].setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.buttons[(idx, 0)].setMinimumSize(QtCore.QSize(80, 70))
        self.buttons[(idx, 0)].setMaximumSize(QtCore.QSize(120, 90))
        self.buttonMapper.setMapping(self.buttons[(idx, 0)], idx)
        self.buttons[(idx, 0)].setCheckable(True)
        self.buttons[(idx, 0)].setStyleSheet(self.btn_style)
        # set first button as selected
        if idx == 0:
            self.buttons[(idx, 0)].setChecked(True)
        if hide:
            self.buttons[(idx, 0)].setVisible(False)
        return self.buttons[(idx, 0)]

    def removeButton(self, idx=None):
        # remove all buttons from button group if no index provided
        if idx is None:
            for idx in self.buttons:
                if idx[1] == 0:
                    self.btn_grp.removeButton(self.buttons[idx])
            self.buttons.clear()
        else:
            self.btn_grp.removeButton(self.buttons[(idx, 0)])
            del self.buttons[(idx, 0)]
            del self.buttons[(idx, 1)]
            del self.buttons[(idx, 2)]
            del self.buttons[(idx, 3)]

    def hideButtons(self):
        for idx in self.buttons:
            if idx[1] == 0:
                self.buttons[idx].setVisible(False)

def main():
    app = QtGui.QApplication(sys.argv)
    form = WacomGui()
    form.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()


# pyuic4 wacom_menu.ui -o wacom_menu.py
#touch icons: <div>Icons made by <a href="https://www.flaticon.com/authors/mobiletuxedo" title="Mobiletuxedo">Mobiletuxedo</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a> is licensed by <a href="http://creativecommons.org/licenses/by/3.0/" title="Creative Commons BY 3.0" target="_blank">CC 3.0 BY</a></div>