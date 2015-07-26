#!/usr/bin/env python2

import os
import sys

from gi.repository import Gtk


class TerraInputDialog(Gtk.Dialog):
    def __init__(self, parent, title, label):
        Gtk.Dialog.__init__(
            self, title, parent, 0,
            (
                Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                Gtk.STOCK_APPLY, Gtk.ResponseType.APPLY,
            )
        )

        # Set the default widget.
        self.set_default_response(Gtk.ResponseType.APPLY)

        box = self.get_content_area()
        """:type: Gtk.Box"""
        box.set_spacing(16)
        box.set_border_width(16)

        grid = Gtk.Grid(column_spacing=8, row_spacing=16)
        box.add(grid)

        label = Gtk.Label(label)
        grid.add(label)

        entry = Gtk.Entry()
        entry_text = '/bin/bash2'
        entry.set_text(entry_text)
        entry.set_can_focus(True)
        entry.set_activates_default(True)
        grid.attach_next_to(entry, label, Gtk.PositionType.RIGHT, 2, 1)

        self.show_all()


class DialogWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Dialog Example")

        self.set_border_width(6)

        button = Gtk.Button("Open dialog")
        button.connect("clicked", self.on_button_clicked)

        self.add(button)

    def on_button_clicked(self, widget):
        dialog = TerraInputDialog(
            parent=self,
            title='Change Shell Command',
            label='Shell Command:',
        )
        response = dialog.run()

        if response == Gtk.ResponseType.APPLY:
            print("The APPLY button was clicked")
        elif response == Gtk.ResponseType.CANCEL:
            print("The Cancel button was clicked")

        dialog.destroy()

win = DialogWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
