#!/usr/bin/python

from PyQt4 import QtCore, QtGui
import sys
import os
import re
import subprocess

class otherOptions(QtGui.QWidget):
    def __init__(self, tabletName, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.tabletName = tabletName.replace('Pad', 'Pen')

        self.initUI()

    def initUI(self):

        self.devices = []
        self.tabletActiveArea = ""
        self.orient = ''
        
        #layout code
        self.mainLayout = QtGui.QHBoxLayout()
        self.mainLayout.setAlignment(QtCore.Qt.AlignLeft)
        screens = self.screenOptions()
        if screens:
            self.mainLayout.addWidget(screens)
        self.mainLayout.addWidget(self.flipOptions())
        self.setLayout(self.mainLayout)
        
        #update current active screen area
        self.getCurrentScreen()

    def screenOptions(self):
        if QtGui.QDesktopWidget().numScreens() == 1:
            return None
        groupBox = QtGui.QGroupBox("Screen Area")
        groupBox.setAlignment(QtCore.Qt.AlignHCenter)
        groupBox.setFixedHeight(120)
        displays = self.get_monitors()
        self.screenGroup = QtGui.QButtonGroup(groupBox)
        self.displays = []
        for x in range(0, QtGui.QDesktopWidget().numScreens()):
            self.displays.append(QtGui.QRadioButton("Monitor %d" % x))
        #self.screenLeft = QtGui.QRadioButton("Left Monitor")
        #self.screenRight = QtGui.QRadioButton("Right Monitor")
        self.screenFull  = QtGui.QRadioButton("All Monitors")

        for screen in self.displays:
            self.screenGroup.addButton(screen)
        #self.screenGroup.addButton(self.screenLeft)
        #self.screenGroup.addButton(self.screenRight)
        self.screenGroup.addButton(self.screenFull)
        
        screenLayout = QtGui.QVBoxLayout()
        for screen in self.displays:
            screenLayout.addWidget(screen)
        #screenLayout.addWidget(self.screenLeft)
        #screenLayout.addWidget(self.screenRight)
        screenLayout.addWidget(self.screenFull)
        screenLayout.addStretch(1)

        self.screenGroup.buttonClicked.connect(self.screenChange)

        groupBox.setLayout(screenLayout)

        return groupBox


    def get_monitors(self):
        p = subprocess.Popen("xrandr | grep \" connected\"", shell=True, stdout=subprocess.PIPE)
        output = p.communicate()[0].split('\n')
        regex = r"^([\w-]+)(\D+)(\d+)x(\d+)\+(\d+)\+(\d+)"
        screens = {}
        for display in output:
            if display != '':
                match = re.search(regex, display)
                if match.group(5) not in screens.keys():
                    screens[match.group(5)] = {}
                screens[match.group(5)][match.group(6)] = match.group(1)
        displays = []
        for x in sorted(screens.keys()):
            for y in sorted(screens[x].keys()):
                displays.append(screens[x][y])
        return displays

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
        
        getCommand = os.popen("xsetwacom --get \"%s stylus\" Rotate" % self.tabletName).readlines()
        # check correct button for orientation
        if getCommand[0] == "none\n":
            self.orient = "xsetwacom --set \"%s stylus\" Rotate none" % self.tabletName
            self.orient += "\nxsetwacom --set \"%s eraser\" Rotate none" % self.tabletName
            self.tabletRight.setChecked(1)
        elif getCommand[0] == "half\n":
            self.orient = "xsetwacom --set \"%s stylus\" Rotate half" % self.tabletName
            self.orient += "\nxsetwacom --set \"%s eraser\" Rotate half" % self.tabletName
            self.tabletLeft.setChecked(1)

        self.tabletFlipGroup.buttonClicked.connect(self.tabletFlipChange)

        groupBox.setLayout(flipLayout)

        return groupBox

    def tabletFlipChange(self, buttonId):
        if buttonId.text() == "Right-Handed":
            self.orient = "xsetwacom --set \"%s stylus\" Rotate none" % self.tabletName
            self.orient += "\nxsetwacom --set \"%s eraser\" Rotate none" % self.tabletName
        elif buttonId.text() == "Left-Handed":
            self.orient = "xsetwacom --set \"%s stylus\" Rotate half" % self.tabletName
            self.orient += "\nxsetwacom --set \"%s eraser\" Rotate half" % self.tabletName
        flipTablet = os.popen(self.orient)


    def screenChange(self, buttonId):
        if buttonId.text() == "All Monitors":
            self.tabletActiveArea = "1 0 0 0 1 0 0 0 1"
            for device in self.devices:
                if device != "pad":
                    cmd = "xinput set-prop \"%s %s\" --type=float \"Coordinate Transformation Matrix\" %s" % \
                          (self.tabletName, device, self.tabletActiveArea)
                    setCommand = os.popen(cmd)
        else:
            self.tabletActiveArea = "HEAD-%s" % buttonId.text().split(' ')[1]
            for device in self.devices:
                if device != "pad":
                    cmd = "xsetwacom set \"%s %s\" MapToOutput %s" % (self.tabletName, device, self.tabletActiveArea)
                    setCommand = os.popen(cmd)


    def getTabletArea(self):
        # get current tablet area
        tabletInfo = os.popen("xinput list-props \"%s stylus\" | grep Coordinate" % self.tabletName).readlines()
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
            #screen1 = QtGui.QDesktopWidget().screenGeometry(0)
            #screen2 = QtGui.QDesktopWidget().screenGeometry(1)
                totalResolution = os.popen("xdpyinfo | grep dimensions | awk '{print $2}' | awk -Fx '{print $1, $2}'").read()
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

            #isLeft = True
                for i in range(0, 3):
                    for j in range(0, 3):
                        if float(tabletScreenCoords[(i, j)]) != float(display[i][j]):
                            valid = False
                            break
                if valid:
                    self.displays[id].setChecked(1)
                    break


            #if isLeft:
            #    self.screenLeft.setChecked(1)
            # crap... check if right
            #else:
            #    display[0][0] = float(screen2.width()) / float(totalResolution[0])
            #    # percent of screen height
            #    display[1][1] = float(screen2.height()) / float(totalResolution[1])
            #    # offset in x
            #    if float(screen2.topLeft().x()) != 0:
            #        display[0][2] = float(screen2.topLeft().x()) / float(totalResolution[0])
            #    # offset in y
            #    if float(screen2.topLeft().y()) != 0:
            #        display[1][2] = float(screen2.topLeft().y()) / float(totalResolution[1])#

            #    isRight = True
            #    for i in range(0,3):
            #        for j in range(0,3):
            #            if float(tabletScreenCoords[(i, j)]) != float(display[i][j]):
            #                isRight = False
            #                break
            #    if isRight:
            #        self.screenRight.setChecked(1)


    def getCurrentScreen(self):
        # check if we actually have more that 1 screen
        if QtGui.QDesktopWidget().numScreens() < 2 or QtGui.QDesktopWidget().numScreens() > 2:
            self.screenLeft.enabled = False 
            self.screenRight.enabled = False 
            self.screenFull.enabled = False 
            if QtGui.QDesktopWidget().numScreens() > 2:
                print "More that 2 monitors; this isn't available yet.  Disabling tablet area option"
        # set correct check box for active area... if it is valid
        else:
            self.getTabletArea()
    
    def setDevices(self, devices):
        for device in devices:
            device = device.split("\t")[0].strip().split(" ")
            self.devices.append(device[len(device)-1])

    def getScreenArea(self):
        setCommands = []
        for device in self.devices:
            if device != "pad" and device != 'touch':
                if 'HEAD' in self.tabletActiveArea:
                    setCommands.append("xsetwacom set \"%s %s\" MapToOutput %s" %
                                       (self.tabletName, device, self.tabletActiveArea))
                else:
                    setCommands.append("xinput set-prop \"%s %s\" --type=float \"Coordinate Transformation Matrix\" %s"
                                       % (self.tabletName, device, self.tabletActiveArea))
        return setCommands


    def getFlip(self):
        return self.orient


    def resetDefaults(self):
        self.orient = "xsetwacom --set \"%s stylus\" Rotate none" % self.tabletName
        self.orient += "\nxsetwacom --set \"%s eraser\" Rotate none" % self.tabletName
        self.tabletRight.setChecked(1)
        os.popen(self.orient)
        for device in self.devices:
            if device != "pad":
                cmd = "xinput set-prop \"%s %s\" --type=float \"Coordinate Transformation Matrix\" 1 0 0 0 1 0 0 0 1" % \
                      (self.tabletName, device)
                setCommand = os.popen(cmd)
        self.screenFull.setChecked(True)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    form = otherOptions()
    form.setDevices(['eraser', 'stylus', 'cursor', 'pad'])
    #form.resize(650,300)
    form.show()
    form.getFlip()
    sys.exit(app.exec_())
