# -*- coding: utf-8 -*-
# @Author: chenym
# @Email:   254906610@qq.com
# @Date:   2019-10-10 14:14:10
# @Last Modified by:   chenym
# @Last Modified time: 2020-06-04 16:56:48
import time
import json
import configparser
class Unvstools():
    def __init__(self):
        self.cf =  configparser.ConfigParser()
    def getTime(self):
        return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    def getCurDate(self):
        return time.strftime('%Y-%m-%d',time.localtime(time.time()))
    def getCurMon(self):
        return time.strftime('%Y%m',time.localtime(time.time()))    
    def toJson(self,str1):
        jsonStr = json.loads(str1)
        return jsonStr
    def getDataFromFile(self,filename):
        self.cf.read(filename)
        sec =  self.cf.sections()
        return self.cf
    def getDataKeyValue(self,section,key):
        value =  self.cf.get(section,key).strip()
        return value

# if __name__ == '__main__':
#     log = Logger('all.log',level='debug')
#     unvstool = Unvstools()
#     File = "E:/SMS/NorthKingUser.ini"

#     cf = unvstool.getDataFromFile(File)
#     userInfos = unvstool.getDataKeyValue('NorthingList',"userList")
#     log.LogInfo(userInfos)
