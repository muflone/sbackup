#   Simple Backup - handling of preferences
#
#   Copyright (c)2019: Fabio Castelli (Muflone) <muflone@vbsimple.net>
#   Copyright (c)2010: Jean-Peer Lorenz <peer.loz@gmx.net>
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
"""
:mod:`sbackup.util.prefs` -- handling of preferences
======================================================

.. module:: prefs
   :synopsis: Handling of preferences applied to all profiles (in contrast to profile settings)
.. moduleauthor:: Jean-Peer Lorenz <peer.loz@gmx.net>

"""

SECTION_OPTIONS = 'options'
FS_BACKEND_GIO = 'gio'
FS_BACKEND_FUSE = 'fuse'

PREFS_FS_BACKEND = 'fs_backend'

import configparser
import os.path

from xdg import BaseDirectory

from . import structs


class Preferences(object, metaclass=structs.Singleton):
    def __init__(self):
        self._config = configparser.RawConfigParser()
        self._config.read(os.path.join(
            BaseDirectory.save_config_path('sbackup'), 'settings.conf'))

    def get(self, key):
        _value = self._get_value(key)
        return _value

    def _get_value(self, key):
        _value = None
        if self._config.has_section(SECTION_OPTIONS) and \
                self._config.has_option(SECTION_OPTIONS, key):
            _value = self._config.get(SECTION_OPTIONS, key)
        return _value

    def _set_value(self, key, value):
        if not self._config.has_section(SECTION_OPTIONS):
            self._config.add_section(SECTION_OPTIONS)
        self._config.set(SECTION_OPTIONS, key, value)
