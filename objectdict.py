from accessify import protected,private
from math import ceil
import random
import json
import urllib.parse
import datetime, time
import imp
from topconnect.functionResult import *


class dict_to_object(object):
	
	ALL_TABELS = None
	QR = None
	NAME = None
	END_RESULT = END_RESULT
	
	def __init__(self, d=None, qr=None, all_tabels=[],t=False):
		if t:
			self.ALL_TABELS = all_tabels
			self.setAttributes(d,qr)
			self.QR = qr

	@private
	def setAttributes(self,d,qr):
		for a, b in d.items():
			if isinstance(b, (list, tuple)):
				setattr(self, a, [dict_to_object(x,qr,t=True) if isinstance(x, dict) else x for x in b])
			else:
				setattr(self, a, dict_to_object(b,qr,t=True) if isinstance(b, dict) else b)

	def start(self, d, qr=None, all_tabels=[]):
		self.ALL_TABELS = all_tabels
		self.setAttributes(d,qr)
		self.QR = qr

	@protected
	def condition_f(self,obj,arr):
		c = []
		j = 0
		for x in obj:
			for i in arr:
				a = self.GetAttribute(str(i),x)
				try:
					if type(c[j]) is dict:
						c[j][i] = a
					else:
						c[j].append({i:a})
				except IndexError as e:
					c.append({i:a})
			j += 1
		return self.json_gop(c)

	@protected
	def sbor(self,values,n):
		for i in range(0,len(values),1):
			if len(values[i]) == n:
				values[i] = self.parser(str(tuple(values[i])))
			elif len(values[i]) < n:
				for j in range(len(values[i]),n):
					values[i].append(None)
			elif len(values[i]) > n:
				values[i] = values[i][:n]
		return "^".join(map(str, values)).replace('None','NULL').replace('True','TRUE').replace('False','FALSE')

	@protected
	def parting(self,xs, parts):
		part_len = ceil(len(xs)/parts)
		return [xs[part_len*k:part_len*(k+1)] for k in range(parts)]

	@protected
	def parser(self,query):
		return urllib.parse.quote(query)
	
	@protected
	def sdf(self,a,b):
		if type(b) is str:
			b = "'" + str(b) + "'"
		elif isinstance(b,(datetime.datetime,datetime.date)):
			b = str(time.mktime(b.timetuple()))
		else:
			b = str(b)
		c = a
		n = len(c)
		if c[0].upper() != 'IN':
			if n > 3:
				t = str(b)
				if ((n-2)%3 == 0):
					for i in c:
						if ((type(i) is str) and not (i in ['>','<','<=','>=','==','!=','and','or','in'])):
							if i.isdigit():
								j = str(i)
							else:
								j = '\'' + str(i) + '\''
						elif isinstance(i,(datetime.datetime,datetime.date)):
							j = str(time.mktime(i.timetuple()))
						else:
							j = str(i)
						if j.upper() in ['AND','OR']:
							t += ' '+j+' '+str(b)
						else:
							t+= ' '+j
					return eval(t)
				else:
					print('Не правильные условия')
					return False
			else:
				if type(c[1]) is str:
					if c[1].isdigit():
						a = str(c[1])
					else:
						a = " '"+str(c[1])+"' "
				elif isinstance(c[1],(datetime.datetime,datetime.date)):
					a = str(time.mktime(c[1].timetuple()))
				else:
					a = str(c[1])
				# print(str(b)+' '+c[0]+a)
				return eval(str(b)+' '+c[0]+a)
		else:
			return eval(b+' in '+str(tuple(c[1:])))
	
	@protected
	def nik(self,a,b,u):
		arr = []
		if len(a) == len(b):
			for i in range(0,len(a)):
				# print(str(a[i])+' '+u+' '+str(b[i]))
				arr.append(eval(str(a[i])+' '+u+' '+str(b[i])))
		return arr
	
	@protected
	def tre(self,a,b):
		dp = []
		i = 0
		t = False
		for j in range(0,len(a)-1):
			if ((len(dp) > 0) or (t)):
				dp = self.nik(dp,a[(2*j)-i],b[j-i])
				i += 1
			else:
				dp = self.nik(a[2*j],a[(j*2)+1],b[j])
				if len(dp) >= 0: t = True
		if len(dp) > 0:
			return dp
		else:
			return a[0]

			
	@protected
	def condition_grupp(self,obj,cond):
		gy = []
		result = []
		if cond != None:
			for i in cond:
				if i == 'where':
					n = len(cond[i]) - 1
					m = len(cond[i]['option'])
					l = 0
					for j in cond[i]:
						if j != 'option':
							arr = []
							for x in obj:
								a = self.GetAttribute(j,x)
								arr.append(self.sdf(cond[i][j],a))
							if ((n >= 1) and (m >= 0)):
								gy.append(arr)
					if len(gy) > 0:
						g = self.tre(gy,cond[i]['option'])
						if len(g) == len(obj):
							result = []
							for j in range(0,len(g)):
								if g[j]:
									result.append(obj[j])
				elif i == 'limit':
					if len(cond[i]) == 1:
						result = result[cond[i][0]:]
					elif len(cond[i]) >= 2:
						result = result[cond[i][0]:cond[i][1]]
				elif i == 'order':
					for j in cond[i]:
						sort = cond[i][j]
						result = sorted(result, key=lambda y: getattr(y,j),reverse=sort)
				elif i == 'random':
					res_rand = []
					# print(result)
					if len(result) > 0:
						random.shuffle(result)
						if len(cond[i]) == 1:
							if cond[i][0] >= 0:
								if len(result) >= cond[i][0]:
									while len(res_rand) != cond[i][0]:
										res_rand.append(result.pop())
									result = res_rand
						elif len(cond[i]) == 2:
							if cond[i][0] < cond[i][1]:
								if (cond[i][0]+cond[i][1]) > 2:
									kn = random.randint(cond[i][0],cond[i][1])
									if len(result) >= kn:
										while len(res_rand) != kn:
											res_rand.append(result.pop())
										result = res_rand
				elif i == 'result':
					default_function = {
						"SUMM":SUMM,
						"OP":OP,
						"DIV":DIV,
						"SUBT":SUBT,
						"DIV_RES":DIV_RES,
						"COUNT":COUNT
					}
					# ["SUMM","OP","DIV","SUBT","DIV_RES","MOD","DEG","RADICAL"]
					for j in cond[i]:
						is_func = lambda x: True if x.upper() in list(default_function.keys()) else False
						if is_func(cond[i][j][0]):
							if len(result) > 0:
								array = []
								for y in range(len(cond[i][j][1])):
									arr = []
									for x in result:
										try:
											arr.append(x.GetAttribute(cond[i][j][1][y]))
										except AttributeError as e:
											if cond[i][j][1][y] in list(self.END_RESULT.__dict__.keys()):
												t = getattr(self.END_RESULT,cond[i][j][1][y])
												if type(t) is list:
													arr = t
												else:
													arr.append(t)
												break
											else:
												raise AttributeError("Атрибут не найден")
									array.append(arr)
								# print(self.END_RESULT.__dict__.keys(),j)
							else:
								array = result
							# print(default_function[cond[i][j][0]](array,cond[i][j][2]).result)
							if j in list(self.END_RESULT.__dict__.keys()):
								delattr(self.END_RESULT, j)
								setattr(self.END_RESULT, j, default_function[cond[i][j][0]](array,cond[i][j][2]).result)
							else:
								setattr(self.END_RESULT, j, default_function[cond[i][j][0]](array,cond[i][j][2]).result)

		else:
			return obj
		return result

	@protected
	def json_gop(self,arr):
		b = []
		for j in range(len(arr)):
			a = {}
			for i in arr[j]:
				try:
					if type(arr[j][i]) is str: a[i] = json.loads(arr[j][i])
					else: a[i] = arr[j][i]
				except BaseException as e:
					a[i] = arr[j][i]
			b.append(a)
		return b

	@protected
	def con_opt(self,c):
		pass
		
	def GetAttribute(self,attr,obj=None,k=True):
		if k:
			if obj == None: obj = self
		else:
			return obj
		if len(attr)  > 0:
			if type(attr) is str:
				attr = list(filter(None,attr.split('.')))
			try:
				return self.GetAttribute(attr[1:],getattr(obj,str(attr[0])),k=False)
			except AttributeError as e:
				# print("Элемент, \"{0}\", не существует\nОшибка:\"{1}\"".format(str(attr[0]),e),obj.help())
				raise e
		else:
			return obj
	
	def help(self):
		return self.__dict__

	def get(self,tabel=None,columns="*",condition=None):
		if ((self.NAME != None) and (tabel == None)):
			a = self
		else:
			a = self.GetAttribute(tabel)
		b = self.condition_grupp(a.VALUES,condition)
		if columns != "*":
			return self.condition_f(b, list(filter(None,columns.replace(" ","").replace("\t","").split(","))))
		else:
			return self.condition_f(b,a.COLUMNS)

	def add(self,values,tabel=None,columns='*'):
		if self.NAME != None:
			tabel = self.NAME
		if type(tabel) is str:
			result = None
			if columns == '*':
				columns = self.COLUMNS
			if (isinstance(columns, (list, tuple)) and isinstance(values, (list, tuple))):
				n = len(columns)
				if len(values) > 0:
					columns = "&".join(columns)
					result = ""
					if len(values) <= 80:
						values = self.sbor(values,n)
						result = tabel+"|"+columns+"=>"+values
					else:
						m = (len(values)//80)+2
						fas = []
						for i in self.parting(values,m):
							fas.append(tabel+"|"+columns+"=>"+self.sbor(values,n))
						result = ";".join(fas)
					# print(result)
					a = self.QR.query(result,[],"INSERT")
					self.QR.enjoy()
					return a

	def update(self,colval,condition=[],tabel=None):
		if self.NAME != None:
			tabel = self.NAME
		if type(tabel) is str:
			result = None
			fas = []
			if len(condition) > 0:
				self.con_opt(condition)
			if len(colval) > 0:
				for i in colval:
					if type(colval[i]) is str:
						fas.append(i+"->"+self.parser(colval[i]))
					elif type(colval[i]) is int:
						fas.append(i+"->"+(str(colval[i])))
					elif type(colval[i]) is float:
						fas.append(i+"->"+(str(colval[i])))
					elif type(colval[i]) is bool:
						fas.append(i+"->"+(str(colval[i])))
					elif colval[i] == None:
						fas.append(i+"->"+("NULL"))
				result = tabel+"|"+",".join(fas)
				# print(result)
				a = self.QR.query(result,condition,"UPDATE")
				self.QR.enjoy()
				return a

	def delet(self,tabel=None,condition=None):
		if self.NAME != None:
			tabel = self.NAME
		if type(tabel) is str:
			a = self.QR.query('{0};'.format(tabel),condition,"DELETE")
			self.QR.enjoy()
			return a