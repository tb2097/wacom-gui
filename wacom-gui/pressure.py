#!/usr/bin/python

#from PyQt4.QtGui import QWidget, QPolygonF, QPainter, QPen, QBrush, QColor, \
#    QApplication, QIcon, QVBoxLayout, QHBoxLayout, QPushButton, QPainterPath,\
#    QFont, QLayout, QGraphicsScene, QGraphicsView, QPixmap, QGraphicsPixmapItem, \
#    QTabletEvent, QLabel, QSplitter, QRadialGradient, QImage
#from PyQt4.QtCore import QObject, SIGNAL, SLOT, QPointF, Qt, QRectF, QPointF, QString, QRect
from PyQt4 import QtCore,QtGui
import sys, os

class pressureSettings(QtGui.QWidget):
    def __init__(self, tabletName,parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setFixedSize(300,300)

        self.tabletName=tabletName
        mainLayout = QtGui.QHBoxLayout()
        mainLayout.setAlignment(QtCore.Qt.AlignLeft)
        self.setLayout(mainLayout)

        self.tracking = None
        self.sensor = None

        self.points = [[50, 250], [250, 50]]

        #self.setWindowTitle('Bonus Example')

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHints(QtGui.QPainter.Antialiasing)

        painter.fillRect(QtCore.QRectF(50, 50, 200, 200), QtGui.QBrush(QtGui.QColor(QtGui.QColor(110, 110, 110))))
        painter.fillRect(QtCore.QRectF(50, 50, 200, 200), QtGui.QBrush(QtCore.Qt.CrossPattern))

        painter.setPen(QtGui.QPen(QtGui.QColor(QtCore.Qt.lightGray), 2, QtCore.Qt.SolidLine))
        path = QtGui.QPainterPath()
        path.moveTo(50, 250)
        path.cubicTo(self.points[0][0], self.points[0][1], self.points[1][0], self.points[1][1], 250, 50)
        painter.drawPath(path)

        painter.setBrush(QtGui.QBrush(QtGui.QColor(QtCore.Qt.darkCyan)))
        painter.setPen(QtGui.QPen(QtGui.QColor(QtCore.Qt.lightGray), 1))


        #for x, y in pts:
        painter.drawEllipse(QtCore.QRectF(self.points[0][0] - 4, self.points[0][1] - 4, 8, 8))
        painter.drawEllipse(QtCore.QRectF(self.points[1][0] - 4, self.points[1][1] - 4, 8, 8))
        painter.setPen(QtGui.QPen(QtGui.QColor(QtCore.Qt.white), 1))
        label1 = "("+ str((self.points[0][0] - 50)/2) + "," + str(100 - ((self.points[0][1] -50)/2)) + ")"
        painter.drawText(self.points[0][0] -25, self.points[0][1] + 18, QtCore.QString(label1))
        label2 = "("+ str((self.points[1][0] - 50)/2) + "," + str(100 - ((self.points[1][1] -50)/2)) + ")"
        painter.drawText(self.points[1][0] -25, self.points[1][1] + 18, QtCore.QString(label2))

    def setSensor(self,sensor):
        self.sensor = sensor
        #print self.sensor
        curPressure = os.popen("xsetwacom --get \""+self.tabletName+" "+self.sensor + "\" PressureCurve").readlines()
        self.setCommand = "xsetwacom --set \""+self.tabletName+" "+self.sensor + "\" PressureCurve \"" + curPressure[0].rstrip('\n') + "\""

    #================================================================
    # And this one too
    # http://stackoverflow.com/a/3220819/736306
    def mousePressEvent(self, event):
        i = min(range(len(self.points)),
            key=lambda i: (event.x() - self.points[i][0]) ** 2 +
                      (event.y() - self.points[i][1]) ** 2)
        #print "X: " + str(event.x()) + "          Y: " + str(event.y())
        #print points

        self.tracking = lambda p: self.points.__setitem__(i, p)

    def mouseMoveEvent(self, event):
       if self.tracking:
            #print "X point: " + str(event.x()) + "    Y point: " + str(event.y())
            x = event.x()
            y = event.y()
            if event.x() < 50:
                x = 50
            elif event.x() > 250: 
                x = 250    
            if event.y() < 50:
                y = 50
            elif event.y() > 250: 
                y = 250

            self.tracking([x, y])
            self.update()

    def mouseReleaseEvent(self, event):
        self.tracking = None
        if self.sensor == None:
            print "Need device to be set"
        else:
            accuratePts = str((self.points[0][0] - 50)/2) + " " + str(100 - ((self.points[0][1] -50)/2)) + \
            " " + str((self.points[1][0] - 50)/2) + " " + str(100 - ((self.points[1][1] -50)/2))  
            self.setCommand = "xsetwacom --set \""+self.tabletName+" "+self.sensor.lower() + "\" PressureCurve \"" + accuratePts + "\""
            os.system(self.setCommand)

    def getSetCommand(self):
        if self.setCommand != None:
            return self.setCommand
    
    def setCurPoints(self,pressure):
        self.points[0][0] = (2 * pressure[0][0]) + 50
        self.points[0][1] = 250 - (2 * pressure[0][1])
        self.points[1][0] = (2 * pressure[1][0]) + 50
        self.points[1][1] = 250 - (2 * pressure[1][1])



#================================================================================================
#================================================================================================

class pressureTest(QtGui.QWidget):
    def __init__(self, tabletName,parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setFixedSize(250,300)
        self.scene = QtGui.QGraphicsScene()
        self.scene.setBspTreeDepth(1)
        self.view = QtGui.QGraphicsView(self.scene)
        self.view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tabletName=tabletName
        self.info = pressureInfo(self.tabletName)

        splitter = QtGui.QSplitter(QtCore.Qt.Vertical)
        splitter.addWidget(self.view)
        splitter.addWidget(self.info)
        splitter.setSizes([200,50])
        splitter.handle(0).setEnabled(False)
        splitter.handle(1).setEnabled(False)
        #print splitter.count()

        testLayout = QtGui.QVBoxLayout()
        testLayout.setAlignment(QtCore.Qt.AlignBottom)
        testLayout.addWidget(splitter)
        self.setLayout(testLayout)
        self.blank = QtGui.QPixmap(250,250)
        self.blank.fill(QtCore.Qt.white)
        self.pixmap_item = QtGui.QGraphicsPixmapItem(self.blank, None, self.scene)

    def tabletEvent(self,event):
        senId = ""
        if self.sensor == "stylus" :
            senId = QtGui.QTabletEvent.Pen
        elif self.sensor == "eraser":
            senId = QtGui.QTabletEvent.Eraser
        elif self.sensor == "cursor":
            senId = QtGui.QTabletEvent.Cursor
        if event.pointerType() == senId:
            curpressure = event.pressure()
            if curpressure < 0:
                curpressure += 1
            amp = int(curpressure * 50)
            color = (1 - amp/50.0) * 255
            pen = QtGui.QPen(QtGui.QColor(color,color,color,0))

            radial = QtGui.QRadialGradient(QtCore.QPointF(event.x(),event.y()),amp,QtCore.QPointF(event.xTilt() * amp/50 ,event.yTilt() * amp))
            radial.setColorAt(0,QtGui.QColor(color,color,color,255))
            radial.setColorAt(1,QtGui.QColor(color,color,color,0))
            brush = QtGui.QBrush(radial)
            if(amp >= 1):
                if len(self.scene.items()) >= 50:
                    render = QtGui.QPixmap(250,250)
                    painter = QtGui.QPainter(render)
                    rect = QtCore.QRectF(0,0,250,250)
                    self.scene.render(painter,rect,rect,QtCore.Qt.KeepAspectRatio)
                    self.scene.clear()
                    self.scene.addPixmap(render)
                    painter.end()
                self.scene.addEllipse(event.x() - amp, event.y() -amp, amp, amp, pen, brush)
            self.info.updateInfo(event.xTilt(),event.yTilt(),amp)


    def setSensor(self,sensor):
        self.sensor = sensor

#================================================================================================
#================================================================================================

class pressureInfo(QtGui.QWidget):
    def __init__(self, tabletName, parent=None):
        QtGui.QWidget.__init__(self, parent)
        row1 = QtGui.QHBoxLayout()
        row2 = QtGui.QHBoxLayout()
        self.tabletName=tabletName
        self.xTilt = QtGui.QLabel("XTilt: 0.0")
        self.yTilt = QtGui.QLabel("YTilt: 0.0")
        self.amp = QtGui.QLabel("Amplitude: 0")
        self.sensor = ""


        row1.addWidget(self.xTilt,0,QtCore.Qt.AlignLeft)
        row1.addWidget(self.yTilt,0,QtCore.Qt.AlignLeft)
        row2.addWidget(self.amp,0,QtCore.Qt.AlignHCenter)
        layout = QtGui.QVBoxLayout()
        layout.addLayout(row1)
        layout.addLayout(row2)
        self.setLayout(layout)

    def updateInfo(self,x,y,amp):
        self.xTilt.setText("xTilt: " + str(x))
        self.yTilt.setText("yTilt: " + str(y))
        self.amp.setText("Amplitude: " + str(amp))

class penOptions(QtGui.QWidget):
    def __init__(self, tabletName, sensor, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setFixedSize(250, 120)

        self.tabletName = tabletName
        self.sensor = sensor
        self.buttons = QtGui.QCheckBox("Inverse Buttons")
        self.buttons.stateChanged.connect(self.buttonChange)
        self.tiptouch = QtGui.QCheckBox("Pen Touch")
        self.tiptouch.setToolTip("When enabled, pen must touch tablet to work.\nWhen disabled, hover will register.")
        self.tiptouch.stateChanged.connect(self.tipChange)
        #layout code
        self.mainLayout = QtGui.QVBoxLayout()
        self.mainLayout.addWidget(self.penSettings())
        self.mainLayout.addWidget(self.buttons)
        self.mainLayout.addWidget(self.tiptouch)
        self.mainLayout.setAlignment(QtCore.Qt.AlignCenter)
        self.setLayout(self.mainLayout)
       
    def buttonChange(self):
        if self.buttons.isChecked():
            but1 = os.popen("xsetwacom --set \"%s %s\" Button 2 3" % (self.tabletName, self.sensor.lower()))
            but2 = os.popen("xsetwacom --set \"%s %s\" Button 3 2" % (self.tabletName, self.sensor.lower()))
        else:
            but1 = os.popen("xsetwacom --set \"%s %s\" Button 2 2" % (self.tabletName, self.sensor.lower()))
            but2 = os.popen("xsetwacom --set \"%s %s\" Button 3 3" % (self.tabletName, self.sensor.lower()))

    def tipChange(self):
        if self.tiptouch.isChecked():
            but1 = os.popen("xsetwacom --set \"%s %s\" TabletPCButton on" % (self.tabletName, self.sensor.lower()))
        else:
            but1 = os.popen("xsetwacom --set \"%s %s\" TabletPCButton off" % (self.tabletName, self.sensor.lower()))

    def penSettings(self):
        groupBox = QtGui.QGroupBox("Mode")
        groupBox.setAlignment(QtCore.Qt.AlignCenter)
        self.penGroup = QtGui.QButtonGroup(groupBox)
        self.penAbs = QtGui.QRadioButton("Absolute")
        self.penRel = QtGui.QRadioButton("Relative")
        
        self.penGroup.addButton(self.penAbs)
        self.penGroup.addButton(self.penRel)
        
        penLayout = QtGui.QHBoxLayout()
        penLayout.addWidget(self.penAbs)
        penLayout.addWidget(self.penRel)
        penLayout.addStretch(1)

        if self.sensor == 'stylus' or self.sensor == 'eraser':
            getCommand = os.popen("xsetwacom --get \"%s %s\" Mode" % (self.tabletName, self.sensor.lower())).readlines()
            #check stylus mode
            if getCommand[0] == "Absolute\n":
                self.penMode = "xsetwacom --set \"%s %s\" mode Absolute" % (self.tabletName, self.sensor.lower())
                self.penAbs.setChecked(1)
            elif getCommand[0] == "Relative\n":
                self.penMode = "xsetwacom --set \"%s %s\" mode Relative" % (self.tabletName, self.sensor.lower())
                self.penRel.setChecked(1)
        if self.sensor == 'stylus':
            #for buttons
            but1 = os.popen(("xsetwacom --get \"%s %s\" Button 2") % (self.tabletName, self.sensor.lower())).readlines()
            but2 = os.popen(("xsetwacom --get \"%s %s\" Button 3") % (self.tabletName, self.sensor.lower())).readlines()
            if but1[0].find('3') != -1 and but2[0].find('2') != -1:
                self.buttons.setChecked(True)
            #for tip touch check
            tip = os.popen("xsetwacom --get \"%s %s\" TabletPCButton" % (self.tabletName, self.sensor.lower())).readlines()
            if tip[0].find('on') != -1:
                self.tiptouch.setChecked(True)
        else:
            self.tiptouch.hide()

        self.penGroup.buttonClicked.connect(self.penChange)

        groupBox.setLayout(penLayout)

        return groupBox

    def penChange(self, buttonId):
        if buttonId.text() == "Absolute":
            self.penMode = "xsetwacom --set \"%s %s\" mode Absolute" % (self.tabletName, self.sensor.lower())
        elif buttonId.text() == "Relative":
            self.penMode = "xsetwacom --set \"%s %s\" mode Relative" % (self.tabletName, self.sensor.lower())
        flipTablet = os.popen(self.penMode)

    def getPenInfo(self):
        info = []
        but1 = os.popen("xsetwacom --get \""+self.tabletName+" stylus\" Button 2").readlines()
        but2 = os.popen("xsetwacom --get \""+self.tabletName+" stylus\" Button 3").readlines()
        tip = os.popen("xsetwacom --get \"" + self.tabletName + " stylus\" TabletPCButton").readlines()
        info.append(self.penMode)
        info.append("xsetwacom --set \""+self.tabletName+" stylus\" Button 2 " + but1[0].rstrip('\n'))
        info.append("xsetwacom --set \""+self.tabletName+" stylus\" Button 3 " + but2[0].rstrip('\n'))
        info.append("xsetwacom --set \"" + self.tabletName + " stylus\" TabletPCButton " + tip[0].rstrip('\n'))
        return info

    def hideButtons(self):
        self.buttons.hide()

class pressure(QtGui.QWidget):
    def __init__(self, name, sensor, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setFixedSize(650, 400)

        self.tabletName = name
        self.sensor = sensor
        self.settings = pressureSettings(self.tabletName)
        self.test = pressureTest(self.tabletName)
        self.pen = penOptions(self.tabletName, sensor)

        #vbox = QtGui.QVBoxLayout()
        #vbox.addWidget(self.settings)
        #vbox.addWidget(self.pen)
        #hbox = QtGui.QHBoxLayout()
        #hbox.setAlignment(QtCore.Qt.AlignTop)
        #hbox.addLayout(vbox)
        #hbox.addWidget(self.test)

        grid = QtGui.QGridLayout()
        grid.addWidget(self.settings,0,0)
        grid.addWidget(self.test,0,1)
        grid.addWidget(self.pen,1,0)

        self.setLayout(grid)

    def setSensor(self,sensor):
        self.settings.setSensor(sensor)
        self.test.setSensor(sensor)

        if sensor != "stylus":
            self.pen.hideButtons()

        curPressure = os.popen("xsetwacom --get \""+self.tabletName+" stylus\" PressureCurve").readlines()
        split = curPressure[0].split(' ')
        self.settings.setCurPoints([[int(split[0]),int(split[1])],[int(split[2]),int(split[3])]])

    def getSetCommand(self):
        return self.settings.getSetCommand()

    def getPenInfo(self):
        return self.pen.getPenInfo()

    def resetDefaults(self):
        # set device to absolute mode
        self.pen.penMode = "xsetwacom --set \"%s %s\" mode Absolute" % (self.tabletName, self.sensor.lower())
        self.pen.penAbs.setChecked(True)
        os.popen(self.pen.penMode)
        if self.sensor.lower() != 'cursor':
            # set pressure curve points
            self.settings.setCurPoints([[0, 0], [100, 100]])
            self.settings.setCommand = "xsetwacom --set \"%s %s\" PressureCurve 0 0 100 100" % (
            self.tabletName, self.sensor.lower())
            os.popen(self.settings.setCommand)
        if self.sensor.lower() == 'stylus':
            # disable tip touch; allows hover
            self.pen.tiptouch.setChecked(False)
            cmd = "xsetwacom --get \"%s %s\" TabletPCButton off" % (self.tabletName, self.sensor.lower())
            os.popen(cmd)
            # set pen buttons to default
            self.pen.buttons.setChecked(False)
            cmd = "xsetwacom --set \"%s %s\" Button 2 2" % (self.tabletName, self.sensor.lower())
            os.popen(cmd)
            cmd = "xsetwacom --set \"%s %s\" Button 3 3" % (self.tabletName, self.sensor.lower())
            os.popen(cmd)




        tmp = 1

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    form = pressure()
    form.setSensor("stylus")
    #form.resize(650,300)
    form.show()
    sys.exit(app.exec_())
