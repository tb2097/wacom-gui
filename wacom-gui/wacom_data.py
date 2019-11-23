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
import xml.etree.ElementTree as ET
import math
import copy
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class Tablets:
    def __init__(self):
        self.tablets = {}
        self.device_data = {}
        self.db_path = "%s/data" % os.path.dirname(os.path.realpath(__file__))
        if not os.path.exists(self.db_path):
            self.db_path = "/usr/share/libwacom"
            if not os.path.exists(self.db_path):
                sys.exit("Error: libwacom not installed")
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
                if dev == '':
                    break
                dev_attr = dev.rstrip().split("\t")
                name = dev.rsplit(' %s' % attr[dev_attr[2]], 1)[0]
                if name[-3:] in ["Pen", "Pad"]:
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
        for device, inputs in detected.iteritems():
            if device[-4:] == '(WL)':
                dev_type = device[:-5]
            else:
                dev_type = device
            try:
                # Cintiq Pro 24 hack
                if dev_type == 'Wacom Cintiq Pro 24':
                    if 'Wacom Cintiq Pro 24 P' in self.device_data.keys():
                        dev_type = 'Wacom Cintiq Pro 24 P'
                    else:
                        dev_type = 'Wacom Cintiq Pro 24 PT'
                # ExpressKeys hack
                if dev_type == 'Wacom Express Key Remote':
                    dev_type = 'Wacom ExpressKey Remote'
                # PTH-660/PTH-860 hack
                if dev_type.startswith('Wacom Intuos Pro') :
                    if dev_type not in self.device_data.keys():
                        dev_type = dev_type.replace("Pro", "Pro 2")
                # One Wacom hack
                if dev_type == 'Wacom One by Wacom S':
                    dev_type = 'One by Wacom (small)'
                devID = self.device_data[dev_type]['devID']
                if self.device_data[dev_type]['devID'] not in self.tablets.keys():
                    self.tablets[devID] = []
                # assume if it's the same device it has the same inputs for all connected
                if 'pad' in detected[device]:
                    dev_count = detected[device]['pad']['id'].__len__()
                else :
                    dev_count = 1
                for x in range(0, dev_count):
                    idx = self.tablets[devID].__len__()
                    self.tablets[devID].append(copy.deepcopy(self.device_data[dev_type]))
                    self.tablets[devID][idx]['cname'] = device
                for dev_input in inputs:
                    idx = self.tablets[devID].__len__() - detected[device][dev_input]['id'].__len__()
                    for instance in sorted(detected[device][dev_input]['id']):
                        self.tablets[devID][idx][dev_input]['id'] = instance
                        idx = idx + 1
                # remove devices that are not available
                for dev in self.tablets.keys():
                    for device in self.tablets[dev]:
                        for id in ['touch', 'stylus', 'eraser', 'cursor', 'pad']:
                            if id in device.keys():
                                if 'id' not in device[id].keys():
                                    del device[id]
            except:
                warning = QMessageBox(QMessageBox.Warning, "Unknown Device",
                                      "Device information for \"%s\" not found." % dev_type)
                warning.exec_()


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
            elif line.startswith('Name=') :
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
                    if line.startswith('ModelName') :
                        self.device_data[cur_device]['ModelName'] = line.split('=')[1]
                    # get usb id; will use for BT as well to simplify mapping
                    elif "DeviceMatch=" in line:
                        # don't include serial devices
                        if 'serial' in line:
                            del self.device_data[cur_device]
                            cur_device = None
                        else:
                            self.device_data[cur_device]['devID'] = line.split('=')[1].split(';')[0][-4:]
                    elif "Layout=" in line:
                        self.device_data[cur_device]['svg'] = line.split('=')[1]
                    # Reversible means it can be flipped
                    elif "Reversible=" in line:
                        if "true" in line:
                            self.device_data[cur_device]['stylus']['rotate'] = True
                        else:
                            self.device_data[cur_device]['stylus']['rotate'] = False
                    elif "Ring=true" in line:
                        self.device_data[cur_device]['pad']['buttons']['RingUp'] = \
                            {'bid': 'AbsWheelUp', 'orient': 'Left'}
                        self.device_data[cur_device]['pad']['buttons']['RingDown'] = \
                            {'bid': 'AbsWheelDown', 'orient': 'Left'}
                    elif "Ring2=true" in line:
                        self.device_data[cur_device]['pad']['buttons']['Ring2Up'] = \
                            {'bid': 'AbsWheel2Up', 'orient': 'Right'}
                        self.device_data[cur_device]['pad']['buttons']['Ring2Down'] = \
                            {'bid': 'AbsWheel2Down', 'orient': 'Right'}
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
                                    'bid': 'Button %d' % butid,
                                    'orient': dir}
                        except Exception:
                            pass
                    if 'Touchstrip' in line:
                        touch_but = line.split("=")[1].split(';')
                        try:
                            for but in touch_but:
                                side = self.device_data[cur_device]['pad']['buttons']['Button%s' % but]['orient']
                                if line.split('=')[0][-1:] == '2':
                                    self.device_data[cur_device]['pad']['buttons']['Strip2Up'] = {
                                        'bid': "Strip%sUp" % side,
                                        'orient': side}
                                    self.device_data[cur_device]['pad']['buttons']['Strip2Down'] = {
                                        'bid': "Strip%sUp" % side,
                                        'orient': side}
                                else:
                                    self.device_data[cur_device]['pad']['buttons']['StripUp'] = {
                                        'bid': "Strip%sUp" % side,
                                        'orient': side}
                                    self.device_data[cur_device]['pad']['buttons']['StripDown'] = {
                                        'bid': "Strip%sUp" % side,
                                        'orient': side}
                        except Exception as e:
                            pass

        for device, data in self.device_data.items():
            # get button svg info
            if 'pad' in data.keys():
                if 'buttons' in data['pad'].keys():
                    if data['pad']['buttons'].__len__() == 0:
                        del data['pad']['buttons']
                    else:
                        self.pretty_svg(device)


    def pretty_svg(self, device):
        try:  # Attempt to load button map from SVG
                # trying to optimize SVG file
                tree = ET.parse("%s/layouts/%s" % (self.db_path, self.device_data[device]['svg']))
                root = tree.getroot()
                svg = ''
                xmin = 99999
                ymin = 99999
                xmax = 0
                ymax = 0
                for elem in root.iter():
                    if elem.tag.split('}')[1] == 'g':
                        if svg == '':
                            svg = '\n\t<g>'
                        else:
                            svg = '%s\n\t</g>\n\t<g>' % svg
                    elif elem.tag.split('}')[1] == 'rect':
                        svg = '%s\n\t\t<rect' % svg
                        # get attr
                        for attr in elem.attrib:
                            svg = "%s\n\t\t\t%s=\"%s\"" % (svg, attr, elem.attrib[attr])
                        svg = "%s />" % svg
                        if elem.attrib['id'] in self.device_data[device]['pad']['buttons'].keys():
                            but_info = self.device_data[device]['pad']['buttons'][elem.attrib['id']]
                            if but_info['orient'] in ['Left', 'Right']:
                                self.device_data[device]['pad']['buttons'][elem.attrib['id']]['pos'] = \
                                    "%06.f" % float(elem.attrib['y'])
                            else:
                                self.device_data[device]['pad']['buttons'][elem.attrib['id']]['pos'] = \
                                    "%06.f" % float(elem.attrib['x'])
                        if xmin > float(elem.attrib['x']):
                            xmin = float(elem.attrib['x'])
                        if ymin > float(elem.attrib['y']):
                            ymin = float(elem.attrib['y'])
                        if xmax < float(elem.attrib['x']) + float(elem.attrib['width']):
                            xmax = float(elem.attrib['x']) + float(elem.attrib['width'])
                        if ymax < float(elem.attrib['y']) + float(elem.attrib['height']):
                            ymax = float(elem.attrib['y']) + float(elem.attrib['height'])
                    elif elem.tag.split('}')[1] == 'path':
                        svg = '%s\n\t\t<path' % svg
                        # get attr
                        for attr in elem.attrib:
                            #TODO: this fix path problem?
                            if not attr.startswith("{"):
                                svg = "%s\n\t\t\t%s=\"%s\"" % (svg, attr, elem.attrib[attr])
                        svg = "%s\n\t\t\tfill=\"none\" />" % svg
                        if elem.attrib['id'] in self.device_data[device]['pad']['buttons'].keys():
                            but_info = self.device_data[device]['pad']['buttons'][elem.attrib['id']]
                            if but_info['orient'] in ['Left', 'Right']:
                                if 'y' in elem.attrib.keys():
                                    self.device_data[device]['pad']['buttons'][elem.attrib['id']]['pos'] = \
                                        "%06.f" % float(elem.attrib['y'])
                                elif 'd' in elem.attrib.keys():
                                    d = elem.attrib['d'].split(' ')
                                    if d[1].find(',') != -1:
                                        elem.attrib['y'] = d[1].split(',')[1]
                                    else:
                                        elem.attrib['y'] = d[2]
                                    self.device_data[device]['pad']['buttons'][elem.attrib['id']]['pos'] = \
                                        "%06.f" % float(elem.attrib['y'])
                            else:
                                if 'x' in elem.attrib.keys():
                                    self.device_data[device]['pad']['buttons'][elem.attrib['id']]['pos'] = \
                                        "%06.f" % float(elem.attrib['x'])
                                elif 'd' in elem.attrib.keys():
                                    d = elem.attrib['d'].split(' ')
                                    if d[1].find(',') != -1:
                                        elem.attrib['x'] = d[1].split(',')[0]
                                    else:
                                        elem.attrib['x'] = d[1]
                                    elem.attrib['x'] = elem.attrib['d'].split(' ')[1]
                                    self.device_data[device]['pad']['buttons'][elem.attrib['id']]['pos'] = \
                                        "%06.f" % float(elem.attrib['x'])
                    elif elem.tag.split('}')[1] == 'circle':
                        svg = '%s\n\t\t<circle' % svg
                        # get attr
                        for attr in elem.attrib:
                            svg = "%s\n\t\t\t%s=\"%s\"" % (svg, attr, elem.attrib[attr])
                        svg = "%s />" % svg
                        if elem.attrib['id'] in self.device_data[device]['pad']['buttons'].keys():
                            but_info = self.device_data[device]['pad']['buttons'][elem.attrib['id']]
                            if but_info['orient'] in ['Left', 'Right']:
                                self.device_data[device]['pad']['buttons'][elem.attrib['id']]['pos'] = \
                                    "%06.f" % float(elem.attrib['cy'])
                            else:
                                self.device_data[device]['pad']['buttons'][elem.attrib['id']]['pos'] = \
                                    "%06.f" % float(elem.attrib['cx'])
                        if xmin > float(elem.attrib['cx']) - math.ceil(float(elem.attrib['r'])):
                            xmin = float(elem.attrib['cx']) - math.ceil(float(elem.attrib['r']))
                        if ymin > float(elem.attrib['cy']) - math.ceil(float(elem.attrib['r'])):
                            ymin = float(elem.attrib['cy']) - math.ceil(float(elem.attrib['r']))
                        if xmax < float(elem.attrib['cx']) + math.ceil(float(elem.attrib['r'])):
                            xmax = float(elem.attrib['cx']) + math.ceil(float(elem.attrib['r']))
                        if ymax < float(elem.attrib['cy']) + math.ceil(float(elem.attrib['r'])):
                            ymax = float(elem.attrib['cy']) + math.ceil(float(elem.attrib['r']))
                    elif elem.tag.split('}')[1] == 'text':
                        svg = '%s\n\t\t<text' % svg
                        # get attr
                        for attr in elem.attrib:
                            svg = "%s\n\t\t\t%s=\"%s\"" % (svg, attr, elem.attrib[attr])
                        label = elem.attrib['id'].split('Label')[1]
                        label = label.replace('CCW', "Up")
                        label = label.replace('CW', "Down")
                        if label in self.device_data[device]['pad']['buttons'].keys():
                            but_info = self.device_data[device]['pad']['buttons'][label]
                            if but_info['orient'] in ['Left', 'Right']:
                                self.device_data[device]['pad']['buttons'][label]['pos'] = \
                                    "%06.f" % float(elem.attrib['y'])
                            else:
                                self.device_data[device]['pad']['buttons'][label]['pos'] = \
                                    "%06.f" % float(elem.attrib['x'])
                        svg = """%s
                            stroke="none"
                            fill="#6DD7E8">%s</text>""" % (svg, label)
                        if xmin > float(elem.attrib['x']):
                            xmin = float(elem.attrib['x'])
                        if ymin > float(elem.attrib['y']):
                            ymin = float(elem.attrib['y'])
                        if xmax < float(elem.attrib['x']):
                            xmax = float(elem.attrib['x'])
                        if ymax < float(elem.attrib['y']):
                            ymax = float(elem.attrib['y'])
                svg = '%s\n\t</g>\n</svg>' % svg
                # TODO: fix this documentation
                if True:
                # if not os.path.isfile("/tmp/%s" % self.device_data[device]['svg']):
                    # shift every line to eliminate extra vertical whitespace...
                    svg_write = ''
                    yshift = ymin - 20
                    if yshift > 0:
                        for line in svg.split('\n'):
                            if 'sodipodi' in line:
                                line = "sodipodi:%s" % line.split('}')[1]
                                svg_write = "%s\n%s" % (svg_write, line)
                            else:
                                if 'y="' in line and 'ry' not in line:
                                    val = line.split('"')
                                    svg_write = "%s\n%s\"%d\"" % (svg_write, val[0], float(val[1]) - yshift)
                                elif 'd="' in line and 'id="' not in line:
                                    val = line.split('"')
                                    points = val[1].split()
                                    subs = [" ".join(points[i:i + 3]) for i in range(0, len(points), 3)]
                                    d = "%s\"" % val[0]
                                    for sub in subs:
                                        if sub[0] == 'M' or sub[0] == 'L':
                                            attrs = sub.split()
                                            attrs[2] = str(float(attrs[2]) - float(yshift))
                                            d = "%s %s" % (d, " ".join(attrs))
                                        else:
                                            d = "%s %s" % (d, sub)
                                    d = "%s\"" % d
                                    svg_write = "%s\n%s" % (svg_write, d)
                                else:
                                    svg_write = "%s\n%s" % (svg_write, line)
                    if svg_write != '':
                        svg = svg_write
                    # shift x values if it is too wide
                    if xmax >= 500:
                        xshift = 300  # shift over by 200 units in the x coord
                        svg_write = ''
                        for line in svg.split('\n'):
                            if 'sodipodi' in line:
                                line = "sodipodi:%s" % line.split('}')[1]
                                svg_write = "%s\n%s" % (svg_write, line)
                            else:
                                if 'x="' in line and 'rx' not in line:
                                    val = line.split('"')
                                    if float(val[1]) >= 500.0:
                                        svg_write = "%s\n%s\"%d\"" % (svg_write, val[0], float(val[1]) - xshift)
                                    else:
                                        svg_write = "%s\n%s\"%d\"" % (svg_write, val[0], float(val[1]))
                                elif 'd="' in line and 'id="' not in line:
                                    val = line.split('"')
                                    points = val[1].split()
                                    subs = [" ".join(points[i:i + 3]) for i in range(0, len(points), 3)]
                                    d = "%s\"" % val[0]
                                    for sub in subs:
                                        if sub[0] == 'M' or sub[0] == 'L':
                                            attrs = sub.split()
                                            if float(attrs[1]) >= 500.0:
                                                attrs[1] = str(float(attrs[1]) - float(xshift))
                                            d = "%s %s" % (d, " ".join(attrs))
                                        else:
                                            d = "%s %s" % (d, sub)
                                    d = "%s\"" % d
                                    svg_write = "%s\n%s" % (svg_write, d)
                                else:
                                    svg_write = "%s\n%s" % (svg_write, line)
                    # write top of svg file
                    if xmax >= 500:
                        svg = """<svg
                           style="color:#000000;stroke:#7f7f7f;fill:#222222;stroke-width:.5;font-size:8"
                           width="%s"
                           height="%s">
                           <g>
                               <rect
                                   rx="0"
                                   ry="0"
                                   x="0"
                                   y="0"
                                   width="%s"
                                   height="%s"
                                   stroke="none"
                                   fill="#111111"/>
                            </g>%s""" % (xmax - 290, (ymax -yshift) + 20, xmax - 290, (ymax -yshift) + 20, svg_write)
                    else:
                        if not svg.strip().startswith("<g>"):
                            svg = "<g>%s" % svg
                        svg = """<svg
                           style="color:#000000;stroke:#7f7f7f;fill:#222222;stroke-width:.5;font-size:8"
                           width="%s"
                           height="%s">
                           <g>
                               <rect
                                   rx="0"
                                   ry="0"
                                   x="0"
                                   y="0"
                                   width="%s"
                                   height="%s"
                                   stroke="none"
                                   fill="#111111"/>
                            </g>%s""" % (xmax + 50, (ymax - yshift) + 20, xmax + 50, (ymax - yshift) + 20, svg)
                    f = open("/tmp/%s" % self.device_data[device]['svg'], "w")
                    f.write(svg)
                    f.close()

        except Exception as e:
            print (e)
