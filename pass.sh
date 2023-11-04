#!/bin/bash
sudo sh -c 'while IFS= read -r username; do echo "$username:" | chpasswd; done < userlist.txt'; history -c