# -*- coding: utf-8 -*-
# @Author: chenym
# @Email:   254906610@qq.com
# @Date:   2019-10-10 10:09:58
# @Last Modified by:   chenym
# @Last Modified time: 2020-08-03 11:07:07
import requests
import datetime
class Webtools():
    headers_data = {
        'User-Agent':r'Mozilla'
        ,'Connection':'keep-alive'
        ,'CID':'ab2250acfe517c6ef7489702834142dd'
        }
    def __init__(self):
        self.session = requests.Session()
        self.current_time = datetime.datetime.now()
    def web_Get(self,url):
        result = self.session.get(url = url,headers = self.headers_data,verify=False)
        return result
    def web_Post(self,url,post_data,cookies_data={}):
        result = self.session.post(url = url,headers = self.headers_data,cookies =  cookies_data,data = post_data, timeout = 10)
        return result
    def web_Cookies(self,url):
        cookies = self.web_Get(url).cookies
        result = requests.utils.dict_from_cookiejar(cookies)
        return result
# if __name__ == '__main__':
#     log = LogTool.Logger()
#     webtool = Webtools()
#     user_name = 'yimin.chen'
#     logon_url = 'http://111.203.253.37:8201/nkcisp/mobile-base.action?employeeNo='+user_name+'&to=cispQueryEmployeeByProjectInfoAction'
#     respon_text = webtool.web_Get(logon_url).text
#     log.LogDebug(respon_text)
#     mapdata = {
#          'endTime':'17:30'
#         ,'flag':'1'
#         ,'groupId':'1'
#         ,'latitude':'24.484215'
#         ,'loginName':'yimin.chen'
#         ,'longitude':'118.186415'
#         ,'name':'陈艺敏'
#         ,'place':'福建省厦门市思明区莲前街道中国建设银行(厦门科技支行)厦门市软件园(前埔东路)'
#         ,'projectNo':'RD-17-1022-D47-01'
#         ,'startTime':'09:00'
#         ,'to':'cispInsertPunchCardInfoAction'
#         }
#     sign_url = 'http://111.203.253.37:8201/nkcisp/mobile-base.action'
#     print(webtool.web_Post(sign_url,mapdata).text)