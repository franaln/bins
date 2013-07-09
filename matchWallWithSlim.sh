#! /usr/bin/env bash

wall=$(cat $HOME/.config/nitrogen/bg-saved.cfg | grep file | sed 's:file=::g')
ln -s $wall /usr/share/slim/themes/default/background.jpg
