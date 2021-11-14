# -*- confing: utf-8 -*-
import imp
#import urllib
import sys
import os
"""
data-select="
    tabel1.col1,col2,col3;
    tabel2.*;
"
data-where="
    tabel1.col1=<val>:int;
    tabel1.col2=<val>:str;
    tabel2.col1=<val>:date;
    tabel2.col2=<val>:datetime;
    OR:0|AND:1|OR:2;
"
data-limit="
    min:int;
    max:int;
"
data-insert="
    tabel1.col1=><val>:int,col2=><val>:str,col3=><val>:date;
    tabel2.col1=><val>:int,col2=><val>:str,col3=><val>:date;
"
data-drop="
    tabel1;
    tabel2;
    tabel3;
"
data-alter="
    tabel1.col4:int(11)|NULL|ADD;
    tabel1.col1|DROP;
    tabel1.col2->col4|CHANGE;
"
data-updata="
    tabel1.col1-><val>:int;
    tabel1.col2-><val>:str;
    tabel2.col1-><val>:date;
    tabel2.col2-><val>:datetime;
"
data-delete="
    tabel1.col1;
    tabel2.col1;
"
data-showTabels=""

data-showColumns="
    tabel1;
    tabel2;
"


"""


class gt(object):
	errorMSG = []
	error = False
	

	def __init__(self, Type, con, method="SELECT", query="", req=[], num=0):
		self.sqlRes = []
		if num >= 0:
			if query != "":
				self.query = query
			self.req = req
			self.method = method.upper()
			self.rt = self.str_to_class(Type)
			if num > 0:
				self.con = con[Type][int(num) - 1]
				if self.rt != False:
					self.sqlRes = [self.rt(self.method, self.con, self.query, self.req).result()]
				else:
					self.error = True
					self.errorMSG.append("Неу(далось найти объект")
			elif num == 0:
				for i in con[Type]:
					if self.rt != False:
						self.sqlRes.append(self.rt(self.method, i, self.query,self.req).result())
					else:
						self.error = True
						self.errorMSG.append("Неудалось найти объект")
		else:
				self.error = True
				self.errorMSG.append("Данные не верные")


	def str_to_class(self, s):
		DATA_DIR = os.path.dirname(__file__) + "/queryPY/"
		if os.path.isdir(DATA_DIR):
			if os.path.isfile(DATA_DIR + s + ".py"):
				module = imp.load_source(s, DATA_DIR + s + ".py")
				return module.queryPY
		return False

