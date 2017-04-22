#!/usr/bin/env python

import gi
gi.require_version('Notify', '0.7')
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk, GObject, Notify

import sys
import subprocess
import os
import re
import datetime

UPDATE_INTERVAL = 15 # in secs

BATTERY_LEVEL_LOW       = 30 # in %
BATTERY_LEVEL_CRITICAL  = 20 # in %

RAM_LEFT_WARNING  = 300
RAM_LEFT_CRITICAL = 75

CPU_TEMP_CRITITCAL = 80

LOGFILE = "/home/fran/.batterylog"

F_ENERGY_NOW  = "/sys/class/power_supply/BAT0/energy_now"
F_ENERGY_FULL = "/sys/class/power_supply/BAT0/energy_full"
F_STATUS      = "/sys/class/power_supply/BAT0/status"
F_VOLTAGE_NOW = "/sys/class/power_supply/BAT0/voltage_now"
F_POWER_NOW   = "/sys/class/power_supply/BAT0/power_now"

F_BACKLIGHT_CURRENT = '/sys/class/backlight/intel_backlight/brightness'
F_BACKLIGHT_MAX     = '/sys/class/backlight/intel_backlight/max_brightness'

# TODO:
# Add logfile backup
# ...

class Monitor:

    def __init__(self):

        # Battery
        self.battery = {}
        self.battery['percentage'] = 999
        self.battery['status'] = 'Unknown'
        self.battery['level'] = 'NORMAL'

        # Blanking
        self.blanking_allowed = True

        # Suspend
        self.suspend_allowed = True

        # RAM clean
        self.ram_clean_allowed = True

        # Icon
        self.icon = Gtk.StatusIcon()
        self.set_icon('battery_full')

        self.icon.connect('activate',   self.on_right_click_event, 3, Gtk.get_current_event_time())
        self.icon.connect('popup-menu', self.on_right_click_event)
        self.icon.connect('scroll-event', self.on_scroll_event)

        self.icon.set_has_tooltip(True)
        self.icon.connect("query-tooltip", self.tooltip_query)

        Notify.init ("monitor")

        self.create_menu()

        self.update()
        GObject.timeout_add_seconds(UPDATE_INTERVAL, self.update)


    def set_icon(self, name):
        self.icon.set_from_icon_name(name)

    def add_seperator(self):
        m_item = Gtk.SeparatorMenuItem()
        self.menu.append(m_item)
        self.menu.show_all()

    def on_left_click_event(self, icon, button):
        print('click')

    def create_menu(self):

        self.menu = Gtk.Menu()

        # Battery
        self.info_battery = Gtk.MenuItem()
        self.info_temp = Gtk.MenuItem()
        self.info_ram = Gtk.MenuItem()

        sep1 = Gtk.SeparatorMenuItem.new()
        sep2 = Gtk.SeparatorMenuItem.new()
        sep3 = Gtk.SeparatorMenuItem.new()

        self.menu.append(self.info_battery)
        self.menu.append(sep1)
        self.menu.append(self.info_temp)
        self.menu.append(sep2)
        self.menu.append(self.info_ram)
        self.menu.append(sep3)

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

        self.menu.append(self.item_pause_blank)
        self.menu.append(self.item_pause_suspend)
        self.menu.append(self.item_pause_clean)
        self.menu.append(quit)

        self.menu.show_all()


    def on_right_click_event(self, icon, button, time):

        self.info_battery.set_label('%s, %i%%, %.2fmW' % (self.battery['status'], self.battery['percentage'], self.battery['power']))

        temperature = self.check_cpu_temperature()
        self.info_temp.set_label('CPU temp: %iC, %iC' % (temperature[0], temperature[1]))

        ram = self.check_ram_usage()
        self.info_ram.set_label('Free RAM: %iMB' % (ram))

        self.menu.popup(None, None, None, self.icon, button, time)

    def on_scroll_event(self, icon, event):
        direction = event.direction
        if direction == Gdk.ScrollDirection.UP:
            self.change_brightness(+1)
        elif direction == Gdk.ScrollDirection.DOWN:
            self.change_brightness(-1)

    def show_notification(self, text, icon, urg):
        # NotifyNotification *noti = notify_notification_new("batterytray", text, icon);
        # notify_notification_set_urgency(noti, urg);
        # notify_notification_show(noti, NULL);
        # g_object_unref(G_OBJECT(noti));
        return


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

    def get_cmd_output(self, cmd):
        try:
            if isinstance(cmd, list):
                output = subprocess.check_output(cmd, stderr=subprocess.DEVNULL)
            else:
                output = subprocess.check_output(cmd, stderr=subprocess.DEVNULL, shell=True)
        except subprocess.CalledProcessError:
            return ''

        return output.decode('utf8').strip()

    ## Brightness
    def get_current_brightness(self):
        with open(F_BACKLIGHT_CURRENT) as curr_file:
            return int(curr_file.read().split('\n')[0])

    def get_max_brightness(self):
        with open(F_BACKLIGHT_MAX) as max_file:
            return int(max_file.read().split('\n')[0])

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


    ## RAM
    def check_ram_usage(self):
        return int(self.get_cmd_output("free -m | grep Mem | awk '{print $7}'").split('\n')[0])

    ## Temperature
    def check_cpu_temperature(self):

        out = self.get_cmd_output(['sensors',]).split('\n')

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

    def update(self):

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
        icon_name = self.get_icon_name(status, percentage)
        self.set_icon(icon_name)

        # show notification if necessary
        if status == self.battery['status'] and status == 'Discharging':
            if percentage < BATTERY_LEVEL_CRITICAL and self.battery['level'] == 'LOW':
                self.send_notification("Battery is under 10%. Suspending in 2 minutes...",
                                       "dialog-information")
                self.battery['level'] = 'CRITICAL'

            elif (percentage <= BATTERY_LEVEL_LOW and self.battery['level'] == 'NORMAL'):
                self.send_notification("Battery is under 15%.",
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
        with open(LOGFILE, "a") as f:
            today = datetime.datetime.today()

            date_str = today.strftime('%Y-%m-%d %H:%M:%S')
            bat_str = '%02d%% %s %.2f' % (percentage, status, power)

            f.write('%s %s\n' % (date_str, bat_str))

        # suspend when reaches BATTERY_LEVEL_CRITICAL-1
        if self.suspend_allowed and status == 'Discharging' and percentage < (BATTERY_LEVEL_CRITICAL-2):
            os.system("systemctl suspend")


        # Check RAM and CPU temperatura and change icon if
        ram_usage = self.check_ram_usage()
        if self.ram_clean_allowed and ram_usage < RAM_LEFT_CRITICAL:
            os.system('killall chromium')
        elif ram_usage < RAM_LEFT_WARNING:
            self.set_icon('software-update-urgent')

        temperatures = self.check_cpu_temperature()
        for temp in temperatures:
            if temp > CPU_TEMP_CRITITCAL:
                self.set_icon('apport')
                break

        # Check discharging rate
        if status == 'Discharging' and power > 25.:
            self.set_icon('apport')

        return True

    def tooltip_query(self, widget, x, y, keyboard_mode, tooltip):

        #  update tooltip
        status = self.battery['status']

        if status == 'Discharging':
            h, m, s = self.battery['time']
            tooltip_text = "Discharging, %i%% (%02d:%02d remaining)\n using %2.2f W" % (self.battery['percentage'], h, m, self.battery['power'])
        elif status == 'Charging':
            tooltip_text = "Charging, %i%%" % self.battery['percentage']
        elif status == 'Full':
            tooltip_text = "Full, %i%%" % self.battery['percentage']
        else:
            tooltip_text = "Unknown, %i%%" % self.battery['percentage']

        tooltip.set_text(tooltip_text)

        return True


    def send_notification(self, msg, type_):
        noti = Notify.Notification.new('Monitor', msg, type_)
        noti.show()


    def get_icon_name(self, status, percentage):

        tmp = ''
        if status == 'Discharging':
            if percentage < BATTERY_LEVEL_CRITICAL:
                tmp = "battery_empty";
            elif percentage < BATTERY_LEVEL_LOW:
                tmp = "battery_caution"
            elif percentage < 45:
                tmp = "battery_low"
            elif percentage < 65:
                tmp = "battery_two_thirds"
            elif percentage < 75:
                tmp = "battery_third_fouth"
            else:
                tmp = "battery_full"

        elif status == 'Charging':
            tmp = "battery_plugged"

        elif status == 'Full':
            tmp = "battery_charged"
        elif status == 'Unknown':
            if percentage > 95:
                tmp = "battery_plugged"
            else:
                tmp = "dialog-question"
        else:
            tmp = "dialog-question"

        return tmp

    def run(self):
        Gtk.main()



if __name__ == '__main__':
    m = Monitor()
    m.run()
