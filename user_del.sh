#!/bin/bash

check_sudo() {
    if [ "$(whoami)" != root ]; then
        echo "Privileges Required"
        exit 1
    fi
}

cat /etc/passwd | grep -i -e "redteam" | cut -d : -f1 > bad_users.txt

check_sudo

for username in $(cat bad_users.txt)
do
    userdel -f -r $username 
done
