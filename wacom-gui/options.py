#!/usr/bin/python

#code repo: linuxproc.rhythm.com/src/systems/git/wacom-gui.git

from PyQt4 import QtCore,QtGui
import sys, os, re

class otherOptions(QtGui.QWidget):
    def __init__(self, tabletName, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.tabletName=tabletName

        self.initUI()

    def initUI(self):

        self.devices = []
        self.tabletActiveArea = ""
        self.orient = ''
        
        #layout code
        self.mainLayout = QtGui.QHBoxLayout()
        self.mainLayout.setAlignment(QtCore.Qt.AlignLeft)
        self.mainLayout.addWidget(self.screenOptions())
        self.mainLayout.addWidget(self.flipOptions())
        self.setLayout(self.mainLayout)
        
        #update current active screen area
        self.getCurrentScreen()

    def screenOptions(self):
        groupBox = QtGui.QGroupBox("Screen Area")
        groupBox.setAlignment(QtCore.Qt.AlignHCenter)
        groupBox.setFixedHeight(120)
        self.screenGroup = QtGui.QButtonGroup(groupBox)
        self.screenLeft = QtGui.QRadioButton("Left Monitor")
        self.screenRight = QtGui.QRadioButton("Right Monitor")
        self.screenFull  = QtGui.QRadioButton("Both Monitors")
        
        self.screenGroup.addButton(self.screenLeft)
        self.screenGroup.addButton(self.screenRight)
        self.screenGroup.addButton(self.screenFull)
        
        screenLayout = QtGui.QVBoxLayout()
        screenLayout.addWidget(self.screenLeft)
        screenLayout.addWidget(self.screenRight)
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
        
        getCommand = os.popen("xsetwacom --get \""+self.tabletName+" pad\" Rotate").readlines()
        #check correct button for orientation
        if getCommand[0] == "none\n":
            self.orient = "xsetwacom --set \""+self.tabletName+" pad\" Rotate none"
            self.tabletRight.setChecked(1)
        elif getCommand[0] == "half\n":
            self.orient = "xsetwacom --set \""+self.tabletName+" pad\" Rotate half"
            self.tabletLeft.setChecked(1)

        self.tabletFlipGroup.buttonClicked.connect(self.tabletFlipChange)

        groupBox.setLayout(flipLayout)

        return groupBox

    def tabletFlipChange(self, buttonId):
        if buttonId.text() == "Right-Handed":
            self.orient = "xsetwacom --set \""+self.tabletName+" pad\" Rotate none"
        elif buttonId.text() == "Left-Handed":
            self.orient = "xsetwacom --set \""+self.tabletName+" pad\" Rotate half"
        flipTablet = os.popen(self.orient)

    def screenChange(self,buttonId):
        screen = ""
        coords = ""
        if buttonId.text() == "Both Monitors":
            self.tabletActiveArea = "1 0 0 0 1 0 0 0 1"
            for device in self.devices:
                if device != self.tabletName+" pad":
                    setCommand = os.popen("xinput set-prop \"" + self.tabletName+ " " + device + "\" --type=float \"Coordinate Transformation Matrix\" " + self.tabletActiveArea)
                    #for i in range(len(self.otherOptionSettings)):
                    #    if self.otherOptionSettings[i].find("xinput set-prop") != -1 and self.otherOptionSettings[i].find(device) != -1:
                    #        self.otherOptionSettings[i] =  "xinput set-prop \"" + device + "\" --type=float \"Coordinate Transformation Matrix\" 1 0 0 0 1 0 0 0 1"
        elif buttonId.text() == "Left Monitor":
            screen = QtGui.QDesktopWidget().screenGeometry(0)
        elif buttonId.text() == "Right Monitor":
            screen = QtGui.QDesktopWidget().screenGeometry(1)
        if screen != "":
            totalResolution = os.popen("xdpyinfo | grep dimensions | awk '{print $2}' | awk -Fx '{print $1, $2}'").read()
            totalResolution = totalResolution.split()

            display = [[0 for x in xrange(3)] for x in xrange(3)]
            display[2][2]=1.0 

            display[0][0] = float(screen.width()) / float(totalResolution[0])
            display[1][1] = float(screen.height()) / float(totalResolution[1])
            if float(screen.topLeft().x())!=0:
                display[0][2] = float(screen.x()) / float(totalResolution[0])
            if float(screen.topLeft().y())!=0:
                display[1][2] = float(screen.y()) / float(totalResolution[1])
            
            self.tabletActiveArea = ''
            for x in xrange(3):
                for y in xrange(3):
                    self.tabletActiveArea = self.tabletActiveArea + " " + str(display[x][y])
            
            for device in self.devices:
                if device != self.tabletName+" pad":
                    setCommand = os.popen("xinput set-prop \"" + self.tabletName+ " " + device + "\" --type=float \"Coordinate Transformation Matrix\" " + self.tabletActiveArea)
                    #for i in range(len(self.otherOptionSettings)): 
                    #    if self.otherOptionSettings[i].find("xinput set-prop") != -1 and self.otherOptionSettings[i].find(device) != -1:
                    #        self.otherOptionSettings[i] =  "xinput set-prop \"" + device + "\" " + coordset

    def getTabletArea(self):
        #get current tablet area
        tabletInfo = os.popen("xinput list-props \""+ self.tabletName+ " stylus\" | grep Coordinate").readlines()
        tabletInfo[0] = tabletInfo[0][41:].rstrip('\n') 
        tabletInfo[0] = re.sub(",","",tabletInfo[0])
        tabletScreenCoords = {}
        blarg = tabletInfo[0].split()
        count = 0
        for i in range(0,3):
            for j in range(0,3):
                tabletScreenCoords[(i,j)] = blarg[count]
                self.tabletActiveArea = self.tabletActiveArea + " " + blarg[count]
                count+=1

        #check if "full screen"
        fullScreen = True
        for i in range(0,3):
            for j in range(0,3):
                if i == j and float(tabletScreenCoords[(i,j)]) != 1.0:
                    fullScreen = False
                    break
                elif i != j and float(tabletScreenCoords[(i,j)]) != 0.0:
                    fullScreen = False
                    break
        if fullScreen:
            self.screenFull.setChecked(1)
        #have to build array then compare... boo
        else:
            screen1 = QtGui.QDesktopWidget().screenGeometry(0)
            screen2 = QtGui.QDesktopWidget().screenGeometry(1)
            totalResolution = os.popen("xdpyinfo | grep dimensions | awk '{print $2}' | awk -Fx '{print $1, $2}'").read()
            totalResolution = totalResolution.split()


            display = [[0 for x in xrange(3)] for x in xrange(3)]
            display[2][2]=1.0 

            display[0][0] = float(screen1.width()) / float(totalResolution[0])
            #percent of screen height
            display[1][1] = float(screen1.height()) / float(totalResolution[1])
            #offset in x
            if float(screen1.topLeft().x())!=0:
                display[0][2] = float(screen1.topLeft().x()) / float(totalResolution[0])
            #offset in y
            if float(screen1.topLeft().y())!=0:
                display[1][2] = float(screen1.topLeft().y()) / float(totalResolution[1])

            isLeft = True
            for i in range(0,3):
                for j in range(0,3):
                    if float(tabletScreenCoords[(i,j)]) != float(display[i][j]):
                        isLeft = False
                        break

            if isLeft:
                self.screenLeft.setChecked(1)
            #crap... check if right
            else:
                display[0][0] = float(screen2.width()) / float(totalResolution[0])
                #percent of screen height
                display[1][1] = float(screen2.height()) / float(totalResolution[1])
                #offset in x
                if float(screen2.topLeft().x())!=0:
                    display[0][2] = float(screen2.topLeft().x()) / float(totalResolution[0])
                #offset in y
                if float(screen2.topLeft().y())!=0:
                    display[1][2] = float(screen2.topLeft().y()) / float(totalResolution[1])

                isRight = True
                for i in range(0,3):
                    for j in range(0,3):
                        if float(tabletScreenCoords[(i,j)]) != float(display[i][j]):
                            isRight = False
                            break
                if isRight:
                    self.screenRight.setChecked(1)

    def getCurrentScreen(self):
        #check if we actually have more that 1 screen
        if QtGui.QDesktopWidget().numScreens() < 2 or QtGui.QDesktopWidget().numScreens() > 2:
            self.screenLeft.enabled = False 
            self.screenRight.enabled = False 
            self.screenFull.enabled = False 
            if QtGui.QDesktopWidget().numScreens() > 2:
                print "More that 2 monitors; this isn't available yet.  Disabling tablet area option"
        #set correct check box for active area... if it is valid
        else:
            self.getTabletArea()
    
    def setDevices(self, devices):
        for device in devices:
            device = device.split("\t")[0].strip().split(" ")
            self.devices.append(device[len(device)-1])

    def getScreenArea(self):
        setCommands = []
        for device in self.devices:
            if device != "pad":
                setCommands.append("xinput set-prop \""+self.tabletName+" "+ device + "\" --type=float \"Coordinate Transformation Matrix\" " + self.tabletActiveArea)
        return setCommands

    def getFlip(self):
        return self.orient

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    form = otherOptions()
    form.setDevices(['eraser','stylus','cursor','pad'])
    #form.resize(650,300)
    form.show()
    form.getFlip()
    sys.exit(app.exec_())
