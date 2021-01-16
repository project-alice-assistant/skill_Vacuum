from core.base.model.AliceSkill import AliceSkill
from core.device.model.Device import Device
from core.device.model.DeviceException import DeviceNotPaired
from core.device.model.DeviceType import DeviceType
from core.myHome.model.Location import Location
from core.dialog.model.DialogSession import DialogSession
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
				device.getDeviceType().locate(device=device)
		except Exception as e:
			self.logError(e)
			self.endDialog(session.sessionId, text=self.randomTalk('oneOfUs'))


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
		links = self.DeviceManager.getDeviceLinksForSession(session=session, skill=self.name, noneIsEverywhere=True)
		devGrouped = self.DeviceManager.groupDeviceLinksByDevice(links)
		# loop devices and call action per links
		for devId, linksList in devGrouped.items():

			# all vac DeviceTypes must implement a "clean" function
			try:
				device = self.DeviceManager.getDeviceById(_id=devId)
				device.getDeviceType().clean(device, linksList)
			except Exception as e:
				self.logError(e)
				self.endDialog(session.sessionId, text=self.randomTalk('communicationError'))
