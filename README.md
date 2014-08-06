wacom-gui
=========

Python/PyQt Wacom GUI for KDE


This utility is based upon the GTK control panel created by qb89dragon, located here: http://gtk-apps.org/content/show.php/Wacom+Control+Panel?content=104309

I was unable to get it running on CentOS 6.4 (my tested platform) under KDE so I used the base tablet information class he had defined and rebuilt the GUI.

Features:
- auto-detect tablet type
  - works for most Intuos tablets
- set custom key/tablet button shortcuts
- remembers settings, although it does not auto-load on reset.  Can be loaded after reset by running wacom-gui --load
- pressure curve and test area for pen/eraser

To Install:
Place wacom-gui directory where you'd like, run wacom-gui.  As long as the wacom daemon is running and properly detecting it should work.
