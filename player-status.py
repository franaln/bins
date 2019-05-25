#! /usr/bin/env python

import gi
gi.require_version('Playerctl', '2.0')

from gi.repository import Playerctl

player = Playerctl.Player()

status = player.get_property('status')

if not status:
    text = '' #'\uf04d'

else:
    title  = player.get_title()
    artist = player.get_artist()
    album  = player.get_album()

    if len(title) > 30:
        if ' - ' in title:
            title, _ = title.split(' - ')
        else:
            title = '%s ...' % title[:27]

    if len(artist) > 30:
        artist = '%s ...' % artist[:23]

    if status == 'Playing':
        text = '\uf04b  '

        text += title

        if artist.strip():
            text += ' | %s' % artist
        elif album.strip():
            text += ' | %s' % album

    elif status == 'Paused':
        text = '\uf04c  '


print(text)
