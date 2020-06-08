# -*- coding: utf-8 -*-
# @Author: chenym
# @Email:   254906610@qq.com
# @Date:   2020-05-27 08:57:09
# @Last Modified by:   chenym
# @Last Modified time: 2020-06-05 08:27:08
# 获取个人签到信息
import datetime
import re
import time
from   WebTool import Webtools
from   LogTool import Logger
class SignInfo():
    def __init__(self):
        self.webTool = Webtools()
        self.log = Logger('all.log',level='info')
        #页面隐藏token值，提交请求时需要带该上参数验证
    def set_csft(self,str):
        pattern =r'<input type="hidden" name="javax.faces.ViewState" id="javax.faces.ViewState" value="(.*?)" />'
        viewStateList = re.findall(pattern,str)
        for v_viewState in viewStateList:
            return v_viewState
    def login(self,queryUser):
        postData = {
                     "loginform:staffId": "chenyimin2"
                    ,"loginform:password": "password"
                    ,"loginform_SUBMIT": "1"
                    ,"loginform:_link_hidden_": ""
                    ,"loginform:_idcl": "loginform:loginBtn"
                 }
        postData.update(queryUser)
        logInfo_url = "http://11.33.186.42:8008/signInfo/faces/login.jsp"
        #页面隐藏token值，提交请求时需要带该上参数验证
        result = self.webTool.web_Get(logInfo_url).text
        postData["javax.faces.ViewState"] = SignInfo().set_csft(result)
        #打印登录参数
        response = self.webTool.web_Post(logInfo_url,postData)
        info_url = "http://11.33.186.42:8008/signInfo/faces/top.jsp"
        response = self.webTool.web_Get(info_url).text
        pattern = r'<td height="20" valign="bottom"><span class="STYLE1">(.*?)</span></td>'
        user_info =  re.findall(pattern,response)
        for v_user in user_info:
            user = v_user.replace('&nbsp;','',5)
            print(user.replace('&nbsp;','\n',1))
        #self.log.LogDebug(response.text)
        postData = {}
        signInfo_url = 'http://11.33.186.42:8008/signInfo/faces/check/person_detail.jsp'
        postData["form1:startdate"] = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        postData["form1:enddate"] = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        postData["form1:look_detail"] = "查  询"
        postData["form1:_idJsp42"] = "1"
        postData["form1_SUBMIT"] = "1"
        postData["form1:_link_hidden_"] = ""
        postData["form1:_idcl"] = ""
        result = self.webTool.web_Get(signInfo_url).text
        pattern =r'<input type="hidden" name="javax.faces.ViewState" id="javax.faces.ViewState" value="(.*?)" />'
        viewStateList = re.findall(pattern,result)
        for v_viewState in viewStateList:
            postData["javax.faces.ViewState"] = v_viewState
        response = self.webTool.web_Post(signInfo_url,postData).text
        pattern = r'<tbody id="form1:_idJsp0:tbody_element">[\d\D]*</tbody>'
        rslt = re.findall(pattern,response)
        List =[]
        for line in rslt:
            pattern1 = r'<tr><td class="wai_b">.*?</td></tr>'
            v_trList =  re.findall(pattern1,line)
            i = 0
            for v_tr in  v_trList:
                data_tr = [i]
                pattern1 = r'<td class="wai_(c|b)">(.*?)</td>'
                for v_td in re.findall(pattern1,v_tr):
                    data_tr.append(v_td[1].replace('&nbsp;','')) #取出第二个匹配结果，第一个匹配结果是C或B，第二个匹配结果才是所需要的
                i = int(i)+1
                List.append(data_tr)
            return List
if __name__ == '__main__':
    sigInf = SignInfo()
    UserList = [["chenyimin2","password"],["lishaoqing","password"]]
    for var in UserList:
        queryUser = {
                     "loginform:staffId": var[0]
                    ,"loginform:password": var[1]
                     }
        #print(sigInf.login(queryUser))
        for var in sigInf.login(queryUser):
            print(var)