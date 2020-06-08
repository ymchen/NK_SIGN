# -*- coding: utf-8 -*-
# @Author: chenym
# @Email:   254906610@qq.com
# @Date:   2019-12-16 15:40:40
# @Last Modified by:   chenym
# @Last Modified time: 2020-06-05 14:24:22

import pymysql

class DataBaseTools():
    def __init__(self):
        #self.con = pymysql.connect("49.235.122.74","carry","carry","krcdb")
        self.con = pymysql.connect("localhost", "root", "root", "qqdb")
        self.cursor = self.con.cursor()
    def query(self,sql):
        print("[Qurey_Sql Info]："+sql)
        try:
            self.cursor.execute(sql)
            self.con.commit()
            data = list(self.cursor.fetchall())
            return data
        except:
            self.con.rollback()
            self.cursor.close()
    def Ins(self,sql):
        connection = self.con
        cursor = self.cursor
        print("[Insert_Sql Info]："+sql)
        rowcount = 0
        cursor.execute(sql)
        rowcount = cursor.rowcount
        connection.commit()
        return rowcount
    def DeleteSql(self,sql):
        print("[DeleteSql Info]："+sql)
        try:
            self.cursor.execute(sql)
            rowcount = self.cursor.rowcount
            self.con.commit()
            return rowcount
        except:
            self.con.rollback()
            self.cursor.close()
    def get_InsertSql(self,List):
        dataTuple = tuple(List)
        dataStr = str(dataTuple)
        colList = []
        for v_col in range(1,len(List)+1):
            colList.append("col"+str(v_col))
        coldata = str(tuple(colList)).replace("'",'')
        v_Intsql = "Insert into  kaoqin  "+coldata+" values "+dataStr+";"
        return  v_Intsql
if __name__ == '__main__':
    db = DataBaseTools()
    alist = ["chenyimin2","password"]
    print(db.get_InsertSql(alist))
    print(db.DeleteSql(" truncate table  kaoqin; "));
    print(db.query("select * from kaoqin limit 11"));

# select date(rec_crt_dt1)  from kaoqin  where  date(rec_crt_dt1) = date('2020-06-05')