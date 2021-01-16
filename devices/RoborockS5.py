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
from miio import Vacuum
from typing import Dict, List, Union


class RoborockS5(Device):

	@classmethod
	def getDeviceTypeDefinition(cls) -> dict:
		return {
			'deviceTypeName'    : 'RoborockS5',
			'perLocationLimit'  : 0,
			'totalDeviceLimit'  : 0,
			'allowLocationLinks': True,
			'allowHeartbeatOverride': False,
			'heartbeatRate'     : 0,
			'deviceSettings'    : { 'ip': '',
					                'token': ''},
			'linkSettings'      : { 'roomId': '' },
			'abilities'         : [DeviceAbility.NONE]
		}

	def __init__(self, data: Union[sqlite3.Row, Dict]):
		super().__init__(data)


	def discover(self, device: Device, uid: str, replyOnSiteId: str = "", session:DialogSession = None) -> bool:
		self.logInfo(f'searching for a roborock')
		if not 'ip' in device.devSettings or not 'token' in device.devSettings:
			device.changedDevSettingsStructure(self.DEV_SETTINGS)
		ip = device.devSettings['ip']
		token = device.devSettings['token']

		# check device settings for ip and token -> end dialog: Please supply informaition via interface
		if not ip or not token:
			raise RequiresGuiSettings()

		# check settings by sending a command(Hello?)
		vac = self.getVac(device=device)
		serial = vac.serial_number()
		vac.find()
		# connected?
		device.pairingDone(uid=serial)
		return True


	#required by every vacuum
	def clean(self, device: Device, links: List[DeviceLink]):
		if not isinstance(links, List): links = [links]

		vac = self.getVac(device=device)
		roomIds = [int(l.locSettings['roomId']) for l in links]

		if device.devSettings['enableQueue'] == "X":
			#todo get device Status - if cleaning, add to buffer and return to prevent overwrite!
			pass

		vac.segment_clean(roomIds)

	#required by every vacuum
	def charge(self, device: Device):
		vac = self.getVac(device=device)
		vac.send("app_charge")


	#required by every vacuum
	def locate(self, device: Device):
		vac = self.getVac(device=device)
		vac.find()


	def getVac(self, device:Device) -> Vacuum:
		# token has to be taken from emulator, backup or similar
		return Vacuum(device.devSettings['ip'], device.devSettings['token'])


	def toggle(self, device: Device):
		self.getVac(device=device).find()
