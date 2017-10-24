#!/usr/bin/env python
# coding: utf-8
#
# Authorization module software developed for the staircase door access control at Hackerspace Kraków.
# Copyright (C) 2016 Tadeusz Magura-Witkowski
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from collections import defaultdict

from auth_plugin import EnterpriseAuthPlugin, main

VALID_PIN = [1, 2, 3, 4]

class Zone(object):
	def __init__(self):
		super(Zone, self).__init__()

		self._buffer = []
		
	def incoming_key(self, key):
		if key == 11: # '#' key
			open_doors = self._buffer == VALID_PIN
			self._buffer = []

			return open_doors

		self._buffer = self._buffer[-len(VALID_PIN):]
		self._buffer.append(key)


class PinEntryAuthPlugin(EnterpriseAuthPlugin):
	def __init__(self):
		super(PinEntryAuthPlugin, self).__init__()
		self.name = 'Example pin-entry plugin'

		self._zones = defaultdict(Zone)

	def on_keypress(self, zoneid, keycode):
		retval = self._zones[zoneid].incoming_key(keycode)

		if retval is None:
			return

		if retval:
			self.accept(zoneid)
		else:
			self.reject(zoneid)


if __name__ == '__main__':
	main(PinEntryAuthPlugin)