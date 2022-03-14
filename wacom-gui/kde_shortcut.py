#!/usr/bin/env python
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: Copyright © 2021 Jason Gerecke <jason.gerecke@wacom.com>
# SPDX-License-Identifier: MIT
"""
# Module

This module provides the ability to add a keyboard shortcut to KDE by
modifying its config files and trigger the daemons to reload. Only
two functions are public: `create` and `activate`. Please see their
documentation for use, or read the commented-out `main` block at the
end of this file for an example.


# KDE Shortcuts

Keyboard shortcuts are handled by the KDE desktop through a pair of
config files and their associated background services. The first file,
`khotkeysrc`, is used by the "khotkeys" module of the KDE Daemon (KDED).
The second file, `kglobalshortcutsrc` is used by the "kglobalaccel"
daemon. The former defines the shortcut itself: e.g. whether it is
enabled, what action to take, how it can be triggered, etc. The latter
is responsible for listening to the keyboard and triggering events as
required.

The documentation contained here was obtained through a combination of
reverse-engineering on CentOS 7.9 and analysis of the khotkeys code
(part of the KDE4 kde-workspace source package and standalone in KDE5).


## Config File Anatomy

The two relevant configuration files can be found inside of the KDE
configuration directory. This may be in one of a few different spots
depending on:

* KDE4: ${KDEHOME}/share/config
* KDE5: ${XDG_CONFIG_HOME}

The default value of the "${KDEHOME}" environment variable is `${HOME}/
.kde4`. The default value of the "${XDG_CONFIG_HOME}" environment
variable is `${HOME}/.config`. If KDE is running, the version number
can be determined by checking the "${KDE_SESSION_VERSION}" environment
variable.


:: khotkeysrc

The khotkeys KDED module is quite flexible and allows the definition of
many kinds of shortcuts that go beyond the scope of this documentation.
The file is capable of describing multiple "groups" of related shortcuts
(with optional "conditions" for the group being used), multiple "triggers"
for each shortcut (which may be keypresses or mouse gestures), and multiple
"actions" to be performed by the shortcut (e.g. command / URL launching,
keyboard input, or dbus calls). All of this leads to a rather complicated
data structure when serialized to disk.

The following is an example of a template that could be filled in to add
a new keyboard shortcut that launches a command:

~~~
[Data_{n}]
Name={name}
Comment={comment}
Enabled=true
Type=SIMPLE_ACTION_DATA

[Data_{n}Actions]
ActionsCount=1

[Data_{n}Actions0]
CommandURL={command}
Type=COMMAND_URL

[Data_{n}Triggers]
Comment=Simple_action
TriggersCount=1

[Data_{n}Triggers0]
Key={shortcut}
Type=SHORTCUT
Uuid={uuid}

[Data_{n}Conditions]
Comment=
ConditionsCount=0
~~~

You might, for instance, replace the template's Python f-string style
variables with values like the following:

~~~
import uuid

n = 1
name = 'Example shortcut'
comment = 'This is an example of a keyboard shortcut to launch the terminal.\\n\\nComments like this can contain simple formatting, "quotations", etc.'
command = 'konsole'
shortcut = 'Ctrl+1'
uuid = f'{{{uuid.uuid4()}}}'
~~~

The value of `n` must be within the range of 1..{N} (inclusive), where
{N} is the value of the `Data` group's `DataCount` key. This key should
be incremented or decremented if a group is inserted or deleted. Note
that inserting and deleting shortcuts may also require a significant
number of the group names to be rewritten...

Curiously, despite KDE's documentation indicating otherwise, the khotkeys
module is very sensitive to the use of ' = ' instead of '=' in the config
file. Using the former may result in unexpected issues.


:: kglobalshortcutsrc

The kglobalaccel daemon uses this file to determine what actions to
trigger when certian keyboard keys are pressed. In the case of shortcuts
handled by khotkeys, the UUID is used to link the two configurations
together.

Interestingly, this reliance on UUID technically means that only the
key sequence defined in this file matters. If the kglobalhsortcutsrc
and khotkeysrc files disagree on what key sequence will trigger a
shortcut, the value in kglobalshortcutsrc "wins".

The following template should be filled in with the same data used in
the khotkeys template for consistency:

~~~
[khotkeys]
{uuid}={shortcut},none,{name}
~~~


## Config File Updating

The khotkeys module and kglobalaccel daemon need to re-read their config
files after changes are made. The former can be commanded to do so over
dbus but the latter appears to only be possible by restarting the daemon.

The following commands could be run from the shell, for example, to cause
both to re-read their configuration. It is sufficient to only trigger a
re-read in a single service if only its configuration changed.

~~~
$ qdbus org.kde.kded /modules/khotkeys reread_configuration
$ kquitapp kglobalaccel && kglobalaccel
~~~
"""

from platform import python_version
if python_version()[0] == '2':
    import configparser as configparser
    from io import StringIO
elif python_version()[0] == '3':
    import configparser
    from io import StringIO

import os
import re
import uuid
from collections import OrderedDict


def _kde4ConfigPath():
    """
    Return a path to the configuration path used by KDE 4.
    """
    defaulthome = os.path.join(os.environ['HOME'], '.kde');
    kdehome = os.environ.get('KDEHOME', defaulthome)
    return os.path.join(kdehome, 'share', 'config')

def _kde5ConfigPath():
    """
    Return a path to the configuration path used by KDE 5.
    """
    defaultconfig = os.path.join(os.environ['HOME'], '.config')
    kdeconfig = os.environ.get('XDG_CONFIG_HOME', defaultconfig)
    return kdeconfig

def _kdeConfigPath(version=None):
    """
    Return a configuration path for an arbitrary KDE version.
    
    This function tries to be clever about detecting the most likely
    path intended. You can request a specific version by providing it
    as an argument. This function will raise an exception if no version
    is explicitly requested and no path is implicitly found.
    """
    if version is None:
        # Use the version of the currently running KDE session, if possible.
        try:
            version = int(os.environ['KDE_SESSION_VERSION'])
        except:
            pass

    if version is None:
        # If the user is not currently running KDE, see if either path exists.
        # Prefer most recent KDE path that is found.
        if os.path.exists(_kde4ConfigPath()):
            version = 4
        if os.path.exists(_kde5ConfigPath()):
            version = 5
        if version is None:
            raise ValueError("Could not automatically discover a KDE version.")

    if version == 4:
        return _kde4ConfigPath()
    if version == 5:
        return _kde5ConfigPath()

def _dumpSection(parser, section):
    """
    For debugging use: prints out the contents of a single section loaded
    by the parser.
    """
    print("======" + section + "======")
    print(parser.items(section))

def _dumpKhotkeysRc():
    """
    For debugging use: prints out the contents of the entire khotkeysrc
    file as read by the parser.
    """
    config_path = os.path.join(_kdeConfigPath(), 'khotkeysrc')
    parser = _KdeConfigParser()
    parser.read(config_path)
    for section in parser.sections():
        dumpSection(parser, section)


class _KdeConfigParser(configparser.RawConfigParser):
    """
    Custom configuration parser designed for KDE files.
    
    This parser extends the RawConfigParser with necessary default options
    and some convenience functions.
    """
    
    def __init__(self):
        configparser.RawConfigParser.__init__(self, allow_no_value = True)
        self.optionxform = str

    def as_dict(self):
        dictionary = OrderedDict()
        for section in self.sections():
            dictionary[section] = OrderedDict(self.items(section))
        return dictionary

    def as_str(self):
        sio = StringIO()
        configparser.RawConfigParser.write(self, sio)
        outstr = sio.getvalue()
        outstr = re.sub(r'(^[^=]+) = ', r'\1=', outstr, flags=re.M)
        return outstr

    def clear(self):
        for section in self.sections():
            self.remove_section(section)

    def read_dict(self, dictionary, source='<dict>'):
        self.clear()
        for section, opts in list(dictionary.items()):
            self.add_section(section)
            for option, value in list(opts.items()):
                self.set(section, option, value)

    def write(self, fileobj):
       outstr = self.as_str()
       fileobj.write(outstr)

def _addShortcutSection(data, parent, value):
    """
    Create a new "Data_{N}" section for a khotkeys shortcut.
    
    This function takes a dictionary of values and assigns them to a
    new "Data_{N}" section of the khotkeys configuration. This function
    takes care of updating the number of declared data sections and
    assigning an appropriate section name from that count.

    Parameters
    ----------
    data : dict
        A dictionary representing the khotkeys configuration.
    parent : str
        The identifier for the parent Data collection to embed the new
        shortcut into. This should be the empty string ("") to embed
        at the top level or the name of a specific parent's identifier
        (e.g. "3" to embed in the "Data_3" group or "3_1" to embed in
        the "Data_3_1" group).
    value : dict
        Dictionary data to be associated with the new section.

    Returns
    -------
    str
        Identifier for the newly-created Data section
    """
    if parent == '':
        parent_name = 'Data'
    else:
        parent_name = 'Data_{}'.format(parent)
    count = int(data[parent_name]['DataCount'])
    count = count + 1
    data[parent_name]['DataCount'] = count
    # Identifier uses one-based indexing
    if parent == '':
        ident = count
    else:
        ident = parent + "_" + count
    ident_name = 'Data_{}'.format(ident)
    data[ident_name] = value
    return ident

def _addShortcutSubsection(data, ident, subsection, value):
    """
    Create a new "Data_{N}{Foo}" subsection for a khotkeys shortcut.
    
    This function takes a dictionary of values and assigns them to a
    new "Data_{N}{Foo}" section of the khotkeys configuration. This
    function takes care of updating the number of declared {Foo}
    sections and assigning an appropriate section name from that count.

    Parameters
    ----------
    data : dict
        A dictionary representing the khotkeys configuration.
    ident : str
        The identifier for the Data section that represents the shortcut
        being updated. For example, "3" to create a subsection of the
        "Data_3" section.
    value : dict
        Dictionary data to be associated with the new subsection.

    Returns
    -------
    int
        Index of the newly-created subsection
    """
    name = 'Data_{}{}'.format(ident, subsection)
    countkey = subsection + 'Count'
    if name not in data:
        data[name] = { countkey: 0 }
    if value is None:
        return None
    count = int(data[name][countkey])
    subsection_name = '{}{}'.format(name, count)
    data[name][countkey] = count + 1
    data[subsection_name] = value
    return count  # zero-based indexing

def _addShortcut(data, parent, name, command, shortcut, comment):
    """
    Add a new shortcut into the khotkeys configuration.
    
    This function creates the multiple sections of khotkeys configuration
    which define a keyboard shortcut that launches a command. No validation
    is performed to check for other conflicting shortcuts; you should
    perform such validation prior to calling this function.

    Parameters
    ----------
    data : dict
        A dictionary representing the khotkeys configuration.
    parent : str
        The identifier for the parent Data collection to embed the new
        shortcut into. This should be the empty string ("") to embed
        at the top level or the name of a specific parent's identifier
        (e.g. "3" to embed in the "Data_3" group or "3_1" to embed in
        the "Data_3_1" group).
    name : str
        Name to be be displayed in the khotkeys configuration.
    command : str
        Command to be executed by the shortcut. An absolute path is
        not required if the executable is in the system's PATH.
    shortcut : str
        Keyboard sequence used to trigger the shortcut. E.g. "Ctrl+3".
    comment : str
        Comment to be displayed in the khotkeys configuration.

    Returns
    -------
    uuid
        UUID of the newly-created shortcut
    """
    shortcut_uuid = '{{{}}}'.format(uuid.uuid4())
    ident = _addShortcutSection(data, parent, {'Name': name, 'Comment': comment, 'Enabled': 'true', 'Type': 'SIMPLE_ACTION_DATA'})
    _addShortcutSubsection(data, ident, 'Actions', {'Type': 'COMMAND_URL', 'CommandURL': command})
    _addShortcutSubsection(data, ident, 'Triggers',  {'Type': 'SHORTCUT', 'Key': shortcut, 'Uuid': shortcut_uuid})
    _addShortcutSubsection(data, ident, 'Conditions', None)
    return shortcut_uuid

def getShortcutData(data, ident):
    """
    Try to return basic information about the requested khotkeys shortcut.
    
    Looks for the provided identifier in the khotkeys configuration and
    returns information about the shortcut, if possible. If the identifier
    could not be found or it does not correspond to a simple command-launching
    keyboard shortcut, this function will return None.

    Parameters
    ----------
    data : dict
        A dictionary representing the khotkeys configuration.
    ident : str
        The identifier for the Data section that represents the shortcut
        of interest. For example, "3" to get information for the "Data_3"
        shortcut.

    Returns
    -------
    dict
        Dictionary of several relevant shortcut properties.
    """
    info = {}
    section_name = "Data_{}".format(ident)
    actions_name = "{}Actions".format(section_name)
    triggers_name = "{}Triggers".format(section_name)
    conditions_name = "{}Conditions".format(section_name)
    
    if section_name not in data:
        return None
    section_data = data[section_name]
    if section_data["Type"] != "SIMPLE_ACTION_DATA":
        return None
    info["Name"] = section_data["Name"]
    info["Comment"] = section_data["Comment"]
    info["Enabled"] = section_data["Enabled"]
    info["commands"] = []
    info["triggers"] = []

    count = int(data[actions_name]["ActionsCount"])
    for i in range(0, count):
        name = "{}{}".format(actions_name, i)
        action_data = data[name]
        if action_data["Type"] != "COMMAND_URL":
            return None
        info["commands"].append({"CommandURL": action_data["CommandURL"]})

    count = int(data[triggers_name]["TriggersCount"])
    for i in range(0, count):
        name = "{}{}".format(triggers_name, i)
        trigger_data = data[name]
        if trigger_data["Type"] != "SHORTCUT":
            return None
        info["triggers"].append({"Key": trigger_data["Key"], "Uuid": trigger_data["Uuid"]})

    return info

def _findShortcut(data, name = None, shortcut = None, uuid = None):
    """
    Search the provided khotkeys dict for a matching shortcut.
    
    This function searches through the khotkeys configuration for any
    shortcut which matches all of the provided paramters. Any parameter
    may be ignored by providing 'None' as its value.

    Parameters
    ----------
    name : str
        Name displayed in the khotkeys configuration. Set to None if this
        parameter should not be matched.
    shortcut : str
        Keyboard sequence used to trigger the shortcut. E.g. "Ctrl+3".
        Set to None if this parameter should not be matched.
    uuid : str
        UUID of the shortcut in the khotkeys configuration. Set to None if
        this parameter should not be matched.

    Returns
    -------
    bool
        True if a shortcut matching all requested properties was found,
        False otherwise.
    """
    data_pattern = re.compile('Data_\d+(_\d+)*$')
    for section, kvdata in list(data.items()):
        if re.match(data_pattern, section):
            ident = section.split("_", 1)[1]
            shortcut_data = getShortcutData(data, ident)
            if shortcut_data is None:
                continue

            name_match = name is None or shortcut_data["Name"] == name
            short_match = shortcut is None
            if not short_match:
                for trigger in shortcut_data["triggers"]:
                    if trigger["Key"] == shortcut:
                        short_match = True
                        break
            uuid_match = shortcut is None
            if not uuid_match:
                for trigger in shortcut_data["triggers"]:
                    if trigger["Uuid"] == uuid:
                        uuid_match = True
                        break

            if all((name_match, short_match, uuid_match)):
                return True
    return False

def _createShortcut(name, command, shortcut, comment=''):
    """
    Create a new shortcut in the khotkeys configuration.
    
    This function will attempt to add a new shortcut into the khotkeys
    file. It will check to ensure the shortcut does not already exist
    first (no other shortcut may share its name or keyboard sequence).
    If the check fails the function will return False and not make any
    modifications.

    Parameters
    ----------
    name : str
        Name to be be displayed in the khotkeys configuration.
    command : str
        Command to be executed by the shortcut. An absolute path is
        not required if the executable is in the system's PATH.
    shortcut : str
        Keyboard sequence used to trigger the shortcut. E.g. "Ctrl+3".
    comment : str
        Comment to be displayed in the khotkeys configuration.

    Returns
    -------
    bool
        True if changes were made to the khotkeysrc configuration file.
    """
    parser = _KdeConfigParser()
    config_path = os.path.join(_kdeConfigPath(), 'khotkeysrc')
    parser.read(config_path)

    data = parser.as_dict()
    if _findShortcut(data, name = name) or \
       _findShortcut(data, shortcut = shortcut):
        return None

    uuid = _addShortcut(data, '', name, command, shortcut, comment)
    parser.read_dict(data)
    
    with open(config_path + ".tmp", 'w') as output:
        parser.write(output)
    return uuid

def _createGlobal(shortcut_uuid, name, shortcut):
    """
    Create a new hotkey shortcut in the kglobalshortcutsrc config file.
    
    This function will attempt to add a new khotkeys shortcut into the
    kglobalshortcutsrc file. It does not perform any checking if the
    shortcut is already in use.

    Parameters
    ----------
    name : str
        Name to be be displayed in the khotkeys configuration.
    shortcut : str
        Keyboard sequence used to trigger the shortcut. E.g. "Ctrl+3".
    """
    parser = _KdeConfigParser()
    config_path = os.path.join(_kdeConfigPath(), 'kglobalshortcutsrc')
    parser.read(config_path)

    data = parser.as_dict()
    hotkeys = data['khotkeys']
    hotkeys[shortcut_uuid] = "{},{},{}".format(shortcut, "none", name)
    parser.read_dict(data)
    with open(config_path + ".tmp", 'w') as output:
        parser.write(output)

def create(name, command, shortcut, comment):
    """
    Create a new shortcut in the necessary KDE config files.
    
    This function will attempt to add a new shortcut into the two config
    files that control custom user shortcuts.

    Parameters
    ----------
    name : str
        Name to be be displayed in the khotkeys configuration.
    command : str
        Command to be executed by the shortcut. An absolute path is
        not required if the executable is in the system's PATH.
    shortcut : str
        Keyboard sequence used to trigger the shortcut. E.g. "Ctrl+3".
    comment : str
        Comment to be displayed in the khotkeys configuration.

    Returns
    -------
    bool
        True if changes were made to the configuration files.
    """
    shortcut_uuid = _createShortcut(name, command, shortcut, comment)
    if shortcut_uuid is not None:
        _createGlobal(shortcut_uuid, name, shortcut)
        return True
    else:
        return False

def activate():
    """
    Cause changes to the shortcut configuration files to become active.
    
    This function will replace the live config files with the temporary
    versions constructed by other functions and cause KDE to re-read its
    configuration files.
    """
    # Move the shortcuts into position
    hotkey_path = os.path.join(_kdeConfigPath(), 'khotkeysrc')
    global_path = os.path.join(_kdeConfigPath(), 'kglobalshortcutsrc')
    os.rename(hotkey_path + ".tmp", hotkey_path)
    os.rename(global_path + ".tmp", global_path)

    # Tell the services to restart
    ret1 = os.system("qdbus org.kde.kded /modules/khotkeys reread_configuration")
    ret2 = os.system("kquitapp kglobalaccel && kglobalaccel")

#if __name__ == '__main__':
#    if create('foo', 'gnome-calculator', 'Ctrl+3', 'this is a test'):
#        activate()
