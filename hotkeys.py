#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui, QtSvg
from functools import partial
import json
import os
import re
import shutil
import keystroke


class Hotkey(QtCore.QObject):
    def __init__(self, devid, bid, cmd, parent=None):
        super(Hotkey, self).__init__(parent)
        self.devid = devid
        self.id = bid
        self.cmd = cmd
        self.btn = QtGui.QPushButton()
        self.btn.setMaximumWidth(90)
        self.btn.setText(bid)
        self.keymap = {}
        self.keymap_custom = {}
        self.keys_list = {}
        self.keys_custom_list = {}
        self.menu_init()
        self.btn.clicked.connect(self.load_menu)
        self.get_custom()
        self.label = QtGui.QLabel()
        self.label.setAutoFillBackground(True)
        # default label
        if self.cmd == '0':
            self.label.setText('Disabled')
            self.label.setStyleSheet("QLabel { background-color: rgba(255,0,0,120); }")
        # TODO: figure out for abswheel/strip...
        elif 'Button' in self.id and self.id.split(' ')[1] == self.cmd:
            self.label.setText('Default')
            self.label.setStyleSheet("QLabel { background-color: rgba(0,255,0,120); }")
        else:
            self.label.setStyleSheet("QLabel { background-color: rgba(200,200,200,120); }")
            if self.cmd in self.keys_list.keys():
                self.label.setText(self.keys_list[self.cmd])
            elif self.cmd in self.keymap_custom.keys():
                self.label.setText(self.keymap_custom[self.cmd]['label'])
                if self.keymap_custom[cmd]['run'] != '':
                    self.label.setStyleSheet("QLabel { background-color: rgba(180,180,20,120); }")

    def menu_init(self):
        self.menu = QtGui.QMenu()
        self.modifiers = QtGui.QMenu("Modifier")
        self.mouse = QtGui.QMenu("Mouse Click")
        self.scroll = QtGui.QMenu("Pan/Scroll")
        self.keypress = QtGui.QMenu("Keypress")
        self.custom = QtGui.QMenu("Custom Hotkeys")
        self.common = {"Letters": QtGui.QMenu("Letters"),
                       "Numbers": QtGui.QMenu("Numbers"),
                       "Special Characters": QtGui.QMenu("Special Characters"),
                       "Control Keys": QtGui.QMenu("Control Keys"),
                       "Function Keys": QtGui.QMenu("Function Keys"),
                       "Keypad": QtGui.QMenu("Keypad"),
                       "System Shortcuts": QtGui.QMenu("System Shortcuts")
                       }
        self.menu.addAction("Disable", lambda: self.set_value(0, 'Disabled'))
        self.menu.addAction("Default", lambda: self.set_value(self.id, 'Default'))
        self.menu.addMenu(self.modifiers)
        self.menu.addMenu(self.mouse)
        self.menu.addMenu(self.scroll)
        self.menu.addMenu(self.keypress)
        self.menu.addMenu(self.custom)
        self.menu.addSeparator()
        self.menu.addAction("Keystroke...", lambda: self.get_keystroke(False))
        self.menu.addAction("Keystroke Run Cmd...", lambda: self.get_keystroke(True))
        # key keystrokes from file
        try:
            config = os.path.join(os.getcwd(), "keymap.json")
            if os.path.exists(config):
                with open(config, 'r') as f:
                    self.keymap = json.load(f)
        except:
            print ("Error Will Robinson!")
        for key in self.keymap.keys():
            if key == 'Modifiers':
                for cmd, label in sorted(self.keymap[key].items()):
                    self.modifiers.addAction(label, partial(self.set_value, cmd, label))
                    self.keys_list[cmd] = label
            elif key == 'Mouse':
                for cmd, label in sorted(self.keymap[key].items()):
                    self.mouse.addAction(label, partial(self.set_value, cmd, label))
                    self.keys_list[cmd] = label
            elif key == 'Scroll':
                for cmd, label in sorted(self.keymap[key].items()):
                    self.scroll.addAction(label, partial(self.set_value, cmd, label))
                    self.keys_list[cmd] = label
            else:
                for cmd, label in sorted(self.keymap[key].items()):
                    self.common[key].addAction(label, partial(self.set_value, cmd, label))
                    self.keys_list[cmd] = label
        for key in sorted(self.common.keys()):
            self.keypress.addMenu(self.common[key])
        # self.load_custom()

    def set_value(self, value, label):
        self.parse_multikey(value)
        self.label.setText(label)
        cmd = "xsetwacom --set %d %s %s" % (self.devid, self.id, self.cmd)
        setCommand = os.popen(cmd)
        if label == 'Disabled':
            self.label.setStyleSheet("QLabel { background-color: rgba(255,0,0,120); }")
        elif label == 'Default':
            self.label.setStyleSheet("QLabel { background-color: rgba(0,255,0,120); }")
        else:
            if value in self.keymap_custom.keys() and self.keymap_custom[value]['run'] != '':
                self.label.setStyleSheet("QLabel { background-color: rgba(180,180,20,120); }")
            else:
                self.label.setStyleSheet("QLabel { background-color: rgba(200,200,200,120); }")

    def get_custom(self):
        # get gui-specific keystrokes from file
        try:
            config = os.path.join(os.getcwd(), "custom.json")
            if os.path.exists(config):
                with open(config, 'r') as f:
                    self.keymap_custom = json.load(f)
                for cmd in self.keymap_custom.keys():
                    if self.keymap_custom[cmd]['run'] == '':
                        self.custom.addAction(self.keymap_custom[cmd]['label'],
                                              partial(self.set_value, cmd,
                                                      self.keymap_custom[cmd]['label']))
                    else:
                        self.custom.addAction("* %s *" % self.keymap_custom[cmd]['label'],
                                              partial(self.set_value, cmd,
                                                      self.keymap_custom[cmd]['label']))
                    self.keys_custom_list[cmd] = self.keymap_custom[cmd]['label']
        except:
            print ("Error Will Robinson!")
        # get user-defined keystrokes from file
        try:
            config = os.path.expanduser("~/.wacom-gui/custom.json")
            if os.path.exists(config):
                with open(config, 'r') as f:
                    user_custom = json.load(f)
                for cmd in user_custom.keys():
                    if cmd not in self.keymap_custom.keys():
                        if user_custom[cmd]['run'] == '':
                            self.custom.addAction(user_custom[cmd]['label'],
                                                  partial(self.set_value, cmd, user_custom[cmd]['label']))
                        else:
                            self.custom.addAction("* %s *" % user_custom[cmd]['label'],
                                                  partial(self.set_value, cmd, user_custom[cmd]['label']))
                        self.keys_custom_list[cmd] = user_custom[cmd]['label']
                self.keymap_custom.update(user_custom)
        except:
            print ("Error Will Robinson!")

    def load_menu(self):
        # need to reset custom keys if changed elsewhere
        self.custom.clear()
        self.get_custom()
        self.menu.exec_(QtGui.QCursor.pos())

    def get_keystroke(self, runcmd):
        ok, cmdstring, label, run = KeystrokeGui.get_keystrokes(runcmd, self.cmd)
        if ok == 1:
            # self.parse_multikey(cmdstring)
            # TODO: update custom keystroke db
            # derp
            self.set_value(self.cmd, label)
            self.keymap_custom[' '.join(filter(None, re.split('{|}| ', str(cmdstring))))] = {'label': label,
                                       'run': run,
                                       'protected': 0}
            config = os.path.expanduser("~/.wacom-gui")
            if not os.path.exists(config):
                os.mkdir(config)
            config = os.path.join(config, 'custom.json')
            if os.path.exists(config):
                shutil.copyfile(config, "%s.bak" % config)
            with open(config, 'w') as fout:
                json.dump(self.keymap_custom, fout, sort_keys=True, indent=4, separators=(',', ": "))

    def parse_multikey(self, cmdstring):
        strokes = filter(None, re.split('{|}| ', str(cmdstring)))
        self.cmd = ""
        button = False
        for stroke in strokes:
            if 'button' in stroke:
                if self.cmd.__len__() == 0:
                    self.cmd = stroke
                else:
                    self.cmd = "%s %s" % (self.cmd, stroke)
                button = True
            else:
                if button:
                    self.cmd = "%s key %s" % (self.cmd, stroke)
                    button = False
                else:
                    if self.cmd.__len__() == 0:
                        self.cmd = "key %s" % stroke
                    else:
                        self.cmd = "%s %s" % (self.cmd, stroke)


class KeystrokeGui(QtGui.QDialog, keystroke.Ui_Dialog):
    def __init__(self, cmd, parent=None):
        super(KeystrokeGui, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Hotkey Config Menu")
        self.keymap = None
        self.keymap_custom = None
        self.keys_list = {}
        self.keys_custom_list = {}
        self.menu = QtGui.QMenu()
        self.modifiers = QtGui.QMenu("Modifier")
        self.mouse = QtGui.QMenu("Mouse Click")
        self.scroll = QtGui.QMenu("Pan/Scroll")
        self.keypress = QtGui.QMenu("Keypress")
        self.letter = QtGui.QMenu("Letters")
        self.num = QtGui.QMenu("Numbers")
        self.special = QtGui.QMenu("Special Characters")
        self.ctrl = QtGui.QMenu("Control Keys")
        self.fn = QtGui.QMenu("Function Keys")
        self.keypad = QtGui.QMenu("Keypad")
        self.custom = QtGui.QMenu("Custom")
        self.common = {}
        self.menu_init()
        self.get_custom()
        cmd = self.sanitize(cmd)
        if cmd in self.keys_custom_list.keys():
            self.populate_fields(cmd)
        self.keystroke.setMenu(self.menu)

    def sanitize(self, cmd):
        strokes = filter(None, re.split('{|}| ', cmd))
        skip = False
        cmdline = ''
        for idx, stroke in enumerate(strokes):
            if stroke != 'key':
                if cmdline == '':
                    cmdline = stroke
                else:
                    cmdline = "%s %s" % (cmdline, stroke)
        return cmdline

    def populate_fields(self, cmd):
        cmdline = ''
        strokes = filter(None, re.split('{|}| ', cmd))
        for stroke in strokes:
            cmdline = "%s{%s}" % (cmdline, stroke)
        self.keystrokeinput.setText(cmdline)
        self.shortcutinput.setText(self.keymap_custom[cmd]['label'])
        if self.keymap_custom[cmd]['run'] != '':
            self.runinput.setText(self.keymap_custom[cmd]['run'])

    def menu_init(self):
        # TODO: Add load option to edit existing shortcuts
        self.menu.addAction("Clear", lambda: self.clear_input())
        self.menu.addAction("Undo", lambda: self.remove_one())
        self.menu.addMenu(self.modifiers)
        self.menu.addMenu(self.mouse)
        self.menu.addMenu(self.scroll)
        self.menu.addMenu(self.keypress)
        self.common = {"Letters": QtGui.QMenu("Letters"),
                       "Numbers": QtGui.QMenu("Numbers"),
                       "Special Characters": QtGui.QMenu("Special Characters"),
                       "Control Keys": QtGui.QMenu("Control Keys"),
                       "Function Keys": QtGui.QMenu("Function Keys"),
                       "Keypad": QtGui.QMenu("Keypad"),
                       "System Shortcuts": QtGui.QMenu("System Shortcuts")
                       }
        # key keystrokes from file
        try:
            config = os.path.join(os.getcwd(), "keymap.json")
            if os.path.exists(config):
                with open(config, 'r') as f:
                    self.keymap = json.load(f)
        except:
            print ("Error Will Robinson!")
        for key in self.keymap.keys():
            if key == 'Modifiers':
                for cmd, label in sorted(self.keymap[key].items()):
                    self.modifiers.addAction(label, partial(self.set_value, cmd))
                    self.keys_list[cmd] = label
            elif key == 'Mouse':
                for cmd, label in sorted(self.keymap[key].items()):
                    self.mouse.addAction(label, partial(self.set_value, cmd))
                    self.keys_list[cmd] = label
            elif key == 'Scroll':
                for cmd, label in sorted(self.keymap[key].items()):
                    self.scroll.addAction(label, partial(self.set_value, cmd))
                    self.keys_list[cmd] = label
            else:
                for cmd, label in sorted(self.keymap[key].items()):
                    self.common[key].addAction(label, partial(self.set_value, cmd))
                    self.keys_list[cmd] = label
        for key in sorted(self.common.keys()):
            if key != "System Shortcuts":
                self.keypress.addMenu(self.common[key])

    def get_custom(self):
        # get gui-specific keystrokes from file
        try:
            config = os.path.join(os.getcwd(), "custom.json")
            if os.path.exists(config):
                with open(config, 'r') as f:
                    self.keymap_custom = json.load(f)
                for cmd in self.keymap_custom.keys():
                    if self.keymap_custom[cmd]['run'] == '':
                        self.custom.addAction(self.keymap_custom[cmd]['label'],
                                              partial(self.set_value, cmd,
                                                      self.keymap_custom[cmd]['label']))
                    else:
                        self.custom.addAction("* %s *" % self.keymap_custom[cmd]['label'],
                                              partial(self.set_value, cmd,
                                                      self.keymap_custom[cmd]['label']))
                    self.keys_custom_list[cmd] = self.keymap_custom[cmd]['label']
        except:
            print ("Error Will Robinson!")
        # get user-defined keystrokes from file
        try:
            config = os.path.expanduser("~/.wacom-gui/custom.json")
            if os.path.exists(config):
                with open(config, 'r') as f:
                    user_custom = json.load(f)
                for cmd in user_custom.keys():
                    if cmd not in self.keymap_custom.keys():
                        if user_custom[cmd]['run'] == '':
                            self.custom.addAction(user_custom[cmd]['label'],
                                                  partial(self.set_value, cmd, user_custom[cmd]['label']))
                        else:
                            self.custom.addAction("* %s *" % user_custom[cmd]['label'],
                                                  partial(self.set_value, cmd, user_custom[cmd]['label']))
                        self.keys_custom_list[cmd] = user_custom[cmd]['label']
                self.keymap_custom.update(user_custom)
        except:
            print ("Error Will Robinson!")

    def clear_input(self):
        self.keystrokeinput.setText("")

    def remove_one(self):
        strokes = filter(None, re.split('{|}', str(self.keystrokeinput.text())))
        strokes.pop()
        newcmd = ''
        for stroke in strokes:
            newcmd = "%s{%s}" % (newcmd, stroke)
        self.keystrokeinput.setText(newcmd)

    def set_value(self, value):
        blah = self.keystrokeinput.text()
        cmd = ''
        if 'button' in value:
            cmd = "{%s}" % value
        else:
            strokes = filter(None, re.split('{|}| ', str(value)))
            for stroke in strokes:
                cmd = "%s{%s}" % (cmd, stroke)
        self.keystrokeinput.setText("%s%s" % (blah, cmd))

    def get_cmd(self):
        return str(self.keystrokeinput.text()), str(self.shortcutinput.text()), str(self.runinput.text())

    @staticmethod
    def cmd_path_search(cmd, mode=os.F_OK | os.X_OK, path=None):
        def _access_check(fn, mode):
            return (os.path.exists(fn) and os.access(fn, mode) and
                    not os.path.isdir(fn))

        if _access_check(cmd, mode):
            return cmd
        path = (path or os.environ.get("PATH", os.defpath)).split(os.pathsep)
        files = [cmd]
        seen = set()
        for dir in path:
            dir = os.path.normcase(dir)
            if dir not in seen:
                seen.add(dir)
                for thefile in files:
                    name = os.path.join(dir, thefile)
                    if _access_check(name, mode):
                        return name
        return None

    def accept(self):
        # check if valid multi-key command
        strokes = filter(None, re.split('{|}| ', str(self.keystrokeinput.text())))
        # invalid new shortcut
        if strokes.__len__() < 1:
            warning = QtGui.QMessageBox(QtGui.QMessageBox.Warning, "Keystroke length too short",
                                        "Please enter more than a single keystroke to make a shortcut.")
            warning.exec_()
        # system shortcut
        elif ' '.join(strokes) in self.keys_list:
            warning = QtGui.QMessageBox(QtGui.QMessageBox.Warning, "System Keystroke Command",
                                        "This command can not be changed.")
            warning.exec_()
        # previously defined  as shortcut
        elif ' '.join(strokes) in self.keys_custom_list.keys():
            # TODO: check if changing run command
            if self.shortcutinput.text() != self.keys_custom_list[' '.join(strokes)]:
                warning = QtGui.QMessageBox(QtGui.QMessageBox.Warning, "Shortcut Name Undefined",
                                            "Please provide a shortcut name before saving.")
                warning.exec_()
        # shortcut name used for a different shortcut
        elif self.shortcutinput.text() in self.keys_custom_list.values():
                warning = QtGui.QMessageBox(QtGui.QMessageBox.Warning, "Shortcut Name In Use",
                                            "This shortcut name is already being used for another shortcut.")
                warning.exec_()
        # check characters used in shortcut name
        elif set("[`~!@#$%^&*=+\\|}{'\":;/?><.,]$").intersection(str(self.shortcutinput.text())):
            warning = QtGui.QMessageBox(QtGui.QMessageBox.Warning, "Invalid Shortcut Name",
                                        "Please do not use special characters, except for _-()")
            warning.exec_()
        elif str(self.shortcutinput.text()) not in self.keys_custom_list.values():
            # check run
            if self.runinput.isHidden() == False:
                # check if it is a valid file path
                runcmd = str(self.runinput.text())
                if self.cmd_path_search(runcmd.split(' ')[0]):
                    super(KeystrokeGui, self).accept()
                else:
                    warning = QtGui.QMessageBox(QtGui.QMessageBox.Warning, "Invalid Command",
                                                "Command path is invalid or is not executable.")
                    warning.exec_()
            else:
                super(KeystrokeGui, self).accept()
            #else:
            #    warning = QtGui.QMessageBox(QtGui.QMessageBox.Warning, "Shortcut Name Exists",
            #                                "This shortcut name is already in use.")
            #    warning.exec_()
        elif str(self.shortcutinput.text()) != self.keys_list[' '.join(strokes)]:
            warning = QtGui.QMessageBox(QtGui.QMessageBox.Warning, "Keystroke Command Duplicate",
                                        "This command already exists as \"%s\"" % self.keys_list[' '.join(strokes)])
            warning.exec_()
        else:
            warning = QtGui.QMessageBox(QtGui.QMessageBox.Warning, "Keystroke Command Exists",
                                        "This command already exists as \"%s\"" % self.keys_list[' '.join(strokes)])
            warning.exec_()

    @staticmethod
    def get_keystrokes(run, parent=None):
        dialog = KeystrokeGui(parent)
        if run is False:
            if str(dialog.runinput.text()) != '':
                dialog.runinput.setDisabled(True)
            else:
                dialog.runLabel.hide()
                dialog.runinput.hide()
        result = dialog.exec_()
        if result == 1:
            cmd, label, run = dialog.get_cmd()
            return QtGui.QDialog.Accepted, cmd, label, run
        else:
            return QtGui.QDialog.Rejected, None, None, None


class HotkeyWidget(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self, None)
        self.button = Hotkey(13, "Button 1", 'lhyper z')
        self.layout = QtGui.QVBoxLayout(self)
        self.layout.setAlignment(QtCore.Qt.AlignLeft)
        self.layout.addWidget(self.button.btn)
        self.layout.addWidget(self.button.label)
        # self.button.btn.clicked.connect(self.test)



if __name__ == '__main__':
    app = QtGui.QApplication([])
    window = HotkeyWidget()
    window.show()
    app.exec_()
