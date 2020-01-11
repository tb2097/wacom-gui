#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from functools import partial
import json
import os
import re
import shutil
import subprocess
import random
import string
import keystroke


class Hotkey(QObject):
    def __init__(self, devid, blabel, bid, cmd, parent=None):
        super(Hotkey, self).__init__(parent)
        self.devid = devid
        self.id = bid
        self.cmd = cmd
        self.cwd = os.path.dirname(os.path.abspath(__file__))
        if self.cwd == '/usr/local/bin':
            self.cwd = '/usr/local/wacom-gui'
        self.btn = QPushButton()
        self.btn.setFocusPolicy(Qt.NoFocus)
        self.btn.setMaximumSize(90, 16)
        self.btn.setMinimumSize(90, 16)
        self.btn.setText(blabel)
        self.keymap = {}
        self.keymap_custom = {}
        self.keys_list = {}
        self.keys_custom_list = {}
        self.menu = QMenu()
        self.modifiers = QMenu("Modifier")
        self.mouse = QMenu("Mouse Click")
        self.scroll = QMenu("Pan/Scroll")
        self.keypress = QMenu("Keypress")
        self.custom = QMenu("Custom Keystrokes")
        self.common = {}
        self.menu_init()
        self.btn.clicked.connect(self.load_menu)
        self.get_custom()
        self.label = QLabel()
        self.label.setFont(QFont('SansSerif', 8))
        self.label.setAutoFillBackground(True)
        self.label.setFixedHeight(14)
        self.set_value(self.cmd, '')

    def menu_init(self):

        self.common = {"Letters": QMenu("Letters"),
                       "Numbers": QMenu("Numbers"),
                       "Special Characters": QMenu("Special Characters"),
                       "Control Keys": QMenu("Control Keys"),
                       "Function Keys": QMenu("Function Keys"),
                       "Keypad": QMenu("Keypad"),
                       "System Shortcuts": QMenu("System Shortcuts")
                       }
        self.menu.addAction("Disable", lambda: self.set_value(self.id, 'Disabled'))
        self.menu.addAction("Default", lambda: self.set_value(self.id, 'Default'))
        self.menu.addMenu(self.modifiers)
        self.menu.addMenu(self.mouse)
        self.menu.addMenu(self.scroll)
        self.menu.addMenu(self.keypress)
        self.menu.addMenu(self.custom)
        self.menu.addSeparator()
        self.menu.addAction("Keystroke...", lambda: self.get_keystroke(False))
        self.menu.addAction("Keystroke/Run...", lambda: self.get_keystroke(True))
        try:
            config = os.path.join(self.cwd, "keymap.json")
            if os.path.exists(config):
                with open(config, 'r') as f:
                    self.keymap = json.load(f)
        except Exception as e:
            print (e)
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

    def set_value(self, value, label):
        if value == 'Default' or label == 'Default':
            if 'button' in self.id.lower():
                value = self.id.split(' ')[1]
            elif self.id in ['AbsWheelUp', 'StripLeftUp', 'StripRightUp']:
                value = 4
            elif self.id in ['AbsWheelDown', 'StripLeftDown', 'StripRightDown']:
                value = 5
            xsetcmd = value
            self.label.setText('Default')
        elif value == 'Disabled' or label == 'Disabled':
            xsetcmd = 0
            value = 'Disabled'
            self.label.setText('Disabled')
        else:
            xsetcmd = self.xsetcmd_gen(value)
            self.label.setText(label)
        self.cmd = value
        self.get_custom()
        cmd = "xsetwacom --set %s %s %s" % (self.devid, self.id, xsetcmd)
        set_command = os.popen(cmd)
        if self.label.text() == 'Disabled':
            self.label.setStyleSheet("QLabel { background-color: rgba(255,0,0,120); }")
        elif self.label.text() == 'Default':
            self.label.setStyleSheet("QLabel { background-color: rgba(0,255,0,120); }")
        elif self.cmd in self.keys_list.keys():
            self.label.setText(self.keys_list[self.cmd])
            self.label.setStyleSheet("QLabel { background-color: rgba(200,200,200,120); }")
        elif value in self.keymap_custom.keys() and self.keymap_custom[value]['run'] != '':
            self.label.setText(self.keys_custom_list[self.cmd])
            self.label.setStyleSheet("QLabel { background-color: rgba(180,180,20,120); }")
            self.label.setToolTip("%s: %s" % (self.cmd, self.keymap_custom[value]['run']))
        else:
            self.label.setStyleSheet("QLabel { background-color: rgba(200,200,200,120); }")
            self.label.setToolTip(self.cmd)

    def get_custom(self):
        # get gui-specific keystrokes from file
        try:
            config = os.path.join(self.cwd, "custom.json")
            if os.path.exists(config):
                with open(config, 'r') as f:
                    self.keymap_custom = json.load(f)
                for cmd in self.keymap_custom.keys():
                    if self.keymap_custom[cmd]['run'] == '':
                        self.custom.addAction(self.keymap_custom[cmd]['label'],
                                              partial(self.set_value, cmd,
                                                      self.keymap_custom[cmd]['label']))
                    else:
                        self.custom.addAction("* %s" % self.keymap_custom[cmd]['label'],
                                              partial(self.set_value, cmd,
                                                      self.keymap_custom[cmd]['label']))
                    self.keys_custom_list[cmd] = self.keymap_custom[cmd]['label']
        except Exception as e:
            print (e)
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
                for key in self.keymap_custom.keys():
                    if key in user_custom.keys():
                        del user_custom[key]
                self.keymap_custom.update(user_custom)
        except Exception as e:
            print (e)

    def load_menu(self):
        # need to reset custom keys if changed elsewhere
        self.custom.clear()
        self.get_custom()
        self.menu.exec_(QCursor.pos())

    def get_keystroke(self, runcmd):
        ok, cmdstring, label, run, dconf = KeystrokeGui.get_keystrokes(runcmd, self.cmd)
        if ok == 1:
            # update custom keystroke db
            self.set_value(cmdstring, label)
            for key in self.keymap_custom.keys():
                if label == self.keymap_custom[key]['label'] or key == cmdstring:
                    del self.keymap_custom[key]
                    break
            if dconf == False:
                dconf = ''
            self.keymap_custom[cmdstring] = {'label': label,
                                             'run': run,
                                             'protected': 0,
                                             'dconf': dconf}
            config = os.path.expanduser("~/.wacom-gui")
            if not os.path.exists(config):
                os.mkdir(config)
            config = os.path.join(config, 'custom.json')
            if os.path.exists(config):
                shutil.copyfile(config, "%s.bak" % config)
            with open(config, 'w') as fout:
                json.dump(self.keymap_custom, fout, sort_keys=True, indent=4, separators=(',', ": "))

    def xsetcmd_gen(self, cmdstring):
        strokes = filter(None, re.split('{|}| ', str(cmdstring)))
        self.cmd = ' '.join(strokes)
        xsetcmd = ''
        button = False
        for stroke in strokes:
            if 'button' in stroke.lower():
                if xsetcmd.__len__() == 0:
                    xsetcmd = stroke
                else:
                    xsetcmd = "%s %s" % (xsetcmd, stroke)
                button = True
            else:
                if button:
                    xsetcmd = "%s %s" % (xsetcmd, stroke)
                    button = False
                else:
                    if xsetcmd.__len__() == 0:
                        xsetcmd = "key %s" % stroke
                    else:
                        xsetcmd = "%s key %s" % (xsetcmd, stroke)
        if re.match(r'^button \d+', xsetcmd):
            xsetcmd = xsetcmd.split(' ')[1]
        return xsetcmd

    def get_button_cmd(self):
        # return wacom id, xsetwacom id, cmd
        return (str(self.btn.text()), self.id, self.cmd)

    def is_toggle(self):
        if self.cmd == 'lhyper z':
            return True
        else:
            return False

class KeystrokeGui(QDialog, keystroke.Ui_Dialog):
    def __init__(self, cmd, parent=None):
        super(KeystrokeGui, self).__init__(parent)
        self.setupUi(self)
        self.cwd = os.path.dirname(os.path.abspath(__file__))
        if self.cwd == '/usr/local/bin':
            self.cwd = '/usr/local/wacom-gui'
        self.setWindowTitle("Define Keystroke")
        self.keymap = None
        self.keymap_custom = None
        self.dconf = None
        self.keys_list = {}
        self.keys_custom_list = {}
        self.menu = QMenu()
        self.modifiers = QMenu("Modifier")
        self.mouse = QMenu("Mouse Click")
        self.scroll = QMenu("Pan/Scroll")
        self.keypress = QMenu("Keypress")
        self.letter = QMenu("Letters")
        self.num = QMenu("Numbers")
        self.special = QMenu("Special Characters")
        self.ctrl = QMenu("Control Keys")
        self.fn = QMenu("Function Keys")
        self.keypad = QMenu("Keypad")
        self.custom = QMenu("Load")
        self.common = {}
        self.menu_init()
        self.get_custom()
        if cmd in self.keys_custom_list.keys():
            self.populate_fields(cmd)
        self.keystroke.setMenu(self.menu)

    def populate_fields(self, cmd):
        cmdline = ''
        strokes = filter(None, re.split('{|}| ', cmd))
        button = False
        for stroke in strokes:
            if 'button' in stroke:
                if cmdline.__len__() == 0:
                    cmdline = '{%s' % stroke
                else:
                    cmdline = "%s{%s" % (cmdline, stroke)
                button = True
            else:
                if button:
                    cmdline = "%s %s}" % (cmdline, stroke)
                    button = False
                else:
                    if cmdline.__len__() == 0:
                        cmdline = "{%s}" % stroke
                    else:
                        cmdline = "%s{%s}" % (cmdline, stroke)
        # for stroke in strokes:
        #    cmdline = "%s{%s}" % (cmdline, stroke)
        self.keystrokeinput.setText(cmdline)
        self.shortcutinput.setText(self.keymap_custom[cmd]['label'])
        if self.keymap_custom[cmd]['run'] != '':
            self.runinput.setText(self.keymap_custom[cmd]['run'])

    def menu_init(self):
        self.menu.addAction("Clear", lambda: self.clear_input())
        self.menu.addAction("Undo", lambda: self.remove_one())
        self.menu.addAction("Delete", lambda: self.delete_hotkey())
        self.menu.addMenu(self.custom)
        self.menu.addSeparator()
        self.menu.addMenu(self.modifiers)
        self.menu.addMenu(self.mouse)
        self.menu.addMenu(self.scroll)
        self.menu.addMenu(self.keypress)
        self.common = {"Letters": QMenu("Letters"),
                       "Numbers": QMenu("Numbers"),
                       "Special Characters": QMenu("Special Characters"),
                       "Control Keys": QMenu("Control Keys"),
                       "Function Keys": QMenu("Function Keys"),
                       "Keypad": QMenu("Keypad"),
                       "System Shortcuts": QMenu("System Shortcuts")
                       }
        # key keystrokes from file
        try:
            config = os.path.join(self.cwd, "keymap.json")
            if os.path.exists(config):
                with open(config, 'r') as f:
                    self.keymap = json.load(f)
        except Exception as e:
            print (e)
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
                    if key != 'Special Characters':
                        self.common[key].addAction(label, partial(self.set_value, cmd))
                    elif ' ' not in cmd:
                        self.common[key].addAction(label, partial(self.set_value, cmd))
                    self.keys_list[cmd] = label
        for key in sorted(self.common.keys()):
            if key != "System Shortcuts":
                self.keypress.addMenu(self.common[key])

    def get_custom(self):
        # get gui-specific keystrokes from file
        try:
            config = os.path.join(self.cwd, "custom.json")
            if os.path.exists(config):
                with open(config, 'r') as f:
                    self.keymap_custom = json.load(f)
                for cmd in self.keymap_custom.keys():
                    if self.keymap_custom[cmd]['run'] == '':
                        self.custom.addAction(self.keymap_custom[cmd]['label'],
                                              partial(self.load_custom, cmd,
                                                      self.keymap_custom[cmd]['run']))
                    else:
                        self.custom.addAction("* %s *" % self.keymap_custom[cmd]['label'],
                                              partial(self.load_custom, cmd,
                                                      self.keymap_custom[cmd]['run']))
                    self.keys_custom_list[cmd] = self.keymap_custom[cmd]['label']
        except Exception as e:
            print (e)
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
                                                  partial(self.load_custom, cmd,
                                                          user_custom[cmd]['run']))
                        else:
                            self.custom.addAction("* %s *" % user_custom[cmd]['label'],
                                                  partial(self.load_custom, cmd,
                                                          user_custom[cmd]['run']))
                        self.keys_custom_list[cmd] = user_custom[cmd]['label']
                self.keymap_custom.update(user_custom)
        except Exception as e:
            print (e)

    def load_custom(self, cmd, run):
        self.populate_fields(cmd)
        self.runinput.setText(run)

    def clear_input(self):
        self.keystrokeinput.setText("")
        self.shortcutinput.setText("")
        self.runinput.setText("")

    def remove_one(self):
        strokes = filter(None, re.split('{|}', str(self.keystrokeinput.text())))
        strokes.pop()
        newcmd = ''
        for stroke in strokes:
            newcmd = "%s{%s}" % (newcmd, stroke)
        self.keystrokeinput.setText(newcmd)

    def delete_hotkey(self):
        strokes = ' '.join(filter(None, re.split('{|}', str(self.keystrokeinput.text()))))
        if strokes in self.keymap_custom.keys():
            if str(self.shortcutinput.text()) == self.keymap_custom[strokes]['label']:
                if self.keymap_custom[strokes]['protected'] == 1:
                    warning = QMessageBox(QMessageBox.Warning, "Protected Shortcut",
                                                "This is a protected shortcut, it can not be removed.")
                    warning.exec_()
                else:
                    msg = 'Hotkey:       %s' % self.keystrokeinput.text()
                    if self.runinput.text().__len__() != 0:
                        msg = "%s\nCommand: %s" % (msg, self.runinput.text())
                    reply = QMessageBox.question(self, 'Delete Hotkey \'%s\'?' %self.shortcutinput.text(), msg,
                                                       QMessageBox.Yes, QMessageBox.No)
                    if reply == QMessageBox.Yes:
                        del self.keymap_custom[strokes]
                        config = os.path.expanduser("~/.wacom-gui")
                        if not os.path.exists(config):
                            os.mkdir(config)
                        config = os.path.join(config, 'custom.json')
                        if os.path.exists(config):
                            shutil.copyfile(config, "%s.bak" % config)
                        with open(config, 'w') as fout:
                            json.dump(self.keymap_custom, fout, sort_keys=True, indent=4, separators=(',', ": "))
                        self.clear_input()

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
        return str(self.keystrokeinput.text()), str(self.shortcutinput.text()), str(self.runinput.text()), self.dconf

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

    def run_hotkey_edit(self):
        # mouse presses not allowed
        xbkbmap = ''
        if 'button' in self.keystrokeinput.text():
            warning = QMessageBox(QMessageBox.Warning, "Invalid Command",
                                        "Mouse/Scroll clicks are not valid for keyboard shortcuts.")
            warning.exec_()
            return False
        strokes = filter(None, re.split('{|}| ', str(self.keystrokeinput.text())))
        # check input
        for idx, val in enumerate(strokes):
            if idx == 0 and val in self.keymap['Modifiers'].keys():
                modifier = True
                if self.keymap['Modifiers'][val] == 'Hyper':
                    xbkbmap = "<Mod4>"
                else:
                    xbkbmap = "<%s>" % self.keymap['Modifiers'][val]
            elif modifier and val in self.keymap['Modifiers'].keys():
                if self.keymap['Modifiers'][val] == 'Hyper':
                    xbkbmap = "%s<Mod4>" % xbkbmap
                else:
                    xbkbmap = "%s<%s>" % (xbkbmap, self.keymap['Modifiers'][val])
            elif modifier and val in self.keys_list.keys():
                if val == 'Caps_Lock':
                    warning = QMessageBox(QMessageBox.Warning, "Invalid Command",
                                                "Caps Lock is not valid for a keyboard shortcuts.")
                    warning.exec_()
                    return False
                elif idx < strokes.__len__() -1:
                    warning = QMessageBox(QMessageBox.Warning, "Invalid Command",
                                                "Only a single non-modifier character is allowed at the end of "
                                                "keyboard shortcuts.")
                    warning.exec_()
                    return False
                else:
                    xbkbmap = "%s%s" % (xbkbmap, val)
        if xbkbmap == '':
            return False
        # setup hotkeys
        custom = self.load_keyboard_shortcuts()
        # TODO: check if we're changing an existing hotkey
        idx = -1
        found = False
        cfg = '/tmp/wc_%s.cfg' % ''.join(random.SystemRandom().choice(string.ascii_uppercase) for _ in range(6))
        for entry in custom.keys():
            if int(entry.split('custom')[1]) > idx:
                idx = int(entry.split('custom')[1])
            # name match
            if custom[entry]['name'] == "'%s'" % self.shortcutinput.text() or \
                    custom[entry]['binding'] == "'%s'" % xbkbmap or \
                    custom[entry]['action'] == "'%s'" % self.runinput.text():
                # update entry
                custom[entry]['name'] = "'%s'" % self.shortcutinput.text()
                custom[entry]['binding'] = "'%s'" % xbkbmap
                custom[entry]['action'] = "'%s'" % self.runinput.text()
                found = True
                break
        if not found:
            new_entry = 'custom%d' % (idx + 1)
            custom[new_entry] = {'name': "'%s'" % self.shortcutinput.text(),
                                 'binding': "'%s'" % xbkbmap,
                                 'action': "'%s'" % self.runinput.text()}
        # generate config file
        try:
            config = os.path.expanduser("~/.wacom-gui")
            if not os.path.isdir(config):
                os.mkdir(config)
            config = os.path.join(config, "keybind.cfg")
            f = open(config, "w")
            for entry in custom:
                f.write("[%s]\naction=%s\nbinding=%s\nname=%s\n\n" %
                        (entry, custom[entry]['action'], custom[entry]['binding'], custom[entry]['name']))
            f.close()
            os.popen("dconf load /org/mate/desktop/keybindings/ < %s" % config)
            return xbkbmap
        except Exception as e:
            print (e)

    def load_keyboard_shortcuts(self):
        custom = {}
        p = subprocess.Popen("dconf dump /org/mate/desktop/keybindings/", shell=True, stdout=subprocess.PIPE)
        p.wait()
        output = p.communicate()[0].split('\n')
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

    def accept(self):
        # check if valid multi-key command
        strokes = filter(None, re.split('{|}| ', str(self.keystrokeinput.text())))
        # invalid new shortcut
        if strokes.__len__() < 1:
            warning = QMessageBox(QMessageBox.Warning, "Keystroke length too short",
                                        "Please enter more than a single keystroke to make a shortcut.")
            warning.exec_()
        # system shortcut
        elif ' '.join(strokes) in self.keys_list:
            warning = QMessageBox(QMessageBox.Warning, "System Keystroke Command",
                                        "This command can not be changed.")
            warning.exec_()
        # no shortcut name entered
        elif self.shortcutinput.text().__len__() <= 1:
            warning = QMessageBox(QMessageBox.Warning, "Shortcut Name Undefined",
                                        "Please provide a shortcut name before saving.")
            warning.exec_()
        # previously defined as shortcut
        elif ' '.join(strokes) in self.keys_custom_list.keys():
            if self.shortcutinput.text() != self.keys_custom_list[' '.join(strokes)]:
                if self.runinput.text() != '':
                    self.dconf = self.run_hotkey_edit()
                    if self.dconf != False:
                        super(KeystrokeGui, self).accept()
                    else:
                        warning = QMessageBox(QMessageBox.Warning, "Something happened...",
                                                    "Not sure why this happened, but it didn't work.")
                        warning.exec_()
                else:
                    super(KeystrokeGui, self).accept()
        # shortcut name used for a different shortcut
        elif self.shortcutinput.text() in self.keys_custom_list.values():
            if self.runinput.text() != '':
                self.dconf = self.run_hotkey_edit()
                if self.dconf != False:
                    super(KeystrokeGui, self).accept()
                else:
                    warning = QMessageBox(QMessageBox.Warning, "Something happened...",
                                                "Not sure why this happened, but it didn't work.")
                    warning.exec_()
            else:
                super(KeystrokeGui, self).accept()
        # check characters used in shortcut name
        elif set("[`~!@#$%^&*=+\\|}{'\":;/?><.,]$").intersection(str(self.shortcutinput.text())):
            warning = QMessageBox(QMessageBox.Warning, "Invalid Shortcut Name",
                                        "Please do not use special characters, except for _-()")
            warning.exec_()
        elif str(self.shortcutinput.text()) not in self.keys_custom_list.values():
            # check run
            if self.runinput.isHidden() == False:
                runcmd = str(self.runinput.text())
                # check if it is a valid file/command path to run
                if self.runinput.text().__len__() == 0:
                    super(KeystrokeGui, self).accept()
                elif self.cmd_path_search(runcmd.split(' ')[0]) is not None:
                    self.dconf = self.run_hotkey_edit()
                    if self.dconf != False:
                        super(KeystrokeGui, self).accept()
                else:
                    warning = QMessageBox(QMessageBox.Warning, "Invalid Command",
                                                "Command path is invalid or is not executable.")
                    warning.exec_()
            else:
                super(KeystrokeGui, self).accept()
            #else:
            #    warning = QMessageBox(QMessageBox.Warning, "Shortcut Name Exists",
            #                                "This shortcut name is already in use.")
            #    warning.exec_()
        elif str(self.shortcutinput.text()) != self.keys_list[' '.join(strokes)]:
            warning = QMessageBox(QMessageBox.Warning, "Keystroke Command Duplicate",
                                        "This command already exists as \"%s\"" % self.keys_list[' '.join(strokes)])
            warning.exec_()
        else:
            warning = QMessageBox(QMessageBox.Warning, "Keystroke Command Exists",
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
            cmd, label, run, dconf = dialog.get_cmd()
            cmd = ' '.join(filter(None, re.split('{|}| ', str(cmd))))
            return QDialog.Accepted, cmd, label, run, dconf
        else:
            return QDialog.Rejected, None, None, None, None


class HotkeyWidget(QWidget):
    def __init__(self, devid, blabel, bid, cmd):
        QWidget.__init__(self, None)
        self.button = Hotkey(devid, blabel, bid, cmd)
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignLeft)
        # self.layout.setMargin(0)
        self.layout.addWidget(self.button.btn)
        self.layout.addWidget(self.button.label)
        self.setMaximumSize(120, 40)
        self.setMinimumSize(120, 40)

    def reset(self):
        self.button.set_value(self.button.id, "Default")

    def is_toggle(self):
        return self.button.is_toggle()


if __name__ == '__main__':
    app = QApplication([])
    window = HotkeyWidget(13, "Button A", "Button 1", 'lhyper z')
    window.show()
    app.exec_()
