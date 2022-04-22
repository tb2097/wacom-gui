#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: Copyright © 2021 Jason Gerecke <jason.gerecke@wacom.com>
# SPDX-License-Identifier: MIT

"""
Add/remove keyboard shortcuts in XFCE.

This module allows you to quickly add a new keyboard shortcut to XFCE
or remove an existing shortcut. Two module-level functions wrap most
of the functionality to make this simple: `createShortcut()` and
`removeShortcut()`. The former, for example, takes care of checking
to make sure that the shortcut does not already exist and the latter
will refuse to remove a shortcut that does not match the expected
command and key sequence.
"""

from enum import Enum
import re
import subprocess


# Typically unavailable in Python 2.x
try:
    from typing import List, Optional, Text, Tuple
except ImportError:
    pass


_DEFAULT_ENCODING = "UTF-8"


class XfconfError(Exception):
    """Error in interfacing with xfconf database."""


class XfconfProptype(Enum):
    """Types of properties that can be stored in the xfconf database."""

    INT = "int"
    UINT = "uint"
    BOOL = "bool"
    FLOAT = "float"
    DOUBLE = "double"
    STRING = "string"


class XfconfInterface:
    """
    Interface for accessing the XFCE xfconf database.

    This class provides methods for interacting with XFCE's xfconf
    database. It can be used to view and change values, e.g. to
    adjust various user settings.

    This class relies heavily on the xfconf command-line interface
    and will not work if the necessary tool is not installed. Methods
    will return an error if this occurs, or if the executed command
    itself returns an error.
    """

    _QUERY_COMMAND = u"xfconf-query"

    @staticmethod
    def _execute(args):
        # type: (List[Text]) -> Tuple[Text, Text, int]
        try:
            proc = subprocess.Popen(
                args, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            stdout, stderr = proc.communicate()
        except OSError as _:
            raise XfconfError("xfconf interface is not avaialble")

        stdout_str = stdout.decode(_DEFAULT_ENCODING)
        stderr_str = stderr.decode(_DEFAULT_ENCODING)
        return (stdout_str, stderr_str, proc.returncode)

    @staticmethod
    def isInterfaceAvailable():
        # type: ()-> bool
        """
        Check if the interface to XFCE's xfconf database is available.

        This method should be used prior to calling anything else to
        ensure that we are able to access the xfconf database.

        Returns
        -------
        bool
            True if the interface is available, False otherwise
        """
        args = [XfconfInterface._QUERY_COMMAND]
        try:
            # pylint: disable-next=unused-variable
            stdout, stderr, retval = XfconfInterface._execute(args)
            return retval == 0
        except XfconfError as _:
            return False

    @staticmethod
    def list(channel):
        # type: (Text) -> List[Text]
        """
        List the properties available in the requested channel.

        Request the list of properties associated with the specified
        channel. If the channel does not exist, an empty list may
        be returned.

        Returns
        -------
        channel: List of Text
            Names of properties associated with the channel.

        Raises
        ------
        XfconfError
            If an error occurred while accessing xfconf
        """
        args = [XfconfInterface._QUERY_COMMAND, "--channel", channel, "--list"]
        # pylint: disable-next=unused-variable
        stdout, stderr, retval = XfconfInterface._execute(args)
        if retval != 0:
            raise XfconfError(stderr)
        return stdout.splitlines()

    @staticmethod
    def reset(channel, prop):
        # type: (Text, Text) -> None
        """
        Reset the requested property.

        Attempt to reset (i.e. clear, remove, or delete) the requested
        property. If the property does not exist, it is possible that
        no error will be raised.

        Raises
        ------
        XfconfError
            If an error occurred while accessing xfconf
        """
        args = [
            XfconfInterface._QUERY_COMMAND,
            "--channel",
            channel,
            "--property",
            prop,
            "--reset",
        ]
        # pylint: disable-next=unused-variable
        stdout, stderr, retval = XfconfInterface._execute(args)
        if retval != 0:
            raise XfconfError(stderr)

    @staticmethod
    def get(channel, prop):
        # type: (Text, Text) -> Text
        """
        Get the value of the requested property.

        Attempt to read the current value of the requested property.
        If the property does not exist, an exception may be raised.

        Parameters
        ----------
        channel: Text
            Name of the channel containing the property
        prop: Text
            Name of the property

        Returns
        -------
        Text
            Value of the requested property.

        Raises
        ------
        XfconfError
            If an error occurred while accessing xfconf
        """
        args = [
            XfconfInterface._QUERY_COMMAND,
            "--channel",
            channel,
            "--property",
            prop,
        ]
        # pylint: disable-next=unused-variable
        stdout, stderr, retval = XfconfInterface._execute(args)
        if retval != 0:
            raise XfconfError(stderr)
        return stdout.rstrip("\n")

    @staticmethod
    def set(channel, prop, value, create=False, proptype=None):
        # type: (Text, Text, Text, bool, Optional[XfconfProptype]) -> None
        """
        Set the value of the requested property.

        Attempt to set the value of the requested property to the
        provided value. If the property does not exist, an exception
        may be raised if the `create` flag is not set to `True`.

        Parameters
        ----------
        channel: Text
            Name of the channel containing the property
        prop: Text
            Name of the property
        value: Text
            Value to be assigned to the property
        create: bool, default=False
            Flag indicating if the property should be created if it does
            not already exist.
        proptype: XfconfProptype, optional
            Type of the property. Must be set if creating a property.

        Raises
        ------
        XfconfError
            If an error occurred while accessing xfconf
        """
        args = [
            XfconfInterface._QUERY_COMMAND,
            "--channel",
            channel,
            "--property",
            prop,
            "--set",
            value,
        ]
        if create:
            args.extend(["--create"])
        if proptype is not None:
            args.extend(["--type", proptype.value])
        # pylint: disable-next=unused-variable
        stdout, stderr, retval = XfconfInterface._execute(args)
        if retval != 0:
            raise XfconfError(stderr)


class XfceShortcut:
    """
    Definition of a keyboard shortcut structure in XFCE.

    Shortcuts in XFCE are defined in two parts: their namespace and
    the key sequence which triggers them. This class serves as a
    container to save us from having to pass the data everywhere as
    arbitrary tuples.
    """

    _CUSTOM_COMMAND_NAMESPACE = u"/commands/custom"

    def __init__(self, namespace, sequence):
        # type: (Optional[Text], Text) -> None
        """
        Define a new XFCE keyboard shortcut.

        This initializer defines a new XFCE shortcut with arbitrary
        namespace and sequence. You most likely want to use either
        the `anyShortcut()` or `customCommand()` constructors
        instead.

        Parameters
        ----------
        namespace: Text, Optional
            XFCE component which is in control of the shortcut.
            If this parameter is set to None, the shortcut will
            not be directly usable, but can be compared based on
            its sequence alone.
        sequence: Text
            Keyboard sequence which triggers the shortcut.
        """
        self.namespace = namespace
        self.sequence = sequence

    def __eq__(self, other):
        # type: (XfceShortcut, object) -> bool
        """Compare two shortcuts for equality."""
        if not isinstance(other, XfceShortcut):
            return NotImplemented
        if self.sequence != other.sequence:
            return False
        if self.namespace is None or other.namespace is None:
            return True
        return self.namespace == other.namespace

    @staticmethod
    def anyShortcut(sequence):
        # type: (Text) -> XfceShortcut
        """
        Define an XFCE shortcut for matching in any namespace.

        There may be instances where you want to provide a shortcut
        to the XFCE interface class methods but don't particularly
        are about what namespace the shortcut is defined for (e.g.
        searching to see if a sequence is in use). This method may
        be used to obtain a shortcut which will compare as equal to
        any shortcut with the same sequence, regardless of namespace.

        Parameters
        ----------
        sequence: Text
            Keyboard sequence which triggers the shortcut.

        Returns
        -------
        XfceShortcut
            A shortcut object which will match as equal to any
            other shortcut which shares the same sequence,
            regardless of namespace.
        """
        return XfceShortcut(None, sequence)

    @staticmethod
    def customCommand(sequence):
        # type: (Text) -> XfceShortcut
        """
        Define an XFCE shortcut for launching a custom command.

        XFCE defines a specific namespace for shortcuts that are to be
        used for launching custom commands. This method will return a
        shortcut which is a part of the correct namespace.

        Parameters
        ----------
        sequence: Text
            Keyboard sequence which triggers the shortcut.

        Returns
        -------
        XfceShortcut
            A shortcut object which is placed inside of the custom
            command namespace.
        """
        return XfceShortcut(XfceShortcut._CUSTOM_COMMAND_NAMESPACE, sequence)

    def isCustomCommand(self):
        # type: (XfceShortcut) -> bool
        """
        Check if this shortcut is intended to launch a custom command.

        Returns
        -------
        bool
            True if this shortcut is part of the custom command namespace,
            False otherwise.
        """
        return self.namespace == XfceShortcut._CUSTOM_COMMAND_NAMESPACE


class XfceShortcutInterface:
    """Interface for setting shortcuts in XFCE."""

    _KEYBOARD_SHORTCUT_CHANNEL = u"xfce4-keyboard-shortcuts"

    @staticmethod
    def _lookupShortcuts(shortcut):
        shortcuts = XfceShortcutInterface.shortcuts()
        return [x for x in shortcuts if x == shortcut]

    @staticmethod
    def normalizeKeySequence(sequence):
        # type: (Text) -> Text
        """Return a normalized version of the key sequence."""

        def yoinkAny(inputlist, canonical, matchset):
            origlen = len(inputlist)
            for item in matchset:
                while item in inputlist:
                    inputlist.remove(item)
            if origlen != len(inputlist):
                return [canonical]
            return []

        pattern = r"<[^>]+>|[^<>]+"
        elements = [x.title() for x in re.findall(pattern, sequence)]

        output = []
        output += yoinkAny(elements, "<Shift>", {"<Shift>"})
        output += yoinkAny(elements, "<Primary>", {"<Control>", "<Ctrl>", "<Primary>"})
        output += yoinkAny(elements, "<Alt>", {"<Alt>", "<Meta>"})
        output += yoinkAny(elements, "<Super>", {"<Super>", "<Hyper>"})

        assert len(elements) == 1
        key = elements[0]
        if len(key) == 1:
            key = key.lower()
        return "".join(output) + key

    @staticmethod
    def shortcuts():
        # type: () -> List[XfceShortcut]
        """
        List all currently defined shortcuts.

        Returns
        -------
        List of XfceShortcut
            List of all shortcuts that are currently defined.

        Raises
        ------
        XfconfError
            If an error occurred while accessing xfconf
        """
        output = XfconfInterface.list(XfceShortcutInterface._KEYBOARD_SHORTCUT_CHANNEL)
        result = []
        for line in output:
            data = line.rsplit("/", 1)
            assert len(data) == 2
            if data[0] == "":
                continue
            shortcut = XfceShortcut(data[0], data[1])
            result.append(shortcut)
        return result

    @staticmethod
    def findShortcuts(sequence):
        # type: (Text) -> List[XfceShortcut]
        """
        Search for a shortcut if you don't know its exact key sequence.

        It can be difficult to know beforehand exactly how a particular
        key sequence will be named in the XFCE database. In some cases this
        is because of inconsistent capitalization (e.g. "<Control>grave"
        but "<Control>Escape") and in others keys may be synonomous (e.g.
        "<Control>Escape" and "<Primary>Escape" on some platforms). This
        function tries to relieve you of dealing with this nonsense.

        You can pass in an an almost-arbitrary sequence like "<Alt>Delete
        <ctrl>". The output will be all the currently-defined sequences
        which are equivalent, e.g. "<Control><Alt>Delete" and "<Primary>
        <Alt>Delete" (if both of those were defined in the database).

        Parameters
        ----------
        shortcut: Text
            Keyboard sequence to search for.

        Returns
        -------
        List of XfceShortcut
            List of all shortcuts in the XFCE database that could be
            triggered by the key sequence.

        Raises
        ------
        XfconfError
            If an error occurred while accessing xfconf
        """
        sequence = XfceShortcutInterface.normalizeKeySequence(sequence)
        result = []
        for shortcut in XfceShortcutInterface.shortcuts():
            if (
                XfceShortcutInterface.normalizeKeySequence(shortcut.sequence)
                == sequence
            ):
                result.append(shortcut)
        return result

    @staticmethod
    def getShortcutCommand(shortcut):
        # type: (XfceShortcut) -> Optional[Text]
        """
        Return the command associated with a shortcut, if set.

        Shortcuts are case- and order-sensitive (i.e. `<Control><Alt>
        Escape`, `<Alt><Control>Escape`, and `<Control><Alt>escape` are
        all considered distinct). To ensure you query the desired shortcut
        it is strongly advised to first use `findShortcut()` to get the
        name of an existing shortcut or `normalizeKeySequence()` when
        creating a new shortcut from scratch.

        Parameters
        ----------
        shortcut: XfceShortcut
            Shortcut defined in the XFCE database.

        Returns
        -------
        bool
            True if the shortcut is defined, False otherwise.

        Raises
        ------
        XfconfError
            If an error occurred while accessing xfconf
        """
        shortcuts = XfceShortcutInterface._lookupShortcuts(shortcut)
        if len(shortcuts) == 0:
            return None
        shortcut = shortcuts[0]

        prop = "{}/{}".format(shortcut.namespace, shortcut.sequence)
        return XfconfInterface.get(
            XfceShortcutInterface._KEYBOARD_SHORTCUT_CHANNEL, prop
        )

    @staticmethod
    def setShortcutCommand(command, shortcut, overwrite=False):
        # type: (Text, XfceShortcut, bool) -> bool
        """
        Set a keyboard shortcut to run a command in XFCE.

        Sets the requested shortcut to the given command. By default
        this command will not overwrite a shortcut that already exists.
        Note, however, that it may creaate a shortcut which shares the
        same key sequence as a different shortcut in another namespace.
        You may want to use `findShortcuts()` to first check that the
        sequence is not already in use.

        Shortcuts are case- and order-sensitive (i.e. `<Control><Alt>
        Escape`, `<Alt><Control>Escape`, and `<Control><Alt>escape` are
        all considered distinct). To ensure you query the desired shortcut
        it is strongly advised to first use `findShortcut()` to get the
        name of an existing shortcut or `normalizeKeySequence()` when
        creating a new shortcut from scratch.

        Parameters
        ----------
        command: Text
            Command that should be executed when the shortcut is triggered.
        shortcut: XfceShortcut
            Shortcut defined (or to be defined) in the XFCE database.
        overwrite: bool, default=False
            True if we should overwrite an existing shortcut, False otherwise.

        Returns
        -------
        bool
            True if the shortcut was created, False otherwise.

        Raises
        ------
        XfconfError
            If an error occurred while accessing xfconf.
        """
        shortcuts = XfceShortcutInterface._lookupShortcuts(shortcut)
        if len(shortcuts) != 0 and not overwrite:
            return False
        if len(shortcuts) == 0:
            assert shortcut.namespace is not None
        else:
            shortcut = shortcuts[0]

        prop = "{}/{}".format(shortcut.namespace, shortcut.sequence)
        XfconfInterface.set(
            XfceShortcutInterface._KEYBOARD_SHORTCUT_CHANNEL,
            prop,
            command,
            True,
            XfconfProptype.STRING,
        )
        return True

    @staticmethod
    def removeShortcut(command, shortcut):
        # type: (Text, XfceShortcut) -> bool
        """
        Remove the specified shortcut from XFCE.

        Attempt to remove the shortcut which triggers the requested
        command. For safety reasons, we require the command to be
        provided so that you don't inadvertantly remove a shortcut
        set for an application different than you expect.

        Shortcuts are case- and order-sensitive (i.e. `<Control><Alt>
        Escape`, `<Alt><Control>Escape`, and `<Control><Alt>escape` are
        all considered distinct). To ensure you query the desired shortcut
        it is strongly advised to first use `findShortcut()` to get the
        name of an existing shortcut or `normalizeKeySequence()` when
        creating a new shortcut from scratch.

        Parameters
        ----------
        command: Text
            Command that is executed when the shortcut is triggered.
        shortcut: XfceShortcut
            Shortcut defined in the XFCE database.

        Returns
        -------
        bool
            True if the shortcut was removed (or was not used for any
            command). False otherwise.

        Raises
        ------
        XfconfError
            If an error occurred while accessing xfconf.
        """
        shortcuts = XfceShortcutInterface._lookupShortcuts(shortcut)
        if len(shortcuts) == 0:
            return True
        shortcut = shortcuts[0]

        current_command = XfceShortcutInterface.getShortcutCommand(shortcut)
        if current_command == command:
            prop = "{}/{}".format(shortcut.namespace, shortcut.sequence)
            XfconfInterface.reset(
                XfceShortcutInterface._KEYBOARD_SHORTCUT_CHANNEL, prop
            )
            return True
        return False


def createShortcut(command, sequence):
    # type: (Text, Text) -> bool
    """
    Attempt to create a new keyboard shortcut for XFCE.

    This method will attempt to create a new keyboard shortcut and
    let you know if if it was sucessful or not. The method may fail
    for several reasons (e.g. no command available, shortcut already
    in use, etc.) but you should always be aware of the failure.

    Shortcuts should take the form of a GTK accelerator. They may be
    a single named key (e.g. "A" or "Up"), or a combination of the
    named key with one or more modifiers (e.g. "<Control><Shift>Up").
    Key names are defined by GTK+, with character keys being defined
    by the name of the symbol rather than the symbol itself (e.g.
    "minus" rather than "-").

    Additional information on GTK accelerator format can be found at
    https://github.com/GNOME/gtk/blob/3.24.0/gtk/gtkaccelgroup.c#L1435

    Parameters
    ----------
    command: Text
        Command XFCE should execute when the shortcut is triggered.
    sequence: Text
        Combination of keyboard keys used to trigger the event.

    Returns
    -------
    bool
        True if the shortcut was able to be set, False otherwise.
    """
    if not XfconfInterface.isInterfaceAvailable():
        print("No command to modify xfconf is available")
        return False
    try:
        matches = XfceShortcutInterface.findShortcuts(sequence)
        if len(matches) != 0:
            print("Refusing to create shortcut that already exists")
            return False

        shortcut = XfceShortcut.customCommand(sequence)
        return XfceShortcutInterface.setShortcutCommand(command, shortcut)
    except XfconfError as ex:
        print("Error while attempting to create shortcut: {}".format(ex))
        return False


def removeShortcut(command, sequence):
    # type: (Text, Text) -> bool
    """
    Attempt to remove an existing keyboard shortcut from XFCE.

    This method will attempt to remove a custom keyboard shortcut and
    let you know if if it was sucessful or not.

    Shortcuts should take the form of a GTK accelerator. They may be
    a single named key (e.g. "A" or "Up"), or a combination of the
    named key with one or more modifiers (e.g. "<Control><Shift>Up").
    Key names are defined by GTK+, with character keys being defined
    by the name of the symbol rather than the symbol itself (e.g.
    "minus" rather than "-").

    Additional information on GTK accelerator format can be found at
    https://github.com/GNOME/gtk/blob/3.24.0/gtk/gtkaccelgroup.c#L1435

    Parameters
    ----------
    command: Text
        Command XFCE executes when the shortcut is triggered.
    sequence: Text
        Combination of keyboard keys used to trigger the shortcut.

    Returns
    -------
    bool
        True if the shortcut was able to be removed, False otherwise.
    """
    if not XfconfInterface.isInterfaceAvailable():
        print("No command to modify xfconf is available")
        return False
    try:
        matches = XfceShortcutInterface.findShortcuts(sequence)
        if len(matches) == 0:
            print("Shortcut not found")
            return True
        matches = [x for x in matches if x.isCustomCommand()]

        remove_count = 0
        failure = False
        for shortcut in matches:
            shortcut_command = XfceShortcutInterface.getShortcutCommand(shortcut)
            if shortcut_command != command:
                continue
            if not XfceShortcutInterface.removeShortcut(command, shortcut):
                failure = True
                continue
            remove_count += 1
        if failure:
            print("Failed to remove one or more shortcuts")
            return False
        if remove_count == 0:
            print("No matching shortcuts found")
            return True
        print("All matches removed")
        return True
    except XfconfError as ex:
        print("Error while attempting to create shortcut: {}".format(ex))
        return False


# if __name__ == "__main__":
#     createShortcut('gnome-calculator', '<Ctrl>3')
