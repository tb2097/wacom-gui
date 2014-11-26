#!/usr/bin/python
# -*- coding: utf-8 -*-

#code repo: linuxproc.rhythm.com/src/systems/git/wacom-gui.git


import sys
import os
from os.path import expanduser
from PyQt4 import QtCore,QtGui
from wacom_data import tabletidentities


class Pad(QtGui.QWidget):
   

    buttonClicked = QtCore.pyqtSignal(int)

    def __init__(self):
        super(Pad, self).__init__()
       
        signalMapper = QtCore.QSignalMapper(self)
        self.initUI()
        
    def initUI(self):
        #get tablet name/type
        tablets = os.popen("lsusb | grep -i wacom").readlines()
        self.TabletIds = tabletidentities()

        label = ''
        if len(tablets) > 1:
            label = "Multiple tablets detected. Please connect only one at a time"
            print label
            sys.exit()
        if len(tablets) == 0:
            label = "No tablet detected"
            print label
            sys.exit()
        else:
            code = tablets[0]
            code = code.split(" ")[5] 
            self.Tablet = self.IdentifyByUSBId(code.split(":")[0],code.split(":")[1])
            label = self.Tablet.Name + ": " + self.Tablet.Model


        #read in previous config file, if exists
        home = expanduser("~") + "/.wacom-gui.sh"
        if os.path.exists(home) and os.access(home, os.X_OK):
            os.system(home)
        else:
            print "No previous config"

        opPath = os.path.dirname(os.path.realpath(__file__)) 

        self.setWindowIcon(QtGui.QIcon(opPath + '/images/wacom-gui.svg')) 
        self.TabletImg = opPath + "/images/" + self.Tablet.Model  + ".png"
        self.TabletLayout = opPath + "/images/pad/" + self.Tablet.Model  + ".png"

        self.pixmap = QtGui.QPixmap(self.TabletImg)
        pixmap2= QtGui.QPixmap(self.TabletLayout)

        self.tabletName = QtGui.QLabel(self.Tablet.Name)

        #trying to draw on pixmap...
        painter = QtGui.QPainter (pixmap2)
        pen = QtGui.QPen(QtGui.QColor(160,160,180,255))
        font = QtGui.QFont(painter.font())
        font.setPointSize(16)
        #font.setWeight(QtGui.QFont.DemiBold)
        painter.setFont(font)
        pen.setWidth(3)
        painter.setPen(pen)
        for i in range(len(self.Tablet.Buttons)):
            box = QtCore.QRectF(self.Tablet.Buttons[i].X1, self.Tablet.Buttons[i].Y1, self.Tablet.Buttons[i].X2, self.Tablet.Buttons[i].Y2)
            painter.drawRect(box)
            painter.drawText(box,QtCore.Qt.AlignCenter,self.Tablet.Buttons[i].Number)
        painter.end()

        #self.tabletIcon = QtGui.QLabel(self)
        #self.tabletIcon.setPixmap(self.pixmap)
        self.tabletPad = QtGui.QLabel(self)
        self.tabletPad.setPixmap(pixmap2)

        self.padButtons = {}
        self.padButtonsLayout = QtGui.QGridLayout()

        self.buttonMapper = QtCore.QSignalMapper(self)

        for i in range(len(self.Tablet.Buttons)):
            getCommand = os.popen("xsetwacom --get \""+self.Tablet.Name+" pad\" Button "+self.Tablet.Buttons[i].Number).readlines()
            if str(getCommand).find("key") == -1 and str(getCommand).find("button") == -1:
                self.padButtons[(i,0)] = QtGui.QLabel("UNDEFINED")
            else:    
                self.padButtons[(i,0)] = QtGui.QLabel(self.wacomToHuman(getCommand[0]))
            self.padButtons[(i,1)] = QtGui.QPushButton(self.Tablet.Buttons[i].Name)

            self.padButtons[(i,1)].clicked[()].connect(self.buttonMapper.map)
            self.padButtons[(i,2)] = self.Tablet.Buttons[i].Number
            self.padButtons[(i,3)] = getCommand[0].rstrip('\n')
            self.buttonMapper.setMapping(self.padButtons[(i,1)],i)
            self.padButtonsLayout.addWidget(self.padButtons[i,0],i,0)
            self.padButtonsLayout.addWidget(self.padButtons[i,1],i,1)

        self.buttonMapper.mapped.connect(self.updatePadButton)

        self.vMaster = QtGui.QHBoxLayout()
        self.vMaster.addLayout(self.padButtonsLayout)
        self.vMaster.addWidget(self.tabletPad)

        self.setLayout(self.vMaster)

        #function to check what button has been pressed
        self.activeButton = None
        self.editButton = lambda : self.activeButton
        self.buttonCommandList = []

    def IdentifyByUSBId(self,VendId,DevId):
        for item in self.TabletIds.Tablets:
            if item.ProductId == int(DevId,16) and int(VendId,16) == int("056a",16):
                return item

    def getTabletName(self):
        return self.Tablet.Name

    def getIcon(self):
        return self.pixmap

    def getCommands(self):
        buttons = []
        for i in range(len(self.Tablet.Buttons)):
            buttons.append("xsetwacom --set \""+self.Tablet.Name+" pad\" Button " + self.padButtons[(i,2)] + " \"" + self.padButtons[(i,3)] + "\"")

        return buttons

    #for pad buttons
    def updatePadButton(self,button):
        if self.activeButton is None:
            self.activeButton = self.padButtons[(button,2)]
            self.padButtons[(button,0)].setText("Recording keypresses... Click button to stop")
            self.buttonCommandList[:] = []
        elif self.activeButton == self.padButtons[(button,2)]:
            self.activeButton = None
            userInput = self.userToWacomKeystrokeTranslate()
            if userInput is None:
                print self.wacomToHuman(self.padButtons[(button,3)])
                #self.padButtons[(button,0)].setText(self.padButtons[(button,3)])
                self.padButtons[(button,0)].setText(self.wacomToHuman(self.padButtons[(button,3)]))
            else:    
                setCommand = self.wacomToHuman(userInput)
                self.padButtons[(button,0)].setText(setCommand)
                setCommand = os.popen("xsetwacom --set \""+self.Tablet.Name+" pad\" Button "+self.padButtons[(button,2)] + " \"" + userInput + "\"")
                self.padButtons[(button,3)] = userInput

    def event(self,event):
        if (event.type() == QtCore.QEvent.ShortcutOverride and (event.key() == QtCore.Qt.Key_Tab or event.key() == QtCore.Qt.Key_Up or \
            event.key() == QtCore.Qt.Key_Down or event.key() == QtCore.Qt.Key_Left or event.key() == QtCore.Qt.Key_Right)) or \
            event.type() == QtCore.QEvent.KeyPress or event.type() == QtCore.QEvent.MouseButtonPress or event.type() == QtCore.QEvent.MouseButtonDblClick:
                if(self.editButton() is not None):
                    #print self.keyTranslate(event.key(),event.text())
                    if event.type() == QtCore.QEvent.MouseButtonPress or event.type() == QtCore.QEvent.MouseButtonDblClick:
                        self.buttonCommandList.append("button")
                        self.buttonCommandList.append("+" + str(event.button()))
                        self.buttonCommandList.append("-" + str(event.button()))
                    else:
                        self.buttonCommandList.append(self.keyTranslate(event.key(),event.text(),'+'))
                return False
        elif event.type() == QtCore.QEvent.KeyRelease:
            if event.key() == QtCore.Qt.Key_Shift or event.key() == QtCore.Qt.Key_Alt or event.key() == QtCore.Qt.Key_Control or event.key() == QtCore.Qt.Key_Meta:
                self.buttonCommandList.append(self.keyTranslate(event.key(),event.text(),'-'))
            return False
        return QtGui.QWidget.event(self, event)

    def keyTranslate(self,keyvalue,keytext,keystate):
        #print "Key value: " + str(keyvalue)
        if (keyvalue >= 33 and keyvalue <=96) or (keyvalue >=123 and keyvalue <=126):
            if keytext != chr(keyvalue):
                keytext = chr(keyvalue)
            return keytext
        else:
            return {
                QtCore.Qt.Key_Shift: keystate + 'Shift_L',
                QtCore.Qt.Key_Alt: keystate + 'Alt_L',
                QtCore.Qt.Key_Control: keystate + 'Control_L',
                QtCore.Qt.Key_Meta: keystate + 'Meta',
                QtCore.Qt.Key_Super_L: '+Super_L',
                QtCore.Qt.Key_Super_R: '+Super_R',
                QtCore.Qt.Key_Hyper_L: '+Hyper_L',
                QtCore.Qt.Key_Hyper_R: '+Hyper_R',
                QtCore.Qt.Key_Escape: '+Escape',
                QtCore.Qt.Key_Backspace: '+Backspace',
                QtCore.Qt.Key_PageUp: '+Prior',
                QtCore.Qt.Key_PageDown: '+Next',
                QtCore.Qt.Key_Up: '+Up',
                QtCore.Qt.Key_Down: '+Down',
                QtCore.Qt.Key_Left: '+Left',
                QtCore.Qt.Key_Right: '+Right',
                QtCore.Qt.Key_Tab: '+Tab',
                QtCore.Qt.Key_F1: '+F1',
                QtCore.Qt.Key_F2: '+F2',
                QtCore.Qt.Key_F3: '+F3',
                QtCore.Qt.Key_F4: '+F4',
                QtCore.Qt.Key_F5: '+F5',
                QtCore.Qt.Key_F6: '+F6',
                QtCore.Qt.Key_F7: '+F7',
                QtCore.Qt.Key_F8: '+F8',
                QtCore.Qt.Key_F9: '+F9',
                QtCore.Qt.Key_F10: '+F10',
                QtCore.Qt.Key_F11: '+F11',
                QtCore.Qt.Key_F12: '+F12',
            }.get(keyvalue,'')

    def userToWacomKeystrokeTranslate(self):
        if len(self.buttonCommandList) !=0:
            inputString = ""
            button = False
            shift = False
            for item in self.buttonCommandList:
                #first check for mouse button crap
                if item == "button":
                    button = True
                    inputString += " " + str(item)
                elif len(inputString) == 0:
                    inputString = "key"
                if button == True and (item == "+1" or item == "-1" or item == "+2" or item == "-2" or item == "+4" or item == "-4" or item == "button"):
                    if item != "button":
                        #print "currently in a button " + str(item)
                        inputString += " " + str(item)
                elif button != False:
                    button = False
                    #print "finished with button; move onto other stuff " + str(item)
                    #inputString += " key " + str(item)
                #now check for special characters
                if item == "shift":
                    shift = True
                    inputString += " " + str(item)
                if shift == True and button == False:
                    # shift active, check if it is being applied to this character or not
                    if len(item) == 1 and str(item).isalpha():
                        #print "This is a letter, shift is active " + str(item)
                        if str(item).isupper():
                            inputString += " " + str(item)
                        else:
                            shift = False
                            inputString += " -shift " + str(item)
                elif button == False:
                    inputString += " " + str(item)



            return inputString
        else:
            return None

    def wacomToHuman(self,command):
        values = command.split()
        humanReadable = ""
        shift = False
        mouseButton = False
        mouseButtonHold = False
        for item in values:
            #print "Values = " + str(item)
            if item == 'key' and mouseButtonHold != False:
                item = mouseButtonHold
                mouseButtonHold = False
            elif item == "+Shift_L" or item == "+Shift_R":
                shift = True
                item = "SHIFT"
            elif item == "-Shift_L" or item == "-Shift_R":
                shift = False
                item = "-SHIFT"
            elif item == "+Alt_L" or item == "+Alt_R":
                item = "ALT"
            elif item == "+Control_L" or item == "+Control_R":
                item = "CTRL"
            elif item == "+Tab":
                item = "TAB"
            elif item == "-Alt_L" or item == "-Alt_R" or item == "-Control_L" or item == "-Control_R" or item == "-Tab":
                item = ""
            elif item.find("button") != -1:
                mouseButton = True
            elif mouseButton == True:
                if item == "+1":
                    if mouseButtonHold == False:
                        mouseButtonHold = "Left-Click"
                        item = ""
                    elif mouseButtonHold == "Left-Click":
                        item = "Dbl Left-Click"
                        mouseButtonHold = False
                    else:
                        item = mouseButtonHold
                        mouseButtonHold = "Left-Click"
                if item == "+2":
                    if mouseButtonHold == False:
                        mouseButtonHold = "Right-Click"
                        item = ""
                    elif mouseButtonHold == "Right-Click":
                        item = "Dbl Right-Click"
                        mouseButtonHold = False
                    else:
                        item = mouseButtonHold
                        mouseButtonHold = "Right-Click"
                if item == "+4":
                    if mouseButtonHold == False:
                        mouseButtonHold = "Middle-Click"
                        item = ""
                    elif mouseButtonHold == "Middle-Click":
                        item = "Dbl Middle-Click"
                        mouseButtonHold = False
                    else: 
                        item = mouseButtonHold
                        mouseButtonHold = "Middle-Click"
                if item == "-1" or item == "-2" or item == "-4":
                    item = ""
                   
            if (item != 'key' and item !='button'):
                if str(item)[:-1] == '+' or str(item)[:-1] == '-' and len(str(item)[1:]) == 1:
                    if str(item)[:-1] == '+':
                        item = str(item)[1:]
                    elif str(item)[:-1] == '-':
                        item = ""
                if len(humanReadable) > 0 and len(item) > 0:
                    humanReadable += " " + str(item)
                elif len(item) > 0:
                    humanReadable = str(item)
        return humanReadable

def main():

    app = QtGui.QApplication(sys.argv)
    window = Pad()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()    
