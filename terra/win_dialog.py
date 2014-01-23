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

from gi.repository import Gtk, Gdk

from config import ConfigManager
from layout import LayoutManager

class WinDialog:
    def __init__(self, sender, active_terminal):
        ConfigManager.disable_losefocus_temporary = True
        self.sender = sender
        self.active_terminal = active_terminal

        self.builder = Gtk.Builder()
        self.builder.set_translation_domain('terra')
        self.builder.add_from_file(ConfigManager.data_dir + 'ui/main.ui')
        self.dialog = self.builder.get_object('win_dialog')

        self.window = self.sender.get_container().parent
        self.dialog.v_alig = self.builder.get_object('v_alig')
        self.dialog.v_alig.set_active(int(LayoutManager.get_conf(self.window.name, 'vertical-position')) / 50)

        self.dialog.h_alig = self.builder.get_object('h_alig')
        self.dialog.h_alig.set_active(int(LayoutManager.get_conf(self.window.name, 'horizontal-position')) / 50)

        self.dialog.btn_cancel = self.builder.get_object('btn_cancela')
        self.dialog.btn_ok = self.builder.get_object('btn_oka')

        self.dialog.btn_cancel.connect('clicked', lambda w: self.close())
        self.dialog.btn_ok.connect('clicked', lambda w: self.update())

        self.dialog.connect('delete-event', lambda w, x: self.close())
        self.dialog.connect('destroy', lambda w: self.close())

        self.dialog.show_all()

    def on_keypress(self, widget, event):
        if Gdk.keyval_name(event.keyval) == 'Return':
            self.update()

    def close(self):
        self.dialog.destroy()
        self.active_terminal.grab_focus()
        ConfigManager.disable_losefocus_temporary = False
        del self

    def update(self):
        LayoutManager.set_conf(self.window.name, 'vertical-position', self.dialog.v_alig.get_active() * 50)
        LayoutManager.set_conf(self.window.name, 'horizontal-position', self.dialog.h_alig.get_active() * 50)
        LayoutManager.save_config()
        self.window.update_ui()
        ConfigManager.disable_losefocus_temporary = False
        self.close()