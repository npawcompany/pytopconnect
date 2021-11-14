from topconnect.connect import gt
from topconnect.objectdict import dict_to_object as do
import datetime
import time
from accessify import protected



VERSION = (1,1,1,'AAA',False)
AUTCHER = {
	'name':'Gor',
	'surname':'Apinyan',
	'company':'PAW©',
	'date_create':'2021-04-14 09:44',
	'title':'Paw Project',
	'programming_language':'Python v. +3.x'
}

class QueryRead(object):

	ERROR_DEBUG = False
	ERROR_MSG = []
	FOCUS = ""
	REQ = []
	APPLICATION = "SELECT"
	RESULT = None
	DATA_BASE_TABELS = None
	DO = do()

	def __init__(self, method, data, number=0):
		super(QueryRead, self).__init__()
		self.METHOD = method
		self.DATA = data
		self.NUMBER = int(number)
		self.enjoy()

	@protected
	def start(self):
		try:
			TIME_START = time.time()
			self.DATA_TIME_START = datetime.datetime.now()
			self.GO_SQL_CON = gt(
				self.METHOD,
				self.DATA,
				self.APPLICATION,
				self.FOCUS,
				self.REQ,
				self.NUMBER
			)
			self.TIME_OUT = time.time() - TIME_START
			return self.GO_SQL_CON.sqlRes
		except BaseException as e:
			self.error_debug(e)
			raise e

	def query(self,focus, req=[], application="SELECT"):
		self.APPLICATION = application
		self.FOCUS = focus
		self.REQ = req
		return self.start()

	@protected
	def all_values(self,focus):
		self.APPLICATION = "SELECT"
		self.FOCUS = focus+"|*"
		return self.start()

	@protected
	def all_columns(self,focus):
		self.APPLICATION = "SHOW_COLUMNS"
		self.FOCUS = focus
		return self.start()

	@protected
	def values_res(self,v,c):
		values = []
		for j in v:
			for x in range(0,len(j)):
				val = {}
				for y in range(0,len(j[x])):
					val[c[0][y]] = j[x][y]
				values.append(val)
		return values

	@protected
	def fetchall_res(self,v,c):
		values = {}
		for j in c[0]:
			index = c[0].index(j)
			values[j] = []
			for x in v[0]:
				values[j].append(x[index])
		return values

	def enjoy(self):
		result = {}
		arr = []
		fr = {"db":[]}
		a = self.query("1",[],"SHOW_TABEL")
		if a != None:
			if len(a) > 0:
				for j in range(0,len(a)):
					for i in a[j]:
						c = self.all_columns(i[0])
						v = self.all_values(i[0])
						result[i[0]] = {
							"LENGTH":i[1],
							"COLUMNS":list(c[0]),
							"VALUES":self.values_res(v,c),
							"FETCHALL":self.fetchall_res(v,c),
							"NAME":i[0]
						}
						arr.append(i[0])
					fr['db'].append(result)
		self.DO.start(fr,self,arr)
		self.DATA_BASE_TABELS = self.DO

	def reset(self):
		self.ERROR_DEBUG = False
		self.ERROR_MSG = []
		self.APPLICATION = "SELECT"
		self.FOCUS = ""
		self.REQ = []
		self.RESULT = None

	@protected
	def error_debug(self,e):
		self.ERROR_DEBUG = True
		self.ERROR_MSG.append(e)
		print(self.ERROR_MSG)
