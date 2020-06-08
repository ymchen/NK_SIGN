# -*- coding: utf-8 -*-
# @Author: chenym
# @Email:   254906610@qq.com
# @Date:   2019-10-10 10:51:10
# @Last Modified by:   chenym
# @Last Modified time: 2019-10-10 11:19:50
import re
from LogTool import Logger
from WebTool import Webtools
log = Logger('all.log',level='info')
webtool = Webtools()
user_name = 'juntao.duan'
logon_url = 'http://oa.northking.net/login/VerifyLogin.jsp'
cookies_data = webtool.web_Cookies(logon_url)
post_data = {
            'loginid':"yimin.chen"
            ,'userpassword':"carry123A@"
            ,'logintype':"1"
            ,'loginfile':"/wui/theme/ecology7/page/login.jsp?templateId=3&logintype=1&gopage="
            }
log.LogInfo(cookies_data)
post_url = 'http://oa.northking.net/login/VerifyLogin.jsp'
response_text = webtool.web_Post(post_url,post_data,cookies_data).text
log.LogDebug(response_text)

url = "http://oa.northking.net/hrm/search/HrmResourceSearchResult.jsp?from="
response_text = webtool.web_Get(url).text

pattern =r"weaver.common.util.taglib.SplitPageXmlServlet',0,'','(.*?)','run',"
v_list = re.findall(pattern,response_text)
log.LogInfo(str(v_list))

post_data_query = {
                    'tableString':v_list[0]
                    ,'pageIndex':""
                    ,'orderBy':""
                    ,'otype':""
                    ,'mode':"run"
                    ,'selectedstrs':""
                    }
post_data.update(post_data_query)
log.LogInfo(str(post_data))
post_url = r'http://oa.northking.net/weaver/weaver.common.util.taglib.SplitPageXmlServlet'
response_text = webtool.web_Post(post_url,post_data,cookies_data).text
log.LogInfo(response_text)