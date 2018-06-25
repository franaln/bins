#! /usr/bin/env python

import os
import sys
import subprocess


def get_cmd_output(cmd):
    try:
        if isinstance(cmd, list):
            output = subprocess.check_output(cmd, stderr=subprocess.DEVNULL)
        else:
            output = subprocess.check_output(cmd, stderr=subprocess.DEVNULL, shell=True)
    except subprocess.CalledProcessError:
        return ''

    return output.decode('utf-8').strip()


# Get audio info
audio_sink = get_cmd_output("pacmd list-sinks | awk '/* index:/{ print $3 }'")

muted  = get_cmd_output("pacmd list-sinks | grep -A 15 '* index' | awk '/muted:/{ print $2 }'")
volume = get_cmd_output("pacmd list-sinks | grep -A 15 '* index' | awk '/volume: front/{ print $5 }' | sed 's/%//g'")


audio_muted = bool(muted == 'yes')
audio_volume = int(float(volume))

# Change volume
if len(sys.argv) > 1:

    arg = sys.argv[1]
    sarg = int(sys.argv[2]) if len(sys.argv) > 2 else 1

    if arg == 'mute':
        os.system('pactl set-sink-mute "%s" toggle' % audio_sink)

    elif arg == 'down':
        if audio_volume > 0:
            os.system('pactl set-sink-volume %s -%i%%' % (audio_sink, sarg))

    elif arg == 'up':
        if audio_volume < 100:
            os.system('pactl set-sink-volume %s +%i%%' % (audio_sink, sarg))


# Print audio info
if audio_muted:
    print('<span color=\'#ff4d4d\'>🔇  %i%%</span>' % audio_volume)
else:
    if audio_volume < 5:
        icon = '🔈'
    elif audio_volume < 50:
        icon = '🔉'
    else:
        icon = '🔊'

    text = '%s  %i%%' % (icon, audio_volume)

    print(text)
