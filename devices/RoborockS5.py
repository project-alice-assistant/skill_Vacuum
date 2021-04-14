#  Copyright (c) 2021
#
#  This file, RoborockS5.py, is part of Project Alice.
#
#  Project Alice is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>
#
#  Last modified: 2021.04.15 at 01:30:27 MESZ

import socket
import sqlite3
import threading
from core.base.model.ProjectAliceObject import ProjectAliceObject
from core.commons import constants
from core.device.model.Device import Device
from core.device.model.DeviceAbility import DeviceAbility
from core.device.model.DeviceException import RequiresGuiSettings
from core.device.model.DeviceLink import DeviceLink
from core.device.model.DeviceType import DeviceType
from core.dialog.model.DialogSession import DialogSession
from core.myHome.model.Location import Location
from core.webui.model.DeviceClickReactionAction import DeviceClickReactionAction
from core.webui.model.OnDeviceClickReaction import OnDeviceClickReaction
from miio import Vacuum
from typing import Dict, List, Union


class RoborockS5(Device):

	@classmethod
	def getDeviceTypeDefinition(cls) -> dict:
		return {
			'deviceTypeName'        : 'RoborockS5',
			'perLocationLimit'      : 0,
			'totalDeviceLimit'      : 0,
			'allowLocationLinks'    : True,
			'allowHeartbeatOverride': False,
			'heartbeatRate'         : 0,
			'abilities'             : [DeviceAbility.NONE]
		}


	def __init__(self, data: Union[sqlite3.Row, Dict]):
		super().__init__(data)


	def onUIClick(self) -> dict:
		self.logInfo(f'searching for a roborock')
		ip = self.getConfig('ip')
		token = self.getConfig('token')

		# check device settings for ip and token -> end dialog: Please supply informaition via interface
		if not ip or not token:
			raise RequiresGuiSettings()

		# check settings by sending a command(Hello?)
		vac = self.getVac()
		serial = vac.serial_number()
		vac.find()
		# connected?
		self.pairingDone(uid=serial)
		return OnDeviceClickReaction(action=DeviceClickReactionAction.NONE.value).toDict()


	# required by every vacuum
	def clean(self, links: List[DeviceLink]):
		if not isinstance(links, List):
			links = [links]

		vac = self.getVac()
		roomIds = [int(l.getConfig('roomId')) for l in links]

		if self.getConfig('enableQueue') == "X":
			# todo get device Status - if cleaning, add to buffer and return to prevent overwrite!
			pass

		vac.segment_clean(roomIds)


	# required by every vacuum
	def charge(self):
		vac = self.getVac()
		vac.send("app_charge")


	# required by every vacuum
	def locate(self):
		vac = self.getVac()
		vac.find()


	def getVac(self) -> Vacuum:
		# token has to be taken from emulator, backup or similar
		return Vacuum(self.getConfig('ip'), self.getConfig('token'))


	def toggle(self):
		self.getVac().find()
