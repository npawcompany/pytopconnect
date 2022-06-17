import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from accessify import protected,private
from math import ceil
from difflib import SequenceMatcher
import random
import json
import urllib.parse
import datetime, time
import types
import re
from functionResult import *

class dict_to_object:
	
	ALL_TABLES = None
	QR = None
	NAME = None
	DATANAME = None
	END_RESULT = END_RESULT
	
	def __init__(self,d=None,dn=None,qr=None,all_tables=[],x={},t=False):
		if t:
			self.setAttributes(d,dn,qr,all_tables,x)
			self.QR = qr

	def setAttributes(self,d,dn,qr,all_tables,ind):
		for a, b in d.items():
			if isinstance(b, (list, tuple)):
				setattr(self, a, [dict_to_object(x,dn,qr,all_tables,ind,t=True) if isinstance(x, dict) else x for x in b])
			else:
				setattr(self, a, dict_to_object(b,dn,qr,all_tables,ind,t=True) if isinstance(b, dict) else b)

	def startDO(self,name,d,dn,qr=None,all_tables=[],x={}):
		try:
			ob = getattr(self,name)
			ob.setAttributes(d[name],dn,qr,all_tables,x)
		except AttributeError as e:
			self.setAttributes(d,dn,qr,all_tables,x)
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
	def array_value_to_str(self,arr):
		for i in range(0,len(arr)):
			arr[i] = str(arr[i])
		return arr

			
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
				elif i == 'like':
					if len(cond[i]) == 3:
						if cond[i][0].replace(" ","") != '':
							arr = []
							for dic in result:
								res = []
								for key in cond[i][1]:
									try:
										res.append(dic.GetAttribute(key))
									except KeyError:
										pass
								res = self.array_value_to_str(res)
								if cond[i][2]:
									if all(re.search(str(wi).upper()," ".join(res).upper()) for wi in list(filter(None,cond[i][0].split(" ")))):
										arr.append(dic)
								else:
									if any(re.search(str(wi).upper()," ".join(res).upper()) for wi in list(filter(None,cond[i][0].split(" ")))):
										arr.append(dic)
							result = arr
				elif i == "search":
					if len(cond[i]) == 4:
						if cond[i][0].replace(" ","") != '':
							arr = []
							a = cond[i][0].strip().upper()
							for dic in result:
								res = []
								for key in cond[i][1]:
									try:
										res.append(dic.GetAttribute(key))
									except KeyError:
										pass
								res = self.array_value_to_str(res)
								if cond[i][2]:
									if all([SequenceMatcher(lambda x: x in [' ','\t','\n','\r'],a,b.upper()).ratio() >= (len(a)/len(a+b))+cond[i][3] for b in res]):
										arr.append(dic)
								else:
									if any([SequenceMatcher(lambda x: x in [' ','\t','\n','\r'],a,b.upper()).ratio() >= (len(a)/len(a+b))+cond[i][3] for b in res]):
										arr.append(dic)
							result = arr
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
							# print(default_function[cond[i][j][0]](array,cond[i][j][2]).result,array)
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

	def get(self,table=None,columns="*",condition=None):
		if ((self.NAME != None) and (table == None)):
			a = self
		else:
			a = self.GetAttribute(table)
		b = self.condition_grupp(a.VALUES,condition)
		if columns != "*":
			return self.condition_f(b, list(filter(None,columns.replace(" ","").replace("\t","").split(","))))
		else:
			return self.condition_f(b,a.COLUMNS)

	def get2(self,table=None,columns="*",condition=None):
		self.QR.enjoy()
		if ((self.NAME != None) and (table == None)):
			a = self
		else:
			a = self.GetAttribute(table)
		b = self.condition_grupp(a.VALUES,condition)
		if columns != "*":
			return self.condition_f(b, list(filter(None,columns.replace(" ","").replace("\t","").split(","))))
		else:
			return self.condition_f(b,a.COLUMNS)

	def add(self,values,table=None,columns='*',t=True,k=0):
		if self.NAME != None:
			table = self.NAME
		if type(table) is str:
			result = None
			if columns == '*':
				columns = self.COLUMNS
			if (isinstance(columns, (list, tuple)) and isinstance(values, (list, tuple))):
				n = len(columns)
				if t:
					if len(values) > 0:
						columns = "&".join(columns)
						result = ""
						if len(values) <= 80:
							values = self.sbor(values,n)
							result = table+"|"+columns+"=>"+values
						else:
							m = (len(values)//80)+2
							fas = []
							for i in self.parting(values,m):
								fas.append(table+"|"+columns+"=>"+self.sbor(values,n))
							result = ";".join(fas)
						# print(result)
						a = self.QR.query(result,[],"INSERT",self.INDEX)
						self.QR.enjoy()
						return a
				else:
					if len(values) == n:
						# print(columns)
						columns = "&".join(columns)
						result = ""
						arr = []
						while((len(arr) < k) and (len(values[-1]) > 0)):
							o = []
							for i in range(0,n):
								o.append(values[i][0])
								values[i].pop(0)
							arr.append(o)
						if len(arr) <= 80:
							arr = self.sbor(arr,n)
							result = table+"|"+columns+"=>"+arr
						else:
							m = (len(arr)//80)+2
							fas = []
							for i in self.parting(arr,m):
								fas.append(table+"|"+columns+"=>"+self.sbor(arr,n))
							result = ";".join(fas)
						# print(result)
						a = self.QR.query(result,[],"INSERT",self.INDEX)
						self.QR.enjoy()
						return a

	def update(self,colval,condition=[],table=None):
		if self.NAME != None:
			table = self.NAME
		if type(table) is str:
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
						fas.append(i+"->"+str(int(colval[i])))
					elif colval[i] == None:
						fas.append(i+"->"+("null"))
				result = table+"|"+",".join(fas)
				# print(result)
				a = self.QR.query(result,condition,"UPDATE",self.INDEX)
				self.QR.enjoy()
				return a

	def delet(self,table=None,condition=None):
		if self.NAME != None:
			table = self.NAME
		if type(table) is str:
			a = self.QR.query('{0};'.format(table),condition,"DELETE",self.INDEX)
			self.QR.enjoy()
			return a

	def type(self,table=None,condition=None):
		if self.NAME != None:
			table = self.NAME
		if type(table) is str:
			a = self.QR.query('{0};'.format(table),condition,"FIELDS",self.INDEX)
			self.QR.enjoy()
			return a

	def create(self,table,*columns,**par):
		if self.NAME != None:
			raise TypeError("Нельзя создать таблицу в таблице")
		try:
			self.GetAttribute(table)
			raise AttributeError("Такая таблица существует")
		except AttributeError:
			list_col = []
			key_defn = {
				"NAME":self.TS.NAME,
				"DATATYPE":self.TS.DATATYPE,
				"NULL":self.TS.NULL,
				"DEFAULT":self.TS.DEFAULT,
				"KEY":self.TS.KEY,
				"AUTO":self.TS.AUTO,
				"COMMENT":self.TS.COMMENT
			}
			def is_empty(s):
				if type(s) is str:
					if s.replace(" ","") != "":
						if not s in list_col:
							list_col.append(s)
							return True
						else:
							raise TypeError(f"Колонка '{s}' уже была добавлена")
					else:
						raise TypeError(f"Название колонки является пустой")
				return False
			def is_datatype(a):
				if isinstance(a, (list, tuple)):
					if len(a) == 2:
						if type(a[0]) is types.MethodType:
							return True
					elif len(a) == 1:
						return True if type(a[0]) is types.MethodType else False
				elif type(a) is types.MethodType:
					return True
				return False
			c = list(filter(None,[([list(key_defn.values())[i](j[i]) if i<len(j) else None for i in range(len(key_defn))] if (is_empty(j[0])) and (is_datatype(j[1])) else None) if len(j)>0 else None for j in columns if isinstance(j, (list, tuple)) ]))
			c = ",".join([ "@".join([i[j] for j in range(len(i)) if i[j] != None ]) for i in c if isinstance(i, (list, tuple))])
			c = f"{table}=>{','.join([f'{k.upper()}:{v}' for k,v in par.items() if is_empty(v)])}=>{c};"
			self.QR.query(c,[],"CREATE",self.INDEX)
			self.QR.enjoy()


	def edit(self,table=None,_type=None,*columns):
		pass