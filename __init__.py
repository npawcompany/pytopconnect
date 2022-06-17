import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from connect import gt
from objectdict import dict_to_object as do
from typesql import *
import datetime
import time
from accessify import protected

class QueryRead(do):

	ERROR_DEBUG = False
	ERROR_MSG = []
	FOCUS = ""
	REQ = []
	APPLICATION = "SELECT"
	RESULT = None

	def __init__(self, method, data, number=0):
		super(QueryRead, self).__init__()
		self.METHOD = method
		self.DATA = data
		self.NUMBER = int(number)
		self.TS = TS(method)
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
			if not self.GO_SQL_CON.error:
				self.DB_NAME = self.GO_SQL_CON.DB_NAME
				self.TIME_OUT = time.time() - TIME_START
				return self.GO_SQL_CON.sqlRes
			else:
				for e in self.GO_SQL_CON.errorMSG:
					raise BaseException(e)
		except BaseException as e:
			self.error_debug(e)
			raise e

	def query(self,focus, req=[], application="SELECT",num=0):
		self.APPLICATION = application
		self.FOCUS = focus
		self.REQ = req
		self.NUMBER = num
		return self.start()

	@protected
	def all_values(self,focus,num=0):
		self.APPLICATION = "SELECT"
		self.FOCUS = focus+"|*"
		self.NUMBER = num
		return self.start()

	@protected
	def all_columns(self,focus,num=0):
		self.APPLICATION = "SHOW_COLUMNS"
		self.FOCUS = focus
		self.NUMBER = num
		# print(focus)
		return self.start()

	@protected
	def fields(self,focus,num=0):
		self.APPLICATION = "FIELDS"
		self.FOCUS = focus
		self.NUMBER = num
		# print(focus)
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

	@protected
	def valid(self,k):
		n = ["database","dbFile"]
		i = 0
		key = None
		while len(n) > i:
			try:
				if n[i] == "dbFile":
					key = "_".join(k[n[i]].split("/")[-2:]).split(".")[0]
				elif n[i] == "database":
					key = k["database"]
				if key:
					return key
				else:
					i += 1
			except KeyError:
				i += 1

	def enjoy(self):
		fr = {}
		name = self.DATA[self.METHOD]
		a = self.query("1",[],"SHOW_TABEL")
		if a != None:
			if len(a) > 0:
				for x in range(0,len(name)):
					result = {
						"INDEX":x+1,
						"TS":self.TS
					}
					arr = []
					kol = self.valid(name[x])
					if kol:
						# print(a[kol])
						for j in range(0,len(a[kol])):
							for i in a[kol][j]:
								c = self.all_columns(i[0],x+1)[kol]
								v = self.all_values(i[0],x+1)[kol]
								val = self.values_res(v,c)
								fet = self.fetchall_res(v,c)
								result[i[0]] = {
									"LENGTH":i[1] if len(i) > 1 else len(val),
									"TYPE":self.fields(i[0],x+1)[kol][0],
									"COLUMNS":list(c[0]),
									"VALUES": val,
									"FETCHALL":fet,
									"NAME":i[0],
									"INDEX":x+1,
									"DATANAME":self.METHOD
								}
								arr.append(i[0])
							result["ALL_TABLES"] = arr
							fr[kol] = result
						# print(fr)
						self.startDO(kol,fr,self.METHOD,self,arr)

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
