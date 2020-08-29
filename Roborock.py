from core.base.model.AliceSkill import AliceSkill
from core.dialog.model.DialogSession import DialogSession
from core.util.Decorators import IntentHandler
from core.device.model.Device import Device
from core.device.model.Location import Location
from core.device.model.DeviceType import DeviceType
from miio import Vacuum
from core.device.model.DeviceException import DeviceNotPaired


class Roborock(AliceSkill):
	"""
	Author: philipp2310
	Description: Control your vacuum
	"""
	##todo have different deviceType abilities, e.g. wet/dry clean


	@IntentHandler('locateVac')
	def locateVac(self, session: DialogSession, **_kwargs):
		links = self.DeviceManager.getDeviceLinksForSession(session=session, skill=self.name)
		devGrouped = self.DeviceManager.groupDeviceLinksByDevice(links)

		try:
			for link in devGrouped.values():
				device = link.getDevice()
				device.getDeviceType().locate(device=device)
		except Exception as e:
			self.logError(e)
			self.endDialog(session.sessionId, text=self.randomTalk('communicationError'))


	@IntentHandler('returnHomeVac')
	def returnHomeVac(self, session: DialogSession, **_kwargs):
		links = self.DeviceManager.getDeviceLinksForSession(session=session, skill=self.name)
		devGrouped = self.DeviceManager.groupDeviceLinksByDevice(links)

		try:
			for link in devGrouped.values():
				device = link.getDevice()
				device.getDeviceType().charge(device=device)
		except Exception as e:
			self.logError(e)
			self.endDialog(session.sessionId, text=self.randomTalk('communicationError'))


	@IntentHandler('cleanVac')
	def cleanVac(self, session: DialogSession, **_kwargs):
		links = self.DeviceManager.getDeviceLinksForSession(session=session, skill=self.name)
		devGrouped = self.DeviceManager.groupDeviceLinksByDevice(links)
		# loop devices and call action per links
		for devId,linksList in devGrouped.items():

			# all vac DeviceTypes must implement a "clean" function
			try:
				device = self.DeviceManager.getDeviceById(_id=devId)
				device.getDeviceType().clean(device, linksList)
			except Exception as e:
				self.logError(e)
				self.endDialog(session.sessionId, text=self.randomTalk('communicationError'))

