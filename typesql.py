from accessify import protected,private
from datetime import *
import urllib.parse
import types

class TS(object):

	def __init__(self,dn):
		self.DATANAME = dn

	@private
	def parser(self,query):
		return urllib.parse.quote(query)

	# Строки запроса

	def NAME(self,x):
		if type(x) is str:
			return f"n|{x}"

	def DATATYPE(self,x):
		if isinstance(x, (list, tuple)):
			if len(x) == 2:
				if type(x[0]) is types.MethodType:
					if isinstance(x[1], (list, tuple)):
						return f"dt|{x[0](*x[1])}"
					else:
						return f"dt|{x[0](x[1])}"
			elif len(x) == 1:
				return f"dt|{x[0]()}" if type(x[0]) is types.MethodType else None
		elif type(x) is types.MethodType:
			return f"dt|{x()}"

	def NULL(self,x):
		if type(x) is bool:
			return f"nu|{'NULL' if x else self.parser('NOT NULL')}"

	def DEFAULT(self,x):
		if type(x) is str:
			return f"de|'{x}'"
		elif type(x) is bool:
			return f"de|{int(x)}"
		elif isinstance(x,(int,float)):
			return f"de|{x}"
		elif isinstance(x,(list,tuple,dict)):
			return f"de|{str(x)}"
		elif isinstance(x,(datetime,date)):
			return f"de|'{str(x)}'"

	def KEY(self,x):
		key = {
			"PR":"PRIMARY KEY",
			"UN":"UNIQUE"
		}
		if type(x) is str:
			if x.upper() in list(key.keys()):
				return f"k|{key[x.upper()]}"
		elif type(x) is int:
			try:
				return f"k|{list(key.values())[x.upper()]}"
			except Exception as e:
				pass

	def AUTO(self,x):
		if type(x) is bool:
			if self.DATANAME.lower() in ['sqlite']:
				return "au|AUTOINCREMENT" if x else None
			elif self.DATANAME.lower() in ['mysql']:
				return "au|AUTO_INCREMENT" if x else None

	def COMMENT(self,x):
		if type(x) is str:
			return f"co|'{self.parser(x)}'"
		elif type(x) is bool:
			return f"co|{int(x)}"
		elif isinstance(x,(int,float)):
			return f"co|{x}"
		elif isinstance(x,(list,tuple,dict)):
			return f"co|{self.parser(str(x))}"
		elif isinstance(x,(datetime,date)):
			return f"co|'{self.parser(str(x))}'"

	# Логические данные

	def BOOL(self):
		if self.DATANAME.lower() in ['mysql']:
			return 'TINYINT(1)'
		elif self.DATANAME.lower() in ['sqlite']:
			return 'BOOLEAN'

	# Числовые данные

	def INTEGER(self,x=11):
		if self.DATANAME.lower() in ['sqlite']:
			return ('INTEGER({})'.format(x) if x>-2147483648 and x <2147483648 else None) if x != None else 'INTEGER'

	def INT(self,x=11):
		if self.DATANAME.lower() in ['mysql','sqlite']:
			return ('INT({})'.format(x) if x>-2147483648 and x <2147483648 else None) if x != None else 'INT'

	def TINYINT(self,x=11):
		if self.DATANAME.lower() in ['mysql']:
			return ('TINYINT({})'.format(x) if x>-128 and x <128 else None) if x != None else 'TINYINT'

	def SMALLINT(self,x=11):
		if self.DATANAME.lower() in ['mysql']:
			return ('SMALLINT({})'.format(x) if x>-32768 and x <32768 else None) if x != None else 'SMALLINT'

	def BIGINT(self,x=11):
		if self.DATANAME.lower() in ['mysql','sqlite']:
			return ('BIGINT({})'.format(x) if x>-9223372036854775808 and x <9223372036854775808 else None) if x != None else 'BIGINT'

	def MEDIUMINT(self,x=11):
		if self.DATANAME.lower() in ['mysql']:
			return ('MEDIUMINT({})'.format(x) if x>-32768 and x <32768 else None) if x != None else 'MEDIUMINT'

	def FLOAT(self,x=11,d=11):
		if self.DATANAME.lower() in ['mysql']:
			return ('FLOAT({})'.format(x) if x>-1.175494351*(10**(-39)) and x <1.175494351*(10**(-39)) else None) if x != None else 'FLOAT'
		elif self.DATANAME.lower() in ['sqlite']:
			return ('REAL({})'.format(x) if x>-1.175494351*(10**(-39)) and x <1.175494351*(10**(-39)) else None) if x != None else 'REAL'

	def DOUBLE(self,x=11,d=2):
		if self.DATANAME.lower() in ['mysql','sqlite']:
			return ('DOUBLE({})'.format(x) if x>-2.2250738585072015*(10**(-308)) and x <2.2250738585072015*(10**(-308)) else None) if x != None else 'DOUBLE'

	def DECIMAL(self,x=11,d=2):
		if self.DATANAME.lower() in ['mysql','sqlite']:
			return ('DECIMAL({})'.format(x) if x>-99.99 and x <99.99 else None) if x != None else 'DECIMAL'

	# Текстовые данные

	def STRING(self,n=None):
		if self.DATANAME.lower() in ['sqlite']:
			return ('STRING({})'.format(n)) if n != None else 'STRING'

	def TEXT(self):
		if self.DATANAME.lower() in ['mysql','sqlite']:
			return 'TEXT'

	def TINYTEXT(self):
		if self.DATANAME.lower() in ['mysql']:
			return 'TINYTEXT'

	def BLOB(self):
		if self.DATANAME.lower() in ['mysql','sqlite']:
			return 'BLOB'

	def MEDIUMTEXT(self):
		if self.DATANAME.lower() in ['mysql']:
			return 'MEDIUMTEXT'

	def MEDIUMBLOB(self):
		if self.DATANAME.lower() in ['mysql']:
			return 'MEDIUMBLOB'

	def LONGTEXT(self):
		if self.DATANAME.lower() in ['mysql']:
			return 'MEDIUMTEXT'

	def LONGBLOB(self):
		if self.DATANAME.lower() in ['mysql']:
			return 'MEDIUMBLOB'

	def CHAR(self,n):
		if self.DATANAME.lower() in ['mysql','sqlite']:
			return 'CHAR({})'.format(n) if type(n) is int else None

	def VARCHAR(self,n):
		if self.DATANAME.lower() in ['mysql','sqlite']:
			return 'VARCHAR({})'.format(n) if type(n) is int else None

	# Временые данные

	def DATE(self):
		if self.DATANAME.lower() in ['mysql','sqlite']:
			return 'DATE()'

	def TIME(self):
		if self.DATANAME.lower() in ['mysql','sqlite']:
			return 'TIME()'

	def DATETIME(self):
		if self.DATANAME.lower() in ['mysql','sqlite']:
			return 'DATETIME()'

	def TIMESTAMP(self):
		if self.DATANAME.lower() in ['mysql']:
			return 'TIMESTAMP()'

	def YEAR(self):
		if self.DATANAME.lower() in ['mysql']:
			return 'YEAR()'
