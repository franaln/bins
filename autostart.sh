#! /usr/bin/bash

setxkbmap -layout us -option ctrl:nocaps
touchpad.sh &
start-pulseaudio-x11 &
tint2 &
batterytray &
volumetray &
nm-applet --sm-disable &
(sleep 5 && dunst -conf $HOME/.dunstrc) &
(sleep 5 && dropboxd) &
