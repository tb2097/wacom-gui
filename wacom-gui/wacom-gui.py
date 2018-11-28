#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import * 
from PyQt4.QtGui import *
import sys
import os
from os.path import expanduser
import json
import argparse
from wacom_data import Tablets
import wacom_menu
from pad import Pad, Touch
from stylus import Stylus

class WacomGui(QMainWindow, wacom_menu.Ui_MainWindow):
    buttonClicked = pyqtSignal(int)
    def __init__(self, parent=None):
        super(WacomGui, self).__init__(parent)
        self.setupUi(self)
        self.toggle = False
        self.cwd = os.path.dirname(os.path.abspath(__file__))
        self.setFocusPolicy(Qt.NoFocus)
        # button instances
        self.tabletButtons = ButtonGroup()
        self.toolButtons = ButtonGroup()
        self.configButtons = ButtonGroup()
        # button layouts
        self.tabletLayout = ButtonLayout()
        self.toolLayout = ButtonLayout()
        self.configLayout = ButtonLayout()
        self.tabletScroll.setWidget(self.tabletLayout.frame)
        self.toolScroll.setWidget(self.toolLayout.frame)
        self.configScroll.setWidget(self.configLayout.frame)
        # config files
        self.configs = {}
        # hold current device info
        self.dev = None
        self.dev_id = None
        self.config = None
        # load widgets
        self.pad = Pad()
        self.pad.hide()
        self.stylus = Stylus()
        self.stylus.hide()
        self.touch = Touch()
        self.touch.hide()
        # ui icon
        self.tabletRefresh.setIcon(QIcon(os.path.join(self.cwd, os.path.join(self.cwd, 'icons/ui/refresh.png'))))
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
        self.controlBox.setContentsMargins(0, 0, 0, 0)
        # add control widgets to control box
        hbox = QHBoxLayout()
        hbox.setAlignment(Qt.AlignHCenter)
        hbox.addWidget(self.pad)
        hbox.addWidget(self.stylus)
        hbox.addWidget(self.touch)
        self.controlBox.setLayout(hbox)
        # save config button
        self.saveConfig.clicked.connect(self.updateConfigs)
        # configure device reset button
        self.deviceDefaults.clicked.connect(self.deviceReset)
        # load first tool found
        self.toolSelect(self.toolButtons.btn_grp.checkedId())
        # init button functions
        self.tabletButtons.btn_grp.buttonClicked['int'].connect(self.tabletSelect)
        self.toolButtons.btn_grp.buttonClicked['int'].connect(self.toolSelect)
        self.configButtons.btn_grp.buttonClicked['int'].connect(self.configSelect)

    def initTabletButtons(self):
        for dev, data in self.tablet_data.tablets.items():
            for dev_id, tablet in enumerate(data):
                icon = os.path.join(self.cwd, "icons/devices/%spng" % tablet['svg'][:-3])
                if not os.path.isfile(os.path.join(os.getcwd(), icon)):
                    icon = os.path.join(self.cwd, 'icons/devices/generic.png')
                self.tabletLayout.addButton(self.tabletButtons.addButton(tablet['cname'], tablet['pad']['id'],
                                                                         str(dev), dev_id, icon))

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
        self.toolLayout.addButton(self.toolButtons.addButton("Functions", 0, 0, 0, os.path.join(self.cwd, 'icons/ui/functions.png'), 48, True))
        self.toolLayout.addButton(self.toolButtons.addButton("Stylus",  0, 0, 0, os.path.join(self.cwd, 'icons/ui/stylus.png'), 48, True))
        self.toolLayout.addButton(self.toolButtons.addButton("Touch",  0, 0, 0, os.path.join(self.cwd, 'icons/ui/touch.png'), 48, True))
        self.toolLayout.addButton(self.toolButtons.addButton("Mouse", 0, 0, 0, os.path.join(self.cwd, 'icons/ui/mouse.png'), 48, True))

    def setToolsAvail(self, idx):
        self.dev = self.tabletButtons.buttons[(idx, 1)]
        self.dev_id = self.tabletButtons.buttons[(idx, 3)]
        if 'pad' in self.tablet_data.tablets[self.dev][self.dev_id].keys():
            self.toolButtons.buttons[(0, 0)].setVisible(True)
            self.toolButtons.buttons[(0, 1)] = self.dev
            self.toolButtons.buttons[(0, 2)] = self.tablet_data.tablets[self.dev][self.dev_id]['pad']['id']
            self.toolButtons.buttons[(0, 3)] = self.dev_id
        else:
            self.toolButtons.buttons[(0, 0)].setVisible(False)
            self.toolButtons.buttons[(0, 1)] = 0
            self.toolButtons.buttons[(0, 2)] = 0
            self.toolButtons.buttons[(0, 3)] = 0
        if 'stylus' in self.tablet_data.tablets[self.dev][self.dev_id].keys():
            self.toolButtons.buttons[(1, 0)].setVisible(True)
            self.toolButtons.buttons[(1, 1)] = self.dev
            self.toolButtons.buttons[(1, 2)] = [self.tablet_data.tablets[self.dev][self.dev_id]['stylus']['id'],
                                                self.tablet_data.tablets[self.dev][self.dev_id]['eraser']['id']]
            self.toolButtons.buttons[(1, 3)] = self.dev_id
        else:
            self.toolButtons.buttons[(1, 0)].setVisible(False)
            self.toolButtons.buttons[(1, 1)] = 0
            self.toolButtons.buttons[(1, 2)] = 0
            self.toolButtons.buttons[(1, 3)] = 0
        if 'touch' in self.tablet_data.tablets[self.dev][self.dev_id].keys():
            self.toolButtons.buttons[(2, 0)].setVisible(True)
            self.toolButtons.buttons[(2, 1)] = self.dev
            self.toolButtons.buttons[(2, 2)] = self.tablet_data.tablets[self.dev][self.dev_id]['touch']['id']
            self.toolButtons.buttons[(2, 3)] = self.dev_id
        else:
            self.toolButtons.buttons[(2, 0)].setVisible(False)
            self.toolButtons.buttons[(2, 1)] = 0
            self.toolButtons.buttons[(2, 2)] = 0
            self.toolButtons.buttons[(2, 3)] = 0
        if 'cursor' in self.tablet_data.tablets[self.dev][self.dev_id].keys():
            self.toolButtons.buttons[(3, 0)].setVisible(True)
            self.toolButtons.buttons[(3, 1)] = self.dev
            self.toolButtons.buttons[(3, 2)] = self.tablet_data.tablets[self.dev][self.dev_id]['cursor']['id']
            self.toolButtons.buttons[(3, 3)] = self.dev_id
        else:
            self.toolButtons.buttons[(3, 0)].setVisible(False)
            self.toolButtons.buttons[(3, 1)] = 0
            self.toolButtons.buttons[(3, 2)] = 0
            self.toolButtons.buttons[(3, 3)] = 0

    def deviceReset(self):
        self.pad.set_default()
        self.stylus.resetPen()
        self.stylus.resetEraser()
        self.stylus.mapping.resetMapping()
        self.touch.reset()
        # TODO: add other resets

    def emptyConfig(self, dev, dev_id):
        config = {}
        for input in self.tablet_data.tablets[dev][dev_id].keys():
            if input in ['pad', 'stylus', 'eraser', 'touch', 'cursor']:
                config[input] = {}
                if input in ['pad', 'stylus', 'eraser']:
                    config[input]['buttons'] = {}
                    if input == 'pad':
                        buttons = self.tablet_data.tablets[dev][dev_id][input]['buttons']
                        for button in buttons.keys():
                            config['pad']['buttons'][button] = 'Default'
        return config

    def getConfigs(self, idx):
        self.configLayout.removeButtons()
        self.configButtons.removeButton()
        dev = self.tabletButtons.buttons[(idx, 1)]
        dev_id = self.tabletButtons.buttons[(idx, 3)]
        home = "%s/.wacom-gui" % expanduser("~")
        conf_path = os.path.join(home, dev)
        self.tablet_data.tablets[dev][dev_id]['conf_path'] = os.path.join(home, dev)
        if dev not in self.configs.keys():
            self.configs[dev] = {}
        if os.path.exists(conf_path):
            # get configs in path
            for config in os.listdir(conf_path):
                if os.path.isfile(os.path.join(conf_path, config)) and config.endswith(".json"):
                    with open(os.path.join(conf_path, config), 'r') as f:
                        self.configs[dev][os.path.splitext(config)[0]] = json.load(f)
            # TODO: allow user to sent alternate config to load by default
            # load default config, if it exists
            if 'default' not in self.configs[dev].keys():
                self.configs[dev]['default'] = self.emptyConfig(dev, dev_id)
            # get default config to load for given device, ie last selected config
            self.config = 'default'
            if os.path.exists("%s/device_default" % conf_path):
                with open("%s/device_default" % conf_path, 'r') as f:
                    device = json.load(f)
                # config file exists, use it
                if str(dev_id) in device.keys() and device[str(dev_id)] in self.configs[dev].keys():
                    self.config = device[str(dev_id)]
                # set defaults in tablet_data, if it's detected
                for idx in device.keys():
                    try:
                        self.tablet_data.tablets[self.dev][int(idx)]['config'] = device[idx]
                    except Exception as e:
                        pass
            self.configLayout.addButton(
                self.configButtons.addButton("default", 0, 0, 0, os.path.join(self.cwd, 'icons/ui/config.png'), 48))
            for config in sorted(self.configs[dev].keys()):
                if config != 'default':
                    self.configLayout.addButton(
                        self.configButtons.addButton(config, 0, 0, 0, os.path.join(self.cwd, 'icons/ui/config.png'), 48))
            # we are loading default config for now...
            self.loadConfig(dev, dev_id, self.config)
            for idx, button in enumerate(self.configButtons.btn_grp.buttons()):
                if button.text() == self.config:
                    self.configButtons.btn_grp.buttons()[idx].setChecked(True)
            # TODO: save the selected config somewhere...
            self.tablet_data.tablets[dev][dev_id]['config'] = self.config
        else:
            os.mkdir(self.tablet_data.tablets[dev][dev_id]['conf_path'])
            self.configLayout.addButton(
                self.configButtons.addButton("default", 0, 0, 0, os.path.join(self.cwd, 'icons/ui/config.png'), 48))

    def loadConfig(self, dev, dev_id, config):
        # TODO: load cursor configs
        # load pad buttons
        self.config = config
        self.tablet_data.tablets[dev][dev_id]['config'] = self.config
        if not self.toolButtons.buttons[(0, 0)].isHidden():
            self.pad.init_keys(self.tablet_data.tablets[dev][dev_id]['pad']['id'],
                               self.tablet_data.tablets[dev][dev_id]['svg'],
                               self.tablet_data.tablets[dev][dev_id]['pad']['buttons'],
                               self.configs[dev][config]['pad']['buttons'])
        if not self.toolButtons.buttons[(1, 0)].isHidden():
            self.stylus.init_pen(self.tablet_data.tablets[dev][dev_id]['stylus']['id'],
                                 self.configs[dev][config]['stylus'])
            self.stylus.init_eraser(self.tablet_data.tablets[dev][dev_id]['eraser']['id'],
                                 self.configs[dev][config]['eraser'])
            if self.tablet_data.tablets[dev][dev_id]['stylus']['rotate'] == False:
                # turn off rotate, if device doesn't support it
                if 'mapping' in self.configs[dev][config]['stylus']:
                    self.configs[dev][config]['stylus']['mapping']['rotate'] = 'False'
                else:
                    self.configs[dev][config]['stylus']['mapping'] = {'rotate': 'False'}
            self.stylus.mapping.initUI(self.tablet_data.tablets[dev][dev_id]['stylus']['id'],
                                       self.tablet_data.tablets[dev][dev_id]['eraser']['id'],
                                       self.configs[dev][config]['stylus'])
        if not self.toolButtons.buttons[(2, 0)].isHidden():
            self.touch.init(self.tablet_data.tablets[dev][dev_id]['touch']['id'],
                            self.configs[dev][config]['touch'])

    def tabletSelect(self, idx):
        self.updateConfigs()
        self.setToolsAvail(idx)
        self.getConfigs(idx)
        # set first available tool as selected
        if not self.toolButtons.buttons[(0, 0)].isHidden():
            self.toolButtons.buttons[(0, 0)].setChecked(True)
        elif not self.toolButtons.buttons[(1, 0)].isHidden():
            self.toolButtons.buttons[(1, 0)].setChecked(True)
        elif not self.toolButtons.buttons[(2, 0)].isHidden():
            self.toolButtons.buttons[(2, 0)].setChecked(True)
        elif not self.toolButtons.buttons[(3, 0)].isHidden():
            self.toolButtons.buttons[(3, 0)].setChecked(True)

    def toolSelect(self, idx):
        if idx == 0 and not self.toolButtons.buttons[(idx, 0)].isHidden():
            # remove previous layout
            self.pad.show()
            self.stylus.hide()
            self.touch.hide()
        # stylus menu
        elif idx == 1 and not self.toolButtons.buttons[(idx, 0)].isHidden():
            # remove previous layout
            self.pad.hide()
            self.stylus.show()
            self.touch.hide()
        # touch menu
        elif idx == 2 and not self.toolButtons.buttons[(idx, 0)].isHidden():
            # remove previous layout
            self.pad.hide()
            self.stylus.hide()
            self.touch.show()
        # cursor menu
        elif idx == 3 and not self.toolButtons.buttons[(idx, 0)].isHidden():
            # remove previous layout
            self.pad.hide()
            self.stylus.hide()
            self.touch.hide()

    def configSelect(self, idx):
        config = str(self.configButtons.buttons[(idx, 0)].text())
        self.loadConfig(self.dev, self.dev_id, config)

    def deleteItemsOfLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    self.deleteItemsOfLayout(item.layout())

    def boxdelete(self, box):
        for i in range(self.keys.count()):
            layout_item = self.keys.itemAt(i)
            if layout_item.layout() == box:
                self.deleteItemsOfLayout(layout_item.layout())
                self.vlayout.removeItem(layout_item)
                break

    def updateConfigs(self):
        write = False
        if not self.toolButtons.buttons[(0, 0)].isHidden():
            pad = self.pad.get_config()
            if pad != self.configs[self.dev][self.config]['pad']['buttons']:
                write = True
                self.configs[self.dev][self.config]['pad']['buttons'] = pad
        if not self.toolButtons.buttons[(1, 0)].isHidden():
            stylus = self.stylus.get_config()
            # if stylus['stylus'] != self.configs[self.dev][self.config]['stylus']:
            write = True
            self.configs[self.dev][self.config]['stylus'] = stylus['stylus']
            # if stylus['eraser'] != self.configs[self.dev][self.config]['eraser']:
            write = True
            self.configs[self.dev][self.config]['eraser'] = stylus['eraser']
        if not self.toolButtons.buttons[(2, 0)].isHidden():
            touch = self.touch.get_config()
            if touch != self.configs[self.dev][self.config]['touch']:
                write = True
                self.configs[self.dev][self.config]['touch'] = touch
        # TODO: cursor
        if not self.toolButtons.buttons[(3, 0)].isHidden():
            tmp = 1
        if write:
            reply = None
            if self.toggle is False:
                reply = QMessageBox.question(self, 'Save Config',
                                                   "Write \"%s\" config file?" % self.config,
                                             QMessageBox.Yes, QMessageBox.No)
            # update config if toggle is set or save is called
            if self.toggle or reply == QMessageBox.Yes:
                home = "%s/.wacom-gui" % expanduser("~")
                conf_path = os.path.join(home, self.dev)
                conf_file = os.path.join(conf_path, "%s.json" % self.config)
                if not os.path.exists(conf_path):
                    os.mkdir(conf_path)
                elif os.path.exists(conf_file):
                    os.rename(conf_file, "%s.bak" % conf_file)
                with open(conf_file, 'w') as outfile:
                    json.dump(self.configs[self.dev][self.config], outfile, sort_keys=True,
                              indent=4, separators=(',', ': '))
                if os.path.exists(conf_file):
                    if os.path.exists("%s.bak" % conf_file):
                        os.remove("%s.bak" % conf_file)
        # check if we need to update what config is loaded
        default = {}
        if self.dev is not None:
            for idx, tablet in enumerate(self.tablet_data.tablets[self.dev]):
                if 'config' in tablet.keys():
                    default[idx] = tablet['config']
                else:
                    default[idx] = 'default'
            conf_path = os.path.join("%s/.wacom-gui" % expanduser("~"), self.dev)
            conf_file = os.path.join(conf_path, 'device_default')
            with open(conf_file, 'w') as outfile:
                json.dump(default, outfile, sort_keys=True,
                          indent=4, separators=(',', ': '))

    def quickLoad(self):
        for idx, button in enumerate(self.tabletButtons.btn_grp.buttons()):
            self.tabletSelect(idx)
        sys.exit()

    def toggleDisplay(self):
        self.toggle = True
        for idx, button in enumerate(self.tabletButtons.btn_grp.buttons()):
            self.tabletSelect(idx)
            if self.pad.is_toggle():
                self.stylus.mapping.toggle_next()
                self.updateConfigs()
        sys.exit()

    def closeEvent(self, event):
        self.updateConfigs()
        event.accept()
        self.deleteLater()


class ButtonLayout:
    def __init__(self):
        self.layout = QHBoxLayout()
        self.layout.setAlignment(Qt.AlignLeft)
        self.frame = QFrame()
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

class ButtonGroup(QObject):
    buttonClicked = pyqtSignal(int)

    def __init__(self):
        super(ButtonGroup, self).__init__()
        self.initUI()

    def initUI(self):
        self.buttonMapper = QSignalMapper(self)
        self.buttons = {}
        self.btn_grp = QButtonGroup()
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
        self.buttons[(idx, 0)] = QToolButton()
        self.btn_grp.addButton(self.buttons[(idx, 0)], idx)
        self.buttons[(idx, 1)] = dev
        self.buttons[(idx, 2)] = wid
        self.buttons[(idx, 3)] = dev_id
        self.buttons[(idx, 0)].clicked[()].connect(self.buttonMapper.map)
        if label.split("Wacom ").__len__() == 2:
            self.buttons[(idx, 0)].setText(QString(label[6:]))
        else:
            self.buttons[(idx, 0)].setText(QString(label))
        if icon is not None:
            self.buttons[(idx, 0)].setIcon(QIcon(icon))
            self.buttons[(idx, 0)].setIconSize(QSize(isize, isize))
            self.buttons[(idx, 0)].setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.buttons[(idx, 0)].setMinimumSize(QSize(80, 70))
        self.buttons[(idx, 0)].setMaximumSize(QSize(120, 90))
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


def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--load", help="load configuration for device", action="store_true")
    parser.add_argument("--toggle", help="toggle display if hotkey is defined for device", action="store_true")
    return parser.parse_args()


def main():
    app = QApplication(sys.argv)
    form = WacomGui()
    opts = parseArgs()
    if opts.load:
        form.quickLoad()
    if opts.toggle:
        form.toggleDisplay()
    form.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()


# pyuic4 wacom_menu.ui -o wacom_menu.py
#touch icons: <div>Icons made by <a href="https://www.flaticon.com/authors/mobiletuxedo" title="Mobiletuxedo">Mobiletuxedo</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a> is licensed by <a href="http://creativecommons.org/licenses/by/3.0/" title="Creative Commons BY 3.0" target="_blank">CC 3.0 BY</a></div>