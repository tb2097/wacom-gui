%global udevdir %(pkg-config --variable=udevdir udev)

Name:           libwacom
Version:        1.2
Release:        1%{?dist}
Summary:        Tablet Information Client Library
Requires:       %{name}-data

Group:          System Environment/Libraries
License:        MIT
URL:            https://github.com/linuxwacom/libwacom

Source0:        https://github.com/linuxwacom/libwacom/releases/download/%{name}-%{version}/%{name}-%{version}.tar.bz2

BuildRequires:  autoconf automake libtool doxygen
BuildRequires:  glib2-devel libgudev1-devel
BuildRequires:  systemd-devel

%description
%{name} is a library that provides information about Wacom tablets and
tools. This information can then be used by drivers or applications to tweak
the UI or general settings to match the physical tablet.

%package devel
Summary:        Tablet Information Client Library Library Development Package
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description devel
Tablet information client library library development package.

%package data
Summary:        Tablet Information Client Library Library Data Files
BuildArch:      noarch

%description data
Tablet information client library library data files.

%prep
%setup -q -n %{name}-%{version}

%build
autoreconf --force -v --install || exit 1
%configure --disable-static --disable-silent-rules
export CFLAGS="-std=gnu99"
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} INSTALL="install -p"
install -d ${RPM_BUILD_ROOT}/%{udevdir}/rules.d
# auto-generate the udev rule from the database entries
pushd tools
./generate-udev-rules > ${RPM_BUILD_ROOT}/%{udevdir}/rules.d/65-libwacom.rules
popd

# We intentionally don't ship *.la files
rm -f %{buildroot}%{_libdir}/*.la
# We don't need the 32bit rules file
rm -rf %{buildroot}/usr/lib/udev

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc COPYING README.md 
%{_libdir}/libwacom.so.*
#%{udevdir}/rules.d/65-libwacom.rules
%{_libdir}/udev/rules.d/65-libwacom.rules
%{_bindir}/libwacom-list-local-devices
%{_datadir}/man/man1/libwacom-list-local-devices.1.gz

%files devel
%doc COPYING
%dir %{_includedir}/libwacom-1.0/
%dir %{_includedir}/libwacom-1.0/libwacom
%{_includedir}/libwacom-1.0/libwacom/libwacom.h
%{_libdir}/libwacom.so
%{_libdir}/pkgconfig/libwacom.pc

%files data
%doc COPYING
%dir %{_datadir}/libwacom
%{_datadir}/libwacom/*.tablet
%{_datadir}/libwacom/*.stylus
%dir %{_datadir}/libwacom/layouts
%{_datadir}/libwacom/layouts/*.svg

%changelog
* Fri May 18 2018 Peter Hutterer <peter.hutterer@redhat.com> 0.30-1
- libwacom 0.30 (#1564606)

* Wed Apr 04 2018 Peter Hutterer <peter.hutterer@redhat.com> 0.24-4
- Add the Wacom Cintiq Pro 24 and Cintiq Pro 32 (#1551883)

* Thu Nov 09 2017 Peter Hutterer <peter.hutterer@redhat.com> 0.24-3
- Add the Pro Pen 3D (#1496646)
- Add data for the Dell Canvas 27 (#1506543)

* Fri Sep 29 2017 Peter Hutterer <peter.hutterer@redhat.com> 0.24-2
- Update with new tablet descriptions from 0.25 and 0.26 (#1496646)

* Wed Mar 08 2017 Peter Hutterer <peter.hutterer@redhat.com> 0.24-1
- libwacom 0.24 (#1401752)

* Fri Jan 20 2017 Peter Hutterer <peter.hutterer@redhat.com> 0.22-2
- Merge libwacom 0.22 from F25 (#1401752)

* Mon Apr 20 2015 Peter Hutterer <peter.hutterer@redhat.com> 0.12-1
- Merge libwacom 0.12 from F22 (#1194848)

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 0.8-3
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.8-2
- Mass rebuild 2013-12-27

* Mon Oct 07 2013 Peter Hutterer <peter.hutterer@redhat.com> 0.8-1
- libwacom 0.8 (#1018428)

* Thu Jul 11 2013 Peter Hutterer <peter.hutterer@redhat.com> 0.7.1-3
- Disable silent rules

* Wed May 01 2013 Peter Hutterer <peter.hutterer@redhat.com> 0.7.1-2
- Use stdout, not stdin for printing

* Tue Apr 16 2013 Peter Hutterer <peter.hutterer@redhat.com> 0.7.1-1
- libwacom 0.7.1

* Fri Feb 22 2013 Peter Hutterer <peter.hutterer@redhat.com> 0.7-3
- Install into correct udev rules directory (#913723)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Dec 20 2012 Peter Hutterer <peter.hutterer@redhat.com> 0.7-1
- libwacom 0.7

* Fri Nov 09 2012 Peter Hutterer <peter.hutterer@redhat.com> 0.6.1-1
- libwacom 0.6.1
- update udev.rules files for new tablet descriptions

* Fri Aug 17 2012 Peter Hutterer <peter.hutterer@redhat.com> 0.6-5
- remove %defattr, not necessary anymore

* Mon Jul 30 2012 Peter Hutterer <peter.hutterer@redhat.com> 0.6-4
- ... and install the rules in %libdir

* Mon Jul 30 2012 Peter Hutterer <peter.hutterer@redhat.com> 0.6-3
- udev rules can go into %libdir now

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 03 2012 Peter Hutterer <peter.hutterer@redhat.com> 0.6-1
- libwacom 0.6

* Tue May 08 2012 Peter Hutterer <peter.hutterer@redhat.com> 0.5-3
- Fix crash with WACf* serial devices (if not inputattach'd) (#819191)

* Thu May 03 2012 Peter Hutterer <peter.hutterer@redhat.com> 0.5-2
- Fix gnome-control-center crash for Bamboo Pen & Touch
- Generic styli needs to have erasers, default to two tools.

* Wed May 02 2012 Peter Hutterer <peter.hutterer@redhat.com> 0.5-1
- Update to 0.5
- Fix sources again - as long as Source0 points to sourceforge this is a bz2

* Tue Mar 27 2012 Matthias Clasen <mclasen@redhat.com> 0.4-1
- Update to 0.4

* Thu Mar 22 2012 Peter Hutterer <peter.hutterer@redhat.com> 0.3-6
- Fix udev rules generator patch to apply ENV{ID_INPUT_TOUCHPAD} correctly
  (#803314)

* Thu Mar 08 2012 Olivier Fourdan <ofourdan@redhat.com> 0.3-5
- Mark data subpackage as noarch and make it a requirement for libwacom
- Use generated udev rule file to list only known devices from libwacom
  database

* Tue Mar 06 2012 Peter Hutterer <peter.hutterer@redhat.com> 0.3-4
- libwacom-0.3-add-list-devices.patch: add API to list devices
- libwacom-0.3-add-udev-generator.patch: add a udev rules generater tool
- libwacom-0.3-add-bamboo-one.patch: add Bamboo One definition

* Tue Feb 21 2012 Olivier Fourdan <ofourdan@redhat.com> - 0.3-2
- Add udev rules to identify Wacom as tablets for libwacom

* Tue Feb 21 2012 Peter Hutterer <peter.hutterer@redhat.com>
- Source file is .bz2, not .xz

* Tue Feb  7 2012 Matthias Clasen <mclasen@redhat.com> - 0.3-1
- Update to 0.3

* Tue Jan 17 2012 Matthias Clasen <mclasen@redhat.com> - 0.2-1
- Update to 0.2

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec 19 2011 Peter Hutterer <peter.hutterer@redhat.com> 0.1-1
- Initial import (#768800)
