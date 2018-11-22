# wacom-gui

Python/PyQt Wacom GUI for MATE/KDE

![Screenshots](https://i.imgur.com/OJW4j4Y.gif)

## Getting Started
These instructions will help you get a copy of the project up and running on yoru local machine for development/testing purposes.

### Prerequisites

You will require a few packages to get this working on your system:
- PyQt4
- qtwebkit (available from epel repo)
- PyQt4-webkit (available from epel repo)

### Installing
- Running from source
  - download the source, run wacom-gui.py from the wacom-gui directory
  - you can also build an RPM from the SPEC file in the wacom-gui directory
- Running from RPM
  - download the RPM, install
  - RPM can be added to a repository for deployment
  - menu option will appear under System > Preferences > Hardware > Wacom Tablet

## Features
- works with most Intuos tablets
- per tablet model configuration files
  - buttons can be disabled if desired
- multi-monitor configuration
  - can support >2 monitors
  - toggle hotkey (Win+Z) to swap display
- auto-load config on login
- pressure curve testing area for stylus/eraser
- pad touch enable/disable (if available)
- Shift/Alt/Ctrl can be set to a pad button for press-and-hold function, as you would for using a keyboard
  - ie. holding Alt to zoom/pan/rotate in Maya with the mouse/pen

## Contributing

If you would have bugs you have found, feature requests, or would like to contribute in some way please feel free to contact me.

## License

This project is licensed under the GPL 3.0 License - See the [LICENSE.nd](LICENSE.md) file for details

## Acknowledgements
This utility is based upon the GTK control panel created by qb89dragon, located here: http://gtk-apps.org/content/show.php/Wacom+Control+Panel?content=104309

I was unable to get it running on CentOS 6.4, my platform at the time, under KDE so I used the base tablet information class he had defined and rebuilt the GUI. It has since been updated to run on CentOS 7 (7.3 latest tested).  *should* run on CentOS 6 still but has not been tested.
