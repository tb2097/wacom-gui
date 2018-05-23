#!/usr/bin/python
# -*- coding: utf-8 -*-

#

import sys
import os
import time
import threading
import subprocess
from os.path import expanduser
from PyQt4 import QtCore, QtGui

# internal widgets
from pressure import pressure
from options import otherOptions
from pad import Pad
from touch import touch
from help import Help


class WacomGui(QtGui.QWidget):
    def __init__(self):
        super(WacomGui, self).__init__()
        self.initUI()
        
    def initUI(self):
        # get tablet name/type
        self.pad           = Pad()
        self.stylusControl = pressure(self.pad.Tablet.deviceNames['stylus'], 'stylus')
        self.eraserControl = pressure(self.pad.Tablet.deviceNames['eraser'], 'eraser')
        self.cursorControl = pressure(self.pad.Tablet.deviceNames['cursor'], 'cursor')
        self.touch = touch(self.pad.Tablet.deviceNames['touch'])
        self.options = otherOptions(self.pad.Tablet.deviceNames)
        self.help = Help()
        self.setMaximumSize(1000, 500)
        self.setMinimumSize(1000, 500)
        self.setGeometry(300, 300, 1000, 500)
        self.setWindowTitle('Wacom GUI')

        # set stylus/eraser sensors up
        self.stylusControl.setSensor("stylus")
        self.eraserControl.setSensor("eraser")

        opPath = os.path.dirname(os.path.realpath(__file__)) 
        self.setWindowIcon(QtGui.QIcon(opPath + '/images/wacom-gui.svg')) 

        devices = os.popen("xsetwacom --list devices").readlines()
        self.Devices = QtGui.QListWidget(self)
        self.Devices.itemClicked.connect(self.itemSelectAction)
        self.options.setDevices(devices)
        for device in devices:
            device = device.split("\t")[0].strip().split(" ")
            if device[len(device)-1] != 'cursor':
                self.Devices.addItem(device[len(device)-1].title())
        self.Devices.addItem("Other Settings")
        self.Devices.addItem("Help")
        self.Devices.setMaximumWidth(128)

        self.tabletIcon = QtGui.QLabel(self)
        self.tabletIcon.setPixmap(self.pad.getIcon())
        self.buttonReset = QtGui.QPushButton("Restore Default Configuration")
        self.buttonReset.clicked.connect(self.restoreDefaults)

        # layout code
        # LEFT SIDE - This doens't ever go away
        self.vlayout1 = QtGui.QVBoxLayout()
        self.vlayout1.setAlignment(QtCore.Qt.AlignLeft)
        self.vlayout1.addWidget(self.tabletIcon)
        self.vlayout1.addWidget(QtGui.QLabel(self.pad.getTabletName()))
        self.vlayout1.addWidget(self.Devices)

        self.vlayout2 = QtGui.QVBoxLayout()
        self.vlayout2.setAlignment(QtCore.Qt.AlignLeft)
        self.vlayout2.addWidget(self.options)
        self.vlayout2.addWidget(self.stylusControl)
        self.vlayout2.addWidget(self.eraserControl)
        self.vlayout2.addWidget(self.cursorControl)
        self.vlayout2.addWidget(self.touch)
        self.vlayout2.addWidget(self.pad)
        self.vlayout2.addWidget(self.buttonReset)
        self.vlayout2.addWidget(self.help)


        self.vMaster = QtGui.QHBoxLayout()
        self.vMaster.addLayout(self.vlayout1)
        self.vMaster.addLayout(self.vlayout2)

        self.setLayout(self.vMaster)


        # hide everything that isn't needed for now
        self.options.hide()
        self.stylusControl.hide()
        self.eraserControl.hide()
        self.cursorControl.hide()
        self.pad.hide()
        self.touch.hide()
        self.buttonReset.hide()
        self.help.hide()


    def restoreDefaults(self):
        self.pad.resetButtons()
        self.stylusControl.resetDefaults()
        self.eraserControl.resetDefaults()
        self.cursorControl.resetDefaults()
        self.touch.resetDefaults()
        self.options.resetDefaults()
        self.help.hide()


    # for Device list => Pad, Stylus, etc
    def itemSelectAction(self, item):
        # print( item.text())
        if(item.text() == 'Pad'):
            self.options.hide()
            self.stylusControl.hide()
            self.eraserControl.hide()
            self.pad.show()
            self.touch.hide()
            self.buttonReset.hide()
            self.help.hide()

        elif(item.text() == 'Stylus'):
            self.options.hide()
            self.eraserControl.hide()
            self.pad.hide()
            self.touch.hide()
            self.buttonReset.hide()
            self.stylusControl.show()
            self.help.hide()
        
        elif(item.text() == 'Eraser'):
            self.options.hide()
            self.stylusControl.hide()
            self.pad.hide()
            self.touch.hide()
            self.buttonReset.hide()
            self.eraserControl.show()
            self.help.hide()

        elif(item.text() == 'Other Settings'):
            self.stylusControl.hide()
            self.eraserControl.hide()
            self.pad.hide()
            self.touch.hide()
            self.options.show()
            self.buttonReset.show()
            self.help.hide()

        elif(item.text() == "Touch"):
            self.stylusControl.hide()
            self.eraserControl.hide()
            self.pad.hide()
            self.touch.show()
            self.options.hide()
            self.buttonReset.hide()
            self.help.hide()

        elif(item.text() == "Help"):
            self.stylusControl.hide()
            self.eraserControl.hide()
            self.pad.hide()
            self.touch.hide()
            self.options.hide()
            self.buttonReset.hide()
            self.help.show()

        else:
            self.options.hide()
            self.stylusControl.hide()
            self.eraserControl.hide()
            self.pad.hide()
            self.touch.hide()
            self.buttonReset.hide()
            self.help.hide()

    def saveData(self):
        config = open(self.pad.Tablet.config, 'w')
        try:
            config.write("#!/bin/bash\n")
            buttons = self.pad.getCommands()
            for button in buttons:
                config.write(button + "\n")
            for screen in self.options.getScreenArea():
                config.write(screen + "\n")
            config.write(self.options.getFlip() + "\n")
            config.write(self.stylusControl.getSetCommand() + "\n")
            for stylus in self.stylusControl.getPenInfo():
                config.write(stylus + "\n")
            config.write(self.eraserControl.getSetCommand() + "\n")
            config.write(self.eraserControl.pen.penMode + "\n")
            if self.Devices.findItems("Touch", QtCore.Qt.MatchExactly):
                config.write(self.touch.getTouchEnable() + "\n")
        finally:
            config.close()
            os.chmod(self.pad.Tablet.config, 0774)

    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message',
                                           "Quit and write config file?",
                                           QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
            tmp = 1
        else:
            event.ignore()


def main():
    loadToggleShortcut()
    parseArgs(sys.argv)
    app = QtGui.QApplication(sys.argv)

    window = WacomGui()
    window.show()
    app.aboutToQuit.connect(window.saveData)
    app.exec_()
    #sys.exit(app.exec_())


def parseArgs(args):
    if len(args) > 1:
        for arg in args:
            if arg == "--help":
                help()
            elif arg == "--toggle":
                toggleScreens()
            elif arg == "--load":
                tablets = os.popen("lsusb | grep -i wacom").readlines()
                if len(tablets) == 0:
                    print "No tablet found"
                    exit(1)
                home = "%s/.wacom-gui" % expanduser("~")
                from wacom_data import tabletidentities
                TabletIds = tabletidentities()
                for tablet in tablets:
                    usbid = 'generic'
                    name = 'generic'
                    DevId = tablet.split(" ")[5].split(":")[1]
                    for item in TabletIds.Tablets:
                        if item.ProductId == int(DevId, 16):
                            usbid = DevId
                            name = item.Name
                            break
                    conf = "%s/%s/default.sh" % (home, usbid)
                    if os.path.exists(conf) and os.access(conf, os.X_OK):
                        os.system(conf)
                    else:
                        print "No default config for %s tablet." % name
        exit()

def toggleScreens():
    # get devices active
    devices = os.popen("xsetwacom --list devices").readlines()
    mod = []
    for idx, device in enumerate(devices):
        name = device.split('\t')[0].strip()
        if name.find('pad') == -1:
            cmd = "xsetwacom set \"%s\" MapToOutput next" % name
            subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)


def loadToggleShortcut():
    loadcheck = os.popen("dconf dump /org/mate/desktop/keybindings/ | grep 'wacom'").read()
    if loadcheck.__len__() == 0:
        os.popen("dconf load /org/mate/desktop/keybindings/ < /usr/local/wacom-gui/keybind.cfg")
    else:
        values = loadcheck.split('\n')
        if values[0].split('=')[1] != '/usr/local/bin/wacom-gui --toggle' or values[1].split('=')[1] != 'wacom toggle':
            os.popen(" dconf reset -f /org/mate/desktop/keybindings/custom0/")
            os.popen("dconf load /org/mate/desktop/keybindings/ < /usr/local/wacom-gui/keybind.cfg")
    keys = os.popen("setxkbmap -query | grep options").read()
    if keys.__len__() == 0:
        os.popen("setxkbmap -option 'altwin:hyper_win'")
    else:
        keys = keys[8:].strip().split(',')
        for idx, key in enumerate(keys):
            if key.find('altwin') != -1 and key.find('hyper_win') == -1:
                keys[idx] = "altwin:hyper_win"
        keys = ",".join(map(str,keys))
        os.popen("setxkbmap -option")
        os.popen("setxkbmap -option '" + keys + "'")


def help():
    print "Commands Guide"
    print "------------------------"
    print "--help\t\tPrint this message"
    print "--load\t\tLoad previous settings"
    print "\n\n\nButton Configuration Guide"
    print "------------------------"
    print "In the Pad section, click on the corresponding button you wish to configure.\n"
    print "Press key commands as you would normally then click on the button again to save command string.\n"
    print "Mouse clicks can be recorded as well by clicking anywhere in the open area in the config area."

if __name__ == '__main__':
    main()    
