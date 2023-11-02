#!/bin/sh

pkg install pftop

sysrc pf_enable=yes
sysrc pflog_enable=yes
#pflog_logifle="/path/to/logfile"
#pflog_flags=""
service pf start
service pflog start

#make sure to move pf.conf into /etc/pf.conf
#
pfctl -e ; pfctl -f /etc/pf.conf

#sleep 5
#pfctl -F all

