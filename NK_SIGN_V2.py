# -*- coding: utf-8 -*-
# @Author: chenym
# @Date:   2020-08-03 09:43:14
# @Last Modified by:   chenym
# @Last Modified time: 2020-08-03 11:24:35
import datetime
import re
import time
from  CYM_TOOLS.WebTool import Webtools
from  CYM_TOOLS.MapTool import Maptools
from  CYM_TOOLS.UnvsTool import Unvstools
from  CYM_TOOLS.DataBaseTool import DataBaseTools
class NK_SIGN_V2():
    HEADERS_DATA = {
        'User-Agent':r'Mozilla'
        ,'Connection':'keep-alive'
        }
    FILE = "NorthKingUser.ini"
    ADDR = '观日路38号'
    def __init__(self):
        self.maptool = Maptools('4d7e070d9ca8a48f2894c852eed08f74',150)
        self.unvstool = Unvstools()
        self.webtool = Webtools()

    def login(self,post_data):
        login_url = 'http://pm2019.i.northking.net:8011/pm2019/login_login'
        print(self.webtool.web_Post(login_url,post_data).text)
    def login(self,post_data):
        login_url = 'http://pm2019.i.northking.net:8011/pm2019/login_login'
        print(self.webtool.web_Post(login_url,post_data).text)
if __name__ == '__main__':
    user_info = {
        'loginName':'yimin.chen'
        ,'loginPassword':'carry123A@'
        ,'tm':'2020-08-03'
        ,'platform':'android'
        ,'KEYDATA':'mobile'
    }
    nk = NK_SIGN_V2()
    nk.login(user_info)
