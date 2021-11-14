import urllib
def parser(query):
    return urllib.parse.unquote(query)

def graf(d):
    if isinstance(d,str):
        if not (d in ['>','<','<=','>=','==','!=']):
            return "'{0}'".format(d)
    return str(d)


class rezDop(object):
    result = ""
    def __init__(self, cond,i="*"):
        if i == "*":
            if len(cond)>0:
                for i in cond:
                    if i == 'where':
                        n = len(cond[i]) - 1
                        m = len(cond[i]['option'])
                        l = 0
                        arr = []
                        for j in cond[i]:
                            pl = []
                            if j != 'option':
                                col = '`{0}` '.format(j)
                                if cond[i][j][0].upper() == 'IN':
                                    val = '{0}IN{1}'.format(col,str(tuple(cond[i][j][1:])).replace(',)',')'))
                                else:
                                    val = col
                                    if len(cond[i][j])>2:
                                        if (len(cond[i][j])-2)%3 == 0:
                                            for x in range(0,len(cond[i][j])):
                                                if (x-2)%3 == 0:
                                                    val += cond[i][j][x].upper()+' '+col
                                                else:
                                                    val += graf(cond[i][j][x])+' '
                                    elif len(cond[i][j]) == 2:
                                        val += '{0} {1}'.format(cond[i][j][0],graf(cond[i][j][1]))
                                arr.append(val)
                        if m%len(arr) != 0:
                            if m == 1:
                                t = '{0} {1} {2} '.format(arr[0],cond[i]['option'][0].upper(),arr[1])
                            elif m > 1:
                                t = ''
                                for j in range(0,m):
                                    if j == (m-1):
                                        t += '{0} {1} '.format(cond[i]['option'][j].upper(),arr[j+1])
                                    else:
                                        t += '{0} {1} {2} '.format(arr[j],cond[i]['option'][j].upper(),arr[j+1])
                            self.result += "{0} {1} ".format(i.upper(),t)
                        elif ((len(arr) == 1) and (m==0)):
                            self.result += "{0} {1} ".format(i.upper(),arr[0])
                    elif i == 'limit':
                        if len(cond[i]) == 1:
                            self.result += "{0} {1} ".format(i.upper(),cond[i][0])
                        elif len(cond[i]) >= 2:
                            self.result += "{0} {1}, {2} ".format(i.upper(),cond[i][0],cond[i][1])        
                    elif i == 'order':
                        arr = []
                        for j in cond[i]:
                            if cond[i][j]:
                                arr.append('`{0}` ASC'.format(j))
                            else:
                                arr.append('`{0}` DESC'.format(j))
                        self.result += '{0} BY {1}'.format(i.upper(),', '.join(arr))
        else:
            if len(cond)>0:
                if i == 'where':
                    n = len(cond[i]) - 1
                    m = len(cond[i]['option'])
                    l = 0
                    arr = []
                    for j in cond[i]:
                        pl = []
                        if j != 'option':
                            col = '`{0}` '.format(j)
                            if cond[i][j][0].upper() == 'IN':
                                val = '{0}IN{1}'.format(col,str(tuple(cond[i][j][1:])).replace(',)',')'))
                            else:
                                val = col
                                if len(cond[i][j])>2:
                                    if (len(cond[i][j])-2)%3 == 0:
                                        for x in range(0,len(cond[i][j])):
                                            if (x-2)%3 == 0:
                                                val += cond[i][j][x].upper()+' '+col
                                            else:
                                                val += graf(cond[i][j][x])+' '
                                elif len(cond[i][j]) == 2:
                                    val += '{0} {1}'.format(cond[i][j][0],graf(cond[i][j][1]))
                            arr.append(val)
                    if m%len(arr) != 0:
                        if m == 1:
                            t = '{0} {1} {2} '.format(arr[0],cond[i]['option'][0].upper(),arr[1])
                        elif m > 1:
                            t = ''
                            for j in range(0,m):
                                if j == (m-1):
                                    t += '{0} {1} '.format(cond[i]['option'][j].upper(),arr[j+1])
                                else:
                                    t += '{0} {1} {2} '.format(arr[j],cond[i]['option'][j].upper(),arr[j+1])
                        self.result += "{0} {1} ".format(i.upper(),t)
                    elif ((len(arr) == 1) and (m==0)):
                        self.result += "{0} {1} ".format(i.upper(),arr[0])
                elif i == 'limit':
                    if len(cond[i]) == 1:
                        self.result += "{0} {1} ".format(i.upper(),cond[i][0])
                    elif len(cond[i]) >= 2:
                        self.result += "{0} {1}, {2} ".format(i.upper(),cond[i][0],cond[i][1])        
                elif i == 'order':
                    arr = []
                    for j in cond[i]:
                        if cond[i][j]:
                            arr.append('`{0}` ASC'.format(j))
                        else:
                            arr.append('`{0}` DESC'.format(j))
                    self.result += '{0} BY {1}'.format(i.upper(),', '.join(arr))