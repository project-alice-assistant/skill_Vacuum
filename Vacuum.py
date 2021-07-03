#  Copyright (c) 2021
#
#  This file, Vacuum.py, is part of Project Alice.
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
#  Last modified: 2021.04.15 at 00:35:02 MESZ

from core.base.model.AliceSkill import AliceSkill
from core.device.model.Device import Device
from core.device.model.DeviceException import DeviceNotPaired
from core.device.model.DeviceType import DeviceType
from core.dialog.model.DialogSession import DialogSession
from core.myHome.model.Location import Location
from core.util.Decorators import IntentHandler


class Vacuum(AliceSkill):
	"""
	Author: philipp2310
	Description: Control your vacuum
	"""

	##todo have different deviceType abilities, e.g. wet/dry clean
	##todo distinct between "clean here" and "clean everywhere"
	##todo allow friendly deviceNames for cleaning, "send robo to the kitchen" or "let rob clean the bathroom"

	@IntentHandler('locateVac')
	def locateVac(self, session: DialogSession, **_kwargs):
		links = self.DeviceManager.getDeviceLinksForSession(session=session, skill=self.name)
		devGrouped = self.DeviceManager.groupDeviceLinksByDevice(links)

		try:
			for link in devGrouped.values():
				device = link.getDevice()
				device.locate()
		except Exception as e:
			self.logError(e)
			self.endDialog(session.sessionId, text=self.randomTalk('oneOfUs'))


	@IntentHandler('returnHomeVac')
	def returnHomeVac(self, session: DialogSession, **_kwargs):
		links = self.DeviceManager.getDeviceLinksForSession(session=session, skill=self.name)
		devGrouped = self.DeviceManager.groupDeviceLinksByDevice(links)

		try:
			for link in devGrouped.values():
				link.device.charge()
		except Exception as e:
			self.logError(e)
			self.endDialog(session.sessionId, text=self.randomTalk('communicationError'))


	@IntentHandler('cleanVac')
	def cleanVac(self, session: DialogSession, **_kwargs):
		links = self.DeviceManager.getDeviceLinksForSession(session=session, skill=self.name, noneIsEverywhere=True)
		self.logDebug(f'got these links to work with: {links}')
		devGrouped = self.DeviceManager.groupDeviceLinksByDevice(links)
		self.logDebug(f'grouped them to {devGrouped}')
		cleaned = 0
		failed = 0

		# loop devices and call action per links
		for devId, linksList in devGrouped.items():

			# all vac DeviceTypes must implement a "clean" function
			try:
				device = self.DeviceManager.getDevice(deviceId=devId)
				device.clean(linksList)
				cleaned = cleaned + 1
			except Exception as e:
				self.logError(e)
				self.endDialog(session.sessionId, text=self.randomTalk('communicationError'))
				failed = failed + 1

		if cleaned == 0 and failed == 0:
			self.endDialog(session.sessionId, text=self.randomTalk('dontknowhow'))
		elif failed == 0:
			return self.endDialog(session.sessionId, text=self.randomTalk('success'))
		else:
			return self.endDialog(session.sessionId, text=self.randomTalk('partiallyFailed'))
