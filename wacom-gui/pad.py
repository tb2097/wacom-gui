#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import errno
import distutils.dir_util
import shutil
import os
import re
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
        self.buttonReset = QtGui.QPushButton("Reset Buttons")
        self.buttonToggle = QtGui.QPushButton("Disable Buttons")
        self.buttonReset.clicked.connect(self.resetButtons)
        self.buttonToggle.clicked.connect(self.toggleButtons)

        label = ''
        if len(tablets) == 0:
            print "No tablet detected"
            w = QtGui.QMessageBox()
            QtGui.QMessageBox.warning(w, "Error", label)
            w.show()
            sys.exit(-1)
        else:
            self.Tablet = []
            for idx, tablet in enumerate(tablets):
                (VendId, DevId) = tablet.split(" ")[5].split(":")
                self.Tablet.append(self.IdentifyByUSBId(VendId, DevId))
                if self.Tablet[idx].Model != "generic":
                    self.Tablet[idx].devID = DevId
                else:
                    self.Tablet[idx].devID = "generic"
                    # break
            # if we have multiple tablets, need to figure out which one we use...
            if self.Tablet.__len__() != 1:
                label = "Multiple Tablets detected; using the first one detected: %s (%s)" % \
                        (self.Tablet.Name, self.Tablet.Model)
                w = QtGui.QMessageBox()
                QtGui.QMessageBox.warning(w, "Information", label)
                w.show()
            self.Tablet = self.Tablet[0]
            # on some tablets each 'device' has a different name ...
            # read in wacom devices into an dict
            deviceNames = {'eraser': "", 'stylus': "", 'cursor': "", 'pad': "", 'touch': ""}
            foundDevs = False
            with os.popen("xsetwacom --list devices") as f:
                for line in f:
                    deviceNames[line.strip().rsplit(" ", 1)[1].lower()] = line.split("\t")[0].strip().rsplit(" ", 1)[0]
                    foundDevs = True

            if not foundDevs:
                label = "Tablet not supported"
                w = QtGui.QMessageBox()
                QtGui.QMessageBox.warning(w, "Error", label)
                w.show()
                # print label
                sys.exit(-1)

            self.Tablet.deviceNames = deviceNames
            self.Tablet.padName = deviceNames['pad']
        # read in previous config file, if exists
        # old config file move/update code
        home = "%s/.wacom-gui.sh" % expanduser("~")
        path = "%s/.wacom-gui/%s" % (expanduser("~"), self.Tablet.devID)
        if os.path.exists(home) and os.access(home, os.X_OK):
            # check if for existing tablet, if it is move to its new home & rename
            if self.Tablet.Name in open(home).read():

                try:
                    shutil.copy(home, "%s/default.sh" % path)
                except IOError as e:
                    if e.errno != errno.ENOENT:
                        raise
                    distutils.dir_util.mkpath(path)
                    shutil.copy(home, "%s/default.sh" % path)
                    shutil.move(home, "%s.bak" % home)
        # check for updated config
        self.Tablet.config = "%s/.wacom-gui/%s/default.sh" % (expanduser("~"), self.Tablet.devID)
        if os.path.exists(self.Tablet.config) and os.access(self.Tablet.config, os.X_OK):
            os.system(self.Tablet.config)
        else:
            # create directory for config
            if not os.path.exists(path):
                distutils.dir_util.mkpath(path)
            label = "No previous config"
            w = QtGui.QMessageBox()
            QtGui.QMessageBox.warning(w, "Information", label)
            w.show()

        opPath = os.path.dirname(os.path.realpath(__file__)) 

        self.setWindowIcon(QtGui.QIcon(opPath + '/images/wacom-gui.svg'))
        self.TabletImg = opPath + "/images/" + self.Tablet.Model + ".png"
        self.TabletLayout = opPath + "/images/pad/" + self.Tablet.Model + ".png"

        self.pixmap = QtGui.QPixmap(self.TabletImg)
        pixmap2= QtGui.QPixmap(self.TabletLayout)

        self.tabletName = QtGui.QLabel(self.Tablet.Name)
        # if no 'pad' found, return None
        if self.Tablet.padName == '':
            return

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
            if (self.Tablet.Buttons[i].Callsign != 'AbsWheelUp' and self.Tablet.Buttons[i].Callsign != 'AbsWheelDown'):
                box = QtCore.QRectF(self.Tablet.Buttons[i].X1, self.Tablet.Buttons[i].Y1,
                                    self.Tablet.Buttons[i].X2, self.Tablet.Buttons[i].Y2)
                painter.drawRect(box)
                painter.drawText(box, QtCore.Qt.AlignCenter, self.Tablet.Buttons[i].Number)
        painter.end()
        self.tabletPad = QtGui.QLabel(self)
        self.tabletPad.setPixmap(pixmap2)
        self.icons = [QtGui.QPixmap("%s/images/enabled.png" % opPath),
                      QtGui.QPixmap("%s/images/disabled.png" % opPath)]
        self.padButtons = {}
        self.padButtonsLayout = QtGui.QGridLayout()
        self.buttonMapper = QtCore.QSignalMapper(self)
        for i in range(len(self.Tablet.Buttons)):
            buttonType = "Button "+self.Tablet.Buttons[i].Number
            if self.Tablet.Buttons[i].Callsign == 'AbsWheelUp' or self.Tablet.Buttons[i].Callsign == 'AbsWheelDown':
                buttonType = self.Tablet.Buttons[i].Callsign
            getCommand = os.popen("xsetwacom --get \"" + self.Tablet.padName + " pad\" " + buttonType).readlines()
            if str(getCommand).find("key") == -1 and str(getCommand).find("button") == -1:
                self.padButtons[(i, 0)] = QtGui.QLabel("UNDEFINED")
            elif getCommand[0] == "button +0 \n":
                self.padButtons[(i, 0)] = QtGui.QLabel("")
            else:    
                self.padButtons[(i, 0)] = QtGui.QLabel(self.wacomToHuman(getCommand[0]))
            self.padButtons[(i, 1)] = QtGui.QPushButton(self.Tablet.Buttons[i].Name)
            self.padButtons[(i, 1)].clicked[()].connect(self.buttonMapper.map)
            self.padButtons[(i, 2)] = self.Tablet.Buttons[i].Number
            # disable button
            if getCommand[0] == "button +0 \n":
                self.padButtons[(i, 3)] = ''
            else:
                self.padButtons[(i, 3)] = getCommand[0].rstrip('\n')
            self.padButtons[(i, 4)] = self.Tablet.Buttons[i].Callsign
            # align text
            self.padButtons[(i, 0)].setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignCenter)
            # disabled button
            self.padButtons[(i, 5)] = QtGui.QPushButton('')
            self.padButtons[(i, 5)].clicked[()].connect(self.buttonMapper.map)
            if self.padButtons[(i, 3)] == '':
                self.padButtons[(i, 1)].setEnabled(False)
                self.padButtons[(i, 5)].setIcon(QtGui.QIcon(self.icons[1]))
            else:
                self.padButtons[(i, 5)].setIcon(QtGui.QIcon(self.icons[0]))
            self.buttonMapper.setMapping(self.padButtons[(i, 1)], i)
            self.buttonMapper.setMapping(self.padButtons[(i, 5)], i + 50)
            self.padButtonsLayout.addWidget(self.padButtons[i, 0], i, 0)
            self.padButtonsLayout.setColumnMinimumWidth(0, 400)
            self.padButtonsLayout.addWidget(self.padButtons[i, 1], i, 1)
            self.padButtonsLayout.addWidget(self.padButtons[i, 5], i, 2)

        self.buttonMapper.mapped.connect(self.updatePadButton)
        # toggle sanity check
        swap = True
        for i in range(len(self.Tablet.Buttons)):
            if self.padButtons[(i, 1)].isEnabled():
                swap = False
                break
        if swap:
            self.buttonToggle.setText("Enable Buttons")
            self.buttonToggle.setIcon(QtGui.QIcon(self.icons[0]))
        else:
            self.buttonToggle.setIcon(QtGui.QIcon(self.icons[1]))
        loc = len(self.Tablet.Buttons) + 1
        self.padButtonsLayout.addWidget(self.buttonReset, loc, 1, 1, 2)
        self.padButtonsLayout.addWidget(self.buttonToggle, loc + 1, 1, 1, 2)
        self.vMaster = QtGui.QHBoxLayout()
        self.vMaster.addLayout(self.padButtonsLayout)
        self.vMaster.addWidget(self.tabletPad)


        self.setLayout(self.vMaster)

        # function to check what button has been pressed
        self.activeButton = None
        self.editButton = lambda: self.activeButton
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
            cmd = "xsetwacom --set \"%s pad\" " % self.Tablet.padName
            if self.padButtons[(i, 4)] == 'AbsWheelUp' or self.padButtons[(i, 4)] == 'AbsWheelDown':
                cmd += "%s " % self.padButtons[(i, 4)]
            else:
                cmd += "Button %s " % self.padButtons[(i, 2)]
            # check if enabled
            if self.padButtons[(i, 1)].isEnabled() == False:
                cmd += "button +0"
            else:
                if len(str(self.padButtons[(i, 3)])) == 0:
                    if 'Abs' in self.padButtons[(i, 4)]:
                        if 'Up' in self.padButtons[(i, 4)]:
                            cmd += "button +4"
                        elif 'Down' in self.padButtons[(i, 4)]:
                            cmd += "button +5"
                    else:
                        cmd += "button +%s" % self.padButtons[(i, 2)]
                else:
                    cmd += " \"%s\"" % str(self.padButtons[(i, 3)])
            buttons.append(cmd)
            # check if command is legit
            #if (i < 9 and len(str(self.padButtons[(i, 3)])) > 1) or \
            #        (i >= 9 and len(str(self.padButtons[(i, 3)])) > 2) or self.padButtons[(i, 3)] == 0:
            #    cmd = "xsetwacom --set \"" + self.Tablet.padName + " pad\" "
            #    if self.padButtons[(i, 4)] == 'AbsWheelUp' or self.padButtons[(i, 4)] == 'AbsWheelDown':
            #        cmd += self.padButtons[(i, 4)] + " "
            #    else:
            #        cmd += "Button " + self.padButtons[(i, 2)]
            #    if self.padButtons[(i, 3)] == 0:
            #        cmd += ' 0'
            #    else:
            #        cmd += " \"" + str(self.padButtons[(i, 3)]) + "\""
            #    buttons.append(cmd)
        return buttons


    #for pad buttons
    def updatePadButton(self, button):
        # enable/disable
        # herp!
        if button >= 50:
            if self.padButtons[(button - 50, 4)] == 'AbsWheelUp' or \
                    self.padButtons[(button - 50, 4)] == 'AbsWheelDown':
                buttonType = self.padButtons[(button - 50, 4)]
            else:
                buttonType = "Button " + self.padButtons[(button - 50, 2)]
            if self.padButtons[(button - 50, 1)].isEnabled():
                cmd = "xsetwacom --set \"%s pad\" %s 0" % (self.Tablet.padName, buttonType)
                setCommand = os.popen(cmd)
                self.padButtons[(button - 50, 5)].setIcon(QtGui.QIcon(self.icons[1]))
                self.padButtons[(button - 50, 1)].setEnabled(False)
                self.padButtons[(button - 50, 3)] = ''
                self.padButtons[(button - 50, 0)].setText('')
            else:
                cmd = "xsetwacom --set \"%s pad\" %s " % (self.Tablet.padName, buttonType)
                if 'Abs' in self.padButtons[(button - 50, 4)]:
                    if 'Up' in self.padButtons[(button - 50, 4)]:
                        cmd += "button +4"
                    elif 'Down' in self.padButtons[(button - 50, 4)]:
                        cmd += "button +5"
                else:
                    cmd += "button +%s" % self.padButtons[(button - 50, 2)]
                setCommand = os.popen(cmd)
                self.padButtons[(button - 50, 5)].setIcon(QtGui.QIcon(self.icons[0]))
                self.padButtons[(button - 50, 1)].setEnabled(True)
                self.padButtons[(button - 50, 3)] = 'button +%s' % self.padButtons[(button - 50, 2)]
                self.padButtons[(button - 50, 0)].setText('<DEFAULT>')
            return
        if self.activeButton is None:
            self.activeButton = self.padButtons[(button, 2)]
            self.padButtons[(button, 0)].setText("Recording keypresses... Click button to stop")
            self.buttonCommandList[:] = []
        elif self.activeButton == self.padButtons[(button, 2)]:
            tmp = 1
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
                    cmd = "xsetwacom --set \"%s pad\" %s %s" % (self.Tablet.padName, buttonType, str(userInput))
                else:
                    cmd = "xsetwacom --set \"%s pad\" %s \"%s\"" %(self.Tablet.padName, buttonType, str(userInput))
                setCommand = os.popen(cmd)
                self.padButtons[(button, 3)] = userInput

    def event(self, event):
        if (event.type() == QtCore.QEvent.ShortcutOverride and
                (event.key() == (QtCore.Qt.Key_Tab or QtCore.Qt.Key_Up or QtCore.Qt.Key_Down
                                 or QtCore.Qt.Key_Left or QtCore.Qt.Key_Right))) or \
                        event.type() == (QtCore.QEvent.KeyPress or QtCore.QEvent.MouseButtonPress or
                                             QtCore.QEvent.MouseButtonDblClick):
                tmp = 1
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
            if event.key() == (QtCore.Qt.Key_Shift or QtCore.Qt.Key_Alt or QtCore.Qt.Key_Control):
                self.buttonCommandList.append(self.keyTranslate(event.key(), event.text(), '-'))
            return False
        if event.type() == QtCore.QEvent.KeyPress and event.key() == QtCore.Qt.Key_Space:
            tmp = 1
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
                QtCore.Qt.Key_Space: keystate + 'Space',
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
        if re.match(r'^button \+\d+ \n', command):
            return "<DEFAULT>"
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
            elif item == "+Space":
                item = "SPACE"
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
            # only reset enabled buttons
            self.padButtons[(i, 1)].setEnabled(True)
            self.padButtons[(i, 5)].setIcon(QtGui.QIcon(self.icons[0]))
            if 'Abs' in self.padButtons[(i, 4)]:
                #touch wheel, do other stuff
                if 'Up' in self.padButtons[(i, 4)]:
                    bid = 4
                    self.padButtons[(i, 3)] = 'button +4'
                else:
                    bid = 5
                    self.padButtons[(i, 3)] = 'button +5'
                cmd = "xsetwacom --set \"%s pad\" %s %i" % (self.Tablet.padName, self.padButtons[(i, 4)], bid)
            else:
                bid = int(self.padButtons[(i, 2)])
                self.padButtons[(i, 3)] = 'button +%i' % bid
                cmd = "xsetwacom --set \"%s pad\" Button %i %i" % (self.Tablet.padName, bid, bid)
            setCommand = os.popen(cmd)
            self.padButtons[(i, 0)].setText("<DEFAULT>")


    def toggleButtons(self):
        for i in range(len(self.Tablet.Buttons)):
            if self.padButtons[(i, 4)] == 'AbsWheelUp' or \
                    self.padButtons[(i, 4)] == 'AbsWheelDown':
                buttonType = self.padButtons[(i, 4)]
            else:
                buttonType = "Button %s" % self.padButtons[(i, 2)]
            if 'Disable' in self.buttonToggle.text():
                if self.padButtons[(i, 1)].isEnabled():
                    cmd = "xsetwacom --set \"%s pad\" %s 0" % (self.Tablet.padName, buttonType)
                    setCommand = os.popen(cmd)
                    self.padButtons[(i, 5)].setIcon(QtGui.QIcon(self.icons[1]))
                    self.padButtons[(i, 1)].setEnabled(False)
                    self.padButtons[(i, 3)] = ''
                    self.padButtons[(i, 0)].setText('')
            if 'Enable' in self.buttonToggle.text():
                if self.padButtons[(i, 1)].isEnabled() is False:
                    cmd = "xsetwacom --set \"%s pad\" %s " % (self.Tablet.padName, buttonType)
                    if 'Abs' in self.padButtons[(i, 4)]:
                        if 'Up' in self.padButtons[(i, 4)]:
                            cmd += "button +4"
                        elif 'Down' in self.padButtons[(i, 4)]:
                            cmd += "button +5"
                    else:
                        cmd += "button +%s" % self.padButtons[(i, 2)]
                    setCommand = os.popen(cmd)
                    self.padButtons[(i, 5)].setIcon(QtGui.QIcon(self.icons[0]))
                    self.padButtons[(i, 1)].setEnabled(True)
                    self.padButtons[(i, 3)] = 'button +%s' % self.padButtons[(i, 2)]
                    self.padButtons[(i, 0)].setText('<DEFAULT>')
        if 'Disable' in self.buttonToggle.text():
            self.buttonToggle.setText("Enable Buttons")
            self.buttonToggle.setIcon(QtGui.QIcon(self.icons[0]))
        else:
            self.buttonToggle.setText("Disable Buttons")
            self.buttonToggle.setIcon(QtGui.QIcon(self.icons[1]))
