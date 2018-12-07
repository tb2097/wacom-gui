%global libwacom_ver 0.32

Name: wacom-gui
Version: 0.3.0
Release: rc13
Summary: Wacom PyQt4 GUI
License: GPLv3
BuildArch: noarch
URL: https://github.com/tb2097/wacom-gui
Requires: PyQt4 
Requires: PyQt4-webkit 
Requires: qtwebkit
Requires: xorg-x11-server-utils
Requires: xorg-x11-drv-wacom
Requires: xorg-x11-xkb-utils
Requires: xorg-x11-utils
Requires: dconf
Requires: usbutils
Requires: python
Requires: systemd
BuildRequires: python
Source0: %{name}-%{version}-%{release}.tar.gz
# latest libwacom source can be downloaded from https://github.com/linuxwacom/libwacom/releases/latest
# this is just to get the .tablet and svg data
Source1: libwacom-%{libwacom_ver}.tar.bz2
Source2: wacom.desktop

%description
Wacom PyQt4 GUI

%prep
%setup -q -n wacom-gui-master
%setup -q -T -D -a 1 -n wacom-gui-master

%build
cd wacom-gui
rm -f *.pyc
rm -f *.ui
python -m compileall .
mv ../LICENSE .
mv ../README.md .
mv ../libwacom-%{libwacom_ver}/data .
rm -f data/Makefile.*
rm -f data/layouts/Makefile.*

%install
%__rm -rf %{buildroot}
cd wacom-gui
install -m 0755 -d %{buildroot}/usr/local/%{name}
cp -r * %{buildroot}/usr/local/%{name}
cd ../rpmbuild
install -D -m 0644 wacom-gui.desktop %{buildroot}/etc/xdg/autostart/wacom-gui.desktop
install -D -m 0755 wacom-gui-rules.sh %{buildroot}/usr/local/wacom-gui/wacom-gui-rules.sh
install -D -m 0644 99-wacom-gui.rules %{buildroot}/etc/udev/rules.d/99-wacom-gui.rules
install -D -m 0755 wacom-gui %{buildroot}/usr/local/bin/wacom-gui
install -D -m 0644 mate-wacom-panel.desktop %{buildroot}/usr/share/applications/mate-wacom-panel.desktop
install -D -m 0644 wacom-gui.service %{buildroot}/etc/systemd/system/wacom-gui.service

%files
/usr/local/%{name}/*
/etc/xdg/autostart/wacom-gui.desktop
/etc/udev/rules.d/99-wacom-gui.rules
/usr/local/bin/wacom-gui
/usr/share/applications/mate-wacom-panel.desktop
/etc/systemd/system/wacom-gui.service
#/usr/share/applications/wacom.desktop


%clean
rm -rf %{buildroot}


%changelog
* Fri Dec 07 2018 Travis Best <tb2097> - 0.3.0-rc13
- Fixed: minor typo in pad.py (line 83)
* Tue Dec 04 2018 Travis Best <tb2097> - 0.3.0-rc12
- Fixed: toggle command running too slow (~2s to toggle), now ~0.5s
- Updated: custom.json file layout
- Update: device_default file layout
* Mon Dec 03 2018 Travis Best <tb2097> - 0.3.0-rc11
- Fixed: crashes if trying to load non-existant custom.json file
* Fri Nov 30 2018 Travis Best <tb2097> - 0.3.0-rc10
- Added: 'partial' value to mapping config (for future feature)
- Fixed: 'Partial...' option is skipped on toggle if value is the same as full screen
- Fixed: 'Intuos5 touch' tablet was parsing name incorrectly when assigning devices; fixed
- Fixed: wasn't loading custom hotkey for toggle from system; also needed to add hyper key (Mod4) mapping to win key
* Thu Nov 29 2018 Travis Best <tb2097> - 0.3.0-rc8
- Fixed: desktop icon moved to icons/ui; updated path
- Fixed: prompting to save config on --load; shouldn't be happening
- Fixed: path for keystrokes was messed up if not running from directory (RPM issue)
- Fixed: if single button is being called, just put it's id.  Otherwise it calls + -.  Effects r/l mouse clicks
- Added: About page
* Thu Nov 29 2018 Travis Best <tb2097> - 0.3.0-rc4
- UI is effectively a ground up rewrite
- Added: tablet refresh (no need to restart the GUI)
- Added: Multi-tablet support
- Added: New hotkey programming widget; supports keyboard shortcuts and creating system shortcuts
- Added: "forced proportions", aka tablet mapping
- ... other things
* Tue Jun 19 2018 Travis Best <tb2097> - 0.2.2-2
- Fixed: missing cursor info on help page
* Thu Jun 14 2018 Travis Best <tb2097> - 0.2.2
- Fixed: naming on PTH-660/PTH-860 to be "Pro 2" to signify difference in version from PTH-651
- Fixed: issue with Cursor not being detected causing crash
- Fixed: inverse buttons menu was showing for eraser; can only be set for stylus. Just cleaning up unneccessary options
- Added: other tablets (smaller/larger variants): PTH-450, PTH-850 (Intuos5 touch), PTH-451, PTH-851 (Intuos Pro)
- Added: Cursor menu to allow setting Absolute/Relative movement (was partially disabled previously)
* Tue Jun 5 2018 Travis Best <tb2097> - 0.2.1-3
- Fixed issue with sigsegv exit error 139; was race condition closing UI before config file completed closing on exit
* Mon Jun 4 2018 Travis Best <tb2097> - 0.2.1
- Fixed naming issue with PTH-860 (was named PTH-680)
- Fixed regression with touch detection (Issue #11)
- Fixed: when shift key is pressed by itself it was not being set as a control modifier.  Shift/Alt/Ctrl should now work as stand-alone shift modifiers
* Mon May 28 2018 Travis Best <tb2097> - 0.2.0-2
- Fixed issues with single screen tablet configuration
- Updated tablet names for PTH-660/PTH-680 to be consistent with naming scheme
- Fixed issue with touch not being properly detected due to change in device name detection
* Wed May 23 2018 Travis Best <tb2097> - 0.2.0b-1
- updated keybind.cfg file to use /usr/local/bin/wacom-gui
* Wed May 23 2018 Travis Best <tb2097> - 0.2.0-1
- updated SPEC file to include dependancies, clean up code (fixes provided by jcpearson)
- Added missing image for PTH-651 (noted missing by jcpearson)
- Do not show pad menu when a tablet does not have buttons (fix suggested by jcpearson)
- Per tablet configs (request from jcpearson)
- Added buttons to enable/disable pad buttons as well as a disable/enable all buttons (request from jcpearson)
- Made help page "pretty"; gets a weird graphical glitch on refresh though (known issue)
- tweaked layout of stylus/eraser config to be more visually consistant
- tweaked layout of pad config to be more visually consistant
- added warning on exit notifying saving of config will occur
- Fixed: eraser pressure curve was being saved and would be set correctly but it was not reflected in the GUI on reload
- Added: ground work for detecting multiple tablets at once; configuring still requires one device at a time but can load configs for all connected devices
- Known Issue: You can not connect 2 devices of the same type, will not load configs correctly
- Known Issue: On exit throws exit code 139; config is saved correctly but something isn't terminating correctly... need to track down
* Wed May 16 2018 Travis Best <tb2097> - 0.1.11-1
- Locked GUI size to be static; allowing resize was the cause of the sensitivity test area bugging out (I think)
- Rolling in patches from jcpearson (all listed below)
- Added new tablets/cintiqs: PTH-680, DTH-1620, DTK-1300
- Added check if touch is available before trying to reset it (doesn't break but presents error in shell)
- Added Help page (I modified to span width of window for easier reading)
- Added service to start configs on login, along with udev rules
- Created /usr/local/bin/wacom-gui wrapper for easier command-line execution
* Fri May 11 2018 Travis Best <tb2097> - 0.1.10-3
- changed screen detection to use MapToOutput (request from jcpearson)
- can detect more that 2 screens at a time
- fixed issue with single monitor causing crash
- removed legacy code used for screen detection (caused crash)
- added warning pop-up when tablet not detected (request from jcpearson)
* Fri Apr 06 2018 Travis Best <tb2097> - 0.1.9-1
- added warning pop-up when tablet not detected (request from jcpearson)
- fixed issue with toggle not working with misaligned screens (issue reported by jcpearson)
* Mon Oct 23 2017 Travis Best <tb2097> - 0.1.8b-1
- broke writing the config file... that was stupid of me
* Mon Oct 23 2017 Travis Best <tb2097> - 0.1.8-1
- broke touch for older tablets
- newer libwacom reports tablets with a different name; ensured tablet name reported correctly
* Fri Oct 20 2017 Travis Best <tb2097> - 0.1.7-1
- Added: PTH-660
- Added: pad button reset
- Added: restore defaults button to options page
- Fixed: PTH-660 for some reason inverts to negative value for pressure at 50% (0.5->-0.5); put in logic to check for this.  Only seems to effect the testing area
- Fixed: TabletPCButton option showing for eraser; is an invalid feature
- Fixed: Absolute/Relative mode was controlling stylus on the eraser page
- Fixed: some options were not being saved for the eraser due to above bug
* Mon May 15 2017 Travis Best <tb2097> - 0.1.6-1
- Added toggle for requiring tip to touch tablet to be "active"
* Thu Apr 13 2017 Travis Best <tb2097> - 0.1.5-1
- Fixed typo that was unchecking touch correctly but not setting the initial command correctly (would be on)
- added "key shortcut" of "000" to set a button to have no action.  Reports as "None" when detected.
* Mon Sep 19 2016 Travis Best <tb2097> - 0.1.4-1
- Fixed regression with adding touch possibly breaking non-touch tablets from working
- added touch wheel button config to PTH-650/PTH-651
* Thu Sep 15 2016 Travis Best <tb2097> - 0.1.3-1
- Fixed button config for PTH-650 (Wacom Intuos 5 Pro M touch)
- Added PTH-651 (Wacom Intuos Pro M touch)
- added option to enable/disable touch
* Fri Aug 12 2016 Travis Best <tb2097> - 0.1.1-1
- Initial Release

