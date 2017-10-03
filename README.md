wacom-gui
=========

Python/PyQt Wacom GUI for MATE/KDE


This utility is based upon the GTK control panel created by qb89dragon, located here: http://gtk-apps.org/content/show.php/Wacom+Control+Panel?content=104309

I was unable to get it running on CentOS 6.4 (my tested platform) under KDE so I used the base tablet information class he had defined and rebuilt the GUI. It has since been updated to run on CentOS 7 (7.3 latest tested).  *should* run on CentOS 6 still but has not been tested.

Features:
- auto-detect tablet type
  - works for most Intuos tablets
- set custom key/tablet button shortcuts
- remembers settings, although it does not auto-load on reset.  Can be loaded after reset by running wacom-gui --load
- pressure curve and test area for pen/eraser
- touch toggle option

To Install:
Place wacom-gui directory where you'd like, run wacom-gui.py.  As long as the wacom daemon is running and properly detecting it should work.

OR:
install RPM.  Adds launcher to Applications > System Tools menu, adds keyboard shortcut Win+Z, which users can assign to a button to toggle between displays.
