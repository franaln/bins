#! /usr/bin/env python

import os
import sys
import subprocess

ICON_MUTE   = "/usr/share/icons/Faenza-Dark/status/16/audio-volume-muted-blocking-panel.png"
ICON_ZERO   = "/usr/share/icons/Faenza-Dark/status/16/audio-volume-zero-panel.png"
ICON_LOW    = "/usr/share/icons/Faenza-Dark/status/16/audio-volume-low-panel.png"
ICON_MEDIUM = "/usr/share/icons/Faenza-Dark/status/16/audio-volume-medium-panel.png"
ICON_HIGH   = "/usr/share/icons/Faenza-Dark/status/16/audio-volume-high-panel.png"


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

    os.system('canberra-gtk-play -i audio-volume-change -d "changeVolume"')

# Print audio info
else:

    if audio_muted:
        icon = ICON_MUTE
        text = '<span color=\'#ff4d4d\'>%i%%</span>' % audio_volume
    else:
        if audio_volume < 5:
            icon = ICON_ZERO
        elif audio_volume < 33:
            icon = ICON_LOW
        elif audio_volume < 66:
            icon = ICON_MEDIUM
        else:
            icon = ICON_HIGH

        text = '%i%%' % (audio_volume)

    print(icon)
    print(text)
