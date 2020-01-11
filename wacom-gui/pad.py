# TODO: mapping to specific


#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtSvg import *
from hotkeys import HotkeyWidget
from stylus import WacomAttribSlider
import pad_ui
import os
import json
import subprocess
import xfce_shortcut
from kde_shortcut import create, activate

# 880, 560

class Pad(QTabWidget, pad_ui.Ui_PadWidget):
    def __init__(self, parent = None):
        super(Pad, self).__init__(parent)
        self.setupUi(self)
        self.cwd = os.path.dirname(os.path.abspath(__file__))
        if self.cwd == '/usr/local/bin':
            self.cwd = '/usr/local/wacom-gui'
        self.keysLayout.setAlignment(Qt.AlignCenter)
        self.reset = QPushButton("Set Defaults")
        self.reset.setMinimumSize(90, 20)
        self.reset.setMaximumSize(90, 20)
        self.reset.clicked.connect(self.set_default)
        self.buttons = {'left': [], 'right': [], 'top': [], 'bottom': []}
        self.setFocusPolicy(Qt.NoFocus)
        desktop = os.environ["DESKTOP_SESSION"]
        if (desktop == "mate"):
            self.load_dconf()
        elif (desktop == "1-kde-plasma-standard"):
            self.load_kde()
            #if the KDE shortcut doesn't exist in the two system files, create it
            if create('Display toggle', 'wacom-gui --toggle', 'Meta+Z', 'This shortcut triggers display toggle for your Wacom tablet.'):
                activate()
        elif (desktop == "xfce"):
            if not xfce_shortcut.createShortcut('wacom-gui --toggle', '<Super>Z'):
                pass
        else:
            print("unknown desktop environment")

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

    def load_dconf(self):
        with open(os.path.join(self.cwd, 'custom.json'), 'r') as f:
            hotkeys = json.load(f)
        if os.path.exists(os.path.expanduser("~/.wacom-gui/custom.json")):
            with open(os.path.expanduser("~/.wacom-gui/custom.json"), 'r') as f:
                custom = json.load(f)
            for key in hotkeys.keys():
                if key in custom.keys():
                    del custom[key]
            hotkeys.update(custom)
        os_custom = self._load_keyboard_shortcuts()
        for key, data in hotkeys.items():
            if data['dconf'] != '':
                idx = -1
                found = False
                for entry in os_custom.keys():
                    if int(entry.split('custom')[1]) > idx:
                        idx = int(entry.split('custom')[1])
                    # name match
                    if os_custom[entry]['name'] == "'%s'" % data['label'] or \
                            os_custom[entry]['binding'] == "'%s'" % data['dconf'] or \
                            os_custom[entry]['action'] == "'%s'" % data['run']:
                        # update entry
                        os_custom[entry]['name'] = "'%s'" % data['label']
                        os_custom[entry]['binding'] = "'%s'" % data['dconf']
                        os_custom[entry]['action'] = "'%s'" % data['run']
                        found = True
                        break
                if not found:
                    new_entry = 'custom%d' % (idx + 1)
                    os_custom[new_entry] = {'name': "'%s'" % data['label'],
                                         'binding': "'%s'" % data['dconf'],
                                         'action': "'%s'" % data['run']}
        # generate config file
        try:
            config = os.path.expanduser("~/.wacom-gui")
            if not os.path.isdir(config):
                os.mkdir(config)
            config = os.path.join(config, "keybind.cfg")
            f = open(config, "w")
            for entry in os_custom:
                f.write("[%s]\naction=%s\nbinding=%s\nname=%s\n\n" %
                        (entry, os_custom[entry]['action'], os_custom[entry]['binding'], os_custom[entry]['name']))
            f.close()
            os.popen("dconf load /org/mate/desktop/keybindings/ < %s" % config)
        except Exception as e:
            print(e)

    # This doesn't actually 'load' kde, but merely replicates the logic of the
    # load_dconf (MATE) path in the KDE path. This code that ensures
    # the ".wacom-gui" directory exists could be factored out and called in a
    # more appropriate place now that multiple desktop enviroments are supported.
    def load_kde(self):
        # generate config file
        try:
            config = os.path.expanduser("~/.wacom-gui")
            if not os.path.isdir(config):
                os.mkdir(config)
        except Exception as e:
            print e

    def _load_keyboard_shortcuts(self):
        custom = {}
        p = subprocess.Popen("dconf dump /org/mate/desktop/keybindings/", shell=True, stdout=subprocess.PIPE)
        p.wait()
        output = p.communicate()[0].decode('utf-8').split('\n')
        for line in output:
            if '[custom' in line:
                entry = line[1:-1]
                custom[entry] = {}
            elif 'action' in line:
                custom[entry]['action'] = line.split('=')[1]
            elif 'binding' in line:
                custom[entry]['binding'] = line.split('=')[1]
            elif 'name' in line:
                custom[entry]['name'] = line.split('=')[1]
        return custom

    def init_keys(self, dev_id, image, buttons, cmds):
        # remove previous stuff
        self.deleteItemsOfLayout(self.keysLayout.layout())
        self.buttons = {'left': [], 'right': [], 'top': [], 'bottom': []}
        # TODO: Bottom, Right
        top = QHBoxLayout()
        top.setAlignment(Qt.AlignHCenter)
        left = QVBoxLayout()
        left.setAlignment(Qt.AlignVCenter)
        right = QVBoxLayout()
        right.setAlignment(Qt.AlignVCenter)
        bottom = QVBoxLayout()
        bottom.setAlignment(Qt.AlignVCenter)
        # add buttons
        but_loc = {}
        for bid in sorted(buttons.keys()):
            but_loc[bid] = buttons[bid]['pos']
        for bid, value in sorted(but_loc.items(), key=lambda t: (t[1], t[0])):
            if cmds.__len__() == 0:
                keystroke = "Default"
            else:
                keystroke = cmds[bid]
            if buttons[bid]['orient'] == 'Top':
                self.buttons['top'].append(HotkeyWidget(dev_id, bid, buttons[bid]['bid'], keystroke))
            elif buttons[bid]['orient'] == 'Left':
                self.buttons['left'].append(HotkeyWidget(dev_id, bid, buttons[bid]['bid'], keystroke))
            elif buttons[bid]['orient'] == 'Right':
                self.buttons['right'].append(HotkeyWidget(dev_id, bid, buttons[bid]['bid'], keystroke))
            elif buttons[bid]['orient'] == 'Bottom':
                self.buttons['bottom'].append(HotkeyWidget(dev_id, bid, buttons[bid]['bid'], keystroke))
        svgWidget = None
        svg_hspace = QSpacerItem(800, 80, QSizePolicy.Fixed, QSizePolicy.Fixed)
        svg_vspace = QSpacerItem(80, 300, QSizePolicy.Fixed, QSizePolicy.Fixed)
        hspace = 0
        vspace = 20  # reset button
        row = 0
        col = 0  # need at least 1 column
        if self.buttons['top'].__len__() != 0:
            vspace = vspace + 40
        if self.buttons['bottom'].__len__() != 0:
            vspace = vspace + 40
        if self.buttons['left'].__len__() != 0:
            col = col + 1
            hspace = hspace + 120
        if self.buttons['right'].__len__() != 0:
            col = col + 1
        try:
            bkground = os.path.join("/tmp", image)
            if os.path.exists(bkground):
                svgWidget = QSvgWidget(bkground)
                col = col + 1
            # get spacing for final image
            svg_size = svgWidget.sizeHint()
            img_h = float(540 - vspace)
            img_w = float(860 - hspace)
            scale_w = float(img_w / svg_size.width())
            scale_h = float(img_h / svg_size.height())
            if scale_h < scale_w:
                vspace = round(img_w - (scale_h * svg_size.width()))
                svg_vspace.changeSize(vspace, img_h, QSizePolicy.Fixed, QSizePolicy.Fixed)
                svg_hspace.changeSize(img_w, 0, QSizePolicy.Fixed, QSizePolicy.Fixed)
            else:
                hspace = round(img_h - (scale_w * svg_size.height()))
                svg_vspace.changeSize(0, img_h, QSizePolicy.Fixed, QSizePolicy.Fixed)
                svg_hspace.changeSize(img_w, hspace, QSizePolicy.Fixed, QSizePolicy.Fixed)
        except Exception as e:
            print (e)
        # start to build...
        # add top row
        if self.buttons['top'].__len__() != 0:
            for button in self.buttons['top']:
                top.addWidget(button)
            self.keysLayout.addLayout(top, row, 0, 1, col)
            row = row + 1
        # add left row
        if self.buttons['left'].__len__() != 0:
            for button in self.buttons['left']:
                left.addWidget(button)
            if svgWidget is None:
                self.keysLayout.addLayout(left, row, 0, 1, 1)
            else:
                self.keysLayout.addLayout(left, row, 0, 2, 1)
        if svgWidget is not None:
            if self.buttons['left'].__len__() == 0:
                self.keysLayout.addWidget(svgWidget, row, 0, 1, 1)
            else:
                self.keysLayout.addWidget(svgWidget, row, 1, 1, 1)
                self.keysLayout.addItem(svg_vspace, row, 2, 1, 1)
                self.keysLayout.addItem(svg_hspace, row + 1, 1, 1, 2)
                row = row + 1
        if self.buttons['right'].__len__() != 0:
            for button in self.buttons['right']:
                right.addWidget(button)
            if svgWidget is None:
                self.keysLayout.addLayout(right, row, 2, 1, 1)
            else:
                self.keysLayout.addLayout(right, row - 1, 3, 2, 1)
        if self.buttons['left'].__len__() != 0 or self.buttons['right'].__len__() != 0:
            row = row + 1
        if self.buttons['bottom'].__len__() != 0:
            for button in self.buttons['bottom']:
                top.addWidget(button)
            self.keysLayout.addLayout(top, row, 0, 1, col)
            row = row + 1
        resetLayout = QHBoxLayout()
        resetLayout.setAlignment(Qt.AlignRight)
        resetLayout.addWidget(self.reset)
        self.keysLayout.addLayout(resetLayout, row, col, 1, col)

    def set_default(self):
        for loc in self.buttons.keys():
            for btn in self.buttons[loc]:
                btn.reset()

    def is_toggle(self):
        for loc in self.buttons:
            for button in self.buttons[loc]:
                if button.is_toggle():
                    return True
        return False

    def get_config(self):
        buttons = {}
        for loc in self.buttons.keys():
            for btn in self.buttons[loc]:
                info = list(btn.button.get_button_cmd())
                id = None
                if 'Button' in info[1]:
                    id = info[1].split(' ')[1]
                elif info[1] in ['AbsWheelUp', 'StripLeftUp', 'StripRightUp']:
                    id = 4
                elif info[1] in ['AbsWheelDown', 'StripLeftDown', 'StripRightDown']:
                    id = 5
                if id == info[2]:
                    buttons[info[0]] = 'Default'
                else:
                    buttons[info[0]] = str(info[2])
        return buttons


class Touch(QWidget):
    def __init__(self):
        QWidget.__init__(self, None)
        self.dev_id = None
        self.touch = None
        self.gesture = None
        self.layout = QGridLayout()
        self.taptime = None
        self.rawsample = None
        self.zoomdistance = None
        self.scrolldistance = None
        self.guide = None

    def init(self, dev_id, settings):
        self.deleteItemsOfLayout(self.layout.layout())
        self.dev_id = dev_id
        self.cwd = os.path.dirname(os.path.abspath(__file__))
        self.touch = QCheckBox("Enable Touch")
        self.gesture = QCheckBox("Enable Gestures")
        self.guide = QVBoxLayout()
        self.guide.setAlignment(Qt.AlignLeft)
        touch = QVBoxLayout()
        touch.addWidget(self.touch)
        touch.addWidget(self.gesture)
        self.touch.setChecked(False)
        self.gesture.setEnabled(False)
        if 'touch' in settings.keys() and settings['touch'] == 'on':
            self.touch.setChecked(True)
            self.gesture.setEnabled(True)
        self.gesture.setChecked(False)
        if 'gesture' in settings.keys() and settings['gesture'] == 'on' and self.gesture.isEnabled():
            self.touch.setChecked(True)
        if 'taptime' in settings.keys():
            self.taptime = WacomAttribSlider(self.dev_id, 'taptime', 250, "Double Tap Time (ms)", 0, 500, 25,
                                                int(settings['taptime']))
        else:
            self.taptime = WacomAttribSlider(self.dev_id, 'taptime', 250, "Threshold", 0, 500, 25)
        self.taptime.setToolTip("Time between taps in ms that will register as a double time")
        if 'rawsample' in settings.keys():
            self.rawsample = WacomAttribSlider(self.dev_id, 'rawsample', 4, "Sample Size", 1, 20, 4,
                                                  int(settings['rawsample']))
        else:
            self.rawsample = WacomAttribSlider(self.dev_id, 'rawsample', 4, "Sample Size", 1, 20, 4)
        self.rawsample.setToolTip("Set the sample window size (a sliding average sampling window) for\n"
                                     "incoming input tool raw data points.")
        if 'zoomdistance' in settings.keys():
            self.zoomdistance = WacomAttribSlider(self.dev_id, 'zoomdistance', 180, "Zoom Distance", 50, 500, 25,
                                                int(settings['zoomdistance']))
        else:
            self.zoomdistance = WacomAttribSlider(self.dev_id, 'zoomdistance', 180, "Zoom Distance", 50, 500, 25)
        self.zoomdistance.setToolTip("A lower value increases the sensitivity when zooming")
        if 'scrolldistance' in settings.keys():
            self.scrolldistance = WacomAttribSlider(self.dev_id, 'scrolldistance', 80, "Scroll Distance", 10, 200, 20,
                                                int(settings['scrolldistance']))
        else:
            self.scrolldistance = WacomAttribSlider(self.dev_id, 'scrolldistance', 80, "Scroll Distance", 10, 200, 20)
        self.scrolldistance.setToolTip("A lower value increases the sensitivity when scrolling")
        self.updateTouch()
        self.updateGesture()
        self.touch.stateChanged.connect(self.updateTouch)
        self.gesture.stateChanged.connect(self.updateGesture)
        try:
            if os.path.isfile(os.path.join(self.cwd, "icons/ui/touch.json")):
                data = None
                with open(os.path.join(self.cwd, "icons/ui/touch.json"), 'r') as f:
                    data = json.load(f)
                for fingers in data.keys():
                    self.guide.addWidget(QLabel(fingers))
                    for control in data[fingers].keys():
                        text = "%s - %s" % (control, data[fingers][control]['text'])
                        self.guide.addWidget(GuideWidget(data[fingers][control]['icon'], text))
        except Exception as e:
            print (e)
        group = QGroupBox("Touch Controls")
        group.setFixedSize(290, 80)
        group.setLayout(touch)
        gesture = QGroupBox("Gesture Controls List")
        gesture.setLayout(self.guide)
        gesture.setContentsMargins(6, 6, 6, 6)
        # self.layout.setMargin(0)
        self.layout.addWidget(group, 0, 0, 1, 1, Qt.AlignTop)
        self.layout.addWidget(gesture, 0, 1, 5, 1, Qt.AlignVCenter)
        self.layout.addWidget(self.taptime, 1, 0, 1, 1, Qt.AlignTop)
        self.layout.addWidget(self.rawsample, 2, 0, 1, 1, Qt.AlignTop)
        self.layout.addWidget(self.zoomdistance, 3, 0, 1, 1, Qt.AlignTop)
        self.layout.addWidget(self.scrolldistance, 4, 0, 1, 1, Qt.AlignTop)
        self.setLayout(self.layout)

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

    def updateTouch(self):
        if self.touch.isChecked():
            cmd = "xsetwacom --set %s touch on" % self.dev_id
            os.popen(cmd)
            self.gesture.setEnabled(True)
            self.taptime.group.setEnabled(True)
            self.rawsample.group.setEnabled(True)
            return ('touch', 'on')
        else:
            cmd = "xsetwacom --set %s touch off" % self.dev_id
            os.popen(cmd)
            cmd = "xsetwacom --set %s gesture off" % self.dev_id
            os.popen(cmd)
            self.gesture.setChecked(False)
            self.gesture.setEnabled(False)
            self.taptime.group.setEnabled(False)
            self.rawsample.group.setEnabled(False)
            self.zoomdistance.group.setEnabled(False)
            self.scrolldistance.group.setEnabled(False)
            return ('touch', 'off')

    def updateGesture(self):
        if self.gesture.isChecked():
            self.zoomdistance.group.setEnabled(True)
            self.scrolldistance.group.setEnabled(True)
            cmd = "xsetwacom --set %s gesture on" % self.dev_id
            os.popen(cmd)
            return ('gesture', 'on')
        else:
            self.zoomdistance.group.setEnabled(False)
            self.scrolldistance.group.setEnabled(False)
            cmd = "xsetwacom --set %s gesture off" % self.dev_id
            os.popen(cmd)
            return ('gesture', 'off')

    def reset(self):
        self.touch.setChecked(False)
        self.updateTouch()
        self.taptime.set_defaults()
        self.rawsample.set_defaults()
        self.zoomdistance.set_defaults()
        self.scrolldistance.set_defaults()

    def get_config(self):
        settings = {}
        (attr, data) = self.updateTouch()
        settings[attr] = str(data)
        (attr, data) = self.updateGesture()
        settings[attr] = str(data)
        (attr, value) = self.rawsample.get_setting()
        settings[attr] = str(value)
        (attr, value) = self.taptime.get_setting()
        settings[attr] = str(value)
        (attr, value) = self.zoomdistance.get_setting()
        settings[attr] = str(value)
        (attr, value) = self.scrolldistance.get_setting()
        settings[attr] = str(value)
        return settings

class GuideWidget(QWidget):
    def __init__(self, icon, info):
        QWidget.__init__(self, None)
        self.cwd = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons/ui")
        self.setFixedSize(500, 70)
        self.icon = QLabel()
        self.icon.setFixedSize(40, 40)
        self.icon.setPixmap(QPixmap(os.path.join(self.cwd, icon)))
        self.icon.setScaledContents(True)
        self.info = QLabel()
        self.info.setFixedWidth(400)
        self.info.setText(info)
        self.info.setWordWrap(True)
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignVCenter)
        layout.addWidget(self.icon)
        layout.addWidget(self.info)
        group = QGroupBox()
        group.setLayout(layout)
        main = QVBoxLayout()
        main.addWidget(group)
        self.setLayout(main)


if __name__ == '__main__':
    app = QApplication([])
    window = Pad()
    buttons = {'ButtonC': {'bid': 'Button 3', 'orient': 'Left'}, 'ButtonB': {'bid': 'Button 2', 'orient': 'Left'}, 'ButtonA': {'bid': 'Button 1', 'orient': 'Left'}, 'ButtonG': {'bid': 'Button 11', 'orient': 'Left'}, 'ButtonF': {'bid': 'Button 10', 'orient': 'Left'}, 'ButtonE': {'bid': 'Button 9', 'orient': 'Left'}, 'ButtonD': {'bid': 'Button 8', 'orient': 'Left'}, 'RingUp': {'bid': 'AbsWheelUp', 'orient': 'Left'}, 'RingDown': {'bid': 'AbsWheelDown', 'orient': 'Left'}}
    # window.init_keys('intuos4-4x6.svg', buttons, {})
    window.show()
    app.exec_()
'''
Config file layout
{
    config name: {
        eraser: {},
        stylus: {},
        cursor: {},
        pad: {
            'Button 1': <bid string>,
            'Button 2': <bid string>,
            'Button 3': <bid string>,
            ...
            'Mode': 'Abosolute',
        },
        touch: {
            'Touch': 'on'
        }
    }
}


'''
