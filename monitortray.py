#!/usr/bin/env python

import sys
import os
import re
import cairo
import argparse
import subprocess
import datetime

import dbus
import dbus.bus
import dbus.service
import dbus.mainloop.glib

import gi
gi.require_version('Notify', '0.7')
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk, GObject, Notify, GLib

UPDATE_AUDIO_INTERVAL = 5  # in secs
UPDATE_POWER_INTERVAL = 15 # in secs

# POWER
BATTERY_LEVEL_LOW       = 15 # in %
BATTERY_LEVEL_CRITICAL  = 10 # in %

RAM_LEFT_WARNING  = 500
RAM_LEFT_CRITICAL = 200

CPU_TEMP_CRITITCAL = 80

LOGFILE = "/home/fran/.batterylog"

F_ENERGY_NOW  = "/sys/class/power_supply/BAT0/energy_now"
F_ENERGY_FULL = "/sys/class/power_supply/BAT0/energy_full"
F_STATUS      = "/sys/class/power_supply/BAT0/status"
F_VOLTAGE_NOW = "/sys/class/power_supply/BAT0/voltage_now"
F_POWER_NOW   = "/sys/class/power_supply/BAT0/power_now"

F_BACKLIGHT_CURRENT = '/sys/class/backlight/intel_backlight/brightness'
F_BACKLIGHT_MAX     = '/sys/class/backlight/intel_backlight/max_brightness'

ICON_BATTERY_FULL_CHARGING    = "battery-full-charging"
ICON_BATTERY_FULL             = "battery-full"
ICON_BATTERY_EMPTY_CHARGING   = "battery-empty-charging"
ICON_BATTERY_EMPTY            = "battery-empty"
ICON_BATTERY_CAUTION_CHARGING = "battery-caution-charging"
ICON_BATTERY_CAUTION          = "battery-caution"
ICON_BATTERY_LOW_CHARGING     = "battery-low-charging"
ICON_BATTERY_LOW              = "battery-low"
ICON_BATTERY_MEDIUM_CHARGING  = "battery-medium-charging"
ICON_BATTERY_MEDIUM           = "battery-medium"
ICON_BATTERY_GOOD_CHARGING    = "battery-good-charging"
ICON_BATTERY_GOOD             = "battery-good"
ICON_BATTERY_MISSING          = "battery-missing"


# AUDIO
VOLUME_STEP = 2.5

ICON_MUTE   = "audio-volume-muted-blocking-panel"
ICON_ZERO   = "audio-volume-zero-panel"
ICON_LOW    = "audio-volume-low-panel"
ICON_MEDIUM = "audio-volume-medium-panel"
ICON_HIGH   = "audio-volume-high-panel"

# TODO:
# Add logfile backup

def get_cmd_output(cmd):
    try:
        if isinstance(cmd, list):
            output = subprocess.check_output(cmd, stderr=subprocess.DEVNULL)
        else:
            output = subprocess.check_output(cmd, stderr=subprocess.DEVNULL, shell=True)
    except subprocess.CalledProcessError:
        return ''

    return output.decode('utf8').strip()


class OSD(Gtk.Window):

    def __init__(self):
        super().__init__(type=Gtk.WindowType.TOPLEVEL)

        self.set_app_paintable(True)
        self.set_decorated(False)
        self.set_size_request(300, 300)
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.set_keep_above(True)
        self.set_focus(None)
        self.set_accept_focus(False)

        self.connect('draw', self.draw)

        self.value = 100

        self.normal_color = (0.93, 0.93, 0.93)
        self.alt_color = (0.93, 0., 0.)

        self.color = self.normal_color

        self.visible = False

    def close(self):
        # if not self.visible:
        #     return
        self.hide()
        self.visible = False

    def show(self, value, icon_name='', alt=False):
        self.value = value
        self.icon_name = icon_name

        if alt:
            self.color = self.alt_color
        else:
            self.color = self.normal_color

        self.queue_draw()
        self.present()

        self.visible = True

        GLib.timeout_add_seconds(3, self.close)

    def draw_icon(self, cr):

        pixel_size = 150
        x = 150-0.5*pixel_size
        y = 130-0.5*pixel_size

        cr.translate(x, y)
        # # cr.rectangle(0, 0, pixel_size, pixel_size)
        # cr.clip()

        icon_theme = Gtk.IconTheme.get_default()
        icon_pixbuf = icon_theme.load_icon(self.icon_name, pixel_size, Gtk.IconLookupFlags.FORCE_SYMBOLIC)

        Gdk.cairo_set_source_pixbuf(cr, icon_pixbuf, 0, 0) #x, y)
        cr.paint()
        #    ctx.paint_with_alpha (with_alpha);


    def draw(self, widget, event):

        cr = Gdk.cairo_create(widget.get_window())

        bkg_color = (0.27, 0.27, 0.27)

        cr.set_source_rgb(*bkg_color)
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.paint()

        if self.icon_name:
            cr.save()
            self.draw_icon(cr)
            cr.restore()

        cr.set_source_rgb(*self.color)
        cr.rectangle(30, 250, self.value*240, 10)
        cr.fill()


class TrayMonitor(dbus.service.Object):

    def __init__(self, bus, path, name):

        dbus.service.Object.__init__(self, bus, path, name)

        # Battery
        self.battery = {}
        self.battery['percentage'] = 999
        self.battery['status'] = 'Unknown'
        self.battery['level'] = 'NORMAL'

        # Blanking/Suspend/RAM-clean
        self.blanking_allowed = True
        self.suspend_allowed = True
        self.ram_clean_allowed = True

        # Audio
        self.audio_sink = ''
        self.audio_muted = False
        self.audio_volume = 0

        # Icon (Power)
        self.icon_power = Gtk.StatusIcon()
        self.set_power_icon(ICON_BATTERY_MISSING)
        self.icon_power.set_has_tooltip(True)
        self.icon_power.connect("query-tooltip", self.tooltip_power_query)

        self.icon_power.connect('activate',   self.on_power_right_click_event, 3, Gtk.get_current_event_time())
        self.icon_power.connect('popup-menu', self.on_power_right_click_event)
        self.icon_power.connect('scroll-event', self.on_power_scroll_event)

        self.create_power_menu()

        # Icon (Audio)
        self.icon_audio = Gtk.StatusIcon()
        self.set_audio_icon()
        self.icon_audio.set_has_tooltip(True)
        self.icon_audio.connect("query-tooltip", self.tooltip_audio_query)

        #self.icon_volume.connect('activate',   self.on_volume_right_click_event, 3, Gtk.get_current_event_time())
        #self.icon_volume.connect('popup-menu', self.on_volume_right_click_event)
        self.icon_audio.connect('scroll-event', self.on_audio_scroll_event)
        self.icon_audio.connect('button-release-event', self.on_audio_button_release_event)

        # Notifications and OSD
        Notify.init("monitor")

        self.osd = OSD()

        # Update power and audio
        self.update_power()
        self.update_audio()

        GLib.timeout_add_seconds(UPDATE_POWER_INTERVAL, self.update_power)
        GLib.timeout_add_seconds(UPDATE_AUDIO_INTERVAL, self.update_audio)


    @dbus.service.method("org.traymon.Daemon", in_signature='', out_signature='')
    def run(self):
        Gtk.main()

    @dbus.service.method("org.traymon.Daemon", in_signature='', out_signature='')
    def close(self):
        Gtk.main_quit()


    def set_power_icon(self, name):
        self.icon_power.set_from_icon_name(name)

    def set_audio_icon(self):
        self.icon_audio.set_from_icon_name(self.get_audio_icon())

    def create_power_menu(self):

        self.menu_power = Gtk.Menu()

        # Battery
        self.info_battery = Gtk.MenuItem()
        self.info_temp = Gtk.MenuItem()
        self.info_ram = Gtk.MenuItem()

        sep1 = Gtk.SeparatorMenuItem.new()
        sep2 = Gtk.SeparatorMenuItem.new()
        sep3 = Gtk.SeparatorMenuItem.new()

        self.menu_power.append(self.info_battery)
        self.menu_power.append(sep1)
        self.menu_power.append(self.info_temp)
        self.menu_power.append(sep2)
        self.menu_power.append(self.info_ram)
        self.menu_power.append(sep3)

        self.item_pause_blank = Gtk.CheckMenuItem()
        self.item_pause_blank.set_label("Pause screen blank")
        self.item_pause_blank.connect('activate', self.toggle_blanking)

        self.item_pause_suspend = Gtk.CheckMenuItem()
        self.item_pause_suspend.set_label("Pause suspend")
        self.item_pause_suspend.connect('activate', self.toggle_suspend)

        self.item_pause_clean = Gtk.CheckMenuItem()
        self.item_pause_clean.set_label("Pause RAM clean")
        self.item_pause_clean.connect('activate', self.toggle_ram_clean)

        quit = Gtk.MenuItem()
        quit.set_label("Quit")
        quit.connect("activate", Gtk.main_quit)

        self.menu_power.append(self.item_pause_blank)
        self.menu_power.append(self.item_pause_suspend)
        self.menu_power.append(self.item_pause_clean)
        self.menu_power.append(quit)

        self.menu_power.show_all()


    def on_power_left_click_event(self, icon, button):
        print('click')

    def on_power_right_click_event(self, icon, button, time):

        self.info_battery.set_label('%s, %i%%, %.2fmW' % (self.battery['status'], self.battery['percentage'], self.battery['power']))

        temperature = self.check_cpu_temperature()
        self.info_temp.set_label('CPU temp: %iC, %iC' % (temperature[0], temperature[1]))

        ram = self.check_ram_usage()
        self.info_ram.set_label('Free RAM: %iMB' % (ram))

        self.menu_power.popup(None, None, None, self.icon_power, button, time)

    def on_power_scroll_event(self, icon, event):
        direction = event.direction
        if direction == Gdk.ScrollDirection.UP:
            self.change_brightness(+1)
        elif direction == Gdk.ScrollDirection.DOWN:
            self.change_brightness(-1)

    def on_audio_left_click_event(self, icon, button):
        pass

    def on_audio_right_click_event(self, icon, button, time):
        pass
        # self.info_battery.set_label('%s, %i%%, %.2fmW' % (self.battery['status'], self.battery['percentage'], self.battery['volume']))

        # temperature = self.check_cpu_temperature()
        # self.info_temp.set_label('CPU temp: %iC, %iC' % (temperature[0], temperature[1]))

        # ram = self.check_ram_usage()
        # self.info_ram.set_label('Free RAM: %iMB' % (ram))

        # self.menu_volume.popup(None, None, None, self.icon_volume, button, time)

    def on_audio_scroll_event(self, icon, event):
        direction = event.direction
        if direction == Gdk.ScrollDirection.UP:
            self.change_volume(+VOLUME_STEP)
        elif direction == Gdk.ScrollDirection.DOWN:
            self.change_volume(-VOLUME_STEP)

    def on_audio_button_release_event(self, icon, event):
        if event.button != 2:
            return False

        self.toggle_muted()
        self.update_audio()

        return True

    ## blank screen functions
    def enable_blanking(self):
        os.system("xset s on; xset +dpms")
        self.blanking_allowed = True

    def disable_blanking(self):
        os.system("xset s off; xset -dpms")
        self.blanking_allowed = False

    def toggle_blanking(self, arg):
        if self.blanking_allowed:
            self.disable_blanking()
        else:
            self.enable_blanking()

    def toggle_suspend(self, arg):
        self.suspend_allowed = (not self.suspend_allowed)

    def toggle_ram_clean(self, arg):
        self.ram_clean_allowed = (not self.ram_clean_allowed)


    ## Brightness
    def get_current_brightness(self):
        with open(F_BACKLIGHT_CURRENT) as curr_file:
            return int(curr_file.read().split('\n')[0])

    def get_max_brightness(self):
        with open(F_BACKLIGHT_MAX) as max_file:
            return int(max_file.read().split('\n')[0])

    @dbus.service.method("org.traymon.Daemon", in_signature='', out_signature='')
    def change_brightness(self, arg):
        current_value = self.get_current_brightness()
        max_value     = self.get_max_brightness()

        step = max_value / 10
        threshold = 2 * step

        if current_value < threshold:
            step /= 4

        step = int(step)

        new_value = int(current_value + step * arg)

        if new_value > max_value:
            new_value = max_value
        elif new_value < step:
            new_value = step

        if new_value != current_value:
            with open(F_BACKLIGHT_CURRENT, 'w') as f:
                f.write(str(new_value))

        #self.osd.show(self.audio_volume/100., self.audio_muted)


    ## RAM
    def check_ram_usage(self):
        return int(get_cmd_output("free -m | grep Mem | awk '{print $7}'").split('\n')[0])

    ## Temperature
    def check_cpu_temperature(self):

        out = get_cmd_output(['sensors',]).split('\n')

        temperature = []
        for line in out:
            if 'Core' not in line:
                continue

            core, temp = line.split(':')

            temp = temp.split()[0][1:-2]
            temperature.append(float(temp))

        return temperature

    ## Battery
    def check_battery(self):
        pass

    def update_power(self):

        status = 'Unknown';
        energy_now = -1
        energy_full = -1
        voltage_now = -1
        power_now = -1
        power = 0.00

        # read status
        with open(F_STATUS, "r") as f:
            tmp = f.read()
            status = 'Unknown'
            if tmp == "Charging\n":
                status = 'Charging'
            elif tmp == "Discharging\n":
                status = 'Discharging'
            elif tmp == "Full\n":
                status = 'Full'

        # read battery values
        energy_now  = float(open(F_ENERGY_NOW).read())
        energy_full = float(open(F_ENERGY_FULL).read())
        voltage_now = float(open(F_VOLTAGE_NOW).read())
        power_now   = float(open(F_POWER_NOW).read())

        seconds = 0
        minutes = 0
        hours = 0
        if power_now > 0:
            if status == 'Charging':
                seconds = 3600 * (energy_full - energy_now) / power_now;
            elif status ==  'Discharging':
                seconds = 3600 * energy_now / power_now
            else:
                seconds = 0

        else:
            seconds = 0

        hours = seconds / 3600
        seconds -= 3600 * hours
        minutes = seconds / 60
        seconds -= 60 * minutes

        power = power_now / 1000000.

        # calculate charged percentage
        percentage = 0;
        if energy_full > 0:
            percentage = (energy_now * 100) / energy_full
        if percentage > 100:
            percentage = 100
        elif percentage < 0:
            percentage = 0

        # update icon
        icon_name = self.get_power_icon_name(status, percentage)
        self.set_power_icon(icon_name)

        # show notification if necessary
        if status == self.battery['status'] and status == 'Discharging':
            if percentage < BATTERY_LEVEL_CRITICAL and self.battery['level'] == 'LOW':
                self.send_notification("Battery is under %s%%. Suspending in 2 minutes..." % BATTERY_LEVEL_CRITICAL,
                                       "dialog-information")
                self.battery['level'] = 'CRITICAL'

            elif (percentage <= BATTERY_LEVEL_LOW and self.battery['level'] == 'NORMAL'):
                self.send_notification("Battery is under %s%%." % BATTERY_LEVEL_LOW,
                                       "dialog-information")
                self.battery['level'] = 'LOW'

        # Suspend after critical notification
        if status == 'Discharging' and percentage <= BATTERY_LEVEL_CRITICAL-1 and percentage >= BATTERY_LEVEL_CRITICAL-2:
            self.send_notification("Battery very low. Suspending in one minute ...",
                                   "dialog-information")


        # save values
        self.battery['status'] = status
        self.battery['percentage'] = percentage
        self.battery['power'] = power
        self.battery['time'] = (hours, minutes, seconds)

        # save to logfile
        # with open(LOGFILE, "a") as f:
        #     today = datetime.datetime.today()

        #     date_str = today.strftime('%Y-%m-%d %H:%M:%S')
        #     bat_str = '%02d%% %s %.2f' % (percentage, status, power)

        #     f.write('%s %s\n' % (date_str, bat_str))

        # suspend when reaches BATTERY_LEVEL_CRITICAL-1
        if self.suspend_allowed and status == 'Discharging' and percentage < (BATTERY_LEVEL_CRITICAL-2):
            os.system("systemctl suspend")


        # Check RAM and CPU temperatura and change icon if
        ram_usage = self.check_ram_usage()
        if self.ram_clean_allowed and ram_usage < RAM_LEFT_CRITICAL:
            os.system('killall chromium')
        elif ram_usage < RAM_LEFT_WARNING:
            self.set_power_icon('software-update-urgent')

        temperatures = self.check_cpu_temperature()
        for temp in temperatures:
            if temp > CPU_TEMP_CRITITCAL:
                self.set_power_icon('apport')
                break

        # Check discharging rate
        if status == 'Discharging' and power > 25.:
            self.set_power_icon('apport')

        return True

    def tooltip_power_query(self, widget, x, y, keyboard_mode, tooltip):

        #  update tooltip
        status = self.battery['status']

        if status == 'Discharging':
            h, m, s = self.battery['time']
            tooltip_text = "Discharging, %i%% (%02d:%02d remaining)\nusing %2.2f W" % (self.battery['percentage'], h, m, self.battery['power'])
        elif status == 'Charging':
            tooltip_text = "Charging, %i%%" % self.battery['percentage']
        elif status == 'Full':
            tooltip_text = "Full, %i%%" % self.battery['percentage']
        else:
            tooltip_text = "Unknown, %i%%" % self.battery['percentage']

        tooltip.set_text(tooltip_text)

        return True

    def get_power_icon_name(self, status, percentage):

        tmp = ''
        if status == 'Discharging':
            if percentage < BATTERY_LEVEL_CRITICAL:
                tmp = ICON_BATTERY_EMPTY
            elif percentage < BATTERY_LEVEL_LOW:
                tmp = ICON_BATTERY_CAUTION
            elif percentage < 45:
                tmp = ICON_BATTERY_LOW
            elif percentage < 65:
                tmp = ICON_BATTERY_MEDIUM
            elif percentage < 75:
                tmp = ICON_BATTERY_GOOD
            else:
                tmp = ICON_BATTERY_FULL

        elif status == 'Charging':
            if percentage < BATTERY_LEVEL_CRITICAL:
                tmp = ICON_BATTERY_EMPTY_CHARGING
            elif percentage < BATTERY_LEVEL_LOW:
                tmp = ICON_BATTERY_CAUTION_CHARGING
            elif percentage < 45:
                tmp = ICON_BATTERY_LOW_CHARGING
            elif percentage < 65:
                tmp = ICON_BATTERY_MEDIUM_CHARGING
            elif percentage < 75:
                tmp = ICON_BATTERY_GOOD_CHARGING
            else:
                tmp = ICON_BATTERY_FULL_CHARGING

        elif status == 'Full':
            tmp = ICON_BATTERY_FULL

        elif status == 'Unknown':
            if percentage > 95:
                tmp = ICON_BATTERY_FULL_CHARGING
            else:
                tmp = ICON_BATTERY_MISSING
        else:
            tmp = ICON_BATTERY_MISSING

        return tmp

    @dbus.service.method("org.traymon.Daemon", in_signature='', out_signature='')
    def toggle_muted(self):
        os.system('pactl set-sink-mute "%s" toggle' % self.audio_sink)
        self.update_audio()

        self.osd.show(self.audio_volume/100., self.get_audio_icon(), self.audio_muted)

    @dbus.service.method("org.traymon.Daemon", in_signature='', out_signature='')
    def change_volume(self, arg):
        if arg > 0:
            if self.audio_volume >= 100:
                return
            cmd = 'pactl set-sink-volume %s +%i%%' % (self.audio_sink, arg)

        elif arg < 0:
            if self.audio_volume <= 0:
                return
            cmd = 'pactl set-sink-volume %s %i%%' % (self.audio_sink, arg)

        os.system(cmd)

        if self.audio_muted:
            self.toggle_muted()

        self.update_audio()
        self.osd.show(self.audio_volume/100., self.get_audio_icon(), self.audio_muted)

    def get_audio_icon(self):
        if self.audio_muted:
            icon_name = ICON_MUTE
        else:
            if self.audio_volume < 5:
                icon_name = ICON_ZERO
            elif self.audio_volume < 33:
                icon_name = ICON_LOW
            elif self.audio_volume < 66:
                icon_name = ICON_MEDIUM
            else:
                icon_name = ICON_HIGH

        return icon_name

    def update_audio(self):

        try:
            self.audio_sink = get_cmd_output("pacmd list-sinks | awk '/* index:/{ print $3 }'")

            muted  = get_cmd_output("pacmd list-sinks | grep -A 15 '* index' | awk '/muted:/{ print $2 }'")
            volume = get_cmd_output("pacmd list-sinks | grep -A 15 '* index' | awk '/volume: front/{ print $5 }' | sed 's/%//g'")

            self.audio_muted = bool(muted == 'yes')
            self.audio_volume = int(float(volume))
        except:
            self.audio_sink = ''
            self.audio_muted = False
            self.audio_volume = 0.


        self.set_audio_icon()

        return True

    def tooltip_audio_query(self, widget, x, y, keyboard_mode, tooltip):

        #  update tooltip
        volume = self.audio_volume

        if self.audio_muted:
            tooltip_text = "Volume: %d%% (muted)" % self.audio_volume
        else:
            tooltip_text = "Volume: %d%%" % self.audio_volume

        tooltip.set_text(tooltip_text)

        return True


    def send_notification(self, msg, type_):
        noti = Notify.Notification.new('Monitor', msg, type_)
        noti.show()

    def run(self):
        Gtk.main()


# class TrayMonitor():

#     def __init__ (self, bus, path, name):

#         dbus.service.Object.__init__(self, bus, path, name)

#         #self.running = False
#         self.monitor = Monitor()

#     # @dbus.service.method("org.traymon.Daemon", in_signature='', out_signature='b')
#     # def is_running(self):
#     #     return self.running



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-q', '--quit', action='store_true', help='quit')

    # Audio
    parser.add_argument('-v', '--volume', type=float, help='Change volume')
    parser.add_argument('-m', '--mute', action='store_true', help='Mute volume (toggle)')

    # Brightness
    parser.add_argument('-b', '--brightness', type=int, help='Change brightness')


    args = parser.parse_args()

    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    bus = dbus.SessionBus()
    request = bus.request_name("org.traymon.Daemon", dbus.bus.NAME_FLAG_DO_NOT_QUEUE)

    if request != dbus.bus.REQUEST_NAME_REPLY_EXISTS:
        if args.quit:
            print('not running')
            return True
        app = TrayMonitor(bus, '/', "org.traymon.Daemon")
    else:
        obj = bus.get_object("org.traymon.Daemon", "/")
        app = dbus.Interface(obj, "org.traymon.Daemon")


    if args.volume is not None:
        app.change_volume(args.volume)
    elif args.mute:
        app.toggle_muted()

    elif args.brightness is not None:
        app.change_brightness(args.brightness)

    elif args.quit:
        app.close()
    else:
        app.run()

    return True

if __name__ == '__main__':
    sys.exit(main())
