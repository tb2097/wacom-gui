#!/usr/bin/python

from PyQt4 import QtCore, QtGui
import sys
import os
import re


class otherOptions(QtGui.QWidget):
    def __init__(self, deviceNames, parent=None):
        QtGui.QWidget.__init__(self, parent)
        #self.tabletName = tabletName.replace('Pad', 'Pen')
        # use the detected device names
        self.tabletStylus = deviceNames['stylus']
        self.tabletEraser = deviceNames['eraser']
        self.tabletCursor = deviceNames['cursor']
        self.tabletTouch = deviceNames['touch']
        self.tabletPad = deviceNames['pad']
        self.deviceNames = deviceNames
        self.initUI()


    def initUI(self):
        self.devices = []
        self.tabletActiveArea = ""
        self.orient = ''
        # layout code
        self.mainLayout = QtGui.QHBoxLayout()
        self.mainLayout.setAlignment(QtCore.Qt.AlignLeft)
        screens = self.screenOptions()
        if screens:
            self.mainLayout.addWidget(screens)
            self.getTabletArea()
        self.mainLayout.addWidget(self.flipOptions())
        self.setLayout(self.mainLayout)


    def screenOptions(self):
        if QtGui.QDesktopWidget().numScreens() == 1:
            self.screenFull = None
            return None
        groupBox = QtGui.QGroupBox("Screen Area")
        groupBox.setAlignment(QtCore.Qt.AlignHCenter)
        groupBox.setFixedHeight(120)
        self.screenGroup = QtGui.QButtonGroup(groupBox)
        self.displays = []
        for x in range(0, QtGui.QDesktopWidget().numScreens()):
            self.displays.append(QtGui.QRadioButton("Monitor %d" % x))
        self.screenFull = QtGui.QRadioButton("All Monitors")
        for screen in self.displays:
            self.screenGroup.addButton(screen)
        self.screenGroup.addButton(self.screenFull)
        screenLayout = QtGui.QVBoxLayout()
        for screen in self.displays:
            screenLayout.addWidget(screen)
        screenLayout.addWidget(self.screenFull)
        screenLayout.addStretch(1)
        self.screenGroup.buttonClicked.connect(self.screenChange)
        groupBox.setLayout(screenLayout)
        return groupBox


    def flipOptions(self):
        groupBox = QtGui.QGroupBox("Tablet Orientation")
        groupBox.setAlignment(QtCore.Qt.AlignHCenter)
        groupBox.setFixedHeight(120)
        self.tabletFlipGroup = QtGui.QButtonGroup(groupBox)
        self.tabletRight = QtGui.QRadioButton("Right-Handed")
        self.tabletLeft = QtGui.QRadioButton("Left-Handed")
        self.tabletFlipGroup.addButton(self.tabletRight)
        self.tabletFlipGroup.addButton(self.tabletLeft)
        flipLayout = QtGui.QVBoxLayout()
        flipLayout.addWidget(self.tabletRight)
        flipLayout.addWidget(self.tabletLeft)
        flipLayout.addStretch(1)
        getCommand = os.popen("xsetwacom --get \"%s stylus\" Rotate" % self.tabletStylus).readlines()
        # check correct button for orientation
        if getCommand[0] == "none\n":
            self.orient = "xsetwacom --set \"%s stylus\" Rotate none" % self.tabletStylus
            self.orient += "\nxsetwacom --set \"%s eraser\" Rotate none" % self.tabletEraser
            self.tabletRight.setChecked(1)
        elif getCommand[0] == "half\n":
            self.orient = "xsetwacom --set \"%s stylus\" Rotate half" % self.tabletStylus
            self.orient += "\nxsetwacom --set \"%s eraser\" Rotate half" % self.tabletEraser
            self.tabletLeft.setChecked(1)
        self.tabletFlipGroup.buttonClicked.connect(self.tabletFlipChange)
        groupBox.setLayout(flipLayout)
        return groupBox


    def tabletFlipChange(self, buttonId):
        if buttonId.text() == "Right-Handed":
            self.orient = "xsetwacom --set \"%s stylus\" Rotate none" % self.deviceNames['stylus']
            self.orient += "\nxsetwacom --set \"%s eraser\" Rotate none" % self.deviceNames['eraser']
        elif buttonId.text() == "Left-Handed":
            self.orient = "xsetwacom --set \"%s stylus\" Rotate half" % self.deviceNames['stylus']
            self.orient += "\nxsetwacom --set \"%s eraser\" Rotate half" % self.deviceNames['eraser']
        flipTablet = os.popen(self.orient)


    def screenChange(self, buttonId):
        if buttonId.text() == "All Monitors":
            self.tabletActiveArea = "1 0 0 0 1 0 0 0 1"
            for device in self.devices:
                if device != "pad":
                    cmd = "xinput set-prop \"%s %s\" --type=float \"Coordinate Transformation Matrix\" %s" \
                          % (self.deviceNames[device], device, self.tabletActiveArea)
                    setCommand = os.popen(cmd)
        else:
            self.tabletActiveArea = "HEAD-%s" % buttonId.text().split(' ')[1]
            for device in self.devices:
                if device != "pad":
                    cmd = "xsetwacom set \"%s %s\" MapToOutput %s" % (self.deviceNames[device], device, self.tabletActiveArea)
                    setCommand = os.popen(cmd)


    def getTabletArea(self):
        # get current tablet area
        tabletInfo = os.popen("xinput list-props \"%s stylus\" | grep Coordinate" % self.tabletStylus).readlines()
        tabletInfo[0] = tabletInfo[0][41:].rstrip('\n')
        tabletInfo[0] = re.sub(",", "", tabletInfo[0])
        tabletScreenCoords = {}
        blarg = tabletInfo[0].split()
        count = 0
        for i in range(0, 3):
            for j in range(0, 3):
                tabletScreenCoords[(i, j)] = blarg[count]
                self.tabletActiveArea = self.tabletActiveArea + " " + blarg[count]
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
            self.screenFull.setChecked(1)
        # have to build array then compare... boo
        else:
            for id in range(0, QtGui.QDesktopWidget().numScreens()):
                screen = QtGui.QDesktopWidget().screenGeometry(id)
                cmd = "xdpyinfo | grep dimensions | awk '{print $2}' | awk -Fx '{print $1, $2}'"
                totalResolution = os.popen(cmd).read()
                totalResolution = totalResolution.split()
                display = [[0 for x in xrange(3)] for x in xrange(3)]
                display[2][2] = 1.0
                display[0][0] = float(screen.width()) / float(totalResolution[0])
                # percent of screen height
                display[1][1] = float(screen.height()) / float(totalResolution[1])
                # offset in x
                if float(screen.topLeft().x()) != 0:
                    display[0][2] = float(screen.topLeft().x()) / float(totalResolution[0])
                # offset in y
                if float(screen.topLeft().y()) != 0:
                    display[1][2] = float(screen.topLeft().y()) / float(totalResolution[1])
                valid = True
                for i in range(0, 3):
                    for j in range(0, 3):
                        if float(tabletScreenCoords[(i, j)]) != float(display[i][j]):
                            valid = False
                            break
                if valid:
                    self.displays[id].setChecked(1)
                    break


    def setDevices(self, devices):
        for device in devices:
            device = device.split("\t")[0].strip().split(" ")
            self.devices.append(device[len(device)-1])


    def getScreenArea(self):
        setCommands = []
        if self.tabletActiveArea == "":
            self.tabletActiveArea = "HEAD-0"
        for device in self.devices:
            if device != "pad" and device != 'touch':
                if 'HEAD' in self.tabletActiveArea:
                    setCommands.append("xsetwacom --set \"%s %s\" MapToOutput %s" %
                                       (self.deviceNames[device], device, self.tabletActiveArea))
                else:
                    setCommands.append("xinput set-prop \"%s %s\" --type=float \"Coordinate Transformation Matrix\" %s"
                                       % (self.deviceNames[device], device, self.tabletActiveArea))
        return setCommands


    def getFlip(self):
        return self.orient


    def resetDefaults(self):
        self.orient = "xsetwacom --set \"%s stylus\" Rotate none" % self.deviceNames['stylus']
        self.orient += "\nxsetwacom --set \"%s eraser\" Rotate none" % self.deviceNames['eraser']
        self.tabletRight.setChecked(1)
        os.popen(self.orient)
        for device in self.devices:
            if device != "pad":
                cmd = "xinput set-prop \"%s %s\" --type=float \"Coordinate Transformation Matrix\" 1 0 0 0 1 0 0 0 1" \
                      % (self.deviceNames[device], device)
                setCommand = os.popen(cmd)
        if self.screenFull is not None:
            self.screenFull.setChecked(True)
