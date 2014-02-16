# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# Copyright (C) 2014 <Gabriel Barbosa Nascimento> <barbosanascimentogabriel@gmail.com>
# Copyright (C) 2014 <Archisman Panigrahi> <apandada1@gmail.com>
# This program is free software: you can redistribute it and/or modify it 
# under the terms of the GNU General Public License version 3, as published 
# by the Free Software Foundation.
# 
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranties of 
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR 
# PURPOSE.  See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along 
# with this program.  If not, see <http://www.gnu.org/licenses/>.
### END LICENSE

### DO NOT EDIT THIS FILE ###

from gi.repository import Gio, Gtk # pylint: disable=E0611
import logging
logger = logging.getLogger('up_clock_lib')

from . helpers import get_builder, show_uri, get_help_uri

# This class is meant to be subclassed by UpClockWindow.  It provides
# common functions and some boilerplate.
class Window(Gtk.Window):
    __gtype_name__ = "Window"

    # To construct a new instance of this method, the following notable 
    # methods are called in this order:
    # __new__(cls)
    # __init__(self)
    # finish_initializing(self, builder)
    # __init__(self)
    #
    # For this reason, it's recommended you leave __init__ empty and put
    # your initialization code in finish_initializing
    
    def __new__(cls):
        """Special static method that's automatically called by Python when 
        constructing a new instance of this class.
        
        Returns a fully instantiated BaseUpClockWindow object.
        """
        builder = get_builder('UpClockWindow')
        new_object = builder.get_object("up_clock_window")
        new_object.finish_initializing(builder)
        return new_object

    def finish_initializing(self, builder):
        """Called while initializing this instance in __new__

        finish_initializing should be called after parsing the UI definition
        and creating a UpClockWindow object with it in order to finish
        initializing the start of the new UpClockWindow instance.
        """
        # Get a reference to the builder and set up the signals.
        self.builder = builder
        self.ui = builder.get_ui(self, True)

        self.settings = Gio.Settings("net.launchpad.up-clock")

        # Optional application indicator support
        # Run 'quickly add indicator' to get started.
        # More information:
        #  http://owaislone.org/quickly-add-indicator/
        #  https://wiki.ubuntu.com/DesktopExperienceTeam/ApplicationIndicators
        try:
            from up_clock import indicator
            # self is passed so methods of this class can be called from indicator.py
            # Comment this next line out to disable appindicator
            self.indicator = indicator.new_application_indicator(self)
        except ImportError:
            pass

    def on_mnu_contents_activate(self, widget, data=None):
        show_uri(self, "ghelp:%s" % get_help_uri())

        # destroy command moved into dialog to allow for a help button

    def on_mnu_close_activate(self, widget, data=None):
        """Signal handler for closing the UpClockWindow."""
        self.destroy()

    def on_destroy(self, widget, data=None):
        """Called when the UpClockWindow is closed."""
        # Clean up code for saving application state should be added here.
        Gtk.main_quit()



