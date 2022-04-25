# I've hacked this to run with Python 3 and PyQt5.

I'm not a Python developer, so don't expect the migration to look pretty.

Also fixed a bug in scanning for `Name=` key, which was preventing one of my tablets from being detected.

# wacom-gui

Python/PyQt Wacom GUI for MATE/KDE

![Screenshots](https://i.imgur.com/OJW4j4Y.gif)

## Getting Started
These instructions will help you get a copy of the project up and running on yoru local machine for development/testing purposes.

### Prerequisites
You will require a few packages to get this working on your system:
- PyQt5

### Installing
- Running from source
  - download the source, run wacom-gui.py from the wacom-gui directory
  - you can also build an RPM from the SPEC file in the wacom-gui directory
  - libwacom-data-0.33 or newer
- Running from RPM
  - download the RPM, install
  - RPM can be added to a repository for deployment
  - menu option will appear under System > Preferences > Hardware > Wacom Tablet

## Features
- should work with any tablet detected by libwacom
- per tablet model configuration files
- supports multiple tablets at once, can be of the same model
- refresh connected devices without restarting the interface
- auto-load config on login
- Configuration Features
  - Express Keys
    - Enable/Disable/Default options
    - supports modifier keys (Alt/Ctrl/Shift)
    - can create custom, global keystrokes
    - can create system hotkeys to run scripts/commands
  - Stylus/Eraser
    - pressure curve, sensitivity, various other options available
    - mapping input to specific display as well as enabling "force perspective" for drawing area
    - rotate tablet at 90° increments, as needed
    - multi-monitor support with toggle to easily swap displays
  - Touch
    - enable/disable, if available for device
    - enable/disable gestures, if desired as well as setting scroll/zoom sensitivity

## Contributing

If you have found any bugs, have feature requests, or would like to contribute in some way please feel free to contact me.

## License

This project is licensed under the GPL 3.0 License - See the [LICENSE.nd](LICENSE.md) file for details

## Acknowledgements
touch icons: <div>Icons made by <a href="https://www.flaticon.com/authors/mobiletuxedo" title="Mobiletuxedo">Mobiletuxedo</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a> is licensed by <a href="http://creativecommons.org/licenses/by/3.0/" title="Creative Commons BY 3.0" target="_blank">CC 3.0 BY</a></div>

All testing has been done on CentOS => 7.3.  Due to major reworks from v0.2.x, it may not work on CentOS 6.x but it should, in theory, work.
