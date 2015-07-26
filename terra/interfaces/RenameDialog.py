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


# According to the Gnome application design patterns, the on_apply_button_clicked()
# method should be moved to the calling function. Once that change is made the
# ShellDialog and RenameDialog classes are the same thing.
# TODO: Merge ShellDialog and RenameDialog.
class RenameDialog:
    def __init__(self, sender, parent_window):
        """
        :type sender: terra.VteObject.VteObject
        :type parent_window: Gtk.Window
        """

        rename_ui_file = os.path.join(TerraHandler.get_resources_path(), 'rename.ui')
        if not os.path.exists(rename_ui_file):
            msg = t('UI data file is missing: {}')
            sys.exit(msg.format(rename_ui_file))

        builder = Gtk.Builder()
        builder.set_translation_domain('terra')
        builder.add_from_file(rename_ui_file)

        dialog = builder.get_object('rename_dialog')
        """:type: Gtk.Dialog"""

        # Associate the dialog with the main window.
        dialog.set_transient_for(parent_window)

        # Attach ShellDialog class methods as signal handlers.
        builder.connect_signals(self)

        # Add the "sender" to the dialog.
        # TODO: Rename!
        dialog.sender = sender

        dialog.new_name_entry = builder.get_object('new_name_entry')
        """:type: Gtk.Entry"""

        # Set the entry text.
        dialog.new_name_entry.set_text(dialog.sender.get_label())

        # Selected the entry text.
        dialog.new_name_entry.grab_focus()

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

        if dialog.new_name_entry.get_text() > 0:
            dialog.sender.set_label(dialog.new_name_entry.get_text())

        dialog.destroy()

    @staticmethod
    def on_shell_command_dialog_close(widget):
        """
        :type widget: Gtk.Dialog
        """

        widget.destroy()
