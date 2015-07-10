# -*- coding: utf-8; -*-
"""
Copyright (C) 2013 - Arnaud SOURIOUX <six.dsn@gmail.com>
Copyright (C) 2012 - Ozcan ESEN <ozcanesen~gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>

"""

import sys
import time

from gi.repository import Gtk, Gdk

import terra.globalhotkeys

from terra.dbusservice import DbusService
from terra.interfaces.terminal import TerminalWin
from terra.handlers import t
from terra.handlers import TerraHandler


class TerminalWinContainer:
    def __init__(self):
        terra.globalhotkeys.init()
        tries = 0
        while True:
            try:
                self.hotkey = terra.globalhotkeys.GlobalHotkey()
            except SystemError:
                tries += 1
                if tries >= 2:
                    sys.exit(t("Can't get GlobalHotkeys instance."))
                time.sleep(1)
            else:
                break

        global_key_string = TerraHandler.config['shortcuts']['global_key']
        if global_key_string:
            if not self.hotkey.bind(global_key_string, lambda w: self.show_hide()):
                sys.exit(t("Can't bind global hotkey: Another Instance of Terra is probably running."))

        self.apps = []
        self.window_id = 0
        self.on_doing = False
        self.is_running = False

    def show_hide(self):
        if not self.on_doing:
            self.on_doing = True
            for app in self.apps:
                app.show_hide()
            self.on_doing = False

    def update_ui(self):
        if not self.on_doing:
            self.on_doing = True
            for app in self.apps:
                app.update_ui()
            self.on_doing = False

    def save_conf(self):
        for app in self.apps:
            app.save_conf()

    def app_quit(self):
        for app in self.apps:
            app.quit()
        sys.stdout.flush()
        sys.stderr.flush()
        if self.is_running:
            Gtk.main_quit()

    def remove_app(self, ext):
        """
        :type ext: TerminalWin
        """
        if ext in self.apps:
            self.apps.remove(ext)
            print("window name is:", ext.name)
            if ext.name in TerraHandler.config:
                # Delete the window settings.
                del TerraHandler.config[ext.name]

        if len(self.apps) == 0:
            self.app_quit()

    # TODO: Properly create new terminal windows.
    def create_app(self, window_name=None):
        """
        :type window_name: str
        """
        # Retrieve information about the window settings.
        window_name, window_settings = self.get_window_settings(window_name)

        if window_settings['disabled']:
            print("[DEBUG] Not creating disabled window: {}".format(window_name))
            return

        # TODO: Pass the whole settings dictionary to TerminalWin().
        partial_settings = Gdk.Rectangle()
        partial_settings.x = window_settings['posx']
        partial_settings.y = window_settings['posy']
        partial_settings.width = window_settings['width']
        partial_settings.height = window_settings['height']

        # Create new terminal window.
        window = TerminalWin(window_name, partial_settings)

        # Attach the global hotkey.
        window.hotkey = self.hotkey

        # Initialize inter-process communication.
        if len(self.apps) == 0:
            DbusService(window)

        # Add to the list of running windows.
        self.apps.append(window)

    def get_apps(self):
        return self.apps

    def start(self):
        self.is_running = True
        Gtk.main()

    def get_window_settings(self, window_name):
        if window_name is None:
            window_name = str('layout-screen-%d' % self.window_id)

        # TODO: Find a different way to manage the screen IDs.
        # This can cause screen IDs to get to huge numbers in the long term.
        new_window_id = max(self.window_id, int(window_name.split('-')[2])) + 1

        updated_window_name = None
        if new_window_id != self.window_id:
            updated_window_name = str('layout-screen-%d' % new_window_id)
            self.window_id = new_window_id

        if updated_window_name:
            # Copy old settings.
            if window_name in TerraHandler.config:
                TerraHandler.config[updated_window_name] = TerraHandler.config[window_name]
                del TerraHandler.config[window_name]
                window_name = updated_window_name

        # TODO: Use a dedicated section or settings file to store window information.
        if window_name not in TerraHandler.config:
            TerraHandler.config[window_name] = TerraHandler.config['layout'].copy()

        return window_name, TerraHandler.config[window_name]
