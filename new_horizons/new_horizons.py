#!/usr/bin/env python2

import os
import sys

from gi.repository import Gtk, Gdk


class MainWindowSignalsHandler:
    @staticmethod
    def on_application_window_destroy(window):
        # Only quit the application when the last window was closed.
        if window.window_identifier in ApplicationHandler.windows:
            del ApplicationHandler.windows[window.window_identifier]

        if len(ApplicationHandler.windows) == 0:
            Gtk.main_quit(window)

    @staticmethod
    def on_close_button_clicked(widget):
        """
        :type widget: Gtk.Widget
        """
        window = widget.get_toplevel()
        if window:
            window.destroy()

    @staticmethod
    def on_fullscreen_button_clicked(widget):
        """
        :type widget: Gtk.Widget
        """
        window = widget.get_toplevel()
        """:type window: Gtk.Window"""

        if ApplicationHandler.windows[window.window_identifier].is_fullscreen:
            window.unfullscreen()
        else:
            window.fullscreen()

    @staticmethod
    def on_addstack_button_clicked(widget):
        """
        :type widget: Gtk.Widget
        """
        # Create a new tab.
        print('adding new stack!')

    @staticmethod
    def on_addwindow_button_clicked(widget):
        """
        :type widget: Gtk.Widget
        """
        # Create a new window.
        ApplicationHandler.create_window()

    @staticmethod
    def on_application_window_window_state_event(widget, event):
        # TODO: Add option to enable hiding the window when "Gdk.WindowState.FOCUSED" is lost.
        WindowHandler.is_fullscreen = bool(Gdk.WindowState.FULLSCREEN & event.new_window_state)


class WindowHandler(object):
    gtk_window = None
    """:type: Gtk.Window"""

    config = None
    """:type: dict"""

    is_fullscreen = False
    """:type: bool"""

    def __init__(self, window_config):
        self.config = window_config

        ui_builder_file = 'new_horizons.ui'
        if not os.path.exists(ui_builder_file):
            sys.exit('UI data file is missing: {}'.format(ui_builder_file))

        self.builder = Gtk.Builder()
        self.builder.add_from_file(ui_builder_file)

        self.gtk_window = self.builder.get_object('application_window')
        """:type: Gtk.Window"""
        self.gtk_window.connect('destroy', MainWindowSignalsHandler.on_close_button_clicked)
        # self.gtk_window.set_decorated(False)

        # Update the window position.
        if 'window_position' in window_config:
            self.update_position(window_config['window_position'])

        # The signals handler needs `WindowHandler.window` to exit.
        self.builder.connect_signals(MainWindowSignalsHandler())

        # Set the window ID.
        self.gtk_window.window_identifier = ApplicationHandler.last_window_identifier + 1
        ApplicationHandler.last_window_identifier = self.gtk_window.window_identifier

    def update_position(self, position_conf):
        # Get the Gdk.Screen information.
        gdk_screen = self.gtk_window.get_screen()
        """:type: Gdk.Screen"""

        # Get the index of screen among the screens in the display to which it belongs.
        screen_number = gdk_screen.get_number()

        # Get the screen geometry.
        screen_geometry = gdk_screen.get_monitor_geometry(screen_number)

        width = -1
        if 'width' in position_conf and position_conf['width']:
            if position_conf['width'][-1:] == '%':
                width = int(
                    float(position_conf['width'][:-1]) * screen_geometry.width / 100
                )

        height = -1
        if 'height' in position_conf:
            if position_conf['height'][-1:] == '%':
                height = int(
                    float(position_conf['height'][:-1]) * screen_geometry.height / 100
                )

        # Set the default size of the window.
        self.gtk_window.set_default_size(width, height)


class ApplicationHandler(object):
    windows = {}
    """:type: dict"""

    last_window_identifier = 0
    """:type: int"""

    default_window_config = {
        'window_position': {
            'vertical': 'top',
            'horizontal': 'left',
            'height': '60%',
            'width': '40%',
        }
    }

    @classmethod
    def __init__(cls):
        pass

    @classmethod
    def create_window(cls, window_config=None):
        if not window_config:
            window_config = cls.default_window_config

        new_window = WindowHandler(window_config)
        new_window.gtk_window.show_all()
        ApplicationHandler.windows[new_window.gtk_window.window_identifier] = new_window

        pass


# Create the first window.
ApplicationHandler.create_window()

Gtk.main()
