import sqlite3

from core.base.model.Widget import Widget


class VacuumStatus(Widget):

	OPTIONS: dict = dict()

	def __init__(self, data: sqlite3.Row):
		super().__init__(data)
