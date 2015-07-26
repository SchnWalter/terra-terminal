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

import os
import sys

from gi.repository import Gtk

from terra.handlers import TerraHandler
from terra.handlers import t


class ShellDialog:
    def __init__(self, sender, parent_window):
        """
        :type sender: terra.VteObject.VteObject
        :type parent_window: Gtk.Window
        """

        shell_ui_file = os.path.join(TerraHandler.get_resources_path(), 'shell.ui')
        if not os.path.exists(shell_ui_file):
            msg = t('UI data file is missing: {}')
            sys.exit(msg.format(shell_ui_file))

        builder = Gtk.Builder()
        builder.set_translation_domain('terra')
        builder.add_from_file(shell_ui_file)

        dialog = builder.get_object('shell_command_dialog')
        """:type: Gtk.Dialog"""

        # Associate the dialog with the main window.
        dialog.set_transient_for(parent_window)

        # Attach ShellDialog class methods as signal handlers.
        builder.connect_signals(self)

        # Add the "sender" to the dialog.
        # TODO: Rename!
        dialog.sender = sender

        dialog.shell_command_path_entry = builder.get_object('shell_command_path_entry')
        """:type: Gtk.Entry"""
        dialog.shell_command_path_entry.set_text(dialog.sender.progname)

        if hasattr(dialog.sender, 'progname') and dialog.sender.progname:
            # Set the entry text.
            dialog.shell_command_path_entry.set_text(dialog.sender.progname)

            # Selected the entry text.
            dialog.shell_command_path_entry.grab_focus()

        # TODO: Use the run() method.
        dialog.show_all()

    @staticmethod
    def on_cancel_button_clicked(widget):
        """
        :type widget: Gtk.Button
        """

        dialog = widget.get_toplevel()
        """:type: Gtk.Dialog"""

        dialog.destroy()

    @staticmethod
    def on_apply_button_clicked(widget):
        """
        :type widget: Gtk.Button
        """

        dialog = widget.get_toplevel()
        """:type: Gtk.Dialog"""

        old_shell_command = dialog.sender.progname

        # TODO: Notify the user about what is happening and cleanup the VTE screen.
        try:
            dialog.sender.progname = dialog.shell_command_path_entry.get_text()
            dialog.sender.fork_process(dialog.sender.progname)
        except:
            dialog.sender.progname = old_shell_command

        dialog.destroy()

    @staticmethod
    def on_shell_command_dialog_close(widget):
        """
        :type widget: Gtk.Dialog
        """

        widget.destroy()
