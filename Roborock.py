from core.base.model.AliceSkill import AliceSkill
from core.dialog.model.DialogSession import DialogSession
from core.util.Decorators import IntentHandler
import miio


class Roborock(AliceSkill):
	"""
	Author: philipp2310
	Description: Control your roborock vacuum
	"""
	def getVac(self, siteId = None) -> miio.Vacuum:
		ip = "192.168.0.205"
		token = '386667686138694a7937787654677938'
		return miio.Vacuum(ip, token)


	@IntentHandler('locateVac')
	def locateVac(self, session: DialogSession, **_kwargs):
		vac = self.getVac()
		try:
			vac.find()
		except Exception as e:
			self.logError(e)
			self.endDialog(session.sessionId, text=self.randomTalk('oneOfUs'))


	@IntentHandler('returnHomeVac')
	def returnHomeVac(self, session: DialogSession, **_kwargs):
		vac = self.getVac()
		try:
			vac.home()
		except Exception as e:
			self.logError(e)
			self.endDialog(session.sessionId, text=self.randomTalk('communicationError'))


	@IntentHandler('cleanVac')
	def cleanVac(self, session: DialogSession, **_kwargs):
		vac = self.getVac(session.siteId)
		try:
			vac.home()
		except Exception as e:
			self.logError(e)
			self.endDialog(session.sessionId, text=self.randomTalk('communicationError'))
