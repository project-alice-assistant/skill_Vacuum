from core.base.model.AliceSkill import AliceSkill
from core.dialog.model.DialogSession import DialogSession
from core.util.Decorators import IntentHandler
from core.device.model.Device import Device
from core.device.model.Location import Location
from core.device.model.DeviceType import DeviceType
import miio


class Roborock(AliceSkill):
	"""
	Author: philipp2310
	Description: Control your roborock vacuum
	"""
	def getVac(self, siteId:str = None, device:Device = None) -> miio.Vacuum:
		if not device:
			if siteId:
				device = self.DeviceManager.getDevicesByLocation(locationID=self.LocationManager.getLocation(siteId=siteId))

		ip = device.getCustomValue('ip')
		token = device.getCustomValue('token')
		ip = "192.168.0.205"
		# token has to be taken from emulator or similar
		token = '386667686138694a7937787654677938'
		return miio.Vacuum(ip, token)


	@IntentHandler('locateVac')
	def locateVac(self, session: DialogSession, **_kwargs):
		vac = self.getVac(siteId=session.siteId)
		try:
			vac.find()
		except Exception as e:
			self.logError(e)
			self.endDialog(session.sessionId, text=self.randomTalk('oneOfUs'))


	@IntentHandler('returnHomeVac')
	def returnHomeVac(self, session: DialogSession, **_kwargs):
		vac = self.getVac(siteId=session.siteId)
		try:
			vac.send("app_charge")
		except Exception as e:
			self.logError(e)
			self.endDialog(session.sessionId, text=self.randomTalk('communicationError'))


	@IntentHandler('cleanVac')
	def cleanVac(self, session: DialogSession, **_kwargs):
		self.logInfo("was asked to clean from " + session.siteId)
		vac = self.getVac(session.siteId)
		try:
			items = [self.getIdForRoom(x.value['value']) for x in session.slotsAsObjects.get('Room', list())]
			if items:
				vac.segment_clean(s(items))
			else:
				self.logInfo("clean everything")
				vac.start()
		except Exception as e:
			self.logError(e)
			self.endDialog(session.sessionId, text=self.randomTalk('communicationError'))

	def getIdForRoom(self, name:str):
		self.DeviceManager.getDevicesByLocation(deviceTypeID=self.DeviceManager.getDeviceTypeByName('device_roborock'))
