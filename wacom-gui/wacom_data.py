#!/usr/bin/python
# -*- coding: utf-8 -*-

############################################
# load now gets device ids
# references saved config file, ie. 1: default, 2: blah, 3: bleh
# config file name loaded in order detected using ids
#
# tablet config now this format:
#     <device name>
############################################



import subprocess
import os
import sys
import xml.dom.minidom
import copy


class Tablets:
    def __init__(self):
        self.tablets = {}
        self.device_data = {}
        self.db_path = "%s/data" % os.path.dirname(os.path.realpath(__file__))
        self.get_connected_tablets()

    def get_connected_tablets(self):
        # check if tablet is actually detected
        p = subprocess.Popen("xsetwacom --list devices", shell=True, stdout=subprocess.PIPE)
        dev_names = p.communicate()[0].split('\n')
        # all devices must have a pad, use this as unique identifier
        detected = {}
        attr = {'type: TOUCH': 'touch',
                'type: STYLUS': 'stylus',
                'type: ERASER': 'eraser',
                'type: CURSOR': 'cursor',
                'type: PAD': 'pad'}
        try:
            for dev in dev_names:
                dev_attr = dev.rstrip().split("\t")
                name = dev.split(' %s' % attr[dev_attr[2]])[0]
                if "Pen" == name[-3:]:
                    name = name[:-4]
                elif "Finger" == name[-6:]:
                        name = name[:-7]
                if name not in detected:
                    detected[name] = {attr[dev_attr[2]]: {'id': [dev_attr[1].split()[1]]}}
                elif attr[dev_attr[2]] not in detected[name].keys():
                    detected[name][attr[dev_attr[2]]] = {'id': [dev_attr[1].split()[1]]}
                else:
                    detected[name][attr[dev_attr[2]]]['id'].append(dev_attr[1].split()[1])
        except Exception:
            pass
        self.__get_libwacom_data()
        self.tablets = {}
        for device in detected.keys():
            if device[-4:] == '(WL)':
                dev_type = device[:-5]
            else:
                dev_type = device
            devID = self.device_data[dev_type]['devID']
            if self.device_data[dev_type]['devID'] not in self.tablets.keys():
                self.tablets[devID] = []
            # assume if it's the same device it has the same inputs for all connected
            dev_count = detected[device]['pad']['id'].__len__()
            for x in range(0, dev_count):
                idx = self.tablets[devID].__len__()
                self.tablets[devID].append(copy.deepcopy(self.device_data[dev_type]))
                self.tablets[devID][idx]['cname'] = device
            for dev_input in detected[dev_type]:
                idx = self.tablets[devID].__len__() - detected[device][dev_input]['id'].__len__()
                for instance in sorted(detected[device][dev_input]['id']):
                    self.tablets[devID][idx][dev_input]['id'] = instance
                    idx = idx + 1

    def __get_libwacom_data(self):
        p = subprocess.Popen("libwacom-list-local-devices --database %s" % self.db_path, shell=True,
                             stdout=subprocess.PIPE)
        output = p.communicate()[0].split('\n')
        cur_device = None
        buttons = False
        for line in output:
            if line == '[Device]':
                cur_device = None
                buttons = False
            elif 'Name=' in line:
                cur_device = line.split('=')[1]
                if cur_device in self.device_data:
                    cur_device = None
                else:
                    self.device_data[cur_device] = {
                        'pad': {
                            'attr': {},
                            'buttons': {}},
                        'stylus': {},
                        'eraser': {},
                        'touch': {},
                        'cursor': {}}
                # check if this is a duplicate device
            elif cur_device is not None:
                if not buttons:
                    # get usb id; will use for BT as well to simplify mapping
                    if "DeviceMatch=" in line:
                        self.device_data[cur_device]['devID'] = line.split('=')[1].split(';')[0][-4:]
                    elif "Layout=" in line:
                        self.device_data[cur_device]['svg'] = line.split('=')[1]
                    # Reversible means it can be flipped
                    elif "Reversible=" in line:
                        if "true" in line:
                            self.device_data[cur_device]['pad']['attr']['rotate'] = True
                        else:
                            self.device_data[cur_device]['pad']['attr']['rotate'] = False
                    elif "Ring=true" in line:
                        self.device_data[cur_device]['pad']['buttons']['RingUp'] = {'cmd': 'AbsWheelUp'}
                        self.device_data[cur_device]['pad']['buttons']['RingDown'] = {'cmd': 'AbsWheelDown'}
                    elif "Ring2=true" in line:
                        self.device_data[cur_device]['pad']['buttons']['Ring2Up'] = {'cmd': 'AbsWheel2Up'}
                        self.device_data[cur_device]['pad']['buttons']['Ring2Down'] = {'cmd': 'AbsWheel2Down'}
                    elif "Touch=" in line:
                        if "true" in line:
                            self.device_data[cur_device]['pad']['attr']['touch'] = True
                        else:
                            self.device_data[cur_device]['pad']['attr']['touch'] = False
                            del self.device_data[cur_device]['touch']
                    elif "NumStrips=" in line:
                        if line.split('=')[1] == '1':
                            self.device_data[cur_device]['pad']['buttons']['StripUp'] = {}
                            self.device_data[cur_device]['pad']['buttons']['StripDown'] = {}
                        if line.split('=')[1] == '2':
                            self.device_data[cur_device]['pad']['buttons']['StripUp'] = {}
                            self.device_data[cur_device]['pad']['buttons']['StripDown'] = {}
                            self.device_data[cur_device]['pad']['buttons']['Strip2Up'] = {}
                            self.device_data[cur_device]['pad']['buttons']['Strip2Down'] = {}
                    # get button info now...
                    elif '[Buttons]' == line:
                        buttons = True
                else:
                    if line.split("=")[0] in ['Left', 'Right', 'Top', 'Bottom']:
                        dir = line.split('=')[0]
                        try:
                            for but in line.split('=')[1].split(';'):
                                butid = ord(but) - 64
                                # buttons 4 - 7 are "reserved" for scroll, so we move these
                                if butid > 3:
                                    butid = butid + 4
                                self.device_data[cur_device]['pad']['buttons']['Button%s' % but] = {
                                    'cmd': 'Button %d' % butid,
                                    'orient': dir}
                        except Exception:
                            pass
                    if 'TouchStrip' in line:
                        touch_but = line.split("=")[1].split(';')
                        try:
                            for but in touch_but:
                                side = self.device_data[cur_device]['pad']['buttons']['Button%s' % but]['orient']
                                del self.device_data[cur_device]['pad']['buttons']['Button%s' % but]
                                if line.split('=')[0][-1:] == '2':
                                    self.device_data[cur_device]['pad']['buttons']['Strip2Up'][
                                        'cmd'] = "Strip%sUp" % side
                                    self.device_data[cur_device]['pad']['buttons']['Strip2Down'][
                                        'cmd'] = "Strip%sDown" % side
                                else:
                                    self.device_data[cur_device]['pad']['buttons']['StripUp'][
                                        'cmd'] = "Strip%sUp" % side
                                    self.device_data[cur_device]['pad']['buttons']['StripDown'][
                                        'cmd'] = "Strip%sDown" % side
                        except Exception:
                            pass

        for device, data in self.device_data.items():
            # get button svg info
            if data['pad']['buttons'].__len__() == 0:
                del data['pad']['buttons']
            else:
                try:  # Attempt to load button map
                    XML = xml.dom.minidom.parse("%s/layouts/%s" % (self.db_path, self.device_data[device]['svg']))
                    XBase = XML.getElementsByTagName("svg")
                    data['pad']['buttons']['width'] = int(XBase[0].attributes["width"].value)
                    data['pad']['buttons']['height'] = int(XBase[0].attributes["height"].value)

                    YBase = XBase[0].getElementsByTagName("g")
                    tmp = 1
                except Exception:
                    tmp = 1
        tmp = 1

# tablet_test = tablet_data()
