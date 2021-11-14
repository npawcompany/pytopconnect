import pymysql
from topconnect.drop import *

class queryPY(object):
    errorMSG = []
    error = False
    try:
        def __init__(self,method,con,query="",req=[]):
            self.conn = self.connect(con)
            self.cursor = self.conn.cursor()
            self.res = self.functinon_list(method)(self.cursor,self.conn,query,req)
            self.conn.close()
        def result(self):
            return self.res
        def functinon_list(self,m):
            MET_FUNC = {
                "SELECT":self.selection_f,
                "INSERT":self.insert_f,
                "UPDATE":self.update_f,
                "DELETE":self.delete_f,
                "SHOW_TABEL":self.show_tabel_f,
                "SHOW_COLUMNS":self.show_coll_f
            }
            return MET_FUNC[m]
        def connect(self,a):
            self.DB_NAME = a["database"]
            # host port user passwd database
            return pymysql.connect(**a)
        def selection_f(self,cursor,con,q,r):
            ex = list(filter(None, q.split(";")))
            select = "SELECT "
            fromSel = " FROM "
            for i in ex:
                a = list(filter(None, i.split("|")))
                tabel = a[0]
                coll = a[1]
                if(coll != "*"):
                    der = list(filter(None, coll.split(",")))
                    c = ""
                    if(type(der) is list):
                        for j in der:
                            c += "`"+tabel+"`.`"+j+"`,"
                        select += c[0:-1] + ","
                    elif(type(der) is str):
                        select += "`"+tabel+"`.`"+der+"`, "
                else:
                    select += "`"+tabel+"`."+coll+","
                fromSel += "`"+tabel+"`,"

            select = select[0:-1] + fromSel[0:-1] + rezDop(r).result
            cursor.execute(select)
            result = cursor.fetchall()
            return result
        def insert_f(self,cursor,con,q,r):
            ex = list(filter(None, q.split(";")))
            arr = []
            innsert = ""
            for i in ex:
                a = list(filter(None, i.split("|")))
                tabel = a[0]
                colval = a[1]
                innsert += "INSERT INTO `"+tabel+"` "
                b = list(filter(None, colval.split("=>")))
                col = str(tuple(filter(None, b[0].split("&"))))
                val = list(filter(None, b[1].split("^")))
                for j in range(0, len(val),1):
                    val[j] = parser(val[j])
                innsert += col.replace("'","`")+" VALUES "+",".join(val)+";"
            # print(innsert)
            if innsert != "":
                try:
                    cursor.execute(innsert)
                    con.commit()
                    return True
                except pymysql.InternalError as e:
                    print(e)
            return False
        def update_f(self,cursor,con,q,r):
            ex = list(filter(None, q.split(";")))
            tab = ""
            col = ""
            for i in ex:
                v = list(filter(None, i.split("|")))
                tabel = v[0]
                coll = v[1]
                tab += "`"+tabel+"`,"
                co,val = list(filter(None, coll.split("->")))
                val = parser(val)
                if(val.isdigit()):
                    col += "`"+co+"` = "+str(val)+","
                else:
                    col += "`"+co+"` = '"+str(val)+"',"
            update = "UPDATE " + tab[0:-1] + " SET " + col[0:-1] + ' '  + rezDop(r,"where").result
            cursor.execute(update.replace("==","="))
            con.commit()
            return True
        def delete_f(self,cursor,con,q,r):
            ex = list(filter(None, q.split(";")))
            delete = "DELETE FROM "
            for i in ex:
                delete += "`"+i+"` ,"
            delete = delete[0:-1] + rezDop(r,"where").result
            cursor.execute(delete)
            con.commit()
            return True
        def show_tabel_f(self,cursor,con,q,r):
            show = "SHOW TABLES FROM `"+self.DB_NAME+"`"
            cursor.execute(show)
            res = cursor.fetchall()
            data = []
            for i in res:
                cursor.execute("SELECT COUNT(1) FROM `{0}`.`{1}`;".format(self.DB_NAME,i[0]))
                data.append((i[0],cursor.fetchall()[0][0]))
            return tuple(data)
        def show_coll_f(self,cursor,con,q,r):
            ex = list(filter(None, q.split(";")))
            names = None
            for i in ex:
                show = "SELECT * FROM `"+str(i)+"`"
                cursor.execute(show)
                names = tuple(description[0] for description in cursor.description)
            return names
    except BaseException as e:
        self.error = True
        self.errorMSG.append(e)