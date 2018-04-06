#!/usr/bin/python
# -*- coding: utf-8 -*-

# code repo: linuxproc.rhythm.com/src/systems/git/wacom-gui.git

import sys
import os
import re
from os.path import expanduser
from PyQt4 import QtCore, QtGui

# internal widgets
from pressure import pressure
from options import otherOptions
from pad import Pad
from touch import touch


class WacomGui(QtGui.QWidget):
    def __init__(self):
        super(WacomGui, self).__init__()
        self.initUI()
        
    def initUI(self):
        # get tablet name/type
        self.pad           = Pad()
        self.stylusControl = pressure(self.pad.Tablet.Name, 'stylus')
        self.eraserControl = pressure(self.pad.Tablet.Name, 'eraser')
        self.cursorControl = pressure(self.pad.Tablet.Name, 'cursor')
        self.touch         = touch(self.pad.Tablet.Name)
        self.options       = otherOptions(self.pad.Tablet.Name)


        self.setMaximumSize(800,500)
        self.setGeometry(300, 300, 650, 450)
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
        self.Devices.setMaximumWidth(180)

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


    def restoreDefaults(self):
        self.pad.resetButtons()
        self.stylusControl.resetDefaults()
        self.eraserControl.resetDefaults()
        self.cursorControl.resetDefaults()
        self.touch.resetDefaults()
        self.options.resetDefaults()


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

        elif(item.text() == 'Stylus'):
            self.options.hide()
            self.eraserControl.hide()
            self.pad.hide()
            self.touch.hide()
            self.buttonReset.hide()
            self.stylusControl.show()
        
        elif(item.text() == 'Eraser'):
            self.options.hide()
            self.stylusControl.hide()
            self.pad.hide()
            self.touch.hide()
            self.buttonReset.hide()
            self.eraserControl.show()

        elif(item.text() == 'Other Settings'):
            self.stylusControl.hide()
            self.eraserControl.hide()
            self.pad.hide()
            self.touch.hide()
            self.options.show()
            self.buttonReset.show()
        elif(item.text() == "Touch"):
            self.stylusControl.hide()
            self.eraserControl.hide()
            self.pad.hide()
            self.touch.show()
            self.options.hide()
            self.buttonReset.hide()
        else:
            self.options.hide()
            self.stylusControl.hide()
            self.eraserControl.hide()
            self.pad.hide()
            self.touch.hide()
            self.buttonReset.hide()

    def saveData(self):
        home = expanduser("~") + "/.wacom-gui.sh"
        config = open(home, 'w')
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
            os.chmod(home, 0774)

def main():
    loadToggleShortcut()
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
            elif arg == "--toggle":
                toggleScreens()
            elif arg == "--load":
                home = expanduser("~") + "/.wacom-gui.sh"
                if os.path.exists(home) and os.access(home, os.X_OK):
                    os.system(home)
                else:
                    print "No config to load"
        exit()

def toggleScreens():
    # get devices active
    devices = os.popen("xsetwacom --list devices").readlines()
    mod = []
    for idx, device in enumerate(devices):
        tmp = device.split('\t')[0].strip()
        if tmp.find('pad') == -1:
            mod.append(tmp)
    # assume all are set to same area
    coords = getTabletArea(mod[0])
    for obj in mod:
        os.popen("xinput set-prop \"" + obj + "\" --type=float \"Coordinate Transformation Matrix\" " + coords)
    tmp = 1


def getTabletArea(*args):
    # get current tablet area
    tabletInfo = os.popen("xinput list-props \"" + args[0] + "\" | grep Coordinate").readlines()
    tabletInfo[0] = tabletInfo[0][41:].rstrip('\n')
    tabletInfo[0] = re.sub(",", "", tabletInfo[0])
    tabletScreenCoords = {}
    blarg = tabletInfo[0].split()
    swap = False
    count = 0
    tabletActiveArea = ''
    for i in range(0, 3):
        for j in range(0, 3):
            tabletScreenCoords[(i, j)] = blarg[count]
            tabletActiveArea = tabletActiveArea + " " + blarg[count]
            count += 1

    # check if "full screen"
    fullScreen = True
    for i in range(0, 3):
        for j in range(0, 3):
            if i == j and float(tabletScreenCoords[(i, j)]) != 1.0:
                fullScreen = False
                break
            elif i != j and float(tabletScreenCoords[(i, j)]) != 0.0:
                fullScreen = False
                break
    if fullScreen:
        swap = True
    # get screen dimensions/coords
    info = os.popen("xrandr | grep ' connected'").read().strip().split('\n')
    screens = []
    for screen in info:
        screen = screen.split('(')[0].strip().rsplit(' ', 1)
        screen[1] = screen[1].replace('x', '+')
        screen[1] = screen[1].split('+')
        screen[1].insert(3, screen[1].pop(0))
        screen[1].insert(3, screen[1].pop(0))
        if screen[0].find('primary') == -1:
            screens.append(screen[1])
        else:
            screens.insert(0, screen[1])
    totalResolution = os.popen("xdpyinfo | grep dimensions | awk '{print $2}' | awk -Fx '{print $1, $2}'").read()
    totalResolution = totalResolution.split()

    display = [[0 for x in xrange(3)] for x in xrange(3)]
    display[2][2] = 1.0

    display[0][0] = float(screens[0][2]) / float(totalResolution[0])
    # percent of screen height
    display[1][1] = float(screens[0][3]) / float(totalResolution[1])
    # offset in x
    if float(screens[0][0]) != 0:
        display[0][2] = float(screens[0][0]) / float(totalResolution[0])
    # offset in y
    if float(screens[0][1]) != 0:
        display[1][2] = float(screens[0][1]) / float(totalResolution[1])
    if swap == True:
        coords = []
        for item in display:
            coords.extend(item)
        return " ".join(format(x, "1.6f") for x in coords)
    isLeft = True
    for i in range(0, 3):
        for j in range(0, 3):
            if round(float(tabletScreenCoords[(i, j)]), 6) != round(float(display[i][j]), 6):
                isLeft = False
                break
    if isLeft:
        swap = True
    display[0][0] = float(screens[1][2]) / float(totalResolution[0])
    # percent of screen height
    display[1][1] = float(screens[1][3]) / float(totalResolution[1])
    # offset in x
    if float(screens[1][0]) != 0:
        display[0][2] = float(screens[1][0]) / float(totalResolution[0])
    # offset in y
    if float(screens[1][1]) != 0:
        display[1][2] = float(screens[1][1]) / float(totalResolution[1])
    if swap == True:
        coords = []
        for item in display:
            coords.extend(item)
        return " ".join(format(x, "1.6f") for x in coords)
    else:
        return "1.000000 0.000000 0.000000 0.000000 1.000000 0.000000 0.000000 0.000000 1.000000"

def loadToggleShortcut():
    loadcheck = os.popen("dconf dump /org/mate/desktop/keybindings/ | grep 'wacom toggle'").read()
    if loadcheck.__len__() == 0:
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

    # I'm lazy and don't want to make a new function... makes sure configs are sourced in .bashrc
    if os.path.isfile(os.path.expanduser('~') + "/.wacom-gui.sh"):
        bash = os.popen("cat " + os.path.expanduser('~') + "/.bashrc | grep wacom-gui.sh").read()
        if bash.__len__() == 0:
            os.popen("echo \"source ~/.wacom-gui.sh\" >>" + os.path.expanduser('~') + "/.bashrc")


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
