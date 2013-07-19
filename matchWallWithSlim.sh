#! /usr/bin/env bash

wall=$(cat /home/fran/.config/nitrogen/bg-saved.cfg | grep file | sed 's:file=::g')

unlink /usr/share/slim/themes/default/background.jpg

ln -s $wall /usr/share/slim/themes/default/background.jpg
