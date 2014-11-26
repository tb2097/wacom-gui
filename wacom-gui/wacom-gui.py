#!/usr/bin/python
# -*- coding: utf-8 -*-

#code repo: linuxproc.rhythm.com/src/systems/git/wacom-gui.git

import sys
import os
from os.path import expanduser
from PyQt4 import QtCore,QtGui

#internal widgets
from pressure import pressure
from options import otherOptions
from pad import Pad


class WacomGui(QtGui.QWidget):
    def __init__(self):
        super(WacomGui, self).__init__()
        self.initUI()
        
    def initUI(self):
        #get tablet name/type
        self.pad           = Pad()
        self.stylusControl = pressure(self.pad.Tablet.Name)
        self.eraserControl = pressure(self.pad.Tablet.Name)
        self.cursorControl = pressure(self.pad.Tablet.Name)
        self.options       = otherOptions(self.pad.Tablet.Name)


        self.setMaximumSize(800,500)
        self.setGeometry(300, 300, 650, 450)
        self.setWindowTitle('Wacom GUI')

        #set stylus/eraser sensors up
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
            self.Devices.addItem(device[len(device)-1].title())
        self.Devices.addItem("Other Settings")
        self.Devices.setMaximumWidth(180)

        self.tabletIcon = QtGui.QLabel(self)
        self.tabletIcon.setPixmap(self.pad.getIcon())

        #layout code
        #LEFT SIDE - This doens't ever go away
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
        self.vlayout2.addWidget(self.pad)

        self.vMaster = QtGui.QHBoxLayout()
        self.vMaster.addLayout(self.vlayout1)
        self.vMaster.addLayout(self.vlayout2)

        self.setLayout(self.vMaster)


        #hide everything that isn't needed for now
        self.options.hide()
        self.stylusControl.hide()
        self.eraserControl.hide()
        self.cursorControl.hide()
        self.pad.hide()

    #for Device list => Pad, Stylus, etc
    def itemSelectAction(self,item):
        #print( item.text())
        if(item.text() == 'Pad'):
            self.options.hide()
            self.stylusControl.hide()
            self.eraserControl.hide()
            self.pad.show()

        elif(item.text() == 'Stylus'):
            self.options.hide()
            self.eraserControl.hide()
            self.pad.hide()
            self.stylusControl.show()
        
        elif(item.text() == 'Eraser'):
            self.options.hide()
            self.stylusControl.hide()
            self.pad.hide()
            self.eraserControl.show()

        elif(item.text() == 'Other Settings'):
            self.stylusControl.hide()
            self.eraserControl.hide()
            self.pad.hide()
            self.options.show()
        else:
            self.options.hide()
            self.stylusControl.hide()
            self.eraserControl.hide()
            self.pad.hide()

    def saveData(self):
        home = expanduser("~") + "/.wacom-gui.sh"
        config = open(home,'w')
        config.write("#!/bin/sh\n")
        buttons = self.pad.getCommands()
        for button in buttons:
            config.write(button + "\n")
        for screen in self.options.getScreenArea():
            config.write(screen + "\n")
        config.write(self.options.getFlip() + "\n")
        config.write(self.stylusControl.getSetCommand() + "\n")
        config.write(self.eraserControl.getSetCommand() + "\n")
        for pen in self.stylusControl.getPenInfo():
            config.write(pen + "\n")

        config.close()
        os.chmod(home,0774)

def main():

    parseArgs(sys.argv)
    app = QtGui.QApplication(sys.argv)

    window = WacomGui()
    window.show()
    app.aboutToQuit.connect(window.saveData)
    sys.exit(app.exec_())


def parseArgs(args):
    if len(args) > 1:
        for arg in args:
            if arg == "--help":
                help()
            elif arg == "--load":
                home = expanduser("~") + "/.wacom-gui.sh"
                if os.path.exists(home) and os.access(home, os.X_OK):
                    os.system(home)
                else:
                    print "No config to load"
        exit()

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
