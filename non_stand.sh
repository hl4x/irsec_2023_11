sudo ls -l /proc/[0-9]*/exe 2>/dev/null | awk '/ -> / && !/\/usr\/(lib(exec)?|s?bin)\// {print $9, $10, $11}' | sed 's,/proc/\([0-9]*\)/exe,\1,'