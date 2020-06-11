# -*- coding: utf-8 -*-
# @Author: chenym
# @Email:	254906610@qq.com
# @Date:   2020-06-04 14:39:31
# @Last Modified by:   chenym
# @Last Modified time: 2020-06-11 17:15:42
import datetime
import re
import time
from  CYM_TOOLS.WebTool import Webtools
from  CYM_TOOLS.MapTool import Maptools
from  CYM_TOOLS.UnvsTool import Unvstools
from  CYM_TOOLS.DataBaseTool import DataBaseTools
unvstool = Unvstools()
maptool = Maptools('4d7e070d9ca8a48f2894c852eed08f74',600)
webtool = Webtools()
db = DataBaseTools()
month = unvstool.getCurMon()
punchCardDate = unvstool.getCurDate()
file = "NorthKingUser.ini"
sign_url = 'http://111.203.253.37:8201/nkcisp/mobile-base.action?to=cispInsertPunchCardInfoAction'
post_data = {
     'endTime':'17:30'
    ,'flag':'1'
    ,'groupId':'1'
    ,'to':'cispInsertPunchCardInfoAction'
    }
cf = unvstool.getDataFromFile(file)
addr = '观日路38号'
def signMonRep(user_name):

    logon_url = 'http://111.203.253.37:8201/nkcisp/mobile-base.action?employeeId='+user_name+'&month='+month+'&to=cispQueryAttendanceByEmployeeAction'
    logon_info = webtool.web_Get(logon_url).text
    logon_json = unvstool.toJson(logon_info)
    employeeInfos = logon_json['RSP_BODY']['employeeInfos']
    return employeeInfos
def signRepNow(user_name):
    sign_info_list =[]
    i = 0
    logon_url = 'http://111.203.253.37:8201/nkcisp/mobile-base.action?employeeNo='+user_name+'&to=cispQueryEmployeeByProjectInfoAction'
    logon_info = webtool.web_Get(logon_url).text
    logon_json = unvstool.toJson(logon_info)
    employeeName = logon_json['RSP_BODY']['projectList'][0]['employeeName']
    projectNo = logon_json['RSP_BODY']['projectList'][0]['projectNo']
    logon_url = 'http://111.203.253.37:8201/nkcisp/mobile-base.action?employeeId='+user_name+'&projectNo='+projectNo+'&punchCardDate='+punchCardDate+'&to=cispQueryNormalCardListAction'
    logon_info = webtool.web_Get(logon_url).text
    logon_json = unvstool.toJson(logon_info)
    employeeId = logon_json['RSP_BODY']['employeeId']
    cardList = logon_json['RSP_BODY']['cardList']
    for var_rec in cardList:
        var_list  = [i]
        var_list.append(employeeId)
        var_list.append(employeeName)
        var_list.append(punchCardDate)
        var_list.append(var_rec['punchCardTime'])
        var_list.append(var_rec['punchPlace'])
        i = i+1
        sign_info_list.append(var_list)
    return sign_info_list
def sign(user_name):
    logon_url = 'http://111.203.253.37:8201/nkcisp/mobile-base.action?employeeNo='+user_name+'&to=cispQueryEmployeeByProjectInfoAction'
    logon_info = webtool.web_Get(logon_url).text
    logon_json = unvstool.toJson(logon_info)
    print(logon_json)
    addList =  maptool.getDestLocatInfo(addr)
    # 获取项目编号
    projectNo = logon_json['RSP_BODY']['projectList'][0]['projectNo']
    groupNo = logon_json['RSP_BODY']['projectList'][0]['groupNo']
    employeeName = logon_json['RSP_BODY']['projectList'][0]['employeeName']
    punchPlace = addList[1]
    itudeList = addList[0]
    itudeArr = itudeList.split(",")
    longitude = itudeArr[0]
    latitude = itudeArr[1]
    loginName = user_name
    queryData = {
         'loginName':user_name
        ,'projectNo':projectNo
        ,'place':punchPlace
        ,'longitude':longitude
        ,'latitude':latitude
        ,'groupId':groupNo
        ,'name':employeeName
    }
    post_data.update(queryData)
    print(webtool.web_Post(sign_url,post_data).text)

userList = unvstool.getDataKeyValue('NorthingList',"userList")
userArr = userList.split(",")
# 循环处理身份信息
delSql = "Delete from nk_sign_log  where  date(rec_crt_tm) = date('"+punchCardDate+"')"
print(db.DeleteSql(delSql));
for var_user in userArr:
    # 打卡
    sign(var_user)
    # 查看当月打卡情况    
    #print(signMonRep(var_user))
    # 查看当天打卡情况
    #print(var_user)
    for var_rec in signRepNow(var_user):
        Insql = db.get_InsertSql("nk_sign_log",var_rec)
        print(db.Ins(Insql))
    #print(db.query("select * from nk_sign_d_info limit 11"));