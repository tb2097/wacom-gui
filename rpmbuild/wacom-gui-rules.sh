#!/bin/sh

# Need to load the Wacom settings for user logged in on the console
#
# Script triggered via /etc/udev/rules.d/99-wacom-gui.rules that
# contains the line:
#
#  SUBSYSTEM=="usb", ATTR{idVendor}=="056a" TAG+="systemd", ENV{SYSTEMD_WANTS}+="wacom-gui.service"
#
# This triggers the systemd service 'wacom-gui.service' which runs this script

# Not sure the best way to get the 'user' running X - but with Mate, there
# will be a 'mate-session' - so lets use that ...
# We also assume that only one user is running X ...
prog="mate-session"

# get the pid of prog
pid="$(pgrep -n -f $prog)"

[ -z "$pid" ] && exit 0

envfile="/proc/$pid/environ"

[ -e "$envfile" ] || exit 0

# make sure these are not set
USER=
DISPLAY=
XAUTHORITY=

# extract the required env vars from the environ file
for e in ^DISPLAY= ^XAUTHORITY= ^USER=; do
    tmp="$(grep -z $e $envfile)"
    eval $(echo $tmp)
done

# Assuming we have what we need (and not root or gdm), run 'wacom-gui' to
# load any Wacom settings the user may have
if [ -n "$DISPLAY" -a -n "$USER" -a "$USER" != "root" -a "$USER" != "gdm" ]; then
    export DISPLAY

    # not sure we need this?
    [ -n "$XAUTHORITY" ] && export XAUTHORITY

    # Device may take a short while to initialize - so loop here for 10
    # seconds looking for the device
    c=0
    while [ $c -lt 10 ]; do
	sleep 1
        ret="$(xsetwacom list)"
	[ -n "$ret" ] && break
        let c=c+1
    done

    # load settings for the console user
    /usr/sbin/runuser $USER -c "wacom-gui --load" >& /dev/null
fi

exit 0
