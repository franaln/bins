#! /usr/bin/env python

import gi
gi.require_version('Playerctl', '1.0')

from gi.repository import Playerctl

player = Playerctl.Player()

status = player.get_property('status')

if not status:
    text = '\uf04d'

else:

    title  = player.get_title()
    artist = player.get_artist()
    album  = player.get_album()

    if len(title) > 25:
        title = ''.join(title[:23])+'...'

    if status == 'Playing':
        text = '\uf04b  '
    elif status == 'Paused':
        text = '\uf04c  '

    text += title

    if artist.strip():
        text += ' | <b>%s</b>' % artist
    elif album.strip():
        text += ' | <b>%s</b>' % album


print(text)
