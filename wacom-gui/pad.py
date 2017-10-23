#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
from os.path import expanduser
from PyQt4 import QtCore, QtGui
from wacom_data import tabletidentities


class Pad(QtGui.QWidget):
    buttonClicked = QtCore.pyqtSignal(int)

    def __init__(self):
        super(Pad, self).__init__()
       
        # signalMapper = QtCore.QSignalMapper(self)
        self.initUI()
        
    def initUI(self):
        #get tablet name/type
        tablets = os.popen("lsusb | grep -i wacom").readlines()
        self.TabletIds = tabletidentities()
        # reset button configs button
        self.buttonReset = QtGui.QPushButton("Button Reset")
        self.buttonReset.clicked.connect(self.resetButtons)

        label = ''
        if len(tablets) == 0:
            label = "No tablet detected"
            print label
            sys.exit()
        #if len(tablets) > 1:
            # no longer checking for multiple tablets; only the first is configured
        #    label = "Multiple tablets detected. Please connect only one at a time"
        #    print label
        #    sys.exit()
        else:
            #for (tab in tablets):
            code = tablets[0]
            code = code.split(" ")[5]
            self.Tablet = self.IdentifyByUSBId(code.split(":")[0], code.split(":")[1])
            #if self.Tablet.Name == 'generic':
            name = os.popen("xsetwacom --list devices | grep pad").readlines()[0].split("\t")[0].strip().rsplit(" ",1)[0]
            self.Tablet.Name = name
            # test if using newer wacom driver, which changed the device name... because they suck
            #name = os.popen("xsetwacom --list devices | grep pad").readlines()[0].split("\t")[0].strip().rsplit(" ", 1)[0]
            #tmp = 1
            label = self.Tablet.Name + ": " + self.Tablet.Model
        #read in previous config file, if exists
        home = expanduser("~") + "/.wacom-gui.sh"
        if os.path.exists(home) and os.access(home, os.X_OK):
            os.system(home)
        else:
            print "No previous config"

        opPath = os.path.dirname(os.path.realpath(__file__)) 

        self.setWindowIcon(QtGui.QIcon(opPath + '/images/wacom-gui.svg'))
        self.TabletImg = opPath + "/images/" + self.Tablet.Model + ".png"
        self.TabletLayout = opPath + "/images/pad/" + self.Tablet.Model + ".png"

        self.pixmap = QtGui.QPixmap(self.TabletImg)
        pixmap2= QtGui.QPixmap(self.TabletLayout)

        self.tabletName = QtGui.QLabel(self.Tablet.Name)

        #trying to draw on pixmap...
        painter = QtGui.QPainter (pixmap2)
        pen = QtGui.QPen(QtGui.QColor(160, 160, 180, 255))
        font = QtGui.QFont(painter.font())
        font.setPointSize(16)
        #font.setWeight(QtGui.QFont.DemiBold)
        painter.setFont(font)
        pen.setWidth(3)
        painter.setPen(pen)
        for i in range(len(self.Tablet.Buttons)):
           # if self.Tablet.Buttons[i].Callsign == 'AbsWheelUp':
           #     box = QtCore.QRectF(self.Tablet.Buttons[i].X1, self.Tablet.Buttons[i].Y1, self.Tablet.Buttons[i].X2, self.Tablet.Buttons[i].Y2)
           #     painter.drawArc(box,-45*16,90*16)
           #     font.setPointSize(8)
           #     painter.setFont(font)
           #     box2 = QtCore.QRectF(self.Tablet.Buttons[i].X1 + self.Tablet.Buttons[i].X2 -10, self.Tablet.Buttons[i].Y1 -20, 40, 40)
           #     painter.drawText(box2,QtCore.Qt.AlignCenter,"Touch\nUp")
           # elif self.Tablet.Buttons[i].Callsign == 'AbsWheelDown':
           #     box = QtCore.QRectF(self.Tablet.Buttons[i].X1, self.Tablet.Buttons[i].Y1, self.Tablet.Buttons[i].X2, self.Tablet.Buttons[i].Y2)
           #     painter.drawArc(box,225*16,-90*16)
           #     font.setPointSize(8)
           #     painter.setFont(font)
           #     box2 = QtCore.QRectF(self.Tablet.Buttons[i].X1 -30, self.Tablet.Buttons[i].Y1 -20, 40, 40)
           #     painter.drawText(box2,QtCore.Qt.AlignCenter,"Touch\nDown")
           # else:
            if (self.Tablet.Buttons[i].Callsign != 'AbsWheelUp' and self.Tablet.Buttons[i].Callsign != 'AbsWheelDown'):
                box = QtCore.QRectF(self.Tablet.Buttons[i].X1, self.Tablet.Buttons[i].Y1,
                                    self.Tablet.Buttons[i].X2, self.Tablet.Buttons[i].Y2)
                painter.drawRect(box)
                painter.drawText(box, QtCore.Qt.AlignCenter, self.Tablet.Buttons[i].Number)
        painter.end()

        #self.tabletIcon = QtGui.QLabel(self)
        #self.tabletIcon.setPixmap(self.pixmap)
        self.tabletPad = QtGui.QLabel(self)
        self.tabletPad.setPixmap(pixmap2)

        self.padButtons = {}
        self.padButtonsLayout = QtGui.QGridLayout()

        self.buttonMapper = QtCore.QSignalMapper(self)

        for i in range(len(self.Tablet.Buttons)):
            buttonType = "Button "+self.Tablet.Buttons[i].Number
            if self.Tablet.Buttons[i].Callsign == 'AbsWheelUp' or self.Tablet.Buttons[i].Callsign == 'AbsWheelDown':
                buttonType = self.Tablet.Buttons[i].Callsign
            getCommand = os.popen("xsetwacom --get \"" + self.Tablet.Name + " pad\" " + buttonType).readlines()
            if str(getCommand).find("key") == -1 and str(getCommand).find("button") == -1:
                self.padButtons[(i, 0)] = QtGui.QLabel("UNDEFINED")
            elif getCommand[0] == "button +0 \n":
                self.padButtons[(i, 0)] = QtGui.QLabel("None")
            else:    
                self.padButtons[(i, 0)] = QtGui.QLabel(self.wacomToHuman(getCommand[0]))
            self.padButtons[(i, 1)] = QtGui.QPushButton(self.Tablet.Buttons[i].Name)

            self.padButtons[(i, 1)].clicked[()].connect(self.buttonMapper.map)
            self.padButtons[(i, 2)] = self.Tablet.Buttons[i].Number
            if getCommand[0] == "button +0 \n":
                self.padButtons[(i, 3)] = 0
            else:
                self.padButtons[(i, 3)] = getCommand[0].rstrip('\n')
            self.padButtons[(i, 4)] = self.Tablet.Buttons[i].Callsign
            self.buttonMapper.setMapping(self.padButtons[(i, 1)], i)
            self.padButtonsLayout.addWidget(self.padButtons[i, 0], i, 0)
            self.padButtonsLayout.addWidget(self.padButtons[i, 1], i, 1)

        self.buttonMapper.mapped.connect(self.updatePadButton)

        self.vMaster = QtGui.QHBoxLayout()
        self.vMaster.addLayout(self.padButtonsLayout)
        self.vMaster.addWidget(self.tabletPad)
        self.vMaster.addWidget(self.buttonReset)

        self.setLayout(self.vMaster)

        #function to check what button has been pressed
        self.activeButton = None
        self.editButton = lambda : self.activeButton
        self.buttonCommandList = []

    def IdentifyByUSBId(self,VendId,DevId):
        for item in self.TabletIds.Tablets:
            if item.ProductId == int(DevId, 16) and int(VendId, 16) == int("056a", 16):
                return item
        return self.TabletIds.Tablets[len(self.TabletIds.Tablets)-1]

    def getTabletName(self):
        return self.Tablet.Name

    def getIcon(self):
        return self.pixmap

    def getCommands(self):
        buttons = []
        for i in range(len(self.Tablet.Buttons)):
            if (i < 9 and len(str(self.padButtons[(i, 3)])) > 1) or \
                    (i >= 9 and len(str(self.padButtons[(i, 3)])) > 2) or self.padButtons[(i, 3)] == 0:
                cmd = "xsetwacom --set \"" + self.Tablet.Name + " pad\" "
                if self.padButtons[(i, 4)] == 'AbsWheelUp' or self.padButtons[(i, 4)] == 'AbsWheelDown':
                    cmd += self.padButtons[(i, 4)] + " "
                    # buttons.append("xsetwacom --set \""+self.Tablet.Name+" pad\" " + self.padButtons[(i, 4)] +
                    #               " \"" + str(self.padButtons[(i, 3)]) + "\"")
                else:
                    cmd += "Button " + self.padButtons[(i, 2)]
                    #buttons.append("xsetwacom --set \""+self.Tablet.Name+" pad\" Button " + self.padButtons[(i, 2)] +
                    #               " \"" + str(self.padButtons[(i, 3)]) + "\"")
                if self.padButtons[(i, 3)] == 0:
                    cmd += ' 0'
                else:
                    cmd += " \"" + str(self.padButtons[(i, 3)]) + "\""
                buttons.append(cmd)
        return buttons

    #for pad buttons
    def updatePadButton(self, button):
        if self.activeButton is None:
            self.activeButton = self.padButtons[(button, 2)]
            self.padButtons[(button, 0)].setText("Recording keypresses... Click button to stop")
            self.buttonCommandList[:] = []
        elif self.activeButton == self.padButtons[(button, 2)]:
            self.activeButton = None
            userInput = self.userToWacomKeystrokeTranslate()
            if userInput is None:
                print self.wacomToHuman(self.padButtons[(button, 3)])
                # self.padButtons[(button,0)].setText(self.padButtons[(button,3)])
                self.padButtons[(button, 0)].setText(self.wacomToHuman(self.padButtons[(button, 3)]))
            else:
                setCommand = self.wacomToHuman(userInput)
                self.padButtons[(button, 0)].setText(setCommand)
                # this is hack-y but should be simplified; need to remove the number as I don't think it's necessary...
                buttonType = "Button " + self.padButtons[(button, 2)]
                if self.padButtons[(button, 4)] == 'AbsWheelUp' or self.padButtons[(button, 4)] == 'AbsWheelDown':
                    buttonType = self.padButtons[(button, 4)]
                # end of hackey shit.  Why did they do this originally??!???
                if userInput == 0:
                    cmd = "xsetwacom --set \"%s pad\" %s %s" % (self.Tablet.Name, buttonType, str(userInput))
                else:
                    cmd = "xsetwacom --set \"%s pad\" %s \"%s\"" %(self.Tablet.Name, buttonType, str(userInput))
                # setCommand = os.popen("xsetwacom --set \"" + self.Tablet.Name + " pad\" " +
                #                      buttonType + " \"" + str(userInput) + "\"")
                setCommand = os.popen(cmd)
                self.padButtons[(button, 3)] = userInput

    def event(self, event):
        if (event.type() == QtCore.QEvent.ShortcutOverride and
                (event.key() == QtCore.Qt.Key_Tab or event.key() == QtCore.Qt.Key_Up or
                         event.key() == QtCore.Qt.Key_Down or event.key() == QtCore.Qt.Key_Left or
                         event.key() == QtCore.Qt.Key_Right)) or event.type() == QtCore.QEvent.KeyPress or \
                        event.type() == QtCore.QEvent.MouseButtonPress or \
                        event.type() == QtCore.QEvent.MouseButtonDblClick:
                if self.editButton() is not None:
                    print self.keyTranslate(event.key(), event.text(), '+')
                    if event.type() == QtCore.QEvent.MouseButtonPress or \
                                    event.type() == QtCore.QEvent.MouseButtonDblClick:
                        self.buttonCommandList.append("button")
                        self.buttonCommandList.append("+" + str(event.button()))
                        self.buttonCommandList.append("-" + str(event.button()))
                    else:
                        self.buttonCommandList.append(self.keyTranslate(event.key(), event.text(), '+'))
                return False
        elif event.type() == QtCore.QEvent.KeyRelease:
            if event.key() == QtCore.Qt.Key_Shift or event.key() == QtCore.Qt.Key_Alt or \
                            event.key() == QtCore.Qt.Key_Control:
                self.buttonCommandList.append(self.keyTranslate(event.key(), event.text(), '-'))
            return False
        return QtGui.QWidget.event(self, event)

    def keyTranslate(self, keyvalue, keytext, keystate):
        #print "Key value: " + str(keyvalue)
        if (33 <= keyvalue <= 96) or (123 <= keyvalue <= 126):
            if keytext != chr(keyvalue):
                keytext = chr(keyvalue)
            return keytext
        else:
            # this is a hack; Mate interprets Win key as Meta instead of Hyper by default
            if keyvalue == 16777250:
                keyvalue = 16777302
            return {
                QtCore.Qt.Key_Shift: keystate + 'Shift_L',
                QtCore.Qt.Key_Alt: keystate + 'Alt_L',
                QtCore.Qt.Key_Control: keystate + 'Control_L',
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
                QtCore.Qt.Key_Meta: keystate + 'Hyper_L',
            }.get(keyvalue, '')

    def userToWacomKeystrokeTranslate(self):
        if len(self.buttonCommandList) != 0:
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
                if button and (item == "+1" or item == "-1" or item == "+2" or item == "-2" or
                                       item == "+4" or item == "-4" or item == "button"):
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
            # keycode to set button to "None"
            if inputString == 'key 0 0 0':
                inputString = 0
            return inputString
        else:
            return None

    def wacomToHuman(self, command):
        if command == 0:
            return "None"
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
            elif item == "+equal":
                item = "+"
            elif item == "+minus":
                item = "-"
            elif item == "+90":
                item = "Ctrl +"
            elif item == "+91":
                item = "Ctrl -"
            elif item == "-Alt_L" or item == "-Alt_R" or item == "-Control_L" or item == "-Control_R" \
                or item == "-Tab" or item == "-equal" or item == "-minus":
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

    def resetButtons(self):
        for i in range(self.Tablet.Buttons.__len__()):
            if 'Abs' in self.padButtons[(i, 4)]:
                #touch wheel, do other stuff
                if 'Up' in self.padButtons[(i, 4)]:
                    bid = 4
                    self.padButtons[(i, 3)] = 'button +4'
                else:
                    bid = 5
                    self.padButtons[(i, 3)] = 'button +5'
                cmd = "xsetwacom --set \"%s pad\" %s %i" % (self.Tablet.Name, self.padButtons[(i, 4)], bid)
            else:
                bid = int(self.padButtons[(i, 2)])
                self.padButtons[(i, 3)] = 'button +%i' % bid
                cmd = "xsetwacom --set \"%s pad\" Button %i %i" % (self.Tablet.Name, bid, bid)
            setCommand = os.popen(cmd)
            self.padButtons[(i, 0)].setText("")
            tmp = 1
                # update text?

def main():

    app = QtGui.QApplication(sys.argv)
    window = Pad()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()    
