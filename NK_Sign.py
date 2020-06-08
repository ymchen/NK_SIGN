# -*- coding: utf-8 -*-
# @Author: chenym
# @Date:   2019-12-16 10:10:13
# @Last Modified by:   chenym
# @Last Modified time: 2020-06-05 17:30:07
import requests
import time
import datetime
import json
import configparser
import random
import urllib3
import logging
from logging import handlers
urllib3.disable_warnings()
#===================================20191009modify=========================
class Logger(object):
    level_relations = {
        'debug':logging.DEBUG,
        'info':logging.INFO,
        'warning':logging.WARNING,
        'error':logging.ERROR,
        'crit':logging.CRITICAL
    }#日志级别关系映射

    def __init__(self,filename,level='info',when='H',backCount=5,fmt='%(asctime)s - %(levelname)s: %(message)s'):
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)#设置日志格式
        self.logger.setLevel(self.level_relations.get(level))#设置日志级别
        sh = logging.StreamHandler()#往屏幕上输出
        sh.setFormatter(format_str) #设置屏幕上显示的格式
        th = handlers.TimedRotatingFileHandler(filename=filename,when=when,backupCount=backCount,encoding='utf-8')#往文件里写入#指定间隔时间自动生成文件的处理器
        #实例化TimedRotatingFileHandler
        #interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨
        th.setFormatter(format_str)#设置文件里写入的格式
        self.logger.addHandler(sh) #把对象加到logger里
        self.logger.addHandler(th)
    def LogFile(self,type,str):
        if type == 10 :
            self.logger.debug(str)
        elif type == 20 :
            self.logger.info(str)
        elif type == 30 :
            self.logger.warning(str)
        elif type == 40 :
            self.logger.error(str)
        elif type == 50 :
            self.logger.critical(str)
#===================================20191009modify=========================
class webtools():
    LOGFILE = Logger('NorthSign.log',level='debug')
    PROC_TIME = datetime.datetime.now()
    SESSION = requests.Session()
    #存储配置文件读取参数数据
    IniContext = {}
    POST_DATA = {
         'endTime':'17:30'
        ,'flag':'1'
        ,'groupId':'1'
        ,'latitude':'24.484215'
        ,'loginName':'yimin.chen'
        ,'longitude':'118.186415'
        ,'name':'陈艺敏'
        ,'place':'福建省厦门市思明区莲前街道中国建设银行(厦门科技支行)厦门市软件园(前埔东路)'
        ,'projectNo':'RD-17-1022-D47-01'
        ,'startTime':'09:00'
        ,'to':'cispInsertPunchCardInfoAction'
        }
    COOKIES = {}
    HEADERS_DATA = {
            'User-Agent':r'Mozilla'
            ,'Connection':'keep-alive'
        }
    def toJson(str1):
        jsonStr = json.loads(str1)
        return jsonStr
    def getTime():
        return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    def web_Get(url):
        result = webtools.SESSION.get(url = url,headers = webtools.HEADERS_DATA,verify=False)
        return result
    def web_Post(url):
        result = webtools.SESSION.post(url = url,headers = webtools.HEADERS_DATA,cookies =  webtools.COOKIES,data = webtools.POST_DATA, timeout = 10)
        return result
    def getUseinfo(user_name):
        logon_url = 'http://111.203.253.37:8201/nkcisp/mobile-base.action?employeeNo='+user_name+'&to=cispQueryEmployeeByProjectInfoAction'
        # 获取登录信息
        logon_info = webtools.web_Get(logon_url).text
        webtools.LOGFILE.LogFile(20,"登录相关信息-LogonINFO:"+logon_info)
        # 转JSON格式
        logon_json = webtools.toJson(logon_info)
        # 获取项目编号
        projectNo = logon_json['RSP_BODY']['projectList'][0]['projectNo']
        groupNo = logon_json['RSP_BODY']['projectList'][0]['groupNo']
        employeeName = logon_json['RSP_BODY']['projectList'][0]['employeeName']
        addList = webtools.getDestLocatInfo()
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
        return queryData

    def getDataFromIni():
        iniFile = "NorthKingUser.ini"
        cf = configparser.ConfigParser()
        cf.read(iniFile)
        webtools.IniContext["userList"] = cf.get('NorthingList',"userList").strip()   # strip去空格\n\r\t lstrip 左边空格 rstrip 右边空格

    #==============新增高德获取地址信息=====20191008modify=======
    # 根据地址获取经纬度
    def getLocation(key,addr):
        url = 'https://restapi.amap.com/v3/geocode/geo?key='+key+'&address='+addr
        respon = webtools.web_Get(url).text
        return respon
    # 根据经纬度获取详细单一地址
    def getAddr(key,locat):
        url = 'https://restapi.amap.com/v3/geocode/regeo?key='+key+'&location='+locat
        respon = webtools.web_Get(url).text
        return respon
    # 根据经纬度获取半径100内的所有建筑信息
    def getAddrList(key,locat,r=100):
        url = 'https://restapi.amap.com/v3/geocode/regeo?key='+key+'&location='+locat+'&radius='+str(r)+'&extensions=all'
        respon = webtools.web_Get(url).text
        return respon
    def getDestLocatInfo():
        key = '4d7e070d9ca8a48f2894c852eed08f74'
        addr = '福建省厦门市思明区观日路38号'
        locat_info = webtools.getLocation(key,addr)
        # 转JSON格式
        locat_json = webtools.toJson(locat_info)
        # 获取经纬度
        location = locat_json['geocodes'][0]['location']
        #print("1.获取经纬度-"+addr+':'+location)
        # 获取半径是50米以内所有建筑物信息
        r = 500
        addr_info = webtools.getAddrList(key,location,r)
        # 转JSON格式
        addr_json = webtools.toJson(addr_info)
        address = addr_json['regeocode']['pois']
        webtools.LOGFILE.LogFile(20,"1.获取经纬度-"+addr+':'+location)
        #print("1.获取经纬度-"+addr+':'+location)
        # 附近建筑物个数
        total = len(address)
        #print("2.获取-"+str(r)+"米以内建筑物总数："+str(total))
        webtools.LOGFILE.LogFile(20,"2.获取-"+str(r)+"米以内建筑物总数："+str(total))
        # 取出经纬度与建筑物信息
        #print("3.获取-"+str(r)+"米以内所有建筑物信息")
        webtools.LOGFILE.LogFile(20,"3.获取-"+str(r)+"米以内所有建筑物信息")
        for v_addr in address:
            #print("    "+v_addr['location'] +':'+v_addr['name'])
            webtools.LOGFILE.LogFile(20,v_addr['location'] +':'+v_addr['name'])
        # 随机取一条信息
        locat_index = random.randint(0,total-1)
        tar_locat = address[locat_index]['location']
        tar_addr = address[locat_index]['name']
        #print("4.随机获取第"+str(locat_index+1)+"条信息-"+tar_locat +':'+tar_addr)
        webtools.LOGFILE.LogFile(20,"4.随机获取第"+str(locat_index+1)+"条信息-"+tar_locat +':'+tar_addr)
        # 取详细的信息
        tar_addr_info = webtools.getAddr(key,tar_locat)
        # 转JSON格式
        tar_addr_json = webtools.toJson(tar_addr_info)
        tar_addr_locat = tar_addr_json['regeocode']['addressComponent']['streetNumber']['location']
        tar_addr_name = tar_addr_json['regeocode']['formatted_address']
        tar_address = [tar_addr_locat,tar_addr_name]
        #print("5.获取-"+str(r)+"米以内随机建筑物信息"+str(tar_address))
        webtools.LOGFILE.LogFile(20,"5.获取-"+str(r)+"米以内随机建筑物信息")
        webtools.LOGFILE.LogFile(20,str(tar_address))
        return tar_address
    #=========================================================
    def do_sign():
        sign_url = 'http://111.203.253.37:8201/nkcisp/mobile-base.action?to=cispInsertPunchCardInfoAction'
        webtools.getDataFromIni()
        #所有身份信息
        userList =  webtools.IniContext["userList"]
        # 按，分割后成新数组
        userArr = userList.split(",")
        # 循环处理身份信息
        for var_user in userArr:
            # 获取个人项目信息
            queryInfo = webtools.getUseinfo(var_user)
            # 更新传输参数
            webtools.POST_DATA.update(queryInfo)
            #print(webtools.web_Post(sign_url).text)
            webtools.LOGFILE.LogFile(20,webtools.web_Post(sign_url).text)
    def setCookies(url):
        res = webtools.web_Get(url)
        webtools.COOKIES =  requests.utils.dict_from_cookiejar(res.cookies)
if __name__ == '__main__':
    print("=====================================")
    print("============="+webtools.getTime()+"==============")
    webtools.do_sign()
    #print(webtools.getCommand())
    #webtools.getUseinfo("yimin.chen")
    print("=====================================")

#e:
#cd E:\SMS
#pyinstaller -F E:\SMS\North_log_v1.py  -n northking
#--icon=HaHaBundle.ico