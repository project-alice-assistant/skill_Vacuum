from core.device.model.Device import Device
from core.device.model.Location import Location
from core.device.model.DeviceType import DeviceType
from core.commons import constants
import sqlite3
import threading
import socket
from core.base.model.ProjectAliceObject import ProjectAliceObject
from core.dialog.model.DialogSession import DialogSession
from core.device.model.DeviceException import requiresGuiSettings
import miio


class device_roborock(DeviceType):

	DEV_SETTINGS = { 'ip': '',
					 'token': '' }
	LOC_SETTINGS = { 'roomId': '' }

	def __init__(self, data: sqlite3.Row):
		super().__init__(data, devSettings=self.DEV_SETTINGS, locSettings=self.LOC_SETTINGS, heartbeatRate=0)


	def discover(self, device: Device, uid: str, replyOnSiteId: str = "", session:DialogSession = None) -> bool:
		ip = device.getCustomValue('ip')
		token = device.getCustomValue('token')
		# check device settings for ip and token -> end dialog: Please supply informaition via interface
		if not ip or not token:
			raise requiresGuiSettings()

		# check settings by sending a command(Hello?)
		# connected? save token as uid
		device.pairingDone(uid=token)
		return


	def getDeviceIcon(self, device: Device) -> str:
		#todo figure out a concept getting the current state of he vac
		return 'device_roborock.png'


	def getDeviceConfig(self):
		# return the custom configuration of that deviceType
		pass


	def toggle(self, device: Device):
		# todo trigger complete clean/send to station
		pass
