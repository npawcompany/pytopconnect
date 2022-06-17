class SUMM(object):
	result = None
	def __init__(self,data,fer=True):
		if fer:
			self.result = self.start_(data)
		else:
			self.result = self._start(data)
	def start_(self,d,a=[]):
		for i in d:
			if len(a) == len(i):
				for j in range(len(i)):
					if ((type(i[j]) is int) or (type(i[j]) is float)):
						a[j] += i[j]
					elif type(i[j]) is str:
						if i[j].isdigit():
							a[j] += int(i[j])
						else:
							a[j] = None
					else:
						a[j] = None
			else:
				for j in range(len(i)):
					if ((type(i[j]) is int) or (type(i[j]) is float)):
						a.append(i[j])
					elif type(i[j]) is str:
						if i[j].isdigit():
							a.append(int(i[j]))
						else:
							a = None
					else:
						a = None
		return a
	def _start(self,d,a=0):
		for i in d:
			if type(i) is list:
				for j in i:
					if ((type(j) is int) or (type(j) is float)):
						a += j
					elif type(j) is str:
						if j.isdigit():
							a += j
						else:
							return None
					else:
						return None
			else:
				if ((type(i) is int) or (type(i) is float)):
					a += i
				elif type(i) is str:
					if i.isdigit():
						a += i
					else:
						return None
				else:
					return None
		return a

class OP(object):
	result = None
	def __init__(self,data,fer=True):
		if fer:
			self.result = self.start_(data)
		else:
			self.result = self._start(data)
	def start_(self,d,a=[]):
		for i in d:
			if len(a) == len(i):
				for j in range(len(i)):
					if ((type(i[j]) is int) or (type(i[j]) is float)):
						a[j] *= i[j]
					elif type(i[j]) is str:
						if i[j].isdigit():
							a[j] *= int(i[j])
						else:
							a = None
					else:
						a = None
			else:
				for j in range(len(i)):
					if ((type(i[j]) is int) or (type(i[j]) is float)):
						a.append(i[j])
					elif type(i[j]) is str:
						if i[j].isdigit():
							a.append(int(i[j]))
						else:
							a[j] = None
					else:
						a[j] = None
		return a
	def _start(self,d,a=1):
		for i in d:
			if type(i) is list:
				for j in i:
					if ((type(j) is int) or (type(j) is float)):
						a *= j
					elif type(j) is str:
						if j.isdigit():
							a *= j
						else:
							return None
					else:
						return None
			else:
				if ((type(i) is int) or (type(i) is float)):
					a *= i
				elif type(i) is str:
					if i.isdigit():
						a *= i
					else:
						return None
				else:
					return None
		return a

class DIV(object):
	result = None
	def __init__(self,data,fer=True):
		if fer:
			self.result = self.start_(data)
		else:
			self.result = self._start(data)
	def start_(self,d,a=[]):
		for i in d:
			if len(a) == len(i):
				for j in range(len(i)):
					if ((type(i[j]) is int) or (type(i[j]) is float)):
						a[j] /= i[j]
					elif type(i[j]) is str:
						if i[j].isdigit():
							a[j] /= int(i[j])
						else:
							a[j] = None
					else:
						a[j] = None
			else:
				for j in range(len(i)):
					if ((type(i[j]) is int) or (type(i[j]) is float)):
						a.append(i[j])
					elif type(i[j]) is str:
						if i[j].isdigit():
							a.append(int(i[j]))
						else:
							a = None
					else:
						a = None
		return a
	def _start(self,d,a=1):
		for i in d:
			if type(i) is list:
				for j in i:
					if ((type(j) is int) or (type(j) is float)):
						a = j/a
					elif type(j) is str:
						if j.isdigit():
							a = j/a
						else:
							return None
					else:
						return None
			else:
				if ((type(i) is int) or (type(i) is float)):
					a = i/a
				elif type(i) is str:
					if i.isdigit():
						a = i/a
					else:
						return None
				else:
					return None
		return a

class SUBT(object):
	result = None
	def __init__(self,data,fer=True):
		if fer:
			self.result = self.start_(data)
		else:
			self.result = self._start(data)
	def start_(self,d,a=[]):
		for i in d:
			if len(a) == len(i):
				for j in range(len(i)):
					if ((type(i[j]) is int) or (type(i[j]) is float)):
						a[j] -= i[j]
					elif type(i[j]) is str:
						if i[j].isdigit():
							a[j] -= int(i[j])
						else:
							a[j] = None
					else:
						a[j] = None
			else:
				for j in range(len(i)):
					if ((type(i[j]) is int) or (type(i[j]) is float)):
						a.append(i[j])
					elif type(i[j]) is str:
						if i[j].isdigit():
							a.append(int(i[j]))
						else:
							a = None
					else:
						a = None
		return a
	def _start(self,d,a=None):
		n = 1
		for i in d:
			if type(i) is list:
				if a == None: a = i[0]
				for j in range(1,len(i)):
					if ((type(i[j]) is int) or (type(i[j]) is float)):
						a -= i[j]
					elif type(i[j]) is str:
						if i[j].isdigit():
							a -= i[j]
						else:
							return None
					else:
						return None
			else:
				if a == None: a = d[0]
				if ((type(d[n]) is int) or (type(d[n]) is float)):
					a -= d[n]
				elif type(d[n]) is str:
					if d[n].isdigit():
						a -= d[n]
					else:
						return None
				else:
					return None
				n += 1
		return a

class DIV_RES(object):
	result = None
	def __init__(self,data,fer=True):
		if fer:
			self.result = self.start_(data)
		else:
			self.result = self._start(data)
	def start_(self,d,a=[]):
		for i in d:
			if len(a) == len(i):
				for j in range(len(i)):
					if ((type(i[j]) is int) or (type(i[j]) is float)):
						a[j] //= i[j]
					elif type(i[j]) is str:
						if i[j].isdigit():
							a[j] //= int(i[j])
						else:
							a[j] = None
					else:
						a[j] = None
			else:
				for j in range(len(i)):
					if ((type(i[j]) is int) or (type(i[j]) is float)):
						a.append(i[j])
					elif type(i[j]) is str:
						if i[j].isdigit():
							a.append(int(i[j]))
						else:
							a = None
					else:
						a = None
		return a
	def _start(self,d,a=1):
		for i in d:
			if type(i) is list:
				for j in i:
					if ((type(j) is int) or (type(j) is float)):
						a //= j
					elif type(j) is str:
						if j.isdigit():
							a //= j
						else:
							return None
					else:
						return None
			else:
				if ((type(i) is int) or (type(i) is float)):
					a //= i
				elif type(i) is str:
					if i.isdigit():
						a //= i
					else:
						return None
				else:
					return None
		return a
class COUNT(object):
	result = None
	def __init__(self,data,fer=True):
		super(COUNT, self).__init__()
		if fer:
			self.result = self.start_(data)
		else:
			self.result = self._start(data)
	def start_(self,d):
		a=[]
		for i in d:
			if isinstance(i,(tuple,list,dict)):
				le = len(list(filter(None,i)))
				la = len(i)
				ln = la-le
				a.append([le,ln,la])
			else:
				a.append([None])
		# print(a)
		return a
	def _start(self,d):
		a=[]
		b = self.start_(d)
		# print(b)
		if len(b) > 0:
			for i in b:
				if len(a) > 0:
					a[0][0] += i[0]
					a[0][1] += i[1]
					a[0][2] += i[2]
				else:
					a.append(i)
		else:
			a = None
		return a

class END_RESULT(object):
	pass