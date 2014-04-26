#!/usr/bin/python
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

from layout import LayoutManager
from i18n import t
from terminal import TerminalWinContainer

import sys

Wins = None

def quit_prog():
   global Wins

   Wins.app_quit()

def save_conf():
    global Wins

    Wins.save_conf()

def create_app():
    global Wins

    Wins.create_app()

def remove_app(app):
    global Wins

    Wins.remove_app(app)

def main():
    global Wins

    if (len(sys.argv) > 1):
        print("Terra Doesn't support any argument")
        return 1

    Wins = TerminalWinContainer()
    try:
        LayoutManager.init()
        for section in LayoutManager.get_sections():
            if (section.find("screen-") == 0 and (LayoutManager.get_conf(section, 'enabled'))):
                Wins.create_app(section)
        if (len(Wins.get_apps()) == 0):
            Wins.create_app()
        if (len(Wins.get_apps()) == 0):
            print("Cannot initiate any screen")
            return
    except Exception as excep:
        print("Exception Catched:")
        print(excep)
        Wins.app_quit()
    except:
        print("Unknow Exception Catched")
        Wins.app_quit()
    else:
        Wins.start()

if __name__ == "__main__":
    main()
