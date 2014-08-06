#!/usr/bin/python

#code repo: linuxproc.rhythm.com/src/systems/git/wacom-gui.git

#from PyQt4.QtGui import QWidget, QPolygonF, QPainter, QPen, QBrush, QColor, \
#    QApplication, QIcon, QVBoxLayout, QHBoxLayout, QPushButton, QPainterPath,\
#    QFont, QLayout, QGraphicsScene, QGraphicsView, QPixmap, QGraphicsPixmapItem, \
#    QTabletEvent, QLabel, QSplitter, QRadialGradient, QImage
#from PyQt4.QtCore import QObject, SIGNAL, SLOT, QPointF, Qt, QRectF, QPointF, QString, QRect
from PyQt4 import QtCore,QtGui
import time, sys, os

class pressureSettings(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setFixedSize(300,300)

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

        painter.fillRect(QtCore.QRectF(50,50,200,200),QtGui.QBrush(QtGui.QColor(QtGui.QColor(110,110,110))))
        painter.fillRect(QtCore.QRectF(50,50,200,200),QtGui.QBrush(QtCore.Qt.CrossPattern))

        painter.setPen(QtGui.QPen(QtGui.QColor(QtCore.Qt.lightGray), 2, QtCore.Qt.SolidLine))
        path = QtGui.QPainterPath()
        path.moveTo(50,250)
        path.cubicTo(self.points[0][0],self.points[0][1],self.points[1][0],self.points[1][1],250,50)
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
        curPressure = os.popen("xsetwacom --get " + self.sensor + " PressureCurve").readlines()
        self.setCommand = "xsetwacom --set " + self.sensor + " PressureCurve \"" + curPressure[0].rstrip('\n') + "\""

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
            self.setCommand = "xsetwacom --set " + self.sensor + " PressureCurve \"" + accuratePts + "\""
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
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setFixedSize(250,300)
        self.scene = QtGui.QGraphicsScene()
        self.scene.setBspTreeDepth(1)
        self.view = QtGui.QGraphicsView(self.scene)
        self.view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.info = pressureInfo()

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
        if self.sensor == "Stylus":
            senId = QtGui.QTabletEvent.Pen
        elif self.sensor == "Eraser":
            senId = QtGui.QTabletEvent.Eraser
        elif self.sensor == "Cursor":
            senId = QtGui.QTabletEvent.Cursor
        if event.pointerType() == senId:
            amp = int(event.pressure() * 50)
            color =  (1 - amp/50.0) * 255
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
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        row1 = QtGui.QHBoxLayout()
        row2 = QtGui.QHBoxLayout()
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
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setFixedSize(250, 100)

        self.buttons = QtGui.QCheckBox("Inverse Buttons")
        self.buttons.stateChanged.connect(self.buttonChange)
        #layout code
        self.mainLayout = QtGui.QVBoxLayout()
        self.mainLayout.addWidget(self.penSettings())
        self.mainLayout.addWidget(self.buttons)
        self.mainLayout.setAlignment(QtCore.Qt.AlignCenter)
        self.setLayout(self.mainLayout)
       
    def buttonChange(self):
        if self.buttons.isChecked():
            but1 = os.popen("xsetwacom --set Stylus Button 2 3")
            but2 = os.popen("xsetwacom --set Stylus Button 3 2")
        else:
            but1 = os.popen("xsetwacom --set Stylus Button 2 2")
            but2 = os.popen("xsetwacom --set Stylus Button 3 3")

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

        getCommand = os.popen("xsetwacom --get Stylus Mode").readlines()
        #check stylus mode
        if getCommand[0] == "Absolute\n":
            self.penMode = "xsetwacom --set Stylus mode Absolute" 
            self.penAbs.setChecked(1)
        elif getCommand[0] == "Relative\n":
            self.penMode = "xsetwacom --set Stylus mode Relative" 
            self.penRel.setChecked(1)
        #for buttons
        but1 = os.popen("xsetwacom --get Stylus Button 2").readlines()
        but2 = os.popen("xsetwacom --get Stylus Button 3").readlines()
        if but1[0].find('3') != -1 and but2[0].find('2') != -1:
            self.buttons.setChecked(True)

        self.penGroup.buttonClicked.connect(self.penChange)

        groupBox.setLayout(penLayout)

        return groupBox

    def penChange(self, buttonId):
        if buttonId.text() == "Absolute":
            self.penMode = "xsetwacom --set Stylus mode Absolute" 
        elif buttonId.text() == "Relative":
            self.penMode = "xsetwacom --set Stylus mode Relative" 
        flipTablet = os.popen(self.penMode)

    def getPenInfo(self):
        info = []
        but1 = os.popen("xsetwacom --get Stylus Button 2").readlines()
        but2 = os.popen("xsetwacom --get Stylus Button 3").readlines()
        info.append(self.penMode)
        info.append("xsetwacom --set Stylus Button 2 " + but1[0].rstrip('\n'))
        info.append("xsetwacom --set Stylus Button 3 " + but2[0].rstrip('\n'))
        return info

    def hideButtons(self):
        self.buttons.hide()

class pressure(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setFixedSize(650, 400)

        self.settings = pressureSettings()
        self.test = pressureTest()
        self.pen  = penOptions()

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

        if sensor != "Stylus":
            self.pen.hideButtons()

        curPressure = os.popen("xsetwacom --get Stylus PressureCurve").readlines()
        split = curPressure[0].split(' ')
        self.settings.setCurPoints([[int(split[0]),int(split[1])],[int(split[2]),int(split[3])]])

    def getSetCommand(self):
        return self.settings.getSetCommand()

    def getPenInfo(self):
        return self.pen.getPenInfo()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    form = pressure()
    form.setSensor("Stylus")
    #form.resize(650,300)
    form.show()
    sys.exit(app.exec_())
