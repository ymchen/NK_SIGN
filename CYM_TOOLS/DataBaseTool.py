# -*- coding: utf-8 -*-
# @Author: chenym
# @Email:   254906610@qq.com
# @Date:   2019-12-16 15:40:40
# @Last Modified by:   chenym
# @Last Modified time: 2020-06-12 20:30:51

import pymysql

class DataBaseTools():
    def __init__(self):
        self.con = pymysql.connect("49.235.122.74","carry","carry","krcdb")
        #self.con = pymysql.connect("localhost", "root", "root", "ccbsign")
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
    def Ins(self,sql):
        print("[Insert_Sql Info]："+sql)
        rowcount = 0
        try:
            self.cursor.execute(sql)
            rowcount = self.cursor.rowcount
            self.con.commit()
            return rowcount
        except:
            self.con.rollback()
    def DeleteSql(self,sql):
        print("[DeleteSql Info]："+sql)
        try:
            self.cursor.execute(sql)
            rowcount = self.cursor.rowcount
            self.con.commit()
            return rowcount
        except:
            self.con.rollback()
    def ExecSql(self,sql):
        print("[Exec Info]："+sql)
        try:
            self.cursor.execute(sql)
            rowcount = self.cursor.rowcount
            self.con.commit()
            return rowcount
        except:
            self.con.rollback()
    def Unconn(self):
        self.cursor.close();
        self.con.close();
        print("[Unconn Info]："+"释放数据库链接。")
    def get_InsertSql(self,tableNm,List):
        dataTuple = tuple(List)
        dataStr = str(dataTuple)
        colList = []
        for v_col in range(1,len(List)+1):
            colList.append("col"+str(v_col))
        coldata = str(tuple(colList)).replace("'",'')
        v_Intsql = "Insert into  "+tableNm+coldata+" values "+dataStr+";"
        return  v_Intsql
if __name__ == '__main__':
    db = DataBaseTools()
    alist = ["chenyimin2","password"]
    print(db.get_InsertSql("nk_sign_d_info",alist))
    print(db.Ins(db.get_InsertSql("nk_sign_d_info",alist)))
    #print(db.DeleteSql(" truncate table  nk_sign_d_info; "));
    #print(db.query("select * from nk_sign_d_info limit 11"));

# select date(rec_crt_dt1)  from kaoqin  where  date(rec_crt_dt1) = date('2020-06-05')