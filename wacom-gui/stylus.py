#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtSvg import *
from hotkeys import HotkeyWidget
import stylus_ui
import os
import subprocess
import re

# 880, 560

class Stylus(QTabWidget, stylus_ui.Ui_StylusWidget):
    def __init__(self, parent = None):
        super(Stylus, self).__init__(parent)
        self.setupUi(self)
        self.cwd = os.path.dirname(os.path.abspath(__file__))
        self.setFocusPolicy(Qt.NoFocus)
        # put pen images in GUI
        self.penImage.setPixmap(QPixmap(os.path.join(self.cwd, "icons/ui/stylus_pen.png")))
        self.penImage.setScaledContents(True)
        self.eraserImage.setPixmap(QPixmap(os.path.join(self.cwd,"icons/ui/stylus_eraser.png")))
        self.eraserImage.setScaledContents(True)
        self.button1 = None
        self.button2 = None
        self.button3 = None
        self.pen_id = None
        self.penPressure = None
        self.penThreshold = None
        self.penTaptime = None
        self.penRawsample = None
        self.penSuppress = None
        self.penTabletPC = QCheckBox("TabletPCButton")
        self.penTabletPC.setToolTip("When enabled, pen must touch screen for the stylus to work.")
        self.penTabletPC.stateChanged.connect(self.updateTabletPC)
        self.eraserPressure = None
        self.eraserThreshold = None
        self.eraserTaptime = None
        self.eraserRawsample = None
        self.eraserSuppress = None
        self.mapping = Mapping()
        self.mappingImage.setPixmap(QPixmap(os.path.join(self.cwd, "icons/ui/mapping.png")))
        self.penImage.setScaledContents(True)
        self.mappingToolRight.addWidget(self.mapping)
        self.penDefault.clicked.connect(self.resetPen)
        self.eraserDefault.clicked.connect(self.resetEraser)
        self.mappingDefault.clicked.connect(self.mapping.resetMapping)

    def init_pen(self, dev_id, pen):
        self.pen_id = dev_id
        self.deleteItemsOfLayout(self.penToolLeft.layout())
        self.deleteItemsOfLayout(self.penToolRight.layout())
    # TODO: button stuff
    # TODO: mapping stuff
        if 'pressurecurve' in pen.keys():
            self.penPressure = WacomPressure(dev_id, pen['pressurecurve'])
        else:
            self.penPressure = WacomPressure(dev_id)
        self.penPressure.setToolTip("Set pressure curve for input pressure.\n"
                                       "It is composed of two anchor points (0,0 and 100,100)")
        self.penPressure.gauge.installEventFilter(self)
        if 'threshold' in pen.keys():
            self.penThreshold = WacomAttribSlider(dev_id, 'threshold', 26, "Threshold", 0, 2047, 50,
                                                  int(pen['threshold']))
        else:
            self.penThreshold = WacomAttribSlider(dev_id, 'threshold', 26, "Threshold", 0, 2047, 50)
        self.penThreshold.setToolTip("Set  the  minimum  pressure  necessary to generate a Button event\n"
                                     "for the stylus tip, eraser, or touch.")
        if 'taptime' in pen.keys():
            self.penTaptime = WacomAttribSlider(dev_id, 'taptime', 250, "Double Tap Time (ms)", 0, 500, 25,
                                                int(pen['taptime']))
        else:
            self.penTaptime = WacomAttribSlider(dev_id, 'taptime', 250, "Double Tape Time (ms)", 0, 500, 25)
        self.penTaptime.setToolTip("Time between taps in ms that will register as a double time")
        if 'rawsample' in pen.keys():
            self.penRawsample = WacomAttribSlider(dev_id, 'rawsample', 4, "Sample Size", 1, 20, 4,
                                                  int(pen['rawsample']))
        else:
            self.penRawsample = WacomAttribSlider(dev_id, 'rawsample', 4, "Sample Size", 1, 20, 4)
        self.penRawsample.setToolTip("Set the sample window size (a sliding average sampling window) for\n"
                                     "incoming input tool raw data points.")
        if 'suppress' in pen.keys():
            self.penSuppress = WacomAttribSlider(dev_id, 'suppress', 2, "Tilt Sensitivity", 0, 100, 10,
                                                  int(pen['suppress']))
        else:
            self.penSuppress = WacomAttribSlider(dev_id, 'suppress', 2, "Tilt Sensitivity", 0, 100, 10)
        self.penSuppress.setToolTip("Set the delta (difference) cutoff level for further processing of\n"
                                    "incoming input tool coordinate values.")

        if 'buttons' in pen.keys():
            if 'Button2' in pen['buttons']:
                self.button2 = HotkeyWidget(dev_id, 'Button2', 'Button 2', pen['buttons']['Button2'])
            else:
                self.button2 = HotkeyWidget(dev_id, 'Button2', 'Button 2', 'Default')
            if 'Button3' in pen['buttons']:
                self.button3 = HotkeyWidget(dev_id, 'Button3', 'Button 3', pen['buttons']['Button3'])
            else:
                self.button3 = HotkeyWidget(dev_id, 'Button3', 'Button 3', 'Default')

        self.penToolLeft.addWidget(self.penPressure)
        self.penToolLeft.addWidget(self.penThreshold)
        self.penToolLeft.addWidget(self.penTaptime)
        self.penToolLeft.addWidget(self.penRawsample)
        spacer = QSpacerItem(20, 200, QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.penToolRight.addWidget(self.button3)
        self.penToolRight.addWidget(self.button2)
        self.penToolRight.addItem(spacer)
        self.penToolRight.addWidget(self.penSuppress)
        self.penToolRight.addWidget(self.penTabletPC)

    def init_eraser(self, dev_id, eraser):
        self.deleteItemsOfLayout(self.eraserToolLeft.layout())
        self.deleteItemsOfLayout(self.eraserToolRight.layout())
        if 'pressurecurve' in eraser.keys():
            self.eraserPressure = WacomPressure(dev_id, eraser['pressurecurve'])
        else:
            self.eraserPressure = WacomPressure(dev_id)
        self.eraserPressure.gauge.installEventFilter(self)
        self.eraserPressure.setToolTip("Set pressure curve for input pressure.\n"
                                       "It is composed of two anchor points (0,0 and 100,100)")
        if 'threshold' in eraser.keys():
            self.eraserThreshold = WacomAttribSlider(dev_id, 'threshold', 26, "Threshold", 0, 2047, 50,
                                                  int(eraser['threshold']))
        else:
            self.eraserThreshold = WacomAttribSlider(dev_id, 'threshold', 26, "Threshold", 0, 2047, 50)
        self.eraserThreshold.setToolTip("Set  the  minimum  pressure  necessary to generate a Button event\n"
                                     "for the stylus tip, eraser, or touch.")
        if 'taptime' in eraser.keys():
            self.eraserTaptime = WacomAttribSlider(dev_id, 'taptime', 250, "Double Tap Time (ms)", 0, 500, 25,
                                                int(eraser['taptime']))
        else:
            self.eraserTaptime = WacomAttribSlider(dev_id, 'taptime', 250, "Double Tap Time (ms)", 0, 500, 25)
        self.eraserTaptime.setToolTip("Time between taps in ms that will register as a double time")
        if 'rawsample' in eraser.keys():
            self.eraserRawsample = WacomAttribSlider(dev_id, 'rawsample', 4, "Sample Size", 1, 20, 4,
                                                  int(eraser['rawsample']))
        else:
            self.eraserRawsample = WacomAttribSlider(dev_id, 'rawsample', 4, "Sample Size", 1, 20, 4)
        self.eraserRawsample.setToolTip("Set the sample window size (a sliding average sampling window) for\n"
                                     "incoming input tool raw data points.")
        if 'suppress' in eraser.keys():
            self.eraserSuppress = WacomAttribSlider(dev_id, 'suppress', 2, "Tilt Sensitivity", 0, 100, 10,
                                                  int(eraser['suppress']))
        else:
            self.eraserSuppress = WacomAttribSlider(dev_id, 'suppress', 2, "Tilt Sensitivity", 0, 100, 10)
        self.eraserSuppress.setToolTip("Set the delta (difference) cutoff level for further processing of\n"
                                    "incoming input tool coordinate values.")
        if 'buttons' in eraser.keys():
            if 'Button1' in eraser['buttons']:
                self.button1 = HotkeyWidget(dev_id, 'Button1', 'Button 1', eraser['buttons']['Button1'])
            else:
                self.button1 = HotkeyWidget(dev_id, 'Button1', 'Button 1', 'Default')

        self.eraserToolLeft.addWidget(self.eraserPressure)
        self.eraserToolLeft.addWidget(self.eraserThreshold)
        self.eraserToolLeft.addWidget(self.eraserTaptime)
        self.eraserToolLeft.addWidget(self.eraserRawsample)
        spacer = QSpacerItem(20, 200, QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.eraserToolRight.addWidget(self.button1)
        self.eraserToolRight.addItem(spacer)
        self.eraserToolRight.addWidget(self.eraserSuppress)

    def updateTabletPC(self):
        if self.penTabletPC.isChecked():
            cmd = "xsetwacom --set %s TabletPCButton on" % self.pen_id
            os.popen(cmd)
            return ('tabletpcbutton', 'on')
        else:
            cmd = "xsetwacom --set %s TabletPCButton off" % self.pen_id
            os.popen(cmd)
            return ('tabletpcbutton', 'off')

    def deleteItemsOfLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    self.deleteItemsOfLayout(item.layout())

    def boxdelete(self, box):
        for i in range(self.keys.count()):
            layout_item = self.keys.itemAt(i)
            if layout_item.layout() == box:
                self.deleteItemsOfLayout(layout_item.layout())
                self.vlayout.removeItem(layout_item)
                break

    def resetPen(self):
        self.button2.reset()
        self.button3.reset()
        self.penPressure.set_defaults()
        self.penThreshold.set_defaults()
        self.penTaptime.set_defaults()
        self.penRawsample.set_defaults()
        self.penSuppress.set_defaults()
        self.penTabletPC.setChecked(False)
        self.updateTabletPC()

    def resetEraser(self):
        self.button1.reset()
        self.eraserPressure.set_defaults()
        self.eraserThreshold.set_defaults()
        self.eraserTaptime.set_defaults()
        self.eraserRawsample.set_defaults()
        self.eraserSuppress.set_defaults()

    #def eventFilter(self, source, event):
    #    print (f"Event ID: {event.type()}")
    #    if event.type() == QTabletEvent.Type.TabletPress:
    #        print (f"Event ID: {event.pointerType()}")
    def tabletEvent(self, event: QTabletEvent):
        if event.type() in [QTabletEvent.TabletMove]:
            if event.pointerType() == 1:
                self.penPressure.update_gauge(event.pressure())
            elif event.pointerType() == 3:
                self.eraserPressure.update_gauge(event.pressure())

    def get_config(self):
        data = {'stylus': {'buttons': {}}, 'eraser': {'buttons': {}}}
        data['stylus']['pressurecurve'] = self.penPressure.setting
        (attr, value) = self.penSuppress.get_setting()
        data['stylus'][attr] = str(value)
        (attr, value) = self.penSuppress.get_setting()
        data['stylus'][attr] = str(value)
        (attr, value) = self.penRawsample.get_setting()
        data['stylus'][attr] = str(value)
        (attr, value) = self.penThreshold.get_setting()
        data['stylus'][attr] = str(value)
        (attr, value) = self.penTaptime.get_setting()
        data['stylus'][attr] = str(value)
        data['stylus']['mapping'] = self.mapping.settings
        (attr, value) = self.updateTabletPC()
        data['stylus'][attr] = str(value)
        data['eraser']['pressurecurve'] = self.eraserPressure.setting
        (attr, value) = self.eraserSuppress.get_setting()
        data['eraser'][attr] = str(value)
        (attr, value) = self.eraserRawsample.get_setting()
        data['eraser'][attr] = str(value)
        (attr, value) = self.eraserThreshold.get_setting()
        data['eraser'][attr] = str(value)
        (attr, value) = self.eraserTaptime.get_setting()
        data['eraser'][attr] = str(value)
        # buttons
        info = list(self.button1.button.get_button_cmd())
        if info[2] == '1':
            data['eraser']['buttons'][info[0]] = 'Default'
        else:
            data['eraser']['buttons'][info[0]] = info[2]
        info = list(self.button2.button.get_button_cmd())
        if info[2] == '2':
            data['stylus']['buttons'][info[0]] = 'Default'
        else:
            data['stylus']['buttons'][info[0]] = info[2]
        info = list(self.button3.button.get_button_cmd())
        if info[2] == '3':
            data['stylus']['buttons'][info[0]] = 'Default'
        else:
            data['stylus']['buttons'][info[0]] = info[2]
        return data

class WacomAttribSlider(QWidget):
    def __init__(self, dev_id, attr, default, label, x, y, ticks=1, setting=None, x_label=None, y_label=None):
        QWidget.__init__(self, None)
        self.dev_id = dev_id
        self.attr = attr
        self.default = default
        self.group = QGroupBox(label)
        self.group.setFixedSize(290, 80)
        self.group.setAlignment(Qt.AlignTop)
        self.min = None
        self.max = None
        self.slider = QSlider(Qt.Horizontal)
        # self.slider.setFocusPolicy(Qt.NoFocus)
        self.slider.setMinimum(x)
        self.slider.setMaximum(y)
        self.slider.setFixedSize(260, 16)
        if setting is not None:
            self.slider.setValue(setting)
        else:
            self.slider.setValue(self.default)
        self.slider.setTickInterval(ticks)
        self.slider.setTickPosition(self.slider.TicksBelow)
        self.value = QLabel(str(self.slider.value()))
        self.value.setStyleSheet("QLabel { "
                                 "font-weight: bold; color: #6DD7E8; "
                                 "background-color: #444444; "
                                 "padding-left: 1px; "
                                 "padding-right: 1px;}")
        self.value.setAlignment(Qt.AlignRight)
        self.value.setFixedSize(46, 14)
        if x_label is not None:
            self.min = QLabel(str(x_label))
        else:
            self.min = QLabel(str(x))
        if y_label is not None:
            self.max = QLabel(str(y_label))
        else:
            self.max = QLabel(str(y))
        self.min.setFixedSize(40, 14)
        self.max.setFixedSize(40, 14)
        self.min.setAlignment(Qt.AlignRight)
        self.spread = QSpacerItem(240, 14, QSizePolicy.Fixed, QSizePolicy.Fixed)

        grid = QGridLayout()
        grid.addWidget(self.value, 0, 1, 1, 1, Qt.AlignRight)
        grid.addWidget(self.slider, 1, 0, 1, 3, Qt.AlignHCenter)
        grid.addWidget(self.min, 2, 0, 1, 1, Qt.AlignRight)
        grid.addItem(self.spread, 2, 1, 1, 1)
        grid.addWidget(self.max, 2, 2, 1, 1, Qt.AlignLeft)
        self.group.setLayout(grid)
        layout = QHBoxLayout()
        layout.addWidget(self.group)
        self.setLayout(layout)

        self.slider.valueChanged.connect(self.update_label)
        self.slider.sliderReleased.connect(self.update_setting)
        self.update_setting()

    def update_label(self):
        self.value.setText(str(self.slider.value()))

    def update_setting(self):
        cmd = "xsetwacom --set %s %s %s" % (self.dev_id, self.attr, self.value.text())
        os.popen(cmd)

    def get_setting(self):
       return self.attr, self.slider.value()

    def set_defaults(self):
        self.value.setText(str(self.default))
        self.slider.setValue(self.default)

class WacomPressure(QWidget):
    def __init__(self, dev_id, setting=None):
        QWidget.__init__(self, None)
        self.dev_id = dev_id
        self.attr = 'pressurecurve'
        self.defaults = [[0, 100, 0, 100],
                         [0, 75, 25, 100],
                         [0, 50, 50, 100],
                         [0, 25, 75, 100],
                         [0, 0, 100, 100],
                         [25, 0, 100, 75],
                         [50, 0, 100, 50],
                         [75, 0, 100, 25],
                         [100, 0, 100, 0]]
        self.setting = [0, 0, 100,  100]
        if setting is not None:
            #values = setting.split(' ')
            self.setting = setting
            #for value in values:
            #    self.setting.append(int(value))
        group = QGroupBox('Tip Feel')
        # Testing fixing boarders
        group.setFixedSize(290, 148)
        group.setAlignment(Qt.AlignTop)
        self.gauge = QProgressBar()
        self.gauge.setRange(0, 1000)
        self.gauge.setValue(0)
        self.gauge.setFixedSize(260, 18)
        self.min = QLabel("Soft")
        self.max = QLabel("Firm")
        self.min.setFixedSize(40, 14)
        self.max.setFixedSize(40, 14)
        self.slider = QSlider(Qt.Horizontal)
        # self.slider.setFocusPolicy(Qt.NoFocus)
        self.slider.setMinimum(0)
        self.slider.setMaximum(8)
        self.slider.setFixedSize(260, 16)
        if self.defaults.index(self.setting) != -1:
            self.slider.setValue(self.defaults.index(self.setting))
        else:
            # TODO: allow custom values
            self.slider.setValue(0)
        self.slider.setTickInterval(1)
        self.slider.setTickPosition(self.slider.TicksBelow)
        self.value = QLabel("[%s]" % ",".join(str(i) for i in self.setting))
        self.value.setStyleSheet("QLabel { font-weight: bold; color: #6DD7E8; "
                                 "background-color: #444444; padding-left: 1px; "
                                 "padding-right: 1px;}"
                                 "QProgressBar {border: 1px solid black;"
                                 "text-align: top;"
                                 "padding: 1px;"
                                 "border-radius: 2px;"
                                 "background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1,"
                                 "stop: 0 #fff,stop: 0.4999 #eee,stop: 0.5 #ddd,stop: 1 #eee );"
                                 "width: 15px;}"
                                 "QProgressBar::chunk {"
                                 "background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1,"
                                 "stop: 0 #a2e7f2,stop: 0.4999 #6DD7E8,stop: 0.5 #58aebc,stop: 1 #213f44 );"
                                 "border-radius: 1px;"
                                 "border: 1px solid black;"
                                 "}")
        self.value.setAlignment(Qt.AlignRight)
        self.value.setFixedSize(144, 14)
        self.min.setAlignment(Qt.AlignRight)
        self.spread = QSpacerItem(240, 14, QSizePolicy.Fixed, QSizePolicy.Fixed)

        grid = QGridLayout()
        grid.addWidget(self.value, 0, 1, 1, 1, Qt.AlignRight)
        grid.addWidget(self.slider, 1, 0, 1, 3, Qt.AlignHCenter)
        grid.addWidget(self.min, 2, 0, 1, 1, Qt.AlignRight)
        grid.addItem(self.spread, 2, 1, 1, 1)
        grid.addWidget(self.max, 2, 2, 1, 1, Qt.AlignLeft)
        grid.addWidget(self.gauge, 3, 0, 1, 3, Qt.AlignHCenter)
        group.setLayout(grid)
        layout = QHBoxLayout()
        layout.addWidget(group)
        self.setLayout(layout)

        self.slider.valueChanged.connect(self.update_label)
        self.slider.sliderReleased.connect(self.update_setting)
        self.update_setting()

    def update_label(self):
        self.value.setText("[%s]" % ','.join(str(i) for i in self.defaults[self.slider.value()]))

    def update_setting(self):
        cmd = "xsetwacom --set %s %s %s" % (self.dev_id, self.attr, self.value.text()[1:-1].replace(',', ' '))
        os.popen(cmd)

    def get_setting(self):
       return self.attr, self.slider.value()

    def set_defaults(self):
        self.setting = self.defaults[4]
        self.value.setText("[%s]" % ",".join(str(i) for i in self.setting))
        self.slider.setValue(4)

    def update_gauge(self, val):
        self.gauge.setValue(int(val * 1000))

class Mapping(QWidget):
    def __init__(self):
        QWidget.__init__(self, None)
        # TODO: orient, mode, screen, forced proportions, tablet area
        # TODO: return values function
        self.sid = None
        self.eid = None
        self.cid = None
        self.settings = {}
        self.displays = None
        self.main = QVBoxLayout()
        self.lorient = QHBoxLayout()
        self.orient = QComboBox()
        self.orient.addItems(['ExpressKeys Left', 'ExpressKeys Right', 'ExpressKeys Up', 'ExpressKeys Down'])
        self.orient.currentIndexChanged.connect(self.update_orient)
        self.orient_lbl = QLabel("Orientation:")
        self.lorient.addWidget(self.orient_lbl)
        self.lorient.addWidget(self.orient)
        self.mode_group = QButtonGroup()
        self.mode_pen = QRadioButton('Pen')
        self.mode_mouse = QRadioButton("Mouse")
        self.mode_lbl = QLabel("Mode: ")
        self.mode_group.addButton(self.mode_pen)
        self.mode_group.addButton(self.mode_mouse)
        self.mode_group.buttonClicked['QAbstractButton *'].connect(self.update_mode)
        self.mode_box = QGroupBox()
        self.mode_box.setFixedSize(290, 40)
        self.lmode = QHBoxLayout()
        self.lmode.addWidget(self.mode_lbl)
        self.lmode.addWidget(self.mode_pen)
        self.lmode.addWidget(self.mode_mouse)
        self.mode_box.setLayout(self.lmode)
        self.main.addLayout(self.lorient)
        self.main.addWidget(self.mode_box)
        self.lscreen = QGridLayout()
        self.screen = QComboBox()
        self.screen_lbl = QLabel("Screen: ")
        self.forced = QCheckBox("Force Proportions")
        self.forced.stateChanged.connect(self.update_forced)
        self.lscreen.addWidget(self.screen_lbl, 0, 0)
        self.lscreen.addWidget(self.screen, 0, 1)
        self.lscreen.addWidget(self.forced, 1, 1)
        self.main.addLayout(self.lscreen)
        # TODO: add tablet mapping
        self.setLayout(self.main)

    def initUI(self, stylus_id, eraser_id, settings={}):
        self.sid = stylus_id
        self.eid = eraser_id
        if 'mapping' in settings.keys():
            self.settings = settings['mapping']
        # load displays
        self.displays = self.get_displays()
        # get display info
        self.screen.addItems(sorted(self.displays.keys()))
        self.screen.currentIndexChanged.connect(self.update_screen)
        # set rotation value
        if 'rotate' in self.settings.keys():
            if self.settings['rotate'] == 'False':
                self.orient.hide()
                self.orient_lbl.hide()
                del self.settings['rotate']
            elif self.settings['rotate'] == 'none':
                self.orient.setCurrentIndex(0)
            elif self.settings['rotate'] == 'half':
                self.orient.setCurrentIndex(1)
            elif self.settings['rotate'] == 'cw':
                self.orient.setCurrentIndex(2)
            elif self.settings['rotate'] == 'ccw':
                self.orient.setCurrentIndex(3)
        else:
            self.orient.setCurrentIndex(0)
        self.update_orient()
        # set mode
        if 'mode' in self.settings.keys() and self.settings['mode'] == 'relative':
            self.mode_mouse.setChecked(True)
            self.screen.setDisabled(True)
            self.update_mode(self.mode_mouse)
        else:
            self.mode_pen.setChecked(True)
            self.screen.setDisabled(False)
            self.update_mode(self.mode_pen)
        # set forced
        if 'forcedproportion' in self.settings.keys():
            if self.settings['forcedproportion'] == 'True':
                self.forced.setChecked(True)
            else:
                self.forced.setChecked(False)
        else:
            self.settings['forcedproportion'] = 'False'
        # TODO: figure out partial...
        if 'maptooutput' in self.settings.keys():
            if self.settings['maptooutput'] in self.displays.keys():
                idx = self.screen.findText(str(self.settings['maptooutput']))
                self.screen.setCurrentIndex(idx)
                self.screen.setToolTip('[%s]' % self.displays[self.settings['maptooutput']]['cmd'])
        else:
            self.settings['maptooutput'] = 'Full'
        # hack note
        idx = self.screen.findText('Partial...')
        self.screen.setItemData(idx, "Just sets display to Full Screen (for now)", Qt.ToolTipRole)

    def update_orient(self):
        opt = self.orient.currentIndex()
        if opt == 0:
            self.settings['rotate'] = 'none'
        elif opt == 1:
            self.settings['rotate'] = 'half'
        elif opt == 2:
            self.settings['rotate'] = 'cw'
        elif opt == 3:
            self.settings['rotate'] = 'ccw'
        cmd = "xsetwacom --set %s rotate %s" % (self.sid, self.settings['rotate'])
        os.popen(cmd)

    def update_mode(self, id):
        if id.text() == 'Pen':
            self.mode_pen.setChecked(True)
            self.screen.setDisabled(False)
            self.forced.setDisabled(False)
            self.settings['mode'] = 'absolute'
        elif id.text() == 'Mouse':
            self.mode_mouse.setChecked(True)
            self.screen.setDisabled(True)
            self.forced.setDisabled(True)
            self.settings['mode'] = 'relative'
        cmd = "xsetwacom --set %s mode %s" % (self.sid, self.settings['mode'])
        os.popen(cmd)
        cmd = "xsetwacom --set %s mode %s" % (self.eid, self.settings['mode'])
        os.popen(cmd)

    def update_screen(self):
        self.settings['maptooutput'] = str(self.screen.currentText())
        coords = self.displays[str(self.screen.currentText())]['cmd']
        cmd = "xsetwacom --set %s maptooutput %s" % (self.sid, coords)
        os.popen(cmd)
        cmd = "xsetwacom --set %s maptooutput %s" % (self.eid, coords)
        os.popen(cmd)
        self.update_forced()

    def update_forced(self):
        # get current display
        cmd = "xsetwacom --set %s resetarea" % (self.sid)
        os.popen(cmd)
        cmd = "xsetwacom --set %s resetarea" % (self.eid)
        os.popen(cmd)
        cmd = "xsetwacom --get %s area" % (self.sid)
        p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        output = p.communicate()[0].rstrip().decode()
        self.settings['area'] = output
        if self.forced.isChecked():
            self.settings['forcedproportion'] = 'True'
            display = self.displays[str(self.screen.currentText())]['cmd']
            display = re.split('\D+', display)
            output = output.split(' ')
            height = output[3]
            width = output[2]
            if 'cw' in self.settings['rotate']:
                height = output[2]
                width = output[3]
            height = int(float(width) * (float(display[1])/float(display[0])))
            self.settings['area'] = "0 0 %d %d" % (int(width), int(height))
            cmd = "xsetwacom --set %s area %s" % (self.sid, self.settings['area'])
            os.popen(cmd)
            cmd = "xsetwacom --set %s area %s" % (self.eid, self.settings['area'])
            os.popen(cmd)
        else:
            self.settings['forcedproportion'] = 'False'

    def toggle_next(self):
        idx = self.screen.currentIndex()
        if idx + 1 <= self.screen.__len__():
            idx = idx + 1
            self.screen.setCurrentIndex(idx)
            # if partial matches full screen, skip it
            if str(self.screen.currentText()) == 'Partial...' and \
                    self.displays['Full']['cmd'] == self.displays['Partial...']['cmd']:
                        self.screen.setCurrentIndex(0)
        self.settings['maptooutput'] = str(self.screen.currentText())
        # self.update_screen()

    def get_displays(self):
        displays = {}
        cmd = "xdpyinfo | grep 'dimensions:'"
        p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        output = p.communicate()[0].decode('utf-8')
        pattern = r"\s+\S+\s+(\d+)x(\d+)"
        full = re.match(pattern, output).groups()
        displays['Full'] = {'cmd': "%sx%s+0+0" % (full[0], full[1]),
                            'x': full[0],
                            'y': full[1],
                            'xoff': 0,
                            'yoff': 0}
        cmd = "xdpyinfo -ext all | grep head"
        p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        output = p.communicate()[0].decode('utf-8')
        pattern = r"\s+(\S+)\s+#(\d+):\s+(\d+)x(\d+)\D+(\d+),(\d+)"
        heads = re.findall(pattern, output)
        for head in heads:
            info = list(head)
            displays['%s-%s' % (info[0].upper(), info[1])] = {'cmd': '%sx%s+%s+%s' %
                                                                     (info[2], info[3], info[4], info[5]),
                                                              'x': int(info[2]),
                                                              'y': int(info[3]),
                                                              'xoff': int(info[4]),
                                                              'yoff': int(info[5])}
        if 'partial' in self.settings.keys():
            displays['Partial...'] = {'cmd': self.settings['partial']}
        else:
            self.settings['partial'] = "%sx%s+0+0" % (full[0], full[1])
            displays['Partial...'] = {'cmd': "%sx%s+0+0" % (full[0], full[1]),
                                  'x': full[0],
                                  'y': full[1],
                                  'xoff': 0,
                                  'yoff': 0}
        return displays


    def resetMapping(self):
        # set default orientation
        if not self.orient.isHidden():
            self.orient.setCurrentIndex(0)
            self.update_orient()
        # set to full screen
        self.screen.setCurrentIndex(self.screen.findText('Full'))
        self.forced.setChecked(False)
        self.update_screen()
        # set to pen mode
        self.update_mode(self.mode_pen)


# TODO: add tabletpcbutton
'''
Stylus values:
- tabletpcbutton [pen needs to touch to register:off]
- buttons
    - button 2/3

Eraser values:
- buttons
    - button 1

Stylus/Eraser both have:
! - pressure curve
    - xsetwacom --set <id> pressurecurve <0 0 100 100>

    0 100 0 100 softerest
    0 75 25 100 # softer
    0 50 50 100 # soft
    0 25 75 100 # less soft
    0  0 100 100 # linear
    25 0 100 75 # little firm
    50 0 100 50 # firm
    75 0 100 25 # firmer
    100 0 100 0 # firmerest

! - suppress [delta sensitivity, effects all inputs; 0 - 100:2] (TBD)
! - rawsample [sample window size; 1 - 20:4](TBD)
! - threshold [min pressure to register; 0 - 2047:26] (TBD)
! - taptime [min time between taps for right click; 0 - 500:250] (TBD)


Mapping values:
- rotate (only applies to stylus, but effects all devices)
    - xsetwacom --set <id> rotate <none|cw|ccw|half>
- mode (relative/absolute)
    - xsetwacom -- set <id> mode <relative|absolute>
    - relative disables all mapping
- map to output
    - for now:
    - xsetwacom --set <id> MapToOutput <display ID>
    - alternate mapping (need to draw box with scalable area...)
        - ie: total screen range (1920x1200; one rotated): 3120x1920
        - if you want it to cover entire area of both screens: +0+0
        - x: + shifts box to the right, - shifts to the left
        - y: + shifts box down, - shifts box up
- force proportions
    - reset area, get max area, scale to what is actually needed
    - xsetwacom set <id> ResetArea
    - xsetwacom set <id> Area 0 0 tablet_width height
    - where height is tablet_width * screen_height / screen_width
- tablet area (disabled if force proportions enabled)
    - xsetwacom set <id> ResetArea
'''
