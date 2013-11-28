#!/usr/bin/python
# -*- coding: utf-8; -*-
"""
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

from gi.repository import Gtk, Gdk, GdkPixbuf, GObject
from config import ConfigManager
import os

class Preferences():

    def __init__(self):
        
        self.init_ui()

    def init_ui(self):
        builder = Gtk.Builder()
        builder.add_from_file(ConfigManager.data_dir + 'ui/preferences.ui')

        self.window = builder.get_object('preferences_window')
        self.window.connect('destroy', self.on_cancel_clicked)

        self.logo = builder.get_object('terra_logo')
        self.logo_buffer = GdkPixbuf.Pixbuf.new_from_file_at_size(ConfigManager.data_dir + 'image/terra.svg', 64, 64)
        self.logo.set_from_pixbuf(self.logo_buffer)

        self.version = builder.get_object('version')
        self.version.set_label('Version: ' + ConfigManager.version)

        self.btn_cancel = builder.get_object('btn_cancel')
        self.btn_cancel.connect('clicked', self.on_cancel_clicked)

        self.btn_apply = builder.get_object('btn_apply')
        self.btn_apply.connect('clicked', self.on_apply_clicked)

        self.btn_ok = builder.get_object('btn_ok')
        self.btn_ok.connect('clicked', self.on_ok_clicked)

        self.adj_seperator = builder.get_object('adjustment_seperator')
        self.adj_seperator.set_value(int(ConfigManager.get_conf('seperator-size')) * 1.0)

        self.adj_width = builder.get_object('adjustment_width')
        self.adj_width.set_value(int(ConfigManager.get_conf('width')) * 1.0)

        self.adj_height = builder.get_object('adjustment_height')
        self.adj_height.set_value(int(ConfigManager.get_conf('height')) * 1.0)

        self.adj_transparency = builder.get_object('adjustment_transparency')
        self.adj_transparency.set_value(int(ConfigManager.get_conf('transparency')) * 1.0)

        self.v_alig = builder.get_object('v_alig')
        self.v_alig.set_active(int(ConfigManager.get_conf('vertical-position')) / 50)

        self.h_alig = builder.get_object('h_alig')
        self.h_alig.set_active(int(ConfigManager.get_conf('horizontal-position')) / 50)

        self.chk_hide_from_taskbar = builder.get_object('chk_hide_from_taskbar')
        self.chk_hide_from_taskbar.set_active(ConfigManager.get_conf('skip-taskbar'))

        self.chk_use_border = builder.get_object('chk_use_border')
        self.chk_use_border.set_active(ConfigManager.get_conf('use-border'))

        self.color_text = builder.get_object('color_text')
        self.color_text.set_color(Gdk.color_parse(ConfigManager.get_conf('color-text')))

        self.color_background = builder.get_object('color_background')
        self.color_background.set_color(Gdk.color_parse(ConfigManager.get_conf('color-background')))

        self.entry_shell = builder.get_object('entry_shell')
        self.entry_shell.set_text(ConfigManager.get_conf('shell'))

        self.dir_custom = builder.get_object('dir_custom')

        self.radio_home = builder.get_object('radio_home')
        self.radio_pwd = builder.get_object('radio_pwd')
        self.radio_dir_custom = builder.get_object('radio_dir_custom')
        self.radio_dir_custom.connect('toggled', lambda w: self.dir_custom.set_sensitive(self.radio_dir_custom.get_active()))

        dir_conf = ConfigManager.get_conf('dir')
        if dir_conf == '$home$':
            self.radio_home.set_active(True)
        elif dir_conf == '$pwd$':
            self.radio_pwd.set_active(True)
        else:
            self.radio_dir_custom.set_active(True)
            self.dir_custom.set_text(dir_conf)
            self.dir_custom.set_sensitive(True)

        self.background_image = builder.get_object('background_image')
        self.background_image.set_filename(ConfigManager.get_conf('background-image'))

        self.clear_background_image = builder.get_object('clear_background_image')
        self.clear_background_image.connect('clicked', lambda w: self.background_image.unselect_all())

        self.font_name = builder.get_object('font_name')
        self.font_name.set_font_name(ConfigManager.get_conf('font-name'))

        self.chk_use_system_font = builder.get_object('chk_use_system_font')
        self.chk_use_system_font.connect('toggled', lambda w: self.font_name.set_sensitive(not self.chk_use_system_font.get_active()))
        self.chk_use_system_font.set_active(ConfigManager.get_conf('use-default-font'))

        self.chk_show_scrollbar = builder.get_object('chk_show_scrollbar')
        self.chk_show_scrollbar.set_active(ConfigManager.get_conf('show-scrollbar'))

        self.chk_always_on_top = builder.get_object('chk_always_on_top')
        self.chk_always_on_top.set_active(ConfigManager.get_conf('always-on-top'))

        self.chk_losefocus = builder.get_object('chk_losefocus')
        self.chk_losefocus.set_active(ConfigManager.get_conf('losefocus-hiding'))

        self.chk_hide_on_start = builder.get_object('chk_hide_on_start')
        self.chk_hide_on_start.set_active(ConfigManager.get_conf('hide-on-start'))

        self.fullscreen_key = builder.get_object('fullscreen_key')
        self.fullscreen_key.set_text(ConfigManager.get_conf('fullscreen-key'))
        self.fullscreen_key.connect('key-press-event', self.generate_key_string)

        self.quit_key = builder.get_object('quit_key')
        self.quit_key.set_text(ConfigManager.get_conf('quit-key'))
        self.quit_key.connect('key-press-event', self.generate_key_string)

        self.new_page_key = builder.get_object('new_page_key')
        self.new_page_key.set_text(ConfigManager.get_conf('new-page-key'))
        self.new_page_key.connect('key-press-event', self.generate_key_string)

        self.close_page_key = builder.get_object('close_page_key')
        self.close_page_key.set_text(ConfigManager.get_conf('close-page-key'))
        self.close_page_key.connect('key-press-event', self.generate_key_string)

        self.rename_page_key = builder.get_object('rename_page_key')
        self.rename_page_key.set_text(ConfigManager.get_conf('rename-page-key'))
        self.rename_page_key.connect('key-press-event', self.generate_key_string)

        self.next_page_key = builder.get_object('next_page_key')
        self.next_page_key.set_text(ConfigManager.get_conf('next-page-key'))
        self.next_page_key.connect('key-press-event', self.generate_key_string)

        self.prev_page_key = builder.get_object('prev_page_key')
        self.prev_page_key.set_text(ConfigManager.get_conf('prev-page-key'))
        self.prev_page_key.connect('key-press-event', self.generate_key_string)

        self.global_key = builder.get_object('global_key')
        self.global_key.set_text(ConfigManager.get_conf('global-key'))
        self.global_key.connect('key-press-event', self.generate_key_string)

        self.select_all_key = builder.get_object('select_all_key')
        self.select_all_key.set_text(ConfigManager.get_conf('select-all-key'))
        self.select_all_key.connect('key-press-event', self.generate_key_string)

        self.copy_key = builder.get_object('copy_key')
        self.copy_key.set_text(ConfigManager.get_conf('copy-key'))
        self.copy_key.connect('key-press-event', self.generate_key_string)

        self.paste_key = builder.get_object('paste_key')
        self.paste_key.set_text(ConfigManager.get_conf('paste-key'))
        self.paste_key.connect('key-press-event', self.generate_key_string)

        self.split_v_key = builder.get_object('split_v_key')
        self.split_v_key.set_text(ConfigManager.get_conf('split-v-key'))
        self.split_v_key.connect('key-press-event', self.generate_key_string)

        self.split_h_key = builder.get_object('split_h_key')
        self.split_h_key.set_text(ConfigManager.get_conf('split-h-key'))
        self.split_h_key.connect('key-press-event', self.generate_key_string)

        self.close_node_key = builder.get_object('close_node_key')
        self.close_node_key.set_text(ConfigManager.get_conf('close-node-key'))
        self.close_node_key.connect('key-press-event', self.generate_key_string)

        self.chk_run_on_startup = builder.get_object('chk_run_on_startup')
        self.chk_run_on_startup.set_active(os.path.exists(os.environ['HOME'] + '/.config/autostart/terra.desktop'))

        self.open_project_homepage = builder.get_object('open_project_homepage')
        self.open_project_homepage.connect('clicked', lambda w: os.system('xdg-open https://launchpad.net/terra'))

        self.report_bug = builder.get_object('report_bug')
        self.report_bug.connect('clicked', lambda w: os.system('xdg-open https://bugs.launchpad.net/terra/+filebug'))



    def generate_key_string(self, widget, event):
        key_str = ''

        if ((Gdk.ModifierType.CONTROL_MASK & event.state) == Gdk.ModifierType.CONTROL_MASK):
            key_str = key_str + '<Control>'

        if ((Gdk.ModifierType.MOD1_MASK & event.state) == Gdk.ModifierType.MOD1_MASK):
            key_str = key_str + '<Alt>'

        if ((Gdk.ModifierType.SHIFT_MASK & event.state) == Gdk.ModifierType.SHIFT_MASK):
            key_str = key_str + '<Shift>'

        if ((Gdk.ModifierType.SUPER_MASK & event.state) == Gdk.ModifierType.SUPER_MASK):
            key_str = key_str + '<Super>'

        key_str = key_str + Gdk.keyval_name(event.keyval)

        widget.set_text(key_str)

    def show(self):
        self.window.show_all()

    def on_apply_clicked(self, widget):
        ConfigManager.set_conf('seperator-size', int(self.adj_seperator.get_value()))

        ConfigManager.set_conf('width', int(self.adj_width.get_value()))

        ConfigManager.set_conf('height', int(self.adj_height.get_value()))

        ConfigManager.set_conf('transparency', int(self.adj_transparency.get_value()))

        ConfigManager.set_conf('vertical-position', self.v_alig.get_active() * 50)

        ConfigManager.set_conf('horizontal-position', self.h_alig.get_active() * 50)

        ConfigManager.set_conf('skip-taskbar', self.chk_hide_from_taskbar.get_active())

        ConfigManager.set_conf('use-border', self.chk_use_border.get_active())

        ConfigManager.set_conf('color-text', self.color_text.get_color().to_string())

        ConfigManager.set_conf('color-background', self.color_background.get_color().to_string())

        ConfigManager.set_conf('shell', self.entry_shell.get_text())

        if self.radio_home.get_active():
            ConfigManager.set_conf('dir', '$home$')
        elif self.radio_pwd.get_active():
            ConfigManager.set_conf('dir', '$pwd$')
        else:
            ConfigManager.set_conf('dir', self.dir_custom.get_text())

        ConfigManager.set_conf('background-image', self.background_image.get_filename())

        ConfigManager.set_conf('use-default-font', self.chk_use_system_font.get_active())

        ConfigManager.set_conf('font-name', self.font_name.get_font_name())

        ConfigManager.set_conf('show-scrollbar', self.chk_show_scrollbar.get_active())

        ConfigManager.set_conf('always-on-top', self.chk_always_on_top.get_active())

        ConfigManager.set_conf('losefocus-hiding', self.chk_losefocus.get_active())

        ConfigManager.set_conf('hide-on-start', self.chk_hide_on_start.get_active())

        ConfigManager.set_conf('fullscreen-key', self.fullscreen_key.get_text())

        ConfigManager.set_conf('quit-key', self.quit_key.get_text())

        ConfigManager.set_conf('new-page-key', self.new_page_key.get_text())

        ConfigManager.set_conf('close-page-key', self.close_page_key.get_text())

        ConfigManager.set_conf('rename-page-key', self.rename_page_key.get_text())

        ConfigManager.set_conf('next-page-key', self.next_page_key.get_text())

        ConfigManager.set_conf('prev-page-key', self.prev_page_key.get_text())

        ConfigManager.set_conf('global-key', self.global_key.get_text())

        ConfigManager.set_conf('select-all-key', self.select_all_key.get_text())

        ConfigManager.set_conf('copy-key', self.copy_key.get_text())

        ConfigManager.set_conf('paste-key', self.paste_key.get_text())

        ConfigManager.set_conf('split-h-key', self.split_h_key.get_text())

        ConfigManager.set_conf('split-v-key', self.split_v_key.get_text())

        ConfigManager.set_conf('close-node-key', self.close_node_key.get_text())

        if (self.chk_run_on_startup.get_active() and not os.path.exists(os.environ['HOME'] + '/.config/autostart/terra.desktop')):
            os.system('cp /usr/share/applications/terra.desktop ' + os.environ['HOME'] + '/.config/autostart/terra.desktop')

        if (not self.chk_run_on_startup.get_active() and os.path.exists(os.environ['HOME'] + '/.config/autostart/terra.desktop')):
            os.system('rm -f ' + os.environ['HOME'] + '/.config/autostart/terra.desktop')

        ConfigManager.save_config()
        ConfigManager.callback()

    def on_ok_clicked(self, widget):
        self.on_apply_clicked(self.btn_ok)
        self.window.hide()
        ConfigManager.disable_losefocus_temporary = False

    def on_cancel_clicked(self, widget):
        self.window.hide()
        ConfigManager.disable_losefocus_temporary = False
