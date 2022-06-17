import sqlite3
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from drop import *

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
                "SHOW_COLUMNS":self.show_coll_f,
                "FIELDS":self.show_field_f,
                "CREATE":self.create_f,
                "ALERT":self.alter_f
            }
            return MET_FUNC[m]
        def connect(self,a):
            self.DB_NAME = "_".join(a["dbFile"].split("/")[-2:]).split(".")[0]
            return sqlite3.connect(a["dbFile"])
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
            if innsert != "":
                try:
                    # print(innsert)
                    cursor.execute(innsert)
                    con.commit()
                    return True
                except BaseException as e:
                    # print(e)
                    # print(innsert)
                    pass
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
            cursor.execute(update)
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
            show = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
            cursor.execute(show)
            return cursor.fetchall()
        def show_field_f(self,cursor,con,q,r):
            ex = list(filter(None, q.split(";")))
            show = "PRAGMA table_info("+ex[0]+")"
            cursor.execute(show)
            return cursor.fetchall()
        def show_coll_f(self,cursor,con,q,r):
            ex = list(filter(None, q.split(";")))
            names = None
            for i in ex:
                show = "SELECT * FROM `"+str(i)+"`"
                cursor.execute(show)
                names = tuple(description[0] for description in cursor.description)
            return names
        def create_f(self,cursor,con,q,r):
            ex = [list(filter(None, e.split("=>"))) for e in list(filter(None, q.split(";")))]
            data_table = ("n","dt","nu","de","k","au","co")
            result = ''
            for e in ex:
                if len(e) > 1:
                    tab = e[0]
                    params = None
                    col = ""
                    if len(e) > 2:
                        ps = list(filter(None, e[1].split(":"))) if len(e) == 3 else []
                        # params = {ps[p*2]:ps[(p*2)+1] for p in range(len(ps)-1)} if len(ps) > 0 else None
                        params = " ".join([f"{ps[p*2]}={ps[(p*2)+1]}" for p in range(len(ps)-1)]) if len(ps) > 0 else None
                        ps = [[list(filter(None, i.split("|"))) for i in list(filter(None, j.split("@")))] for j in list(filter(None, e[2].split(",")))]
                    else:
                        ps = [[list(filter(None, i.split("|"))) for i in list(filter(None, j.split("@")))] for j in list(filter(None, e[1].split(",")))]
                    # col = [{t[0]:t[1] for t in p if t[0] in data_table} for p in ps]
                    col = ", ".join([" ".join([t[1] for t in p if t[0] in data_table]) for p in ps])
                    result += f'CREATE TABLE {tab} ({parser(col)}) {params if params != None else ""};'
            if result.replace(" ", "") != '':
                cursor.execute(result)
                con.commit()
                return True
            return False
        def alter_f(self,cursor,con,q,r):
            pass



    except BaseException as e:
        self.error = True
        self.errorMSG.append(e)
